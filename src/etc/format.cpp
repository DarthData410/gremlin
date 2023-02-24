#include "format.hpp"

format::format() { }

string format::gray() {
    return _gray;
}
string format::red() {
    return _red;
}
string format::redtxt() {
    return _redtxt;
}
string format::green() {
    return _green;
}
string format::greentxt() {
    return _greentxt;
}
string format::gold() {
    return _gold;
}
string format::goldtxt() {
    return _goldtxt;
}
string format::blue() {
    return _blue;
}
string format::bluetxt() {
    return _bluetxt;
}
string format::dblue() {
    return _dblue;
}
string format::purple() {
    return _purple;
}
string format::turq() {
    return _turq;
}
string format::white() {
    return _white;
}
string format::none() {
    return _none;
}
string format::gb(string fmt) {
    return gray()+fmt+none();
}