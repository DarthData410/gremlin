# +-------------------------------------------------------------------------------------+
# | gremlin - PyFryLabs -> @pyfryday | darth.data410@gmail.com                          |
# | -------                                                                             |
# | register.py is a python module for the gremlin app that wraps the JSON register doc |
# | that a PseudoActor sends to an Actor to register with and await manuscript & acts.  |
# | (part of /meta)                                                                     |
# +-------------------------------------------------------------------------------------+
# | Apache License v2.0
# |$>

import json
import dataclasses as dc

PSDACT="PseudoActor"
REGNOW="RegisterNow"
HOST="Host"
PORT="Port"
MANU="Manu"
REGED="Registered"

@dc.dataclass
class reginfo:
    """ for use with conversion between python objects/JSON. acts as a data contract """
    PseudoActor: str
    RegisterNow: str
    Host: str
    Port: int

    def fromjson(jsonobj):
        ljo = json.loads(jsonobj)
        ret = reginfo(
            PseudoActor=ljo[PSDACT],
            RegisterNow=ljo[REGNOW],
            Host=ljo[HOST],
            Port=ljo[PORT]
        )
        return ret
    
    def new(PseudoActor,RegisterNow,Host,Port):
        ret = reginfo(
            PseudoActor=PseudoActor,
            RegisterNow=RegisterNow,
            Host=Host,
            Port=Port
        )
        return ret

    def tojson(self):
        d = self.todict()
        ret = json.dumps(d)
        return ret
    
    def todict(self):
        d = dict()
        d[PSDACT] = self.PseudoActor
        d[REGNOW] = self.RegisterNow
        d[HOST] = self.Host
        d[PORT] = self.Port
        return d

@dc.dataclass
class regACK:
    """ registry server ACKnowledgement of Pseudo-Actor registry  """
    PseudoActor: str
    ManuHost: str
    ManuPort: int
    Registered: bool = False

    def fromjson(jsonobj):
        ljo = json.loads(jsonobj)
        ret = reginfo(
            PseudoActor=ljo[PSDACT],
            ManuHost=ljo[MANU+HOST],
            ManuPort=ljo[MANU+PORT],
            RegisterNow=ljo[REGED]
        )
        return ret
    
    def new(PseudoActor,ManuHost,ManuPort,Registered):
        ret = reginfo(
            PseudoActor=PseudoActor,
            ManuHost=ManuHost,
            ManuPort=ManuPort,
            Registered=Registered
        )
        return ret

    def tojson(self):
        d = self.todict()
        ret = json.dumps(d)
        return ret
    
    def todict(self):
        d = dict()
        d[PSDACT] = self.PseudoActor
        d[MANU+HOST] = self.ManuHost
        d[MANU+PORT] = self.ManuPort
        d[REGED] = self.Registered
        return d

    def fromdict(d):
        ret = regACK(
            PseudoActor=d[PSDACT],
            ManuHost=d[MANU+HOST],
            ManuPort=d[MANU+PORT],
            Registered=d[REGED]
        )
        return ret


# example usgae:
if __name__=="__main__":
    rdc = reginfo(
        PseudoActor="test1",
        RegisterNow="ux00-yu-12-345-ght7",
        Host="127.0.0.1",
        Port=41013
    )    

    jsonobj = rdc.tojson()
    print(jsonobj)
    nrdc = reginfo.fromjson(jsonobj)
    print(nrdc)