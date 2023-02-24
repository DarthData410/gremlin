#include <iostream>
#include "cons.hpp"

class settings{
private:
    Command _cmd;
    Module _mod;
    char nullargs[MAX_ARGS];

public:
    settings();
    bool isquit(string _r);
    bool isun(string _r);
    bool ishelp(string _r);
    bool isload(string _r);
    Command getcmd(string _r,char args[MAX_ARGS]);
    Command cmd();
    Module getmod(string _r);
    Module mod();
};