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
import actrlib as lib

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
    
    def __init_listen__(self):
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._sock.bind((self._host, self._port))
        self._sock.listen()
        self._sock.setblocking(False)
        print("\n [+] --->"+Fore.GREEN+" gremlin"+Fore.WHITE+" /meta - "+Fore.BLUE+"Registry"+Fore.WHITE+" ready @ "+Fore.BLUE+"{"+str(self._host)+","+str(self._port)+"}"+Fore.WHITE+"")
    
    def __init_selector__(self):
        self._sel = selectors.DefaultSelector()
        self._sel.register(self._sock, selectors.EVENT_READ, data=None)

    def iserror(self) -> bool:
        return self._iserror
    def msgback(self) -> str:
        return self._msgback
    
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
                    print(
                        f"gremlin /meta Registry fault: {message.addr}:\n"
                        f"{self._msgback}"
                    )
                    self._iserror = True
                    message.close()

    def close_out(self):
        self._sel.close()
        self._msgback = self._msgback + "\n [+] --->"  
        self._msgback = self._msgback + Fore.GREEN + " gremlin " + Fore.WHITE
        self._msgback = self._msgback + "/meta "+Fore.BLUE+"Registry"+Fore.WHITE+" closed"

    def __accept_wrapper__(self,sock):
        conn, addr = sock.accept()  
        print(f"Accepted connection from {addr}")
        conn.setblocking(False)
        msg = lib.RegisterMsg(self._sel, conn, addr)
        self._sel.register(conn, selectors.EVENT_READ, data=msg)


class Actor:

    _sel = None
    _host = ''
    _port = 0
    _action = ''
    _value = ''
    
    def __init__(self,host,port,action,value) -> None:
        self._sel = selectors.DefaultSelector()
        self._host = host
        self._port = port
        self._action = action
        self._value = value

    def execute(self):
        request = self.create_request(self._action, self._value)
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

    def start_connection(self,host, port, request):
        addr = (host, port)
        print(f"Starting connection to {addr}")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setblocking(False)
        sock.connect_ex(addr)
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        message = lib.CliMessage(self._sel, sock, addr, request)
        self._sel.register(sock, events, data=message)
