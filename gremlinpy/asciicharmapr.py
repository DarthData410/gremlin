# +-------------------------------------------------------------------------------------+
# | gremlin - PyFryLabs -> @pyfryday | darth.data410@gmail.com                          |
# | -------                                                                             |
# | asciicharmapr.py is a module for the python code of gremlin that exposes a custom   |
# | hex-bin-ascii char set conversion. Helpful in memory and net packet decoding.       |
# +-------------------------------------------------------------------------------------+
# | Apache License v2.0
# |$>
# | references: 
# |---> https://docs.python.org/3/library/csv.html

import csv as cv

ACMAP='./gremlinpy/res/asciicharmap.csv'
ANULL='NUL'
ANULLR='.'

class asciimaprow:

    _dec = ''
    _hex = ''
    _bin = ''
    _html = ''
    _achar = ''
    _desc = ''
    _isnull = False

    def __init__(self,_row):
        self._dec = _row[0]
        self._hex = _row[1]
        self._bin = _row[2]
        self._html = _row[3]
        self._achar = _row[4]
        self._desc = _row[5]

        if self._achar == ANULL:
            self._isnull = True
        else:
            self._isnull = False
    
    def dec(self) -> str:
        return str(self._dec)
    def hex(self) -> str:
        return str(self._hex)
    def bin(self) -> str:
        return str(self._bin)
    def html(self) -> str:
        return str(self._html)
    def achar(self) -> str:
        return str(self._achar)
    def desc(self) -> str:
        return str(self._desc)
    def isnull(self) -> bool:
        return bool(self._isnull)


class asciimapr:

    _lines = dict()

    def __init__(self):
        self._lines = dict()
        self.__init_map__()
    
    def __init_map__(self):
        try:
            with open(ACMAP, newline='') as f:
                reader = cv.reader(f)
                for row in reader:
                    nacr = asciimaprow(row)
                    self._lines[nacr.hex()] = nacr
        except FileNotFoundError as e:
            print("\033[31m *** CRITICAL -> Missing asciicharmap.csv file. install corrupt ***")

    def hex2char(self,hex,show_null=False,suff=False) -> str:
        """ usage example: a.hex2char('0A') returns LF, a.hex2char('0A',True) returns ac:[LF] """
        ret = ANULLR
        if self._lines.__contains__(hex):
            r = self._lines[hex]
            if r.isnull() and show_null:
                ret = self._lines[hex].achar()
            elif not r.isnull():
                ret = self._lines[hex].achar()
        if ret != '' and suff:
            ret = 'ac:['+ret+']'
        return str(ret)