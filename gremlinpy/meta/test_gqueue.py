# ---> Test

import sys
import os
from gremlinpy.meta.actr import *


if __name__=="__main__":

    
    _h = str(sys.argv[1])
    _p = int(sys.argv[2])
    os.system("clear")
    
    gq = GQueue(_h,_p)
    try:
        
        while True:
            gq.execute()
    except KeyboardInterrupt:
        print("...stopping GQueue...")
    finally:
        gq.close_out()
        print(gq.msgback())
    
