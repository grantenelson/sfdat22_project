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
	frames = make_frames(blocks, level = 'sentence')
	print 'Total frames: ', len(frames)
	for i, frame in enumerate(frames):
		print 'Processing frame ', i
		frames[i] = process_sentence_frame(frames[i])
		print 'Finished processing frame ', i
		print '\n'
	with open('/Users/grantnelson/desktop/data_science/sfdat22_project/' + book + '_sentence_frames.txt', 'wb') as f:
		pickle.dump(frames, f, protocol = 2)
	print 'Finished processing ', book