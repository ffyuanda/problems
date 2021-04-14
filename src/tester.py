import re
pattern = r'^([1-9]|1[0-2])/(0[1-9]|[1-9]|[1-2][0-9]|[1-3][0-1])/?([0-9][0-9]|[1|2][9|0][0-9][0-9])?$'
pattern = re.compile(pattern)
print()
m = pattern.match('10/13/2099')
# m = re.match(pattern, '10/13/2099')
print(m.groups())