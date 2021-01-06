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
