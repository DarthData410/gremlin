# +-------------------------------------------------------------------------------------+
# | gremlin - PyFryLabs -> @pyfryday | darth.data410@gmail.com                          |
# | -------                                                                             |
# | regsrv.py is a python module for the gremlin app /meta mod enabling the registry    |
# | server needs of /meta from Pseudo-Actors -> Actors.                                 |
# | (part of /meta)                                                                     |
# +-------------------------------------------------------------------------------------+
# | Apache License v2.0
# |$>

import sys
import os
import actr as actr


if __name__=="__main__":

    
    _h = str(sys.argv[1])
    _p = int(sys.argv[2])
    os.system("clear")
    
    rsrv = actr.Registry(_h,_p)
    try:
        
        while True:
            rsrv.execute()
    except KeyboardInterrupt:
        print("...stopping registry...")
    finally:
        rsrv.close_out()
        print(rsrv.msgback())
    
