import CORBA, Messaging, Messaging__POA
import time, sys, random
from pycsp import *

class Message:
	def __init__(self, from_, to, ts, v, t):
		self.origin = from_
		self.dest = to
		self.ts = ts
		self.v = v
		self.t = t

	def __str__(self):
		return "Message(" + str((self.origin, self.dest, self.ts, self.v, self.t))

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
		
	@process
	def send_helper(self, sin, eout, tout, tin):
		while 1:
			msg = sin()
			tout(msg.ts)
			tin()
			eout(msg)

	def send(self, m_id, ts, v):
		self.send_c(Message(m_id, self.my_id, ts, v, "recv"))

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
		# if this is a local event
		if(m == 0):
			eout(Message(self.my_id, self.my_id, mtic, v, "loc"))
		# if this is a send event
		else:
			for k in [x for x in self.recs.keys() if x != self.my_id]:
				eout(Message(self.my_id, k, mtic, v, "send"))
				self.recs[k].send(self.my_id, mtic, v * 2)
	
	@process
	def do_sends(self, tout, tin, eout, fout):
		ms = self.messages(5)
		print "messages: " + str(ms)
		for m in ms:
			self.do_event(m, tout, tin, eout, 1)
		self.do_event(1, tout, tin, eout, -1)
		self.do_event(0, tout, tin, eout, -2)
		fout(0)

	def do_dequeue(self):
		while((len(self.recs_q) > 0) and 
				reduce(lambda r,i: r and i, [len(self.recs_q[x]) != 0 for x in self.recs_q], True)):
			min_q = min([self.recs_q[x] for x in self.recs_q], key=lambda k : k[0].ts)
			min_msg = min_q[0]
			self.events.append(min_msg)
			if min_msg.v == -2:
				assert(len(self.recs_q[min_msg.origin]) == 1)
				del self.recs_q[min_msg.origin]
			del min_q[0]

	@process
	def do_receives(self, tout, tin, ein, fout):
		while 1:
			#received a message!
			msg = ein()
			print "Recorded event: " + str(msg)
			self.recs_q[msg.origin].append(msg)

			self.do_dequeue()
			#self.events.append(msg)

			if msg.v == -2:
				self.ends = self.ends + 1
			# if received end events from all partners

			if len(self.recs_q) == 0:
				fout(0)


	@process
	def do_finish(self, fin, tout, eout):
		fin()
		fin()
		tout.poison()
		eout.poison()
		self.send_c.poison()

	def do_test(self):
		tin_c = Channel("tics-in")
		tout_c = Channel("tics-out")
		event_c = Channel("event")
		send_c = Channel("event")
		f_c = Channel("finish")

		self.send_c = send_c.writer()

		self.init_receivers()


		Parallel(
			self.do_tics(tin_c.reader(), tout_c.writer()),

			self.send_helper(send_c.reader(), event_c.writer(),
				tin_c.writer(), tout_c.reader()),

			self.do_sends(tin_c.writer(), tout_c.reader(), event_c.writer(),
				f_c.writer()),
			self.do_receives(tin_c.writer(), tout_c.reader(), event_c.reader(),
				f_c.writer()),
			self.do_finish(f_c.reader(), tin_c.writer(), event_c.writer())
		)

		print "This client id: " + str(self.my_id)
		print "Recorded events"
		print "\n".join([str(x) for x in self.events])
		print "Recorded event queues"
		for ek in self.recs_q.keys():
			print "\n".join([str(e) for e in self.recs_q[ek]])

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
