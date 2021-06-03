import controller
import model   # Calls to update in update_all are passed a reference to model

Use the reference to this module to pass it to update methods

from ball      import Ball
from floater   import Floater
from blackhole import Black_Hole
from pulsator  import Pulsator
from hunter    import Hunter


# Global variables: declare them global in functions that assign to them: e.g., ... = or +=



#return a 2-tuple of the width and height of the canvas (defined in the controller)
def world():
    return (controller.the_canvas.winfo_width(),controller.the_canvas.winfo_height())

#reset all module variables to represent an empty/stopped simulation
def reset ():
    pass


#start running the simulation
def start ():
    pass


#stop running the simulation (freezing it)
def stop ():
    pass


#step just one update in the simulation
def step ():
    pass


#remember the kind of object to add to the simulation when an (x,y) coordinate in the canvas
#  is clicked next (or remember to remove an object by such a click)   
def select_object(kind):
    pass


#add the kind of remembered object to the simulation (or remove all objects that contain the
#  clicked (x,y) coordinate
def mouse_click(x,y):
    pass


#add simulton s to the simulation
def add(s):
    pass
    

# remove simulton s from the simulation    
def remove(s):
    pass
    

#find/return a set of simultons that each satisfy predicate p    
def find(p):
    pass


# for each simulton in this simulation, call update (passing model to it) 
#this function should loop over one set containing all the simultons
#  and should not call type or isinstance: let each simulton do the
#  right thing for itself, without this function knowing what kinds of
#  simultons are in the simulation
def update_all():
    pass

#How to animate: 1st: delete all simultons on the canvas; 2nd: call display on
#  all simulton being simulated, adding each back to the canvas, maybe in a
#  new location; 3rd: update the label defined in the controller for progress 
#this function should loop over one set containing all the simultons
#  and should not call type or isinstance: let each simulton do the
#  right thing for itself, without this function knowing what kinds of
#  simultons are in the simulation
def display_all():
    pass
