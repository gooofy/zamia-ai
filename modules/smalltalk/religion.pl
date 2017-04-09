%prolog

answer(topic, en) :-
    context_score(topic, religion, 100, SCORE), say_eoa(en, 'We were talking about faith and religion.', SCORE).
answer(topic, de) :-
    context_score(topic, religion, 100, SCORE), say_eoa(de, 'Wir hatten das Thema Glaube und Religion.', SCORE).

nlp_gen (de, '(HAL,|Computer,|) (oh mein|glaubst du an|gibt es einen|bei) gott',
             'Bist Du ein gläubiger Mensch?', 'glaubst du denn an gott?').

nlp_gen (de, '(HAL,|Computer,|) bin ich gott',
             'Nein, das bezweifele ich.').

nlp_gen (de, '(HAL,|Computer,|) bin ich jesus',
             'Das glaube ich nicht. Mit den kaputten Händen könnte der sicherlich nicht mehr tippen.').

nlp_gen (de, '(HAL,|Computer,|) bist du jesus',
             'Nein, der chattet in einem anderen Channel.').

