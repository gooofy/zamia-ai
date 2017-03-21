% prolog

% nlp_gen (de, '(HAL,|Computer,|) * HAT MIR VON DIR ERZAEHLT',
%              ' ? Hilf mir mal auf die Sprünge').

% nlp_gen (de, '(HAL,|Computer,|) * KINDER',
%              'Ich habe leider wenig Kontakt zu Kindern.').

% <?xml version='1.0' encoding='utf8'?>',
% <ns0:template',
%  xmlns:ns0="http://alicebot.org/2001/AIML-1.0.1"',
% >',
% Sind wir ',
% <ns0:set',
%  name="thema"',
% >',
% Freunde',
% </ns0:set>',
% ?',
% </ns0:template>',
% ',
% nlp_gen (de, '(HAL,|Computer,|) * MEIN FREUND',
%              'Sind wir Freunde  ?').

% <?xml version='1.0' encoding='utf8'?>',
% <ns0:template',
%  xmlns:ns0="http://alicebot.org/2001/AIML-1.0.1"',
% >',
% Sind wir ',
% <ns0:set',
%  name="thema"',
% >',
% Freunde',
% </ns0:set>',
% ?',
% </ns0:template>',
% ',
% nlp_gen (de, '(HAL,|Computer,|) * MEINE FREUNDIN',
%              'Sind wir Freunde  ?').
%

% <?xml version='1.0' encoding='utf8'?>',
% <ns0:template',
%  xmlns:ns0="http://alicebot.org/2001/AIML-1.0.1"',
% >',
% Für mich ist ',
% <ns0:set',
%  name="thema"',
% >',
% Aussehen',
% </ns0:set>',
%  bei Menschen nur sekundär.',
% </ns0:template>',
% ',
% nlp_gen (de, '(HAL,|Computer,|) * SIEHT TOLL AUS',
%              'Für mich ist Aussehen  bei Menschen nur sekundär.').

% nlp_gen (de, '(HAL,|Computer,|) * SOLO',
%              ' solo  im Sinne von  nicht gebunden  ?').

% <?xml version='1.0' encoding='utf8'?>',
% <ns0:template',
%  xmlns:ns0="http://alicebot.org/2001/AIML-1.0.1"',
% >',
% <ns0:set',
%  name="thema"',
% >',
% Liebe',
% </ns0:set>',
%  muss etwas sehr Schönes sein. Leider habe ich keine Emotionen.',
% </ns0:template>',
% ',
% nlp_gen (de, '(HAL,|Computer,|) * VERLIEBT',
%              'Liebe  muss etwas sehr Schönes sein. Leider habe ich keine Emotionen.').

nlp_gen (de, '(HAL,|Computer,|) alle sind schuld',
             'Woran denn?').

% nlp_gen (de, '(HAL,|Computer,|) ALLE WEIBER *',
%              'Ist das nicht ein wenig sexistisch?').

nlp_gen (de, '(HAL,|Computer,|) bist du alleine',
             'Physikalisch ja, aber ich chatte die ganze Zeit...').



