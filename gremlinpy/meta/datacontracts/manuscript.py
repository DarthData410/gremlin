# +-------------------------------------------------------------------------------------+
# | gremlin - PyFryLabs -> @pyfryday | darth.data410@gmail.com                          |
# | -------                                                                             |
# | manuscript.py is a python module for the gremlin app that wraps the actor<->pseudo  |
# | actor communincation, specifically for the manuscript JSON/dataclass.               |
# | (part of /meta)                                                                     |
# +-------------------------------------------------------------------------------------+
# | Apache License v2.0
# |$>

import json
import dataclasses as dc

MANUID="ManuscriptID"
PSDACT="PseudoActor"
REPHOST="ReportingHost"
REPPORT="ReportingPort"
REQNOW="RequestNow"
ACTNOW="ActorNow"
TYPE="Type"
NUMOFACTS="NumOfActs"
ACTS="Acts"
SEQ="Seq"
COMM="Command"
ARGS="Args"
OUT="Output"
CHRONO="Chrono"

@dc.dataclass
class manuscript:
    ManuscriptID: str
    PseudoActor: str
    ReportingPort: str
    ActorNow: str
    Type: int
    NumOfActs: int
    Acts: list

    def fromjson(jsonobj):
        ljo = json.loads(jsonobj)
        ljoa = ljo[ACTS]
        ljoal = list()

        for ak in ljoa:
            a = act.newfromdict(ljoa[ak])
            ljoal.append(a)
        
        ret = manuscript(
            ManuscriptID=ljo[MANUID],
            PseudoActor=ljo[PSDACT],
            ReportingPort=ljo[REPPORT],
            ActorNow=ljo[ACTNOW],
            Type=ljo[TYPE],
            NumOfActs=ljo[NUMOFACTS],
            Acts=ljoal
        )
        
        return ret
    
    def tojson(self):
        d = dict()
        d[MANUID] = self.ManuscriptID
        d[PSDACT] = self.PseudoActor
        d[REPPORT] = self.ReportingPort
        d[ACTNOW] = self.ActorNow
        d[TYPE] = self.Type
        d[NUMOFACTS] = self.NumOfActs
        actsd = dict()

        for a in self.Acts:
            ad = a.todict()
            actsd[ad[SEQ]]=ad
        
        d[ACTS]=actsd

        ret = json.dumps(d)
        return ret
    
    def fromdict(d):
        actsl = list()
        adict = d[ACTS]
        for dk in adict:
            actsl.append(act.newfromdict(adict[str(dk)]))

        ret = manuscript(
            ManuscriptID=d[MANUID],
            PseudoActor=d[PSDACT],
            ReportingPort=d[REPPORT],
            ActorNow=d[ACTNOW],
            Type=d[TYPE],
            NumOfActs=d[NUMOFACTS],
            Acts=actsl
        )
        return ret
    
    def todict(self):
        ret = dict()
        actsd = dict()
        for ea in self.Acts:
            actsd[ea.Seq]=ea.todict()

        ret[MANUID]=self.ManuscriptID
        ret[PSDACT]=self.PseudoActor
        ret[REPPORT]=self.ReportingPort
        ret[ACTNOW]=self.ActorNow
        ret[TYPE]=self.Type
        ret[NUMOFACTS]=self.NumOfActs
        ret[ACTS]=actsd
        return ret


@dc.dataclass
class act:
    Seq: str
    Command: str
    Args: str
    Output: int
    Chrono: int

    def newfromdict(d):
        
        ret = act(
            Seq = d[SEQ],
            Command=d[COMM],
            Args=d[ARGS],
            Output=d[OUT],
            Chrono=d[CHRONO]
        )
        return ret

    def todict(self):
        d = dict()
        d[SEQ] = self.Seq
        d[COMM] = self.Command
        d[ARGS] = self.Args
        d[OUT] = self.Output
        d[CHRONO] = self.Chrono
        ret = d
        return ret
    def fromdict(d):
        ret = act(
            Seq=d[SEQ],
            Command=d[COMM],
            Args=d[ARGS],
            Output=d[OUT],
            Chrono=d[CHRONO]
        )
        return ret

@dc.dataclass
class actUpdate:
    ManuscriptID: str
    UpAct: act
    UpNow: str
    Status: int
    UpMsg: str

    def fromdict(d):
        ret = actUpdate(
            ManuscriptID=d[MANUID],
            UpAct=d["UpAct"],
            UpNow=d["UpNow"],
            Status=d["Status"],
            UpMsg=d["UpMsg"]
        )
        return ret
    def todict(a):
        ret = dict()
        ret[MANUID]=a.ManuscriptID
        ret["UpAct"]=a.UpAct.todict()
        ret["UpNow"]=a.UpNow
        ret["Status"]=a.Status
        ret["UpMsg"]=a.UpMsg
        return ret

@dc.dataclass
class RequestManuscript:
    PseudoActor: str
    ReportHost: str
    ReportPort: int
    RequestNow: str

    def newfromdict(d):
        ret = RequestManuscript(
            PseudoActor=d[PSDACT],
            ReportHost=d[REPHOST],
            ReportPort=d[REPPORT],
            RequestNow=d[REQNOW]
        )
        return ret
    
    def todict(self):
        ret = dict()
        ret[PSDACT] = self.PseudoActor
        ret[REPHOST] = self.ReportHost
        ret[REPPORT] = self.ReportPort
        ret[REQNOW] = self.RequestNow
        return ret

    def fromdict(d):
        ret = RequestManuscript(
            PseudoActor=d[PSDACT],
            ReportHost=d[REPHOST],
            ReportPort=d[REPPORT],
            RequestNow=d[REQNOW]
        )
        return ret

@dc.dataclass
class SubmitManuscript:
    ManuscriptID: str
    Now: str
    NewManuscript: dict

    def todict(self):
        ret = dict()
        ret["ManuscriptID"] = self.ManuscriptID
        ret["Now"] = self.Now
        ret["NewManuscript"] = self.NewManuscript
        return ret
    def fromdict(d):
        ret = SubmitManuscript(
            ManuscriptID=d["ManuscriptID"],
            Now=d["Now"],
            NewManuscript=d["NewManuscript"]
        )
        return ret

@dc.dataclass
class ManuscriptCompleted:
    ManuscriptID: str
    Status: int
    Now: str

    def todict(self):
        ret = dict()
        ret[MANUID] = self.ManuscriptID
        ret["Status"] = self.Status
        ret["Now"] = self.Now
        return ret
    
    def fromdict(d):
        ret = ManuscriptCompleted(
            ManuscriptID=d[MANUID],
            Status=d["Status"],
            Now=d["Now"]
        )
        return ret
