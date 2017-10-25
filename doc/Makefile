all: aiprolog.html frames.html

aiprolog.html:	aiprolog.adoc
	asciidoctor -r asciidoctor-diagram -a toc aiprolog.adoc

frames.html:	frames.adoc
	asciidoctor -r asciidoctor-diagram -a toc frames.adoc

clean:
	rm -f *.html *.png

