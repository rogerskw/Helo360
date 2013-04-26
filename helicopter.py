import pygame

# These values all relate to playing the signal at 44100 Hz
header = [-4]*100
wait = [0]*5199
on = [1.5]*33 + [-4]*15
off = [1.5]*13 + [-4]*35
sig = on*32

def add_header_wait(sig):
    s = header + sig + wait
    return s*100

if __name__ == '__main__':
    # Initialize pygame stuff
    pygame.init()
    pygame.mixer.init()
    pygame.joystick.init()

    x360 = pygame.joystick.Joystick(0)
    x360.init()

    while True:
        pygame.event.wait() # Wait for something to happen before doing anything
        # Left stick is axis 0 and 1, right trigger is axis 5
        x_axis = x360.get_axis(0)
        y_axis = x360.get_axis(1)
        throttle = x360.get_axis(5)
        print throttle
        print x_axis
        print y_axis
