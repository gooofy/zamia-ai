#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import sys
import re
import os
import StringIO
import ConfigParser
from os.path import expanduser
from gutils import detect_latin1, isgalnum, compress_ws
import random
import datetime

def gen_dirname ():

    today = datetime.date.today()
   
    rstr = '%c%c%c' % (random.randint(97,122),random.randint(97,122),random.randint(97,122))
 
    ds = today.strftime ('%Y%m%d')

    dir_name = '%s-%s-%s' % (vflogin, ds, rstr)

    #print 'dir_name: %s' % dir_name

    return dir_name

random.seed (42)

#
# load config, set up global variables
#

home_path = expanduser("~")

config = ConfigParser.RawConfigParser()
config.read("%s/%s" % (home_path, ".airc"))

vflogin   = config.get("speech", "vflogin")
audiodir  = config.get("speech", "audiodir")

#
# command line
#

if len(sys.argv) != 2:
    print "usage: %s promptsfile" % sys.argv[0]
    sys.exit(1)

promptsfile = sys.argv[1]

#
# generate dir name
#

dir_name = ''
dir_path = ''

while True:

    dir_name = gen_dirname()

    dir_path = '%s/%s' % (audiodir, dir_name)

    print "path: %s" % dir_path

    if not os.path.isdir (dir_path):
        break

#
# generate skeleton
#

os.system ('mkdir %s' % (dir_path))
os.system ('mkdir %s/etc' % (dir_path))
os.system ('mkdir %s/wav' % (dir_path))
os.system ('cp input_files/voxforge-LICENSE %s/LICENSE' % (dir_path))
os.system ('cp input_files/voxforge-README %s/etc/README' % (dir_path))
os.system ('cp input_files/voxforge-GPL %s/etc/GPL_license.txt' % (dir_path))

#
# generate prompts
#

cnt = 1
prefix = 'de5'

outf_poriginal = open ('%s/etc/prompts-original' % dir_path, 'w')
outf_prompts   = open ('%s/etc/PROMPTS' % dir_path, 'w')

for line in open (promptsfile):

    outf_poriginal.write ('%s-%03d %s' % (prefix, cnt, line))

    prompt = compress_ws(line.decode('UTF8').rstrip().upper().replace(',',' ').rstrip('.').replace('!', ' ').replace('"', ' ').replace('?', ' ')).lstrip(' ')

    #print "prompt: '%s'" % prompt

    outf_prompts.write ( ('%s/mfc/%s-%03d %s\n' % (dir_name, prefix, cnt, prompt)).encode('UTF8'))
    
    cnt += 1


outf_poriginal.close()
outf_prompts.close()
