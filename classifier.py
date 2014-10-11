import operator
def countBytes(data):
    
    m = {}
    for i in range(0,256):
        m[i] = 0

    for byte in data:
        m[byte] += 1

    return m

def scale(val, src_range, dst_range):
    return int((
        (val - src_range[0]) / (src_range[1]-src_range[0]))\
        * (dst_range[1]-dst_range[0]) + dst_range[0])

def makeFreqMapper(data):
    counts = countBytes(data)
    sortd = sorted(counts.items(), key=operator.itemgetter(0))

    maximum = max([x[1] for x in sortd])
    minimum = min([x[1] for x in sortd])
    print "Minimum is {}".format(minimum)
    print "Maximum is {}".format(maximum)
    dest_range = (0.0,255.0)
    src_range = (minimum * 1.0, maximum * 1.0)

    def mapper(byte):
        count = counts[byte]
        val = scale(count, src_range, dest_range)
        return (val, val, val)

    return mapper

    
