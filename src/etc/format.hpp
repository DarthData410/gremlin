#include <iostream>

using namespace std;

class format{
private:
    string _gray = "\e[0;100m";
    string _graytxt = "\033[90m";
    string _red =  "\e[41m";
    string _redtxt = "\033[31m";
    string _green = "\e[0;102m";
    string _greentxt = "\033[32m";
    string _gold = "\e[0;103m";
    string _goldtxt = "\033[93m";
    string _blue = "\e[0;104m";
    string _dblue = "\e[44m";
    string _bluetxt = "\033[34m";
    string _purple = "\e[0;105m";
    string _turq = "\e[0;106m";
    string _white = "\e[0;107m";
    string _none = "\e[0;0m";

public:
    format();
    string gray();
    string red();
    string redtxt();
    string green();
    string greentxt();
    string gold();
    string goldtxt();
    string blue();
    string bluetxt();
    string dblue();
    string purple();
    string turq();
    string white();
    string none();
    string gb(string fmt);

};