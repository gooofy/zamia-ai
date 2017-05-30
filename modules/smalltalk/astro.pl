%prolog

% answer(topic, en) :-
%     context_score(topic, astronomy, 100, SCORE), say_eoa(en, 'We were talking about astronomy.', SCORE).
% answer(topic, de) :-
%     context_score(topic, astronomy, 100, SCORE), say_eoa(de, 'Wir hatten das Thema Astronomie.', SCORE).

nlp_gens (en, '@SELF_ADDRESS:LABEL (like|) (on|) the moon',
          'ah, the moon. fascinating.').
nlp_gens (de, '@SELF_ADDRESS:LABEL (wie|als|) auf (den|dem) mond',
          'ah, der mond. faszinierend.').

nlp_gens (en, '@SELF_ADDRESS:LABEL (on|) (the|) earth',
             'the blue planet.').
nlp_gens (de, '@SELF_ADDRESS:LABEL auf der erde',
             'der blaue planet.').

