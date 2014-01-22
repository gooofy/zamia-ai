#!/bin/bash

rm -rf output
mkdir output

#
# audio model
#

./audio-gen-model.py >output/genmodel.log

./lm-export-dict.py 

cp -r /home/ai/voxforge/de/work/acoustic_model_files output/
cp /home/ai/voxforge/de/work/dict.txt output/
cp /home/ai/voxforge/de/lm/dict-julius.txt output/

./audio-stats.py >output/audio-stats.log

# 
# language model
#

./lm-prompts.py
pushd /home/ai/voxforge/de/lm
~/projects/ai/speech/lm-reverse.pl prompts.sent > prompts.rev
ngram-count -order 2 -text prompts.sent -unk -lm german.arpa -vocab wlist.txt
ngram-count -order 4 -text prompts.rev -unk -lm german-rev.arpa -vocab wlist.txt
mkbingram -nlr german.arpa -nrl german-rev.arpa german.bingram
popd

cp /home/ai/voxforge/de/lm/german.bingram output/
cp /home/ai/voxforge/de/lm/dict-julius.txt output/

#
# eval
#

./eval-model.py >output/eval-model.log

#
# export data, db dump
#

pg_dump -U lexicon lexicon_de >output/db.sql
gzip output/db.sql

cp README.md output/readme.txt

./audio-export-csv.py >output/audio-transcripts.csv
./lex-export.py

#
# upload
#

rsync -avP --delete output/ goofy:/var/www/html/voxforge/de

