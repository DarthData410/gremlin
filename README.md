# gremlin
By: J. Brandon George | darth.data410@gmail.com | twitter: @PyFryDay | medium.com: https://darth-data410.medium.com/ | youtube: https://www.youtube.com/@pyfryday
license found @: gremlin/LICENSE (Apache License Version 2.0 Janurary 2004)

# Details:
This purpose of this open source project is to enable a deeper understanding of security conepts related to linux systems. The goal of this framework is to offer a toolkit that someone could easily use to help trace, record, analyze,report upon and simulate threats. This should be used to help protect systems YOU OWN or have responsibility for. USE AS-IS without WARRANTY.  

# /ank - A NetworK sniffer (current focus)
/ank is a network sniffer module that records to a log file structure starting in the root of where sudo ./gremlin is executed. It offers parameters for recoridng only -TCP packets, -UDP packet, or combining both. (ICMP and other protocol packets will be offered as well in future releases.) The goal of /ank is not to just record packet data, including payload, but also to build out a postgresql database, along with initial reporitng using D3 javascript/html to render insights about trace runs. 

# /meta - pentesting MangemEnT And execution (current focus)
/meta is an execution engine, that relies heavliy on python scripts to drive its different workflows and schedules of jobs. At its core /meta is a job execution engine, with driven log and workflow output to file or database format. This module allows for easily stringing together multiple information gathers, simulated attack vectors, etc. and working with the output of each step to build upon the previous for execution and execution tracked feedback. 

# /gh0st - Packet Data Transformation, Storage, and Analytics (future development)
/gh0st will target using Apache Arrow, through python, specifically PyArrow. /gh0st will enable the output of /ank
to be harvested and strored in a postegresql db, and then into a PyArrow set of tabular datasets for use in driving
analytics about threat vectors, etc.