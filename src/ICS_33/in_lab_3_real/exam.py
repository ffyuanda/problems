from collections import defaultdict
from ile3helper import  hide, nth_for_m, primes, Memoize


def chain_switch(pred,*iterables):
    if len(iterables) == 0:
        return
    else:
        iters = [iter(item) for item in iterables]
        empty_mark = [False] * len(iters)
        while True:
            if all(empty_mark):
                break
            for index, item in enumerate(iters):
                if empty_mark[index]:
                    continue
                while True:
                    try:
                        v = next(item)
                    except StopIteration:
                        empty_mark[index] = True
                        break
                    if pred(v):  # switch
                        yield v
                        break
                    else:
                        yield v


def same_num(s : str) -> bool:
    if len(s) == 0:
        return True
    count = s.count(s[0])
    for sub in s:
        if s.count(sub) != count:
            return False
    return True


@Memoize
def min_cuts_same_num(s : str) -> str:
    if same_num(s):
        return s
    if s.count('|') >= 1:
        sub_list = s.split('|')
        for i in range(len(sub_list)):
            sub_list[i] = same_num(sub_list[i])
        if all(sub_list):
            return s

    else:
        for i in range(1, len(s)):
            s_copy = s[:i] + '|' + s[i:]
            return min(min_cuts_same_num(s_copy), key=lambda y: y.count('|'))

class freq_dict(dict):    
    def get_info(self):
        return dict.__repr__(self._info)    

    def get_keys(self):
        return ' -> '.join(repr(k) for k in self)    

    def __init__(self):
        super().__init__()
        self._added = 0
        self._info = dict()

    def __setitem__(self, key,value):
        if key not in self._info.keys():
            self._added += 1
            self._info[key] = [self._added, 1]
        else:
            self._info[key][1] += 1
        super().__setitem__(key, value)

    def __getitem__(self, key):
        if key in self._info.keys():
            self._info[key][1] += 1

    def __delitem__(self, key):
        if key in self._info.keys():
            del self._info[key]

    def __iter__(self):
        out_list = [key for key in sorted(self._info.keys(), key=lambda x: self._info[x][0])]
        out_list = sorted(out_list, key=lambda x: self._info[x][1], reverse=True)
        return iter(out_list)

    # Extra credit worth 1 point: don't attempt unless you have written all
    #   the previous methods correctly
    def __repr__(self):
        output = ""
        for i in self:
            output += f"'{i}': {super().__getitem__(i)}, "
        output = output.rstrip(", ")
        return '{' + output + '}'

if __name__ == '__main__':

    # print('\n\nTesting min_cuts_same_num. Feel free to test other cases: e.g, base cases you choose')
    # print("same_num('')           =", same_num(''), ' ...no characters, so vacuously True')
    # print("same_num('a')          =", same_num('a'))
    # print("same_num('aab')        =", same_num('aab'))
    # print("same_num('aba')        =", same_num('aba'))
    # print("same_num('abcacb')     =", same_num('abcacb'), ' ... 2 as, 2 bs, 2 cs')
    # print("same_num('cabcaabcb')  =", same_num('cabcaabcb'), ' ... 3 as, 3 bs, 3 cs')
    # print("same_num('cabcababcb') =", same_num('cabcababcb'), '... 3 as, 4 bs, 3 cs')
    #
    # print('\n\nTesting min_cuts_same_num. Feel free to test other cases')
    # print("min_cuts_same_num('')           =", repr(min_cuts_same_num('')), '               ... minimal is 0 |s')
    # print("min_cuts_same_num('a')          =", repr(min_cuts_same_num('a')), '              ... minimal is 0 |s')
    # print("min_cuts_same_num('aaa')        =", repr(min_cuts_same_num('aaa')), '            ... minimal is 0 |s')
    # print("min_cuts_same_num('ab')         =", repr(min_cuts_same_num('ab')), '             ... minimal is 0 |')
    # print("min_cuts_same_num('aba')        =", repr(min_cuts_same_num('aba')), '           ... minimal is 1 |')
    #
    # print("min_cuts_same_num('cbbbba')     =", repr(min_cuts_same_num('cbbbba')), '       ... minimal is 2 |s')
    # print("min_cuts_same_num('bbacba')     =", repr(min_cuts_same_num('bbacba')), '       ... minimal is 2 |s')
    # print("min_cuts_same_num('cbcabb')     =", repr(min_cuts_same_num('cbcabb')), '       ... minimal is 2 |s')
    #
    # print("min_cuts_same_num('cabbcabbbc') =", repr(min_cuts_same_num('cabbcabbbc')), '   ... minimal is 2 |s')
    # print("min_cuts_same_num('accbccbcbc') =", repr(min_cuts_same_num('accbccbcbc')), '  ... minimal is 3 |s')
    # print("min_cuts_same_num('cbcacbbbcb') =", repr(min_cuts_same_num('cbcacbbbcb')), ' ... minimal is 4 |s')
    #
    #
    #
    print()
    import driver
    #Uncomment the following lines to see MORE details on exceptions
    driver.default_file_name = 'bscile3S21.txt'
    #But better to debug putting testing code above
#     driver.default_show_exception=True
#     driver.default_show_exception_message=True
    driver.driver()
