#include "settings.hpp"

settings::settings() {
    nullargs[0] = CNULL;
}

bool settings::isquit(string _r) {
    bool ret = false;

    if(getcmd(_r,nullargs).value==CQUIT) {
        ret = true;
    }

    return ret;
}
bool settings::isun(string _r) {
    bool ret = false;

    if(getcmd(_r,nullargs).value==CUNLOAD) {
        ret = true;
    }

    return ret;
}
bool settings::ishelp(string _r) {
    bool ret = false;

    if(getcmd(_r,nullargs).value==CHELP) {
        ret = true;
    }

    return ret;
}
bool settings::isload(string _r) {
    bool ret = false;

    if(getcmd(_r,nullargs).value==CLOAD) {
        ret = true;
    }

    return ret;
}
Command settings::getcmd(string _r,char args[]) {
    //char ret = CNULL;
    Command ret = Command();
    ret._base = _r;

    if(args[0]!=CNULL) { ret.hasargs=1; } else { ret.hasargs=0; }
    
    if(ret._base.find('Q',0)==0 || ret._base.find('q',0)==0) {
        ret.value = CQUIT;
    }
    else if(ret._base.find('U',0)==0 || ret._base.find('u',0)==0) {
        ret.value = CUNLOAD;
    }
    else if(ret._base.find('?',0)==0 || ret._base=="Help" || ret._base=="HELP") {
        ret.value = CHELP;
        // need to check for loaded mod, and load its help...
    }
    else if(ret._base.find(CLOAD,0)==0) {
        ret.value = CLOAD;
    }
    else {
        if(args[0]!=CNULL && (ret._base.find(CRUN,0)==0)) {
            ret.value = CRUN;
            bool sp=false;
            int i=0;
            
            if(ret._base.length()>2) {
                for(char c : ret._base) {
                    
                    if(sp && c!=CNULL) {
                        if(c!=CTERM) {
                            ret.parm[i] += c;
                        }
                    }
                    else if(sp && c==CNULL) {
                        sp = false;
                        i++;
                    }

                    if(c==CPS) {
                        sp = true;
                    }
                }

                ret.args[2] = CPARMS;
            }
            else {
                ret.args[2] = CNULL;
            }

        }
    }

    _cmd = ret;
    return ret;
}
Command settings::cmd() {
    return _cmd;
}

Module settings::getmod(string _r) {
    Module ret = Module();
    ret._base = _r;
    
    if(ret._base=="ank~;"||ret._base=="/ank~;"||ret._base=="ANK~;"||ret._base=="/ANK~;") { ret.value=MLC_ANK; ret.name="ank"; ret.title="a network sniffer"; ret.prompt="/ank"; }
    else {
        ret.value=MLC_BASE; ret.name=""; ret.title=""; ret.prompt="";
    }

    _mod = ret;
    return ret;
}
Module settings::mod() {
    return _mod;
}
