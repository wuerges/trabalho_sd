
#
# The client, on the command line
#

import CORBA, Fortune
import CosNaming
from ReceiverServ import *

orb = CORBA.ORB_init()
poa = orb.resolve_initial_references("RootPOA")
poa._get_the_POAManager().activate()

# Obtain a reference to the root naming context
obj         = orb.resolve_initial_references("NameService")
name_server = obj._narrow(CosNaming.NamingContext)

cs_name = [CosNaming.NameComponent("messaging", "coordinator")]
coord_o = name_server.resolve(cs_name)
coord = coord_o._narrow(CoordinatorServer)

def test_callback(msg_s):
	print "doing callback"
	ms = [random.sample([0,1], 1)[0] for i in range(5)]
	print "messages: " + str(ms)
	for m in ms:
		if m == 0:
			msg_s.app_local("<test local>")
		else:
			msg_s.app_send("<test send>")

ms = MessageServer(coord)
ms.start(test_callback)

