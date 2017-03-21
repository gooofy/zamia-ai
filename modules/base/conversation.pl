% prolog

%
% very basic conversational building blocks
%

answer(topic, de) :-
    say_eoa(de, 'Wir hatten schon viele Themen.'), 
    say_eoa(de, 'Ich glaube vor allem über Dich!').

answer(topic, de) :-
    context_score(topic, ENTITY, 100, S),
    rdf (limit(1),
         ENTITY, rdfs:label, LABEL,
         filter (lang(LABEL) = 'de')),
    say_eoa(de, format_str('Wir hatten über %s gesprochen.', LABEL), S).

nlp_gen(de, '(HAL,|Computer,|) Worüber haben wir (eben|) gesprochen?', answer(topic, de)).
nlp_gen(de, '(HAL,|Computer,|) (Wie|Was) war (doch gleich|gleich|) unser Thema?', answer(topic, de)).
nlp_gen(de, '(HAL,|Computer,|) Hilf mir auf die Sprünge?', answer(topic, de)).
nlp_gen(de, '(HAL,|Computer,|) Welches Thema hatten wir (doch gleich|)?', answer(topic, de)).
nlp_gen(de, '(HAL,|Computer,|) Ich (glaub|glaube|) ich habe (jetzt|) den Faden verloren.', answer(topic, de)).
nlp_gen(de, '(HAL,|Computer,|) jetzt habe ich (glaube ich|) den Faden verloren.', answer(topic, de)).

