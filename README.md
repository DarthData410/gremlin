# gremlin
By: J. Brandon George | darth.data410@gmail.com | twitter: @PyFryDay | medium.com: https://darth-data410.medium.com/ | youtube: https://www.youtube.com/@pyfryday
license found @: gremlin/LICENSE (Apache License Version 2.0 Janurary 2004)

# Details:
This purpose of this open source project is to enable a deeper understanding of security conepts related to linux systems. The goal of this framework is to offer a toolkit that someone could easily use to help trace, record, analyze and report upon threats upon the recording/reporting system. This should be used to help protect systems YOU OWN or have responsibility for. 

# /ank - a network sniffer
The first module of gremlin is /ank - a netowkr sniffer. As the name implies this module records to a log file structure starting in the root of where sudo ./gremlin is executed. It offers parameters for recoridng only -TCP packets, -UDP packet, or combining both. (ICMP and other protocol packets will be offered as well in future releases.)

The goal of /ank is not to just record packet data, including payload, but also to build out a postgresql database, along with initial reporitng using D3 javascript/html to render insights about trace runs. 
