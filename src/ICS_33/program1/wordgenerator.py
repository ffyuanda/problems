import goody
import copy
from collections import defaultdict
from goody import irange
import prompt
from random import choice


# For use in read_corpus: leave unchanged in this file
def word_at_a_time(file : open):
    for line in file:
        for item in line.strip().split():
                yield item


def read_corpus(os : int, file : open) -> {(str):[str]}:
    output_dict, words = defaultdict(list), word_at_a_time(file)
    tuple_list = [next(words) for i in range(os)]
    for word in words:
        if word not in output_dict[tuple(tuple_list)]:
            output_dict[tuple(tuple_list)].append(word)
        tuple_list.pop(0)
        tuple_list.append(word)
    return output_dict


def corpus_as_str(corpus : {(str):[str]}) -> str:
    output_str = ""
    corpus = {key: corpus[key] for key in sorted(corpus.keys())}
    for key, item in corpus.items():
        output_str += "  {} can be followed by any of {}\n".format(key, item)
    len_list = [len(value) for value in corpus.values()]
    min_list, max_list = min(len_list), max(len_list)
    return output_str + "min/max list lengths = {}/{}\n".format(min_list, max_list)


def produce_text(corpus : {(str):[str]}, start : [str], count : int) -> [str]:
    n_list, result_list = copy.deepcopy(start), copy.deepcopy(start)
    for i in range(count):
        try:
            next_word = choice(corpus[tuple(n_list)])
        except KeyError:
            result_list.append(None)
            return result_list
        n_list.pop(0)
        n_list.append(next_word)
        result_list.append(next_word)
    return result_list

        
if __name__ == '__main__':
    # Write script here
    os = int(input("Input an order statistic: "))
    file = goody.safe_open('Input the file name detailing the text to read: ', 'r', 'Illegal file name', default='wginput1.txt')
    corpus = read_corpus(os, file)
    print("Corpus")
    print(corpus_as_str(corpus))

    print("Input {} words at the start of the list".format(os))
    random_text = []
    for i in range(os):
        random_text.append(input("Input word {}: ".format(i + 1)))
    count = int(input("Input # of words to append to the end of the list: "))
    print("Random text =", produce_text(corpus, random_text, count))
    # For running batch self-tests
    print()
    import driver
    driver.default_file_name = "bsc5.txt"
#     driver.default_show_traceback = True
#     driver.default_show_exception = True
#     driver.default_show_exception_message = True
    driver.driver()
