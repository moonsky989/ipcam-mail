#!/usr/bin/env python

import os
import time
import glob
from shutil import copyfile

year = time.strftime("%y") 
month = time.strftime("%m")
day = time.strftime("%d")
hour = time.strftime("%H")

for x in range(1, 6):
    path = '/media/exstorage/zoneminder/events/' + str(x) + '/' + year + '/' + month + '/' + day + '/' + hour
    print path
    filelist = glob.glob("/usr/lib/checkmail/zoneminder/images/" + str(x) + "/*.jpg")
    for f in filelist:
        os.remove(f)
 
    newest = max(glob.iglob(path + '/*/*/*.jpg'), key=os.path.getctime)
    print newest
    copyfile(newest, '/usr/lib/checkmail/zoneminder/images/' + str(x) + '/camera' + str(x) + '.jpg') 
