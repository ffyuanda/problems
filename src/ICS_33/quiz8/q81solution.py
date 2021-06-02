# Put your imports here
import random, traceback
from performance import Performance
from nearestneighbor import closest_2d
# Put your code for performance analysis here

def doubling_signature(start=0, end=0) -> int or float:
    while start <= end:
        yield start
        start *= 2

def create_random(size: int = 0):
    out_list = []
    for i in range(size):
        out_list.append((random.random(), random.random()))
    return out_list


if __name__ == '__main__':
    coor_list = []
    x = doubling_signature(100, 25600)
    for i in x:
        coor_list = create_random(i)
        title = f"Nearest Neighbor, size = {i}"
        try:
            p = Performance(lambda: closest_2d(coor_list), title=title)
            p.evaluate()
            p.analyze()
            print()
        except ValueError:
            traceback.print_exc()
