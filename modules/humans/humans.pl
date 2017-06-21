%prolog

%
% named entity recognition (NER)
%

% this will switch to much smaller training sets so we can keep 
% debug turn-around cycle times low
debug_mode('humans').

ner_learn_humans(LANG) :-
    atom_chars(LANG, LSTR),

    rdf_lists (distinct,
               HUMAN_ENTITIES, wdpd:InstanceOf,   wde:Human,
               HUMAN_ENTITIES, rdfs:label,        HUMAN_LABELS,
               filter (lang(HUMAN_LABELS) = LSTR)),

    ner_learn(LANG, human, HUMAN_ENTITIES, HUMAN_LABELS).

init('humans') :-
    ner_learn_humans(en),
    ner_learn_humans(de).

%
% utils
%

nlp_f1_ent_pp(en, I, ENTITY) :-
    is_male(ENTITY),
    setz(ias(I, f1_ent_pp3s, _), "he"),
    setz(ias(I, f1_ent_pp3o, _), "him"),
    !.
nlp_f1_ent_pp(en, I, ENTITY) :-
    is_female(ENTITY),
    setz(ias(I, f1_ent_pp3s, _), "she"),
    setz(ias(I, f1_ent_pp3o, _), "her"),
    !.
nlp_f1_ent_pp(en, I, ENTITY) :-
    setz(ias(I, f1_ent_pp3s, _), "it"),
    setz(ias(I, f1_ent_pp3o, _), "it").

nlp_f1_ent_pp(de, I, ENTITY) :-
    is_male(ENTITY),
    setz(ias(I, f1_ent_pp3s, _), "er"),
    setz(ias(I, f1_ent_pp3o, _), "ihn"),
    !.
nlp_f1_ent_pp(de, I, ENTITY) :-
    is_female(ENTITY),
    setz(ias(I, f1_ent_pp3s, _), "sie"),
    setz(ias(I, f1_ent_pp3o, _), "sie"),
    !.
nlp_f1_ent_pp(de, I, ENTITY) :-
    setz(ias(I, f1_ent_pp3s, _), "es"),
    setz(ias(I, f1_ent_pp3o, _), "es").

nlp_f1_ent_human(LANG, I, HUMAN) :-
    
    entity_label(LANG, HUMAN, LABEL),
    setz(ias(I, f1_entlabel, _), LABEL),

    nlp_f1_ent_pp(LANG, I, HUMAN).

%
% datasets
%

% debug

known_humans_data(en, SIZE, HUMAN, LABEL) :-
    debug_mode('humans'),
    HUMAN is 'http://www.wikidata.org/entity/Q39829',
    LABEL is 'Stephen King'.

known_humans_data(de, SIZE, HUMAN, LABEL) :-
    debug_mode('humans'),
    HUMAN is 'http://www.wikidata.org/entity/Q39829',
    LABEL is 'Stephen King'.

% production

known_humans_data(LANG, small, HUMAN, LABEL) :-
    not(debug_mode('humans')),
    atom_chars(LANG, LSTR),
    rdf (distinct, 
         limit(23),
         HUMAN, wdpd:InstanceOf,   wde:Human,
         HUMAN, rdfs:label,        LABEL,
         filter (lang(LABEL) = LSTR)).

known_humans_data(LANG, large, HUMAN, LABEL) :-
    not(debug_mode('humans')),
    atom_chars(LANG, LSTR),
    rdf (distinct, 
         HUMAN, wdpd:InstanceOf,   wde:Human,
         HUMAN, rdfs:label,        LABEL,
         filter (lang(LABEL) = LSTR)).

%
% known humans with their LABELs
%

nlp_known_humans_s (en, SIZE, S, HUMAN, LABEL, TSTART, TEND) :-
    known_humans_data(en, SIZE, HUMAN, LABEL),
    length(S, TSTART),
    hears (en, S, LABEL),
    length(S, TEND).
    
nlp_known_humans_gen_s (en, SIZE, S, HUMAN, LABEL, TSTART, TEND) :-
    known_humans_data(en, SIZE, HUMAN, L),
    LABEL is format_str("%s's", L),
    length(S, TSTART),
    hears (en, S, LABEL),
    length(S, TEND).

nlp_known_humans_s (de, SIZE, S, HUMAN, LABEL, TSTART, TEND) :-
    known_humans_data(de, SIZE, HUMAN, LABEL),
    length(S, TSTART),
    hears (de, S, LABEL),
    length(S, TEND).
    
%
% questions about humans known
%

nlp_humans_s (en, SIZE, start, doyouknow, S, TSTART, TEND) :- hears (en, S, "do you know"),           nlp_known_humans_s (en, SIZE, S, _, _, TSTART, TEND).
nlp_humans_s (en, SIZE, start, doyouknow, S, TSTART, TEND) :- hears (en, S, "do you happen to know"), nlp_known_humans_s (en, SIZE, S, _, _, TSTART, TEND).

nlp_humans_s (de, SIZE, start, doyouknow, S, TSTART, TEND) :- hears (de, S, "kennst Du"),             nlp_known_humans_s (de, SIZE, S, _, _, TSTART, TEND).
nlp_humans_s (de, SIZE, start, doyouknow, S, TSTART, TEND) :- hears (de, S, "kennst Du eigentlich"),  nlp_known_humans_s (de, SIZE, S, _, _, TSTART, TEND).

nlp_humans_r (en, doyouknow, R) :- says (en, R, "Sure I know %(f1_entlabel)s.").
nlp_humans_r (en, doyouknow, R) :- says (en, R, "Yes I know %(f1_entlabel)s.").
nlp_humans_r (en, doyouknow, R) :- says (en, R, "Sure I know %(f1_ent_pp3o)s.").
nlp_humans_r (en, doyouknow, R) :- says (en, R, "Yes I know %(f1_ent_pp3o)s.").
nlp_humans_r (de, doyouknow, R) :- says (de, R, "Klar kenne ich %(f1_entlabel)s.").
nlp_humans_r (de, doyouknow, R) :- says (de, R, "Ja ich kenne %(f1_entlabel)s.").
nlp_humans_r (de, doyouknow, R) :- says (de, R, "Klar kenne ich %(f1_ent_pp3o)s.").
nlp_humans_r (de, doyouknow, R) :- says (de, R, "Ja ich kenne %(f1_ent_pp3o)s.").

nlp_humans_g(LANG, start, doyouknow, G, TSTART, TEND) :-
    G is [
        % trace(on),
        ner(LANG, I, NER1CLASS, TSTART, TEND, NER1ENTITY),

        setz(ias(I, f1_type,     _), question),
        setz(ias(I, f1_topic,    _), familiarity),
        setz(ias(I, f1_entclass, _), NER1CLASS),
        setz(ias(I, f1_ent,      _), NER1ENTITY),

        nlp_f1_ent_human(LANG, I, NER1ENTITY)
        ].

nlp_humans_sgr(LANG, SIZE, start, TOPIC, S, G, R) :-
    nlp_humans_s (LANG, SIZE, start, TOPIC, S, TSTART, TEND),
    nlp_humans_g (LANG, start, TOPIC, G, TSTART, TEND),
    nlp_humans_r (LANG, TOPIC, R).

nlp_train('humans', en, [[], S1, G1, R1]) :-
    self_address(en, S1, _),
    nlp_humans_sgr(en, large, start, doyouknow, S1, G1, R1).

nlp_train('humans', de, [[], S1, G1, R1]) :-
    self_address(de, S1, _),
    nlp_humans_sgr(de, large, start, doyouknow, S1, G1, R1).

nlp_test('humans', de, 'know1', [],
         ['Kennst Du Stephen King?', 'Ja ich kenne Stephen King', []]).
nlp_test('humans', en, 'know2', [],
         ['Do you know Stephen King?', 'Sure I know Stephen King', []]).
nlp_test('humans', en, 'know3', [],
         ['Do you know Stephen King?', 'Sure I know him', []]).

%
% birthplace and birtdate questions
%

nlp_humans_g (LANG, start, birthplace, G, TSTART, TEND) :-
    G is [
        % trace(on),
        ner(LANG, I, NER1CLASS, TSTART, TEND, NER1ENTITY),

        setz(ias(I, f1_type,     _), question),
        setz(ias(I, f1_topic,    _), birthplace),
        setz(ias(I, f1_entclass, _), NER1CLASS),
        setz(ias(I, f1_ent,      _), NER1ENTITY),

        nlp_f1_ent_human (LANG, I, NER1ENTITY),

        rdf (distinct, limit(1),
             NER1ENTITY, wdpd:PlaceOfBirth, BIRTHPLACE),
        setz(ias(I, f1_loc, _), BIRTHPLACE),

        entity_label(LANG, BIRTHPLACE, BPLABEL),

        setz(ias(I, f1_loclabel, _), BPLABEL)
        ].

nlp_humans_s (en, SIZE, start, birthplace, S, TSTART, TEND) :-
    hears (en, S, [ [ "where", "in which town", "in which city"], ["was", "is"] ] ),
    nlp_known_humans_s (en, SIZE, S, _, _, TSTART, TEND),    
    hears (en, S, "born?").
nlp_humans_s (en, SIZE, start, birthplace, S, TSTART, TEND) :-
    hears (en, S, [ "which is", [ "the birthplace", "the place of birth"], "of" ] ),
    nlp_known_humans_s (en, SIZE, S, _, _, TSTART, TEND).

nlp_humans_s (de, SIZE, start, birthplace, S, TSTART, TEND) :-
    hears (de, S, [ [ "wo", "in welcher Stadt", "an welchem Ort"], ["wurde", "ist"], ["eigentlich", ""] ] ),
    nlp_known_humans_s (de, SIZE, S, _, _, TSTART, TEND),    
    hears (de, S, "geboren?").
nlp_humans_s (de, SIZE, start, birthplace, S, TSTART, TEND) :-
    hears (de, S, [ ["welches", "was"], "ist", [ "der Geburtsort", "die Geburtsstadt"], "von" ] ),
    nlp_known_humans_s (de, SIZE, S, _, _, TSTART, TEND).

nlp_humans_r (en, birthplace, R) :- says (en, R, "%(f1_entlabel)s was born in %(f1_loclabel)s.").
nlp_humans_r (en, birthplace, R) :- says (en, R, "%(f1_ent_pp3s)s was born in %(f1_loclabel)s.").
nlp_humans_r (de, birthplace, R) :- says (de, R, "%(f1_entlabel)s wurde in %(f1_loclabel)s geboren.").
nlp_humans_r (de, birthplace, R) :- says (de, R, "%(f1_ent_pp3s)s wurde in %(f1_loclabel)s geboren.").

nlp_train('humans', en, [[], S1, G1, R1]) :-
    self_address(en, S1, _),
    nlp_humans_sgr(en, large, start, birthplace, S1, G1, R1).

nlp_train('humans', de, [[], S1, G1, R1]) :-
    self_address(de, S1, _),
    nlp_humans_sgr(de, large, start, birthplace, S1, G1, R1).

nlp_test('humans', en, 'whereborn1', [],
         ['Where was Stephen King born?', 'Stephen King was born in Portland.', []]).

nlp_test('humans', de, 'whereborn2', [],
         ['Wo wurde Stephen King geboren?', 'Stephen King wurde in Portland geboren.', []]).
 

nlp_humans_g (LANG, start, birthdate, G, TSTART, TEND) :-
    G is [
        % trace(on),
        ner(LANG, I, NER1CLASS, TSTART, TEND, NER1ENTITY),

        setz(ias(I, f1_type,     _), question),
        setz(ias(I, f1_topic,    _), birthdate),
        setz(ias(I, f1_entclass, _), NER1CLASS),
        setz(ias(I, f1_ent,      _), NER1ENTITY),

        nlp_f1_ent_human (LANG, I, NER1ENTITY),

        rdf (distinct, limit(1),
             NER1ENTITY,   wdpd:DateOfBirth,  BIRTHDATE),
        setz(ias(I, f1_time, _), BIRTHDATE),

        transcribe_date(LANG, dativ, BIRTHDATE, BDLABEL),
        setz(ias(I, f1_timelabel, _), BDLABEL)

        ].

nlp_humans_s (en, SIZE, start, birthdate, S, TSTART, TEND) :-
    hears (en, S, [ [ "when", "in which year"], ["was", "is"] ] ),
    nlp_known_humans_s (en, SIZE, S, _, _, TSTART, TEND),    
    hears (en, S, "born?").
nlp_humans_s (en, SIZE, start, birthdate, S, TSTART, TEND) :-
    hears (en, S, [ ["when is", "on what day is"] ] ),
    nlp_known_humans_s (en, SIZE, S, _, _, TSTART, TEND),
    hears (en, S, "birthday?").

nlp_humans_s (de, SIZE, start, birthdate, S, TSTART, TEND) :-
    hears (de, S, [ [ "wann", "in welchem Jahr"], ["wurde", "ist"], ["eigentlich", ""] ] ),
    nlp_known_humans_s (de, SIZE, S, _, _, TSTART, TEND),    
    hears (de, S, "geboren?").
nlp_humans_s (de, SIZE, start, birthdate, S, TSTART, TEND) :-
    hears (de, S, [ ["wann hat", "an welchem Tag hat"], [ "eigentlich", ""] ] ),
    nlp_known_humans_s (de, SIZE, S, _, _, TSTART, TEND),
    hears (de, S, "Geburtstag?").

nlp_humans_r (en, birthdate, R) :- says (en, R, "%(f1_entlabel)s was born on %(f1_timelabel)s.").
nlp_humans_r (en, birthdate, R) :- says (en, R, "%(f1_ent_pp3s)s was born on %(f1_timelabel)s.").
nlp_humans_r (de, birthdate, R) :- says (de, R, "%(f1_entlabel)s wurde am %(f1_timelabel)s geboren.").
nlp_humans_r (de, birthdate, R) :- says (de, R, "%(f1_ent_pp3s)s wurde am %(f1_timelabel)s geboren.").

nlp_train('humans', en, [[], S1, G1, R1]) :-
    self_address(en, S1, _),
    nlp_humans_sgr(en, large, start, birthdate, S1, G1, R1).

nlp_train('humans', de, [[], S1, G1, R1]) :-
    self_address(de, S1, _),
    nlp_humans_sgr(de, large, start, birthdate, S1, G1, R1).

nlp_test('humans', en, 'whenborn1', [],
         ['When was Stephen King born?', 'Stephen King was born on September 21, 1947.', []]).

nlp_test('humans', de, 'whenborn2', [],
         ['Wann wurde Stephen King geboren?', 'Stephen King wurde am einundzwanzigsten September 1947 geboren.', []]).
 
%
% multi-round / followup birthday/birthplace questions
%

nlp_humans_g (LANG, followup, birthplace, G) :-
    G is [
        setz(ias(I, f1_type,     _), question),
        setz(ias(I, f1_topic,    _), birthplace),
        
        ias(I, f1_ent, NER1ENTITY),

        nlp_f1_ent_human (LANG, I, NER1ENTITY),

        rdf (distinct, limit(1),
             NER1ENTITY, wdpd:PlaceOfBirth, BIRTHPLACE),
        setz(ias(I, f1_loc, _), BIRTHPLACE),

        entity_label(LANG, BIRTHPLACE, BPLABEL),

        setz(ias(I, f1_loclabel, _), BPLABEL)
        ].

nlp_humans_s (en, followup, birthplace, S) :-
    hears (en, S, [["and",""], ["where","in which town","in which city"] ] ).
nlp_humans_s (de, followup, birthplace, S) :-
    hears (de, S, [["und",""], ["wo","in welcher stadt","an welchem ort"]] ).
nlp_humans_s (en, followup, birthplace, S) :-
    not(debug_mode('humans')),
    hears (en, S, [["and",""], ["where","in which town","in which city"], ["was","is"], ["she","he"], "born", ["again",""] ] ).
nlp_humans_s (de, followup, birthplace, S) :-
    not(debug_mode('humans')),
    hears (de, S, [["und",""], ["wo","in welcher stadt","an welchem ort"], ["wurde","ist"], ["sie","er"], ["eigentlich",""], ["nochmal",""], "geboren" ] ).

nlp_humans_s (en, followup, birthplace, S) :-
    not(debug_mode('humans')),
    hears (en, S, [["and",""], "which", "is", ["the birthplace","place of birth"], "of", ["him","her"], ["again",""]]).
nlp_humans_s (de, followup, birthplace, S) :-
    not(debug_mode('humans')),
    hears (de, S, [["und",""], "welches", "ist", ["eigentlich","nochmal",""], ["der Geburtsort","die Geburtsstadt"], "von", ["ihm","ihr"]] ).


nlp_humans_g (LANG, followup, birthdate, G) :-
    G is [
        setz(ias(I, f1_type,     _), question),
        setz(ias(I, f1_topic,    _), birthdate),
        
        ias(I, f1_ent, NER1ENTITY),

        nlp_f1_ent_human (LANG, I, NER1ENTITY),

        rdf (distinct, limit(1),
             NER1ENTITY,   wdpd:DateOfBirth,  BIRTHDATE),
        setz(ias(I, f1_time, _), BIRTHDATE),

        transcribe_date(LANG, dativ, BIRTHDATE, BDLABEL),
        setz(ias(I, f1_timelabel, _), BDLABEL)
        ].

nlp_humans_s (en, followup, birthdate, S) :-
    hears (en, S, [["and",""], ["when","in which year"] ] ).
nlp_humans_s (de, followup, birthdate, S) :-
    hears (de, S, [["und",""], ["wann","in welchem Jahr"] ] ).
nlp_humans_s (en, followup, birthdate, S) :-
    not(debug_mode('humans')),
    hears (en, S, [["and",""], ["when","in which year"], ["was","is"], ["she","he"], "born", ["again",""] ] ).
nlp_humans_s (de, followup, birthdate, S) :-
    not(debug_mode('humans')),
    hears (de, S, [["und",""], ["wann","in welchem Jahr"], ["wurde","ist"], ["sie","er"], ["eigentlich",""], ["nochmal",""], "geboren" ] ).

nlp_humans_sgr(LANG, followup, TOPIC, S, G, R) :-
    nlp_humans_s (LANG, followup, TOPIC, S),
    nlp_humans_g (LANG, followup, TOPIC, G),
    nlp_humans_r (LANG, TOPIC, R).

nlp_train('humans', en, [[], S1, G1, R1, [], S2, G2, R2]) :-
    nlp_humans_sgr(en, small, start, TOPIC1, S1, G1, R1),
    nlp_humans_sgr(en, followup, TOPIC2, S2, G2, R2).

nlp_train('humans', de, [[], S1, G1, R1, [], S2, G2, R2]) :-
    nlp_humans_sgr(de, small, start, TOPIC1, S1, G1, R1),
    nlp_humans_sgr(de, followup, TOPIC2, S2, G2, R2).

nlp_test('humans', en, 'multi1', [],
         ['When was Stephen King born?', 'Stephen King was born on September 21, 1947.', [],
          'and where?', 'Stephen King was born in Portland.', []]).

nlp_test('humans', de, 'multi2', [],
         ['Wann wurde Stephen King geboren?', 'Stephen King wurde am einundzwanzigsten September 1947 geboren.', [],
          'und wo?', 'Stephen King wurde in Portland geboren.', []]).

% nlp_test(en,
%          ivr(in('Where was Angela Merkel born?'),
%              out('angela merkel was born in barmbek-nord')),
%          ivr(in('What were we talking about?'),
%              out('angela merkels birthday')),
%          ivr(in('and where was she born again?'),
%              out('angela merkel was born in barmbek-nord'))).
% nlp_test(de,
%          ivr(in('Wo wurde Angela Merkel geboren?'),
%              out('angela merkel wurde in barmbek-nord geboren')),
%          ivr(in('Welches Thema hatten wir?'),
%              out('angela merkels geburtstag.')),
%          ivr(in('und wo wurde sie nochmal geboren?'),
%              out('angela merkel wurde in barmbek-nord geboren'))).
%

% nlp_test(en,
%          ivr(in('When was Angela Merkel born?'),
%              out('Angela Merkel was born on july seventeen, 1954.')),
%          ivr(in('What were we talking about?'),
%              out('angela merkels birthday')),
%          ivr(in('and when was she born?'),
%              out('Angela Merkel was born on july seventeen, 1954.')),
%          ivr(in('and where?'),
%              out('she was born in barmbek nord'))
%         ).
% 
% nlp_test(de,
%          ivr(in('Wann wurde Angela Merkel geboren?'),
%              out('Angela Merkel wurde am siebzehnten juli 1954 geboren.')),
%          ivr(in('Welches Thema hatten wir?'),
%              out('angela merkels geburtstag')),
%          ivr(in('und wann wurde sie nochmal geboren?'),
%              out('Angela Merkel wurde am siebzehnten juli 1954 geboren.')),
%          ivr(in('und wo?'),
%              out('Angela Merkel wurde in barmbek nord geboren.'))
%         ).

%
% if we don't know anything else, we can tell the user about the human's birthplace
%

nlp_train('humans', en, [[], S1, G1, R1]) :-

    self_address(en, S1, _),
    hears (en, S1, [ [ "what about", "who is", "what is", "what do you know about", "what do you know of" ] ] ),
    nlp_known_humans_s (en, large, S1, _, _, TSTART, TEND),    

    nlp_humans_g (en, start, birthplace, G1, TSTART, TEND),

    says (en, R1, "%(f1_entlabel)s was born in %(f1_loclabel)s.").

nlp_train('humans', de, [[], S1, G1, R1]) :-

    self_address(de, S1, _),
    hears (de, S1, [ [ "wer ist", "wer ist eigentlich", "was ist mit", "was ist eigentlich mit", "was weisst du über", "was weisst du eigentlich über" ] ] ),
    nlp_known_humans_s (de, large, S1, _, _, TSTART, TEND),    

    nlp_humans_g (de, start, birthplace, G1, TSTART, TEND),

    says (de, R1, "%(f1_entlabel)s wurde in %(f1_loclabel)s geboren.").

nlp_test('humans', en, 'whatabout1', [],
         ['What about Stephen King?', 'Stephen King was born in Portland.', []]).
 
nlp_test('humans', de, 'whatabout2', [],
         ['Was ist mit Stephen King?', 'Stephen King wurde in Portland geboren.', []]).
 
