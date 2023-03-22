diff = 4
hash = 983280000
x = str(hash)
check = ''
for i in range (diff):
    check = check+'0'
print(check)
print(x[-diff:])
if x[-diff:] == check:
    print (True)
else:
    print(False)


