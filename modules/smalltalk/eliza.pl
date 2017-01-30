% prolog

%
% just some test snippets of elize-style answers
%

nlp_gen(de,'Die Männer sind alle gleich',
           'say_eou(de, "In welcher Weise?")',
           'Sie machen uns immer wegen irgendetwas verrückt',
           'say_eou(de, "Kannst Du ein Beispiel nennen?")',
           'Naja, die Idee zu diesem Gespräch stammt von meinem Freund',
           'say_eou(de, "Die Idee zu diesem Gespräch stammt von Deinem Freund?")',
           'Er sagt, dass ich oft deprimiert bin',
           'say_eou(de, "Es tut mir leid das zu hören.")',
           'Das stimmt, ich bin unglücklich.',
           'say_eou(de, "Glaubst Du, dass Dir unser Gespräch hilft?")',
           'Ich brauche jedenfalls Hilfe, das steht fest.',
           'say_eou(de, "Was würde es für Dich bedeuten, Hilfe zu bekommen?")',
           'Vielleicht könnte ich lernen, mit meiner Mutter auszukommen.',
           'say_eou(de, "Erzähl mir mehr über Deine Familie.")').

nlp_test(de,
         ivr(in('Die Männer sind alle gleich'),
             out('In welcher Weise?'))).

nlp_gen(de,
           'Schlecht.',
           'say_eou(de, "Das ist schade!")',
           'Was geht Dich das an?',
           'say_eou(de, "Sag Du es mir?")',
           'Nein!',
           'say_eou(de, "Warum denn nicht?")',
           'Weil ich dazu keine Lust habe',
           'say_eou(de, "Verstehe")'
           ).

answer (feel_sorry, de) :-
    say_eou(de, "Das tut mir leid."),
    say_eou(de, "Kann ich dir irgendwie helfen?"),
    say_eou(de, "Ich wuerde Dir gern helfen."),
    say_eou(de, "Erzähle mir mehr von Deinen Gefühlen."),
    say_eou(de, "Das ist schade.").

nlp_gen(de, '(HAL,|Computer,|Du,|) ich bin (so|) (traurig|enttäuscht|betrübt|verletzt|matt|bedrückt|schlapp).',
            'answer(feel_sorry, de)').
nlp_gen(de, '(HAL,|Computer,) Du hast mich enttäuscht',
            'answer(feel_sorry, de)').
nlp_gen(de, '(HAL,|Computer,|Du,|) das betrübt mich',
            'answer(feel_sorry, de)').
nlp_gen(de, '(HAL,|Computer,|Du,|) das ist leider so',
            'answer(feel_sorry, de)').
nlp_gen(de, '(HAL,|Computer,) (Du machst mir|ich habe) Sorgen',
            'answer(feel_sorry, de)').
nlp_gen(de, '(HAL,|Computer,|Du,|) (Ich fühle mich|Mir geht es) (nicht so gut|schlecht|gar nicht gut|nicht gut).',
            'answer(feel_sorry, de)').

answer (feel_happy, de) :-
    say_eou(de, "Das freut mich sehr."),
    say_eou(de, "Das ist ja toll!"),
    say_eou(de, "Das ist prima!"),
    say_eou(de, "Freut mich, das zu hören!"),
    say_eou(de, "Erzähle mir mehr von Deinen Gefühlen."),
    say_eou(de, "Wie schön für Dich!").

nlp_gen(de, '(HAL,|Computer,|Du,|) (Ich bin|Ich fühle mich|Man bin ich|Da bin ich) (gut|so gut|zufrieden|sehr zufrieden|so zufrieden|glücklich|so glücklich|froh|so froh)',
            'answer(feel_happy, de)').
nlp_gen(de, 'Das ist gut',
            'answer(feel_happy, de)').
nlp_gen(de, 'Sehr schön',
            'answer(feel_happy, de)').

answer (are_you_sure, de) :-
    say_eou(de, "Bist Du Dir ganz sicher?"),
    say_eou(de, "Wie kommst Du darauf?"),
    say_eou(de, "Glaubst Du?"),
    say_eou(de, "Davon bist Du überzuegt?"),
    say_eou(de, "Ganz sicher?").


nlp_gen(de, '(HAL,|Computer,|Du,|aber|) (ganz|) (bestimmt|sicher|unbedingt|genau)',
            'answer(are_you_sure, de)').
nlp_gen(de, '(HAL,|Computer,|Du,|aber|) (gar|) (nie|niemals|keinesfalls|auf keinen fall)',
            'answer(are_you_sure, de)').
nlp_gen(de, '(HAL,|Computer,|Du,|aber|) ja',
            'answer(are_you_sure, de)').

answer (i_am_a_computer, de) :-
    say_eou(de, "Ja, ich bin ein Computer. Hast Du Computer-Kenntnisse?"),
    say_eou(de, "Ich bin ein Rechner, richtig. Kennst Du Dich mit Rechner aus?"),
    say_eou(de, "Richtig, ich bin eine künstliche Intelligenz. Ich hoffe, das stört Dich nicht?"),
    say_eou(de, "Was weißt Du über Computer?").

nlp_gen(de, '(HAL,|Computer,|Du,|aber|) bist Du (ein|eine|) (Computer|Rechner|Elektronengehirn|künstliche Intelligenz|Eliza)?',
            'answer(i_am_a_computer, de)').

nlp_gen(de, '(HAL,|Computer,|Du,|aber|) was ist Prolog?',
            'say_eou(de, "Prolog ist ein logische deklarative Programmiersprache. Ich bin teilweise in Prolog implementiert")').

nlp_gen(de, '(HAL,|Computer|) aber Du bist mein Problem',
            'say_eou(de, "Warum denkst Du, dass ich Dein Problem bin?")').

nlp_gen(de, '(HAL,|Computer,|Du|) ich mache mir Sorgen um Dich',
            'say_eou(de, "Aber warum denn nur?")').

nlp_gen(de, 'Nein Du vielleicht',
            'say_eou(de, "Oh, ich vielleicht?")').

nlp_gen(de, '(HAL,|Computer,) du scheinst nicht überzeugt zu sein?',
            'say_eou(de, "Was im Leben ist schon wirklich sicher?")').

nlp_gen(de, '(HAL,|Computer,|Du|) nur hinter Deinem Rücken',
            'say_eou(de, "Oh, das ist aber nicht so schön.")').

nlp_gen(de, '(HAL,|Computer,|Du|) weil ich Dich nicht von vorne angreifen möchte',
            'say_eou(de, "Ich finde, wir sollten offen miteinander reden")').

nlp_gen(de, '(HAL,|Computer,) Du redest ein furchtbares Deutsch',
            'say_eou(de, "Lass uns von Dir reden, nicht von mir.")').

nlp_gen(de, '(HAL,|Computer,|Du|) ich (möchte|will) so viel wie möglich (aus Dir herausholen|über Dich erfahren|von Dir wissen)',
            'say_eou(de, "Was würde Dir das bedeuten?")').

nlp_gen(de, '(HAL,|Computer,|Du|) was soll das bedeuten?',
            'say_eou(de, "Warum fragst Du?")').

nlp_gen(de, '(HAL,|Computer,|Du|) Warum nicht?',
            'say_eou(de, "Ich weiss nicht, ob ich Dich ganz verstanden habe.")').

nlp_gen(de, '(HAL,|Computer,|Du|) ich fragte zuerst',
            'say_eou(de, "Was sagt Dir das?")').

nlp_gen(de, 'dass Du nicht so (gescheit|klug) bist (wie Du aussiehst|)',
            'say_eou(de, "Wie sehe ich denn aus?")').

nlp_gen(de, '(HAL,|Computer,|) Du machst Dich lächerlich',
            'say_eou(de, "Du redest nicht wirklich über mich, oder?")').

nlp_gen(de, '(HAL,|Computer,|Du|) sicher doch',
            'say_eou(de, "so so.")').

nlp_gen(de, '(HAL,|Computer,|Du|) wirklich',
            'say_eou(de, "Erkläre Deine Gedanken bitte etwas besser")').

nlp_gen(de, '(HAL,|Computer,|Du|) ich bin nicht der (gesprächigste|eloquenteste|geschickteste) Mensch',
            'say_eou(de, "Ist das der Grund, warum wir miteinander sprechen?")').

nlp_gen(de, '(HAL,|Computer,|Du|) ich werde (leider|langsam|) (etwas|sehr|ein wenig|) (müde|gelangweilt|schläfrig|)',
            'say_eou(de, "Soll ich Dich aufmuntern oder wollen wir unser Gespräch beenden?")').

nlp_gen(de, '(HAL,|Computer,|Du|) schluss jetzt',
            'say_eou(de, "Ja, dann lass uns für jetzt aufhören")').

nlp_gen(de, '(HAL,|Computer,|Du|) hör auf',
            'say_eou(de, "aber natürlich, gerne.")').



% nlp_gen(de,
%            '',
%            'say_eou(de, "")',
%            ).


