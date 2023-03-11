#include "meta.hpp"

meta::meta() {

}

int meta::testpy()
{
    PyObject *pName, *pModule, *pFunc;
    PyObject *pArgs, *pValue, *pValue2;
    int i;

    Py_Initialize();
    //pName = PyUnicode_DecodeFSDefault("gremlinpy.pseudoactr.PseudoActor");
    pName = PyUnicode_DecodeFSDefault("gremlinpy.tester");
    /* Error checking of pName left out */

    pModule = PyImport_Import(pName);
    Py_DECREF(pName);

    if (pModule != NULL) {
        pFunc = PyObject_GetAttrString(pModule, "testcpp");
        /* pFunc is a new reference */

        if (pFunc && PyCallable_Check(pFunc)) {
            pArgs = PyTuple_New(2);
            pValue = PyLong_FromLong(atoi("410"));
            PyTuple_SetItem(pArgs, 0, pValue);
            pValue2 = PyLong_FromLong(atoi("410"));
            PyTuple_SetItem(pArgs, 1, pValue2);
            
            pValue = PyObject_CallObject(pFunc, pArgs);
            Py_DECREF(pArgs);
            
            if (pValue != NULL) {
                printf("Result of call: %ld\n", PyLong_AsLong(pValue));
                Py_DECREF(pValue);
            }
            else {
                Py_DECREF(pFunc);
                Py_DECREF(pModule);
                PyErr_Print();
                fprintf(stderr,"Call failed\n");
                return 1;
            }
        }
        else {
            if (PyErr_Occurred())
                PyErr_Print();
            fprintf(stderr, "Cannot find function\n");
        }
        Py_XDECREF(pFunc);
        Py_DECREF(pModule);
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


