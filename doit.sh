#!/bin/bash

rm -rf output
mkdir output
mkdir output/logs

#
# audio model
#

./audio-gen-model.py >output/logs/genmodel.log

./lm-export-dict.py 

cp -r /home/ai/voxforge/de/work/acoustic_model_files output/
cp /home/ai/voxforge/de/work/dict.txt output/
cp /home/ai/voxforge/de/lm/dict-julius.txt output/
cp /home/ai/voxforge/de/work/logs/Step* output/logs

./audio-stats.py >output/audio-stats.txt

# 
# language model
#

./lm-prompts.py
pushd /home/ai/voxforge/de/lm
~/projects/ai/speech/lm-reverse.pl prompts.sent > prompts.rev
ngram-count -order 2 -text prompts.sent -unk -kndiscount1 -kndiscount2 -kndiscount3 -lm german.arpa -vocab wlist.txt
ngram-count -order 4 -text prompts.rev -unk -kndiscount1 -kndiscount2 -kndiscount3 -lm german-rev.arpa -vocab wlist.txt
#ngram-count -order 2 -text prompts.sent -unk -lm german.arpa -vocab wlist.txt
#ngram-count -order 4 -text prompts.rev -unk -lm german-rev.arpa -vocab wlist.txt
mkbingram -nlr german.arpa -nrl german-rev.arpa german.bingram
popd

cp /home/ai/voxforge/de/lm/german.bingram output/
cp /home/ai/voxforge/de/lm/dict-julius.txt output/

#
# eval
#

./eval-model.py >output/logs/eval-lm.log

#
# grammar / dfa
#

./grammar-gen.py
pushd output
mkdfa.pl eval >output/logs/mkdfa.log
popd

#
# eval grammar
#

./eval-grammar.py >output/logs/eval-grammar.log

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

#rsync -avP --delete output/ goofy:/var/www/html/voxforge/de

