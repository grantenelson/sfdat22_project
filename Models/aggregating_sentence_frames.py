import pickle
import pandas as pd

with open('/Users/grantnelson/desktop/data_science/sfdat22_project/all_sentences_df.txt','rb') as f:
	all_sentences = pickle.load(f)

# Group by author, work, and block
grouped = all_sentences.groupby(['author','work','block'], as_index = False)

word_count = grouped.word_count.describe().reset_index()
word_count.drop(['count','min','25%'], axis = 1, inplace = True)
rename_dict = {name : 'word_count_' + name for name in word_count.columns[3:]}
word_count.rename(columns = rename_dict, inplace = True)

sentiment = grouped.sentiment.mean()
sentiment.rename(columns = {'mean':'sentiment_mean'}, inplace = True)

punct = grouped['commas','semicolons','colons','hyphens'].mean()
rename_dict = {name : name + '_mean' for name in punct.columns[3:]}
punct.rename(columns = rename_dict, inplace = True)

total_punct = grouped.total_punct.agg(['mean','std']).reset_index()
total_punct.rename(columns = {'mean':'total_punct_mean', 'std':'total_punct_std'}, inplace = True)

agg_df = pd.merge(word_count, sentiment, on = ['author','work','block'])
agg_df = pd.merge(agg_df, punct, on = ['author','work','block'])
agg_df = pd.merge(agg_df, total_punct, on = ['author','work','block'])