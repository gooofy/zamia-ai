%prolog

answer(topic, en) :-
    context_score(topic, astronomy, 100, SCORE), say_eoa(en, 'We were talking about astronomy.', SCORE).
answer(topic, de) :-
    context_score(topic, astronomy, 100, SCORE), say_eoa(de, 'Wir hatten das Thema Astronomie.', SCORE).

nlp_gen (en, '@SELF_ADDRESS_EN:LABEL (like|) (on|) the moon',
             context_push(topic, astronomy), say_eoa(en, 'ah, the moon. fascinating.')).
nlp_gen (de, '@SELF_ADDRESS_DE:LABEL (wie|als|) auf (den|dem) mond',
             context_push(topic, astronomy), say_eoa(de, 'ah, der mond. faszinierend.')).

nlp_gen (en, '@SELF_ADDRESS_EN:LABEL (on|) (the|) earth',
             'the blue planet.').
nlp_gen (de, '@SELF_ADDRESS_DE:LABEL auf der erde',
             'der blaue planet.').

