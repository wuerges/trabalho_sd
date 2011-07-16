#
# The server
#

#!/usr/bin/env python

import sys, os
import CORBA, Fortune, Fortune__POA
import CosNaming

FORTUNE_PATH = "/usr/games/fortune"

class CookieServer_i (Fortune__POA.CookieServer):
    def get_cookie(self):
        pipe   = os.popen(FORTUNE_PATH)
        cookie = pipe.read()
        if pipe.close():
            # An error occurred with the pipe
            cookie = "Oh dear, couldn't get a fortune\n"
        return cookie

orb = CORBA.ORB_init(sys.argv)
poa = orb.resolve_initial_references("RootPOA")
poa._get_the_POAManager().activate()

# Obtain a reference to the root naming context
obj         = orb.resolve_initial_references("NameService")
name_server = obj._narrow(CosNaming.NamingContext)

servant = CookieServer_i()
poa.activate_object(servant)
cs_name = [CosNaming.NameComponent("cookies", "chocolate")]
name_server.rebind(cs_name, servant._this())

#print orb.object_to_string(servant._this())

orb.run()
