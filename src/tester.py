class API:
    def __init__(self, value):
        self.value = value
        pass

    def test1(self):
        print('Im API dad')


class APIChild(API):
    def __init__(self, value):
        super(APIChild, self).__init__(value)
        pass


a = APIChild('lol')
a.test1()
print(a.value)