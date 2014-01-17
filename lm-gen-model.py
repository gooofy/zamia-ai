#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import sys
import re
import os
from os.path import expanduser
import StringIO
import ConfigParser
import psycopg2

# simple wrapper around os.system, will 
# - cd to workdir first
# - print out command to stdout
# - redirect output to logfile
def systemlog (cmd, logfile):

    lcmd = 'cd %s ; %s > logs/%s' % (workdir, cmd, logfile)
    print lcmd

    res = os.system (lcmd)

    if res != 0:
        sys.exit(res)

print
print "Step 1 - Preparation"
print

#
# load config, set up global variables
#

home_path = expanduser("~")

config = ConfigParser.RawConfigParser()
config.read("%s/%s" % (home_path, ".airc"))

workdir   = config.get("speech", "lmworkdir")

os.system ('cd %s ; rm -rf german.0 ; mkdir german.0' % (workdir))
os.system ('cd %s ; rm -rf german.1 ; mkdir german.1' % (workdir))
os.system ('cd %s ; rm -rf model ; mkdir model' % (workdir))
os.system ('cd %s ; rm -rf logs ; mkdir logs' % (workdir))

systemlog ('LNewMap -f WFC german empty.wmap', 'Step1_LNewMap.log')

print
print "Step 2 - Initial ngrams"
print

systemlog ('LGPrep -T 1 -a 1000000 -b 500000 -d german.0 -n 3 -s "German Model" empty.wmap *.sent', 'Step2_LGPrep.log')

print
print "Step 3 - Sequencing"
print

systemlog ('LGCopy -T 1 -b 500000 -d german.1 german.0/wmap german.0/gram.*', 'Step3_LGCopy.log')

print
print "Step 4 - Mapping OOV words"
print

systemlog ('LGCopy -T 1 -o -m model/model.wmap -b 500000 -d model -w wlist.txt german.0/wmap german.1/data.*', 'Step4_LGCopy.log')

print
print "Step 5 - Language model generation"
print


systemlog ('LFoF -T 1 -n 4 -f 32 model/model.wmap model/model.fof german.1/data.* model/data.*', 'Step4_LGCopy.log')

