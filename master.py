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
		x.append(r.get(elem))
	return x

def update_data(args):
    ax.clear()
    x=histdata()
    ax.hist(x, normed=True)


fig=plt.figure()
ax = fig.add_subplot(111)
bar=animation.FuncAnimation(fig,update_data,repeat=False,interval=100)
plt.show()
