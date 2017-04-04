% prolog

init ('radio') :-

    % by default, tune into self's favorite radio station
    
    rdf (aiu:self, ai:favChannel, CHANNEL),
    context_set (channel, CHANNEL),
    eoa.

%
% test setup and context
%

test_setup('radio') :-
    rdf (aiu:self, ai:favChannel, CHANNEL),
    context_set (channel, CHANNEL),
    eoa.

%
% media_tune: set context, look up slot and title in RDF, generate action
%

media_tune (C) :-

    context_set(channel, C),

    rdf(distinct, limit(1),
        C, ai:MediaSlot, SLOT,
        optional(C, ai:MediaTitle, TITLE)),
    
    action (media, tune, SLOT, TITLE),
    eoa.


%
% natural language part
%

nlp_macro('VERB_EN', W, P) :- W is 'switch to' , P is 'media_tune(C)'.
nlp_macro('VERB_EN', W, P) :- W is 'switch on' , P is 'media_tune(C)'.
nlp_macro('VERB_EN', W, P) :- W is 'tune to'   , P is 'media_tune(C)'.
nlp_macro('VERB_EN', W, P) :- W is 'turn on'   , P is 'media_tune(C)'.
nlp_macro('VERB_EN', W, P) :- W is 'tune into' , P is 'media_tune(C)'.
nlp_macro('VERB_EN', W, P) :- W is 'switch off', P is 'action(media, off);eoa'.
nlp_macro('VERB_EN', W, P) :- W is 'turn off'  , P is 'action(media, off);eoa'.

nlp_macro('VERB_DE', W, V, P) :- W is 'schalte'   , V is 'ein', P is 'media_tune(C)'.
nlp_macro('VERB_DE', W, V, P) :- W is 'mach '     , V is 'an',  P is 'media_tune(C)'.
nlp_macro('VERB_DE', W, V, P) :- W is 'mach '     , V is 'aus', P is 'action(media, off);eoa'.
nlp_macro('VERB_DE', W, V, P) :- W is 'schalte '  , V is 'aus', P is 'action(media, off);eoa'.

nlp_macro('STATION_EN', W, P) :- W is 'the radio' , P is 'context_get(channel, C)'.
nlp_macro('STATION_EN', W, P) :-
    rdf (distinct,
         STATION, ai:MediaSlot, SLOT,
         STATION, rdfs:label, LABEL,
         filter(lang(LABEL) = 'en')),
    W is LABEL,
    P is format_str('C is "%s"', STATION).

nlp_macro('STATION_DE', W, P) :- W is 'das Radio' , P is 'context_get(channel, C)'.
nlp_macro('STATION_DE', W, P) :-
    rdf (distinct,
         STATION, ai:MediaSlot, SLOT,
         STATION, rdfs:label, LABEL,
         filter(lang(LABEL) = 'de')),
    W is LABEL,
    P is format_str('C is "%s"', STATION).

nlp_gen(en, 
        '@SELF_ADDRESS_EN:LABEL (please|) @VERB_EN:W @STATION_EN:W',
        @STATION_EN:P, @VERB_EN:P).
nlp_gen(de, 
        '@SELF_ADDRESS_DE:LABEL @VERB_DE:W (bitte|) (mal|) @STATION_DE:W @VERB_DE:V',
        @STATION_DE:P, @VERB_DE:P).

nlp_test(en,
         ivr(in('computer, please switch on the radio'),
             action(media, tune, 9, 1))).
nlp_test(de,
         ivr(in('computer, schalte bitte das Radio ein'),
             action(media, tune, 9, 1))).

nlp_test(en,
         ivr(in('computer please tune into new rock'),
             action(media, tune, 3, []))).
nlp_test(de,
         ivr(in('computer schalte bitte new rock ein'),
             action(media, tune, 3, []))).

nlp_test(en,
         ivr(in('turn off the radio'),
             action(media, off))).
nlp_test(de,
         ivr(in('mach das radio aus'),
             action(media, off))).

nlp_test(en,
         ivr(in('computer please switch on new rock'),
             action(media, tune, 3, [])),
         ivr(in('switch off the radio'),
             action(media, off)),
         ivr(in('please turn on the radio'),
             action(media, tune, 3, []))). 
nlp_test(de,
         ivr(in('computer schalte bitte new rock ein'),
             action(media, tune, 3, [])),
         ivr(in('mach das radio aus'),
             action(media, off)),
         ivr(in('schalte bitte das radio ein'),
             action(media, tune, 3, []))). 

