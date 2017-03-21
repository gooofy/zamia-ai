% prolog

%
% test setup and context
%

context_set_default('test', channel, URI) :- uriref(wde:Q795291, URI).

%
% media_tune: set context, look up slot and title in RDF, generate action
%

media_tune (C) :-

    context_set(channel, C),

    rdf(distinct, limit(1),
        C, hal:MediaSlot, SLOT,
        optional(C, hal:MediaTitle, TITLE)),
    
    action (media, tune, SLOT, TITLE),
    eoa.


%
% natural language part
%

nlp_macro('VERB', W, V, P) :- W is 'schalte'   , V is 'ein', P is 'media_tune(C)'.
nlp_macro('VERB', W, V, P) :- W is 'mach '     , V is 'an',  P is 'media_tune(C)'.
nlp_macro('VERB', W, V, P) :- W is 'mach '     , V is 'aus', P is 'action(media, off);eoa'.
nlp_macro('VERB', W, V, P) :- W is 'schalte '  , V is 'aus', P is 'action(media, off);eoa'.

nlp_macro('STATION', W, P) :- W is 'das Radio' , P is 'context_get(channel, C)'.
nlp_macro('STATION', W, P) :-
    rdf (distinct,
         STATION, hal:MediaSlot, SLOT,
         STATION, rdfs:label, LABEL,
         filter(lang(LABEL) = 'de')),
    W is LABEL,
    P is format_str('C is "%s"', STATION).

nlp_gen(de, 
        '(Hallo|Hi|) (HAL|Computer|) @VERB:W (bitte|) (mal|) @STATION:W @VERB:V',
        @STATION:P, @VERB:P).

nlp_test(de,
         ivr(in('HAL, schalte bitte das Radio ein'),
             action(media, tune, 9, 1))).

nlp_test(de,
         ivr(in('computer schalte bitte new rock ein'),
             action(media, tune, 3, []))).


nlp_test(de,
         ivr(in('mach das radio aus'),
             action(media, off))).


nlp_test(de,
         ivr(in('computer schalte bitte new rock ein'),
             action(media, tune, 3, [])),
         ivr(in('hal mach das radio aus'),
             action(media, off)),
         ivr(in('schalte bitte das radio ein'),
             action(media, tune, 3, []))). 

