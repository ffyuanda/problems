from math import sqrt, pow
from itertools import combinations
def combination(in_list, n):

    return [list(x) for x in combinations(in_list, n)]

def standard_dev(in_list):
    deviation = 0
    avg = sum(in_list) / len(in_list)
    for i in in_list:
        deviation += pow((i - avg), 2)
    deviation /= len(in_list)
    deviation = sqrt(deviation)
    return deviation


def calculate(cases):
    length, n = [int(i) for i in input().split(' ')]
    in_list = [int(j) for j in input().split(' ')]
    combined = combination(in_list, n)
    curr_std = 0
    min_std = 99999999999999
    index = 0
    for i in range(len(combined)):
        curr_std = standard_dev(combined[i])
        if curr_std <= min_std:
            min_std = curr_std
            index = i
        else:
            continue
    min_group = combined[index]
    count = max(min_group) * len(min_group) - sum(min_group)

    return 'Case #{}: {}'.format(cases, count)

# read test cases
t = int(input())

# execution
for i in range(1, t+1):
    print(calculate(i))
