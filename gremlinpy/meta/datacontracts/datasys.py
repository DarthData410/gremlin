# +-------------------------------------------------------------------------------------+
# | gremlin - PyFryLabs -> @pyfryday | darth.data410@gmail.com                          |
# | -------                                                                             |
# | datasys.py is a python module for the gremlin app that wraps actor<->pseudo         |
# | actor communincation, specifically sys REQ/ACK/DWN.                                 |
# | (part of /meta)                                                                     |
# +-------------------------------------------------------------------------------------+
# | Apache License v2.0
# |$>

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
    PseudoActor: str
    ToHost: str
    ToPort: int
    ReqMsg: str
    Type: int
    ReqNow: str

    def create(Pseudo,To,ToPort,Msg,Type):
        ret = REQ(
            ReqID = genuid(),
            PseudoActor=Pseudo,
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
        ret["PseudoActor"]=self.PseudoActor
        ret["ToHost"]=self.ToHost
        ret["ToPort"]=self.ToPort
        ret["ReqMsg"]=self.ReqMsg
        ret["Type"]=self.Type
        ret["ReqNow"]=self.ReqNow
        return ret
    def fromdict(d):
        ret = REQ(
            ReqID=d["ReqID"],
            PseudoActor=d["PseudoActor"],
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
