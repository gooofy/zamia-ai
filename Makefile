SHELL := /bin/bash

all:	README.html README.md dist

%.html: %.adoc
	asciidoctor -r asciidoctor-diagram -a toc $<

README.md: README.adoc
	asciidoc -b docbook README.adoc
	iconv -t utf-8 README.xml | pandoc -f docbook -t markdown_strict | iconv -f utf-8 > README.md

dist:	README.md
	python setup.py sdist
	python setup.py bdist_wheel --universal

upload:
	twine upload dist/*

clean:
	rm -f *.html 
	rm -rf dist build  zamia_ai.egg-info  README.md  README.xml 

