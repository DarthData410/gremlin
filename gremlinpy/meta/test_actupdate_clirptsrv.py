
import pseudoactr as pse

if __name__=="__main__":
    #req = pse.ReqHeartBeat("192.168.56.1",41001,"uxzt149er","2023-03-07~05:10:10")
    #req.execute()
    guid = pse.lib.genuid()
    
    a = pse.lib.act(
        Seq="01",
        Command="nwmcli",
        Args="Arg1,Arg2",
        Output=1,
        Chrono=60
    )

    req = pse.ReqActUpdate("192.168.56.1",41001,guid,pse.lib.getnow(),a,1,(guid+" finished..."))
    req.execute()