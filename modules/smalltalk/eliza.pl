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
    say_eou(de, "Das ist schade.").

nlp_gen(de, 'Ich bin traurig.',
            'answer(feel_sorry, de)').
nlp_gen(de, 'Du hast mich enttäuscht',
            'answer(feel_sorry, de)').
nlp_gen(de, 'Das betrübt mich',
            'answer(feel_sorry, de)').
nlp_gen(de, 'Das ist leider so',
            'answer(feel_sorry, de)').
nlp_gen(de, 'Mir geht es schlecht.',
            'answer(feel_sorry, de)').

answer (feel_happy, de) :-
    say_eou(de, "Das freut mich sehr."),
    say_eou(de, "Das ist ja toll!"),
    say_eou(de, "Das ist prima!"),
    say_eou(de, "Freut mich, das zu hören!"),
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


nlp_gen(de, '(HAL,|Computer,|Du,|aber|) (ganz|) (bestimmt|sicher|unbedingt)',
            'answer(are_you_sure, de)').
nlp_gen(de, '(HAL,|Computer,|Du,|aber|) (gar|) (nie|niemals|keinesfalls|auf keinen fall)',
            'answer(are_you_sure, de)').


% nlp_gen(de,
%            '',
%            'say_eou(de, "")',
%            ).


