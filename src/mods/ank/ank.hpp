#include <iostream>
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

// packet header:
struct packet_header {
public:
	struct iphdr _iphdr;
	uint8_t _ip_protocol;
	packet_header(struct iphdr _set_iphdr);
	string protocol_str();

};

class ank{
public:
    char _c;
    string _opmsg;
    FILE *_lgf;
    struct sockaddr_in _src,_dest;
    void ProcessPacket(unsigned char* , int);
    void print_ip_header(unsigned char* , int);
    void print_tcp_packet(unsigned char * , int );
    void print_udp_packet(unsigned char * , int );
    void print_icmp_packet(unsigned char* , int );
    void print_ethernet_header(unsigned char* Buffer, int Size);
    void PrintData (unsigned char* , int);
    void ank_main();
    char _v='^';
    ank(string &msg);
};