SHELL := /bin/bash

all:	doc

prolog:
	./ai_cli.py compile all

train:
	./ai_cli.py train -n 50000

doc:	README.adoc
	asciidoctor -r asciidoctor-diagram README.adoc

clean:
	./ai_cli.py clean -a all
