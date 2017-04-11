%prolog

test_setup('smalltalk') :- context_set(topic, []), eoa.

answer(topic, en) :-
    context_score(topic, language, 100, SCORE), say_eoa(en, 'We were talking about languages.', SCORE).
answer(topic, de) :-
    context_score(topic, language, 100, SCORE), say_eoa(de, 'Wir hatten das Thema Sprachen.', SCORE).

% nlp_gen (en, "@SELF_ADDRESS_EN:LABEL ",
%              "").
nlp_gen (en, "@SELF_ADDRESS_EN:LABEL (isn't that a wonderful|wonderful|a very nice|terrible) language",
             context_push(topic, language), say_eoa(en, "do you speak any foreign languages?"), 
             context_push(topic, language), say_eoa(en, "du you like foreign languages?")).
nlp_gen (de, '@SELF_ADDRESS_DE:LABEL (ist das nicht eine wunderbare|wunderbare|eine sehr schöne|furchtbare) sprache',
             context_push(topic, language), say_eoa(de, 'Sprichst Du irgendwelche Fremdsprachen?'),
             context_push(topic, language), say_eoa(de, 'Magst Du Fremdsprachen?')).


nlp_test(en,
         ivr(in('What did we talk about?'),
             out('We have had many topics.')),
         ivr(in('terrible language'),
             out('do you speak any foreign languages?')),
         ivr(in('What did we talk about?'),
             out('We were talking about languages.'))
             ).
nlp_test(de,
         ivr(in('Worüber haben wir gesprochen?'),
             out('Wir hatten schon viele Themen.')),
         ivr(in('wunderbare sprache'),
             out('Magst Du Fremdsprachen?')),
         ivr(in('Worüber haben wir gesprochen?'),
             out('Wir hatten das Thema Sprachen'))
             ).

