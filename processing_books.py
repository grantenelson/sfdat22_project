## Cleaning book data
import pandas as pd
import textblob as tb
import re
from wordnik import *

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

blocks = make_text_blocks(txt)

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

	frames = []
	for b in blocks:
		blob = tb.TextBlob(b.decode('utf-8','ignore'))
		if level == 'block':
			frames.append(pd.DataFrame(b, columns = ['block']))
		elif level == 'sentence':
			sentences = list(blob.sentences)
			frames.append(pd.DataFrame(sentences, columns = ['sentence']))
		else:
			words = list(blob.words)
			frames.append(pd.DataFrame(words, columns = ['word']))
	return frames

# Word-level features: length of word, number of syllables, year of most common
# usage, country of origin, scrabble score, function words

def get_syllables(word):
	"""
	Takes in a word and returns the number of syllables in that word as an int.
	Data on syllables obtained through the Wordnik API
	"""
	try: syllables = wordApi.getHyphenation(word)
	except UnicodeEncodeError:
		return 0
	if syllables is None:
		return 0
	return len(syllables)

def get_max_frequency_year(word):
	"""
	Takes in a word and uses the Wordnik API to return the year between 1800
	and the present in which that word was most commonly used as an int.
	"""
	if '\'' in word:
		return 0
	try:
		freq = wordApi.getWordFrequency(word)
	except UnicodeEncodeError:
		return 0
	if not freq:
		return 0
	year_counts = []
	for i in freq.frequency:
		year = i.year
		count = i.count
		year_counts.append((year,count))
	df = pd.DataFrame(year_counts, columns = ['year','count'])
	try: return df['year'].loc[df['count'].idxmax()]
	except ValueError:
		print word, '\n'
		raise

def get_etymology(word):
	"""
	Takes in a word and uses the Wordnik API to return the language from which
	that word orginiated as a string.
	"""
	### FIGURE OUT HOW TO PARSE WORDNIK ETYMOLOGY OBJECT RETURNED BY API
	pass

def get_scrabble_score(word):
	"""
	Takes in a word and uses the Wordnik API to return the number of points
	that word is worth in a Scrabble game as an int.
	"""
	scrabble = wordApi.getScrabbleScore(word)
	return scrabble.value

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
	fw_cols = []
	for fw in function_words:
		series = df['word'] == fw
		column = pd.Series(series, name = fw)
		fw_cols.append(column)
	data = pd.concat(fw_cols, axis = 1)
	merged = pd.merge(df, data, left_index = True, right_index = True)
	return merged


word_frames = make_frames(blocks, level = 'word')

# This block of code may break and through urllib2 HTTPError
counter = 0
for df in word_frames:
	df['lemma'] = df.word.map(lambda x: x.lemmatize())
	df['length'] = df.word.map(len)
	df['syllable_count'] = df.word.map(get_syllables)
	df['most_frequent_year'] = df.word.map(get_max_frequency_year)
	# df['scrabble_score'] = df.word.map(get_scrabble_score)
	df = make_function_word_cols(df)
	print 'Processed block number ', counter
	counter += 1

# Once columns have all been created, figure out what aggregation is meaningful
# E.g. for word length could be mean length, pct of words over 10 letters, etc.

### TO DO

# Sentence-level features: number of words, number of clauses, use of punctuation,
# sentiment

# sentence_frames = make_frames(txt, level = 'sentence')

# Block-level features: use of punctuation, pct dialogue, gender ratio of names
# mentioned, location of places mentioned, lexical diversity

#b lock_frames = make_frames(txt, level = 'block')
