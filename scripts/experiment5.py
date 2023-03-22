path = 'C:/Users/Desktop/Desktop/Εργασίες Παναγιώτης 7/katanemimena/ergasia/5nodes/transactions0.txt'
with open(path, 'r') as file:
    data = file.readlines()

import subprocess
import time
count = 0
t = time.time()
for line in data:
    attributes = line.replace('\n', '').split(' ')
    print(attributes)
    count = count+1
t1 = time.time()
timetotal = t1-t
throughput = count/timetotal
print(throughput)

    # command = 'cli.py t '+ attributes[0] + ' ' + attributes[1]
    # process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    # output, error = process.communicate()