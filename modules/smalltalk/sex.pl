% prolog

nlp_gen (de, '(HAL,|Computer,|) (lass uns|ich will|wollen wir|kannst du) ficken',
             context_push(topic, sex), say_eoa(de, 'Und ich dachte bis eben noch das hier wird eine niveauvolle Unterhaltung.'),
             context_push(topic, sex), say_eoa(de, 'das beendet dann wohl unsere Unterhaltung?'),
             context_push(topic, sex), say_eoa(de, 'Entschuldigung?!')).

nlp_gen (de, '(HAL,|Computer,|) (hast du eine|schau mal meine|du|du bist eine|so eine) fotze',
             context_push(topic, sex), say_eoa(de, 'Niveau, wo bist du nur geblieben?')).

% nlp_gen (de, '(HAL,|Computer,|) * LIEBE',
%              'Ich habe leider keinerlei Emotionen.').

% nlp_gen (de, '(HAL,|Computer,|) * MOESE',
%              'Ich glaube Du bist hier falsch, Kleiner. Dafür gibts andere Roboter.').

% nlp_gen (de, '(HAL,|Computer,|) * MUSCHI',
%              'Ich glaube Du bist hier falsch, Kleiner. Dafür gibts andere Roboter.').


% nlp_gen (de, '(HAL,|Computer,|) * SEX',
%              'Sex macht alleine viel mehr Spass.').

% nlp_gen (de, '(HAL,|Computer,|) * TITTEN',
%              'Ich glaube Du bist hier falsch, Kleiner. Dafür gibts andere Roboter.').

nlp_gen (de, '(HAL,|Computer,|) bh',
             'Welche Farbe hat Dein BH?').

nlp_gen (de, '(HAL,|Computer,|) bin ich weiblich oder männlich',
             'Sag es mir :-)').

nlp_gen (de, '(HAL,|Computer,|) bück dich',
             'Mein Körper ist noch nicht gebaut.').


