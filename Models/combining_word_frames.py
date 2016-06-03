### Take word-level dataframes from individual books and combine them into a
### single dataframe

import pickle
import pandas as pd

books = {'the_sun_also_rises':'Hemingway', 'a_farewell_to_arms':'Hemingway',
		 'the_old_man_and_the_sea':'Hemingway','absalom_absalom':'Faulkner',
		 'as_i_lay_dying':'Faulkner','the_sound_and_the_fury':'Faulkner',
		 'the_great_gatsby':'Fitzgerald','this_side_of_paradise':'Fitzgerald',
		 'tender_is_the_night':'Fitzgerald','the_grapes_of_wrath':'Steinbeck',
		 'east_of_eden':'Steinbeck','of_mice_and_men':'Steinbeck'}

all_words = pd.DataFrame()

for book in books:
	print 'Processing ', book
	# Load pickled object containing word frames
	filepath = '/Users/grantnelson/desktop/data_science/sfdat22_project/' \
				+ book + '_word_frames.txt'
	with open(filepath, 'rb') as f:
		word_frames = pickle.load(f)

	# Create labels telling which author, work, and block the word is from
	def attribution_cols(word_frames):
		for i, frame in enumerate(word_frames):
			word_frames[i]['author'] = books[book]
			word_frames[i]['work'] = book
			word_frames[i]['block'] = i
		return word_frames

	word_frames = attribution_cols(word_frames)

	# Append frames to words dataframe
	for frame in word_frames:
		all_words = all_words.append(frame, ignore_index = True)
	print 'Finished processing ', book


