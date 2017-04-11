%prolog

answer(topic, en) :-
    context_score(topic, religion, 100, SCORE), say_eoa(en, 'We were talking about faith and religion.', SCORE).
answer(topic, de) :-
    context_score(topic, religion, 100, SCORE), say_eoa(de, 'Wir hatten das Thema Glaube und Religion.', SCORE).

nlp_gen (en, "@SELF_ADDRESS_EN:LABEL (oh my|do you believe in|is there a|by) god",
             context_push(topic, religion), say_eoa(en, "are you a religious person?"), 
             context_push(topic, religion), say_eoa(en, "do you believe in god")).
nlp_gen (de, '@SELF_ADDRESS_DE:LABEL (oh mein|glaubst du an|gibt es einen|bei) gott',
             context_push(topic, religion), say_eoa(de, 'Bist Du ein gläubiger Mensch?'), 
             context_push(topic, religion), say_eoa(de, 'glaubst du denn an gott?')).

nlp_gen (en, "@SELF_ADDRESS_EN:LABEL (are you|am I) (jesus|god)",
             "Ich bin ein Berliner.").
nlp_gen (de, '@SELF_ADDRESS_DE:LABEL (bist du|bin ich) (jesus|gott)',
             'ich habe zweifel').

