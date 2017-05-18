all: semantics.html frames.html

semantics.html:	semantics.adoc
	asciidoctor -r asciidoctor-diagram -a toc semantics.adoc

frames.html:	frames.adoc
	asciidoctor -r asciidoctor-diagram -a toc frames.adoc

clean:
	rm -f *.html *.png

