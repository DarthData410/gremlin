#include "meta.hpp"

PseudoActor::PseudoActor() {

}

PyObject *PseudoActor::regsrv_tuple() {
    PyObject *ret = PyTuple_New(2);
    ret  = Py_BuildValue("(si)",_regsrvr.host.c_str(),_regsrvr.port);
    return ret;
}

PyObject *PseudoActor::idx_tuple(int i) {
    PyObject *ret = PyTuple_New(1);
    ret  = Py_BuildValue("(i)",i);
    return ret;
}

PyObject *PseudoActor::empty_tuple() {
    PyObject *ret = PyTuple_New(0);
    return ret;
}

PyObject *PseudoActor::psa_pyclass(PyObject *pmod) {
    PyObject *ret = PyObject_GetAttrString(pmod, PSA);
    return ret;
}

PyObject *PseudoActor::psa_inst(PyObject *pclass,PyObject *pargs) {
    PyObject *ret = PyEval_CallObject(pclass, pargs);
    return ret;
}

// Uses an empty tuple|args for functions without parameters:
PyObject *PseudoActor::pfbase(PyObject *psainst,const char *_type) {
    PyObject *et = empty_tuple();
    PyObject *ret = pfbase(psainst,_type,et);
    Py_DECREF(et);
    return ret;
}

// Asllows for python tuple|args sent in for functions with parameters:
PyObject *PseudoActor::pfbase(PyObject *psainst,const char *_type,PyObject *_args) {
    PyObject *func = PyObject_GetAttrString(psainst, _type);
    PyObject *ret = PyObject_CallObject(func,_args);
    Py_DECREF(func);
    return ret;
}
string PseudoActor::pys(PyObject *pyobj) {
    string ret;
    char *_res;
    PyArg_Parse(pyobj,"s",&_res);
    ret = _res;
    return ret;
}
int PseudoActor::pyi(PyObject *pyobj) {
    int ret,_ret;
    PyArg_Parse(pyobj,"i",&_ret);
    ret = _ret;
    return ret;
}
bool PseudoActor::pyb(PyObject *pyobj) {
    bool ret,_res;
    PyArg_Parse(pyobj,"b",&_res);
    ret = _res;
    return ret;
}

void PseudoActor::pf_registerpa(PyObject *psainst) {
    PyObject *ret = pfbase(psainst,pfREGPA);
    Py_DECREF(ret);
    pf_paid(psainst);
    pf_parat(psainst);
}
void PseudoActor::pf_paid(PyObject *psainst){
    PyObject *ret = pfbase(psainst,pfREGPAID);
    _paid = pys(ret);
    Py_DECREF(ret);
}
void PseudoActor::pf_parat(PyObject *psainst){
    PyObject *ret = pfbase(psainst,pfREGPARAT);
    _parat = pys(ret);
    Py_DECREF(ret);
}
void PseudoActor::pf_request_manuscript(PyObject *psainst) {
    PyObject *ret = pfbase(psainst,pfREQMANU);
    Py_DECREF(ret);
    // build manuscript struct:
    PyObject *manuid = pfbase(psainst,pfMANU_ID);
    _manuscript.ManuscriptID = pys(manuid);
    Py_DECREF(manuid);
    // -
    PyObject *actnow = pfbase(psainst,pfMANU_ACTNOW);
    _manuscript.ActorNow = pys(actnow);
    Py_DECREF(actnow);
    // -
    PyObject *type = pfbase(psainst,pfMANU_TYPE);
    _manuscript.Type = pyi(type);
    Py_DECREF(type);
    // -
    PyObject *psaid = pfbase(psainst,pfMANU_PSAID);
    _manuscript.PseudoActor = pys(psaid);
    Py_DECREF(psaid);
    // -
    PyObject *numacts = pfbase(psainst,pfMANU_NUMACT);
    _manuscript.NumOfActs = pyi(numacts);
    Py_DECREF(numacts);

    // build out acts|schedule:
    for(int i=0;i<_manuscript.NumOfActs;i++) {
        act a = pf_getact(psainst,i);
        _acts.push_back(a);
    }
}

act PseudoActor::pf_getact(PyObject *psainst,int idx) {
    act ret = act(); 
    PyObject *args = idx_tuple(idx);
    // seq:
    PyObject *seq = pfbase(psainst,pfMANUACT_SEQ,args);
    string rseq = pys(seq);
    Py_DECREF(seq);
    // command:
    PyObject *comm = pfbase(psainst,pfMANUACT_COMM,args);
    string rcomm = pys(comm);
    Py_DECREF(comm);
    // args:
    PyObject *aargs = pfbase(psainst,pfMANUACT_ARGS,args);
    string raargs = pys(aargs);
    Py_DECREF(aargs);
    // output:
    PyObject *output = pfbase(psainst,pfMANUACT_OUT,args);
    int routput = pyi(output);
    Py_DECREF(output);
    // output:
    PyObject *chrono = pfbase(psainst,pfMANUACT_CHRONO,args);
    int rchrono = pyi(chrono);
    Py_DECREF(chrono);

    // set act:
    ret.Seq = rseq;
    ret.Command = rcomm;
    ret.Args = raargs;
    ret.Output = routput;
    ret.Chrono = rchrono;

    Py_DECREF(args);
    return ret;
}

bool PseudoActor::process_manuscript(PyObject *psainst) {
    bool ret = false;
    for(int i=0;i<_acts.size();i++) {
        Act a = _acts[i];
        //printf("<...starting /meta->manuscript->acts->%s::%s in %i seconds...> \n",a.Seq.c_str(),a.Command.c_str(),a.Chrono);
        chrono::steady_clock::time_point tp = chrono::steady_clock::now() + chrono::seconds(a.Chrono);
	    this_thread::sleep_until(tp);
        PyObject *args = idx_tuple(i);
        PyObject *ares = pfbase(psainst,pfMANUACT_EXEC,args);
        int _aer = pyi(ares);
        Py_DECREF(ares);
        Py_DECREF(args);
        if(_aer==1) {
            ret = ret && true;
        }
        else {
            ret = ret && false;
        }
        
        PyObject *ermsg = pfbase(psainst,pfMANUACT_EXECMSG);
        ActResult ar = ActResult();
        ar.ResAct = a;
        ar.Result = pys(ermsg);
        Py_DECREF(ermsg);
        _actresults.push_back(ar);
    }
    return ret;
}

void PseudoActor::pf_report_server(PyObject *psainst) {
    PyObject *ret = pfbase(psainst,pfREPSRV);
    _repsrvr.host = pys(ret);
    Py_DECREF(ret);
}
void PseudoActor::pf_report_server_port(PyObject *psainst) {
    PyObject *ret = pfbase(psainst,pfREPSRVPRT);
    _repsrvr.port = pyi(ret);
    Py_DECREF(ret);
}

meta::meta(string _rsrvr,int _rsrvrport) {
    _psa = PseudoActor();
    _psa._regsrvr = RegistryServer();
    _psa._regsrvr.host = _rsrvr;
    _psa._regsrvr.port = _rsrvrport;
}

void meta::execute_as_psa() {
    PyObject *pName,*pModule,*pcPSA,*piPSA;
    PyObject *piPSAargs;

    Py_Initialize();
    pName = PyUnicode_DecodeFSDefault(GREMPY);
    pModule = PyImport_Import(pName);

    if(pModule != NULL) {
        pcPSA = _psa.psa_pyclass(pModule);
        piPSAargs = _psa.regsrv_tuple();
        piPSA = _psa.psa_inst(pcPSA,piPSAargs);
        // register and set report server variables:
        _psa.pf_registerpa(piPSA);
        _psa.pf_report_server(piPSA);
        _psa.pf_report_server_port(piPSA);
        _psa.pf_request_manuscript(piPSA);
        _psa.process_manuscript(piPSA);
        
    }
    else {
        PyErr_Print();
        fprintf(stderr, "Failed to load /meta.py \n");
    }

}
string meta::get_info() {
    string ret = "";
    ret += "    +-{/meta->info}\n";
    ret += "    |\n";
    ret += "   [+]--Registry Server-> ";
    ret += _psa._regsrvr.host;
    ret += "\n";
    ret += "   [+]--Registry Server Port-> ";
    ret += to_string(_psa._regsrvr.port);
    ret += "\n";
    ret += "   [+]--Pseudo-Actor ID-> ";
    ret += _psa._paid;
    ret += "\n";
    ret += "   [+]--Pseudo-Actor @-> ";
    ret += _psa._parat;
    ret += "\n";
    ret += "   [+]--Report Server-> ";
    ret += _psa._repsrvr.host;
    ret += "\n";
    ret += "   [+]--Report Server Port-> ";
    ret += to_string(_psa._repsrvr.port);
    ret += "\n";
    ret += "    |\n";
    ret += "    |-{/meta->info->manuscript}\n";
    ret += "   [+]--Manuscript ID-> ";
    ret += _psa._manuscript.ManuscriptID;
    ret += "\n";
    ret += "   [+]--Actor Now @-> ";
    ret += _psa._manuscript.ActorNow;
    ret += "\n";
    ret += "   [+]--Type-> ";
    ret += to_string(_psa._manuscript.Type);
    ret += "\n";
    ret += "   [+]--Number of Acts-> ";
    ret += to_string(_psa._manuscript.NumOfActs);
    ret += "\n";
    ret += "    |\n";
    ret += "    |-{/meta->info->manuscript->act results}\n";
    
        for(ActResult ar : _psa._actresults) {
            ret += "   [+]--Command->";
            ret += ar.ResAct.Command;
            ret += "\n";
            ret += "   [+]--Result:\n";
            ret += "    " + ar.Result;
            ret += "\n    --------<end>\n";        
        }
    
    ret += "    |\n";
    ret += "    ^";
    return ret;
}


