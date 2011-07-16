import CORBA, Messaging, Messaging__POA
import time, sys

class MessageServer(Messaging__POA.Receiver):
	def __init__(self, coord):
		self.coord = coord
		self.my_id = coord.register(self._this())
		
	def send(self, m_id, ts):
		print m_id, ts
	
	def do_test(self):
		while(not self.coord.ready()):
			time.sleep(1)
		recs = self.coord.receivers()
		map(lambda x: x.send(self.my_id, 0), recs)
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
