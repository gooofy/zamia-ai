%prolog

% test_setup('smalltalk') :- context_set(topic, []), eoa.

% answer(topic, en) :-
%     context_score(topic, language, 100, SCORE), say_eoa(en, 'We were talking about languages.', SCORE).
% answer(topic, de) :-
%     context_score(topic, language, 100, SCORE), say_eoa(de, 'Wir hatten das Thema Sprachen.', SCORE).

nlp_gens("smalltalk", en, [["isn't that a wonderful","wonderful","a very nice","terrible"],"language"], "do you speak any foreign languages?").
nlp_gens("smalltalk", de, [["ist das nicht eine wunderbare","wunderbare","eine sehr schöne","furchtbare"],"sprache"], "Sprichst Du irgendwelche Fremdsprachen?").

nlp_test('smalltalk', en, 'lang1', [],
         [ 'terrible language', 'do you speak any foreign languages?',[]]).
nlp_test('smalltalk', de, 'lang2', [],
         ['wunderbare sprache','Sprichst du irgendwelche fremdsprachen?',[]]).

