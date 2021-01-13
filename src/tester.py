def painter(num, curr=0):

    curr += 1
    if curr >= num:
        print('*' * curr)
        return
    else:
        print('*' * curr)
        painter(num, curr)
        print('*' * curr)

painter(3)
