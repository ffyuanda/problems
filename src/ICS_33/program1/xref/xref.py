from collections import defaultdict
from goody       import safe_open

# Prompt the user for a file name (to 'r'ead) and ensure the name of the file
# entered exists: see the sample file xrefin.txt; observe what happens if you
# enter the name of a file that does not exist
file = safe_open('Enter name of file to cross-reference','r','Illegal file name',default='xrefin.txt')

# When accessing the value associated with any key, substitute a parameterless call
# to set -set()- as the association, if the key is not present in the defaultdict.
# By using a set, words will be associated with # each line just once, even if the
# word appears on a line multiple times.
xref = defaultdict(set)

# Iterate over every line_number and line in the file
#    Strip the newline off the right end of the text and covert it to all lower case
#    If the result is not an empty line
#      Iterate over a list of words separated by the space character
#        Add the current line_number to the set of line numbers associated with each word
#          (recall for defaultdict, if xref[word] does not exist, associate it with
#          set() before mutating the set to include line_number
for line_number,text in enumerate(file,1):
    text = text.rstrip().lower()
    if len(text) != 0:
        for word in text.split(' '):
            xref[word].add(line_number)


# Close the file (it has no more lines to read)
file.close() 


# Compute the maximum length of all words that are keys in xref
# Iterate over every word and its associated set in the in xref, in the standard order
#    Print every word formatted to be left-justified in the appropriate field-width,
#      followed by a string that joins together the string equivalent of the values
#      in the set, in sorted order
#       
max_len = max(len(x) for x in xref.keys())
print('Formatted by increasing alphabetical order')
for word,lines in sorted(xref.items()):
    print( f"{word:<{max_len}}: {', '.join(str(x) for x in sorted(lines))}" )

# For example, if max_len is 10, then the string object that format operates on is left
# justified in a fixed field width of 10. See Sections 2.4.3 (Formatted String Literals)
# in the Python Library. Anything in  {} is evaluated.
# See https://docs.python.org/3/reference/lexical_analysis.html#formatted-string-literals

# str(x) for x in sorted(lines) produces a generator for a tuple containing the string
# equivalent of each set of lines: if the set were {2, 5, 1} think of the result being
# able to iterate over the tuple ('1', '2', '5')

# The call to join produces one big string, built by using ', ' to separate all the
# strings the generator for a tuple: '1, 2, 5'

# Iterate over every word and its associated set in the in xref, in decreasing order of
#   how frequent the word appears in the text.
print('\nFormatted by decreasing frequency of use (equally used words may appear in any order')
for word,lines in sorted(xref.items(), key = lambda x: -len(x[1])):
    print( f"{word:<{max_len}}: {', '.join(str(x) for x in sorted(lines))}" )
