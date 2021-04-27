from helpers import primes, hide, nth
from builtins import RuntimeError


def differences(iterable1, iterable2):
    zipped = zip(iterable1, iterable2)
    for index, i in enumerate(zipped):
        if i[0] != i[1]:
            yield index + 1, i[0], i[1]
            
   
def once_in_a_row(iterable):
    last_yield = '!@#$%^&^&**(()123222'
    for i in iterable:
        if i != last_yield:
            yield i
        last_yield = i
                

def in_between(iterable, starter, stopper):
    find_start, find_stop = True, False
    for i in iterable:
        if find_start:
            if starter(i) and stopper(i):
                yield i
                continue
            if starter(i):  # find the start
                find_start, find_stop = False, True
                yield i

        elif find_stop:
            if stopper(i):
                find_start, find_stop = True, False
                yield i
            else:
                yield i


def pick(iterable,n):
    count, yield_list = 0, []
    yield_list = []
    for i in iterable:
        if count != n:
            yield_list.append(i)
            count += 1
        if count == n:
            yield yield_list
            count, yield_list = 0, []


def slice_gen(iterable, start: int, stop: int, step: int):
    if start < 0 or stop < 0 or step <= 0:
        raise AssertionError("illegal input")
    stepper = 1

    for i in iterable:
        if start == 0: # at the beginning
            stepper -= 1
            if stepper == 0:
                yield i
                stepper = step
        else:
            start -= 1

        if stop == 1: # at the end
            break
        else:
            stop -= 1


def alternate_all(*args):
    fail_count = 0
    iter_args = [iter(arg) for arg in args]
    while fail_count < len(args):
        fail_count = 0
        for arg in iter_args:
            try:
                yield arg.__next__()
            except:
                fail_count += 1


class ListSI:
    def __init__(self,initial):
        self._real_list  = list(initial)
        self._iter_count = 0
    
    def __repr__(self):
        return repr(self._real_list)
    
    def __len__(self):
        return len(self._real_list)
    
    def append(self,value):
        if self._iter_count > 0:
            raise RuntimeError('ListSI is immutable during iterations')
        self._real_list.append(value)
            
    def __getitem__(self,index):
        return self._real_list[index]
            
    def __setitem__(self,index, value):
        self._real_list[index] = value
            
    def __delitem__(self,index):
        if self._iter_count > 0:
            raise RuntimeError('ListSI is immutable during iterations')
        del self._real_list[index]
            
    def __iter__(self):

        class ListSI_iter:
            def __init__(self, aListSI):
                self.count = -1
                self.ListSI = aListSI
                self.ListSI._iter_count += 1
             
            def __next__(self):
                try:
                    self.count += 1
                    return self.ListSI[self.count]
                except IndexError:
                    self.ListSI._iter_count -= 1
                    raise StopIteration

            def __iter__(self):
                return self
             
        return ListSI_iter(self)


def fool_it():
    l = ListSI(['a','b', 'c'])
    for i in l:
        break
    
    l.append('z')  # so that this statement incorrectly raises a RuntimeError exception    


if __name__ == '__main__':
    
    # Test differences; you can add your own test cases
    print('Testing differences')
    for i in differences('3.14159265', '3x14129285'):
        print(i,end=' ')
    print()

    for i in differences(hide('3.14159265'), hide('3x14129285')):
        print(i,end=' ')
    print()

    for i in differences(primes(), hide([2, 3, 1, 7, 11, 1, 17, 19, 1, 29])):
        print(i,end=' ')
    print('\n')

    for i in differences(hide([2, 3, 1, 7, 11, 1, 17, 19, 1, 29]), primes()):
        print(i,end=' ')
    print('\n')

              
    # Test once_in_a_row; you can add your own test cases
    print('\nTesting once_in_a_row')
    for i in once_in_a_row([None, None, 1, 2, None]):
        print(i,end='')    
    print()

    for i in once_in_a_row(hide('abcccaaabddeee')):
        print(i,end='')
    print('\n')
    
        
    # Test in_between; you can add your own test cases
    print('\nTesting in_between')
    for i in in_between('123abczdefalmanozstuzavuwz45z', (lambda x : x == 'a'), (lambda x : x == 'z')):
        print(i,end='')
    print()
    
    for i in in_between(hide('123abczdefalmanozstuzavuwz45z'), (lambda x : x == 'a'), (lambda x : x == 'z')):
        print(i,end='')
    print()

    for i in in_between(primes(), (lambda x : x%10 == 3), (lambda x : x%10 == 7)):
        print(i,end=' ')
        if i > 100:
            break
    print()
    
    for i in in_between('123abczdefalmanozstuzavuwz45z', (lambda x : x == 'a'), (lambda x : x == 'a')):
        print(i,end='')
    print('\n')


    # Test pick' you can add your own test cases
    print('\nTesting pick')
    for i in pick('abcdefghijklm',4):
        print(i,end='')
    print()
    
    for i in pick(hide('abcdefghijklm'),4):
        print(i,end='')
    print()

    for i in pick(primes(),5):
        print(i,end=' ')
        if i[3] > 100:
            break
    print('\n')


    # Test slice_gen; add your own test cases
    print('\nTesting slice_gen')
    for i in slice_gen('abcdefghijk', 3,7,1):
        print(i,end='')
    print()
       
    for i in slice_gen('abcdefghijk', 3,20,1):
        print(i,end='')
    print()
       
    for i in slice_gen(hide('abcdefghijklmnopqrstuvwxyz'), 3, 20, 3):
        print(i,end='')
    print()
       
    for i in slice_gen(primes(), 100,200,5):
        print(i,end=' ')
    print('\n')

    
    # Test alternate_all; you can add your own test cases
    print('Testing alternate_all')
    for i in alternate_all('abcde','fg','hijk'):
        print(i,end='')
    print('\n')
    
    for i in alternate_all(hide('ab'), hide('ac'),hide('ad')):
        print(i,end='')
    print('\n\n')


    # Test ListSI; you can add your own test cases
    print('Testing ListSI: no exception')
    l = ListSI(['a', 'b', 'c'])
    for i in l:
        print(i)
        # print(l._iter_count)
    l.append('z')
    print(l)
    print()

    print('Testing ListSI: exception by append')
    l = ListSI(['a', 'b', 'c'])
    try:
        for i in l:
            l.append('z')
            print('worked, but should have raised exception')
    except RuntimeError:
        print('correctly raised exception')
    print(l)
    print()
    #
    print('Testing ListSI: exception by del')
    l = ListSI(['a', 'b', 'c'])
    try:
        for i in l:
            del l[0]
            print('worked, but should have raised exception')
    except RuntimeError:
        print('correctly raised exception')
    print(l)
    print()

    print('Testing ListSI: no exception')
    l = ListSI(['a', 'b', 'c'])
    try:
        for i in l:
            for j in l:
                pass
        l.append('z')
    except RuntimeError:
        print('incorrectly raised exception')
    print(l)
    print()

    print('Testing ListSI: exception by append, nested 2')
    l = ListSI(['a', 'b', 'c'])
    try:
        for i in l:
            for j in l:
                l.append('z')
                print('worked, but should have raised exception')
    except RuntimeError:
        print('correctly raised exception')
    print(l)
    print()
    #
    print('Testing ListSI: exception by append, nested 1')
    l = ListSI(['a', 'b', 'c'])
    try:
        for i in l:
            for j in l:
                pass
            l.append('z')
            print('worked, but should have raised exception')
    except RuntimeError:
        print('correctly raised exception')
    print(l)
    print('\n')

    print('Testing fool_it')
    try:
        fool_it()
        print('worked, but should have raised exception')
    except RuntimeError:
        print('correctly raised exception')
    print('\n\n')
    
    
    
    import driver
    driver.default_file_name = 'bscq4S21.txt'
#     driver.default_show_exception=True
#     driver.default_show_exception_message=True
#     driver.default_show_traceback=True
    driver.driver()
    
    
