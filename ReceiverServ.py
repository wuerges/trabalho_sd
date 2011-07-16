import CORBA, Messaging, Messaging__POA
import time

class MessageServer(Messaging__POA.Receiver):
	def __init__(self, coord):
		self.coord = coord
		
	def send(self, m_id, ts):
		print m_id, ts
	
	def do_test(self):
		self.my_id = coord.register(self)
		while(!coord.ready()):
			time.sleep(1)
		recs = self.coord.receivers()
		map(lambda x: x.send(self.my_id, 0), recs)

class CoordinatorServer(Messagin__POA.Coordinator):
	def __init__(self, num):
		self.num = num

	def register(self, rec):
		self.msgs.append(rec)
		return len(self.msgs)

	def ready(self):
		return len(self.msgs) == self.num



