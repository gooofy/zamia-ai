#!/bin/bash

CHATTERBOTS=/home/bofh/projects/ai/data/chatterbots

rm -r bots
mkdir bots

./aiml2csv.py -o bots/eliza.csv       -l en ${CHATTERBOTS}/en/eliza.aiml 
./aiml2csv.py -o bots/square_bear.csv -l en ${CHATTERBOTS}/en/square-bear.co.uk/*.aiml
./aiml2csv.py -o bots/proalias.csv    -l en ${CHATTERBOTS}/en/proalias.com/*.aiml
./aiml2csv.py -o bots/runabot.csv     -l en ${CHATTERBOTS}/en/runabot.com/*.aiml
./aiml2csv.py -o bots/dobby.csv       -l en ${CHATTERBOTS}/en/dobby/*.aiml
./aiml2csv.py -o bots/emmie.csv       -l en ${CHATTERBOTS}/en/aiml-en-us-pandorabots-infotabby/Emmie/*.aiml
./aiml2csv.py -o bots/rosie.csv       -l en ${CHATTERBOTS}/en/pandorabots/rosie/lib/aiml/*.aiml
./aiml2csv.py -o bots/alice_old.csv   -l en ${CHATTERBOTS}/en/alice/*.aiml
./aiml2csv.py -o bots/alice_new.csv   -l en ${CHATTERBOTS}/en/aiml-en-us-foundation-alice/*.aiml

sort -u bots/*.csv >all_bots.csv

