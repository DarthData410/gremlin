# +-------------------------------------------------------------------------------------+
# | gremlin - PyFryLabs -> @pyfryday | darth.data410@gmail.com                          |
# | -------                                                                             |
# | gremcer.py is a submodule for the python code of gremlin that allows for calling of |
# | subprocesses, and then working with the output of said subprocesses.                |
# +-------------------------------------------------------------------------------------+
# | Apache License v2.0
# |$>

import subprocess as sp

class __cer__:

    _c = ['']
    _ret = None
    _iserr = False

    def __init__(self,c=['None']):
        """ supply an array set like: c=['ls','-l']. If c=['None'] returns None """
        self._c = c
        self.__exec__()

    def __exec__(self):
        _ret = None
        
        try:
            _ret = sp.run(self._c, capture_output=True, text=True).stdout
        except sp.CalledProcessError as e:
            _ret = e.stderr
            self._iserr = True
        except FileNotFoundError as fe:
            _ret = fe.strerror
            self._iserr = True
        self._ret = _ret
    
    def iserr(self) -> bool:
        return self._iserr

    def ret(self):
        return self._ret