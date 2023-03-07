# +-------------------------------------------------------------------------------------+
# | gremlin - PyFryLabs -> @pyfryday | darth.data410@gmail.com                          |
# | -------                                                                             |
# | manuscript.py is a python module for the gremlin app that wraps the actor<->pseudo  |
# | actor communincation, specifically for the manuscript JSON/dataclass.               |
# | (part of /meta)                                                                     |
# +-------------------------------------------------------------------------------------+
# | Apache License v2.0
# |$>

#import bitstruct
import json
import dataclasses as dc
#import io
#import snappy as snp #TODO: get an example of how to compress/decompress JSON file to send

#"document": "/meta json manuscript template",
#    "PseudoActor": "<uuid of registered PseudoActor>",
#    "ReportingPort": "<port in-which PseudoActor reports back info from manuscript acts>",
#    "ActorNow": "<Time manuscript generated from Actor perspective>",
#    "Type": "<1=recon,2=exploit>",
#    "NumOfActs": 2,
#    "Acts": {
#        "Seq01": {
#            "Command": "<command to execute>",
#            "Args": "<command args>",
#            "Output": "<output type: 1=JSON Cap Cmd Output, 2=Large Expected JSON broken seq msgs, compressed, 3=log local and 1 for success, 2 for fail>",
#            "Chrono": "<time in seconds before executing after last Act. If first will wait supplied seconds beforing starting>"
#        },
#        "Seq02": {
#            "Command": "<command to execute>",
#            "Args": "<command args>",
#            "Output": "<output type: 1=JSON Cap Cmd Output, 2=Large Expected JSON broken seq msgs, compressed, 3=log local and 1 for success, 2 for fail>",
#            "Chrono": "<time in seconds before executing after last Act. If first will wait supplied seconds beforing starting>"
#        }
#    }

PSDACT="PseudoActor"
REPPORT="ReportingPort"
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

if __name__ == "__main__":
    
    a1 = act(
        Seq="Seq1",
        Command="Test1",
        Args="Arg1,Arg2",
        Output=1,
        Chrono=30
    )
    
    a2 = act(
        Seq="Seq2",
        Command="Test2",
        Args="Arg1",
        Output=1,
        Chrono=120
    )

    m = manuscript
    m.PseudoActor = "x23-78p-qs47-2z"
    m.ReportingPort = 41013
    m.ActorNow = "2023-03-07~12::13::44"
    m.Type = 1
    m.NumOfActs = 2
    al = list()
    al.append(a1)
    al.append(a2)
    m.Acts = al

    jsonobj = m.tojson(m)
    print(jsonobj)
    mret = manuscript.fromjson(jsonobj)
    print(mret)
    
