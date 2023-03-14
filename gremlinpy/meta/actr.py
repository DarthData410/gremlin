# +-------------------------------------------------------------------------------------+
# | gremlin - PyFryLabs -> @pyfryday | darth.data410@gmail.com                          |
# | -------                                                                             |
# | actr.py is a python module for the gremlin app that directs PseudoActors/Actors and |
# | registry server. A single registry and actor is designed to work with multiple      |
# | Pseudo-Actors.                                                                      |
# | (part of /meta)                                                                     |
# +-------------------------------------------------------------------------------------+
# | Apache License v2.0
# |$>

import sys 
from colorama import Fore
import traceback
import selectors
import socket
from .actrlib import *

# registry server:
class Registry:
    _sel = None
    _host = ''
    _port = 0
    _sock = None
    _iserror = False
    _msgback = ''
    _ran_post = False

    def __init__(self,host,port) -> None:
        self._host = host
        self._port = port
        self.__init_listen__()
        self.__init_selector__()
    
    def __message_out__(self):
        print("\n ["+Fore.YELLOW+"+"+Fore.RESET+"] --->"+Fore.GREEN+" gremlin"+Fore.RESET+" /meta - "+Fore.LIGHTGREEN_EX+"Registry"+Fore.RESET+" ready: "+Fore.CYAN+"{"+Fore.MAGENTA+str(self._host)+Fore.RESET+"@"+Fore.MAGENTA+str(self._port)+Fore.CYAN+"}"+Fore.RESET+"")

    def __init_listen__(self):
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._sock.bind((self._host, self._port))
        self._sock.listen()
        self._sock.setblocking(False)
        self.__message_out__()
    
    def __init_selector__(self):
        self._sel = selectors.DefaultSelector()
        self._sel.register(self._sock, selectors.EVENT_READ, data=None)

    def iserror(self) -> bool:
        return self._iserror
    def msgback(self) -> str:
        return self._msgback
    
    def __print_except__(self,addr):
        eadr = addr
        print(""+Fore.GREEN+"gremlin"+Fore.WHITE+" /meta "+Fore.RED+"Registry fault"+Fore.WHITE+":"+str(eadr[0])+":"+str(eadr[1]))
        print(self._msgback)

    def execute(self):
        """ main execution point fired from gremlin /meta -Registry ! """

        events = self._sel.select(timeout=None)
        for key, mask in events:
            if key.data is None:
                self.__accept_wrapper__(key.fileobj)
            else:
                message = key.data
                        
                try:
                    message.process_events(mask)
                    self.__post_process__(message)
                except Exception:
                    self._msgback = f"PAF: {message.addr} = " + traceback.format_exc()
                    self.__print_except__(message.addr)
                    self._iserror = True
                    message.close()

    def __post_process__(self,msg):
        self._ran_post = True

    def __print_closeout_msg__(self):
        self._msgback = self._msgback + "\n [+] --->"  
        self._msgback = self._msgback + Fore.GREEN + " gremlin " + Fore.WHITE
        self._msgback = self._msgback + "/meta "+Fore.LIGHTGREEN_EX+"Registry"+Fore.WHITE+" closed"

    def close_out(self):
        self._sel.close()
        self.__print_closeout_msg__()
    
    def __message__(self,conn, addr):
        msg = RegisterMsg(self._sel, conn, addr)
        return msg

    def __accept_wrapper__(self,sock):
        conn, addr = sock.accept()  
        print(f"Accepted connection from {addr}")
        conn.setblocking(False)
        msg = self.__message__(conn,addr)
        self._sel.register(conn, selectors.EVENT_READ, data=msg)

# report server:
class ReportSrvr(Registry):

    def __init__(self, host, port) -> None:
        super().__init__(host, port)
    def __message_out__(self):
        print("\n ["+Fore.YELLOW+"+"+Fore.RESET+"] --->"+Fore.GREEN+" gremlin"+Fore.RESET+" /meta - "+Fore.LIGHTYELLOW_EX+"Report Server"+Fore.RESET+" ready: "+Fore.CYAN+"{"+Fore.MAGENTA+str(self._host)+Fore.RESET+"@"+Fore.MAGENTA+str(self._port)+Fore.CYAN+"}"+Fore.RESET+"")
    def __print_except__(self,addr):
        print(
            f""+Fore.GREEN+"gremlin"+Fore.WHITE+" /meta "+Fore.RED+"Report Server fault"+Fore.WHITE+": "+addr+":\n"
            f"{self._msgback}"
        )
    def __print_closeout_msg__(self):
        self._msgback = self._msgback + "\n [+] --->"  
        self._msgback = self._msgback + Fore.GREEN + " gremlin " + Fore.WHITE
        self._msgback = self._msgback + "/meta "+Fore.LIGHTYELLOW_EX+"Report Servr"+Fore.WHITE+" closed"
    def __message__(self,conn, addr):
        msg = ReportSrvMsg(self._sel, conn, addr)
        return msg
#
# GQueue Section ****************************
#

class gqcli: 
    _sel = None
    _host = ''
    _port = 0
    _action = ''
    _value = ''
    _manuid = ''
    _now = ''
    _retmsg = None
    _manuscript = ''
    
    def __init__(self,host,port,manuid,now,manu) -> None:
        self._sel = selectors.DefaultSelector()
        self._host = host
        self._port = port
        self._manuid = manuid
        self._now = now
        self._manuscript = manu

    def returnmsg(self):
         return self._retmsg

    def manuscriptID(self):
        return self._manuid
    def curr_manuscript(self) -> manuscript:
        return self._manuscript

    def execute(self):
        request = self.gq_request()
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

    def gq_request(self):
            
            nm = SubmitManuscript(
                ManuscriptID=self._manuid,
                Now=self._now,
                NewManuscript=self._manuscript.todict()
            )
            #print(nm)
            sub = dict()
            sub["submit_manuscript"]=nm.todict()

            return dict(
                type="text/json",
                encoding="utf-8",
                content=sub,
            )
        
    def __get_message__(self,sock,addr,request):
        """ message = GQueue ACK Message Back: subclass """
        message = gqCliSubManuACKMsg(self._sel, sock, addr, request)
        return message

    def start_connection(self,host, port, request):
        addr = (host, port)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setblocking(False)
        sock.connect_ex(addr)
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        message = self.__get_message__(sock,addr,request)
        self._sel.register(sock, events, data=message)

# requests:
class gqReqManuscript(gqcli):
    _active_pa = ''
    def __init__(self, host,port,manuid,now,manu,pa) -> None:
        self._active_pa = pa
        super().__init__(host,port,manuid,now,manu)
    def __get_message__(self, sock, addr, request):
        message = gqCliReqManuACKMsg(self._sel, sock, addr, request)
        return message
    def gq_request(self):
            
            mu = RequestManuscript(
                PseudoActor=self._active_pa,
                ReportHost=self._host,
                ReportPort=self._port,
                RequestNow=self._now
            )

            reg = dict()
            reg["manuscript_request"]=mu.todict()

            return dict(
                type="text/json",
                encoding="utf-8",
                content=reg,
            )

class GQueue(Registry):
    
    def __init__(self, host, port) -> None:
        self._gqueue = list()
        super().__init__(host, port)
    def __message_out__(self):
        print("\n ["+Fore.YELLOW+"+"+Fore.RESET+"] --->"+Fore.GREEN+" gremlin"+Fore.RESET+" /meta - "+Fore.LIGHTRED_EX+"GQueue"+Fore.RESET+" ready: "+Fore.CYAN+"{"+Fore.MAGENTA+str(self._host)+Fore.RESET+"@"+Fore.MAGENTA+str(self._port)+Fore.CYAN+"}"+Fore.RESET+"")
    def __print_except__(self,addr):
        print(""+Fore.GREEN+"gremlin"+Fore.WHITE+" /meta "+Fore.RED+"GQueue fault"+Fore.WHITE+": "+addr+"")
        print(self._msgback)
    
    def __has_manus__(self) -> bool:
        ret = False
        if self._gqueue.__len__() > 0:
            ret = True
        return ret
    
    def __get_manu__(self) -> manuscript:
        ret = self._gqueue[0]
        self._gqueue.pop(0)
        return ret
    
    def __check_gq__(self,id) -> bool:
        ret = False
        for q in self._gqueue:
            if q.ManuscriptID==id:
                ret = True
                break
        return ret
    
    def __blank_manu__(self) -> manuscript:
        return manuscript(
            ManuscriptID="0",
            PseudoActor="0",
            ReportingPort="0",
            ActorNow="0",
            Type=0,
            NumOfActs=0,
            Acts=list()
        )
    
    def __post_process__(self, msg):
        if type(msg._gqmanu)==type(self.__blank_manu__()):
            if msg._gqmanu.ManuscriptID.__len__()>10:
                if not self.__check_gq__(msg._gqmanu.ManuscriptID):
                    self.__queue_manu__(msg._gqmanu)
                    self._ran_post = True

    def __print_closeout_msg__(self):
        self._msgback = self._msgback + "\n [+] --->"  
        self._msgback = self._msgback + Fore.GREEN + " gremlin " + Fore.WHITE
        self._msgback = self._msgback + "/meta "+Fore.LIGHTRED_EX+"GQueue"+Fore.WHITE+" closed"
    def __queue_manu__(self,manu):
        self._gqueue.append(manu)
        print(Fore.GREEN+"gremlin"+Fore.WHITE+" /meta "+Fore.LIGHTRED_EX+"GQueue"+Fore.RESET+" +manuscript:"+Fore.LIGHTCYAN_EX+manu.ManuscriptID+Fore.RESET+"::Total-Of:"+Fore.LIGHTYELLOW_EX+str(self._gqueue.__len__())+Fore.RESET)
    def __message__(self,conn, addr):
        msg = gqMsg(self._sel, conn, addr,self)
        return msg
