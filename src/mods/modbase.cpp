#include "modbase.hpp"

// base:
modloader::modloader() {
    _prompt = "";
}
string modloader::prompt() {
    return _loaded_mod.prompt;
}
string modloader::ret() {
    return _ret;
}
string modloader::msg() {
    return _msg;
}
bool modloader::iserror() {
    return _iserror;
}
void modloader::setmod(Module _m) {
    _loaded_mod = _m;
    _prompt = _loaded_mod.prompt;
    _title = _loaded_mod.title;
    _modname = _loaded_mod.name;
}
Command modloader::process(Command _process) {
    Command ret = Command();
    modank a = modank();
    
    switch(_loaded_mod.value) {
        case MLC_ANK :
            ret = a.process(_process);
            break;
        default :
            ret.args[0]=CNULL;
            ret.args[3]=CNULL;
            ret.msg = "";
            break;
    }

    modloader::logit(ret.msg,ret);
    
    return ret;
}
string modloader::logfile() {
    string ret = "";
    
    time_t ct;
    time(&ct);
    ret = "gl";
    ret += to_string(ct);
    ret += ".greml";

    return ret;
}
string modloader::getlogfile() {
    string ret = "";

    // command logger dir:
    if(!filesystem::is_directory(GREML)) { 
        filesystem::path _gp = filesystem::path();
	    _gp.append(GREML);
	    filesystem::create_directories(_gp);
    }

    ret = GREML+modloader::logfile();
    while(filesystem::is_regular_file(ret)) {
        ret = GREML+modloader::logfile();
    }

    return ret;
}
void modloader::logit(string &msg,Command _lcmd) {

    if(_lcmd._base!="" && _lcmd.msg!="")
    {
        FILE *lf;
        string _lfs = modloader::getlogfile();
        lf = fopen(_lfs.c_str(),"w");
        fprintf(lf,"gremlin log for command: %s \n",_lcmd._base.c_str()); 
        fprintf(lf,"-------------------------- \n");
        fprintf(lf,"\n[+]-> this file: %s",_lfs.c_str());
        fprintf(lf,"[+]-> msg: \n");
        fprintf(lf,"  %s",_lcmd.msg.c_str());
        fclose(lf);
    }
}

// ank:
modank::modank() {
    _modname = MOD_ANK;
    _title = "a network sniffer";
    _prompt = "/";
    _prompt += MOD_ANK; 
}
void modank::parmset(Command _process) {

    if(_process.parm[0]=="TCP"||_process.parm[1]=="TCP"||_process.parm[2]=="TCP"||_process.parm[3]=="TCP") 
    { _prots[0]=true; _prots_msg += "[+TCP]"; }
    
    if(_process.parm[0]=="UDP"||_process.parm[1]=="UDP"||_process.parm[2]=="UDP"||_process.parm[3]=="UDP") 
    { _prots[1]=true; _prots_msg += "[+UDP]"; }

    if(_process.parm[0]=="ICMP"||_process.parm[1]=="ICMP"||_process.parm[2]=="ICMP"||_process.parm[3]=="ICMP") 
    { _prots[2]=true; _prots_msg += "[+ICMP]"; }

}
Command modank::process(Command _process) {
    format f = format();
    Command ret = Command();
    ret._base = _process._base;
    char _c = '^';
    const char *_tar_logfile;

    ret.msg = "\n";
    
    if(_process.value==CRUN && _process.args[2]==CPARMS) {    
        ret.msg += "   [+] - executed ank with args -> ";
        parmset(_process);
        ret.msg += ""+_prots_msg+" \n";
    }
    else if(_process.value==CRUN) {
        // default tcp only:
        ret.msg = "   [+] - executed ank with default [TCP] trace only \n";
        _prots[0] = true;
        _prots[1] = false;
        _prots[2] = false;
    }
    
    if(_process.value==CRUN) {
    
        string message = "^";
        string _msgout ="";
        string _trun="";
        double _spc=0,_spt=0;
        thread ptx(run_lil_prog, ref(message), ref(_msgout));
        &_msgout.append("Trace on for "+_prots_msg);
        thread tx(run, ref(message),_prots[2],_prots[1],_prots[0],ref(_spc),ref(_spt),ref(_trun));

        &_msgout.append("::[Processing with:"+_prots_msg+"]");

        string msg_back;
        cin >> msg_back;
        bool _qit = false;
        while(!_qit) {
            if(msg_back.find('q',0)==0) {
                _qit = true;
            }
            else {
                &_msgout.append("::["+msg_back+"]");
                cin >> msg_back;
            }
        }
        
        try
        {
            &message.append("q");
            &_msgout.append("::[QUITING TRACE]");
            tx.join();
            &message.append("q");
            ptx.join();
            system("clear");
            ret.msg += "   [+] - captured packets -> ";
            ret.msg += to_string(_spc);
            ret.msg += " \n";
            ret.msg += "   [+] - traced packets -> ";
            ret.msg += to_string(_spt);
            ret.msg += " \n";

            double _percent = (_spt/_spc);
            _percent = _percent * 100;
            ret.msg += "   [+] - traced packets % -> ";
            ret.msg += to_string(_percent);
            ret.msg += "% \n";

            ret.msg += "   [+] - trace run logs located @ -> ";
            ret.msg += _trun;
            ret.msg += " \n";
        }
        catch(const std::exception& e)
        {
            std::cerr << e.what() << '\n';
        }
        
    }

    return ret;
}

void modank::run(string &msg,bool _ri,bool _ru, bool _rt,double &_stat_pc, double &_stat_pt, string &_trun) {
    
    ank a = ank();
    a.ank_main(ref(msg),_ri,_ru,_rt,ref(_stat_pc),ref(_stat_pt),ref(_trun));
    // allow for file hanlde release:
    std::chrono::steady_clock::time_point tp = std::chrono::steady_clock::now() + std::chrono::milliseconds(150);
	std::this_thread::sleep_until(tp);
}


void modank::run_lil_prog(string &msg,string &msgout) {
    format f = format();
    string _px = "";
    string _out = "";
    int i = 0;
    
    mutex _m;
    deque<string> _q;

    while(msg!="^qq") {
        if(i>14) { i=0; }
        system("clear");
        _out = "";

        _px = "[";
        switch(i) {
            case 0 : _px += ""+f.goldtxt()+"*"+f.none()+"----"; break;
            case 1 : _px += "-"+f.goldtxt()+"*"+f.none()+"---"; break;
            case 2 : _px += "--"+f.goldtxt()+"*"+f.none()+"--"; break;
            case 3 : _px += "---"+f.goldtxt()+"*"+f.none()+"-"; break;
            case 4 : _px += "----"+f.goldtxt()+"*"+f.none()+""; break;
            case 5 : _px += ""+f.goldtxt()+"*"+f.none()+"---"+f.goldtxt()+"*"+f.none()+""; break;
            case 6 : _px += "-"+f.goldtxt()+"*"+f.none()+"-"+f.goldtxt()+"*"+f.none()+"-"; break;
            case 7 : _px += "--"+f.goldtxt()+"*"+f.none()+"--"; break;
            case 8 : _px += "---"+f.goldtxt()+"*"+f.none()+"-"; break;
            case 9 : _px += "----"+f.goldtxt()+"*"+f.none()+""; break;
            case 10 : _px += "---"+f.goldtxt()+"*"+f.none()+"-"; break;
            case 11 : _px += "--"+f.goldtxt()+"*"+f.none()+"--"; break;
            case 12 : _px += "-"+f.goldtxt()+"*"+f.none()+"---"; break;
            case 13 : _px += ""+f.goldtxt()+"*"+f.none()+"----"; break;
            case 14 : _px += f.bluetxt()+"-----"+f.none(); break;
            default: _px += "*"; break;
        }
        _px += "]";

        _out += "\n";
        _out += f.bluetxt()+"  gremlin - task executing"+f.none() + "\n";
        _out += "  |  press the "+f.greentxt()+"q"+f.none()+" key & "+f.greentxt()+"enter"+f.none()+" to quit process. \n";
        _out += "  |\n";
        _out += "  |-->"+_px+"\n";
        _out += "  "+f.goldtxt()+"+"+f.none()+"\n";
        
        if(msgout!="") {
            _out += "  |->"+msgout+"\n";
        }
        
        cout << _out;
        i++;
        std::chrono::steady_clock::time_point tp = std::chrono::steady_clock::now() + std::chrono::milliseconds(800);
	    std::this_thread::sleep_until(tp);
    }

}


