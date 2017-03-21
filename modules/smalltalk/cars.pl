% prolog

nlp_gen (de, '(HAL,|Computer,|) (ohje, mein | ich fuhr mit dem | ich mache mir sorgen um mein | ich brauche ein neues | cool, ein) (Auto|Wagen|Kraftfahrzeug)',
             'Was für einen Wagen fährst Du?', 'Welche Marke?', 'Hast Du auch ein Fahrrad?').

nlp_gen (de, '(HAL,|Computer,|) auto fahren',
             'Denkst Du dabei auch an die Umwelt?').

% <?xml version='1.0' encoding='utf8'?>',
% <ns0:template',
%  xmlns:ns0="http://alicebot.org/2001/AIML-1.0.1"',
% >',
% Eines Tages werden die Leute keine ',
% <ns0:set',
%  name="thema"',
% >',
% Autos',
% </ns0:set>',
%  mehr brauchen.',
% </ns0:template>',
% ',
% nlp_gen (de, '(HAL,|Computer,|) AUTOS *',
%              'Eines Tages werden die Leute keine Autos  mehr brauchen.').


