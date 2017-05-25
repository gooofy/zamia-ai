% prolog

%
% named entity recognition (NER)
%

ner_learn_media_stations(LANG) :-
    atom_chars(LANG, LSTR),

    rdf_lists (distinct,
               MEDIA_STATIONS, ai:MediaSlot, SLOTS,
               MEDIA_STATIONS, rdfs:label, LABELS,
               filter(lang(LABELS) = LSTR)),

    ner_learn(LANG, media_station, MEDIA_STATIONS, LABELS).

init ('media') :-
    ner_learn_media_stations(en),
    ner_learn_media_stations(de).

% init ('media') :-
% 
%     % by default, tune into self's favorite media station
%     
%     rdf (aiu:self, ai:favChannel, CHANNEL),
%     context_set (channel, CHANNEL),
%     eoa.

% %
% % test setup and context
% %
% 
% test_setup('media') :-
%     rdf (aiu:self, ai:favChannel, CHANNEL),
%     context_set (channel, CHANNEL),
%     eoa.
% 
% %
% % media_tune: set context, look up slot and title in RDF, generate action
% %
% 
% media_tune (C) :-
% 
%     context_set(channel, C),
% 
%     rdf(distinct, limit(1),
%         C, ai:MediaSlot, SLOT,
%         optional(C, ai:MediaTitle, TITLE)),
%     
%     action (media, tune, SLOT, TITLE),
%     eoa.
% 
% 

l4proc (I, F, zfChangeMediaStation) :-

    SELF is uriref(aiu:self),
    frame(F, age,      SELF),
    frame(F, device,   media),
    frame(F, degree,   on),
    frame(F, station,  STATION),
    frame(F, slot,     SLOT),
    frame(F, title,    TITLE),

    assertz (ias(I, action, media(tune, SLOT, TITLE))).

l4proc (I, F, zfChangeMediaStation) :-

    SELF is uriref(aiu:self),
    frame(F, age,      SELF),
    frame(F, device,   media),
    frame(F, degree,   off),

    assertz (ias(I, action, media(off))).

fill_blanks (I, F, zfChangeMediaStation, station) :- frame(F, station, S).
fill_blanks (I, F, zfChangeMediaStation, station) :- 
    not (frame (F, station, S)),
    % log(info, "looking for previous media change frame..."),
    % if we have one, tune into previous media station
    context_search_l1_frame (I, I, 100, 5, rframe, zfChangeMediaStation, OF),
    % log(info, "looking for previous media change frame... found one."),
    frame (OF, station, S),
    assertz(frame(F, station, S)).
fill_blanks (I, F, zfChangeMediaStation, station) :- 
    not (frame (F, station, S)),
    % by default, tune into self's favorite media station
    rdf (aiu:self, ai:favChannel, S),
    assertz(frame(F, station, S)).
fill_blanks (I, F, zfChangeMediaStation, slot_title) :- frame(F, slot, S).
fill_blanks (I, F, zfChangeMediaStation, slot_title) :- 
    not (frame (F, slot, S)),
    frame (F, station, STATION),
    rdf (limit(1), 
         STATION, ai:MediaSlot, SLOT,
         optional(STATION, ai:MediaTitle, TITLE)),
    assertz(frame(F, slot, SLOT)),
    assertz(frame(F, title, TITLE)).

fill_blanks (I, F, zfChangeMediaStation) :-
    fill_blanks (I, F, zfChangeMediaStation, station),
    fill_blanks (I, F, zfChangeMediaStation, slot_title).

l3proc (I, F, fnRequest, MSGF, zfChangeMediaStation) :-

    fill_blanks (I, MSGF),

    % remember our utterance interpretation

    assertz(ias(I, uframe, F)),

    % produce response frame graph (here: operate media player)
    
    frame(MSGF, degree,   DEGREE),
    frame(MSGF, station,  STATION),
    frame(MSGF, slot,     SLOT),
    frame(MSGF, title,    TITLE),

    list_append(VMC, fe(station, STATION)),
    list_append(VMC, fe(slot,    SLOT)),
    list_append(VMC, fe(title,   TITLE)),
    list_append(VMC, fe(degree,  DEGREE)),
    list_append(VMC, fe(device,  media)),
    list_append(VMC, fe(age,     uriref(aiu:self))),
    list_append(VMC, frame(zfChangeMediaStation)),

    fnvm_graph(VMC, RFRAME),

    scorez(I, 100),

    % remember response frame

    assertz(ias(I, rframe, RFRAME)),

    % generate response actions
    
    l4proc (I).

% %
% % natural language part
% %
% 
% nlp_macro('VERB_EN', W, P) :- W is 'switch to' , P is 'media_tune(C)'.
% nlp_macro('VERB_EN', W, P) :- W is 'switch on' , P is 'media_tune(C)'.
% nlp_macro('VERB_EN', W, P) :- W is 'tune to'   , P is 'media_tune(C)'.
% nlp_macro('VERB_EN', W, P) :- W is 'turn on'   , P is 'media_tune(C)'.
% nlp_macro('VERB_EN', W, P) :- W is 'tune into' , P is 'media_tune(C)'.
% nlp_macro('VERB_EN', W, P) :- W is 'switch off', P is 'action(media, off);eoa'.
% nlp_macro('VERB_EN', W, P) :- W is 'turn off'  , P is 'action(media, off);eoa'.
% 
% nlp_macro('VERB_DE', W, V, P) :- W is 'schalte'   , V is 'ein', P is 'media_tune(C)'.
% nlp_macro('VERB_DE', W, V, P) :- W is 'mach '     , V is 'an',  P is 'media_tune(C)'.
% nlp_macro('VERB_DE', W, V, P) :- W is 'mach '     , V is 'aus', P is 'action(media, off);eoa'.
% nlp_macro('VERB_DE', W, V, P) :- W is 'schalte '  , V is 'aus', P is 'action(media, off);eoa'.
% 
% nlp_macro('STATION_EN', W, P) :- W is 'the radio' , P is 'context_get(channel, C)'.
% nlp_macro('STATION_EN', W, P) :-
%     rdf (distinct,
%          STATION, ai:MediaSlot, SLOT,
%          STATION, rdfs:label, LABEL,
%          filter(lang(LABEL) = 'en')),
%     W is LABEL,
%     P is format_str('C is "%s"', STATION).
% 
% nlp_macro('STATION_DE', W, P) :- W is 'das Radio' , P is 'context_get(channel, C)'.
% nlp_macro('STATION_DE', W, P) :-
%     rdf (distinct,
%          STATION, ai:MediaSlot, SLOT,
%          STATION, rdfs:label, LABEL,
%          filter(lang(LABEL) = 'de')),
%     W is LABEL,
%     P is format_str('C is "%s"', STATION).

nlp_macro(en, 'MEDIA_STATIONS', STATION, LABEL) :-
    rdf (distinct,
         STATION, ai:MediaSlot, SLOT,
         STATION, rdfs:label,   LABEL,
         filter(lang(LABEL) = 'en')).

nlp_macro(de, 'MEDIA_STATIONS', STATION, LABEL) :-
    rdf (distinct,
         STATION, ai:MediaSlot, SLOT,
         STATION, rdfs:label,   LABEL,
         filter(lang(LABEL) = 'de')).

l2proc_changeMediaStationTokens(LANG) :-

    ner(LANG, I, media_station, @MEDIA_STATIONS:TSTART_LABEL_0, @MEDIA_STATIONS:TEND_LABEL_0, NER1ENTITY),

    list_append(VMC, fe(station, NER1ENTITY)),
    list_append(VMC, fe(degree, on)),
    list_append(VMC, fe(age, uriref(aiu:self))),
    list_append(VMC, frame(zfChangeMediaStation)),
    
    list_append(VMC, fe(msg,  vm_frame_pop)),
    list_append(VMC, fe(add,  uriref(aiu:self))),
    ias(I, user, USER),
    list_append(VMC, fe(spkr, USER)),
    list_append(VMC, frame(fnRequest)),

    fnvm_exec (I, VMC).

nlp_gen(en, 
        '@SELF_ADDRESS:LABEL (please|) (switch|turn|tune) (to|on|into) @MEDIA_STATIONS:LABEL',
        inline (l2proc_changeMediaStationTokens, en)).
nlp_gen(de, 
        '@SELF_ADDRESS:LABEL (schalte|mach|stell) (bitte|) (mal|) @MEDIA_STATIONS:LABEL (an|ein)',
        inline (l2proc_changeMediaStationTokens, de)).

l2proc_changeMediaStationContext :-

    list_append(VMC, fe(degree, on)),
    list_append(VMC, fe(age, uriref(aiu:self))),
    list_append(VMC, frame(zfChangeMediaStation)),
    
    list_append(VMC, fe(msg,  vm_frame_pop)),
    list_append(VMC, fe(add,  uriref(aiu:self))),
    ias(I, user, USER),
    list_append(VMC, fe(spkr, USER)),
    list_append(VMC, frame(fnRequest)),
    
    fnvm_exec (I, VMC).

nlp_gen(en, 
        '@SELF_ADDRESS:LABEL (please|) (switch|turn|tune) (to|on|into) (the radio|the music|media|the media player)',
        inline (l2proc_changeMediaStationContext)).
nlp_gen(de, 
        '@SELF_ADDRESS:LABEL (schalte|mach|stell) (bitte|) (mal|) (das radio|musik|die musik|ein bischen musik|die unterhaltung|den media player) (an|ein)',
        inline (l2proc_changeMediaStationContext)).

l2proc_switchOffMedia :-

    list_append(VMC, fe(degree, off)),
    list_append(VMC, fe(age, uriref(aiu:self))),
    list_append(VMC, frame(zfChangeMediaStation)),
    
    list_append(VMC, fe(msg,  vm_frame_pop)),
    list_append(VMC, fe(add,  uriref(aiu:self))),
    ias(I, user, USER),
    list_append(VMC, fe(spkr, USER)),
    list_append(VMC, frame(fnRequest)),
    
    fnvm_exec (I, VMC).

nlp_gen(en, 
        '@SELF_ADDRESS:LABEL (please|) (switch|turn|tune) off (the radio|the music|media|the media player)',
        inline (l2proc_switchOffMedia)).
nlp_gen(de, 
        '@SELF_ADDRESS:LABEL (schalte|mach|stell) (bitte|) (mal|) (das radio|musik|die musik|ein bischen musik|die unterhaltung|den media player) (aus|still)',
        inline (l2proc_switchOffMedia)).

nlp_test(en,
         ivr(in('computer, please switch on the radio'),
             action(media(tune, 9, 1)))).
nlp_test(de,
         ivr(in('computer, schalte bitte das Radio ein'),
             action(media(tune, 9, 1)))).

nlp_test(en,
         ivr(in('computer please tune into new rock'),
             action(media(tune, 3, [])))).
nlp_test(de,
         ivr(in('computer schalte bitte new rock ein'),
             action(media(tune, 3, [])))).

nlp_test(en,
         ivr(in('turn off the radio'),
             action(media(off)))).
nlp_test(de,
         ivr(in('mach das radio aus'),
             action(media(off)))).

nlp_test(en,
         ivr(in('computer please switch on new rock'),
             action(media(tune, 3, []))),
         ivr(in('switch off the radio'),
             action(media(off))),
         ivr(in('please turn on the radio'),
             action(media(tune, 3, [])))). 
nlp_test(de,
         ivr(in('computer schalte bitte new rock ein'),
             action(media(tune, 3, []))),
         ivr(in('mach das radio aus'),
             action(media(off))),
         ivr(in('schalte bitte das radio ein'),
             action(media(tune, 3, [])))). 

