class Point:
    _fields = ['x', 'y']
    _mutable = False

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return 'Point(x={x},y={y})'.format(x=self.x, y=self.y)

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y
