#!/bin/bash

#julius -input pulseaudio -smpFreq 48000 -h output/acoustic_model_files/hmmdefs -hlist output/acoustic_model_files/tiedlist -nlr output/german.lm -v output/dict-julius.txt

#julius -input pulseaudio -smpFreq 48000 -h output/acoustic_model_files/hmmdefs -hlist output/acoustic_model_files/tiedlist -d output/german.bingram -v output/dict-julius.txt -silhead '<s>' -siltail '</s>' 

julius -input file -filelist files.txt -smpFreq 48000 -h output/acoustic_model_files/hmmdefs -hlist output/acoustic_model_files/tiedlist -d output/german.bingram -v output/dict-julius.txt -silhead '<s>' -siltail '</s>' 

#julius -input pulseaudio -smpFreq 48000 -h output/acoustic_model_files/hmmdefs -hlist output/acoustic_model_files/tiedlist -d output/german.bingram -v output/dict-julius.txt -silhead '<s>' -siltail '</s>' -gprune safe -lmp 9.0 -9.0 -lmp2 9.0 -9.0

