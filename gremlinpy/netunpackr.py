# +-------------------------------------------------------------------------------------+
# | gremlin - PyFryLabs -> @pyfryday | darth.data410@gmail.com                          |
# | -------                                                                             |
# | netpackr.py is a module for the python code of gremlin that reads /ank traced net   |
# | packets and preps for harvesting/data analysis.                                     |
# +-------------------------------------------------------------------------------------+
# | Apache License v2.0
# |$>
# | references: 
# |---> https://stackoverflow.com/questions/15918314/how-to-detect-string-byte-encoding
# |---> https://en.wikipedia.org/wiki/Windows-1252
# |---> https://donsnotes.com/tech/charsets/ascii.html
# |---> https://www.rapidtables.com/code/text/ascii-table.html

import chardet
import io as io
from asciicharmapr import asciimapr

class decyph:

    _lines = list()

    def __init__(self,file):
        """ supply network packet file that contains hex lines for decoding. work with decyph.lines() to operate on """
        amapr = asciimapr()
        f = io.FileIO(file,'r')
        npupl = f.readlines()
        npuplc = list()
        for l in npupl:
            _cx = ''
            _cxt = ''
            l = self.__clean_decode__(l)
            li = 0
            while li < l.__len__():
                _x = str(l[li])
                if _x == "%":
                    # start of line:
                    li += 1
                    continue
                elif _x == ">":
                    # end of line:
                    li += 1
                    continue
                elif _x == " " and _cx.__len__()==2:
                    # detect encoding and decode:
                    tenc = chardet.detect(bytearray.fromhex(_cx))['encoding']
                    if tenc != None:
                        if tenc == 'ascii':
                            _cx = amapr.hex2char(_cx)
                            #_cx = '.'
                            _cxt = _cxt + str(_cx)
                        else:
                            # all other types:
                            _cx = bytearray.fromhex(_cx).decode(encoding=tenc)
                            _cxt = _cxt + str(_cx)
                    else:
                        _cxt = _cxt + " "
                    li += 1
                    _cx = ''
                    continue
                
                elif _x == '.':
                    # packet hex ended:
                    li += 1
                    _cx = ''
                    continue
                
                # add _x value to _cx for hex value char read in:
                else:
                    _cx = _cx + str(_x)
                    li += 1
                    continue
                
            npuplc.append(_cxt)
            _cxt = ''
        
        self._lines = npuplc
    
    def __clean_decode__(self,b) -> str:
        b = b.replace(bytes('[+]-> ','utf-8'),bytes('','utf-8'))
        b = b.replace(bytes('{ ','utf-8'),bytes('%','utf-8'))
        b = b.replace(bytes('}','utf-8'),bytes('>','utf-8'))
        ret = b.decode()
        return ret
    
    def lines(self) -> list:
        return self._lines
    def hex2char(self,hex) -> str:
        ret = ''

        return ret

# usage example:
if __name__ == '__main__':
    
    c = decyph('./gremlinpy/tpl_294.det')
    lines = c.lines()
    for l in lines:
        print(l)
