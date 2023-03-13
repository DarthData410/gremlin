# +-------------------------------------------------------------------------------------+
# | gremlin - PyFryLabs -> @pyfryday | darth.data410@gmail.com                          |
# | -------                                                                             |
# | pseudoactr.py is a python module for the gremlin app that enables tcp server        |
# | operations for processing both manuscripts by child actors as well as processing    |
# | updates from child actors back to registered parent actor.                          |
# | (part of /meta)                                                                     |
# +-------------------------------------------------------------------------------------+
# | Apache License v2.0
# |$>

import subprocess as sp
from colorama import Fore
import socket
import selectors
import traceback
from .actrlib import *

# register messages::
class register: 
    _sel = None
    _host = ''
    _port = 0
    _action = ''
    _value = ''
    _pa = ''
    _now = ''
    _retmsg = None
    
    def __init__(self,host,port,pa,now) -> None:
        self._sel = selectors.DefaultSelector()
        self._host = host
        self._port = port
        self._pa = pa
        self._now = now

    def returnmsg(self):
         return self._retmsg

    def execute(self):
        request = self.register_request(self._pa,self._host,self._port,self._now)
        self.start_connection(self._host, self._port, request)

        try:
            while True:
                events = self._sel.select(timeout=1)
                for key, mask in events:
                    message = key.data
                    try:
                        message.process_events(mask)
                        self._retmsg = message

                    except Exception:
                        print(
                            f"Main: Error: Exception for {message.addr}:\n"
                            f"{traceback.format_exc()}"
                        )
                        message.close()
                # Check for a socket being monitored to continue.
                if not self._sel.get_map():
                    break
        except KeyboardInterrupt:
            print("Caught keyboard interrupt, exiting")
        finally:
            self._sel.close()

    def register_request(self,pa,host,port,now):
            
            ri = reginfo (
                PseudoActor=pa,
                RegisterNow=now,
                Host=host,
                Port=port
            )
            reg = dict()
            reg["register"]=ri.todict()

            return dict(
                type="text/json",
                encoding="utf-8",
                content=reg,
            )
        
    def __get_message__(self,sock,addr,request):
        """ message = actrlib.<Message Type>(CliMessage): subclass """
        message = CliRegACKMsg(self._sel, sock, addr, request)
        return message

    def start_connection(self,host, port, request):
        addr = (host, port)
        #print(f"Starting connection to {addr}")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setblocking(False)
        sock.connect_ex(addr)
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        message = self.__get_message__(sock,addr,request)
        self._sel.register(sock, events, data=message)

# requests:
class ReqManuscript(register):

    def __init__(self, host, port, pa, now) -> None:
        super().__init__(host, port, pa, now)
    def __get_message__(self, sock, addr, request):
        message = CliReqManuscript(self._sel, sock, addr, request)
        return message
    def register_request(self,pa,host,port,now):
            
            mu = RequestManuscript(
                PseudoActor=pa,
                ReportHost=host,
                ReportPort=port,
                RequestNow=now
            )

            reg = dict()
            reg["manuscript_request"]=mu.todict()

            return dict(
                type="text/json",
                encoding="utf-8",
                content=reg,
            )

class ReqHeartBeat(register):
    """ heartbeat REQ<->ACK between Pseudo-Actor<->Actor/ReportSrv """
    def __init__(self, host, port, pa, now) -> None:
        super().__init__(host, port, pa, now)
    def __get_message__(self, sock, addr, request):
        message = CliReqHeartBeat(self._sel, sock, addr, request)
        return message
    def register_request(self,pa,host,port,now):
            
            req = REQ.create(
                Pseudo=pa,
                To=host,
                ToPort=port,
                Msg="heartbeat",
                Type=1
            )


            reg = dict()
            reg["heartbeat_request"]=req.todict()

            return dict(
                type="text/json",
                encoding="utf-8",
                content=reg,
            )
    
class ReqActUpdate(register):
    """ update for when Act is completed. """
    
    _actup = None
    _status = None
    _upresult = None
    _manuscriptID = None

    def __init__(self, host, port, pa, now, aup, st, res, manuid) -> None:
        super().__init__(host, port, pa, now)
        self._actup = aup
        self._status = st
        self._upresult = res
        self._manuscriptID = manuid
    def __get_message__(self, sock, addr, request):
        message = CliReqActUpdate(self._sel, sock, addr, request)
        return message
    def register_request(self,pa,host,port,now):
            
            # build act update from aup, st, res passed on instance init:
            au = actUpdate(
                UpAct=self._actup,
                UpNow=now,
                Status=self._status,
                UpMsg=self._upresult,
                ManuscriptID=self._manuscriptID
            )
            
            req = REQ.create(
                Pseudo=pa,
                To=host,
                ToPort=port,
                Msg=au.todict(),
                Type=1
            )

            reg = dict()
            reg["actupdate_request"]=req.todict()

            return dict(
                type="text/json",
                encoding="utf-8",
                content=reg,
            )

class ReqManuComplete(register):
    """ update for when manuscript is completed. """
    
    _manuid = None
    _status = None

    def __init__(self, host, port, pa, now, manuid, st) -> None:
        super().__init__(host, port, pa, now)
        self._manuid = manuid
        self._status = st
        
    def __get_message__(self, sock, addr, request):
        message = CliReqManuComplete(self._sel, sock, addr, request)
        return message
    
    def register_request(self,pa,host,port,now):
            
            # build manuscript complete dc:
            mc = ManuscriptCompleted(
                 ManuscriptID=self._manuid,
                 Status=self._status,
                 Now=getnow()
            )
            
            req = REQ.create(
                Pseudo=pa,
                To=host,
                ToPort=port,
                Msg=mc.todict(),
                Type=9
            )

            reg = dict()
            reg["manuscriptcomplete_request"]=req.todict()

            return dict(
                type="text/json",
                encoding="utf-8",
                content=reg,
            )

# pseudo-actor:
class paexec:

    _c = ['']
    _ret = None
    _iserr = False

    def __init__(self,c=['None']):
        """ supply an array set like: c=['ls','-l']. If c=['None'] returns None """
        self._c = c
        self.__exec__()

    def __exec__(self):
        _ret = None
        
        try:
            _ret = sp.run(self._c, capture_output=True, text=True).stdout
        except sp.CalledProcessError as e:
            _ret = e.stderr
            self._iserr = True
        except FileNotFoundError as fe:
            _ret = fe.strerror
            self._iserr = True
        self._ret = _ret
    
    def iserr(self) -> bool:
        return self._iserr

    def ret(self):
        return self._ret

class PseudoActor:
    """ main class used to enable communcation between Pseudo-Actor <-> Actor. (Register,Manuscript,HeartBeat,ActUpdate) """
     
    _host = None
    _port = 0
    _isregistered = False
    _registeredat = '' # getnow() registered value
    _registeredpa = '' # genuid() Pseudo-Actor id value
    _CliRegACKMsg = None
    _CliRegACK = None
    _reportsrv = ''
    _reportsrvport = 0
    _CliReqManuscript = None
    _manuscript = None
    _CliReqHeartBeat = None
    _heartbeat = None
    _CliReqActUpdate = None
    _actupdateACK = None
    _CliReqManuComplete = None
    _manucompleteACK = None
    _executeCERMSG = ''
     
    def __init__(self,acthost:str,actport:int) -> None:
        self._host = acthost
        self._port = actport

    def host(self) -> str:
        return self._host
    def port(self) -> int:
        return self._port
    def paid(self) -> str:
         return self._registeredpa
    def parat(self) -> str:
         return self._registeredat
    def isregistered(self) -> bool:
         return self._isregistered
    def paCliRegACKMsg(self) -> CliRegACKMsg:
         return self._CliRegACKMsg
    def paCliRegACK(self) -> regACK:
         return self._CliRegACK
    def report_server(self) -> str:
         return str(self._reportsrv)
    def report_server_port(self) -> int:
         return int(self._reportsrvport)
    
    # manuscript section: -------------------------
    def manuscript(self) -> manuscript:
         return self._manuscript
    def manuscriptID(self) -> str:
         return self.manuscript().ManuscriptID
    def manuscriptActorNow(self) -> str:
        return self.manuscript().ActorNow
    def manuscriptType(self) -> int:
         return self.manuscript().Type
    def manuscriptPseudoActor(self) -> str:
         return self.manuscript().PseudoActor
    # Acts:
    def manuscriptNumOfActs(self) -> int:
         return self.manuscript().NumOfActs
    def manuact_seq(self,idx) -> str:
         return self.manuscript().Acts[idx].Seq
    def manuact_command(self,idx) -> str:
         return self.manuscript().Acts[idx].Command
    def manuact_args(self,idx) -> str:
         return self.manuscript().Acts[idx].Args
    def manuact_output(self,idx) -> int:
         return self.manuscript().Acts[idx].Output
    def manuact_chrono(self,idx) -> int:
         return self.manuscript().Acts[idx].Chrono
    # end manuscript section -----------------------
    
    # ACK section: ---------------------------------
    def heartbeat(self) -> ACK:
         return self._heartbeat
    def actupdateACK(self) -> ACK:
         return self._actupdateACK
    def manucompleteACK(self) -> ACK:
         return self._manucompleteACK
    # end ACK section: -----------------------------

    def registerpa(self):
        if not self._isregistered:
            self._registeredpa = genuid()
            self._registeredat = getnow()
            r = register(
                 host=self._host,
                 port=self._port,
                 pa=self._registeredpa,
                 now=self._registeredat
            )
            r.execute()
            self._CliRegACKMsg = r.returnmsg()
            self._CliRegACK = self._CliRegACKMsg.result
            self._reportsrv = self.paCliRegACK().ManuHost
            self._reportsrvport = self.paCliRegACK().ManuPort
            self._isregistered = self.paCliRegACK().Registered
    
    def request_manuscript(self):
        r = ReqManuscript(
            host=self.report_server(),
            port=self.report_server_port(),
            pa=self.paid(),
            now=self.parat()
        )
        r.execute()
        self._CliReqManuscript = r.returnmsg()
        self._manuscript = self._CliReqManuscript.result
    
    def send_heartbeat(self):
        r = ReqHeartBeat(
            host=self.report_server(),
            port=self.report_server_port(),
            pa=self.paid(),
            now=self.parat()
        )
        r.execute()
        self._CliReqHeartBeat = r.returnmsg()
        self._heartbeat = self._CliReqHeartBeat.result
    
    def update_act(self,actu):
        r = ReqActUpdate(
              host=self.report_server(),
              port=self.report_server_port(),
              pa=self.paid(),
              now=getnow(),
              aup=actu,
              st=1,
              res="...finished...",
              manuid=self.manuscript().ManuscriptID
        )
        
        r.execute()
        self._CliReqActUpdate = r.returnmsg()
        self._actupdateACK = self._CliReqActUpdate.result
    
    def notify_manuscript_complete(self,status):
         r = ReqManuComplete(
              host=self.report_server(),
              port=self.report_server_port(),
              pa=self.paid(),
              now=getnow(),
              manuid=self.manuscript().ManuscriptID,
              st=status
         )
         r.execute()
         self._CliReqManuComplete = r.returnmsg()
         self._manucompleteACK = self._CliReqManuComplete.result
    
    def geta(self,idx) -> act:
        return self.manuscript().Acts[idx]
    
    def executeactmsg(self) -> str:
        return self._executeCERMSG

    def executeact(self,idx) -> int:
        ret = 0
        ea = self.geta(idx)
        exec = paexec([ea.Command,ea.Args])
        self._executeCERMSG = exec.ret()
        if not exec.iserr():
             ret = 1
        return ret
    

     
