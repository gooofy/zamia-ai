Audio Model
===========

Record Audio, Create Dictionary Entries, Review + Transcribe
------------------------------------------------------------

record:

    ./audio-record-init.py /home/ai/corpora/de/chat/conversation_starters.txt 
    ./audio-record.py /home/ai/voxforge/de/audio/guenter-20131123-qah

import into db:

    ./audio-import.py

check dictionary:

    [guenter@dagobert speech]$ ./lex-todo.py 
    loading transcripts... done. 9891 unique words found.
    Looking up words in dictionary... done

    STATS: 32 of 9891 words have no entry yet => 99% done.

add missing pronounciations:

    ./lex-edit.py `./lex-prompts.py`

transcribe, rate:

    ./audio-transcribe.py 
    point web browser to: http://localhost:8000/


Compute Model
-------------

    ./audio-gen-model.py

    [guenter@dagobert speech]$ ./audio-gen-model.py
    
    Step 1 - Preparation
    
    Loading dict...
    30222 words found in dictionary.
    
    Step 2 - Collect Prompts, generate words.mlf, convert audio
    
    ...
    
    Step 10 - Making Tied-State Triphones
    
    cd /home/ai/voxforge/de/work ; HDMan -A -D -T 1 -b sp -n fulllist -g ./input_files/global.ded dict-tri dict.txt > logs/Step10_HDMan.log
    making hmm13
    cd /home/ai/voxforge/de/work ; HHEd -A -D -T 1 -H hmm12/macros -H hmm12/hmmdefs -M hmm13 tree.hed triphones1 > logs/Step10_HHed_hmm13.log
    making hmm14
    cd /home/ai/voxforge/de/work ; HERest -A -D -T 1 -T 1 -C ./input_files/config -I wintri.mlf -t 250.0 150.0 3000.0 -s stats -S train.scp -H hmm13/macros -H hmm13/hmmdefs -M hmm14 tiedlist > logs/Step10_HERest_hmm14.log
    making hmm15
    cd /home/ai/voxforge/de/work ; HERest -A -D -T 1 -T 1 -C ./input_files/config -I wintri.mlf -t 250.0 150.0 3000.0 -s stats -S train.scp -H hmm14/macros -H hmm14/hmmdefs -M hmm15 tiedlist > logs/Step11_HERest_hmm15.log
    
    *** completed ***

    Final model copied to: /home/ai/voxforge/de/work/acoustic_model_files

collect final model:

    cp /home/ai/voxforge/de/work/acoustic_model_files/* /home/guenter/projects/ai/speech/output/acoustic_model_files
    ...
    cp /home/ai/voxforge/de/work/dict.txt /home/guenter/projects/ai/speech/output/


Language Models
===============

SRILM Language Model Generation
-------------------------------

workdir: /home/ai/voxforge/de/lm

References:
* http://julius.sourceforge.jp/forum/viewtopic.php?f=5&t=132&p=783&hilit=reverse+model#p783
* http://www.speech.sri.com/projects/srilm/download.html
* http://trulymadlywordly.blogspot.de/2011/03/creating-text-corpus-from-wikipedia.html
* HTK Book

SRILM Installation:
* unpack
* export SRILM=`pwd`
* make MACHINE_TYPE=i686-m64-rhel World

Download from http://www.statmt.org/europarl/

Export dictionary, generate wordlist:

    ./lm-export-dict.py

Generate corpus:

    ./lm-europarl.py
    ./lm-prompts.py 

Generate reverse corpus:

    ~/projects/ai/speech/lm-reverse.pl conversation_starters.sent >conversation_starters.rev
    ~/projects/ai/speech/lm-reverse.pl europarl.sent >europarl.rev
    ~/projects/ai/speech/lm-reverse.pl prompts.sent > prompts.rev

Train forward 2-gram in ARPA format:

    #ngram-count -order 2 -text prompts.sent -text conversation_starters.sent -text europarl.sent -unk -lm german.arpa -vocab wlist.txt
    ngram-count -order 2 -text prompts.sent -unk -lm german.arpa -vocab wlist.txt

Train backward N-gram:

    #ngram-count -order 4 -text prompts.rev -text conversation_starters.rev -text europarl.rev -unk -lm german-rev.arpa -vocab wlist.txt
    ngram-count -order 4 -text prompts.rev -unk -lm german-rev.arpa -vocab wlist.txt

Combine the two ARPA N-grams and convert into binary format for Julius:

    mkbingram -nlr german.arpa -nrl german-rev.arpa german.bingram

collect results:

    cp /home/ai/voxforge/de/lm/german.bingram /home/guenter/projects/ai/speech/output/
    cp /home/ai/voxforge/de/lm/dict-julius.txt /home/guenter/projects/ai/speech/output/

test julius:

    ./run-julius.sh

if fail:

    ./run-julius.sh &>t.log
    ./lm-export-dict.py t.log
    cp /home/ai/voxforge/de/lm/dict-julius.txt /home/guenter/projects/ai/speech/output/


MITLM Language Model Generation
-------------------------------

workdir: /home/ai/voxforge/de/lm

References:

* http://trulymadlywordly.blogspot.de/2011/03/creating-text-corpus-from-wikipedia.html
* HTK Book

Download from http://www.statmt.org/europarl/

    ./lm-europarl.py
    ./lm-export-dict.py

estimate-ngram -vocab wlist.txt -text europarl.sent -write-lm german.lm

    ./lm-collect-sentences.py /home/ai/corpora/de/chat/conversation_starters.txt > /home/ai/voxforge/de/lm/conversation_starters.sent

    estimate-ngram -vocab wlist.txt -text conversation_starters.sent,europarl.sent -write-lm german.lm

    cp /home/ai/voxforge/de/lm/german.lm /home/guenter/projects/ai/speech/output/
    cp /home/ai/voxforge/de/lm/dict-julius.txt /home/guenter/projects/ai/speech/output/


test julius:

    ./run-julius.sh

if fail:

    ./run-julius.sh &>t.log
    ./lm-export-dict.py t.log


Grammar Generation:
===================

edit grammar/starter.grammar
     grammar/starter.voca

cd grammar
[guenter@dagobert grammar]$ mkdfa.pl starter
starter.grammar has 3 rules
starter.voca    has 8 categories and 8 words
---
Now parsing grammar file
Now modifying grammar to minimize states[-1]
Now parsing vocabulary file
Now making nondeterministic finite automaton[11/11]
Now making deterministic finite automaton[11/11] 
Now making triplet list[11/11]
8 categories, 11 nodes, 11 arcs
-> minimized: 9 nodes, 9 arcs
---
generated: starter.dfa starter.term starter.dict




Running Julius
==============

    julius -input pulseaudio -h output/acoustic_model_files/hmmdefs -hlist output/acoustic_model_files/tiedlist -nlr output/german.lm -v output/dict-julius.txt

    julius -input file -filelist files.txt -h output/acoustic_model_files/hmmdefs -hlist output/acoustic_model_files/tiedlist -dfa grammar/starter.dfa -v grammar/starter.dict -smpFreq 48000

    julius -input rawfile -realtime -filelist $sndfile -h $mmf -gramlist julius/gramlist.txt -multipath -lv 2500 -rejectshort 70 -headmargin 50 -tailmargin 50 -progout -sp sil -b 0

