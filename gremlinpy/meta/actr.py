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

    def __init__(self,host,port) -> None:
        self._host = host
        self._port = port
        self.__init_listen__()
        self.__init_selector__()
    
    def __message_out__(self):
        print("\n ["+Fore.YELLOW+"+"+Fore.RESET+"] --->"+Fore.GREEN+" gremlin"+Fore.RESET+" /meta - "+Fore.BLUE+"Registry"+Fore.RESET+" ready: "+Fore.CYAN+"{"+Fore.MAGENTA+str(self._host)+Fore.RESET+"@"+Fore.MAGENTA+str(self._port)+Fore.CYAN+"}"+Fore.RESET+"")

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
                except Exception:
                    self._msgback = f"PAF: {message.addr} = " + traceback.format_exc()
                    self.__print_except__(message.addr)
                    self._iserror = True
                    message.close()

    def __print_closeout_msg__(self):
        self._msgback = self._msgback + "\n [+] --->"  
        self._msgback = self._msgback + Fore.GREEN + " gremlin " + Fore.WHITE
        self._msgback = self._msgback + "/meta "+Fore.BLUE+"Registry"+Fore.WHITE+" closed"

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
            f""+Fore.GREEN+"gremlin"+Fore.WHITE+" /meta "+Fore.RED+"ReportSrvr fault"+Fore.WHITE+": "+addr+":\n"
            f"{self._msgback}"
        )
    def __print_closeout_msg__(self):
        self._msgback = self._msgback + "\n [+] --->"  
        self._msgback = self._msgback + Fore.GREEN + " gremlin " + Fore.WHITE
        self._msgback = self._msgback + "/meta "+Fore.BLUE+"ReportSrvr"+Fore.WHITE+" closed"
    def __message__(self,conn, addr):
        msg = ReportSrvMsg(self._sel, conn, addr)
        return msg
