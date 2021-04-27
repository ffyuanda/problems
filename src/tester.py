from helpers import hide

# for index, i in enumerate(hide('3.14159265')):
#     print(index, i)
# n = 3
# while n > 0:
#     print(n)
#     n -= 1
#     if n == 0:
#         n=3


class iter_test:
    def __init__(self):
        self.countdown = 5

    def __iter__(self):
        return self

    def __next__(self):
        self.countdown -= 1
        if self.countdown <=0 :
            raise StopIteration
        return self.countdown


test = iter_test()
for i in test:
    print(i)