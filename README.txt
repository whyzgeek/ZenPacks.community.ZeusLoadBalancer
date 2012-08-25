
ZenPacks.community.ZeusLoadBalancer-2.1.8-py2.7 -- for Zenoss 4.1.1

Special Zenpack monitoring Riverbed Stingray/Zeus LoadBalanacers.

* It discovers all the Virtual Servers and the Pools and display them nicely as componets of Zeus device in Zenoss.
* It graphs many useful peformance indicators of the device and its virtual servers and pools.
* It alerts if a pool becomes empty.

Release notes for version 2.1.8
-------------------------------
1- A new daemon(based on zenperfsnmp) added, to collect the virtual servers and pools. This new daemon has following benefits:
	- It calculates the 64bit values out of SNMPv1 style two 32bit OIDs and save them in single 64bit RRD.
	- It exposes number of active nodes in a pool as a single value by aggregating the state of each node registered in that pool.
	  This enables adding threshold and graph for number active nodes.(creates pesudo datasource from multiple datasources)
2- Added a lot of extra KPIs from Zeus MIB to be monitored.
3- Now the UI does the dictionary lookup to show more descriptive status for each component.
4- The UI component list, now shows live values from collection rather than static values from modeling.(where it made sense)

Enjoy!

Whyzgeek