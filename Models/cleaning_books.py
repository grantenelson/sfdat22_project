### MUNGING DATA
from unidecode import unidecode
import re

### HEMINGWAY

### The Sun Also Rises:
filepath = '/Users/grantnelson/Desktop/Data_Science/sfdat22_project/books/Hemingway/The_Sun_Also_Rises.txt'

with open(filepath, 'r') as f:
	txt = f.read()

# Remove extra info at start and end of book 
txt = txt[1111:-20]

# Replace weirdly formatted charcters that cause decoding issues
txt = txt.replace('”','\"')
txt = txt.replace('“','\"')
txt = txt.replace('’','\'')

# Remove dividers for chapters and books within text
txt = re.sub(r'\n{6}\d{1,2}\n{3}',' ', txt)
txt = re.sub(r'\n{6}BOOK\s\w+','',txt)

# Remove double new-lines between paragraphs
txt = txt.replace('\n\n', ' ')


### Farewell to Arms:
filepath = '/Users/grantnelson/Desktop/Data_Science/sfdat22_project/books/Hemingway/A_Farewell_To_Arms.txt'
with open(filepath,'r') as f:
	txt = f.read()

# Remove extra info at start and end of book 
txt = txt[114:-15]
txt = unidecode(unicode(txt, encoding = 'utf-8'))

# Remove title and page number at the top of every page
txt = re.sub(r'(\n+)?(\d+\s)?A FAREWELL TO ARMS(\s\d+)?(\n)?',' ',txt)

# Remove dividers for chapters and books within text
txt = re.sub(r'\n{4}CHAPTER\s\w+\n{2}',' ',txt)
txt = re.sub(r'\n{4,6}BOOK\s\w{1,3}\n{2}',' ',txt)

# Remove a few weird characters
txt = txt.replace('T4.>\n\n','\n\n"')
txt = txt.replace('>','"')
txt = re.sub("/\\'",'"',txt)

# Remove newlines
txt = re.sub(r'\n+',' ',txt)


### The Old Man and the Sea
filepath = '/Users/grantnelson/Desktop/Data_Science/sfdat22_project/books/Hemingway/The_Old_Man_And_The_Sea.txt'
with open(filepath,'r') as f:
	txt = f.read()

# Remove extra info at start and end of book 
txt = txt[97:-2346]

# Replace quotation marks formatted as '' with "
txt = txt.replace("''",'"')

# Remove double new-lines between paragraphs
txt = re.sub(r'\n+',' ',txt) 

### FITZGERALD

### The Great Gatsby:
filepath = '/Users/grantnelson/Desktop/Data_Science/sfdat22_project/books/Fitzgerald/The_Great_Gatsby.txt'
with open(filepath, 'r') as f:
	txt = f.read()

# Replace characters that can't be read
txt = unidecode(unicode(txt, encoding = 'utf-8'))

# Remove extra info at start and end of book 
txt = txt[1403:-48]

# Remove dividers for chapters within text
txt = re.sub(r'\n{6}Chapter\s\d{1,2}\n{6}',' ',txt)

# Remove new-lines between paragraphs
txt = re.sub(r'\n+',' ',txt)


### Tender Is The Night
filepath = '/Users/grantnelson/Desktop/Data_Science/sfdat22_project/books/Fitzgerald/Tender_Is_The_Night.txt'
with open(filepath, 'r') as f:
	txt = f.read()

# Remove extra info at start and end of book 
txt = txt[2287:-264]
txt = unidecode(unicode(txt, encoding = 'utf-8'))

# Remove dividers for books and chapters within text
txt = re.sub(r'\n{6}https://ebooks.adelaide.edu.au/f/fitzgerald/f_scott/tender/chapter\d+.html\n{2}Last updated Sunday, March 27, 2016 at 11:54\n{6}Tender is the Night, by F. Scott Fitzgerald\n{6}BOOK \d\n{3}I\n{6}',' ',txt)
txt = re.sub(r'\n{6}https://ebooks.adelaide.edu.au/f/fitzgerald/f_scott/tender/chapter\d+.html\n{2}Last updated Sunday, March 27, 2016 at 11:54\n{6}Tender is the Night, by F. Scott Fitzgerald\n{6}\w+\n{6}',' ',txt)

# Remove new-lines between paragraphs
txt = re.sub(r'\n+',' ',txt)


### This Side of Paradise
filepath = '/Users/grantnelson/Desktop/Data_Science/sfdat22_project/books/Fitzgerald/This_Side_Of_Paradise.txt'
with open(filepath, 'r') as f:
	txt = f.read()

# Remove extra info at start and end of book 
txt = txt[1412:-20492]
txt = unidecode(unicode(txt, encoding = 'utf-8'))

# Remove dividers for books, chapters, etc. within text
txt = re.sub(r'\n+\* \* \*\n{4}.+\n{2}',' ',txt)

# Remove new-lines between paragraphs
txt = re.sub(r'\n+',' ',txt)

### FAULKNER

### The Sound And The Fury:
filepath = '/Users/grantnelson/Desktop/Data_Science/sfdat22_project/books/Faulkner/The_Sound_And_The_Fury.txt'
with open(filepath, 'r') as f:
	txt = f.read()

# Replace characters that can't be read
txt = unidecode(unicode(txt, encoding = 'utf-8'))

# Remove extra info at start and end of book 
txt = txt[18692:-33338]

# Remove new-lines throughout text
txt = re.sub(r'\n+',' ',txt)

### As I Lay Dying
filepath = '/Users/grantnelson/Desktop/Data_Science/sfdat22_project/books/Faulkner/As_I_Lay_Dying.txt'
with open(filepath, 'r') as f:
	txt = f.read()

# Remove extra info at start and end of book 
txt = txt[347:-30]

# Remove dividers for chapters
txt = re.sub(r'\n{4}\w+(\s\w+)?\n{4}',' ',txt)
txt = re.sub(r'\n{4}\* \* \*\n{6}Chapter\s\d\n','',txt)
txt = re.sub(r'\n{4}TULL\n{2}', '', txt)

# Remove new-lines throughout text
txt = re.sub(r'\n+',' ',txt)

### Absalom Absalom!
filepath = '/Users/grantnelson/Desktop/Data_Science/sfdat22_project/books/Faulkner/Absalom_Absalom.txt'
with open(filepath, 'r') as f:
	txt = f.read()

# Remove weirdly formatted breaks in text
txt.replace('\xc2\xa0\xc2\xa0\xc2\xa0\xc2\xa0\xc2\xa0\xc2\xa0\xc2\xa0\xc2\xa0\xc2\xa0\xc2\xa0\xc2\xa0','')
txt = txt.replace('\xe2\x80\x94',' ')

# Change format of quotations from ' to "
txt = txt.replace(" \'", ' "')
txt = txt.replace("\' ", '" ')
txt = txt.replace("(\'", '("')
txt = txt.replace("\')", '")')

# Remove new-lines throughout text
txt = re.sub(r'\n+',' ',txt)

### STEINBECK

### Grapes of Wrath
filepath = '/Users/grantnelson/Desktop/Data_Science/sfdat22_project/books/Steinbeck/The_Grapes_Of_Wrath.txt'
with open(filepath, 'r') as f:
	txt = f.read()

txt = unidecode(unicode(txt, encoding = 'utf-8'))

txt = re.sub(r'\n{6}?Chapter\s\d{1,2}\n{2}',' ',txt)
txt = re.sub(r'\n+',' ',txt)
txt = [1:]

write_filepath = filepath[:-4] + '_clean' + '.txt'
with open(write_filepath, 'w') as f:
	f.write(txt)

### East of Eden
filepath = '/Users/grantnelson/Desktop/Data_Science/sfdat22_project/books/Steinbeck/East_Of_Eden.txt'
with open(filepath, 'r') as f:
	txt = f.read()

# Remove extra info at start and end of book
txt = txt[2872:-759]
txt = unidecode(unicode(txt, encoding = 'utf-8'))

# Remove dividers for chapters and sub-chapters
txt = re.sub(r'\n{6}Chapter\s\d+\n{2}1\n{2}',' ',txt)
txt = re.sub(r'\n{2}\d+\n{2}',' ',txt)
txt = re.sub(r'\n{2}\d\.',' ', txt)

# Remove new-lines throughout text
txt = re.sub(r'\n+',' ',txt)

### Of Mice and Men
filepath = '/Users/grantnelson/Desktop/Data_Science/sfdat22_project/books/Steinbeck/Of_Mice_And_Men.txt'
with open(filepath, 'r') as f:
	txt = f.read()

# Remove dividers for chapters and sub-chapters
txt = txt[5260:-6]

# Remove new-lines throughout text
txt = re.sub(r'\n+',' ',txt)

