from q4solution import ListSI

# Should not raise exception
def test1():
    l = ListSI(['a', 'b', 'c'])
    for _ in l:
        pass
    l.append('z')
    return l

# Should raise exception
def test2():
    l = ListSI(['a', 'b', 'c'])
    for _ in l:
        l.append('z')

# Should raise exception
def test3():
    l = ListSI(['a', 'b', 'c'])
    for _ in l:
        del l[0]

# Should not raise exception
def test4():
    l = ListSI(['a', 'b', 'c'])
    for _ in l:
        for _ in l:
            pass
    l.append('z')
    return l
    
# Should raise exception
def test5():
    l = ListSI(['a', 'b', 'c'])
    for _ in l:
        for _ in l:
            l.append('z')

# Should raise exception
def test6():
    l = ListSI(['a', 'b', 'c'])
    for _ in l:
        for _ in l:
            pass
        l.append('z')
