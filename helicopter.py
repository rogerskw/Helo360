import pygame
import numpy
import sys

bits_per_byte = 8

# These values all relate to playing the signal at 44100 Hz
header_len = 100
bit_len = 48
wait_len = 5199
bits_per_sig = 32
up_amp = 2**14
down_amp = -(2**14)
empty_amp = 0

header = [down_amp]*header_len
wait = [empty_amp]*wait_len
on = [up_amp]*33 + [down_amp]*15
off = [up_amp]*13 + [down_amp]*35
sig = header + on*bits_per_sig + wait

bin_sig = [0]*bits_per_sig
s = None

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
    sig_bytes = [binary_sig[0:bits_per_byte], binary_sig[bits_per_byte:2*bits_per_byte], binary_sig[2*bits_per_byte:3*bits_per_byte]]
    carry = 0
    check = [0]*bits_per_byte
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
def restofsignal(x_axis_val=0, y_axis_val=0):
    return [1,0,0,0,1,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0]

def create_bin_sig(throttle_val=-1, x_axis_val=0, y_axis_val=0):
    bin_sig[0:8] = throttle(throttle_val)
    bin_sig[8:28] = restofsignal(x_axis_val,y_axis_val)
    bin_sig[28:32] = checksum(bin_sig)

def test_script(t):

    bin_sig[0:8] = throttle(t)
    bin_sig[8:28] = restofsignal()
    bin_sig[28:32] = checksum(bin_sig)

    print bin_sig
    sig = create_audiosig(bin_sig)*1000
    pygame.mixer.init(44100,-16,1)


    num_ary = numpy.array(sig,dtype=numpy.dtype('int16'))
    if (sys.argv[1] == 'on'):
        s = pygame.sndarray.make_sound(num_ary)
        s.play()

    while (pygame.mixer.get_busy()):
        None

if __name__ == '__main__':
    test_script(float(sys.argv[2]))

'''
    x360.init()
    pygame.init()
    pygame.mixer.init(44100,-16,1)

if __name__ == '__main__':
    pygame.init()
    pygame.mixer.init(44100,-16,1)
    while True:
        pygame.event.wait() # Wait for something to happen before doing anything
        # Left stick is axis 0 and 1, right trigger is axis 5
        x_axis = x360.get_axis(0)
        y_axis = x360.get_axis(1)
        throttle_trig = x360.get_axis(5)
        create_bin_sig(throttle_trig,x_axis,y_axis)
        sig = create_audiosig(bin_sig)*120
        if (s != None):
            s.stop()
        s = pygame.sndarray.make_sound(sig)
        s.play()


    s = pygame.sndarray.make_sound(sig)
    s.play()

'''
