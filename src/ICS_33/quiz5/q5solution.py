def compare(a : str, b : str) -> str:
    if a[0:1] > b[0:1]:
        return '>'
    elif a[0:1] < b[0:1]:
        return '<'
    else:  # must be equal for now
        if len(a) > 0 and len(b) > 0:
            result = compare(a[1:], b[1:])
        else:
            return '='
        return result

   
def is_sorted(l : list) -> bool:
    if len(l) < 2:
        return True
    else:
        if l[1:2] < l[0:1]:
            return False
        return is_sorted(l[1:])


def merge (l1 : list, l2 : list) -> list:
    if len(l1) == 0 or len(l2) == 0:
        return l2 if len(l1) == 0 else l1
    else:
        if l1[0:1] > l2[0:1]:
            return l2[0:1] + merge(l1, l2[1:])
        elif l1[0:1] < l2[0:1]:
            return l1[0:1] + merge(l1[1:], l2)
        else:
            return l1[0:1] + l2[0:1] + merge(l1[1:], l2[1:])


def sort(l : list) -> list:
    if len(l) <= 2:
        if len(l) == 2:
            return [l[1], l[0]] if l[0] > l[1] else [l[0], l[1]]
        else:
            return [l[0]]
    else:
        return merge(sort(l[:len(l) // 2]), sort(l[len(l) // 2:]))


def max_value(gifts : ((int,int),) , weight_limit : int) -> int:
    if len(gifts) == 0: # base case
        return 0
    else:
        w, v = gifts[0]
        if weight_limit < w:
            return max_value(gifts[1:], weight_limit)
        return max(max_value(gifts[1:], weight_limit), v + max_value(gifts[1:], weight_limit - w))


if __name__=="__main__":
    import random 
       
    print('\nTesting compare')
    print(compare('',''))
    print(compare('','abc'))
    print(compare('abc',''))
    print(compare('abc','abc'))
    print(compare('bc','abc'))
    print(compare('abc','bc'))
    print(compare('aaaxc','aaabc'))
    print(compare('aaabc','aaaxc'))
   
    
    print('\nTesting is_sorted')
    print(is_sorted([]))
    print(is_sorted([1,2,3,4,5,6,7]))
    print(is_sorted([1,2,3,7,4,5,6]))
    print(is_sorted([1,2,3,4,5,6,5]))
    print(is_sorted([7,6,5,4,3,2,1]))
    
    print('\nTesting merge')
    print(merge([],[]))
    print(merge([],[1,2,3]))
    print(merge([1,2,3],[]))
    print(merge([1,2,3,4],[5,6,7,8]))
    print(merge([5,6,7,8],[1,2,3,4]))
    print(merge([1,3,5,7],[2,4,6,8]))
    print(merge([2,4,6,8],[1,3,5,7]))
    print(merge([1,2,5,7,10],[1,2,6,10,12]))


    print('\nTesting sort')
    print(sort([1,2,3,4,5,6,7]))
    print(sort([7,6,5,4,3,2,1]))
    print(sort([4,5,3,1,2,7,6]))
    print(sort([1,7,2,6,3,5,4]))
    l = list(range(20))  # List of values 0-19
    for i in range(10):  # Sort 10 times
        random.shuffle(l)
        print(sort(l),sep='-->')
    
    
    print('\nTesting max_value')
    gifts1 = ((10,60), (20,100), (30,120))
    print(max_value(gifts1,50))
    gifts2 = ((10,70),(15,80),(20,140),(20,150),(30,200))
    print(max_value(gifts2,50))
    gifts3 = ((4, 35), (4, 40), (7, 45), (18, 30), (4, 45), (19, 40), (4, 10), (10, 40), (13, 25), (9, 40), (9, 15), (19, 15))
    print(max_value(gifts3,50))

    print()

   
    import driver
    driver.default_file_name = 'bscq5S21.txt'
#     driver.default_show_traceback = True
#     driver.default_show_exception = True
#     driver.default_show_exception_message = True
    driver.driver()
