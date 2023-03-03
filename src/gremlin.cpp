#include "gremlin.hpp"

gremlin::gremlin() {
    _isrunning = true;
}
    
string gremlin::title(){
    return appname()+" - "+fm.bluetxt()+_title+fm.none();
}
string gremlin::appname(){
    return fm.greentxt()+_appname+fm.none();
}
string gremlin::ver(){
    return fm.greentxt()+_ver+fm.none();
}
string gremlin::by(){
    return fm.greentxt()+_by+fm.none();
}
string gremlin::prompt(){
    return fm.goldtxt()+_prompt+fm.none();
}
string gremlin::promptend(){
    return fm.goldtxt()+_promptend+fm.none();
}
string gremlin::help(){
    _help = "\n";
    _help += "   "+fm.greentxt()+"{help}"+fm.none()+" \n";
    _help += "   [(Q/q)uit = exits app]\n";
    _help += "   [? = loads help] \n";
    _help += "   [* = set module loading mode ("+prompt()+""+fm.greentxt()+"*"+fm.none()+""+promptend()+""+fm.none()+" /<mod>)] \n";
    _help += "   "+fm.bluetxt()+"(note: module specific help, when mod loaded)"+fm.none()+"\n\n";

    return _help;
}

string gremlin::modprompt() {
    return _modprompt;
}

char gremlin::modload(string _run) {
    char ret = MLC_BASE;

    ret = stg.getmod(_run).value;
    _mod_loaded = stg.mod().name;
    _mod.setmod(stg.mod());
    
    return ret;
}

string gremlin::process(string _run) {
    string ret = "";
    string _mdp = "";
    Command cm;
    
    // generate base help and return:
    if(stg.ishelp(_run)) {
        ret = help();
        return ret;
    }
    // unload module:
    else if(stg.isun(_run)) {
        if(_mod_loaded!="") {
            ret += "  mod: "+_mod_loaded+" unloaded. \n";
        }
        _mlc = modload(CMD_START);
    }
    // prep for loading module:
    else if(stg.isload(_run) && _loadmod==false) {
        ret += "  load which mod? \n";
        _loadmod=true;
    }
    // load module
    else if(_loadmod==true) {
        _loadmod=false;
        _mlc = modload(_run);
        if(_mlc==MLC_BASE) {
            ret += "  ...no such mod: "+_run+" ... \n";
        }
        else
        {
            ret += "  mod: "+stg.mod().name+" loaded";
            _mod._loaded_mod = stg.mod();
        }
    }
    else {
        char cx[MAX_ARGS];
        cx[0]=_mlc;
        cm = stg.getcmd(_run,cx);
        cm.hasargs=1;
    }
    
    // call to process loaded module command, then prompt:
    Command cret = _mod.process(cm);
    ret += cret.msg;
    _mdp = _mod.prompt();
    _modprompt =  fm.greentxt()+_mdp+fm.none();

    ret += "\n";

    return ret;
}
    
bool gremlin::run(string runit){
    bool ret = true;

    system("clear");
    _return = header();
    _return +=  " "+fm.goldtxt()+"|"+fm.none()+"";
    
    /* TODO: Add 'echo' option:
    if(runit!=CMD_START) {
         _return += "$: {"+runit+"} \n";
    }
    else {
        _return += "\n";
    }
    */

    // test for quit:
    if(stg.isquit(runit)) {
        ret = false;
        _return += "\n  ... goodbye";
        return ret;
    }
    else{
        // continue to run:
        if(runit!=CMD_START) {
            _return += process(runit);
        }
        _return += " "+prompt();
        _return += modprompt();
        _return += promptend()+" ";\
    }

    return ret;

}
bool gremlin::iserror(){
    return _iserror;
}

string gremlin::header(){
    _header = "\n";
    _header += " "+fm.goldtxt()+"+"+fm.none()+"------"+title()+"-"+fm.goldtxt()+"+"+fm.none()+"\n";
    _header += " |      "+fm.bluetxt()+"^===============================^ "+fm.none()+"|\n";
    _header += " | "+prompt()+promptend()+"   "+fm.bluetxt()+"                                  "+fm.none()+"|\n";
    _header += " | "+appname()+"                                |\n";
    _header += " | "+ver()+"                           |\n";
    _header += " |                 "+by()+" |\n";
    _header += " "+fm.goldtxt()+"+"+fm.none()+"----------------------------------------"+fm.goldtxt()+"+"+fm.none()+"\n";
    _header += " | "+fm.bluetxt()+"[(Q/q)uit | ? | *]"+fm.none()+" \n";
    _header += " |\n";
    
    return _header;
}
string gremlin::msg(){
    return _msg;
}
string gremlin::ret(){
    return _return;
}