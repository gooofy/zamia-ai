all: aiprolog.html frames.html

aiprolog.html:	aiprolog.adoc
	asciidoctor -r asciidoctor-diagram -a toc aiprolog.adoc

frames.html:	frames.adoc
	asciidoctor -r asciidoctor-diagram -a toc frames.adoc

what_to_say.html:	what_to_say.adoc
	asciidoctor -r asciidoctor-diagram -a toc what_to_say.adoc

clean:
	rm -f *.html *.png

