# Put your imports here
import cProfile, pstats, random, traceback
from nearestneighbor import closest_2d

# Put your code for profile analysis here

def create_random(size: int = 0) -> list:
    out_list = []
    for i in range(size):
        out_list.append((random.random(), random.random()))
    return out_list

coor_list = create_random(25600)

def perform_task():
    closest_2d(coor_list)

cProfile.run("perform_task()", "profile")
p = pstats.Stats('profile')
p.strip_dirs().sort_stats('calls').print_stats(12)
p.strip_dirs().sort_stats('time').print_stats(12)
