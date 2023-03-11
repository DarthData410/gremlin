#include "meta.hpp"

PseudoActor::PseudoActor() {

}

PyObject *PseudoActor::regsrv_tuple() {
    PyObject *ret = PyTuple_New(2);
    ret  = Py_BuildValue("(si)",_regsrvr.host.c_str(),_regsrvr.port);
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

PyObject *PseudoActor::pfbase(PyObject *psainst,const char *_type) {
    PyObject *et = empty_tuple();
    PyObject *func = PyObject_GetAttrString(psainst, _type);
    PyObject *ret = PyObject_CallObject(func,et);
    Py_DECREF(et);
    Py_DECREF(func);
    return ret;
}
void PseudoActor::pf_registerpa(PyObject *psainst) {
    PyObject *ret = pfbase(psainst,pfREGPA);
    Py_DECREF(ret);
}
void PseudoActor::pf_report_server(PyObject *psainst) {
    PyObject *ret = pfbase(psainst,pfREPSRV);
    char *_res;
    PyArg_Parse(ret,"s",&_res);
    _repsrvr.host = _res;
    Py_DECREF(ret);
}
void PseudoActor::pf_report_server_port(PyObject *psainst) {
    PyObject *ret = pfbase(psainst,pfREPSRVPRT);
    int _res;
    PyArg_Parse(ret,"i",&_res);
    _repsrvr.port = _res;
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

        //printf("\n Report Server: %s",_psa._repsrvr.host.c_str());
        //printf("\n Report Server Port: %i",_psa._repsrvr.port);
    }
    else {
        PyErr_Print();
        fprintf(stderr, "Failed to load /meta.py \n");
    }

}
string meta::get_info() {
    string ret = "\n";
    ret += "   +---{/meta->info}\n";
    ret += "   |\n";
    ret += "  [+]--Report Server-> ";
    ret += _psa._repsrvr.host;
    ret += "\n";
    ret += "  [+]--Report Server Port-> ";
    ret += to_string(_psa._repsrvr.port);
    ret += "\n";
    ret += "   |\n";
    ret += "   ^\n";
    return ret;
}

int meta::testpy()
{
    PyObject *pName, *pModule, *pClass, *pClassName, *pPSTup, *pEmptyTup, *pFunc, *pFunc2, *pFunc3, *pClassInt;
    PyObject *pFReqManu, *pManuOBJ, *pFManuObjID;
    PyObject *pArgs, *pValue, *pValue2, *pResult, *pRptSrvr, *pRptSrvPort;
    PyObject *pRReqManuID;
    string arg1="192.168.56.1";
    char *cstr,*manuID;
    int rptPort;
    int i,arg2=41011;

    Py_Initialize();
    pName = PyUnicode_DecodeFSDefault("gremlinpy.meta.pseudoactr");
    printf("...made it pname...");
    //pName = PyUnicode_DecodeFSDefault("gremlinpy.tester");
    /* Error checking of pName left out */

    pModule = PyImport_Import(pName);
    Py_DECREF(pName);

    if (pModule != NULL) {
        pPSTup = PyTuple_New(2);
        pEmptyTup = PyTuple_New(0);
        pClass = PyObject_GetAttrString(pModule, "PseudoActor");
        
        Py_DECREF(pModule);
        printf("..made it pClass..");
        
        pPSTup  = Py_BuildValue("(si)",arg1.c_str(),arg2);
        printf("...made it pPSTup...");
        pClassInt  = PyEval_CallObject(pClass, pPSTup);        // call class(  ) 
        Py_DECREF(pClass);
        Py_DECREF(pPSTup);
        printf("..made it pClassInt..");
        
        pFunc  = PyObject_GetAttrString(pClassInt, "registerpa"); // fetch bound method 

        printf("...made it pFunc...");
        pResult = PyObject_CallObject(pFunc,pEmptyTup);

        pFunc2 = PyObject_GetAttrString(pClassInt, "report_server");
        pRptSrvr = PyObject_CallObject(pFunc2,pEmptyTup);
        PyArg_Parse(pRptSrvr,"s",&cstr);
        pFunc3 = PyObject_GetAttrString(pClassInt, "report_server_port");
        pRptSrvPort = PyObject_CallObject(pFunc3,pEmptyTup);
        PyArg_Parse(pRptSrvPort,"i",&rptPort);

        pFReqManu = PyObject_GetAttrString(pClassInt, "request_manuscript");
        pManuOBJ = PyObject_CallObject(pFReqManu,pEmptyTup);
        pFManuObjID = PyObject_GetAttrString(pClassInt, "manuscriptID");
        pRReqManuID = PyObject_CallObject(pFManuObjID,pEmptyTup);
        PyArg_Parse(pRReqManuID,"s",&manuID);
        
        printf("\n %s",cstr);
        printf("\n %i",rptPort);
        printf("\n %s",manuID);
        printf("\n executed CPP->PY");

        Py_DECREF(pResult);
        Py_DECREF(pClassInt);
        Py_DECREF(pFunc);
        Py_DECREF(pFunc2);
        Py_DECREF(pFunc3);
        Py_DECREF(pEmptyTup);
        Py_DECREF(pRptSrvr);
        Py_DECREF(pRptSrvPort);
    }
    else {
        PyErr_Print();
        fprintf(stderr, "Failed to load\n");
        return 1;
    }
    if (Py_FinalizeEx() < 0) {
        return 120;
    }

    // call to free up memory from any remaining Py objects:
    PyMem_Free(pModule);
    
    return 0;
}

// Reference: http://books.gigatux.nl/mirror/pythonprogramming/0596000855_python2-CHP-20-SECT-5.html
/*
main(  ) {
  // run objects with low-level calls 
  char *arg1="sir", *arg2="robin", *cstr;
  PyObject *pmod, *pclass, *pargs, *pinst, *pmeth, *pres;

  // instance = module.klass(  ) 
  Py_Initialize(  );
  pmod   = PyImport_ImportModule("module");         // fetch module 
  pclass = PyObject_GetAttrString(pmod, "klass");   // fetch module.class 
  Py_DECREF(pmod);

  pargs  = Py_BuildValue("(  )");
  pinst  = PyEval_CallObject(pclass, pargs);        // call class(  ) 
  Py_DECREF(pclass);
  Py_DECREF(pargs);

  // result = instance.method(x,y) 
  pmeth  = PyObject_GetAttrString(pinst, "method"); // fetch bound method 
  Py_DECREF(pinst);
  pargs  = Py_BuildValue("(ss)", arg1, arg2);       // convert to Python 
  pres   = PyEval_CallObject(pmeth, pargs);         // call method(x,y) 
  Py_DECREF(pmeth);
  Py_DECREF(pargs);

  PyArg_Parse(pres, "s", &cstr);                    // convert to C 
  printf("%s\n", cstr);
  Py_DECREF(pres);
} */
