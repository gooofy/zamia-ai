%prolog

answer(topic, en) :-
    context_score(topic, religion, 100, SCORE), say_eoa(en, 'We were talking about faith and religion.', SCORE).
answer(topic, de) :-
    context_score(topic, religion, 100, SCORE), say_eoa(de, 'Wir hatten das Thema Glaube und Religion.', SCORE).

nlp_gen (en, "@SELF_ADDRESS_EN:LABEL (are you|am I) (jesus|god)",
             "Ich bin ein Berliner.").
nlp_gen (de, '@SELF_ADDRESS_DE:LABEL (bist du|bin ich) (jesus|gott)',
             'ich habe zweifel').

