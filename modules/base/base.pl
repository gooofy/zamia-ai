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
% basic layer 3 processing predicates
%

l3proc (I, F) :-
    frame (F, type, FT),
    l3proc (I, F, FT).

fnvm_exec (I, VMC) :-
    fnvm_graph (VMC, F),
    l3proc(I, F).

% context_search_l1_frame(TOPI, I, POINTS, MIN_POINTS, URFRAME, FRAMETYPE, FRAME) :-
%     POINTS > MIN_POINTS,
%     ias (I, URFRAME, FRAME),
%     frame (FRAME, type, FRAMETYPE),
%     assertz (ias(TOPI, score, POINTS)).
% 
% context_search_l1_frame(TOPI, I, POINTS, MIN_POINTS, URFRAME, FRAMETYPE, FRAME) :-
%     POINTS > MIN_POINTS,
%     ias(I, prevIAS, PREVI),
%     P is POINTS  / 2,
%     context_search_l1_frame(TOPI, PREVI, P, MIN_POINTS, URFRAME, FRAMETYPE, FRAME).
%

%
% recursive search for level 2 frames through conversation history
%

context_search_l2(TOPI, I, POINTS, MIN_POINTS, URFRAME, L1FRAMETYPE, L1FRAME, L1FE, L2FRAMETYPE, L2FRAME) :-
    POINTS > MIN_POINTS,
    ias (I, URFRAME, L1FRAME),
    frame (L1FRAME, type, L1FRAMETYPE),
    frame (L1FRAME, L1FE, L2FRAME),
    frame (L2FRAME, type, L2FRAMETYPE),
    assertz (ias(TOPI, score, POINTS)).

context_search_l2(TOPI, I, POINTS, MIN_POINTS, URFRAME, L1FRAMETYPE, L1FRAME, L1FE, L2FRAMETYPE, L2FRAME) :-
    POINTS > MIN_POINTS,
    ias(I, prevIAS, PREVI),
    P is POINTS  / 2,
    context_search_l2(TOPI, PREVI, P, MIN_POINTS, URFRAME, L1FRAMETYPE, L1FRAME, L1FE, L2FRAMETYPE, L2FRAME).

%
% recursive search for level 2 FEs through conversation history
%

context_search_l2(TOPI, I, POINTS, MIN_POINTS, URFRAME, L1FRAMETYPE, L1FRAME, L1FE, L2FRAMETYPE, L2FRAME, L2FE, V) :-
    POINTS > MIN_POINTS,
    ias (I, URFRAME, L1FRAME),
    frame (L1FRAME, type, L1FRAMETYPE),
    frame (L1FRAME, L1FE, L2FRAME),
    frame (L2FRAME, type, L2FRAMETYPE),
    frame (L2FRAME, L2FE, V),
    assertz (ias(TOPI, score, POINTS)).

context_search_l2(TOPI, I, POINTS, MIN_POINTS, URFRAME, L1FRAMETYPE, L1FRAME, L1FE, L2FRAMETYPE, L2FRAME, L2FE, V) :-
    POINTS > MIN_POINTS,
    ias(I, prevIAS, PREVI),
    P is POINTS  / 2,
    context_search_l2(TOPI, PREVI, P, MIN_POINTS, URFRAME, L1FRAMETYPE, L1FRAME, L1FE, L2FRAMETYPE, L2FRAME, L2FE, V).


%     frame (F, type, fnQuestioning),
%     frame (F, msg, MSGF),
%     context_search (TOPI, I, POINTS, MIN_POINTS, V, MSGF).
% 
% context_search(TOPI, I, POINTS, MIN_POINTS, V, F) :-
%     frame (F, type, fnFamiliarity),
%     frame (F, ent, V),
%     assertz (ias(TOPI, score, POINTS)).
% 
% context_search (TOPI, I, POINTS, MIN_POINTS, V) :-
%     POINTS > MIN_POINTS,
%     ias (I, rframe, F),
%     context_search(TOPI, I, POINTS, MIN_POINTS, V, F).
% 
% context_search (TOPI, I, POINTS, MIN_POINTS, V) :-
%     POINTS > MIN_POINTS,
%     ias (I, uframe, F),
%     P is POINTS - 10,
%     context_search(TOPI, I, P, MIN_POINTS, V, F).
% 
% context_search (TOPI, I, POINTS, MIN_POINTS, V) :-
%     POINTS > MIN_POINTS,
%     ias(I, prevIAS, PREVI),
%     P is POINTS  / 2,
%     context_search(TOPI, PREVI, P, MIN_POINTS, V, F).

fill_blanks (I, F) :- frame (F, type, FT), fill_blanks (I, F, FT).

%
% basic layer 4 processing predicates
%

l4proc (I) :-
    ias(I, rframe, F),
    frame (F, type, FT),
    l4proc(I, F, FT).

l4proc (I, F, fnTelling) :-
    frame (F, msg, MSGF),
    frame (F, top, TOP),
    frame (MSGF, type, MSGFT),
    l4proc (I, F, fnTelling, TOP, MSGF, MSGFT).

sayz(I, LANG, S) :- assertz(ias(I, action, say(LANG, S))).
scorez(I, SCORE) :- assertz(ias(I, score, SCORE)).

%
% some self address NLP macros
%

% nlp_macro(en, 'SELF_ADDRESS', LABEL) :- rdf (aiu:self, rdfs:label, LABEL, filter(lang(LABEL) = 'en')).
nlp_macro(en, 'SELF_ADDRESS', LABEL) :- rdf (aiu:self, ai:forename, LABEL, filter(lang(LABEL) = 'en')).
nlp_macro(en, 'SELF_ADDRESS', LABEL) :- LABEL is ''.

% NE: not empty
nlp_macro(en, 'SELF_ADDRESS_NE', LABEL) :- rdf (aiu:self, ai:forename, LABEL, filter(lang(LABEL) = 'en')).

% nlp_macro(de, 'SELF_ADDRESS', LABEL) :- rdf (aiu:self, rdfs:label, LABEL, filter(lang(LABEL) = 'de')).
nlp_macro(de, 'SELF_ADDRESS', LABEL) :- rdf (aiu:self, ai:forename, LABEL, filter(lang(LABEL) = 'de')).
nlp_macro(de, 'SELF_ADDRESS', LABEL) :- LABEL is ''.

% NE: not empty
nlp_macro(de, 'SELF_ADDRESS_NE', LABEL) :- rdf (aiu:self, ai:forename, LABEL, filter(lang(LABEL) = 'de')).

