import CORBA, Messaging, Messaging__POA
import time, sys, random
from pycsp import *

class MessageServer(Messaging__POA.Receiver):
	def __init__(self, coord, infile=None):
		self.coord = coord
		self.my_id = coord.register(self._this())
		self.events = []
		self.recs = {}
		self.recs_q = {}
		self.tic = 0
		self.ends = 0
		self.infile = infile
		
	def send(self, m_id, ts, v):
		self.send_c((m_id, ts, v))

	def get_id(self):
		return self.my_id

	def init_receivers(self):
		while(not self.coord.ready()):
			time.sleep(1)
		recs = self.coord.receivers()
		self.recs = dict([(x.get_id(), x) for x in recs])
		self.recs_q = dict([(x.get_id(), []) for x in recs])

	def messages(self, size):
		if(self.infile == None):
			return [random.sample([0,1], 1)[0] for i in range(size)]
		else:
			f = open(infile)
			return [int(s) for s in f.readlines]
	
	@process
	def do_store_event(self, ein):
		while(1):
			self.events.append(ein())

	@process
	def do_tics(self, cin, cout):
		while(1):
			t = cin()
			if  t > self.tic:
				self.tic = t
			self.tic = self.tic + 1
			cout(self.tic) 

	def do_event(self, m, tout, tin, eout, v):
		tout(0)
		mtic = tin()
		if(m == 0):
			eout((m, mtic, v, "loc"))
		else:
			for k in [x for x in self.recs.keys() if x != self.my_id]:
				eout((k, mtic, v, "send"))
				self.recs[k].send(self.my_id, mtic, v * 2)
	
	@process
	def do_sends(self, tout, tin, eout, fout):
		ms = self.messages(5)
		print "messages: " + str(ms)
		for m in ms:
			self.do_event(m, tout, tin, eout, 1)
		self.do_event(1, tout, tin, eout, -1)
		fout(0)
		#never will receive
		if len(self.recs.keys()) == 1:
			fout(0)

	@process
	def do_receives(self, tout, tin, eout, sin, fout):
		while 1:
			(origin, tic, v) = sin()
			tout(tic)
			t = tin()
			eout((origin, t, v, "rec"))
			if v < 0:
				self.ends = self.ends + 1
			# if received end events from all partners
			if self.ends == (len(self.recs.keys()) - 1):
				fout(0)

	@process
	def do_finish(self, fin, tout, eout, sin):
		fin()
		fin()
		tout.poison()
		eout.poison()
		sin.poison()

	def do_test(self):
		tin_c = Channel("tics-in")
		tout_c = Channel("tics-out")
		event_c = Channel("event")
		send_c = Channel("send")
		f_c = Channel("finish")
		self.send_c = send_c.writer()

		self.init_receivers()


		Parallel(
			self.do_store_event(event_c.reader()),
			self.do_tics(tin_c.reader(), tout_c.writer()),
			self.do_sends(tin_c.writer(), tout_c.reader(), event_c.writer(),
				f_c.writer()),
			self.do_receives(tin_c.writer(), tout_c.reader(), event_c.writer(),
				send_c.reader(), f_c.writer()),
			self.do_finish(f_c.reader(), tin_c.writer(), event_c.writer(),
				send_c.writer())
		)

		print "\n".join([str(x) for x in self.events])
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
