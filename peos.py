from threading import Thread
import time

def peos():
	time.sleep(3)
	print('peos')

for i in range(5):
	thread = Thread(target=peos)
	thread.start()

