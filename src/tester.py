from collections import namedtuple
DataTuple = namedtuple('DataTuple', ['type', 'message', 'token'])
x = DataTuple(123, 123, 123)
print(type(x))