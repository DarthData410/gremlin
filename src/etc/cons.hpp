#include <iostream>

// Commands:
#define CMD_START "_"

// Char Commands:
#define CNULL '^'
#define CHELP '?'
#define CLOAD '*'
#define CQUIT 'q'
#define CSTART '_'
#define CUNLOAD 'u'
#define CRUN '!'

// ModLoadChars:
#define MLC_BASE '*'
#define MLC_ANK '1'

// Mod Args:
#define MAX_ARGS 4

// Ank:
#define MOD_ANK "ank"

using namespace std;

typedef struct command{
    string _base;
    int hasargs;
    char args[MAX_ARGS];
    char value;
    string msg;
}Command;

typedef struct module{
    string _base;
    string name;
    string title;
    string prompt;
    char value;
}Module;