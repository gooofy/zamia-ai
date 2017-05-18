SHELL := /bin/bash

all:	prolog 

kb:
	./ai_cli.py kb_import all

cron:
	./ai_cli.py cron all

prolog:
	./ai_cli.py compile common_sense weather smalltalk radio knowledge

train:
	./ai_cli.py train -n 50000

doc:	README.adoc
	asciidoctor -r asciidoctor-diagram README.adoc

clean:
	./ai_cli.py clean -a all
