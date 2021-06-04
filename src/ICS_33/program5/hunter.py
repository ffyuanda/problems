# The Hunter class is derived (in order) from both Pulsator and Mobile_Simulton.
#   It updates/displays like its Pulsator base, but is also mobile (moving in
#   a straight line or in pursuit of Prey), like its Mobile_Simultion base.

import model
from prey  import Prey
from pulsator import Pulsator
from mobilesimulton import Mobile_Simulton
from math import atan2


class Hunter(Pulsator, Mobile_Simulton):  
    def __init__(self, x, y):
        Pulsator.__init__(self, x, y)
        self.sight = 200
        Mobile_Simulton.set_speed(self, 5)
        Mobile_Simulton.randomize_angle(self)

    def update(self):
        preys = model.find(lambda x: isinstance(x, Prey))
        closest_prey, closest_range = None, self.sight

        for s in preys:
            if self.contains(s.get_location(), _range=self.sight):  # within distance of 200
                # print("SPOTTED!")
                if self.distance(s.get_location()) <= closest_range:
                    closest_range = self.distance(s.get_location())
                    closest_prey = s
            else:  # out of sight
                print("NO SIGHT!")

        if closest_prey is not None:  # closest_prey is found
            prey_x, prey_y = closest_prey.get_location()
            self_x, self_y = self.get_location()

            diff_x, diff_y = prey_x - self_x, prey_y - self_y
            hunt_angle = atan2(diff_y, diff_x)
            self.set_angle(hunt_angle)

        self.move()
        return Pulsator.update(self)
