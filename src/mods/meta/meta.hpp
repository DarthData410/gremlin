#include <iostream>
#include <vector>
#define PY_SSIZE_T_CLEAN
#include <python3.10/Python.h>

using namespace std;

#define GREMPY "gremlinpy.meta.pseudoactr"
#define PSA "PseudoActor"
// py function constants:
#define pfREGPA "registerpa"
#define pfREPSRV "report_server"
#define pfREPSRVPRT "report_server_port"

typedef struct server {
    string host;
    int port;
} RegistryServer,ReportServer;

typedef struct reg {
    string paid;
    string rat;
    bool isreg;
} Register;

typedef struct manuscript {
    string ManuscriptID;
    string PseudoActor;
    string ActorNow;
    int Type;
    int NumOfActs;
} Manuscript;

typedef struct act {
    string Seq;
    string Command;
    string Args;
    int Output;
    int Chrono;
} Act;

class PseudoActor {
public:
    RegistryServer _regsrvr;
    ReportServer _repsrvr;
    Register _reg;
    Manuscript _manuscript;
    vector<act> _acts;

    PyObject *regsrv_tuple();
    PyObject *empty_tuple();
    PyObject *psa_pyclass(PyObject *pmod);
    PyObject *psa_inst(PyObject *pclass,PyObject *pargs);
    PyObject *pfbase(PyObject *psainst,const char *_type);
    void pf_registerpa(PyObject *psainst);
    void pf_report_server(PyObject *psainst);
    void pf_report_server_port(PyObject *psainst);
    PseudoActor();
};

class meta {
private:
    PseudoActor _psa;

public:
    meta(string _rsrvr,int _rsrvrport);
    void execute_as_psa();
    string get_info();
    int testpy();

};