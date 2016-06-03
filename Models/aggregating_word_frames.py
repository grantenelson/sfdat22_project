import pickle
import pandas as pd

with open('/Users/grantnelson/desktop/data_science/sfdat22_project/all_words_df.txt','rb') as f:
	all_words = pickle.load(f)

# Look only at words that are not function words
all_words_sub = all_words[all_words['function_word'] == 0]

# Group by author, work, and block
grouped = all_words_sub.groupby(['author','work','block'], as_index = False)

syllable_count = grouped.syllable_count.describe().reset_index()
syllable_count.drop(['count','min','max'], axis = 1, inplace = True)
rename_dict = {name : 'syllable_count_' + name for name in syllable_count.columns[3:]}
syllable_count.rename(columns = rename_dict, inplace = True)

most_freq_year = grouped.most_frequent_year.describe().reset_index()
most_freq_year.drop(['count','min','max'], axis = 1, inplace = True)
rename_dict = {name : 'most_freq_year_' + name for name in most_freq_year.columns[3:]}
most_freq_year.rename(columns = rename_dict, inplace = True)

length = grouped.length.mean()
length.rename(columns = {'mean':'length_mean'}, inplace = True)

scrabble = grouped.scrabble_score.agg(['mean','max']).reset_index()
scrabble.rename(columns = {'mean':'scrabble_score_mean', 'max':'scrabble_score_max'}, inplace = True)

agg_df = pd.merge(syllable_count, most_freq_year, on = ['author','work','block'])
agg_df = pd.merge(agg_df, length, on = ['author','work','block'])
agg_df = pd.merge(agg_df, scrabble, on = ['author','work','block'])