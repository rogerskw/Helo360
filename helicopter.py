import pygame


# Initialize pygame stuff
pygame.init()
pygame.joystick.init()

x360 = pygame.joystick.Joystick(0)
x360.init()

pygame.mixer.init()


'''
This section is devoted to setting up the sound files for controlling the helicopter
It reads in prerecorded wav files and puts them into a 3 dimensional array (3x3x3)
Each element in the array representing a specific direction with respect to the center
of the array.
'''
alts = ["min","mid","max"]
north_south = ["n","0","s"]
east_west = ["e","0","w"]

signals = [[[None]*len(alts)]*len(east_west)]*len(north_south)

for alt_i in xrange(len(alts)):
    alt = alts[alt_i]
    for dir_x_i in xrange(len(east_west)):
        dir_x = east_west[dir_x_i]

        for dir_y_i in xrange(len(north_south)):
            dir_y = north_south[dir_y_i]
            print alt + " " + dir_x + " " + dir_y
            f_name = str(alt + "_" + dir_x + "_" + dir_y + ".wav")
            print f_name
            signals[alt_i][dir_x_i][dir_y_i] = str(f_name)

print signals

s = signals[0][1][1] # initialize s to being low alt and no direction

'''
This section relates to the Xbox 360 controller.
It reads in information about the direction and throttle from the controller
and links it to the appropriate sound file
'''

curr_state = [0,1,1]

while True:
    pygame.event.wait() # Wait for something to happen before doing anything
    # Left stick is axis 0 and 1, right trigger is axis 5
    x_axis = int(round(x360.get_axis(0)))
    y_axis = int(round(x360.get_axis(1)))
    throttle = int(round(x360.get_axis(5)))
    print throttle
    print x_axis
    print y_axis
    print signals[throttle+1][x_axis+1][y_axis+1]
    if (curr_state[0] != throttle or curr_state[1] != x_axis or curr_state[2] != y_axis):

        curr_state[0] = throttle
        curr_state[1] = x_axis
        curr_state[2] = y_axis
        #s = signals[right_trigger_val][x_axis_val][y_axis_val]

