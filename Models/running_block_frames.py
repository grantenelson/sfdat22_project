books = {'the_sun_also_rises':'Hemingway', 'a_farewell_to_arms':'Hemingway',
		 'the_old_man_and_the_sea':'Hemingway','absalom_absalom':'Faulkner',
		 'as_i_lay_dying':'Faulkner','the_sound_and_the_fury':'Faulkner',
		 'the_great_gatsby':'Fitzgerald','this_side_of_paradise':'Fitzgerald',
		 'tender_is_the_night':'Fitzgerald','the_grapes_of_wrath':'Steinbeck',
		 'east_of_eden':'Steinbeck','of_mice_and_men':'Steinbeck'}

for book in books:
	print 'Processing ', book
	with open('/Users/grantnelson/desktop/data_science/sfdat22_project/books/' + books[book] + '/' + book + '_clean.txt', 'r') as f:
		txt = f.read()
	blocks = make_text_blocks(txt)
	block_frame = make_frames(blocks, level = 'block')
	print 'Total blocks: ', len(block_frame)
	block_frame = process_block_frame(block_frame)
	with open('/Users/grantnelson/desktop/data_science/sfdat22_project/' + book + '_block_frame.txt', 'wb') as f:
		pickle.dump(block_frame, f, protocol = 2)
	print 'Finished processing ', book