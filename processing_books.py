## Cleaning book data
import pandas as pd
import textblob as tb
import re
from wordnik import *
import urllib2
from unidecode import unidecode
from textstat.textstat import textstat
import pickle

apiUrl = 'http://api.wordnik.com/v4'
apiKey = '21eadfda10890c9c9200b0e672503c34c23ada14b03d86121'
client = swagger.ApiClient(apiKey, apiUrl)
wordApi = WordApi.WordApi(client)

# Imports munged copy of The Sun Also Rises saved by cleaning_books.py script
filepath = '/Users/grantnelson/Desktop/Data_Science/sfdat22_project/books/Hemingway/the_sun_also_rises_cleaned.txt'

f = open(filepath)
txt = f.read()
f.close()

# Defining blocks from raw text
def make_text_blocks(txt):
	"""
	Takes in text and returns a list of consecutive blocks of 1700 words
	"""
	blocks = []
	whitespace_count = 0
	prev_stop = 0
	for idx, val in enumerate(txt):
		if val == ' ':
			whitespace_count += 1
		if whitespace_count == 1700:
			blocks.append(txt[prev_stop:idx])
		 	prev_stop = idx
		 	whitespace_count = 0
	return blocks

bl = make_text_blocks(txt)

blocks = []
for b in bl:
	dc = unidecode(unicode(b, encoding = "utf-8"))
	blocks.append(dc)


### FEATURE DEFINITION

# Some features will be at the word level, others will be at the sentence or
# block level. For each level, define a separate dataframe containing data from
# a block at that level and begin defining features, i.e. each row in dataframe
# is a word/sentence/block and each column is a feature. Word- and
# sentence-level features then need to be aggregated to block-level to be used
# in analysis.

def make_frames(blocks, level):
	"""
	Takes in a list of n text blocks and returns a list of n dataframes with
	information from each text block at the level specified in the 'level'
	parameter. Each dataframe returned has one column that contains a row for
	each observation in the corresponding text block at the given level.

	blocks: list of strings encoded in utf-8
	level: str equal to either 'word', 'sentence', or 'block'

	returns: list of dataframes
	"""
	assert level in ('word', 'sentence', 'block'), \
	'level parameter must be one of: \'word\', \'sentence\', \'block\''
	
	if level == 'block':
		return pd.DataFrame(blocks, columns = ['block',])
	else:
		frames = []
		for b in blocks:
			blob = tb.TextBlob(b.decode('utf-8','ignore'))
			if level == 'sentence':
				sentences = [str(i) for i in blob.sentences]
				frames.append(pd.DataFrame(sentences, columns = ['sentence']))
			else:
				words = list(blob.words)
				frames.append(pd.DataFrame(words, columns = ['word']))
		return frames

# Word-level features: length of word, number of syllables, year of most common
# usage, country of origin, scrabble score, function words

def get_lemma(word):
	if word in ('is','us','was','as','its'):
		return word
	return str(tb.TextBlob(word).words.lemmatize()[0])

syllable_dict = {}

def get_syllables(word):
	"""
	Takes in a word and returns the number of syllables in that word as an int.
	Data on syllables obtained through the Wordnik API
	"""
	if word not in syllable_dict:
		try: syllables = wordApi.getHyphenation(word)
		except UnicodeEncodeError:
			syllable_dict[word] = 0
		if not syllables:
			syllables = wordApi.getHyphenation(word.lower())
			if not syllables:
				syllables = wordApi.getHyphenation(word.capitalize())
				if not syllables:
					syllable_dict[word] = 0
					return syllable_dict[word]
		syllable_dict[word] = len(syllables)
	return syllable_dict[word]

frequency_dict = {}

def get_max_frequency_year(word):
	"""
	Takes in a word and uses the Wordnik API to return the year between 1800
	and the present in which that word was most commonly used as an int.
	"""
	if word not in frequency_dict:
		if '\'' in word:
			frequency_dict[word] = 0
			return frequency_dict[word]
		else:
			try:
				freq = wordApi.getWordFrequency(word)
			except urllib2.HTTPError:
				try:
					freq = wordApi.getWordFrequency(word.lower())
				except urllib2.HTTPError:
					frequency_dict[word] = 0
					return frequency_dict[word]
		if not freq or len(freq.frequency) == 0:
			frequency_dict[word] = 0
		else:
			year_counts = {}
			for i in freq.frequency:
				year_counts[i.year] = i.count
			frequency_dict[word] = sorted(year_counts, key = year_counts.get, reverse = True)[0]
	return frequency_dict[word]

def get_etymology(word):
	"""
	Takes in a word and uses the Wordnik API to return the language from which
	that word orginiated as a string.
	"""
	### FIGURE OUT HOW TO PARSE WORDNIK ETYMOLOGY OBJECT RETURNED BY API
	pass

scrabble_dict = {}

def get_scrabble_score(word):
	"""
	Takes in a word and uses the Wordnik API to return the number of points
	that word is worth in a Scrabble game as an int.
	"""
	if word not in scrabble_dict:
		try:
			scrabble = wordApi.getScrabbleScore(word.lower())
			scrabble_dict[word] = scrabble.value
		except urllib2.HTTPError:
			scrabble_dict[word] = 0
	return scrabble_dict[word]
	
def make_function_word_cols(df):
	"""
	Takes in a word-level dataframe and returns a dataframe with a column added
	for each function word. Each new column is a boolean indicating whether the
	word in the 'word' column at that row is equal to the funciton word
	specified in the column name.
	"""
	function_words = ['a', 'been', 'all', 'but', 'also', 'by', 'an', 'can',
					  'and','do', 'any', 'down', 'are', 'even', 'had', 'its',
					  'one','has', 'may', 'only', 'have', 'more', 'or', 'her',
					  'must','our', 'his', 'my', 'should', 'if', 'no', 'so',
					  'as', 'at','be', 'in', 'not', 'some', 'every', 'into',
					  'now', 'such','for', 'is', 'of', 'than', 'the', 'were',
					  'their', 'what','then', 'when', 'there', 'which', 'things',
					  'who', 'this','will', 'to', 'with', 'up', 'would', 'upon',
					  'you', 'from','it', 'on', 'that', 'was']
	fw_cols = {}
	for fw in function_words:
		values = df['lemma'] == fw
		fw_cols[fw] = values
	data = pd.DataFrame.from_dict(fw_cols)
	merged = pd.merge(df, data, left_index = True, right_index = True)
	return merged

print 'functions defined'

word_frames = make_frames(blocks, level = 'word')

print 'word_frames made'

def process_word_frame(df):
	df['length'] = df.word.map(len)
	print 'len done'
	df['lemma'] = df.word.map(get_lemma)
	print 'lemma done'
	df['syllable_count'] = df.lemma.map(get_syllables)
	print 'syllables done'
	df['most_frequent_year'] = df.lemma.map(get_max_frequency_year)
	print 'most frequent year done'
	df['scrabble_score'] = df.lemma.map(get_scrabble_score)
	print 'scrabble score done'
	df = make_function_word_cols(df)
	print 'function word columns done'
	return df



# Once columns have all been created, figure out what aggregation is meaningful
# E.g. for word length could be mean length, pct of words over 10 letters, etc.

### TO DO

# Sentence-level features: number of words, number of clauses, use of punctuation,
# sentiment

sentence_frames = make_frames(txt, level = 'sentence')

def count_words(sentence):
	"""
	Takes in sentence as string and returns the number of words in that
	sentence as an int. Excludes words containing single quote, since TextBlob
	splits contractions and possesives into two words.
	"""
	blob = tb.TextBlob(sentence.decode('utf-8','ignore'))
	word_list = [w for w in blob.words if '\'' not in w]
	return len(word_list)

def get_sentiment(sentence):
	"""
	Takes in sentence as string and uses TextBlob to return the sentiment
	polarity of that sentence
	"""
	blob = tb.TextBlob(sentence.decode('utf-8','ignore'))
	return blob.sentiment[0]

def count_commas(sentence):
	c = [i for i in df.sentence if i == ',']
	return len(c)

def count_semicolons(sentence):
	c = [i for i in df.sentence if i == ';']
	return len(c)

def count_colons(sentence):
	c = [i for i in df.sentence if i == ':']
	return len(c)
 
def count_hyphens(sentence):
 	c = [i for i in df.sentence if i == '-']
	return len(c)

for df in sentence_frames:
	df['word_count'] = df.sentence.map(count_words)
	df['sentiment'] = df.sentence.map(get_sentiment)
	df['commas'] = df.sentence.map(count_commas)
	df['semicolons'] = df.sentence.map(count_semicolons)
	df['colons'] = df.sentence.map(count_colons)
	df['hyphens'] = df.sentence.map(count_hyphens)



# Block-level features: pct dialogue, gender ratio of names
# mentioned, location of places mentioned, lexical diversity

block_frame = make_frames(blocks, level = 'block')

def get_lexical_diversity(block):
	blob = tb.TextBlob(block.decode('utf-8','ignore'))
	return len(set(blob.words))/float(len(blob.words))

def get_grade_level(block):
	consensus = textstat.text_standard(block)
	return float(consensus[0]) + .5

def get_pct_dialogue(block):
	quote_lengths = []
	start = None
	end = None
	for idx, val in enumerate(block):
		if val == '"':
			if not start:
				start = idx
			else:
				end = idx
				quote_lengths.append(end - start)
				start = None
				end = None
	if start and not end:
		quote_lengths.append(len(block) - start)
	return sum(quote_lengths)/float(len(block))




block_frame['lexical_diversity'] = block_frame.block.map(get_lexical_diversity)
block_frame['grade_level'] = block_frame.block.map(get_grade_level)
block_frame['difficult_words'] = block_frame.block.map(textstat.difficult_words)
block_frame['pct_dialogue'] = block_frame.block.map(get_pct_dialogue)
