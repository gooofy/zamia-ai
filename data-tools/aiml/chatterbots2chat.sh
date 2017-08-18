#!/bin/bash

CHATTERBOTS=~/projects/ai/data/chatterbots

rm -rf bots_en
mkdir bots_en

./aiml2chat.py -o bots_en/square_bear.chat ${CHATTERBOTS}/en/square-bear.co.uk/*.aiml
./aiml2chat.py -o bots_en/proalias.chat    ${CHATTERBOTS}/en/proalias.com/*.aiml
./aiml2chat.py -o bots_en/runabot.chat     ${CHATTERBOTS}/en/runabot.com/*.aiml
./aiml2chat.py -o bots_en/dobby.chat       ${CHATTERBOTS}/en/dobby/*.aiml
./aiml2chat.py -o bots_en/eliza.chat       ${CHATTERBOTS}/en/eliza.aiml
./aiml2chat.py -o bots_en/emmie.chat       ${CHATTERBOTS}/en/aiml-en-us-pandorabots-infotabby/Emmie/*.aiml
./aiml2chat.py -o bots_en/rosie.chat       ${CHATTERBOTS}/en/pandorabots/rosie/lib/aiml/*.aiml
./aiml2chat.py -o bots_en/alice_old.chat   ${CHATTERBOTS}/en/alice/*.aiml
./aiml2chat.py -o bots_en/alice_new.chat   ${CHATTERBOTS}/en/aiml-en-us-foundation-alice/*.aiml

rm -rf bots_de
mkdir bots_de

./aiml2chat.py -o bots_de/alice.chat -n    ${CHATTERBOTS}/de/GermanAIML-2005-05-14/*.aiml

