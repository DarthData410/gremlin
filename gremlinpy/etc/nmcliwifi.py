# +-------------------------------------------------------------------------------------+
# | gremlin - PyFryLabs -> @pyfryday | darth.data410@gmail.com                          |
# | -------                                                                             |
# | nmcliwifi.py is a module for the python code of gremlin that allows for sweeping &  |
# | harvesting wifi network information at a given point-in-time.                       |
# | (wraps nmcli dev wifi)                                                              |
# +-------------------------------------------------------------------------------------+
# | Apache License v2.0
# |$>

import json as json
from datetime import datetime
import gremcer as grem

UUIDGC=['uuidgen']
NMCLIR=['nmcli','dev','wifi']
JSONLOC='./'        

class nmcline:

    _slb = list()

    def __init__(self,sl):
        self._slb = self.__init_list__()
        sl = sl.split(',')
        i = 0
        for s in sl:
            if s != '' and self._slb[7] == '':
                self._slb[i] = s
                i += 1
            elif s != '' and self._slb[7] != '':
                self._slb[7] = self._slb[7] + "-" + s
                i += 1

    
    def __init_list__(self) -> list:
        ret = list()
        i = 0
        while i <= 7:
            ret.append('')
            i+=1
        
        return ret

    def bssid(self) -> str:
        return self._slb[0]
    def ssid(self) -> str:
        return self._slb[1]
    def mode(self) -> str:
        return self._slb[2]
    def chan(self) -> str:
        return self._slb[3]
    def rate(self) -> str:
        return self._slb[4]
    def signal(self) -> str:
        return self._slb[5]
    def bars(self) -> str:
        return self._slb[6]
    def security(self) -> str:
        return self._slb[7]
    def asdict(self) -> dict:
        ret = dict()
        ret["bssid"] = self.bssid()
        ret["ssid"] = self.ssid()
        ret["mode"] = self.mode()
        ret["chan"] = self.chan()
        ret["rate"] = self.rate()
        ret["signal"] = self.signal()
        ret["security"] = self.security()
        return ret

class nmclijson: 

    _lines = list()
    _uuid = ''
    _tnow = ''
    _filename = ''

    def __init__(self,lines,uuid,tnow):
        self._lines = lines
        self._uuid = str(uuid).replace('\n','')
        self._tnow = tnow
        self._filename = self._uuid+".json"
        
        # process passed in lines:
        jdoc = dict()
        jdoc["document"] = "[gremlin - *nix security framework]::gremlinpy.nmcliwifi.sweeper scan details"
        jdoc["date"] = self._tnow

        # build networks:
        jdocnets = dict()
        for l in self._lines:
            netdoc = l.asdict()
            jdocnets[l.bssid()]=netdoc
        
        # combine now:
        jdoc["networks"] = jdocnets

        # Serializing json
        json_object = json.dumps(jdoc, indent=4)

        # Writing to sample.json
        with open(self._filename, "w") as outfile:
            outfile.write(json_object)
    
    def filename(self) -> str:
        return self._filename


class sweeper:

    _cmd = ''
    _jsono = False
    _jsonl = ''
    _lines = list()
    _iserr = False
    _msg = ''
    
    def __init__(self,_cmd=NMCLIR,_json=False,_jsonloc=JSONLOC) -> None:
        
        self._cmd = _cmd
        self._jsono = _json
        self._jsonl = _jsonloc
        self.__exec__()
    
    def __exec__(self):
        cx = grem.__cer__(self._cmd)
        
        if cx.iserr():
            self._iserr = True
            self._msg = 'sweeper error: ' + cx.ret()
            return
        
        rl = cx.ret().splitlines()
        i = 0
        for r in rl:
            
            if i == 0:
                i += 1
                continue
            
            # clean inbound data:
            r = r.replace('*','')
            r = r.lstrip()
            r = r.replace(' Mbit/s','Mb/s')
            r = r.replace('WPA1 802.1X','WPA1-802.1X')
            r = r.replace('WPA2 802.1X','WPA2-802.1X')
            r = r.replace('WPA1 WPA2','WPA1-WPA2')
            r = r.replace('WPA1 WPA2 802.1X','WPA1-WPA2-802.1X')
            r = r.replace(' ',',')
            
            nmc = nmcline(r)
            self._lines.append(nmc)
        
    def __getnow__(self) -> str:
        """ returns datetime.now() in Y-M-D~H::M::S str format. """
        now = datetime.now()
        ret = now.strftime("%Y-%m-%d~%H::%M::%S")
        return ret  

    def __getfuid__(self) -> str:
        """ returns a safe uuid to use within app or file/dir names """
        ret = ''
        cx = grem.__cer__(UUIDGC)
        ret = cx.ret()
        
        return ret

    def lines(self) -> list:
        return self._lines
    def writejson(self) -> str:
        """ returns json generated file location/name.json """
        ret = ''
        jf = nmclijson(self.lines(),self.__getfuid__(),self.__getnow__())
        ret = jf.filename()
        return ret

########################################
# usage example:
if __name__ == '__main__':
    s = sweeper()
    lines = s.lines()
    for l in lines:
        print(l.bssid())
        print(l.ssid())
        print(l.security())
    
    print(s.__getnow__())
    jfn = s.writejson()
    print(jfn)