# import re
#
# pattern = "^([a-z]+)(_prev)([0-9]*?)$"
# m = re.match(pattern, "sasda_prev")
# print(len(m.group(3)))

# print(['2'] * 3)
#
# from collections import defaultdict
#
# i = defaultdict(int)
# i['x'] = 1
# # i.pop('x')
# print(i)
# x = '12345'
# x=x.lower()
# print(x.index('13'))
import math
def truncate(number, digits) -> float:
    stepper = 10.0 ** digits
    return math.trunc(stepper * number) / stepper

x = 3.14159265358979323846264338327950228625461732116543
# y = 3.14159265358979323846264338327950228625461732116543
# print(str(int(x*100000000000000000000000000)))
# print("{:.50f}".format(x))
# print(format(x, '.60g'))
# print(list(x))
import decimal

# print(math.ulp(x))


def real_divide(dividend, divisor, digits=100):
    quo_str = ''
    count = 1
    add_zero = 1
    while digits > 0:
        if dividend // divisor == 0 and dividend % divisor != 0:
            dividend *= 10
            if add_zero == 1:  # add_zero should only perform once
                quo_str += '0'
                if count == 0:  # after the decimal point
                    digits -= 1
            if count == 1:
                quo_str += '.'
                count = 0
            continue

        add_zero = 0

        quo = dividend // divisor
        quo_str += str(quo)

        if count == 1:  # we are passing the decimal point
            quo_str += '.'
            count = 0

        subtract = quo * divisor
        if subtract == 0:
            break

        dividend = dividend - subtract
        if count == 0: # after the decimal point
            digits -= 1

    return quo_str


# def real_divide2(dividend, divisor, digits=100):
#     quo_str = ''
#     add_decimal = True
#     add_zero = True
#     while digits > 1:
#         if dividend // divisor == 0 and dividend % divisor != 0:
#             dividend *= 10
#             if add_zero:
#                 quo_str += '0'
#                 if add_decimal:
#                     quo_str += '.'
#                     add_decimal = False
#                 else:
#                     digits -= 1
#             continue
#
#         add_zero = False
#
#         quo, dividend = dividend // divisor, dividend % divisor
#         quo_str += str(quo)
#
#         if add_decimal:
#             quo_str += '.'
#             add_decimal = False
#         if not add_decimal:
#             digits -= 1
#     return quo_str

def real_divide2(dividend, divisor, digits=100):
    quo_str = '0'
    add_decimal = True
    while digits > 0:
        if dividend // divisor == 0 and dividend % divisor != 0:
            dividend *= 10
            if add_decimal:
                quo_str += '.'
                add_decimal = False
            quo_str += '0'
            continue

        quo, dividend = dividend // divisor, dividend % divisor
        quo_str = quo_str[:-1] + str(quo)
        if dividend == 0:
            break

        if add_decimal:
            quo_str += '.'
            add_decimal = False
        else:
            digits -= 1
    return quo_str


result = real_divide2(2, 3)
print(result)
print(len(result))
print(len("14159265358979323846264338327950228625461732116543"))
# print(math.pi)