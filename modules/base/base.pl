%prolog

test_setup('base').

%
% basic RDF / Wikidata utils
%

entity_label(LANG, ENTITY, LABEL) :-
    atom_chars(LANG, LSTR),
    rdf (distinct,
         ENTITY, rdfs:label, LABEL,
         filter (lang(LABEL) = LSTR)).

is_entity(ENTITY) :-
    rdf (limit(1), ENTITY, rdfs:label, LABEL).

% humans / persons

is_human(ENTITY) :- rdf (ENTITY, wdpd:InstanceOf, wde:Human).

is_male(ENTITY) :- rdf (ENTITY, wdpd:SexOrGender, wde:Male).
is_female(ENTITY) :- rdf (ENTITY, wdpd:SexOrGender, wde:Female). 

entity_gender(ENTITY, GENDER) :- is_male(ENTITY), GENDER is male.
entity_gender(ENTITY, GENDER) :- is_female(ENTITY), GENDER is female.

%
% hears/says/score utilities
%

scorez(I, SCORE) :- assertz(ias(I, score, SCORE)).

hears (LANG, S, STR) :-
    tokenize (LANG, STR, TOKENS),
    list_extend(S, TOKENS).

% says is implemented in python

%
% some self address NLP macros
%

self_address(en, S, "").
self_address(en, S, LABEL) :- 
    rdf (aiu:self, ai:forename, LABEL, filter(lang(LABEL) = 'en')),
    hears(en, S, LABEL).

self_address(de, S, "").
self_address(de, S, LABEL) :- 
    rdf (aiu:self, ai:forename, LABEL, filter(lang(LABEL) = 'de')),
    hears(de, S, LABEL).

% NE: not empty

self_address_ne(en, S, LABEL) :- 
    rdf (aiu:self, ai:forename, LABEL, filter(lang(LABEL) = 'en')),
    hears(en, S, LABEL).
self_address_ne(de, S, LABEL) :- 
    rdf (aiu:self, ai:forename, LABEL, filter(lang(LABEL) = 'de')),
    hears(de, S, LABEL).

