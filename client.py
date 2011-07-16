
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

ms = MessageServer(coord)
ms.do_test()

