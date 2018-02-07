"""
__author__: Nunzuio Meli
The algorithm store an histogram of your log files.
"""

import sys
import redis
import re

#
# Constants
#
APP_NAME= "POC"

#
# Tuning parameters
#
observation_window = 1000 # lines

#
# Variables
#
count  = 0

# Get an instance of the Redis Server
r = redis.StrictRedis(host='localhost', port=6379, db=0)
r.flushdb()

# Function to sanitize the string:
pattern_to_excludes = (r'\d\d/\d\d-\d\d:\d\d:\d\d\.\d\d\d\s',\
                       r'\d*\.{0,1}\d*',\
                       r'(\[|\]|\<|\>|\:|\.|\-|\(|\)|\{|\}|\,|\/)')

words_to_exlude = (r'QUEUE',\
                   r'CHILD',\
                   r'QUEUE_CONTROL')

def sanitize(line):
    for elem in set(pattern_to_excludes).union(words_to_exlude):
        line = re.sub(elem, "", line)
    line = re.sub(r'(\s)+', "", line)
    return line

buff_dict = {}

with sys.stdin as log:
    while(True):
        
        line = log.readline()
        if line == "": break
        line = sanitize(line)
        print(line)
        if line != "":
            if line not in buff_dict:
              buff_dict[line] = 1
            else:      
              buff_dict[line] = buff_dict[line] + 1
        
        count = (count + 1) % observation_window

        if count == 0:
            r.flushdb()
            for line in buff_dict:
                r.set(line,buff_dict[line])
            buff_dict = {}