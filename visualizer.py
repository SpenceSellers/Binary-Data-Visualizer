#!/usr/bin/python

import Image
import ImageFilter
import numpy
import os
import math
import itertools
import colormaps
from optparse import OptionParser



def d2xy(n, d):
    """
    take a d value in [0, n**2 - 1] and map it to
    an x, y value (e.g. c, r).
    """
    #assert(d <= n**2 - 1)
    t = d
    x = y = 0
    s = 1
    while (s < n):
        rx = 1 & (t >> 1)
        ry = 1 & (t ^ rx)
        x, y = rot(s, x, y, rx, ry)
        x += s * rx
        y += s * ry
        t >>= 2
        s <<= 1
    return x, y

def rot(n, x, y, rx, ry):
    """
    rotate/flip a quadrant appropriately
    """
    if ry == 0:
        if rx == 1:
            x = n - 1 - x
            y = n - 1 - y
        return y, x
    return x, y

def cbool(tf):
    return 1 if tf else 0

def xy2d(n, x, y):
    rx = 0
    ry = 0
    s = n/2
    d = 0
    while s > 0:
        rx = cbool((x & s) > 0)
        ry = cbool((y & s) > 0)

        d += s * s * ((3 * rx) ^ ry)
        x, y = rot(s, x, y, rx, ry)
        
        s /= 2
    return d
    
def nearest_power(n):
    power = 1
    while power < n:
        power <<= 1
    return power >> 1



def mask(data, start, end, maskval):
    for i in itertools.chain(range(0, start), range(end, len(data))):
        data[i] = maskval
    return data

def main():
    parser = OptionParser()
    parser.add_option('-f', help='File to use', dest='file')
    parser.add_option('-l', help='Length in bytes to read', dest='len', type='int')
    parser.add_option('-n',
                      help='Side size of image to generate',
                      dest='size',
                      type='int',
                      default=-1)
    parser.add_option('--offset', '-o', type='int', dest='offset', default=0)
    parser.add_option('--mask', type='int', nargs=3)
    parser.add_option('--scale', type='int', dest='scale', default = -1)
    parser.add_option('-m', '--mapping', dest='mapping', default='Weird')
    
    options, args = parser.parse_args()
    file_size = os.path.getsize(options.file)
    sizen = None
    data_length = options.len or file_size - options.offset
    if options.size <= 0:
        sizen = nearest_power(math.sqrt(data_length))
        print "Setting image size to %s" % sizen
        if sizen > 4048:
            print "Size too large, forcing size to be 2048"
            sizen = 2048
    else:
        sizen = options.size

    if sizen <= 64 and options.scale == -1:
        print "Image is going to be very small, setting scale to 8"
        options.scale = 8
    elif sizen <= 256 and options.scale == -1:
        print "Image is going to be small, setting scale to 3"
        options.scale = 3
    img = Image.new("RGB", (sizen, sizen))

    data_to_be_shown = min(sizen ** 2, data_length)
    print "Showing {0} of {1} bytes, ({2} %)"\
        .format(data_to_be_shown, data_length, (data_to_be_shown * 100.0/data_length))

    f = open(options.file, 'r')
    f.seek(options.offset)
    data = bytearray(f.read(options.len or sizen**2))
    if options.mask:
        data = mask(data, options.mask[0], options.mask[1], options.mask[2])
    mapper = colormaps.__dict__[options.mapping](data)

    
    print "Done reading"
    for i in range(len(data)):
        if i > sizen**2 - 1:
            print "Incomplete"
            break

        if i % 100000 == 0:
            print "Processed %s bytes (%s)" % (i, i * 1.0 / len(data))

        color = mapper.color(i)
        if color == (0,0,0): #Optimize for black
            continue
        pos = d2xy(sizen, i)
        img.putpixel(pos, color)

    print "Showing"
    if options.scale > 1:
        img = img.resize((sizen * options.scale, sizen * options.scale))
    img.show()
    
if __name__ == "__main__":
    main()
