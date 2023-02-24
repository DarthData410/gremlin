#include "gremlin.hpp"

int main() {

    format fm = format();
    gremlin g = gremlin();
    string rcmd = "";

    // set *this* program as Py_SetProgramName value.:
    wchar_t *program = Py_DecodeLocale("gremlin", NULL);
    Py_SetProgramName(program); 
    
    Py_Initialize();
    
    //PyRun_SimpleString("print('...hello from python3...')");
    
    g.run("_");
    cout << g.ret();\
    cin >> rcmd;

    while(g.run(rcmd)) {
        cout << g.ret();\
        cin >> rcmd;
    }
    
    cout << g.ret() << endl;

    if (Py_FinalizeEx() < 0) {
        exit(120);
    }
    
    // remove any memory related to *this* program.:
    PyMem_RawFree(program);
    return 0;
}