import prompt
import goody
import copy
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
    return p1 if order.index(p1) < order.index(p2) else p2


def extract_matches(men : {str:[str,[str]]}) -> {(str,str)}:
    return {(key, value[0]) for key, value in men.items()}


def make_match(men : {str:[str,[str]]}, women : {str:[str,[str]]}, trace : bool = False) -> {(str,str)}:
    if trace:
        print("Women Preferences (unchanging)\n" + dict_as_str(women))
    men_copy = copy.deepcopy(men)
    unmatched = set(men_copy.keys())
    while len(unmatched) > 0:
        if trace:
            print("Men Preferences (current)\n" + dict_as_str(men_copy))
            print("unmatched men = " + str(unmatched) + '\n')

        anyman = unmatched.pop()
        the_woman = men_copy[anyman][prefs][0] # the first woman on the list
        match_pair = [p for p in list(extract_matches(men_copy)) if p[1] == the_woman] # get the match that contains the woman

        if len(match_pair) == 0: # if the women is unmatched
            men_copy[anyman][match] = the_woman # set the woman to the matched slot
            men_copy[anyman][prefs].remove(the_woman) # remove the woman from the preference list
            if trace:
                print("{} proposes to {} (an unmatched woman); so she accepts the proposal\n".format(anyman, the_woman))
        elif len(match_pair) == 1: # if the women is matched
            curr_match = match_pair[0][0]
            prefer = who_prefer(women[the_woman][prefs], curr_match, anyman)
            if prefer == anyman: # prefers anyman to curr_match
                men_copy[curr_match][match] = None # unmatch curr_math and the_woman
                unmatched.add(curr_match) # curr_match is now unmatched
                men_copy[anyman][match] = the_woman  # set the woman to the matched slot
                men_copy[anyman][prefs].remove(the_woman)  # remove the woman from the preference list
                if trace:
                    print("{} proposes to {} (a matched woman); she prefers her new match, so she accepts the proposal\n".format(anyman, the_woman))
            else: # prefers curr_match to anyman
                men_copy[anyman][prefs].remove(the_woman)
                unmatched.add(anyman)
                if trace:
                    print("{} proposes to {} (a matched woman); she prefers her current match, so she rejects the proposal\n".format(anyman, the_woman))
    if trace:
        print("Tracing option finished: final matches = {}".format(str(extract_matches(men_copy))))
    else:
        print("\nThe final matches = {}".format(str(extract_matches(men_copy))))
    return extract_matches(men_copy)

    
if __name__ == '__main__':
    # Write script here
    mfile = goody.safe_open('Input the file name detailing the preferences for men: ',
                           'r', 'Illegal file name', default='men0.txt')
    wfile = goody.safe_open('Input the file name detailing the preferences for women: ',
                            'r', 'Illegal file name', default='women0.txt')
    men_d = read_match_preferences(mfile)
    women_d = read_match_preferences(wfile)
    print("\nMen Preferences\n" + dict_as_str(men_d))
    print("Women Preferences\n" + dict_as_str(women_d))
    trace = False if input("Input tracing algorithm option[True]: ") == "False" else True
    make_match(men_d, women_d, trace)

    # For running batch self-tests
    print()
    import driver
    driver.default_file_name = "bsc2.txt"
#     driver.default_show_traceback = True
#     driver.default_show_exception = True
#     driver.default_show_exception_message = True
    driver.driver()
