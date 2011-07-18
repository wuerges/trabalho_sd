# -*- coding: utf-8 -*-
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
	print "waiting for message:"
	print msg_s.app_receive()
	print "finished callback"

def callback_S1(s):
	print "running S1 ( e11, m21, m31, e41, m51, m61)"
	s.app_local("e11")
	s.app_send("m21")
	s.app_send("m31")
	s.app_local("e41")
	s.app_send("m51")
	s.app_send("m61")

def callback_S2(s):
	print "S2 ( e12, m22, e32, m42, m52, e62, m72)"
	s.app_local("e12")
	s.app_send("m22")
	s.app_local("e32")
	s.app_send("m42")
	s.app_send("m52")
	s.app_local("e62")
	s.app_send("m72")

#Implementar a partir de objeto aplicação correspondente a dependência
#da mensagem m53 como sendo precedida pela emissão dos eventos evento
#interno e32 e mensagem m21.

def callback_S3(s):
	print "S3 ( m13, m23, e33, e43, m53, m63)"
	s.app_send("m13")
	s.app_send("m23")
	s.app_local("e33")
	s.app_local("e43")

	wl = set(["m42", "m21"])
	while len(wl) != 0:
		print "waiting for " + str(wl)
		(r, m) = s.app_receive() 
		if r == 0 and m in wl:
			wl.discard(m)

	s.app_send("m53")
	s.app_send("m63")



argd = { "S1" : callback_S1, "S2" : callback_S2, "S3" : callback_S3 }

ms = MessageServer(coord)
if(len(sys.argv) > 1):
	ms.start(argd[sys.argv[1]])

else:
	ms.start(test_callback)

