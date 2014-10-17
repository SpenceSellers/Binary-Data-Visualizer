import Image
import functools
import memoize
import ccode
globalMap = None

class Positioner(object):
    def __init__(self):
        self.sizes = {}

    def get_map_for_size(self, size):
        if self.sizes[size]:
            return self.sizes[size]
        else:
            self.gen_map(size)
            return self.get_map_for_size(size)
        
    def gen_map(self, size):
        if self.sizes.has_key(size):
            return
        print 'Generating positioning for size {}'.format(size)
        self.sizes[size] = []
        for i in range(size**2):
            val = d2xy(size, i)
            self.sizes[size].append(val)
        print "Done generating positioning."

    def get(self, size, i):
        if self.sizes.has_key(size):
            return self.sizes[size][i]
        else:
            self.gen_map(size)
            return self.get(size, i)

    def convert(self, size, xy):
        x, y = xy
        return y * size + x
            
positioner = Positioner() # Make a global positioner singleton for efficiency.

def nearest_power(n):
    power = 1
    while power < n:
        power <<= 1
    return power >> 1

def mask(data, start, end, maskval):
    for i in itertools.chain(range(0, start), range(end, len(data))):
        data[i] = maskval
    return data

def d2xy(n, d):
    return ccode.d2xy(n, d)

class View(object):
    def __init__(self, data, mapper_constructor, size = None):
        self.data = data
        self.mapper = mapper_constructor(data)

        if size:
            self.size = size
        else:
            self.size = nearest_power(len(data))

        self.default_color = self.mapper.predictDefault()
        
    def get_pos(self, index):
        return positioner.get(self.size, index)
    
    def gen_image(self):
        img = Image.new("RGB", (self.size, self.size), color=self.default_color)
        pixels = list(img.getdata())
        for i in range(len(self.data)):
            if i > self.size**2 - 1:
                print "Not all data has been displayed."
                break

            if i % 100000 == 0:
                print "Processed %s bytes (%s)" % (i, i * 1.0 / len(self.data))
    
            color = self.mapper.color(i)
            if color == self.default_color: #Optimize for the default.
                continue
            
            pos = self.get_pos(i)
            
            pixels[pos] =  color
        img.putdata(pixels)

        return img
        
        
