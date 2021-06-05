from pulsator import Pulsator
from blackhole import Black_Hole

"""
The Special object acts like a Pulsator but in the opposite way.
It shrinks every time it eats an object, symbolizing that it is condensing
energy. And after it eats more than 5 objects, it enters "explode" mode, in
which it expands by its expand_factor (default is 8), and it turns red to
symbolize that it is exploding. And after its explode lifespan (default 15 updates)
it will remove itself from the canvas (just like the Pulsator).
"""


class Special(Pulsator, Black_Hole):
    def __init__(self, x, y):
        Pulsator.__init__(self, x, y)
        self.explode = False
        self.expand = False
        self.countdown = 15
        self.expand_factor = 8

    def update(self):
        eaten = Black_Hole.update(self)
        width, height = self.get_dimension()

        if self.explode:

            if self.expand:
                self.radius *= self.expand_factor
                self.set_dimension(width * self.expand_factor, height * self.expand_factor)
                self.expand = False

            self.countdown -= 1
            if self.countdown <= 0:
                eaten.add(self)
                return eaten

        if len(eaten) > 0 and not self.explode:  # ate something
            self.radius -= 0.5 * len(eaten)
            self.set_dimension(width - 1 * len(eaten), height - 1 * len(eaten))

            self.counter += 1  # reset

        if self.counter > 5 and not self.explode:
            self.explode = True
            self.expand = True

        return eaten

    def display(self, canvas):
        canvas.create_oval(self._x - self.radius, self._y - self.radius,
                           self._x + self.radius, self._y + self.radius,
                           fill="red" if self.explode else "black")
