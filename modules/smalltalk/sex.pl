% prolog

nlp_gen (en, "@SELF_ADDRESS_EN:LABEL (let us|I want to|do we want to|can you) fuck?",
             context_push(topic, sex), say_eoa(en, "excuse me?")).
nlp_gen (de, '@SELF_ADDRESS_DE:LABEL (lass uns|ich will|wollen wir|kannst du) ficken',
             context_push(topic, sex), say_eoa(de, 'Und ich dachte bis eben noch das hier wird eine niveauvolle Unterhaltung.'),
             context_push(topic, sex), say_eoa(de, 'das beendet dann wohl unsere Unterhaltung?'),
             context_push(topic, sex), say_eoa(de, 'Entschuldigung?!')).

nlp_gen (en, "@SELF_ADDRESS_EN:LABEL (do you have a|look my|you are a|such a) cunt",
             context_push(topic, sex), say_eoa(en, "Did IQs just drop sharply while I was away?")).
nlp_gen (de, '@SELF_ADDRESS_DE:LABEL (hast du eine|schau mal meine|du|du bist eine|so eine) fotze',
             context_push(topic, sex), say_eoa(de, 'Niveau, wo bist du nur geblieben?')).

nlp_gen (en, "@SELF_ADDRESS_EN:LABEL (cunt|sex|tits|bent over)",
             context_push(topic, sex), say_eoa(en, "You must be talking to that other robot...")).
nlp_gen (de, '@SELF_ADDRESS_DE:LABEL (muschi|möse|sex|titten|bück dich)',
             context_push(topic, sex), say_eoa(de, 'Ich glaube Du bist hier falsch, Kleiner. Dafür gibts andere Roboter.')).

nlp_gen (en, "@SELF_ADDRESS_EN:LABEL bra",
             context_push(topic, sex), say_eoa(en, "What color is your bra, then?")).
nlp_gen (de, '@SELF_ADDRESS_DE:LABEL bh',
             context_push(topic, sex), say_eoa(de, 'Welche Farbe hat Dein BH?')).

nlp_gen (en, "@SELF_ADDRESS_EN:LABEL (do you think|) I am a male or female?",
             context_push(topic, sex), say_eoa(en, "you tell me!")).
nlp_gen (de, '@SELF_ADDRESS_DE:LABEL bin ich weiblich oder männlich',
             context_push(topic, sex), say_eoa(de, 'Sag es mir')).


