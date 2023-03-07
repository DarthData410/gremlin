# ---> https://pypi.org/project/bitstruct/
import chardet
from bitstruct import *

# BASE EXAMPLE:
bs = pack('u1u3u4s16', 1, 2, 3, -4)
#b'\xa3\xff\xfc'
upbs = unpack('u1u3u4s16', b'\xa3\xff\xfc')
#(1, 2, 3, -4)
cs = calcsize('u1u3u4s16')
#24


# ---> bitstruct packing and unpacking for enclosing in messages.:
# --> This would be the manuscript step to execute as well as update messages back to parent actor from children
# pack bit:
bp1 = pack('u13',120)
print(bp1)

# get encoding:
et = chardet.detect(bp1)['encoding']
print(et)

# decode bit:
sb = bp1.decode(et)
print(sb)

# <-- transmit -->

# encode bit
eb = sb.encode(et)
print(eb)

# unpack and operate off of passed in value.:
upbp1 = unpack('u13',eb)
print(upbp1)