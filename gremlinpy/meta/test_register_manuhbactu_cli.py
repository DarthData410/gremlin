
import pseudoactr as pse

if __name__=="__main__":
    
    psa = pse.PseudoActor("192.168.56.1",41011)
    # regiter Pseudo-Actor:
    psa.registerpa()
    print("Pseudo-Actor: "+psa.paCliRegACK().PseudoActor)
    print("Registered: "+str(psa.paCliRegACK().Registered))

    # request manuscript to act upon:
    psa.request_manuscript()
    print("Manuscript ID: "+psa.manuscript().ManuscriptID)
    print("Manuscript Acts: ")
    print(psa.manuscript().Acts)

    # update act to report server:
    a = psa.manuscript().Acts[0]
    psa.update_act(a)

    # send heartbeat to update report server still alive:
    psa.send_heartbeat()
    
    # print Acks:
    print(pse.Fore.CYAN+"HEARTBEAT ACK"+pse.Fore.RESET)
    print("ACK Msg: "+psa.heartbeat().AckMsg)
    print("REQ ID: "+psa.heartbeat().ReqID)
    print("ACK Now: "+psa.heartbeat().AckNow)

    print(pse.Fore.CYAN+"ACT UPDATE ACK"+pse.Fore.RESET)
    print("ACK Msg: "+psa.actupdateACK().AckMsg)
    print("REQ ID: "+psa.actupdateACK().ReqID)
    print("ACK Now: "+psa.actupdateACK().AckNow)

    # notify manuscript completed:
    psa.notify_manuscript_complete("SHUTDOWN")
    print(pse.Fore.CYAN+"MANUSCRIPT COMPLETE ACK"+pse.Fore.RESET)
    print("ACK Msg: "+psa.manucompleteACK().AckMsg)
    print("REQ ID: "+psa.manucompleteACK().ReqID)
    print("ACK Now: "+psa.manucompleteACK().AckNow)
    
    