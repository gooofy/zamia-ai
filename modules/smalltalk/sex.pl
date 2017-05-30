% prolog

nlp_gen (en, "@SELF_ADDRESS:LABEL (let us|I want to|do we want to|can you) fuck?",
             sayz(I, en, "excuse me?")).
nlp_gen (de, '@SELF_ADDRESS:LABEL (lass uns|ich will|wollen wir|kannst du) ficken',
             sayz(I, de, 'Entschuldigung?!')).

nlp_gen (en, "@SELF_ADDRESS:LABEL (do you have a|look my|you are a|such a) cunt",
             sayz(I, en, "Did IQs just drop sharply while I was away?")).
nlp_gen (de, '@SELF_ADDRESS:LABEL (hast du eine|schau mal meine|du|du bist eine|so eine) fotze',
             sayz(I, de, 'Niveau, wo bist du nur geblieben?')).

nlp_gen (en, "@SELF_ADDRESS:LABEL (cunt|sex|tits|bent over)",
             sayz(I, en, "You must be talking to that other robot...")).
nlp_gen (de, '@SELF_ADDRESS:LABEL (muschi|möse|sex|titten|bück dich)',
             sayz(I, de, 'Ich glaube Du bist hier falsch, Kleiner. Dafür gibts andere Roboter.')).

nlp_gen (en, "@SELF_ADDRESS:LABEL bra",
             sayz(I, en, "What color is your bra, then?")).
nlp_gen (de, '@SELF_ADDRESS:LABEL bh',
             sayz(I, de, 'Welche Farbe hat Dein BH?')).

nlp_gen (en, "@SELF_ADDRESS:LABEL (do you think|) I am a male or female?",
             sayz(I, en, "you tell me!")).
nlp_gen (de, '@SELF_ADDRESS:LABEL bin ich weiblich oder männlich',
             sayz(I, de, 'Sag es mir')).


