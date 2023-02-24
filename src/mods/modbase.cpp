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
    
    return ret;
}

// ank:
modank::modank() {
    _modname = MOD_ANK;
    _title = "a network sniffer";
    _prompt = "/";
    _prompt += MOD_ANK; 
}
Command modank::process(Command _process) {
    Command ret = Command();
    ret._base = _process._base;
    char _c = '^';
    
    if(_process.value==CRUN) {
        ret.hasargs=1;
        ret.args[3]='Y';
        ret.msg = "...executed ank..->";
        //ank a = ank();
        //ret.args[1]=a.ank_main();

        string message = "^";
        string _msgout ="";
        thread ptx(run_lil_prog, ref(message), ref(_msgout));
        thread tx(run_lil, ref(message));

        string msg_back;
        cin >> msg_back;
        bool _qit = false;
        while(!_qit) {
            if(msg_back.find('q',0)==0) {
                _qit = true;
            }
            else {
                &_msgout.append("["+msg_back+"]~");
                cin >> msg_back;
            }
        }
        
        try
        {
            &message.append("q");
            ptx.join();
            tx.join();
        }
        catch(const std::exception& e)
        {
            std::cerr << e.what() << '\n';
        }
        
    }

    return ret;
}

void modank::run(string &msg) {
    
    ank a = ank(ref(msg));
    std::chrono::steady_clock::time_point tp = std::chrono::steady_clock::now() + std::chrono::seconds(5);
	std::this_thread::sleep_until(tp);
    a.ank_main();
}

void modank::run_lil(string &msg) {

    lil l = lil();
    int i = 0;
    
    while(l.run(ref(msg))) {
        i++;
    }
    system("clear");
    cout << "  ended run_lil..." << endl;

}

void modank::run_lil_prog(string &msg,string &msgout) {
    format f = format();
    string _px = "";
    string _out = "";
    int i = 0;
    
    mutex _m;
    deque<string> _q;

    while(msg!="^q") {
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

lil::lil() {

}
bool lil::run(string &msg) {
    bool ret = false;

    if(msg!="^q") {
        ret = true;
    }
    return ret;
}

