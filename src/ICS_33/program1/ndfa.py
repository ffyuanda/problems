import goody
import copy
from collections import defaultdict


def read_ndfa(file : open) -> {str:{str:{str}}}:
    output_dict = defaultdict(dict)
    for row in file:
        r_list = row.strip().split(';')
        output_dict[r_list[0]] = {
            r_list[i]: set([r_list[j + 1] for j in range(1, len(r_list), 2) if r_list[j] == r_list[i]])
            for i in range(1, len(r_list), 2)}
    return dict(output_dict)


def ndfa_as_str(ndfa : {str:{str:{str}}}) -> str:
    output_str = ""
    for state, trans_dict in sorted(ndfa.items(), key=lambda x: x[0]):
        sorted_trans_list = sorted([(item[0], sorted(list(item[1]))) for item in trans_dict.items()], key=lambda x: x[0])
        output_str += "  {} transitions: {}\n".format(state, str(sorted_trans_list))
    return output_str

       
def process(ndfa : {str:{str:{str}}}, state : str, inputs : [str]) -> [None]:
    output_list, unchange_curr, curr = [state], {state}, set()
    for tran in inputs:

        for key in unchange_curr:
            try:
                curr.update(ndfa[key][tran])
            except KeyError:
                pass
        else:
            output_list.append((tran, curr))
            unchange_curr = copy.copy(curr)
            if len(unchange_curr) == 0: # empty set of states
                return output_list
            curr = set()
    return output_list


def interpret(result : [None]) -> str:
    output_str = "Start state = {}\n".format(result[0])
    for i in range(1, len(result)):
        if result[i][1] is None:
            output_str += "  Input = {}; illegal input: simulation terminated\n".format(result[i][0])
        else:
            output_str += "  Input = {}; new possible states = {}\n".format(result[i][0], sorted(list(result[i][1])))
    return output_str + "Stop state(s) = {}\n".format(sorted(list(result[-1][1])))


if __name__ == '__main__':
    # Write script here
    file = goody.safe_open('Input the file name detailing the Non-Deterministic Finite Automaton:',
                           'r', 'Illegal file name', default='ndfaendin01.txt')
    ndfa = read_ndfa(file)
    print("\nThe details of the Non-Deterministic Finite Automaton")
    print(ndfa_as_str(ndfa))

    input_file = goody.safe_open('Input the file name detailing groups of start-states and their inputs:', 'r', 'Illegal file name', default='ndfainputendin01.txt')
    for row in input_file:
        r_list = row.strip().split(';')
        ndfa_result = process(ndfa, r_list[0], r_list[1:])
        print("\nNDFA: the trace from its start-state")
        print(interpret(ndfa_result))
        # print(interpret(ndfa_result))
    # For running batch self-tests
    print()
    import driver
    driver.default_file_name = "bsc4.txt"
#     driver.default_show_traceback = True
#     driver.default_show_exception = True
#     driver.default_show_exception_message = True
    driver.driver()
