#!/bin/bash

rm -rf output/phonetisaurus
mkdir output/phonetisaurus

#Align the dictionary
phonetisaurus-align \
    --input=output/dict/dict-xsampa-spaces.txt \
    --ofile=output/phonetisaurus/dict-xsampa.corpus \
    --seq1_del=false

#Train a model
/apps/mitlm-0.4.1/bin/estimate-ngram \
    -t output/phonetisaurus/dict-xsampa.corpus \
    -o 7 \
    -s FixKN \
    -wl output/phonetisaurus/dict-xsampa.arpa

#Convert to FST format
phonetisaurus-arpa2wfst-omega \
    --lm=output/phonetisaurus/dict-xsampa.arpa \
    --ofile=output/phonetisaurus/dict-xsampa.fst


