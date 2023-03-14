import gremlinpy.meta.actr as actr

if __name__=="__main__":
    
    a = actr.act(
        Seq="01",
        Command="ls",
        Args="-l",
        Output=1,
        Chrono=30
    )

    al = list()
    al.append(a)
    
    sm = actr.manuscript(
        ManuscriptID=actr.genuid(),
        PseudoActor=actr.genuid(),
        ReportingPort="41001",
        ActorNow=actr.getnow(),
        Type=1,
        NumOfActs=1,
        Acts=al
    )

    gqc = actr.gqcli(
        host="192.168.56.1",
        port=41002,
        manuid=sm.ManuscriptID,
        now=actr.getnow(),
        manu=sm
    )
    gqc.execute()