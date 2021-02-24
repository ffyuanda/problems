import copy
import collections
import math


ItemToPurchase = collections.namedtuple('ItemToPurchase', ['item_name', 'item_price', 'item_quantity'])


def combination(in_list, n):
    answer = []
    one = n * [0]
    length = len(in_list)

    def step_forward(list_index=0, n_num=0):
        if n_num == n:
            answer.append(copy.copy(one))
            return
        for i in range(list_index, length):
            one[n_num] = in_list[i]
            step_forward(i+1, n_num+1)
    step_forward()
    return answer


def intersection(lst1, lst2):
    return list(set(lst1) & set(lst2))


def decimal_to_binary(num):
    if num > 0:
        decimal_to_binary(num // 2)
        print(num % 2, end='')


def myReplace(s, sub, dest, times=None):
    #如果times是None，替换的次数是s.count(sub)
    if times == None:
        times = s.count(sub)
    sub_index = []
    sub_length = len(sub)
    dest_length = len(dest)
    s = list(s)
    for i in range(len(s)):
        print(i+sub_length)
        # something learned, list will not have out of bound error when cutting it
        if s[i:i+sub_length] == list(sub):

            sub_index.append(i)

    n = 0
    for index in sub_index:
        if times > 0:
            offset = n * (dest_length - sub_length)
            index = index + offset
            s[index:index+sub_length] = list(dest)
            n += 1
            times -= 1
    return "".join(s)


def is_prime(in_int: int) -> bool:
    assert in_int >= 2, 'Input is smaller than 2.'
    x = math.floor(math.sqrt(in_int))

    while x >= 2:
        if in_int % x == 0:
            return False
        x -= 1
    return True


def flip_diag(in_list):

    center = math.floor((len(in_list) - 1) / 2)
    marker = math.ceil((len(in_list) - 1) / 2)
    for i in range(len(in_list)):
        for j in range(len(in_list)):
            if i == j:
                alt = in_list[i][center + marker - j]
                in_list[i][center + marker - j] = in_list[i][j]
                in_list[i][j] = alt
    return in_list


def file_operation():
    sum_ = 0
    quan = 0
    avg = 0
    with open("file1.txt", 'r') as f:
        lines = f.readlines()
        for line in lines:
            print(line, end='')
            for i in line.strip().split(' '):
                sum_ += int(i)
            quan += len(line.strip().split(' '))
        avg = math.floor(sum_ / quan)

    with open('result.txt', 'w') as r:
        r.write(str(avg))


s = list('abcc1a')
a = s[5:118]
print(a)


class bcolors:
    """
    This color class is cited and modified from
    https://stackoverflow.com/questions/287871/how-to-print-colored-text-to-the-terminal
    for color coded text.
    """

    def __init__(self):
        self.HEADER = '\033[95m'
        self.OKBLUE = '\033[94m'
        self.OKCYAN = '\033[96m'
        self.OKGREEN = '\033[92m'
        self.WARNING = '\033[93m'
        self.FAIL = '\033[91m'
        self.ENDC = '\033[0m'
        self.BOLD = '\033[1m'
        self.UNDERLINE = '\033[4m'

    def color_code(self, string: str, ctype: str) -> str:
        """
        To return a color-coded string.
        :param string: the original string without color
        :param ctype: the type of color you want to encode
        :return: a color-coded string

        Example usage:
        color_mod = bcolors()
        print(color_mod.color_code("sad", 'ok'))
        """
        if ctype == 'ok':
            output = "{}{}{}".format(self.OKGREEN, string, self.ENDC)
            return output
        elif ctype == 'warning':
            output = "{}{}{}".format(self.WARNING, string, self.ENDC)
            return output
        elif ctype == 'error':
            output = "{}{}{}".format(self.FAIL, string, self.ENDC)
            return output

# error handling tests
# if raise from None, then the outer error would not be displayed
# if raise from e, then the outer error would be the direct cause to this error
# if simply raise, then this error would be another exception
# during handling the above outer error.
# try:
#     x = 1 / 0
# except ZeroDivisionError as e:
#     try:
#         x = 'i' + 1
#     except TypeError:
#         raise TypeError('We cannot add str and int!') from None
