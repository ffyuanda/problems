from collections import defaultdict
import copy
from goody import type_as_str
import prompt


class Bag:

    def __init__(self, iterable: list = list()):
        self.values = defaultdict(int)
        for i in iterable:
            self.values[i] += 1

    def __repr__(self) -> str:
        return_list = self.return_list()
        return "Bag({})".format(str(return_list)) if return_list != [] else "Bag()"

    def __str__(self):
        result_list = ["{}[{}]".format(key, count) for key, count in self.values.items()]
        result_str = ''
        for i in result_list:
            result_str += i + ', '
        result_str = result_str.rstrip(', ')
        return "Bag({})".format(result_str)

    def __iter__(self):
        copy_dict = copy.deepcopy(dict(self.values))
        return_list = self.return_list(copy_dict)
        return iter(return_list)

    def __add__(self, other):
        if other.__class__.__name__ != self.__class__.__name__:
            raise TypeError('Not supported type concatenation')
        big_list = self.return_list() + other.return_list()
        return Bag(big_list)

    def __len__(self):
        return len(self.return_list())

    def __eq__(self, other):
        return repr(self) == repr(other)

    def remove(self, key):
        if key not in self.values.keys():
            raise ValueError("The value needs to be removed does not exist")
        else:
            self.values[key] -= 1
            if self.values[key] == 0:
                self.values.pop(key)

    def count(self, key):
        return self.values[key]

    def add(self, key):
        self.values[key] += 1

    def unique(self):
        return len(self.values.keys())

    def return_list(self, iter_dict=None):
        if iter_dict is None:
            iter_dict = self.values
        return_list = []
        for key, times in iter_dict.items():
            return_list += ([key] * times)
        return sorted(return_list)


if __name__ == '__main__':
    
    #Simple tests before running driver
    #Put your own test code here to test Bag before doing the bsc tests
    #Debugging problems with these tests is simpler

    b = Bag(['d','a','d','b','c','b','d'])
    # print(b.values)
    # k = (repr(b).count('\''+v+'\'')==c for v,c in dict(a=1,b=2,c=1,d=3).items())
    # s = (v + '[' + str(c) + ']' in str(b) for v, c in dict(a=1, b=2, c=1, d=3).items())
    # print(k, s)
    print(len(b))
    print(b)
    print(repr(b))
    print(all((repr(b).count('\''+v+'\'')==c for v,c in dict(a=1,b=2,c=1,d=3).items())))
    for i in b:
        print(i)

    b2 = Bag(['a','a','b','x','d'])
    print(repr(b2+b2))
    print(str(b2+b2))
    print([repr(b2+b2).count('\''+v+'\'') for v in 'abdx'])
    b = Bag(['a','b','a'])
    print(repr(b))
    print()
    
    import driver
    driver.default_file_name = 'bscp21S21.txt'
#     driver.default_show_exception = True
#     driver.default_show_exception_message = True
#     driver.default_show_traceback = True
    driver.driver()
