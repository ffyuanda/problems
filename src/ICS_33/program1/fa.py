import goody
from collections import defaultdict


def read_fa(file : open) -> {str:{str:str}}:
    output_dict = defaultdict(dict)
    for row in file:
        r_list = row.strip().split(';')
        output_dict[r_list[0]] = {r_list[i]:r_list[i+1] for i in range(1, len(r_list), 2)}
    return dict(output_dict)


def fa_as_str(fa : {str:{str:str}}) -> str:
    output_str = ""
    for state, trans_dict in sorted(fa.items(), key=lambda x: x[0]):
        sorted_trans_list = sorted([(item[0], item[1]) for item in trans_dict.items()], key=lambda x: x[0])
        output_str += "  {} transitions: {}\n".format(state, str(sorted_trans_list))
    return output_str


def process(fa : {str:{str:str}}, state : str, inputs : [str]) -> [None]:
    output_list, curr = [state], state
    for tran in inputs:
        try:
            curr = fa[curr][tran]
        except KeyError:
            output_list.append((tran, None))
            break
        output_list.append((tran, curr))
    return output_list


def interpret(fa_result : [None]) -> str:
    output_str = "Start state = {}\n".format(fa_result[0])
    for i in range(1, len(fa_result)):
        if fa_result[i][1] is None:
            output_str += "  Input = {}; illegal input: simulation terminated\n".format(fa_result[i][0])
        else:
            output_str += "  Input = {}; new state = {}\n".format(fa_result[i][0], fa_result[i][1])
    return output_str + "Stop state = {}\n".format(fa_result[-1][1])


if __name__ == '__main__':
    # Write script here
    file = goody.safe_open('Input the file name detailing the Finite Automaton:', 'r', 'Illegal file name', default='faparity.txt')
    fa = read_fa(file)
    print("\nThe details of the Finite Automaton")
    print(fa_as_str(fa))

    input_file = goody.safe_open('Input the file name detailing groups of start-states and their inputs:', 'r', 'Illegal file name', default='fainputparity.txt')
    for row in input_file:
        r_list = row.strip().split(';')
        fa_result = process(fa, r_list[0], r_list[1:])
        print("\nFA: the trace from its start-state")
        print(interpret(fa_result))

    # For running batch self-tests
    print()
    import driver
    driver.default_file_name = "bsc3.txt"
#     driver.default_show_traceback = True
#     driver.default_show_exception = True
#     driver.default_show_exception_message = True
    driver.driver()
