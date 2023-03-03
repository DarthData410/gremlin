#include <iostream>
#include <filesystem>
#include <vector>
#include <thread>
#include <random>
#include<netinet/in.h>
#include<errno.h>
#include<netdb.h>
#include<stdio.h>	
#include<stdlib.h>	//malloc
#include<string.h>	//strlen

#include<netinet/ip_icmp.h>	// icmp header
#include<netinet/udp.h>	// udp header
#include<netinet/tcp.h>	// tcp header
#include<netinet/ip.h>	// ip header
#include<netinet/if_ether.h> // ETH_P_ALL
#include<net/ethernet.h>	// ether_header

#include<sys/socket.h>
#include<arpa/inet.h>
#include<sys/ioctl.h>
#include<sys/time.h>
#include<sys/types.h>
#include<unistd.h>

using namespace std;

typedef struct netaddy {
public:
    uint32_t base;
    string base_str;
    char * converted;
} NetAddress;

typedef struct tcpport {
public:
    uint16_t base;
    string converted;
} TcpPort;

// packet:
class pck {
public:
    string _key;
    unsigned char* _buffer;
    int _size;
    struct ethhdr _eth;
    struct iphdr _iph;
    bool has_tcp=false;
    struct tcphdr _tcp;
    bool has_udp=false;
    struct udphdr _udp;
    bool has_icmp=false;
    struct icmphdr _icmp;
};

class ptcp:public pck{
public:
    ptcp(struct ethhdr set_eth,struct iphdr set_iph,struct tcphdr set_tcp);
    
};
class pudp:public pck{
public:
    pudp(struct ethhdr set_eth,struct iphdr set_iph,struct udphdr set_udp);
    
};
class picmp:public pck{
public:
    picmp(struct ethhdr set_eth,struct iphdr set_iph,struct icmphdr set_icmp);
    
};

class ank{
private:
    double _packets_captured=0.0;
    double _packets_traced=0.0;

public:
    bool _run_icmp=false;
    bool _run_tcp=false;
    bool _run_udp=false;
    string _trunid;
    vector<picmp> icmp_packets;
    vector<pudp> udp_packets;
    vector<ptcp> tcp_packets;
    char _c;
    string _opmsg;
    FILE *_lgf;
    struct sockaddr_in _src,_dest;
    void ProcessPacket(unsigned char* , int);
    void createdir(string _runid,string _dir);
    void writelog();
    void writelog_tcp(string _rid);
    void writelog_udp(string _rid);
    void writeindex(FILE *_if, string _k, string _rv,string _cv);
    NetAddress convert_net(NetAddress na);
    string runid();

    void print_icmp_packet(unsigned char* , int );
    
    void genpayload(FILE *_fpd,unsigned char* , int);
    void ank_main(string &msg,bool _ricmp,bool _rudp,bool _rtcp,double &_spc, double &_spt, string &_trun);
    
    ank();
};