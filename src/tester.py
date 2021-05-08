from helpers import hide

# for index, i in enumerate(hide('3.14159265')):
#     print(index, i)
# n = 3
# while n > 0:
#     print(n)
#     n -= 1
#     if n == 0:
#         n=3


class iter_test:
    def __init__(self):
        self.countdown = 5

    def __iter__(self):
        return self

    def __next__(self):
        self.countdown -= 1
        if self.countdown <=0 :
            raise StopIteration
        return self.countdown


# test = iter_test()
# for i in test:
#     print(i)

from goody import type_as_str
import math


class prange:
    def __init__(self,*args):
        for a in args:
            if not type(a) is int:
                raise TypeError('\''+type_as_str(a)+'\' object cannot be interpreted as an integer')

        self.start, self.step = 0, 1   # defaults for non-required parameters
        if len(args) == 1:
            self.stop = args[0]                       # store single argument
        elif len(args) == 2:
            self.start, self.stop = args              # unpack 2 arguments
        elif len(args) == 3:
            self.start, self.stop, self.step = args   # unpack 3 arguments
            if self.step == 0:
                raise ValueError('3rd argument must not be 0')
        else:
            raise TypeError('range expected at most 3 arguments, got '+str(len(args)))

    def __repr__(self):
        return 'prange('+str(self.start)+','+str(self.stop)+('' if self.step==1 else ','+str(self.step))+')'

    def __iter__(self):
        self.n = self.start  # first value to return from __next__
        return self  # must return object on which __next__ is callable

    def __next__(self):
        if self.step > 0 and self.n >= self.stop or \
                self.step < 0 and self.n <= self.stop:
            raise StopIteration
        answer = self.n
        self.n += self.step
        return answer

    def __len__(self):
        if self.step > 0 and self.start >= self.stop or \
                self.step < 0 and self.start <= self.stop:
            return 0
        else:
            return math.ceil((self.stop - self.start) / self.step)

    def __getitem__(self, n):
        if n < 0:  # Handle negative (index from end)
            n = len(self) + n
        if n < 0 or n >= len(self):  # yes, could be n >= self.__len__()
            raise IndexError(str(self) + '[' + str(n) + '] index out of range')
        return self.start + n * self.step

    def __contains__(self, n):
        if self.step > 0:
            return self.start <= n < self.stop and (n - self.start) % self.step == 0
        else:
            return self.stop < n <= self.start and abs(n - self.start) % abs(self.step) == 0
    # def __del
    def __reversed__(self):
        if self.step > 0:
            return prange(self.start + (len(self) - 1) * self.step, self.start - 1, -self.step)
        else:
            return prange(self.start + (len(self) - 1) * self.step, self.start + 1, -self.step)


# tester_prange = prange(0, 10, 2)
# print(tester_prange[1])
# for i in tester_prange:
#     print(i)
# xyz_list = ['x', 'y', 'z']
# abc_list = ['a', 'b', 'c']
#
# print('|'.join(['x', 'y', 'z']))
# zipped = zip(xyz_list, abc_list)
# print(list(zipped))

from collections import defaultdict
db = {
 'Ann': {'plumbing':2, 'painting':3},
 'Ben': {'painting':4, 'gardening':4},
 'Cal': {'painting':5, 'plumbing':5, 'gardening':5},
 'Dee': {'gardening':5}
 }
def can_do (db : {str:{str:int}}, job : str) -> [str]:
    # return_list = [(key, value[job]) for key, value in db.items() if job in value.keys()]
    # for key, value in db.items():
    #     if job in value.keys():
    #         return_list.append((key, value[job]))
    return set([(key, value[job]) for key, value in db.items() if job in value.keys()])
    return sorted([(key, value[job]) for key, value in db.items() if job in value.keys()],
                  key=lambda x:x[1], reverse=True)

def jobbers (db : {str:{str:int}}) -> {str: {int: {str}}}: # use defaultdict
    return_dict = defaultdict()
    for value in db.values():
        for job in value.keys():
            return_dict[job] = defaultdict(set)

    for key, value in db.items():
        for db_job, db_skill in value.items():
            return_dict[db_job][db_skill].add(key)

    return return_dict


def experts (db : {str:{str:int}}) -> [str]:
    rl = []
    for name, job_list in db.items():
        if sum(job_list.values()) == len(job_list) * 5:
            rl.append((name, len(job_list)))
    return [x[0] for x in sorted(sorted(rl, key=lambda x:x[0]), key=lambda x:x[1], reverse=True)]
print(can_do(db, "painting"))
#
#
# import re
# pattern = '(Mr.\s|Ms.\s)([A-Z])([a-z]*)'
# # rep_func = lambda x: "Person"
# string = 'Mr. Smith bribed Ms. Jones; but Mr. Green reported Mr. Smith.'
# match = re.match(pattern, string)
# # result = re.sub(pattern, rep_func, string)
#
# # def rep_func(mo) -> str :
# #     name_dict = dict()
# #     return re.sub(pattern, rep_func, string, count=1)
# #
# # print(re.sub(pattern, rep_func, string))
#
#
# class Modular:
#
#     def __init__(self,value,modulus):
#      self.value = value % modulus # Guarantees value < modulus
#      self.modulus = modulus
#
#
#     def __repr__(self):
#         return "{} mod {}".format(self.value, self.modulus)
#
#     def __add__(self, other):
#         # print(other.__class__.__name__)
#         if type(other) == int:
#             return Modular(other + self.value, self.modulus)
#         elif other.__class__.__name__ == "Modular":
#             if other.modulus != self.modulus:
#                 raise AssertionError
#             return Modular(other.value + self.value, self.modulus)
#         else:
#             return "NotImplemented"
#
#     def __radd__(self, other):
#         return self.__add__(other)
#
#     def __contains__(self, item):
#         if self.modulus == 5:
#             if 0 <= item <= 4:
#                 return True
#         return False
#
#
# a = Modular(13, 5)
# b = Modular(1, 5)
# print(8 in b)
# a = [2]
#
#
# b = [1,2,3,4]
# divide = len(b) // 2
# b_1 = b[:divide]
# b_2 = b[divide:]
# print(b_1, b_2)
# a = ((10,60), (20,100), (30,120))
# print(a[0])
a = 1
print(type(a))
a = '1'
print(type(a))
# print("aaa">"aaab")
gift = [1, 2, 3, 4]
print(gift[0:2])
print(gift[0:1])
print(gift[0:0])


def func_test(var1, var2) -> int:
    print(var1, var2)


func_test(1, 2)
x = 1
