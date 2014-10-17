import Image

def nearest_power(n):
    power = 1
    while power < n:
        power <<= 1
    return power >> 1

def mask(data, start, end, maskval):
    for i in itertools.chain(range(0, start), range(end, len(data))):
        data[i] = maskval
    return data
# Thanks to github user dentearl for the original d2xy code
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

class View(object):
    def __init__(self, data, mapper_constructor, size = None):
        self.data = data
        self.mapper = mapper_constructor(data)

        if (size):
            self.size = size
        else:
            self.size = nearest_power(len(data))

        self.default_color = self.mapper.predictDefault()
        
    def get_pos(self, index):
        return d2xy(self.size, index)
    def gen_image(self):
        img = Image.new("RGB", (self.size, self.size), color=self.default_color)
        
        for i in range(len(self.data)):
            if i > self.size**2 - 1:
                print "Incomplete"
                break

            if i % 100000 == 0:
                print "Processed %s bytes (%s)" % (i, i * 1.0 / len(self.data))
    
            color = self.mapper.color(i)
            if color == self.default_color: #Optimize
                continue
            pos = self.get_pos(i)
            
            img.putpixel(pos, color)

        return img
        
        
