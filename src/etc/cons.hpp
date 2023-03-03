#include <iostream>

// Commands:
#define CMD_START "_"

// Char Commands:
#define CNULL '^'
#define CTERM ';'
#define CHELP '?'
#define CLOAD '*'
#define CQUIT 'q'
#define CSTART '_'
#define CUNLOAD 'u'
#define CRUN '!'
#define CPARMS 'p'
#define CANCHOR '~'
#define CPS '-'

// ModLoadChars:
#define MLC_BASE '*'
#define MLC_ANK '1'
#define GREML "./greml/"

// Mod Args:
#define MAX_ARGS 4
#define MAX_PARM 4

// Ank:
#define MOD_ANK "ank"

using namespace std;

typedef struct command{
    string _base;
    int hasargs;
    char args[MAX_ARGS];
    char value;
    string parm[MAX_PARM];
    string msg;
}Command;

typedef struct module{
    string _base;
    string name;
    string title;
    string prompt;
    char value;
}Module;