# +-------------------------------------------------------------------------------------+
# | gremlin - PyFryLabs -> @pyfryday | darth.data410@gmail.com                          |
# | -------                                                                             |
# | datasys.py is a python module for the gremlin app that wraps actor<->pseudo         |
# | actor communincation, specifically sys REQ/ACK/DWN.                                 |
# | (part of /meta)                                                                     |
# +-------------------------------------------------------------------------------------+
# | Apache License v2.0
# |$>

import json
import dataclasses as dc
import uuid
import datetime

# utils:
def genuid() -> str:
    """ return uuid value for use within /meta """
    u = uuid.uuid1()
    return str(u)

def getnow() -> str:
    now = datetime.datetime.now()
    ret = now.strftime("%Y-%m-%d~%H::%M::%S")
    return ret

# system wide datacontracts:
@dc.dataclass
class REQ:
    ReqID: str
    HostFrom: str
    HostPort: int
    ToHost: str
    ToPort: int
    ReqMsg: str
    Type: int
    ReqNow: str

    def create(From,FrmPort,To,ToPort,Msg,Type):
        ret = REQ(
            ReqID = genuid(),
            HostFrom=From,
            HostPort=FrmPort,
            ToHost=To,
            ToPort=ToPort,
            ReqMsg=Msg,
            Type=Type,
            ReqNow = getnow()
        )
        return ret
    def todict(self):
        ret = dict()
        ret["ReqID"]=self.ReqID
        ret["HostFrom"]=self.HostFrom
        ret["HostPort"]=self.HostPort
        ret["ToHost"]=self.ToHost
        ret["ToPort"]=self.ToPort
        ret["ReqMsg"]=self.ReqMsg
        ret["Type"]=self.Type
        ret["ReqNow"]=self.ReqNow
        return ret
    def fromdict(d):
        ret = REQ(
            ReqID=d["ReqID"],
            HostFrom=d["HostFrom"],
            HostPort=d["HostPort"],
            ToHost=d["ToHost"],
            ToPort=d["ToPort"],
            ReqMsg=d["ReqMsg"],
            Type=d["Type"],
            ReqNow=d["ReqNow"]
        )
        return ret

@dc.dataclass
class ACK:
    HostFrom: str
    HostPort: int
    AckMsg: str
    AckNow: str
    ReqID: str

    def fromreq(req):
        ret = ACK(
            HostFrom=req.ToHost,
            HostPort=req.ToPort,
            AckMsg="ACK",
            AckNow=getnow(),
            ReqID=req.ReqID
        )
        return ret
    def fromdict(d):
        ret = ACK(
            HostFrom=d["HostFrom"],
            HostPort=d["HostPort"],
            AckMsg=d["AckMsg"],
            AckNow=d["AckNow"],
            ReqID=d["ReqID"]
        )
        return ret
    def todict(self):
        ret = dict()
        ret["HostFrom"]=self.HostFrom
        ret["HostPort"]=self.HostPort
        ret["AckMsg"]=self.AckMsg
        ret["AckNow"]=self.AckNow
        ret["ReqID"]=self.ReqID
        return ret

@dc.dataclass
class DWN:
    DWNID: str
    DWNNOW: str
    Actor: str
    PseudoActor: str
    Chrono: int
    ShutDown: bool = False

    def create(Actor,PseudoActor,Chrono,ShutDown):
        ret = DWN(
            DWNID=genuid(),
            DWNNOW=getnow(),
            Actor=Actor,
            PseudoActor=PseudoActor,
            Chrono=Chrono,
            ShutDown=ShutDown
        )
        return ret


if __name__=="__main__":
    
    r = REQ.create("1001",10,"2001",20,"ALS",1)
    print(r)
    a = ACK.fromreq(r)
    print(a)
    d = DWN.create(a.HostFrom,r.HostFrom,120,True)
    print(d)

    """
    REQ(ReqID='fb26d2bf-bdf9-11ed-a9c4-b94e40e120b5', HostFrom='1001', HostPort=10, ToHost='2001', ToPort=20, ReqMsg='ALS', Type=1, ReqNow='2023-03-08~15::41::27')
    ACK(HostFrom='2001', HostPort=20, AckMsg='ACK', AckNow='2023-03-08~15::41::27', ReqID='fb26d2bf-bdf9-11ed-a9c4-b94e40e120b5')
    DWN(DWNID='fb26d2c0-bdf9-11ed-a9c4-b94e40e120b5', DWNNOW='2023-03-08~15::41::27', Actor='2001', PseudoActor='1001', Chrono=120, ShutDown=True)
    """