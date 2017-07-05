%prolog

% answer(topic, en) :-
%     context_score(topic, astronomy, 100, SCORE), say_eoa(en, 'We were talking about astronomy.', SCORE).
% answer(topic, de) :-
%     context_score(topic, astronomy, 100, SCORE), say_eoa(de, 'Wir hatten das Thema Astronomie.', SCORE).

nlp_gens("smalltalk", en, [["like",""],["on",""],"the moon"], "ah, the moon. fascinating.").
nlp_gens("smalltalk", de, [["wie","als",""],"auf",["den","dem"],"mond"], "ah, der mond. faszinierend.").
nlp_gens("smalltalk", en, [["on",""],["the",""],"earth"], "the blue planet.").
nlp_gens("smalltalk", de, ["auf der erde"], "der blaue planet.").

