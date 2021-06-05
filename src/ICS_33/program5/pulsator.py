# A Pulsator is a Black_Hole; it updates as a Black_Hole
#   does, but also by growing/shrinking depending on
#   whether or not it eats Prey (and removing itself from
#   the simulation if its dimension becomes 0), and displays
#   as a Black_Hole but with varying dimensions 


from blackhole import Black_Hole


class Pulsator(Black_Hole): 
    def __init__(self, x, y):
        Black_Hole.__init__(self, x, y)
        self.counter = 0

    def update(self):
        eaten = Black_Hole.update(self)
        width, height = self.get_dimension()

        if len(eaten) > 0:  # ate something
            self.radius += 0.5 * len(eaten)

            self.set_dimension(width + 1 * len(eaten), height + 1 * len(eaten))  # after eat
            self.counter = 0  # reset

        else:  # nothing eaten
            self.counter += 1

        if self.counter % 30 == 0 and self.counter > 0:  # shirk if hungry for every 30 updates
            self.radius -= 0.5
            self.set_dimension(width - 1, height - 1)
            self.counter = 0

        if self.radius <= 0:  # kill itself
            eaten.add(self)
        return eaten
