from threading import Thread
import time

class Peos:
	def __init__(self):
		self.lis = []
	def push(self):
		self.lis.append(1)

def peos():
	time.sleep(3)
	p.push()
	print(p.lis)
	

p = Peos()	
for i in range(5):
	thread = Thread(target=peos)
	thread.start()

