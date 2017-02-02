SHELL := /bin/bash

all:	prolog 

kb:
	./nlp_cli.py kb_import all

cron:
	./nlp_cli.py cron all

prolog:
	./nlp_cli.py compile common_sense weather smalltalk radio

train:
	./nlp_cli.py train

clean:
	./nlp_cli.py clean -a all
