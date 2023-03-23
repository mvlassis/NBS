import subprocess
import time

path = './5nodes/trans0.txt'
with open('mine_times.txt', 'r') as file1:
	data1 = file1.readlines()
y = len(data1)
with open(path, 'r') as file:
    data = file.readlines()
count = 0
t = time.time()
for line in data:
	attributes = line.replace('\n', '').split(' ')
	# print(attributes)
	id = attributes[0][2]
	if id == '1':
		ip_port = '192.168.0.5:5000'
	elif id == '2':
		ip_port = '192.168.0.1:5000'
	elif id == '3':
		ip_port = '192.168.0.2:5000'
	elif id == '4':
		ip_port = '192.168.0.3:5000'
	
	full_command = 'python cli.py t ' + ip_port + ' ' + attributes[1]
	print(full_command)
	# full_command = 'ls' 
	process = subprocess.Popen(full_command.split(), stdout=subprocess.PIPE)
	print(ip_port)
	count = count+1
	if count == 1:
		#flag = True
		#while (flag):
		#	with open('mine_times.txt', 'r') as file1:
		#		data1 = file1.readlines()
		#		if len(data1) == (y+1):
		#			y = y+1
		#			flag = False
		time.sleep(10)
	if (count-1) % 3 == 0:
		#flag = True
		#while (flag):
		#	with open('mine_times.txt', 'r') as file1:
		#		data1 = file1.readlines()
		#		if len(data1) == (y+1):
		#			y=y+1
		#			flag = False
		time.sleep(10)
			
t1 = time.time()
timetotal = t1-t
throughput = count/(timetotal/1000)
print(throughput)
total_trans = 0
blocktime = 0
with open('mine_times.txt', 'r') as file:
	data = file.readlines()
	for line in data:
		total_trans += 1
		blocktime = blocktime + int(line.replace('\n',''))
	meanblock = blocktime/total_trans
	print('Mean block time =', meanblock)

			# command = 'cli.py t '+ attributes[0] + ' ' + attributes[1]
			# process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
			 # output, error = process.communicate()
