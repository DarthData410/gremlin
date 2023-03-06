# +-------------------------------------------------------------------------------------+
# | gremlin - PyFryLabs -> @pyfryday | darth.data410@gmail.com                          |
# | -------                                                                             |
# | metactrsrvr.py is a python module for the gremlin app that enables tcp server       |
# | operations for processing both manuscripts by child actors as well as processing    |
# | updates from child actors back to registered parent actor.                          |
# | (part of /meta)                                                                     |
# +-------------------------------------------------------------------------------------+
# | Apache License v2.0
# |$>

import socket
import selectors
import traceback
import metactrsrvrlib as srvr

class PseudoActor:

    _sel = None
    _host = ''
    _port = 0

    def __init__(self,host,port) -> None:
        self._sel = selectors.DefaultSelector()
        self._host = host
        self._port = port 

    def execute(self):
        lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        lsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        lsock.bind((self._host, self._port))
        lsock.listen()
        print(f"Listening on {(self._host, self._port)}")
        lsock.setblocking(False)
        self._sel.register(lsock, selectors.EVENT_READ, data=None)

        try:
            while True:
                events = self._sel.select(timeout=None)
                for key, mask in events:
                    if key.data is None:
                        self.accept_wrapper(key.fileobj)
                    else:
                        message = key.data
                        try:
                            message.process_events(mask)
                        except Exception:
                            print(
                                f"Main: Error: Exception for {message.addr}:\n"
                                f"{traceback.format_exc()}"
                            )
                            message.close()
        except KeyboardInterrupt:
            print("Caught keyboard interrupt, exiting")
        finally:
            self._sel.close()


    def accept_wrapper(self,sock):
        conn, addr = sock.accept()  
        print(f"Accepted connection from {addr}")
        conn.setblocking(False)
        message = srvr.Message(self._sel, conn, addr)
        self._sel.register(conn, selectors.EVENT_READ, data=message)


# usage example:
if __name__=="__main__":
    srv = PseudoActor("192.168.56.10",41013)
    srv.execute()
