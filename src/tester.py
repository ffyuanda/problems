# s = "a17,b__1,c__2"
# s_comma_split = s.split(',')
# if len(s_comma_split) == 1:  # no commas in s
#     s_space_split = s_comma_split[0].split(' ')
#     s_split = [i for i in s_space_split if i != '']
#     print(s_split)
# else:  # comma-split s
#     s_split = [i.strip() for i in s_comma_split]
#     print(s_split)
# print("{one}{two}{three}".format(one='1', two=2, three=3))
# def __init__(self, x, y):
#     self.x = x
namespace = dict()
func_str = """def test_func():
    print('YES!')"""
exec(func_str, namespace)
# print(namespace)
print(globals())
