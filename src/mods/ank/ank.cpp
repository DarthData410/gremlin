#include "ank.hpp"

packet_header::packet_header(struct iphdr _set_iphdr) {
	_iphdr = _set_iphdr;
	_ip_protocol = _iphdr.protocol;
}

string packet_header::protocol_str() {
	string ret = "";

	switch (_ip_protocol) {
		case 1 : ret = "ICMP"; break;
		case 2 : ret = "IGMP"; break;
		case 6 : ret = "TCP"; break;
		case 17 : ret = "UDP"; break;
		default: ret = "*other"; break;
	}

	return ret;
}

// packet
struct packet {
public:
	string _type;
};



ank::ank(string &msg) {
    _opmsg = msg;
}

void ank::ank_main()
{
	int saddr_size , data_size;
	struct sockaddr saddr;
		
	unsigned char *buffer = (unsigned char *) malloc(65536); //Its Big!
	
	_lgf=fopen("sniff.log","w");
	if(_lgf==NULL) 
	{
		printf("Unable to create log file.");
	}
	printf("Starting...\n");
	
	int sock_raw = socket(AF_PACKET , SOCK_RAW , htons(ETH_P_ALL)) ;
	//setsockopt(sock_raw , SOL_SOCKET , SO_BINDTODEVICE , "eth0" , strlen("eth0")+ 1 );
	
	if(sock_raw < 0)
	{
		//Print the error with proper message
		perror("Socket Error");
		
	}
	while(_opmsg!="^q")
	{
		cout << _opmsg;
        saddr_size = sizeof saddr;
		//Receive a packet
		data_size = recvfrom(sock_raw , buffer , 65536 , 0 , &saddr , (socklen_t*)&saddr_size);
		if(data_size <0 )
		{
			printf("Recvfrom error , failed to get packets\n");
			
		}
		//Now process the packet
		ProcessPacket(buffer , data_size);
	}
	close(sock_raw);
	printf("Finished");
	//return 0;
}

/*
int main() {

    cout << "...starting sniff..." << endl;
    cout << " [end Q|q to quit] " << endl;

    thread t(runit());
    bool run=true;
    string feedback="";
    while(run) {

        cout << "\n";
        cout << " $*> ";\
        cin >> feedback;
        if(feedback=="Q"||feedback=="q") {
            run = false;
        }
    }

    if(t.joinable()) {
        t.join();
        exit(0);
    }

    return 0;
} */

void ank::ProcessPacket(unsigned char* buffer, int size)
{
	//Get the IP Header part of this packet , excluding the ethernet header
	struct iphdr *iph = (struct iphdr*)(buffer + sizeof(struct ethhdr));

	struct packet_header pckhdr = packet_header(*iph);
	/*
	system("clear");
	cout << "[Packet Header Protocol: " << pckhdr.protocol_str() << "]" << endl;
	cout << "..: " << pckhdr._iphdr.protocol << endl;
	//cout << " .prot     : " << pckhdr._ip_protocol << endl;
	cout << " .ver      : " << pckhdr._iphdr.version << endl; 
	cout << " .ttl      : " << pckhdr._iphdr.ttl << endl;
	cout << " .id       : " << pckhdr._iphdr.id << endl;
	cout << " .check    : " << pckhdr._iphdr.check << endl;
	cout << " .daddr    : " << pckhdr._iphdr.daddr << endl;
	cout << " .frag_off : " << pckhdr._iphdr.frag_off << endl;
	cout << " .ihl      : " << pckhdr._iphdr.ihl << endl;
	cout << " .saddr    : " << pckhdr._iphdr.saddr << endl;
	cout << " .tos      : " << pckhdr._iphdr.tos << endl;
	cout << " .tos_len  : " << pckhdr._iphdr.tot_len << endl;
	cout << "... end packet_ip_header ..." << endl;
	*/

	//++total;
	switch (iph->protocol) //Check the Protocol and do accordingly...
	{
		case 1:  //ICMP Protocol
			//++icmp;
			print_icmp_packet( buffer , size);
			break;
		
		case 2:  //IGMP Protocol
		//	++igmp;
			break;
		
		case 6:  //TCP Protocol
		//	++tcp;
			print_tcp_packet(buffer , size);
			break;
		
		case 17: //UDP Protocol
		//	++udp;
			print_udp_packet(buffer , size);
			break;
		
		default: //Some Other Protocol like ARP etc.
		//	++others;
			break;
	}
	//printf("TCP : %d   UDP : %d   ICMP : %d   IGMP : %d   Others : %d   Total : %d\r", tcp , udp , icmp , igmp , others , total);
}

void ank::print_ethernet_header(unsigned char* Buffer, int Size)
{
	struct ethhdr *eth = (struct ethhdr *)Buffer;

	cout << " {ethernet header} " << endl;
	cout << " .proto  : " << eth->h_proto << endl;
	cout << " .source : " << eth->h_source << endl;
	cout << " .dest   : " << eth->h_dest << endl;
	cout << " ... end ethernet header ..." << endl;
	
	fprintf(_lgf , "\n");
	fprintf(_lgf , "Ethernet Header\n");
	fprintf(_lgf , "   |-Destination Address : %.2X-%.2X-%.2X-%.2X-%.2X-%.2X \n", eth->h_dest[0] , eth->h_dest[1] , eth->h_dest[2] , eth->h_dest[3] , eth->h_dest[4] , eth->h_dest[5] );
	fprintf(_lgf , "   |-Source Address      : %.2X-%.2X-%.2X-%.2X-%.2X-%.2X \n", eth->h_source[0] , eth->h_source[1] , eth->h_source[2] , eth->h_source[3] , eth->h_source[4] , eth->h_source[5] );
	fprintf(_lgf , "   |-Protocol            : %u \n",(unsigned short)eth->h_proto);
}

void ank::print_ip_header(unsigned char* Buffer, int Size)
{
	print_ethernet_header(Buffer , Size);
  
	unsigned short iphdrlen;
		
	struct iphdr *iph = (struct iphdr *)(Buffer  + sizeof(struct ethhdr) );
	iphdrlen =iph->ihl*4;
	
	memset(&_src, 0, sizeof(_src));
	_src.sin_addr.s_addr = iph->saddr;
	
	memset(&_dest, 0, sizeof(_dest));
	_dest.sin_addr.s_addr = iph->daddr;
	
	fprintf(_lgf , "\n");
	fprintf(_lgf , "IP Header\n");
	fprintf(_lgf , "   |-IP Version        : %d\n",(unsigned int)iph->version);
	fprintf(_lgf , "   |-IP Header Length  : %d DWORDS or %d Bytes\n",(unsigned int)iph->ihl,((unsigned int)(iph->ihl))*4);
	fprintf(_lgf , "   |-Type Of Service   : %d\n",(unsigned int)iph->tos);
	fprintf(_lgf , "   |-IP Total Length   : %d  Bytes(Size of Packet)\n",ntohs(iph->tot_len));
	fprintf(_lgf , "   |-Identification    : %d\n",ntohs(iph->id));
	//fprintf(_lgf , "   |-Reserved ZERO Field   : %d\n",(unsigned int)iphdr->ip_reserved_zero);
	//fprintf(_lgf , "   |-Dont Fragment Field   : %d\n",(unsigned int)iphdr->ip_dont_fragment);
	//fprintf(_lgf , "   |-More Fragment Field   : %d\n",(unsigned int)iphdr->ip_more_fragment);
	fprintf(_lgf , "   |-TTL      : %d\n",(unsigned int)iph->ttl);
	fprintf(_lgf , "   |-Protocol : %d\n",(unsigned int)iph->protocol);
	fprintf(_lgf , "   |-Checksum : %d\n",ntohs(iph->check));
	fprintf(_lgf , "   |-Source IP        : %s\n",inet_ntoa(_src.sin_addr));
	fprintf(_lgf , "   |-Destination IP   : %s\n",inet_ntoa(_dest.sin_addr));
}

void ank::print_tcp_packet(unsigned char* Buffer, int Size)
{
	unsigned short iphdrlen;
	
	struct iphdr *iph = (struct iphdr *)( Buffer  + sizeof(struct ethhdr) );
	iphdrlen = iph->ihl*4;
	
	struct tcphdr *tcph=(struct tcphdr*)(Buffer + iphdrlen + sizeof(struct ethhdr));
			
	int header_size =  sizeof(struct ethhdr) + iphdrlen + tcph->doff*4;
	
	fprintf(_lgf , "\n\n***********************TCP Packet*************************\n");	
		
	print_ip_header(Buffer,Size);
		
	fprintf(_lgf , "\n");
	fprintf(_lgf , "TCP Header\n");
	fprintf(_lgf , "   |-Source Port      : %u\n",ntohs(tcph->source));
	fprintf(_lgf , "   |-Destination Port : %u\n",ntohs(tcph->dest));
	fprintf(_lgf , "   |-Sequence Number    : %u\n",ntohl(tcph->seq));
	fprintf(_lgf , "   |-Acknowledge Number : %u\n",ntohl(tcph->ack_seq));
	fprintf(_lgf , "   |-Header Length      : %d DWORDS or %d BYTES\n" ,(unsigned int)tcph->doff,(unsigned int)tcph->doff*4);
	//fprintf(_lgf , "   |-CWR Flag : %d\n",(unsigned int)tcph->cwr);
	//fprintf(_lgf , "   |-ECN Flag : %d\n",(unsigned int)tcph->ece);
	fprintf(_lgf , "   |-Urgent Flag          : %d\n",(unsigned int)tcph->urg);
	fprintf(_lgf , "   |-Acknowledgement Flag : %d\n",(unsigned int)tcph->ack);
	fprintf(_lgf , "   |-Push Flag            : %d\n",(unsigned int)tcph->psh);
	fprintf(_lgf , "   |-Reset Flag           : %d\n",(unsigned int)tcph->rst);
	fprintf(_lgf , "   |-Synchronise Flag     : %d\n",(unsigned int)tcph->syn);
	fprintf(_lgf , "   |-Finish Flag          : %d\n",(unsigned int)tcph->fin);
	fprintf(_lgf , "   |-Window         : %d\n",ntohs(tcph->window));
	fprintf(_lgf , "   |-Checksum       : %d\n",ntohs(tcph->check));
	fprintf(_lgf , "   |-Urgent Pointer : %d\n",tcph->urg_ptr);
	fprintf(_lgf , "\n");
	fprintf(_lgf , "                        DATA Dump                         ");
	fprintf(_lgf , "\n");
		
	fprintf(_lgf , "IP Header\n");
	PrintData(Buffer,iphdrlen);
		
	fprintf(_lgf , "TCP Header\n");
	PrintData(Buffer+iphdrlen,tcph->doff*4);
		
	fprintf(_lgf , "Data Payload\n");	
	PrintData(Buffer + header_size , Size - header_size );
						
	fprintf(_lgf , "\n###########################################################");
}

void ank::print_udp_packet(unsigned char *Buffer , int Size)
{
	
	unsigned short iphdrlen;
	
	struct iphdr *iph = (struct iphdr *)(Buffer +  sizeof(struct ethhdr));
	iphdrlen = iph->ihl*4;
	
	struct udphdr *udph = (struct udphdr*)(Buffer + iphdrlen  + sizeof(struct ethhdr));
	
	int header_size =  sizeof(struct ethhdr) + iphdrlen + sizeof udph;
	
	fprintf(_lgf , "\n\n***********************UDP Packet*************************\n");
	
	print_ip_header(Buffer,Size);			
	
	fprintf(_lgf , "\nUDP Header\n");
	fprintf(_lgf , "   |-Source Port      : %d\n" , ntohs(udph->source));
	fprintf(_lgf , "   |-Destination Port : %d\n" , ntohs(udph->dest));
	fprintf(_lgf , "   |-UDP Length       : %d\n" , ntohs(udph->len));
	fprintf(_lgf , "   |-UDP Checksum     : %d\n" , ntohs(udph->check));
	
	fprintf(_lgf , "\n");
	fprintf(_lgf , "IP Header\n");
	PrintData(Buffer , iphdrlen);
		
	fprintf(_lgf , "UDP Header\n");
	PrintData(Buffer+iphdrlen , sizeof udph);
		
	fprintf(_lgf , "Data Payload\n");	
	
	//Move the pointer ahead and reduce the size of string
	PrintData(Buffer + header_size , Size - header_size);
	
	fprintf(_lgf , "\n###########################################################");
}

void ank::print_icmp_packet(unsigned char* Buffer , int Size)
{
	unsigned short iphdrlen;
	
	struct iphdr *iph = (struct iphdr *)(Buffer  + sizeof(struct ethhdr));
	iphdrlen = iph->ihl * 4;
	
	struct icmphdr *icmph = (struct icmphdr *)(Buffer + iphdrlen  + sizeof(struct ethhdr));
	
	int header_size =  sizeof(struct ethhdr) + iphdrlen + sizeof icmph;
	
	fprintf(_lgf , "\n\n***********************ICMP Packet*************************\n");	
	
	print_ip_header(Buffer , Size);
			
	fprintf(_lgf , "\n");
		
	fprintf(_lgf , "ICMP Header\n");
	fprintf(_lgf , "   |-Type : %d",(unsigned int)(icmph->type));
			
	if((unsigned int)(icmph->type) == 11)
	{
		fprintf(_lgf , "  (TTL Expired)\n");
	}
	else if((unsigned int)(icmph->type) == ICMP_ECHOREPLY)
	{
		fprintf(_lgf , "  (ICMP Echo Reply)\n");
	}
	
	fprintf(_lgf , "   |-Code : %d\n",(unsigned int)(icmph->code));
	fprintf(_lgf , "   |-Checksum : %d\n",ntohs(icmph->checksum));
	//fprintf(_lgf , "   |-ID       : %d\n",ntohs(icmph->id));
	//fprintf(_lgf , "   |-Sequence : %d\n",ntohs(icmph->sequence));
	fprintf(_lgf , "\n");

	fprintf(_lgf , "IP Header\n");
	PrintData(Buffer,iphdrlen);
		
	fprintf(_lgf , "UDP Header\n");
	PrintData(Buffer + iphdrlen , sizeof icmph);
		
	fprintf(_lgf , "Data Payload\n");	
	
	//Move the pointer ahead and reduce the size of string
	PrintData(Buffer + header_size , (Size - header_size) );
	
	fprintf(_lgf , "\n###########################################################");
}

void ank::PrintData (unsigned char* data , int Size)
{
	int i , j;
	for(i=0 ; i < Size ; i++)
	{
		if( i!=0 && i%16==0)   //if one line of hex printing is complete...
		{
			fprintf(_lgf , "         ");
			for(j=i-16 ; j<i ; j++)
			{
				if(data[j]>=32 && data[j]<=128)
					fprintf(_lgf , "%c",(unsigned char)data[j]); //if its a number or alphabet
				
				else fprintf(_lgf , "."); //otherwise print a dot
			}
			fprintf(_lgf , "\n");
		} 
		
		if(i%16==0) fprintf(_lgf , "   ");
			fprintf(_lgf , " %02X",(unsigned int)data[i]);
				
		if( i==Size-1)  //print the last spaces
		{
			for(j=0;j<15-i%16;j++) 
			{
			  fprintf(_lgf , "   "); //extra spaces
			}
			
			fprintf(_lgf , "         ");
			
			for(j=i-i%16 ; j<=i ; j++)
			{
				if(data[j]>=32 && data[j]<=128) 
				{
				  fprintf(_lgf , "%c",(unsigned char)data[j]);
				}
				else 
				{
				  fprintf(_lgf , ".");
				}
			}
			
			fprintf(_lgf ,  "\n" );
		}
	}
}