#include <iostream>
#include <thread>
#include <future>
#include <deque>
#include <mutex>
#include <functional>
#include <exception>
#include <chrono>
#include <python3.10/Python.h>
#include "../../src/etc/format.hpp"
#include "../../src/etc/settings.hpp"
#include "ank/ank.hpp"

using namespace std;

class modloader{
public:
    Module _loaded_mod=Module();
    void setmod(Module _m);
    string _modname="_";
    string _title="";
    string _process="";
    string _prompt="";
    string _ret="";
    string _msg="";
    bool _iserror;

    modloader();
    string prompt();
    string ret();
    string msg();
    bool iserror();
    Command process(Command _process);

};

class lil{
public:
    string _opmsg;
    lil();
    bool run(string &msg);
};

class mb{
public:
    string _modname="_";
    string _title="";
    string _prompt="";
};

class modank:public mb{

static void run(string &msg);
static void run2(string &msg);
static void run_lil(string &msg);
static void run_lil_prog(string &msg,string &msgout);

public:
    modank();
    Command process(Command _process);
        
};