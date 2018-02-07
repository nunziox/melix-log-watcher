import redis
import time

import matplotlib.pyplot as plt
from matplotlib import animation

# Get an instance of the Redis Server
r = redis.StrictRedis(host='localhost', port=6379, db=0)

def histdata():
	keys = r.keys()
	x = []
	for elem in r.keys():
		elem = r.get(elem)
		if elem is not None:
			x.append(int(elem))
	x.sort(reverse=True)
	return x

def update_data(args):
    ax.clear()
    x=histdata()
    print(x)
    ax.bar([i for i in range(len(x))],x)


fig=plt.figure()
ax = fig.add_subplot(111)
bar=animation.FuncAnimation(fig,update_data,repeat=False,interval=50)
plt.show()
