# Update dicts used in defining word-level features to store NaN when the
# Wordnik API cannot find the word, isntead of 0
import pandas as pd
import numpy as np 
import pickle

for d in ('syllable_dict', 'frequency_dict', 'scrabble_dict'):
	filepath = '/Users/grantnelson/desktop/data_science/sfdat22_project/' + d + '.txt'
	with open(filepath, 'rb') as f:
		temp_dict = pickle.load(f)
	for key, value in temp_dict.iteritems():
		if value == 0:
			temp_dict[key] = np.NaN
	writepath = filepath[:-4] + '_1.txt'
	with open(writepath, 'wb') as f:
		pickle.dump(temp_dict, f, protocol = 2)
	print d + ' updated'