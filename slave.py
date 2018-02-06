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

# Get an instance of the Redis Server
r = redis.StrictRedis(host='localhost', port=6379, db=0)
r.flushdb()

# Function to sanitize the string:
pattern_to_excludes = [r'\d\d/\d\d-\d\d:\d\d:\d\d\.\d\d\d\s',\
                       r'\d*\.{0,1}\d*',\
                       r'(\[|\]|\<|\>|\:|\.|\-|\(|\)|\{|\}|\,)']

def sanitize(line):
    for elem in pattern_to_excludes:
        line = re.sub(elem, "", line)
    line = re.sub(r'(\s)+', " ", line)
    return line

with sys.stdin as log:
    while(True):
        line = log.readline()
        if line == "": break
        line = sanitize(line)
        print(line)
        words = line.split(" ")
        for word in words:
            if word != "":
                if r.get(word) is None:
                    r.set(word,1)
                else:      
                    r.set(word,int(r.get(word))+1)