# my_dict = {1:2, 3:4}
# my_dict2 = {1:23, 3: 44}
# my_list = my_dict2 + my_dict
# print(my_list)
# x = [1, 2, 3]
# x[1] = x
# print(x)
from collections import defaultdict
pairs = [('d', 15), ('d', 12), ('d', 10), ('d', 30), ('i', 15), ('i', 30), ('i', 15), ('r', 15), ('r', 8), ('r', 22), ('r', 30), ('r', 15), ('l', 20), ('l', 20), ('l', 15)]
# some_dict = defaultdict(int)
parties = ['d', 'l', 'r', 'i']
some_list = [(party, list(map(lambda y: y[1], filter(lambda x: x[0] == party, pairs)))) for party in parties]
some_list = [(i[0], sum(i[1])) for i in some_list]
# some_list = list(map(lambda y: y[1], filter(lambda x: x[0] == 'd', pairs)))
# some_list = [pairs[p][1] if pairs[p][0] == pairs[p - 1][0] else pairs[p][1] for p in range(0, len(pairs))]
# some_dict = {pairs[p][0]: (pairs[p - 1][1] + pairs[p][1]) if pairs[p][0] == pairs[p - 1][0] else (pairs[p][1]) for p in range(1, len(pairs))}
print(some_list)
