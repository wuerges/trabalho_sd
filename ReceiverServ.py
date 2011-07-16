import CORBA, Messaging, Messaging__POA
import time, sys, random
from pycsp import *

class MessageServer(Messaging__POA.Receiver):
	def __init__(self, coord):
		self.coord = coord
		self.my_id = coord.register(self._this())
		self.events = []
		self.recs = {}
		self.recs_q = {}
		self.tic = 0
		
	def send(self, m_id, ts):
		self.send_c((m_id, ts))

	def get_id(self):
		return self.my_id

	def init_receivers(self):
		while(not self.coord.ready()):
			time.sleep(1)
		recs = self.coord.receivers()
		self.recs = dict([(x.get_id(), x) for x in recs])
		self.recs_q = dict([(x.get_id(), []) for x in recs])

	def messages(self, size):
		return [random.sample(self.recs.keys(), 1)[0] for i in range(10)]
	
	@process
	def do_store_event(self, ein):
		while(1):
			print "doing store"
			self.events.append(ein())

	@process
	def do_tics(self, cin, cout):
		while(1):
			print "doing tick"
			t = cin()
			if t > self.tic:
				self.tic = t 
			self.tic = self.tic + 1
			cout(self.tic) 

	def do_event(self, m, tout, tin, eout):
		# this next 2 lines must be synchronized
		print "doing event"
		tout(0)
		mtic = tin()
		if(m == self.my_id):
			eout((m, mtic))
		else:
			self.recs[m].send(self.my_id, mtic)
	
	@process
	def do_sends(self, tout, tin, eout):
		for m in self.messages(10):
			self.do_event(m, tout, tin, eout)
		self.do_event(-1, tout, tin, eout)

	@process
	def do_receives(self, tout, tin, eout, sin):
		while 1:
			(origin, tic) = sin()
			tout(tic)
			t = tin()
			eout((origin, t))
			if origin == -1:
				print "reached end"
				tout.poison()
				eout.poison()
				sin.poison()

	def do_test(self):
		tin_c = Channel("tics-in")
		tout_c = Channel("tics-out")
		event_c = Channel("event")
		send_c = Channel("send")
		self.send_c = send_c.writer()

		self.init_receivers()


		Parallel(
			self.do_store_event(event_c.reader()),
			self.do_tics(tin_c.reader(), tout_c.writer()),
			self.do_sends(tin_c.writer(), tout_c.reader(), event_c.writer()),
			self.do_receives(tin_c.writer(), tout_c.reader(), event_c.writer(),
				send_c.reader()),
		)

		print self.events
		self.coord.unregister(self.my_id)

class CoordinatorServer(Messaging__POA.Coordinator):
	def __init__(self, num):
		self.num = num
		self.msgs = {}
		self.id_gen = self.gen_num()
		self.ready_v = False

	def gen_num(self):
		i = 1
		while 1:
			yield i
			i = i + 1

	def register(self, rec):
		r = self.id_gen.next()
		print "registered " + str(r)
		self.msgs[r] = rec
		return r

	def unregister(self, rec):
		print self.msgs
		del self.msgs[rec]
		if self.msgs == {}:
			self.ready_v = False

	def ready(self):
		print "ready? " + str(len(self.msgs)) + " " + str(self.num)
		print self.msgs.keys()
		if not self.ready_v:
			self.ready_v = len(self.msgs.keys()) >= self.num
		return self.ready_v

	def receivers(self):
		return self.msgs.values()
