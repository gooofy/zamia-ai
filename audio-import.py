#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import sys
import re
import os
import StringIO
import ConfigParser
from os.path import expanduser
from gutils import detect_latin1, isgalnum, run_command
import psycopg2

def canon_fn (fn):

    return fn[:250].replace('/', '_')

#
# load config, set up global variables
#

home_path = expanduser("~")

config = ConfigParser.RawConfigParser()
config.read("%s/%s" % (home_path, ".airc"))

db_server = config.get("speech", "dbserver")
db_name   = config.get("speech", "dbname")
db_user   = config.get("speech", "dbuser")
db_pass   = config.get("speech", "dbpass")

audiodir  = config.get("speech", "audiodir")
mfccdir   = config.get("speech", "mfccdir")

#
# connect to db
#

conn_string = "host='%s' dbname='%s' user='%s' password='%s'" % (db_server, db_name, db_user, db_pass)

conn = psycopg2.connect(conn_string)

cur = conn.cursor()

#
# iterate over audiodir subdirectories, collect prompts, convert audio
#

cfns = set()

for submission in os.listdir (audiodir):

    subdir = "%s/%s" % (audiodir, submission)

    if not os.path.isdir(subdir):
        continue

    prompts = "%s/etc/PROMPTS" % subdir

    encoding = 'utf-8'
    if detect_latin1(prompts):
        encoding = 'latin-1'


    promptsfile = open (prompts)
    for line in promptsfile:
        parts = re.split ('\s+', line.decode(encoding))

        # filename

        fn = parts[0]
        fn = fn [ fn.rindex('/')+1: ]
        cfn = canon_fn ("%s_%s" % (submission, fn))
        #print "Filename: %s, canon: %s" % (fn, cfn)

        if cfn in cfns:
            print "ERROR: filename not unique: %s" % cfn
            sys.exit(1)
        cfns.add(cfn)

        # convert audio if not done yet

        mfccfilename = "%s/%s.mfc" % (mfccdir, cfn)

        if not os.path.isfile (mfccfilename):

            wavfilename  = "%s/wav/%s.wav" % (subdir, fn)

            if not os.path.isfile (wavfilename):
                # flac ?
                flacfilename  = "%s/flac/%s.flac" % (subdir, fn)
        
                if not os.path.isfile (flacfilename):
                    print "   WAV file '%s' does not exist, neither does FLAC file '%s' => skipping submission." % (wavfilename, flacfilename)
                    continue

                print "%-20s: converting %s => %s" % (cfn, flacfilename, '/tmp/foo.wav')
                os.system ("flac -s -f -d '%s' -o /tmp/foo.wav" % flacfilename)
                print "%-20s: converting %s => %s" % (cfn, '/tmp/foo.wav', mfccfilename)
                os.system ("HCopy -T 0 -C input_files/wav_config /tmp/foo.wav '%s'" % mfccfilename)
            
            else:

                print "%-20s: converting %s => %s" % (cfn, wavfilename, mfccfilename)
                os.system ("HCopy -T 0 -C input_files/wav_config '%s' '%s'" % (wavfilename, mfccfilename))

        # db entry

        pstr = ' '.join(parts[1:]).upper()

        cur.execute ("SELECT id FROM submissions WHERE cfn=%s", (cfn,))

        if not cur.fetchone():
           
            # compute num samples

            num_samples = 0
            for line in run_command ( ['HList', '-h', '-e', '0', mfccfilename] ):

                m = re.match (r"^  Num Samples:\s+(\d+)\s+File Format:   HTK", line)
                if not m:
                    continue

                num_samples = int (m.group(1))
                break
            
            print "%-20s: adding submission entry, %6d samples, prompt is: '%s'" % (cfn, num_samples, pstr)

            cur.execute ("INSERT INTO submissions (dir, audiofn, cfn, prompt, comment, numsamples) VALUES (%s, %s, %s, %s, '', %s)", (submission, fn, cfn, pstr, num_samples))


conn.commit()


