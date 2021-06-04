# A Ball is Prey; it updates by moving in a straight
#   line and displays as blue circle with a radius
#   of 5 (width/height 10).
from prey import Prey


class Ball(Prey):

    def __init__(self, x, y, angle, speed=0, width=0, height=0):
        Prey.__init__(self, x, y, width, height, angle, speed)
        self.radius = 5
        self.set_dimension(self.radius * 2, self.radius * 2)
        self.set_speed(5)

    def update(self):
        self.move()

    def display(self, canvas):
        canvas.create_oval(self._x - self.radius, self._y - self.radius,
                           self._x + self.radius, self._y + self.radius,
                           fill="blue")
