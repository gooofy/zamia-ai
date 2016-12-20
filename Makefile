SHELL := /bin/bash

all:	prolog 

prolog:
	./prolog_compile.py data/src/common-sense.pl
	./prolog_compile.py data/src/weather.pl
	./prolog_compile.py data/src/greetings.pl 
	./prolog_compile.py data/src/radio.pl 

weather:
	./kb_weather.py

kb:
	./kb_shell.py graph_clear  -g http://hal.zamia.org
	./kb_shell.py graph_import -g http://hal.zamia.org data/src/kb/weather_base.n3
	./kb_shell.py graph_import -g http://hal.zamia.org data/src/kb/weather_test.n3
	./kb_weather.py
	./kb_shell.py <data/src/kb/dbpedia.kb
	./kb_shell.py dump

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
