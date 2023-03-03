#include "ank.hpp"


ptcp::ptcp(struct ethhdr set_eth,struct iphdr set_iph,struct tcphdr set_tcp) {
	// has tcp
	has_tcp = true;
	this->_eth = set_eth;
	this->_iph = set_iph;
	this->_tcp = set_tcp;
}
pudp::pudp(struct ethhdr set_eth,struct iphdr set_iph,struct udphdr set_udp){
	// has udp
	has_udp = true;
	this->_eth = set_eth;
	this->_iph = set_iph;
	this->_udp = set_udp;
}
picmp::picmp(struct ethhdr set_eth,struct iphdr set_iph,struct icmphdr set_icmp){
	// has icmp
	has_icmp = true;
	this->_eth = set_eth;
	this->_iph = set_iph;
	this->_icmp = set_icmp;
}


ank::ank() {
    
}

void ank::ank_main(string &msg,bool _ricmp,bool _rudp,bool _rtcp,double &_spc, double &_spt, string &_trun)
{
	int saddr_size , data_size;
	struct sockaddr saddr;

	// set trace protocols:
	_run_icmp = _ricmp;
	_run_udp = _rudp;
	_run_tcp = _rtcp;
		
	unsigned char *buffer = (unsigned char *) malloc(65536);
	int sock_raw = socket(AF_PACKET , SOCK_RAW , htons(ETH_P_ALL)) ;
	if(sock_raw < 0)
	{ perror("Error binding to socket. Might be a rights issue. Run ./gremlin as sudo."); }
	
	try
	{
		while(msg!="^q")
		{
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

	}
	catch(const std::exception& e)
	{
		std::cerr << e.what() << '~' << 'P' << 'x' << '\n';
	}

	writelog();
	close(sock_raw);

	// report stats to main thread variables:
	_spc = _packets_captured;
	_spt = _packets_traced;
	_trun = _trunid;
	
}

string ank::runid() {
	string ret = "";
	
	time_t _ct;
	time(&_ct);
	ret += "./gremr_";
	ret += to_string(_ct);

	return ret;
}

void ank::writelog() {

	string _runid = runid();
	while(filesystem::is_directory(_runid))
	{ 
		// wait 200 milliseconds:
		chrono::steady_clock::time_point tp = chrono::steady_clock::now() + chrono::milliseconds(200);
	    this_thread::sleep_until(tp);
		_runid = runid();
	}

	_trunid = _runid;

	if(_run_tcp) {
		writelog_tcp(_runid);
	}

	if(_run_udp) {
		writelog_udp(_runid);
	}

}

void ank::createdir(string _runid, string _dir) {
	
	filesystem::path _runp = filesystem::path();
	_runp.append(_runid+_dir);
	filesystem::create_directories(_runp);
}

void ank::writelog_tcp(string _rid) {

	FILE *tcpl,*ethl,*tcph;
	
	vector<NetAddress> ipindex;
	vector<NetAddress> usrcs;
	vector<NetAddress> udests;
	vector<TcpPort> utcpports;
	vector<unsigned int> tchecks;
	
	bool hasip=false;
	bool hassrc=false;
	bool hasdest=false;
	bool hastcpport=false;
	bool haschecks=false;

	string _runid = _rid;

	try
	{
		createdir(_runid,"");
		createdir(_runid,"/tcp");
		createdir(_runid,"/tcp/idx");
		createdir(_runid,"/tcp/hdr");
		createdir(_runid,"/tcp/det");
		createdir(_runid,"/tcp/det/h");
		createdir(_runid,"/tcp/det/h/ip");
		createdir(_runid,"/tcp/det/h/tcp");
		createdir(_runid,"/tcp/det/p");
		
		// hdr files:
		string _ethlfs = _runid+"/tcp/hdr/teth.hdr"; 
		ethl = fopen(_ethlfs.c_str(),"w");
		string _tcplfs = _runid+"/tcp/hdr/tip.hdr";
		tcpl = fopen(_tcplfs.c_str(),"w");
		string _tcphfs = _runid+"/tcp/hdr/tcp.hdr";
		tcph = fopen(_tcphfs.c_str(),"w");
		
	}
	catch(const std::exception& e)
	{
		std::cerr << e.what() << '^' << '\n';
	}
	
	for(ptcp p : tcp_packets) {
		
		memset(&_src, 0, sizeof(_src));
		_src.sin_addr.s_addr = p._iph.saddr;

		memset(&_dest, 0, sizeof(_dest));
		_dest.sin_addr.s_addr = p._iph.daddr;

		sockaddr_in src2,dest2;
		src2 = sockaddr_in();
		src2.sin_addr.s_addr = p._iph.saddr;
		dest2 = sockaddr_in();
		dest2.sin_addr.s_addr = p._iph.daddr;

		string srcaddy = to_string(p._iph.saddr);
		string desaddy = to_string(p._iph.daddr);
		
		// ETH:
		fprintf(ethl,"%s,",p._key.c_str());
		fprintf(ethl,"\"%.2X-%.2X-%.2X-%.2X-%.2X-%.2X\",",p._eth.h_dest[0] , p._eth.h_dest[1] , p._eth.h_dest[2] , p._eth.h_dest[3] , p._eth.h_dest[4] , p._eth.h_dest[5]);
		fprintf(ethl,"\"%.2X-%.2X-%.2X-%.2X-%.2X-%.2X\",", p._eth.h_source[0] , p._eth.h_source[1] , p._eth.h_source[2] , p._eth.h_source[3] , p._eth.h_source[4] , p._eth.h_source[5] );
		fprintf(ethl,"%u",(unsigned short)p._eth.h_proto);
		fprintf(ethl,"\n");
		
		// IPH:
		fprintf(tcpl,"%s,",p._key.c_str());
		fprintf(tcpl,"%d,",ntohs(p._iph.id));
		fprintf(tcpl,"%s,%s,",srcaddy.c_str(),desaddy.c_str());
		fprintf(tcpl,"%d,%d,%d,%d,%d,",(unsigned int)p._iph.version,(unsigned int)p._iph.ihl,((unsigned int)(p._iph.ihl))*4,(unsigned int)p._iph.tos,ntohs(p._iph.tot_len));
		fprintf(tcpl,"%d,%d,%d",(unsigned int)p._iph.ttl,(unsigned int)p._iph.protocol,ntohs(p._iph.check));
		fprintf(tcpl,"\n");

		// TCPH:
		fprintf(tcph,"%s,",p._key.c_str());
		fprintf(tcph,"%u,%u",ntohs(p._tcp.source),ntohs(p._tcp.dest));
		fprintf(tcph,"%u,",ntohl(p._tcp.seq));
		fprintf(tcph,"%u,",ntohl(p._tcp.ack_seq));
		fprintf(tcph,"%d,%d,",(unsigned int)p._tcp.doff,(unsigned int)p._tcp.doff*4);
		fprintf(tcph,"%d,",(unsigned int)p._tcp.urg);
		fprintf(tcph,"%d,",(unsigned int)p._tcp.ack);
		fprintf(tcph,"%d,",(unsigned int)p._tcp.psh);
		fprintf(tcph,"%d,",(unsigned int)p._tcp.rst);
		fprintf(tcph,"%d,",(unsigned int)p._tcp.syn);
		fprintf(tcph,"%d,",(unsigned int)p._tcp.fin);
		fprintf(tcph,"%d,",ntohs(p._tcp.window));
		fprintf(tcph,"%d,",ntohs(p._tcp.check));
		fprintf(tcph,"%d",p._tcp.urg_ptr);
		fprintf(tcph,"\n");

		// create ip header *.det file, tied to key:
		FILE *fiphdet;
		string _fiphdetfs = _runid+"/tcp/det/h/ip/ip_"+p._key+".det"; 
		fiphdet = fopen(_fiphdetfs.c_str(),"w");
		unsigned short iphdrlen;
		iphdrlen = p._iph.ihl*4;
		genpayload(fiphdet,p._buffer,iphdrlen);
		fclose(fiphdet);

		// create tcp header *.det file, tied to key:
		FILE *ftcphdet;
		string _ftcphdetfs = _runid+"/tcp/det/h/tcp/tcp_"+p._key+".det"; 
		ftcphdet = fopen(_ftcphdetfs.c_str(),"w");
		genpayload(ftcphdet,p._buffer+iphdrlen,p._tcp.doff*4);
		fclose(ftcphdet);

		// create data payload *.det file, tied to key:
		int header_size =  sizeof(struct ethhdr) + iphdrlen + p._tcp.doff*4;
		FILE *ftcppldet;
		string _ftcppldetfs = _runid+"/tcp/det/p/tpl_"+p._key+".det"; 
		ftcppldet = fopen(_ftcppldetfs.c_str(),"w");
		genpayload(ftcppldet,p._buffer+header_size,p._size-header_size);
		fclose(ftcppldet);

		// Index builds:
		// tos:
		for(int i=0;i<tchecks.size();i++) {
			unsigned int it = tchecks[i];
			if(it==(unsigned int)ntohs(p._iph.check)) {
				haschecks = true;
				break;
			}
		}
		if(!haschecks) {
			tchecks.push_back((unsigned int)ntohs(p._iph.check));
		}
		haschecks = false;

		// src ports:
		for(int i=0;i<utcpports.size();i++) {
			TcpPort tp = utcpports[i];

			if(tp.base==p._tcp.source) {
				hastcpport = true;
				break;
			}
		}
		if(!hastcpport) {
			TcpPort ta = TcpPort();
			ta.base = p._tcp.source;
			ta.converted = to_string(ntohs(p._tcp.source));
			utcpports.push_back(ta);
		}
		hastcpport = false;

		// dest ports:
		for(int i=0;i<utcpports.size();i++) {
			TcpPort tp = utcpports[i];

			if(tp.base==p._tcp.dest) {
				hastcpport = true;
				break;
			}
		}
		if(!hastcpport) {
			TcpPort ta = TcpPort();
			ta.base = p._tcp.dest;
			ta.converted = to_string(ntohs(p._tcp.dest));
			utcpports.push_back(ta);
		}
		hastcpport = false;

		// Src check:
		for(int x=0;x<ipindex.size();x++) {
			NetAddress n = ipindex[x];

			if(n.base==p._iph.saddr) {
				hasip = true;
				break;
			}
		}
		if(!hasip) {
			NetAddress na = NetAddress();
			na.base = p._iph.saddr;
			na.base_str = to_string(p._iph.saddr);
			ipindex.push_back(na);
		}
		hasip=false;

		// Dest check:
		for(int x=0;x<ipindex.size();x++) {
			NetAddress n = ipindex[x];

			if(n.base==p._iph.daddr) {
				hasip = true;
				break;
			}
		}
		if(!hasip) {
			NetAddress na = NetAddress();
			na.base = p._iph.daddr;
			na.base_str = to_string(p._iph.daddr);
			ipindex.push_back(na);
		}
		hasip=false;

		
		for(int y=0;y<usrcs.size();y++) {
			NetAddress s = usrcs[y];
			
			if(s.base==p._iph.saddr) {
				hassrc = true;
				break;
			}
			
		}

		if(!hassrc) {
			
			NetAddress ns = NetAddress();
			ns.base = p._iph.saddr;
			ns.base_str = to_string(p._iph.saddr);
			usrcs.push_back(ns);
		}
		hassrc = false;

		for(int x=0;x<udests.size();x++) {
			NetAddress dt = udests[x];
			if(dt.base==p._iph.daddr) {
				hasdest = true;
				break;
			}
		}

		if(!hasdest) {
			
			NetAddress nd = NetAddress();
			nd.base = p._iph.daddr;
			nd.base_str = to_string(p._iph.daddr);
			udests.push_back(nd);
		}
		hasdest = false;
	}
	
	// close main files:
	fclose(tcph);
	fclose(tcpl);
	fclose(ethl);
	tcp_packets.clear();

	// build index files:
	FILE *ipidxf;
	string _ipidxfs = _runid+"/tcp/idx/tip.idx";
	ipidxf = fopen(_ipidxfs.c_str(),"w");
	for(int i=0; i<ipindex.size();i++) {
		NetAddress n = ipindex[i];
		n = convert_net(n);
		writeindex(ipidxf,to_string(i+1),n.base_str,n.converted);
	}
	fclose(ipidxf);
	ipindex.clear();

	FILE *utcpf;
	string _utcpfs = _runid+"/tcp/idx/tuports.idx";
	utcpf = fopen(_utcpfs.c_str(),"w");
	for(int i=0; i<utcpports.size();i++) {
		TcpPort t = utcpports[i];
		writeindex(utcpf,to_string(i+1),to_string(t.base),t.converted);
	}
	fclose(utcpf);
	utcpports.clear();

	FILE *tcpsu;
	string _tcpsufs = _runid+"/tcp/idx/tipusrc.idx";
	tcpsu = fopen(_tcpsufs.c_str(),"w");
	
	for(int i=0; i<usrcs.size();i++) {
		NetAddress n = usrcs[i];
		n = convert_net(n);
		writeindex(tcpsu,to_string(i+1),n.base_str,n.converted);
	}
	fclose(tcpsu);
	usrcs.clear();

	
	FILE *tcpdu;
	string _tcpdufs = _runid+"/tcp/idx/tipudest.idx";
	tcpdu = fopen(_tcpdufs.c_str(),"w");
	
	for(int i=0; i<udests.size();i++) {
		NetAddress n = udests[i];
		n = convert_net(n);
		writeindex(tcpdu,to_string(i+1),n.base_str,n.converted);
	}
	
	fclose(tcpdu);
	udests.clear();

	FILE *txf;
	string _txfs = _runid+"/tcp/idx/tipchecks.idx";
	txf = fopen(_txfs.c_str(),"w");

	for(int i=0;i<tchecks.size();i++) {
		unsigned int x = tchecks[i];
		writeindex(txf,to_string(i+1),to_string(x),"");
	}

	fclose(txf);
	tchecks.clear();
	
}

void ank::writelog_udp(string _rid) {

	FILE *udpl,*ethl,*udph;
	
	vector<NetAddress> ipindex;
	bool hasip=false;

	string _runid = _rid;

	try
	{
		
		createdir(_runid,"");
		createdir(_runid,"/udp");
		createdir(_runid,"/udp/idx");
		createdir(_runid,"/udp/hdr");
		createdir(_runid,"/udp/det");
		createdir(_runid,"/udp/det/h");
		createdir(_runid,"/udp/det/h/ip");
		createdir(_runid,"/udp/det/h/udp");
		createdir(_runid,"/udp/det/p");
		
		// hdr files:
		string _ethlfs = _runid+"/udp/hdr/ueth.hdr"; 
		ethl = fopen(_ethlfs.c_str(),"w");
		string _tcplfs = _runid+"/udp/hdr/uip.hdr";
		udpl = fopen(_tcplfs.c_str(),"w");
		string _tcphfs = _runid+"/udp/hdr/udp.hdr";
		udph = fopen(_tcphfs.c_str(),"w");
		
	}
	catch(const std::exception& e)
	{
		std::cerr << e.what() << '^' << '\n';
	}
	
	for(pudp u : udp_packets) {
		
		memset(&_src, 0, sizeof(_src));
		_src.sin_addr.s_addr = u._iph.saddr;

		memset(&_dest, 0, sizeof(_dest));
		_dest.sin_addr.s_addr = u._iph.daddr;

		sockaddr_in src2,dest2;
		src2 = sockaddr_in();
		src2.sin_addr.s_addr = u._iph.saddr;
		dest2 = sockaddr_in();
		dest2.sin_addr.s_addr = u._iph.daddr;

		string srcaddy = to_string(u._iph.saddr);
		string desaddy = to_string(u._iph.daddr);
		
		// ETH:
		fprintf(ethl,"%s,",u._key.c_str());
		fprintf(ethl,"\"%.2X-%.2X-%.2X-%.2X-%.2X-%.2X\",",u._eth.h_dest[0] , u._eth.h_dest[1] , u._eth.h_dest[2] , u._eth.h_dest[3] , u._eth.h_dest[4] , u._eth.h_dest[5]);
		fprintf(ethl,"\"%.2X-%.2X-%.2X-%.2X-%.2X-%.2X\",", u._eth.h_source[0] , u._eth.h_source[1] , u._eth.h_source[2] , u._eth.h_source[3] , u._eth.h_source[4] , u._eth.h_source[5] );
		fprintf(ethl,"%u",(unsigned short)u._eth.h_proto);
		fprintf(ethl,"\n");
		
		// IPH:
		fprintf(udpl,"%s,",u._key.c_str());
		fprintf(udpl,"%d,",ntohs(u._iph.id));
		fprintf(udpl,"%s,%s,",srcaddy.c_str(),desaddy.c_str());
		fprintf(udpl,"%d,%d,%d,%d,%d,",(unsigned int)u._iph.version,(unsigned int)u._iph.ihl,((unsigned int)(u._iph.ihl))*4,(unsigned int)u._iph.tos,ntohs(u._iph.tot_len));
		fprintf(udpl,"%d,%d,%d",(unsigned int)u._iph.ttl,(unsigned int)u._iph.protocol,ntohs(u._iph.check));
		fprintf(udpl,"\n");

		// UDPH:
		fprintf(udph,"%s,",u._key.c_str());
		fprintf(udph,"%d,",ntohs(u._udp.source));
		fprintf(udph,"%d,",ntohs(u._udp.dest));
		fprintf(udph,"%d,",ntohs(u._udp.len));
		fprintf(udph,"%d,",ntohs(u._udp.check));
		fprintf(udph,"\n");

		// create ip header *.det file, tied to key:
		FILE *fiphdet;
		string _fiphdetfs = _runid+"/udp/det/h/ip/ip_"+u._key+".det"; 
		fiphdet = fopen(_fiphdetfs.c_str(),"w");
		unsigned short iphdrlen;
		iphdrlen = u._iph.ihl*4;
		genpayload(fiphdet,u._buffer,iphdrlen);
		fclose(fiphdet);

		// create tcp header *.det file, tied to key:
		FILE *ftcphdet;
		string _ftcphdetfs = _runid+"/udp/det/h/udp/udp_"+u._key+".det"; 
		ftcphdet = fopen(_ftcphdetfs.c_str(),"w");
		genpayload(ftcphdet,u._buffer+iphdrlen,sizeof(u._udp));
		fclose(ftcphdet);

		// create data payload *.det file, tied to key:
		int header_size =  sizeof(struct ethhdr) + iphdrlen + sizeof(u._udp);
		FILE *ftcppldet;
		string _ftcppldetfs = _runid+"/udp/det/p/upl_"+u._key+".det"; 
		ftcppldet = fopen(_ftcppldetfs.c_str(),"w");
		genpayload(ftcppldet,u._buffer+header_size,u._size-header_size);
		fclose(ftcppldet);

		// build unique ip index address:
		for(int x=0;x<ipindex.size();x++) {
			NetAddress n = ipindex[x];

			if(n.base==u._iph.saddr) {
				hasip = true;
				break;
			}
		}
		if(!hasip) {
			NetAddress na = NetAddress();
			na.base = u._iph.saddr;
			na.base_str = to_string(u._iph.saddr);
			ipindex.push_back(na);
		}
		hasip=false;
	}
	
	// close main files:
	fclose(udph);
	fclose(udpl);
	fclose(ethl);
	tcp_packets.clear();

	// build index files:
	FILE *ipidxf;
	string _ipidxfs = _runid+"/udp/idx/uip.idx";
	ipidxf = fopen(_ipidxfs.c_str(),"w");
	for(int i=0; i<ipindex.size();i++) {
		NetAddress n = ipindex[i];
		n = convert_net(n);
		writeindex(ipidxf,to_string(i+1),n.base_str,n.converted);
	}
	fclose(ipidxf);
	ipindex.clear();

}


void ank::writeindex(FILE *_if, string _k, string _rv,string _cv) {

	fprintf(_if,"%s,",_k.c_str());
	fprintf(_if,"%s",_rv.c_str());
	if(_cv!="") {
		fprintf(_if,",%s",_cv.c_str());
	}
	fprintf(_if,"\n");
}

NetAddress ank::convert_net(NetAddress na) {
	NetAddress ret = na;

	// Convert supplied base to converted na value:
	sockaddr_in scvt = sockaddr_in();
	scvt.sin_addr.s_addr = na.base;
	ret.converted = inet_ntoa(scvt.sin_addr);

	return ret;
}

void ank::ProcessPacket(unsigned char* buffer, int size)
{	
	struct iphdr *iph = (struct iphdr*)(buffer + sizeof(struct ethhdr));
	unsigned short iphdrlen = iph->ihl*4;
	struct ethhdr *eth = (struct ethhdr *)buffer;

	_packets_captured++;

	try
	{		
		if(iph->protocol==1 && _run_icmp) {
			struct icmphdr *icmph = (struct icmphdr *)(buffer + iphdrlen  + sizeof(struct ethhdr));
			picmp _icmp = picmp(*eth,*iph,*icmph);

			_icmp._key = to_string(icmp_packets.size()+1);
			_icmp._buffer = buffer;
			_icmp._size = size;

			icmp_packets.push_back(_icmp);
			_packets_traced++;
		}
		else if(iph->protocol==6 && _run_tcp) {
			struct tcphdr *tcph=(struct tcphdr*)(buffer + iphdrlen + sizeof(struct ethhdr));
			ptcp _tcp = ptcp(*eth,*iph,*tcph);

			_tcp._key = to_string(tcp_packets.size()+1);
			_tcp._buffer = buffer;
			_tcp._size = size;

			tcp_packets.push_back(_tcp);
			_packets_traced++;
		}
		else if(iph->protocol==17 && _run_udp) {
			struct udphdr *udph = (struct udphdr*)(buffer + iphdrlen  + sizeof(struct ethhdr));
			pudp _udp = pudp(*eth,*iph,*udph);

			_udp._key = to_string(udp_packets.size()+1);
			_udp._buffer = buffer;
			_udp._size = size;

			udp_packets.push_back(_udp);
			_packets_traced++;
		}
	
	}
	catch(const std::exception& e)
	{
		std::cerr << e.what() << '\n';
	}
}

/*
void ank::writelog_icmp(unsigned char* Buffer , int Size)
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
	//genpayload(Buffer,iphdrlen);
		
	fprintf(_lgf , "UDP Header\n");
	//genpayload(Buffer + iphdrlen , sizeof icmph);
		
	fprintf(_lgf , "Data Payload\n");	
	
	//Move the pointer ahead and reduce the size of string
	//genpayload(Buffer + header_size , (Size - header_size) );
	
	fprintf(_lgf , "\n###########################################################");
} */

void ank::genpayload(FILE *_fpd,unsigned char* data , int Size)
{
	int i , j;
	for(i=0 ; i < Size ; i++)
	{
		// hex line complete
		if( i!=0 && i%16==0)   
		{
			fprintf(_fpd , "         ");
			for(j=i-16 ; j<i ; j++)
			{
				if(data[j]>=32 && data[j]<=128) { fprintf(_fpd , "%c",(unsigned char)data[j]); }
					else { fprintf(_fpd , "."); } 
			}

			// end payload file line
			fprintf(_fpd , " } \n"); 
		} 
		
		// start payload file line
		if(i%16==0) fprintf(_fpd , "[+]-> {"); { fprintf(_fpd , " %02X",(unsigned int)data[i]); }
				
		if( i==Size-1) 
		{
			for(j=0;j<15-i%16;j++) { fprintf(_fpd , "   "); }
			
			fprintf(_fpd , "         ");
			
			for(j=i-i%16 ; j<=i ; j++)
			{
				if(data[j]>=32 && data[j]<=128) { fprintf(_fpd , "%c",(unsigned char)data[j]); }
					else { fprintf(_fpd , "."); }
			}
			
			fprintf(_fpd ,  " } \n" ); // end payload file line
		}
	}
}