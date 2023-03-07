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

import socket
import selectors
import traceback
import actrsrvrlib as srvr

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
        print(f"gremlin /meta - PseudoActor ready @ {(self._host, self._port)}")
    
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
        self._msgback = self._msgback + "\n [+] ---> gremlin /meta PseudoActor closed"

    def __accept_wrapper__(self,sock):
        conn, addr = sock.accept()  
        print(f"Accepted connection from {addr}")
        conn.setblocking(False)
        message = srvr.Message(self._sel, conn, addr)
        self._sel.register(conn, selectors.EVENT_READ, data=message)


# usage example:
if __name__=="__main__":
    srv = PseudoActor("192.168.56.1",41013)
    
    try:
        while True:
            srv.execute()
    except KeyboardInterrupt: 
        print("Ctrl+C caught, exiting PseudoActor...")
    finally:
        srv.close_out()
    
    print(srv.msgback())
