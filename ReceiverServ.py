import CORBA, Messaging, Messaging__POA
import time, sys, random

class MessageServer(Messaging__POA.Receiver):
	def __init__(self, coord):
		self.coord = coord
		self.my_id = coord.register(self._this())
		self.events = []
		self.recs = {}
		self.tic = 0
		
	def send(self, m_id, ts):
		print m_id, ts

	def get_id(self):
		return self.my_id

	def init_receivers(self):
		while(not self.coord.ready()):
			time.sleep(1)
		recs = self.coord.receivers()
		self.recs = dict([(x.get_id(), x) for x in recs])

	def messages(self, size):
		return [random.sample(self.recs.keys(), 1)[0] for i in range(10)]
	
	def do_event(self, m):
		# this next 2 lines must be synchronized
		self.tic = self.tic + 1
		mtic = self.tic
		if(m == self.my_id):
			self.events.append((m, mtic))
		else:
			self.recs[m].send(self.my_id, mtic)

	def do_test(self):
		self.init_receivers()
		
		for m in self.messages(10):
			self.do_event(m)

		print self.events
		self.coord.unregister(self.my_id)

class CoordinatorServer(Messaging__POA.Coordinator):
	def __init__(self, num):
		self.num = num
		self.msgs = {}

	def gen_num(self):
		i = 1
		while 1:
			yield i
			i = i + 1

	def register(self, rec):
		r = self.gen_num().next()
		self.msgs[r] = rec
		return r

	def unregister(self, rec):
		print self.msgs
		del self.msgs[rec]

	def ready(self):
		return len(self.msgs) == self.num

	def receivers(self):
		return self.msgs.values()
