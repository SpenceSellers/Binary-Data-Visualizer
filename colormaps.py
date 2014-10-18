import classifier
import ccode
class ColorMap(object):
    def __init__(self, data):
        self.data = data

    def getByte(self, index):
        return self.data[index]

    def predictDefault(self):
        return (0,0,0)

    def greyscale(self, val):
        return (val, val, val)
    
    def getByteOrElse(self, index, elseval):
        if index < 0 or index >= len(self.data):
            return elseval
        else:
            return getByte(index)
    def color(self, index):
        return self.colorVal(self.getByte(index))
        
    def colorVal(self, val):
        return (0,0,0)

    def average(self, colorvals):
        redAccum = 0
        greenAccum = 0
        blueAccum = 0

        scale = 1.0/len(colorvals)
        for color in colorvals:
            redAccum += scale * color[0]
            greenAccum += scale * color[1]
            blueAccum += scale * color[2]

        return (redAccum, greenAccum, blueAccum)
        

class Luminosity(ColorMap):
    def colorVal(self, val):
        return self.greyscale(val)

class Mod2(ColorMap):
    def colorVal(self, val):
        val = (val % 2) * 255
        return self.greyscale(val)

class WeirdOld(ColorMap):
    def colorVal(self, val):
        return ((val >> 4) * 16,val ,(val & 15)*16)

class Weird(ColorMap):
    def colorVal(self, val):
        return ccode.weirdMap(val)
        #return (max((val >> 7) * 255, val >> 4), val, (val & 15)*16)


class BitColors(ColorMap):
    def colorVal(self, char):
        green = char &   0b11100000
        red = char &     0b00011100
        blue = char &    0b00000011
        return (red, green, blue)

class Frequency(ColorMap):
    def __init__(self, data):
        super(Frequency, self).__init__(data)
        self.mapper = classifier.makeFreqMapper(data)

    def colorVal(self, val):
        return self.mapper(val)

class AverageWeird(ColorMap):
    def color(self, index):
        bytes = [self.getByteOrElse(index - 1, 0),
                  self.getByteOrElse(index, 0),
                  self.getByteOrElse(index, 1)]
        color = self.average(colors)

        
