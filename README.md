# Note

If you're looking for the scripts that I am using to build my VoxForge models, those
are over at [https://github.com/gooofy/speech](https://github.com/gooofy/speech).

# NLP

Various scripts that one day could form a complete A.I. system. 

Right now the rough idea is to use a custom prolog system at the core for logic reasoning,
an RDF triple store for holding data and a seq2seq model to map natural language to prolog.

```
natural language -> [ tokenizer ] -> tokens -> [ seq2seq model ] -> prolog -> [ prolog engine ] -> say/action preds
```

One of the key features of the current setup is the way training data is stored/generated.
I am using a modularized approach here (see the modules/ directory for humble beginnings of this)
where I store snippets of natural language which uses a macro system for somewhat rule-based
generation of language examples along with RDF triples for data and prolog code to execute it

Links
=====

* [Code](https://github.com/gooofy/nlp "github")

Requirements
============

*Note*: very incomplete.

* Python 2.7 with nltk, numpy, ...
* tensorflow
* from my other repositories: py-nltools, rdflib-sqlalchemy2

Setup Notes
===========

Just some rough notes on the environment needed to get these scripts to run. This is in no way a complete set of
instructions, just some hints to get you started.

`~/.nlprc`:

```ini
[db]
url                 = postgresql://semantics:password@dagobert:5432/nlp

[semantics]
modules             = common_sense, weather, smalltalk, radio
server_host         = dagobert
server_port         = 8302

[weather]
api_key             = xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
city_id             = 2825297
city_pred           = stuttgart
```

Language Model
==============

dump sentences from training data for LM generation:

```bash
./nlp_cli.py utterances 
```

or to dump out a set of 20 random utterances which contain words not covered by the dictionary:

```bash
./nlp_cli.py utterances -d ../speech/data/src/speech/de/dict.ipa -n 20
```

License
=======

My own scripts as well as the data I create is LGPLv3 licensed unless otherwise noted in the script's copyright headers.

Some scripts and files are based on works of others, in those cases it is my
intention to keep the original license intact. Please make sure to check the
copyright headers inside for more information.

Author
======

Guenter Bartsch <guenter@zamia.org>

