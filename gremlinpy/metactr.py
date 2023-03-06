# +-------------------------------------------------------------------------------------+
# | gremlin - PyFryLabs -> @pyfryday | darth.data410@gmail.com                          |
# | -------                                                                             |
# | metactr.py is a python module for the gremlin app that directs PseudoActors and     |
# | manuscripts sent from a main actor/parent to child actor/server(s). The metactr.py  |
# | module is also used by pseudo actor(s)/child to parent actor/server to report back  |
# | updates related to the processing of scheduled manuscripts that are being acted on  |
# | by scheduled child/pseudo actors. Such child actors typically would be running on   |
# | multiple workstations/devices/servers to achieve a distrubuted set of acts.         |
# | (part of /meta)                                                                     |
# +-------------------------------------------------------------------------------------+
# | Apache License v2.0
# |$>

import traceback
import selectors
import socket
import metactrclilib as cli

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
        message = cli.Message(self._sel, sock, addr, request)
        self._sel.register(sock, events, data=message)


# usage example:
if __name__ == "__main__":
    act = Actor("192.168.56.10",41013,"search","/ank")
    act.execute()