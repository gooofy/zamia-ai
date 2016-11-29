SHELL := /bin/bash

all:	prolog 

prolog:
	./prolog_compile.py data/src/common-sense.pl
	./prolog_compile.py data/src/weather.pl
	# ./prolog_compile.py data/src/greetings.pl 
	# ./prolog_compile.py data/src/radio.pl 

weather:
	./kb_weather.py

nlp_train:
	./nlp_train_keras.py

kaldi:
	rm -rf data/dst/speech/de/kaldi
	./speech_kaldi_export.py
	pushd data/dst/speech/de/kaldi && ./run.sh && popd

sphinx:
	rm -rf data/dst/speech/de/cmusphinx
	./speech_sphinx_export.py 
	pushd data/dst/speech/de/cmusphinx && ./sphinx-run.sh && popd
	
sequitur:
	rm -rf data/dst/speech/de/sequitur/
	./speech_sequitur_export.py
	./speech_sequitur_train.sh

stats:
	./speech_stats.py

clean:
	./prolog_compile.py -C
	rm -rf data/dst/*
