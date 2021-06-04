# The Black_Hole class is derived from Simulton; for updating it finds+removes
#   objects (of any class derived from Prey) whose center is contained inside
#   its radius (returning a set of all eaten simultons), and displays as a
#   black circle with a radius of 10 (width/height 20).
# Calling get_dimension for the width/height (for containment and displaying)'
#   will facilitate inheritance in Pulsator and Hunter

import model
from simulton import Simulton
from prey import Prey


class Black_Hole(Simulton):
    def __init__(self, x, y, width=0, height=0):
        Simulton.__init__(self, x, y, width, height)
        self.radius = 10
        self.set_dimension(self.radius * 2, self.radius * 2)

    def update(self):
        eaten = set()
        preys = model.find(lambda x: isinstance(x, Prey))
        for s in preys:
            if self.contains(s.get_location()):
                eaten.add(s)
        return eaten

    def display(self, canvas):
        canvas.create_oval(self._x - self.radius, self._y - self.radius,
                           self._x + self.radius, self._y + self.radius,
                           fill="black")

    def contains(self, location, _range=None):
        if _range is None:
            return True if self.distance(location) < self.radius else False
        else:
            return True if self.distance(location) < _range else False
