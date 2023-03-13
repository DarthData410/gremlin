#include <iostream>
#include <vector>
#define PY_SSIZE_T_CLEAN
#include <python3.10/Python.h>

using namespace std;

#define GREMPY "gremlinpy.meta.pseudoactr"
#define PSA "PseudoActor"
// py function constants:
#define pfREGPA "registerpa"
#define pfREGPAID "paid"
#define pfREGPARAT "parat"
#define pfREPSRV "report_server"
#define pfREPSRVPRT "report_server_port"
#define pfREQMANU "request_manuscript"
// manuscript calls:
#define pfMANU_ID "manuscriptID"
#define pfMANU_ACTNOW "manuscriptActorNow"
#define pfMANU_TYPE "manuscriptType"
#define pfMANU_PSAID "manuscriptPseudoActor"
#define pfMANU_NUMACT "manuscriptNumOfActs"
// manuscript act calls:
#define pfMANUACT_SEQ "manuact_seq"
#define pfMANUACT_COMM "manuact_command"
#define pfMANUACT_ARGS "manuact_args"
#define pfMANUACT_OUT "manuact_output"
#define pfMANUACT_CHRONO "manuact_chrono"

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
    string _paid;
    string _parat;
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
    string pys(PyObject *pyobj);
    int pyi(PyObject *pyobj);
    void pf_registerpa(PyObject *psainst);
    void pf_paid(PyObject *psainst);
    void pf_parat(PyObject *psainst);
    void pf_request_manuscript(PyObject *psainst);
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