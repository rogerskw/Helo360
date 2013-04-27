import pygame


# These values all relate to playing the signal at 44100 Hz
header = [-4]*100
wait = [0]*5199
on = [2]*33 + [-4]*15
off = [2]*13 + [-4]*35
sig = on*32

def add_header_wait(audiosig):
    s = header + audiosig + wait
    return s

def create_audiosig(binary_sig):
    sig = []
    for bit in binary_sig:
        b = on
        if (bit == 0):
            b = off
        sig = sig + b
    return sig

def checksum(binary_sig):
    sig_bytes = [binary_sig[0:8], binary_sig[8:16], binary_sig[16:24]]
    carry = 0
    check = [0]*8
    for bit_num in reversed(xrange(8)):
        c = carry + sig_bytes[0][bit_num] + sig_bytes[1][bit_num] + sig_bytes[2][bit_num]
        carry = c / 2
        check[bit_num] = c % 2
    while carry != 0:
        for bit_num in reversed(xrange(8)):
            c = carry + check[bit_num]
            carry = c / 2
            check[bit_num] = c % 2
            if carry == 0:
                break
    return check[:4]
'''
def throttle(trigger_val):
    print 5

x = [1,1,0,1,1,1,1,1,1,0,0,0,1,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0]
x = [1]*28
c = checksum(x)

sig = create_audiosig(x+c)
full_sig = add_header_wait(sig)
print len(sig)
print len(full_sig)


if __name__ == '__main__':
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

'''
