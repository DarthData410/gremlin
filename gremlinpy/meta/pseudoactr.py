# +-------------------------------------------------------------------------------------+
# | gremlin - PyFryLabs -> @pyfryday | darth.data410@gmail.com                          |
# | -------                                                                             |
# | actrsrvr.py is a python module for the gremlin app that enables tcp server          |
# | operations for processing both manuscripts by child actors as well as processing    |
# | updates from child actors back to registered parent actor.                          |
# | (part of /meta)                                                                     |
# +-------------------------------------------------------------------------------------+
# | Apache License v2.0
# |$>

import sys
import colorama
from colorama import Fore
import socket
import selectors
import traceback
import actrlib as lib

class register: 
    _sel = None
    _host = ''
    _port = 0
    _action = ''
    _value = ''
    _pa = ''
    _now = ''
    
    def __init__(self,host,port,pa,now) -> None:
        self._sel = selectors.DefaultSelector()
        self._host = host
        self._port = port
        self._pa = pa
        self._now = now

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
            
            ri = lib.reginfo (
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
        

    def create_request(self,action, value):
        if action == "search":
            return dict(
                type="text/json",
                encoding="utf-8",
                content=dict(action=action, value=value),
            )
        else:
            return dict(
                type="binary/custom-client-binary-type",
                encoding="binary",
                content=bytes(action + value, encoding="utf-8"),
            )
    def __get_message__(self,sock,addr,request):
        message = lib.CliRegACKMsg(self._sel, sock, addr, request)
        return message

    def start_connection(self,host, port, request):
        addr = (host, port)
        print(f"Starting connection to {addr}")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setblocking(False)
        sock.connect_ex(addr)
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        message = self.__get_message__(self._sel,sock,addr,request)
        self._sel.register(sock, events, data=message)

class ReqManuscript(register):

    def __init__(self, host, port, pa, now) -> None:
        super().__init__(host, port, pa, now)
    def __get_message__(self, sock, addr, request):
        message = lib.CliReqManuscript(self._sel, sock, addr, request)
        return message
    def register_request(self,pa,host,port,now):
            
            mu = lib.RequestManuscript(
                PseudoActor="zz::41::82::34::23::12::zz",
                ReportHost="192.168.56.1",
                ReportPort=41001,
                RequestNow="2023-03-08~14::15::30"
            )
            
            reg = dict()
            reg["manuscript_request"]=mu.todict()

            return dict(
                type="text/json",
                encoding="utf-8",
                content=reg,
            )

class PseudoActor:

    _sel = None
    _host = ''
    _port = 0
    _sock = None
    _iserror = False
    _msgback = ''

    def __init__(self,host,port) -> None:
        self._host = host
        self._port = port
        self.__init_listen__()
        self.__init_selector__()
    
    def __init_listen__(self):
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._sock.bind((self._host, self._port))
        self._sock.listen()
        self._sock.setblocking(False)
        print(""+Fore.GREEN+"gremlin"+Fore.WHITE+" /meta - "+Fore.BLUE+"PseudoActor"+Fore.WHITE+" ready @ "+Fore.BLUE+"{"+str(self._host)+","+str(self._port)+"}"+Fore.WHITE+"")
    
    def __init_selector__(self):
        self._sel = selectors.DefaultSelector()
        self._sel.register(self._sock, selectors.EVENT_READ, data=None)

    def iserror(self) -> bool:
        return self._iserror
    def msgback(self) -> str:
        return self._msgback
    
    def execute(self):
        """ main execution point fired from gremlin /meta -PseudoActor ! """

        events = self._sel.select(timeout=None)
        for key, mask in events:
            if key.data is None:
                self.__accept_wrapper__(key.fileobj)
            else:
                message = key.data
                        
                try:
                    message.process_events(mask)
                except Exception:
                    self._msgback = f"PAF: {message.addr} = " + traceback.format_exc()
                    print(
                        f"gremlin /meta PseudoActor fault: {message.addr}:\n"
                        f"{self._msgback}"
                    )
                    self._iserror = True
                    message.close()

    def close_out(self):
        self._sel.close()
        self._msgback = self._msgback + "\n [+] --->"  
        self._msgback = self._msgback + Fore.GREEN + " gremlin " + Fore.WHITE
        self._msgback = self._msgback + "/meta "+Fore.BLUE+"PseudoActor"+Fore.WHITE+" closed"

    def __accept_wrapper__(self,sock):
        conn, addr = sock.accept()  
        print(f"Accepted connection from {addr}")
        conn.setblocking(False)
        message = lib.SrvMessage(self._sel, conn, addr)
        self._sel.register(conn, selectors.EVENT_READ, data=message)

# usage example:
if __name__=="__main__":
    if sys.argv.__len__() != 3:
        print(Fore.GREEN + "gremlin"+Fore.WHITE+" /meta - Pseudo-Actor"+Fore.RED+" Fault"+Fore.WHITE)
        print("...expected "+Fore.BLUE+"pseudoactr.py <host> <port>"+Fore.WHITE+"...")
        raise SyntaxError(Fore.RED+"SystaxError"+Fore.WHITE+" starting Pseudo-Actor")

    _h = str(sys.argv[1])
    _p = int(sys.argv[2])
    srv = PseudoActor(_h,_p)

    try:
        while True:
            srv.execute()
    except KeyboardInterrupt: 
        print("Ctrl+C caught, exiting PseudoActor...")
    finally:
        srv.close_out()
    
    print(srv.msgback())
