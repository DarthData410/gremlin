#include <iostream>
#include <python3.10/Python.h>
#include "mods/modbase.hpp"

class gremlin{
private:
    format fm = format();
    settings stg = settings();
    bool _isrunning = false;
    bool _iserror = false;
    string _title = "*nix security framework";
    string _appname = "gremlin";
    string _ver = "v1.0 (feb23)";
    string _by = "PyFryLabs -> @pyfryday";
    string _prompt = "$";
    string _promptend = ">";

    string _header;
    string _help;
    string help();
    string _return;
    string _process; 
    string process(string _run); // internally process for return
    char modload(string _run);
    string _modprompt = "";
    string modprompt();
    
    // mods:
    char _mlc='*';
    string _mod_loaded="";
    modloader _mod=modloader();
    // end mods:

    bool _loadmod=false;
    string _msg;

public:
    gremlin();
    
    string title();
    string appname();
    string ver();
    string by();
    string prompt();
    string promptend();
    
    bool run(string runit);
    bool iserror();

    string header();
    string msg();
    string ret();

};