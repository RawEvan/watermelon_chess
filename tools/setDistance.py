# coding:utf-8
# watermelon chess
import json
f = open('../distance.txt', 'wb')
distance = [[0] * 21] * 21
rec = True
p1 = 1
while p1 >= 0:
    if rec:
        p1 = int(raw_input())
        rec = False
        print 'rec p1:' + str(p1)
    else:
        p2 = int(raw_input())
        rec = True
        distance[p1][p2] = 1
        distance[p2][p1] = 1
        print 'rec p2:' + str(p2)
        for x in distance:
            print x
f.write(json.dumps(distance))
print 'write!'
f.close()
