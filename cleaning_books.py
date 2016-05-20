### MUNGING DATA

# The Sun Also Rises:
filepath = '/Users/grantnelson/Desktop/Data_Science/sfdat22_work/project/books/Hemingway/The_Sun_Also_Rises.txt'

f = open(filepath)
txt = f.read()
f.close()

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

# Farewell to Arms:
#txt = re.sub(r'(\n+)?(\d+)? A FAREWELL TO ARMS (\d+)?(\n)?',' ',txt)