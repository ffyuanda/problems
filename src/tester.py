# from collections import defaultdict
# d = defaultdict()
# print(isinstance(d, dict))
# print(".".join(["1", "2"]))
# l = ['a', 'b']
# for i, v in enumerate(l):
#     print(i, v)
s = "a|baab|aca|||c"
x = "a|baab|ac||||ac"
# s.pop()
# for i in s:
#     print(i)
# print(s.union())
# l = "123"
# l = iter(l)
#
# for i in range(45):
#     print(next(l))
print(min(s, x, key=lambda y: y.count('|')))
# print(s)