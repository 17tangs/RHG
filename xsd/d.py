f = open('hi.txt','r')
l = [s for s in f.read().split('\n') if s != '']
f.close()
l = list(set(l))
l.sort()
k = open('hi.txt', 'w')
for i in l:
    k.write(i + '\n')
k.close()
