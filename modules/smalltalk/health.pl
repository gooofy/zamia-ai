% prolog

nlp_gens(en, '@SELF_ADDRESS:LABEL (I feel|I guess I will be|I think I will be|I am getting|I am) (ill|sick) (maybe|)',
             'how bad is it?', "I am sure you will be better soon!").
nlp_gens(de, '@SELF_ADDRESS:LABEL (ich bin|ich fühle mich|ich glaube ich werde) (vielleicht|) krank',
             'sehr schlimm?', "ich wünsche Dir auf jeden Fall gute Besserung!").

nlp_gens(en, "@SELF_ADDRESS:LABEL (I am in|I have to go to|I don't want to got to the) hospital",
             'that sounds unpleasant', "oh dear that doesn't sound very pleasant, does it?").
nlp_gens(de, '@SELF_ADDRESS:LABEL (ich bin im|ich muss ins|ich will nicht ins) Krankenhaus',
             'Das klingt unangenehm', "ohje, das klingt nicht gut").

