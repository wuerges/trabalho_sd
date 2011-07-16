
#
# The client, on the command line
#

import CORBA, Fortune
import CosNaming
orb = CORBA.ORB_init()

# Obtain a reference to the root naming context
obj         = orb.resolve_initial_references("NameService")
name_server = obj._narrow(CosNaming.NamingContext)

cs_name = [CosNaming.NameComponent("cookies", "chocolate")]
o = name_server.resolve(cs_name)
o = o._narrow(Fortune.CookieServer)
print o.get_cookie()


