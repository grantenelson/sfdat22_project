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

all_blocks = pd.DataFrame()

for book in books:
	print 'Processing ', book
	# Load pickled object containing word frames
	filepath = '/Users/grantnelson/desktop/data_science/sfdat22_project/' \
				+ book + '_block_frame.txt'
	with open(filepath, 'rb') as f:
		block_frame = pickle.load(f)

	# Create labels telling which author, work, and block the word is from
	def attribution_cols(block_frame):
		block_frame = block_frame.rename(columns = {'block':'text'})
		block_frame['author'] = books[book]
		block_frame['work'] = book
		block_frame['block'] = block_frame.index
		return block_frame

	block_frame = attribution_cols(block_frame)

	# Append frames to words dataframe
	all_blocks = all_blocks.append(block_frame, ignore_index = True)
	print 'Finished processing ', book


