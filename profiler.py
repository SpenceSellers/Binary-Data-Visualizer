import cProfile
import sys
import View
import colormaps
f = open(sys.argv[1], 'rb')
data = bytearray(f.read())
cProfile.run("View.View(data, colormaps.Weird, size=1024).gen_image()")
