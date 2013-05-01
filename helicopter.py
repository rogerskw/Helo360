import pygame
import numpy
import matplotlib.pyplot as plt
import sys
#from datetime import datetime

# These values all relate to playing the signal at 44100 Hz
header_len = 100
bit_len = 48
wait_len = 5199
bits_per_sig = 32

header = [-40000]*header_len
wait = [0]*wait_len
on = [100000]*33 + [-40000]*15
off = [100000]*13 + [-40000]*35
sig = header + on*bits_per_sig + wait

bin_sig = [0]*bits_per_sig

# Converts the binary signal array to the signal that the computer actually
# outputs as audio
def create_audiosig(binary_sig):
    for i in xrange(len(binary_sig)):
        pos = header_len + i*bit_len
        bit = binary_sig[i]
        b = on
        if (bit == 0):
            b = off
        sig[pos:pos+bit_len] = b
    sig[header_len + bit_len*bits_per_sig:header_len+bit_len*bits_per_sig+wait_len ] = wait
    return sig

# Converts a number, val, to a binary array of size n
# [val_min,val_max] => [0,2**n) => [bit0,bit1,...bitn)
# val = number to be converted
# n = number of bits for the binary array
# val_min = the minimum possible value for n
# val_max = the maximum possible value for n
def num2binary(val,n, val_min, val_max):
    r = val_max - val_min # Calculate the range
    val = val - val_min # [val_min,val_max] => [0,r]
    new_max = 2**n-1
    step_size = r / float(new_max)
    new_val = int(round(val/step_size))
    ans = [0]*n
    bin_val = bin(new_val)
    l = len(bin_val)
    val_curr = new_val
    for i in xrange(2,l):
        ans[i-2] = val_curr % 2
        val_curr = val_curr / 2
    for i in xrange(l,n):
        ans[i] = 0
    ret = ans
    for i in xrange(0,n):
        ret[i] = ans[n-i-1]
    return ret

# Calculates the checksum for the binary_sig according to the Helo TC helicopter
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

# Finds the binary array to represent the throttle in the signal
def throttle(trigger_val):
    return num2binary(trigger_val,8,-1,1)

# This just substitues in standard values for the signal that is not throttle
# or checksum. These values should be zero x,y movement.
def restofsignal():
    return [1,0,0,0,1,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0]

def test_script(t):
    bin_sig[0:8] = throttle(t)
    bin_sig[8:28] = restofsignal()
    bin_sig[28:32] = checksum(bin_sig)

    print bin_sig
    sig = create_audiosig(bin_sig)*60
    print len(sig)
    pygame.mixer.init(44100,-16,1,2**16)
    num_ary = numpy.array(sig)
    plt.plot(num_ary)
    plt.savefig('generated_signal.jpg')

    if (sys.argv[1] == 'on'):
        s = pygame.sndarray.make_sound(num_ary)
        s.play()

    plt.show()

if __name__ == '__main__':
    test_script(float(sys.argv[2]))

'''


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
