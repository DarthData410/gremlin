#include <iostream>
#include <vector>
#include <thread>
#include <regex>
#include <random>
#include <ranges>
#include <filesystem>
#include<netinet/in.h>
#include<errno.h>
#include<netdb.h>
#include<stdio.h>	//For standard things
#include<stdlib.h>	//malloc

#include<string.h>	//strlen

#include<netinet/ip_icmp.h>	//Provides declarations for icmp header
#include<netinet/udp.h>	//Provides declarations for udp header
#include<netinet/tcp.h>	//Provides declarations for tcp header
#include<netinet/ip.h>	//Provides declarations for ip header
#include<netinet/if_ether.h>	//For ETH_P_ALL
#include<net/ethernet.h>	//For ether_header
#include<sys/socket.h>
#include<arpa/inet.h>
#include<sys/ioctl.h>
#include<sys/time.h>
#include<sys/types.h>
#include<unistd.h>

using namespace std;


int main() {

    struct ethhdr _eth;
    struct iphdr _iph;

    _iph = iphdr();
    _iph.daddr = 171485376; // 192.168.56.10
    _iph.saddr = 1698212032; // 192.168.56.101

    sockaddr_in _sck = sockaddr_in();
    _sck.sin_addr.s_addr = _iph.daddr;

    sockaddr_in _src_sck = sockaddr_in();
    _src_sck.sin_addr.s_addr = _iph.saddr;

    //cout << inet_ntoa(_sck.sin_addr) << endl;
    //cout << inet_ntoa(_src_sck.sin_addr) << endl;
    //cout << this_thread::get_id() << endl;

    
    long l = random();
    //cout << l << endl;

    time_t ct;
    time(&ct);
    string lfn = "greml_";
    lfn += to_string(ct);
    lfn += ".greml";

    cout << lfn << endl;    

    time_t ct2;
    time(&ct2);
    lfn = "greml_";
    lfn += to_string(ct2);
    lfn += ".greml";

    cout << lfn << endl;
    cout << filesystem::is_regular_file("./greml_163741.greml");

    return 0;

}




/*
int main() {

    string parm = "! ./sniff.log";

    for(int i=1;i<parm.length();i++) {
        char _c = parm[i];
        if(_c!=32) {
            cout << _c << endl;
        }
    }

    string rcmd;
    string _parms;
    char _c='_';
    bool cget=true;

    cin >> rcmd;
    _parms = cin.get();
    while(cget) {
        
        _c = cin.get();
        if(_c=='\n') {
            cget = false;
        }
        else {
            _parms += _c;
        }
    }

    cout << " parms: " + _parms << endl;

    return 0;
}
*/