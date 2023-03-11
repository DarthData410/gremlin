# ---> Test

import sys
import os
from gremlinpy.meta.actr import *


if __name__=="__main__":

    
    _h = str(sys.argv[1])
    _p = int(sys.argv[2])
    os.system("clear")
    
    rsrv = ReportSrvr(_h,_p)
    try:
        
        while True:
            rsrv.execute()
    except KeyboardInterrupt:
        print("...stopping ReportSrvr...")
    finally:
        rsrv.close_out()
        print(rsrv.msgback())
    
