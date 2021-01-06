# def travel_time(dists, vels):
#
#
#    total_travel_time = 0
#
#    for x in range(len(dists)):
#        total_travel_time += dists[x] * vels[x]
#
#    return total_travel_time
#
# print(travel_time([5, 5], [5, 5]))
# assert travel_time([1, 1], [1, 1]) == 1
# print([list(range(i)) for i in range(15) if i > 5])

# new_list = []
# for i in range(15):
#     if i > 5:
#         a_list = []
#         for j in range(i):
#             a_list.append(j)
#         new_list.append(a_list)
# if -1:
#     print(True)

# def weave(a, b):
#     """
#         Function weave takes two lists, a and b.
#         Then, if the longer list length can be divided by the second list’s length,
#         The function will weave together the two lists.
#
#         For each element of the smaller list, it will weave in X elements of the bigger list,
#         where X = length of big list / length of small list.
#         Example: weave [1, 4, 7] with [2, 3, 5, 6, 8, 9] will result in [1, 2, 3, 4, 5, 6, 7, 8, 9]
#         If the two lists are the same size, list a will be used first.
#         If the two lengths are incompatible, it will return None.
#
#         At the end, it returns the final list.
#     """
#
#     if len(a) > len(b):
#         big = a
#         small = b
#     else:
#         big = b
#         small = a
#
#     if len(big) % len(small) != 0:
#         return None
#
#     jump_number = int(len(big) / len(small))
#
#     new_arr = []
#
#     for i in range(len(small)):
#         new_arr.append(small[i])
#         j = i * jump_number
#         app = big[j:j + jump_number]
#         for x in app:
#
#             new_arr.append(x)
#
#     return new_arr
#
# assert (weave([7, 4, 7], [1, 6, 2, 5, 8, 9]) == [7, 1, 6, 4, 2, 5, 7, 8, 9])
# assert (weave([2, 3, 5, 6, 8, 9], [1, 4, 7]) == [1, 2, 3, 4, 5, 6, 7, 8, 9])
# assert (weave([1, 3, 5], [2, 4, 6]) == [1, 2, 3, 4, 5, 6])
# assert (weave(['a', 'c', 'e'], ['b', 'd', 'f']) == ['a', 'b', 'c', 'd', 'e', 'f'])
# assert (weave([1, 4, 7], [8, 9]) == None)


# def print_file(in_list):
#
#     for file in in_list:
#         with open(file, 'r') as f:
#             fread = f.readlines()
#             print(file + ' : ' + fread[1])
#
# print_file(['file1.txt', 'file2.txt'])

# def get_book(**kwargs):
#     output = dict()
#     for category, content in kwargs.items():
#         print(str(category) + ':' + str(content))
#         output[category] = content
#     return output
# print(get_book(book_name="A Game of Thrones", isbn="123-123-1234", author="GRR Martin", pages=694))

from collections import namedtuple
Wizard = namedtuple('Wizard', 'name attending_year')
wizard1 = Wizard('wizard1', '2000')
wizard2 = Wizard('wizard2', '2001')
wizard3 = Wizard('wizard3', '2001')
wizard4 = Wizard('wizard4', '2002')
wizard5 = Wizard('wizard5', '2002')
wizard6 = Wizard('wizard6', '2003')

d = {'house1': [wizard1, wizard2, wizard3], 'house2': [wizard4, wizard5, wizard6]}


def print_names(house, year):

    for wizard in d[house]:
        if int(wizard.attending_year) == int(year):
            print(wizard.name)


print_names('house2', '2003')
