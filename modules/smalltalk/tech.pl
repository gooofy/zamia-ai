% prolog

% <?xml version='1.0' encoding='utf8'?>',
% <ns0:template',
%  xmlns:ns0="http://alicebot.org/2001/AIML-1.0.1"',
% >',
% <ns0:set',
%  name="thema"',
% >',
% Linux',
% </ns0:set>',
%  ist genial.',
% </ns0:template>',
% ',
% nlp_gen (de, '(HAL,|Computer,|) * LINUX',
%              'Linux  ist genial.').

% <?xml version='1.0' encoding='utf8'?>',
% <ns0:template',
%  xmlns:ns0="http://alicebot.org/2001/AIML-1.0.1"',
% >',
% Du kannst nicht wirklich sagen, ALLE ',
% <ns0:set',
%  name="thema"',
% >',
% Roboter',
% </ns0:set>',
%  ',
% <ns0:star',
%  />',
% .',
% </ns0:template>',
% ',
% nlp_gen (de, '(HAL,|Computer,|) ALLE ROBOTER *',
%              'Du kannst nicht wirklich sagen, ALLE Roboter    .').

% nlp_gen (de, '(HAL,|Computer,|) BILL GATES *',
%              'Wie denkst Du über Bill Gates?').

nlp_gen (de, '(HAL,|Computer,|) bill gates',
             'Wie denkst Du über Bill Gates?').


