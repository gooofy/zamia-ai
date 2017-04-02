# Note

If you're looking for the scripts that I am using to build my VoxForge models, those
are over at [https://github.com/gooofy/speech](https://github.com/gooofy/speech).

# Zamia AI

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

# Knowledge Base Notes

## contexts

Contexts are stored individually per-user in KB (sparqlalchemy/rdf)

e.g.
```
   aiu:Alice  aiup:name       'Alice Green'
              aiup:topics     "[weather, wde:Q37373, ...]"
              aiup:favMovie   wde:Q...
              ...
```
stored values can be arbitrary prolog structures (e.g. lists) which are stored in JSON format
if no corresponding RDF datatype exists. context\_push/context\_score operations work on such
stored list literals, see aiup:topics above for an example.

a dedicated default user exists which can be used to store defaults for context values
```
   aiu:default aiup:name       'Alice Green'
               aiup:favMovie   wde:Q...
               ...
```
when processing input, a special node ai:curin (http://ai.zamia.org/kb/curin) is set up with 
context information about the current input:
```
    ai:curin  ai:user        aiu:Alice
              ai:utterance   "hello computer"
              ai:uttLang     en
              ai:tokens      ["hello", "computer"]
              ai:currentTime 1490816071.601048 (seconds since epoch)
```
while executing tests, currentTime is set to the fixed value of 1481027286.0, corresponding to
December 6th, 2016 13:28:06 .

### self context

to store information the AI system knows about itself (i.e. its name, when it was born, favorite
movie etc) a special user aiu:self is used

e.g.
```
    aiu:self   rdfs:label    "HAL 9000"@en;
               rdfs:label    "HAL 9000"@de;
               wdpd:P31      wde:Q68;       # InstanceOf computer
               wdpd:P21      wde:Q6581097;  # SexOrGender male
               wdpd:P131     wde:Q1022;     # LocatedIn Stuttgart
               ai:favMovie   wde:Q103474;   # favMovie 2001: A Space Odyssey
               ai:favChannel wde:Q795291.   # favChannel b5 aktuell
```

# module initialization / test setup

when a aiprolog module is loaded for processing, a special target

```prolog
    init("module_name")
```

is searched for and actions produced from this search are executed. this mechanism can
be used to initialize the module through prolog code in general and setup default 
context values in particular, as 

```
    ai:curin  ai:user aiu:default
```

is set during execution.

Additionally, before running each test, a special target
```prolog
    test_setup("module_name")
```
is searched. 
```
    ai_curin  ai:user aiu:test
```
is set during execution

Links
=====

* [Code](https://github.com/gooofy/zamia-ai "github")

Requirements
============

*Note*: very incomplete.

* Python 2.7 with nltk, numpy, ...
* tensorflow
* from my other repositories: py-nltools, sparqlalchemy

Setup Notes
===========

Just some rough notes on the environment needed to get these scripts to run. This is in no way a complete set of
instructions, just some hints to get you started.

`~/.airc`:

```ini
[db]
url                 = postgresql://semantics:password@dagobert:5432/zamia_ai

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
./ai_cli.py utterances 
```

or to dump out a set of 20 random utterances which contain words not covered by the dictionary:

```bash
./ai_cli.py utterances -d ../speech/data/src/speech/de/dict.ipa -n 20
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

