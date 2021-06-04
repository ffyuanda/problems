# A Floater is Prey; it updates by moving mostly in
#   a straight line, but with random changes to its
#   angle and speed, and displays as ufo.gif (whose
#   dimensions (width and height) are computed by
#   calling .width()/.height() on the PhotoImage 

import math
from PIL.ImageTk import PhotoImage
from prey import Prey
from random import random


class Floater(Prey): 
    def __init__(self, x, y, angle, speed=0, width=0, height=0):
        Prey.__init__(self, x, y, width, height, angle, speed)
        self.radius = 5
        self._image = PhotoImage(file="ufo.gif")
        self.set_dimension(self._image.width(), self._image.height())
        self.set_speed(5)

    def update(self):
        rand_num = random()
        if rand_num <= 0.3:  # changed
            print("changed!")
            speed_change = random() - 0.5
            angle_change = (random() - 0.5) * math.pi
            if 3 <= self.get_speed() <= 7:
                self.set_speed(self.get_speed() + speed_change)
            self.set_angle(self.get_angle() + angle_change)
        else:  # not changed
            pass
        self.move()

    def display(self, canvas):
        canvas.create_image(self.get_location(), image=self._image)
