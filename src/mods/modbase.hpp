#include <iostream>
#include <sys/time.h>
#include <sys/timerfd.h>
#include <filesystem>
#include <stdio.h>
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
#include "meta/meta.hpp"

using namespace std;

class modloader{
static string logfile();
static string getlogfile();
static void logit(string &msg,Command _lcmd);

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

class mb{

public:
    string _modname="_";
    string _title="";
    string _prompt="";


};

class modank:public mb{

static void run(string &msg,bool _ri,bool _ru, bool _rt,double &_stat_pc, double &_stat_pt, string &_trun);
static void run_lil_prog(string &msg,string &msgout);

private:
    const char *_tlg;
    bool _prots[3];
    string _prots_msg;
    void parmset(Command _process);

public:
    modank();
    Command process(Command _process);
        
};

class modmeta:public mb{

public:
    modmeta();
    Command process(Command _process);
};