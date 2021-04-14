import re
from goody import irange
from collections import defaultdict

# Before running the driver on the bsc.txt file, ensure you have put a regular
#   expression pattern in the files repattern1a.txt, repattern1b.txt,
#   repattern1c.txt, and repattern2.txt.
# The patterns must be all on the first line, enclosed in ^ and $


def expand_re(pat_dict:{str:str}):
    for key in pat_dict.keys():
        while '#' in pat_dict[key]:
            for in_key, in_value in pat_dict.items():
                pat_dict[key] = re.sub('#'+in_key+'#', '(?:'+in_value+')', pat_dict[key])


def multi_search(pat_file : open, text_file : open) -> [(int,str,[int])]:
    output_list, pat_list = [], pat_file.readlines()
    for line, text in enumerate(text_file):
        pattern_line_list, pattern_line_count = [], 0
        for pattern in pat_list:
            pattern_line_count += 1
            if re.search(pattern.rstrip(), text.rstrip()) is not None:
                pattern_line_list.append(pattern_line_count)
        if len(pattern_line_list) > 0:
            output_list.append((line+1, text.rstrip(), pattern_line_list))
    return output_list


if __name__ == '__main__':
    
    p1a = open('repattern1a.txt').readline().rstrip() # Read pattern on first line
    print('Testing the pattern p1a: ',p1a)
    for text in open('bm1a.txt'):
        text = text.rstrip()
        print('Matching against:',text)
        m = re.match(p1a,text)
        print(' ','Matched' if m != None else "Not matched")


    p1b = open('repattern1b.txt').readline().rstrip() # Read pattern on first line
    print('\nTesting the pattern p1b: ',p1b)
    for text in open('bm1b.txt'):
        text = text.rstrip()
        print('Matching against:',text)
        m = re.match(p1b,text)
        print('  ','Matched' if m != None else 'Not matched' )
        
        
    p1c = open('repattern1c.txt').readline().rstrip() # Read pattern on first line
    print('\nTesting the pattern p1c: ',p1c)
    for text in open('bm1b.txt'):                 # Same file as before
        text = text.rstrip()
        print('Matching against:',text)
        m = re.match(p1c,text)
        print('  ','Matched with groups ='+ str(m.groups()) if m != None else 'Not matched' )
        
        
    p2 = open('repattern2.txt').read().rstrip() # Read pattern on first line
    print('\nTesting the pattern p2: ',p2)
    for text in open('bm2.txt'):
        text = text.rstrip()
        print('Matching against:',text)
        m = re.match(p2,text)
        print('  ','Matched' if m != None else 'Not matched' )
        
    
    
    print('\nTesting expand_re')
    pd = dict(digit = r'[0-9]', integer = r'[+-]?#digit##digit#*')
    print('  Expanding ',pd)
    expand_re(pd)
    print('  result =',pd)
    # produces/prints the dictionary
    # {'digit': '[0-9]', 'integer': '[+-]?(?:[0-9])(?:[0-9])*'}
     
    pd = dict(integer       = r'[+-]?[0-9]+',
              integer_range = r'#integer#(..#integer#)?',
              integer_list  = r'#integer_range#(,#integer_range#)*',
              integer_set   = r'{#integer_list#?}')
    print('\n  Expanding ',pd)
    expand_re(pd)
    print('  result =',pd)
    # produces/prints the dictionary 
    # {'integer': '[+-]?[0-9]+',
    #  'integer_range': '(?:[+-]?[0-9]+)(..(?:[+-]?[0-9]+))?',
    #  'integer_list': '(?:(?:[+-]?[0-9]+)(..(?:[+-]?[0-9]+))?)(,(?:(?:[+-]?[0-9]+)(..(?:[+-]?[0-9]+))?))*',
    #  'integer_set': '{(?:(?:(?:[+-]?[0-9]+)(..(?:[+-]?[0-9]+))?)(?,(?:(?:[+-]?[0-9]+)(..(?:[+-]?[0-9]+))?))*)?}'
    # }
     
    pd = dict(a='correct',b='#a#',c='#b#',d='#c#',e='#d#',f='#e#',g='#f#')
    print('\n  Expanding ',pd)
    expand_re(pd)
    print('  result =',pd)
    # produces/prints the dictionary 
    # {'a': 'correct',
    #  'b': '(?:correct)',
    #  'c': '(?:(?:correct))',
    #  'd': '(?:(?:(?:correct)))',
    #  'e': '(?:(?:(?:(?:correct))))',
    #  'f': '(?:(?:(?:(?:(?:correct)))))',
    #  'g': '(?:(?:(?:(?:(?:(?:correct))))))'
    # }


        
    print()
    print()
    import driver
    driver.default_file_name = "bscq2S21.txt"
#     driver.default_show_traceback = True
#     driver.default_show_exception = True
#     driver.default_show_exception_message = True
    driver.driver()
