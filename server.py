# -*- coding: utf-8 -*-
#
# The server
#

#!/usr/bin/env python

import sys, os
import CORBA, Fortune, Fortune__POA
import CosNaming
from ReceiverServ import *

orb = CORBA.ORB_init(sys.argv)
poa = orb.resolve_initial_references("RootPOA")
poa._get_the_POAManager().activate()

# Obtain a reference to the root naming context
obj         = orb.resolve_initial_references("NameService")
name_server = obj._narrow(CosNaming.NamingContext)

servant = CoordinatorServer(int(sys.argv[1]))

poa.activate_object(servant)
cs_name = [CosNaming.NameComponent("messaging", "coordinator")]
name_server.rebind(cs_name, servant._this())

orb.run()
