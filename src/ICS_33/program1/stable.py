import prompt
import goody
from collections import defaultdict

# Use these global variables to index the list associated with each name in the dictionary.
# e.g., if men is a dictionary, men['m1'][match] is the woman who matches man 'm1', and 
# men['m1'][prefs] is the list of preference for man 'm1'.
# It would seems that this list might be better represented as a named tuple, but the
# preference list it contains is mutated, which is not allowed in a named tuple. 

match = 0   # Index 0 of list associate with name is match (str)
prefs = 1   # Index 1 of list associate with name is preferences (list of str)


def read_match_preferences(open_file : open) -> {str:[str,[str]]}:
    result_dict = defaultdict(list)
    for text in open_file:
        t_list = text.strip().split(';')
        result_dict[t_list[0]] = [None, t_list[1:]]
    return dict(result_dict)


def dict_as_str(d : {str:[str,[str]]}, key : callable=None, reverse : bool=False) -> str:
    output = ""
    for d_key in sorted(d.keys(), key=key, reverse=reverse):
        output += "  {} -> {}\n".format(d_key, d[d_key])
    return output


def who_prefer(order : [str], p1 : str, p2 : str) -> str:
    pass


def extract_matches(men : {str:[str,[str]]}) -> {(str,str)}:
    pass


def make_match(men : {str:[str,[str]]}, women : {str:[str,[str]]}, trace : bool = False) -> {(str,str)}:
    pass    
  


  
    
if __name__ == '__main__':
    # Write script here
    mfile = goody.safe_open('Input the file name detailing the preferences for men: ',
                           'r', 'Illegal file name', default='men0.txt')
    # wfile = goody.safe_open('Input the file name detailing the preferences for women: ',
    #                         'r', 'Illegal file name', default='men0.txt')
    d = read_match_preferences(mfile)
    print(dict_as_str(d, reverse=True))
    # For running batch self-tests
    print()
    import driver
    driver.default_file_name = "bsc2.txt"
#     driver.default_show_traceback = True
#     driver.default_show_exception = True
#     driver.default_show_exception_message = True
    driver.driver()
