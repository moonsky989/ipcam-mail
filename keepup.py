#!/usr/bin/env python

import sys
import time
import subprocess

#use python keepup.py ./process.py

cmd = ' '.join(sys.argv[1:])

def start_subprocess():
    return subprocess.Popen(cmd, shell=True)

p = start_subprocess()

while True:
    
    res = p.poll()
    if res is not None:
        print p.pid, 'was killed, restarting it'
        p = start_subprocess()

    time.sleep(1)
