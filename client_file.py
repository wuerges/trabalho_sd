# -*- coding: utf-8 -*-
#
# The client, on the command line, reads events from file
#

import CORBA, Fortune
import CosNaming
from ReceiverServ import *
import re

orb = CORBA.ORB_init()
poa = orb.resolve_initial_references("RootPOA")
poa._get_the_POAManager().activate()

# Obtain a reference to the root naming context
obj         = orb.resolve_initial_references("NameService")
name_server = obj._narrow(CosNaming.NamingContext)

cs_name = [CosNaming.NameComponent("messaging", "coordinator")]
coord_o = name_server.resolve(cs_name)
coord = coord_o._narrow(CoordinatorServer)

def callback_stdin(s):
	for line in sys.stdin:
		ev = line.strip()
		tks = line.strip().split("->")
		if len(tks) > 1:
			#this has a guard
			m = re.match('^\[(.*)\]$', tks[0].strip())
			gs = m.group(1).split(',')
			print "Guard: " + str(gs)
			wl = set([x.strip() for x in gs])
			print "Guard: " + str(wl)
			while len(wl) != 0:
				(r, m) = s.app_receive() 
				if r == 0 and m in wl:
					wl.discard(m)
			ev = tks[1].strip()

		print "Event: " + str(ev)
		if re.match('^m.*', ev):
			s.app_send(ev)
		elif re.match('^e.*', ev):
			s.app_local(ev)
		else:
			raise "Irrecognized event: " + str(ev)

ms = MessageServer(coord)
ms.start(callback_stdin)



