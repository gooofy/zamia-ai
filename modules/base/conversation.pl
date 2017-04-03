% prolog

%
% very basic conversational building blocks
%

answer(topic, en) :-
    say_eoa(en, 'We have had many topics.'), 
    say_eoa(en, 'We were talking about you for the most part, I believe.').

answer(topic, de) :-
    say_eoa(de, 'Wir hatten schon viele Themen.'), 
    say_eoa(de, 'Ich glaube vor allem über Dich!').

answer(topic, en) :-
    context_score(topic, ENTITY, 100, S),
    rdf (limit(1),
         ENTITY, rdfs:label, LABEL,
         filter (lang(LABEL) = 'en')),
    say_eoa(en, format_str('We were talking about %s.', LABEL), S).

answer(topic, de) :-
    context_score(topic, ENTITY, 100, S),
    rdf (limit(1),
         ENTITY, rdfs:label, LABEL,
         filter (lang(LABEL) = 'de')),
    say_eoa(de, format_str('Wir hatten über %s gesprochen.', LABEL), S).

nlp_gen(en, '@SELF_ADDRESS_EN:LABEL What were we talking about (again|)?', answer(topic, en)).
nlp_gen(en, '@SELF_ADDRESS_EN:LABEL (Which|What) was our Topic (again|)?', answer(topic, en)).
nlp_gen(en, '@SELF_ADDRESS_EN:LABEL Give me a hint', answer(topic, en)).
nlp_gen(en, '@SELF_ADDRESS_EN:LABEL Which topic did we have (again|)?', answer(topic, en)).
nlp_gen(en, '@SELF_ADDRESS_EN:LABEL I (think|believe) I lost my train of thought (just now|).', answer(topic, en)).
nlp_gen(en, '@SELF_ADDRESS_EN:LABEL (lets get|) Back to our topic', answer(topic, en)).
nlp_gen(en, '@SELF_ADDRESS_EN:LABEL (uh|) now for a different subject!', 'What would you like to talk about?').

nlp_gen(de, '@SELF_ADDRESS_DE:LABEL Worüber haben wir (eben|) gesprochen?', answer(topic, de)).
nlp_gen(de, '@SELF_ADDRESS_DE:LABEL (Wie|Was) war (doch gleich|gleich|) unser Thema?', answer(topic, de)).
nlp_gen(de, '@SELF_ADDRESS_DE:LABEL Hilf mir auf die Sprünge?', answer(topic, de)).
nlp_gen(de, '@SELF_ADDRESS_DE:LABEL Welches Thema hatten wir (doch gleich|)?', answer(topic, de)).
nlp_gen(de, '@SELF_ADDRESS_DE:LABEL Ich (glaub|glaube|) ich habe (jetzt|) den Faden verloren.', answer(topic, de)).
nlp_gen(de, '@SELF_ADDRESS_DE:LABEL jetzt habe ich (glaube ich|) den Faden verloren.', answer(topic, de)).
nlp_gen(de, '@SELF_ADDRESS_DE:LABEL also zurück zum thema', answer(topic, de)).
nlp_gen(de, '@SELF_ADDRESS_DE:LABEL (ach|) (jetzt ein|mal ein|) anderes thema', 'Worüber möchtest Du sprechen?').

