import sys

try:
    x = 1 / 0
except ZeroDivisionError as e:
    # print(e)
    try:
        x = 'i' + 1
    except TypeError as t:
        # print(t)
        raise TypeError('We cannot add str and int!')
