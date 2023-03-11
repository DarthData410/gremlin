# +-------------------------------------------------------------------------------------+
# | gremlin - PyFryLabs -> @pyfryday | darth.data410@gmail.com                          |
# | -------                                                                             |
# | actrlib.py is a python module for the gremlin app /meta mod that enables tcp net    |
# | communication for the actors & pseudo-actors that are parent/child instances.       |
# | (part of /meta)                                                                     |
# +-------------------------------------------------------------------------------------+
# | Apache License v2.0
# |$>

import sys
import struct
import selectors
import io
import json
from colorama import Fore
# /meta JSON/data contracts:
from datacontracts.register import *
from datacontracts.manuscript import *
from datacontracts.datasys import *

# Client Message Operations:
class CliMessage:
    def __init__(self, selector, sock, addr, request):
        self.selector = selector
        self.sock = sock
        self.addr = addr
        self.request = request
        self._recv_buffer = b""
        self._send_buffer = b""
        self._request_queued = False
        self._jsonheader_len = None
        self.jsonheader = None
        self.response = None
        self.result = None

    def return_result(self):
        return self.result

    def _set_selector_events_mask(self, mode):
        """Set selector to listen for events: mode is 'r', 'w', or 'rw'."""
        if mode == "r":
            events = selectors.EVENT_READ
        elif mode == "w":
            events = selectors.EVENT_WRITE
        elif mode == "rw":
            events = selectors.EVENT_READ | selectors.EVENT_WRITE
        else:
            raise ValueError(f"Invalid events mask mode {mode!r}.")
        self.selector.modify(self.sock, events, data=self)

    def _read(self):
        try:
            # Should be ready to read
            data = self.sock.recv(4096)
        except BlockingIOError:
            # Resource temporarily unavailable (errno EWOULDBLOCK)
            pass
        else:
            if data:
                self._recv_buffer += data
            else:
                raise RuntimeError("Peer closed.")

    def _write(self):
        if self._send_buffer:
            #print(f"Sending {self._send_buffer!r} to {self.addr}")
            try:
                # Should be ready to write
                sent = self.sock.send(self._send_buffer)
            except BlockingIOError:
                # Resource temporarily unavailable (errno EWOULDBLOCK)
                pass
            else:
                self._send_buffer = self._send_buffer[sent:]

    def _json_encode(self, obj, encoding):
        return json.dumps(obj, ensure_ascii=False).encode(encoding)

    def _json_decode(self, json_bytes, encoding):
        tiow = io.TextIOWrapper(
            io.BytesIO(json_bytes), encoding=encoding, newline=""
        )
        obj = json.load(tiow)
        tiow.close()
        return obj

    def _create_message(
        self, *, content_bytes, content_type, content_encoding
    ):
        jsonheader = {
            "byteorder": sys.byteorder,
            "content-type": content_type,
            "content-encoding": content_encoding,
            "content-length": len(content_bytes),
        }
        jsonheader_bytes = self._json_encode(jsonheader, "utf-8")
        message_hdr = struct.pack(">H", len(jsonheader_bytes))
        message = message_hdr + jsonheader_bytes + content_bytes
        return message

    def _process_response_json_content(self):
        content = self.response
        result = content.get("result")
        #print(f"Got result: {result}")

    def _process_response_binary_content(self):
        content = self.response
        #print(f"Got response: {content!r}")

    def process_events(self, mask):
        if mask & selectors.EVENT_READ:
            self.read()
        if mask & selectors.EVENT_WRITE:
            self.write()

    def read(self):
        self._read()

        if self._jsonheader_len is None:
            self.process_protoheader()

        if self._jsonheader_len is not None:
            if self.jsonheader is None:
                self.process_jsonheader()

        if self.jsonheader:
            if self.response is None:
                self.process_response()

    def write(self):
        if not self._request_queued:
            self.queue_request()

        self._write()

        if self._request_queued:
            if not self._send_buffer:
                # Set selector to listen for read events, we're done writing.
                self._set_selector_events_mask("r")

    def close(self):
       # print(f"Closing connection to {self.addr}")
        try:
            self.selector.unregister(self.sock)
        except Exception as e:
            print(
                f"Error: selector.unregister() exception for "
                f"{self.addr}: {e!r}"
            )

        try:
            self.sock.close()
        except OSError as e:
            print(f"Error: socket.close() exception for {self.addr}: {e!r}")
        finally:
            # Delete reference to socket object for garbage collection
            self.sock = None

    def queue_request(self):
        content = self.request["content"]
        content_type = self.request["type"]
        content_encoding = self.request["encoding"]
        if content_type == "text/json":
            req = {
                "content_bytes": self._json_encode(content, content_encoding),
                "content_type": content_type,
                "content_encoding": content_encoding,
            }
        else:
            req = {
                "content_bytes": content,
                "content_type": content_type,
                "content_encoding": content_encoding,
            }
        message = self._create_message(**req)
        self._send_buffer += message
        self._request_queued = True

    def process_protoheader(self):
        hdrlen = 2
        if len(self._recv_buffer) >= hdrlen:
            self._jsonheader_len = struct.unpack(
                ">H", self._recv_buffer[:hdrlen]
            )[0]
            self._recv_buffer = self._recv_buffer[hdrlen:]

    def process_jsonheader(self):
        hdrlen = self._jsonheader_len
        if len(self._recv_buffer) >= hdrlen:
            self.jsonheader = self._json_decode(
                self._recv_buffer[:hdrlen], "utf-8"
            )
            self._recv_buffer = self._recv_buffer[hdrlen:]
            for reqhdr in (
                "byteorder",
                "content-length",
                "content-type",
                "content-encoding",
            ):
                if reqhdr not in self.jsonheader:
                    raise ValueError(f"Missing required header '{reqhdr}'.")

    def process_response(self):
        content_len = self.jsonheader["content-length"]
        if not len(self._recv_buffer) >= content_len:
            return
        data = self._recv_buffer[:content_len]
        self._recv_buffer = self._recv_buffer[content_len:]
        if self.jsonheader["content-type"] == "text/json":
            encoding = self.jsonheader["content-encoding"]
            self.response = self._json_decode(data, encoding)
            #print(f"Received response {self.response!r} from {self.addr}")
            self._process_response_json_content()
        
        self.close()

class CliRegACKMsg(CliMessage):

    def __init__(self, selector, sock, addr, request):
        super().__init__(selector, sock, addr, request)
    
    def _process_response_json_content(self):
        content = self.response
        result = content.get("result")
        r = result 
        ra = regACK.fromdict(r)
        self.result = ra
    
class CliReqManuscript(CliMessage):
    def __init__(self, selector, sock, addr, request):
        super().__init__(selector, sock, addr, request)
    
    def _process_response_json_content(self):
        content = self.response
        result = content.get("result")
        r = result 
        manu = manuscript.fromdict(r)
        self.result = manu
        
class CliReqHeartBeat(CliMessage):
    def __init__(self, selector, sock, addr, request):
        super().__init__(selector, sock, addr, request)
    
    def _process_response_json_content(self):
        content = self.response
        result = content.get("result")
        hback = ACK.fromdict(result)
        self.result = hback

class CliReqActUpdate(CliMessage):
    def __init__(self, selector, sock, addr, request):
        super().__init__(selector, sock, addr, request)
    
    def _process_response_json_content(self):
        content = self.response
        result = content.get("result")
        print(Fore.GREEN+" *** RESPNOSE->ReportSrvr::CliReqActUpdate::ACK ***"+Fore.WHITE)
        hback = ACK.fromdict(result)
        self.result = hback

class CliReqManuComplete(CliMessage):
    def __init__(self, selector, sock, addr, request):
        super().__init__(selector, sock, addr, request)
    
    def _process_response_json_content(self):
        content = self.response
        result = content.get("result")
        print(Fore.GREEN+" *** RESPNOSE->ReportSrvr::CliReqManuComplete::ACK ***"+Fore.WHITE)
        hback = ACK.fromdict(result)
        self.result = hback
        
# Server Message Operations:        
class SrvMessage:
    def __init__(self, selector, sock, addr):
        self.selector = selector
        self.sock = sock
        self.addr = addr
        self._recv_buffer = b""
        self._send_buffer = b""
        self._jsonheader_len = None
        self.jsonheader = None
        self.request = None
        self.response_created = False

    def _set_selector_events_mask(self, mode):
        """Set selector to listen for events: mode is 'r', 'w', or 'rw'."""
        if mode == "r":
            events = selectors.EVENT_READ
        elif mode == "w":
            events = selectors.EVENT_WRITE
        elif mode == "rw":
            events = selectors.EVENT_READ | selectors.EVENT_WRITE
        else:
            raise ValueError(f"Invalid events mask mode {mode!r}.")
        self.selector.modify(self.sock, events, data=self)

    def _read(self):
        try:
            # Should be ready to read
            data = self.sock.recv(4096)
        except BlockingIOError:
            # Resource temporarily unavailable (errno EWOULDBLOCK)
            pass
        else:
            if data:
                self._recv_buffer += data
            else:
                raise RuntimeError("Peer closed.")

    def _write(self):
        if self._send_buffer:
            #print(f"Sending {self._send_buffer!r} to {self.addr}")
            try:
                # Should be ready to write
                sent = self.sock.send(self._send_buffer)
            except BlockingIOError:
                # Resource temporarily unavailable (errno EWOULDBLOCK)
                pass
            else:
                self._send_buffer = self._send_buffer[sent:]
                # Close when the buffer is drained. The response has been sent.
                if sent and not self._send_buffer:
                    self.close()

    def _json_encode(self, obj, encoding):
        return json.dumps(obj, ensure_ascii=False).encode(encoding)

    def _json_decode(self, json_bytes, encoding):
        tiow = io.TextIOWrapper(
            io.BytesIO(json_bytes), encoding=encoding, newline=""
        )
        obj = json.load(tiow)
        tiow.close()
        return obj

    def _create_message(
        self, *, content_bytes, content_type, content_encoding
    ):
        jsonheader = {
            "byteorder": sys.byteorder,
            "content-type": content_type,
            "content-encoding": content_encoding,
            "content-length": len(content_bytes),
        }
        jsonheader_bytes = self._json_encode(jsonheader, "utf-8")
        message_hdr = struct.pack(">H", len(jsonheader_bytes))
        message = message_hdr + jsonheader_bytes + content_bytes
        return message
        
    def _create_response_json_content(self):
        
        #default:
        content = {"result": "GENERIC RETURN|INVALID REQ"}
        content_encoding = "utf-8"

        response = {
            "content_bytes": self._json_encode(content, content_encoding),
            "content_type": "text/json",
            "content_encoding": content_encoding,
        }
        
        return response

    def _create_response_binary_content(self):
        response = {
            "content_bytes": b"First 10 bytes of request: "
            + self.request[:10],
            "content_type": "binary/custom-server-binary-type",
            "content_encoding": "binary",
        }
        return response

    def process_events(self, mask):
        if mask & selectors.EVENT_READ:
            self.read()
        if mask & selectors.EVENT_WRITE:
            self.write()

    def read(self):
        self._read()

        if self._jsonheader_len is None:
            self.process_protoheader()

        if self._jsonheader_len is not None:
            if self.jsonheader is None:
                self.process_jsonheader()

        if self.jsonheader:
            if self.request is None:
                self.process_request()

    def write(self):
        if self.request:
            if not self.response_created:
                self.create_response()

        self._write()

    def close(self):
        #print(f"Closing connection to {self.addr}")
        try:
            self.selector.unregister(self.sock)
        except Exception as e:
            print(
                f"Error: selector.unregister() exception for "
                f"{self.addr}: {e!r}"
            )

        try:
            self.sock.close()
        except OSError as e:
            print(f"Error: socket.close() exception for {self.addr}: {e!r}")
        finally:
            # Delete reference to socket object for garbage collection
            self.sock = None

    def process_protoheader(self):
        hdrlen = 2
        if len(self._recv_buffer) >= hdrlen:
            self._jsonheader_len = struct.unpack(
                ">H", self._recv_buffer[:hdrlen]
            )[0]
            self._recv_buffer = self._recv_buffer[hdrlen:]

    def process_jsonheader(self):
        hdrlen = self._jsonheader_len
        if len(self._recv_buffer) >= hdrlen:
            self.jsonheader = self._json_decode(
                self._recv_buffer[:hdrlen], "utf-8"
            )
            self._recv_buffer = self._recv_buffer[hdrlen:]
            for reqhdr in (
                "byteorder",
                "content-length",
                "content-type",
                "content-encoding",
            ):
                if reqhdr not in self.jsonheader:
                    raise ValueError(f"Missing required header '{reqhdr}'.")

    def process_request(self):
        content_len = self.jsonheader["content-length"]
        if not len(self._recv_buffer) >= content_len:
            return
        data = self._recv_buffer[:content_len]
        self._recv_buffer = self._recv_buffer[content_len:]
        if self.jsonheader["content-type"] == "text/json":
            encoding = self.jsonheader["content-encoding"]
            self.request = self._json_decode(data, encoding)
            print(Fore.BLUE+"...processing request from: "+Fore.GREEN+str(self.addr[0])+"@"+str(self.addr[1])+Fore.WHITE)
            #print(f"Received request {self.request!r} from {self.addr}")
        
        # Set selector to listen for write events, we're done reading.
        self._set_selector_events_mask("w")

    def create_response(self):
        if self.jsonheader["content-type"] == "text/json":
            response = self._create_response_json_content()
            #response = self._create_registry_json_response()
        else:
            # Binary or unknown content-type
            response = self._create_response_binary_content()
        message = self._create_message(**response)
        self.response_created = True
        self._send_buffer += message

class RegisterMsg(SrvMessage) : 

    def __init__(self, selector, sock, addr):
        super().__init__(selector, sock, addr) 
    
    def _create_response_json_content(self):
        _reg = self.request.get("register")
        _regjs = json.dumps(_reg)
        regi = reginfo.fromjson(_regjs)

        # build reply:
        rACK = regACK(
            PseudoActor=regi.PseudoActor,
            ManuHost="192.168.56.1",
            ManuPort=41001,
            Registered=True
        )

        resultd = dict()
        resultd["result"] = rACK.todict()

        encoding = "utf-8"
        resp = {
            "content_bytes": self._json_encode(resultd, encoding),
            "content_type": "text/json",
            "content_encoding": encoding,
        }
        return resp

class ReportSrvMsg(SrvMessage) : 

    def __init__(self, selector, sock, addr):
        super().__init__(selector, sock, addr) 
    
    def __manuscript_completed_response__(self): 
        _req = self.request.get("manuscriptcomplete_request")
        r = REQ.fromdict(_req)

        mc = ManuscriptCompleted.fromdict(r.ReqMsg)
        ra = ACK.fromreq(r)
        ra.AckMsg="ACK::"+Fore.CYAN+"ManuscriptCompleted"+Fore.WHITE+"::"+Fore.LIGHTBLUE_EX+"["+Fore.LIGHTCYAN_EX+mc.ManuscriptID+Fore.WHITE+"::"+Fore.LIGHTMAGENTA_EX+r.PseudoActor+Fore.WHITE+"@"+Fore.LIGHTGREEN_EX+mc.Now+Fore.LIGHTBLUE_EX+"]"+Fore.RESET
        print(ra.AckMsg)

        resultd = dict()
        resultd["result"] = ra.todict()

        encoding = "utf-8"
        resp = {
            "content_bytes": self._json_encode(resultd, encoding),
            "content_type": "text/json",
            "content_encoding": encoding,
        }
        return resp

    def __act_result_response__(self): 
        _req = self.request.get("actupdate_request")
        r = REQ.fromdict(_req)
    
        au = actUpdate.fromdict(r.ReqMsg)
        a = act.fromdict(au.UpAct)
        ra = ACK.fromreq(r)

        ra.AckMsg = "ACK::"+Fore.CYAN+"ActUpdate"+Fore.LIGHTBLUE_EX+"["+Fore.LIGHTCYAN_EX+a.Seq+Fore.WHITE+"::"+Fore.LIGHTMAGENTA_EX+a.Command+Fore.LIGHTBLUE_EX+"]"+Fore.RESET

        resultd = dict()
        resultd["result"] = ra.todict()

        encoding = "utf-8"
        resp = {
            "content_bytes": self._json_encode(resultd, encoding),
            "content_type": "text/json",
            "content_encoding": encoding,
        }
        return resp

    def __heartbeat_response__(self):
        _req = self.request.get("heartbeat_request")
        r = REQ.fromdict(_req)
        print("...heartbeat: "+Fore.GREEN+r.PseudoActor+Fore.WHITE)
        ra = ACK.fromreq(r)

        resultd = dict()
        ra.AckMsg = "ACK::"+Fore.CYAN+"HeartBeat"+Fore.LIGHTBLUE_EX+"["+Fore.LIGHTCYAN_EX+r.ReqID+Fore.WHITE+"::"+Fore.LIGHTMAGENTA_EX+r.PseudoActor+Fore.LIGHTBLUE_EX+"]"+Fore.RESET
        resultd["result"] = ra.todict()

        encoding = "utf-8"
        resp = {
            "content_bytes": self._json_encode(resultd, encoding),
            "content_type": "text/json",
            "content_encoding": encoding,
        }
        return resp
    
    def __manuscript_response__(self):
        _reg = self.request.get("manuscript_request")
        regi = RequestManuscript.fromdict(_reg)

        print("...manuscript for: "+Fore.GREEN+regi.PseudoActor+Fore.WHITE+" @ "+Fore.BLUE+regi.RequestNow+Fore.WHITE)

        al = list()
        a = act(
            Seq="01",
            Command="/Test1",
            Args="Arg1",
            Output=1,
            Chrono=30
        )
        al.append(a)

        retManu = manuscript(
            ManuscriptID=genuid(),
            PseudoActor=regi.PseudoActor,
            ReportingPort=regi.ReportPort,
            ActorNow=regi.RequestNow,
            Type=1,
            NumOfActs=1,
            Acts=al
        )

        resultd = dict()
        resultd["result"] = retManu.todict()

        encoding = "utf-8"
        resp = {
            "content_bytes": self._json_encode(resultd, encoding),
            "content_type": "text/json",
            "content_encoding": encoding,
        }
        return resp

    def _create_response_json_content(self):
        
        # detect request type:
        if self.request.__contains__("heartbeat_request"):
            return self.__heartbeat_response__()
        elif self.request.__contains__("manuscript_request"):
            return self.__manuscript_response__()
        elif self.request.__contains__("actupdate_request"):
            return self.__act_result_response__()
        elif self.request.__contains__("manuscriptcomplete_request"):
            return self.__manuscript_completed_response__()
        else:
            # generic ACK back to NVREQ = Non-Valid REQuest
            genACK = ACK(
                HostFrom=self.addr,
                HostPort=0,
                AckMsg="NVREQ",
                AckNow=getnow(),
                ReqID=genuid()
            )

            resultd = dict()
            resultd["result"] = genACK.todict()

            encoding = "utf-8"
            resp = {
                "content_bytes": self._json_encode(resultd, encoding),
                "content_type": "text/json",
                "content_encoding": encoding,
            }
            return resp