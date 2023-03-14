import gremlinpy.meta.actr as actr

if __name__=="__main__":
    
    rgqc = actr.gqReqManuscript(
        host="192.168.56.1",
        port=41002,
        manuid="^",
        now=actr.getnow(),
        manu="^",
        pa="^"
    )
    rgqc.execute()