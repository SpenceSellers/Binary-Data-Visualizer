import Image
import functools
import memoize
import ccode

def nearest_power(n):
    power = 1
    while power < n:
        power <<= 1
    return power >> 1

def mask(data, start, end, maskval):
    for i in itertools.chain(range(0, start), range(end, len(data))):
        data[i] = maskval
    return data

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
        return ccode.d2xy(self.size, index)

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
        
        
