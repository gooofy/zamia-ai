#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import sys
import re
import os
from os.path import expanduser
import StringIO
import ConfigParser
import psycopg2

from gutils import detect_latin1
from phonetic_alphabets import ipa2xsampa, xsampa2ipa, xsampa2xarpabet

def word2label (word):

    if word[0].isdigit():
        return "#" + word

    return word

# transform phonemes so they're proper labels
# \ -> \\
# prepend phonemes starting with digits
def phoneme2label (ph):

    if ph[0].isdigit():
        return 'n'+ph.replace ('\\', '\\\\')

    return ph.replace ('\\', '\\\\')

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

db_server = config.get("speech", "dbserver")
db_name   = config.get("speech", "dbname")
db_user   = config.get("speech", "dbuser")
db_pass   = config.get("speech", "dbpass")

audiodir  = config.get("speech", "audiodir")
mfccdir   = config.get("speech", "mfccdir")
workdir   = config.get("speech", "workdir")
minqual   = config.get("speech", "minqual")

#
# connect to db
#

conn_string = "host='%s' dbname='%s' user='%s' password='%s'" % (db_server, db_name, db_user, db_pass)

conn = psycopg2.connect(conn_string)

cur = conn.cursor()

#
# prepare work dir
#

os.system ("rm -rf %s" % workdir)
os.system ("mkdir %s" % workdir)
os.system ("mkdir %s/mfcc" % workdir)
os.system ("mkdir %s/hmm0" % workdir)
os.system ("mkdir %s/hmm1" % workdir)
os.system ("mkdir %s/hmm2" % workdir)
os.system ("mkdir %s/hmm3" % workdir)
os.system ("mkdir %s/hmm5" % workdir)
os.system ("mkdir %s/hmm6" % workdir)
os.system ("mkdir %s/hmm7" % workdir)
os.system ("mkdir %s/hmm8" % workdir)
os.system ("mkdir %s/hmm9" % workdir)
os.system ("mkdir %s/hmm10" % workdir)
os.system ("mkdir %s/hmm11" % workdir)
os.system ("mkdir %s/hmm12" % workdir)
os.system ("mkdir %s/hmm13" % workdir)
os.system ("mkdir %s/hmm14" % workdir)
os.system ("mkdir %s/hmm15" % workdir)
os.system ("mkdir %s/logs" % workdir)
os.system ('cp -a input_files %s' % workdir)

#
# load dictionary from db
#


print "Loading dict..."

srcdict = {}

cur.execute ("SELECT phonemes, grapheme_id, id FROM pronounciations")

rows = cur.fetchall()
for row in rows:

    ipa = row[0].decode('UTF8')
    gid = row[1]
    pid = row[2]

    cur.execute ("SELECT grapheme FROM graphemes WHERE id=%s", (gid,))

    row2 = cur.fetchone()
    if not row2:
        continue

    word = row2[0].decode('UTF8')

    xs = ipa2xsampa(word, ipa)
    xa = xsampa2xarpabet(word, xs)

    ph = xa + " sp"

    if not word in srcdict:
        srcdict[word] = [ ph ]
    else:
        srcdict[word].append(ph)

print "%d words found in dictionary." % len(srcdict)

print
print "Step 2 - Collect Prompts, generate words.mlf, convert audio"
print

#
# prompts
#

wlist = set()

mlff = open ('%s/words.mlf' % workdir,'w')

mlff.write ('#!MLF!#\n')

#codetrainscp = open ('%s/codetrain.scp' % workdir, 'w')
trainscp = open ('%s/train.scp' % workdir, 'w')

cur.execute ("SELECT filename, transcript FROM audio WHERE quality >= %s ORDER BY quality DESC", (minqual,))

rows = cur.fetchall()
for row in rows:

    cfn = row[0]
    transcript = row[1].decode('UTF8')

    words = re.split ('\s+', transcript)

    #
    # we will only use those prompts for our model that contain only words from our dictionary
    #

    badprompt = False
    for word in words:
        w = re.sub(r"[,.?\-! ;:]", '', word.rstrip()).upper()
        if len(w) == 0:
            continue

        if not w in srcdict:
            print "   Skipping prompt %s because word is not in dict: %s" % (cfn, w)
            badprompt = True
            break

    if badprompt:
        continue

    mlff.write ('"*/%s.lab"\n' % (cfn))
    #trainscp.write ("mfcc/%s.mfc\n" % (cfn))
    trainscp.write ("%s/%s.mfc\n" % (mfccdir, cfn))

    for word in words:

        w = re.sub(r"[,.?\-! ;:]", '', word.rstrip()).upper()
        if len(w) > 0:
            wlist.add(w)
            mlff.write ("%s\n" % word2label(w).encode ('utf-8'))

    mlff.write ('.\n')

mlff.close()
#codetrainscp.close()
trainscp.close()

print
print "%s/words.mlf written." % workdir
print "%s/train.scp written." % workdir
print "Got %d words." % len(wlist)

#wlist_fn = "%s/wlist" % workdir
#
#outf = open (wlist_fn, 'w')
#
#for grapheme in sorted (wlist):
#   outf.write ("%s\n" % grapheme.encode('utf-8'))
#
#outf.close()


print
print "Step 3 - Pronunciation Dictionnary"
print

dict = {}

for word in wlist:
    ps = []
    for p in srcdict[word]:
        ps.append (p)

    dict[word] = ps

dict ['SENT-START'] = [ 'sil' ]
dict ['SENT-END'] = [ 'sil' ]

dict_fn = '%s/dict.txt' % workdir

outf = open (dict_fn, 'w')

for word in sorted (dict.iterkeys()):

    ps = dict[word]
    label = word2label (word)

    prob = 1.0 / len(ps)

    for p in ps:
        outf.write ("%-20s [%s] %g %s\n" % (label.encode('utf-8'), word.encode('utf-8'), prob, p.encode('utf-8')))

outf.close()

print '%s/dict.txt written.' % workdir

print
print "Step 4 - Monophones"
print

monophones = set()

for word in dict:

    phss = dict[word]

    for phs in phss:
        for ph in phs.split(' '):
            if len(ph) > 0:
                monophones.add(ph)

print "Got %d monophones." % len(monophones)

monophones0_fn = "%s/monophones0" % workdir
monophones1_fn = "%s/monophones1" % workdir

outf0 = open (monophones0_fn, 'w')
outf1 = open (monophones1_fn, 'w')
for p in monophones:
    if p != "sp":
        outf0.write ("%s\n" % p)
    outf1.write ("%s\n" % p)
outf0.close()
outf1.close()

print "%s/monophones0 written." % workdir
print "%s/monophones1 written." % workdir

print
print "Step 5 - Creating Transcription Files"
print

systemlog ('HLEd -A -D -T 1 -l \'*\' -d dict.txt -i phones0.mlf input_files/mkphones0.led words.mlf', 'Step5_HLEd_phones0.log')

systemlog ('HLEd -A -D -T 1 -l \'*\' -d dict.txt -i phones1.mlf input_files/mkphones1.led words.mlf', 'Step5_HLEd_phones1.log')

print
print "Step 6 - Creating Monophones"
print

systemlog ('HCompV -A -D -T 1 -C ./input_files/config -f 0.01 -m -S train.scp -M hmm0 input_files/proto', 'Step6_HCompV_hmm0.log')

hmmdefs = open ('%s/hmm0/hmmdefs' % workdir, 'w')
for p in monophones:
    if p == 'sp':
        continue

    proto = open ('%s/hmm0/proto' % workdir)
    linecnt = 0
    for line in proto:
        linecnt += 1
        if linecnt < 4:
            continue

        hmmdefs.write (line.replace ('proto', p))

    proto.close()

hmmdefs.close()

print '%s/hmm0/hmmdefs written.' % workdir

#os.system ('cd %s ; for WORD in `cat monophones0`; do tail -n 28 hmm0/proto | sed s/~h\ \"proto\"/~h\ \"$WORD\"/g >> hmm0/hmmdefs; done' % (workdir))
os.system ('cd %s ; head -n 3 hmm0/proto > hmm0/macros' % (workdir))
os.system ('cd %s ; cat hmm0/vFloors >> hmm0/macros' % (workdir))

print "making hmm1"
systemlog ('HERest -A -D -T 1 -C ./input_files/config -I phones0.mlf -t 250.0 150.0 1000.0 -S train.scp -H hmm0/macros -H hmm0/hmmdefs -M hmm1 monophones0', 'Step6_HERest_hmm1.log')

print "making hmm2"
systemlog ('HERest -A -D -T 1 -C ./input_files/config -I phones0.mlf -t 250.0 150.0 1000.0 -S train.scp -H hmm1/macros -H hmm1/hmmdefs -M hmm2 monophones0', 'Step6_HERest_hmm2.log')

print "making hmm3"
systemlog ('HERest -A -D -T 1 -C ./input_files/config -I phones0.mlf -t 250.0 150.0 1000.0 -S train.scp -H hmm2/macros -H hmm2/hmmdefs -M hmm3 monophones0', 'Step6_HERest_hmm3.log')

print
print "Step 7 - Fixing the Silence Model"
print

print "making hmm4"
os.system ('cd %s ; cp -a hmm3 hmm4 ' % (workdir))

infile = open ("%s/hmm3/hmmdefs" % workdir)
outfile = open ("%s/hmm4/hmmdefs" % workdir, "w")
sp = StringIO.StringIO()

linecnt = -1
for line in infile:

    if "~h \"sil\"" in line:
        linecnt = 0
    elif "~h" in line:
        linecnt = -1

    outfile.write (line)
    
    if linecnt >= 0:
        if linecnt >= 10 and linecnt <= 14:
            sp.write (line)

        linecnt += 1

outfile.write ("~h \"sp\"\n")
outfile.write ("<BEGINHMM>\n")
outfile.write ("<NUMSTATES> 3\n")
outfile.write ("<STATE> 2\n")
outfile.write (sp.getvalue())
outfile.write ("<TRANSP> 3\n")
outfile.write (" 0.0 1.0 0.0\n")
outfile.write (" 0.0 0.9 0.1\n")
outfile.write (" 0.0 0.0 0.0\n")
outfile.write ("<ENDHMM>\n")

outfile.close()
infile.close()

print "making hmm5"
systemlog ('HHEd -A -D -T 1 -H hmm4/macros -H hmm4/hmmdefs -M hmm5 input_files/sil.hed monophones1', 'Step7_HHEd_hmm5.log')

systemlog ('HERest -A -D -T 1 -C ./input_files/config  -I phones1.mlf -t 250.0 150.0 3000.0 -S train.scp -H hmm5/macros -H hmm5/hmmdefs -M hmm6 monophones1', 'Step7_HERest_hmm6.log')

print "making hmm6"
systemlog ('HERest -A -D -T 1 -C ./input_files/config  -I phones1.mlf -t 250.0 150.0 3000.0 -S train.scp -H hmm6/macros -H hmm6/hmmdefs -M hmm7 monophones1', 'Step7_HERest_hmm7.log')

print
print "Step 8 - Realigning the Training Data"
print

print "making hmm7"
os.system ('cd %s ; cat dict.txt > dict1.txt' % (workdir))
os.system ('cd %s ; echo "silence  []  sil" >> dict1.txt' % (workdir))
systemlog ('HVite -A -D -T 1 -l \'*\' -o SWT -b silence -C ./input_files/config -H hmm7/macros -H hmm7/hmmdefs -i aligned.mlf -m -t 250.0 150.0 1000.0 -y lab -a -I words.mlf -S train.scp dict1.txt monophones1', 'Step8_HVite.log')

#print "***Please review the following HVite output***:"
#os.system ('cat %s/logs/Step8_HVite.log' % workdir)

print "making hmm8"
systemlog ('HERest -A -D -T 1 -C ./input_files/config -I aligned.mlf -t 250.0 150.0 3000.0 -S train.scp -H hmm7/macros -H hmm7/hmmdefs -M hmm8 monophones1', 'Step8_HERest_hmm8.log')

print "making hmm9"
systemlog ('HERest -A -D -T 1 -C ./input_files/config -I aligned.mlf -t 250.0 150.0 3000.0 -S train.scp -H hmm8/macros -H hmm8/hmmdefs -M hmm9 monophones1', 'Step8_HERest_hmm9.log')

print
print "Step 9 - Making Triphones from Monophones"
print

print "making triphones"
systemlog ('HLEd -A -D -T 1 -n triphones1 -l \'*\' -i wintri.mlf ./input_files/mktri.led aligned.mlf', 'Step9_HLed.log')

# maketrihed - make a .hed script to clone monophones in a phone list

outf = open ('%s/mktri.hed' % workdir, 'w')
outf.write ('CL triphones1\n')
for p in monophones:
    outf.write ('TI T_%s {(*-%s+*,%s+*,*-%s).transP}\n' % (p, p, p, p))
    
outf.close()

print "making hmm10"
systemlog ('HHEd -A -D -T 1 -H hmm9/macros -H hmm9/hmmdefs -M hmm10 mktri.hed monophones1', 'Step9_HHEd_hmm10.log')
print "making hmm11"
systemlog ('HERest  -A -D -T 1 -C ./input_files/config -I wintri.mlf -t 250.0 150.0 3000.0 -S train.scp -H hmm10/macros -H hmm10/hmmdefs -M hmm11 triphones1', 'Step9_HERest_hmm10.log')
print "making hmm12"
systemlog ('HERest  -A -D -T 1 -C ./input_files/config -I wintri.mlf -t 250.0 150.0 3000.0 -s stats -S train.scp -H hmm11/macros -H hmm11/hmmdefs -M hmm12 triphones1', 'Step9_HERest_hmm11.log')

print
print "Step 10 - Making Tied-State Triphones"
print

systemlog ('HDMan -A -D -T 1 -b sp -n fulllist -g ./input_files/global.ded dict-tri dict.txt', 'Step10_HDMan.log')
os.system ('cd %s ; cat fulllist > fulllist-original ' % (workdir))

# cat ./interim_files/triphones1 >> ./interim_files/fulllist
# perl fixfulllist.pl ./interim_files/fulllist ./interim_files/fulllist1
# cat ./interim_files/fulllist1 > ./interim_files/fulllist
# rm ./interim_files/fulllist1

fout = open ('%s/fulllist' % workdir, 'w')
seen = set()
fin = open ('%s/fulllist-original' % workdir)
for line in fin:
    ph = line.lstrip().rstrip()
    if ph in seen:
        continue
    seen.add(ph)
    fout.write("%s\n" % ph)
fin.close()
fin = open ('%s/triphones1' % workdir)
for line in fin:
    ph = line.lstrip().rstrip()
    if ph in seen:
        continue
    seen.add(ph)
    fout.write("%s\n" % ph)
fin.close()
fout.close()

os.system ('cd %s ; cat ./input_files/tree1.hed >tree.hed' % (workdir))

fout = open ('%s/tree.hed' % workdir, 'a')
COMMAND='TB'
THRESHOLD='350'

fin = open ('%s/monophones0' % workdir)
for line in fin:
    ph = line.rstrip().lstrip()
    fout.write("TB 350 \"ST_%s_2_\" {(\"%s\",\"*-%s+*\",\"%s+*\",\"*-%s\").state[2]}\n" % (ph,ph,ph,ph,ph))
fin.close()
fin = open ('%s/monophones0' % workdir)
for line in fin:
    ph = line.rstrip().lstrip()
    fout.write("TB 350 \"ST_%s_3_\" {(\"%s\",\"*-%s+*\",\"%s+*\",\"*-%s\").state[3]}\n" % (ph,ph,ph,ph,ph))
fin.close()
fin = open ('%s/monophones0' % workdir)
for line in fin:
    ph = line.rstrip().lstrip()
    fout.write("TB 350 \"ST_%s_4_\" {(\"%s\",\"*-%s+*\",\"%s+*\",\"*-%s\").state[4]}\n" % (ph,ph,ph,ph,ph))
fin.close()

fout.write (' \n')
fout.write ('TR 1\n')
fout.write (' \n')
fout.write ('AU "fulllist" \n')
fout.write ('CO "tiedlist" \n')
fout.write (' \n')
fout.write ('ST "trees" \n')

fout.close()

print "making hmm13"
systemlog ('HHEd -A -D -T 1 -H hmm12/macros -H hmm12/hmmdefs -M hmm13 tree.hed triphones1', 'Step10_HHed_hmm13.log')

print "making hmm14"
systemlog ('HERest -A -D -T 1 -T 1 -C ./input_files/config -I wintri.mlf -t 250.0 150.0 3000.0 -s stats -S train.scp -H hmm13/macros -H hmm13/hmmdefs -M hmm14 tiedlist', 'Step10_HERest_hmm14.log')

print "making hmm15"
systemlog ('HERest -A -D -T 1 -T 1 -C ./input_files/config -I wintri.mlf -t 250.0 150.0 3000.0 -s stats -S train.scp -H hmm14/macros -H hmm14/hmmdefs -M hmm15 tiedlist', 'Step11_HERest_hmm15.log')

os.system ('cd %s ; rm -rf acoustic_model_files' % (workdir))
os.system ('cd %s ; mkdir acoustic_model_files' % (workdir))
os.system ('cd %s ; cp hmm15/hmmdefs acoustic_model_files' % (workdir))
os.system ('cd %s ; cp tiedlist acoustic_model_files' % (workdir))

print
print "*** completed ***"
print

print 'Final model copied to: %s/acoustic_model_files' % (workdir)
print

