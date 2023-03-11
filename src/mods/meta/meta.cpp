#include "meta.hpp"

meta::meta() {

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
