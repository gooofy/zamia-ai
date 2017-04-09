%prolog

answer(topic, en) :-
    context_score(topic, language, 100, SCORE), say_eoa(en, 'We were talking about languages.', SCORE).
answer(topic, de) :-
    context_score(topic, language, 100, SCORE), say_eoa(de, 'Wir hatten das Thema Sprachen.', SCORE).

% <?xml version='1.0' encoding='utf8'?>',
% <ns0:template',
%  xmlns:ns0="http://alicebot.org/2001/AIML-1.0.1"',
% >',
% Sprichst Du irgendwelche ',
% <ns0:set',
%  name="thema"',
% >',
% Fremdsprachen',
% </ns0:set>',
% ?',
% </ns0:template>',
% ',
% nlp_gen (de, '(HAL,|Computer,|) * SPRACHE',
%              'Sprichst Du irgendwelche Fremdsprachen  ?').

