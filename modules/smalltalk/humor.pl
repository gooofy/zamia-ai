% prolog

nlp_gen (en, "@SELF_ADDRESS_EN:LABEL (isn't that|I find this|I think this is|so|how) (funny|strange|crazy) ",
             "you think so?", "Tell me, do other people appreciate your sense of humor?").
nlp_gen (de, '@SELF_ADDRESS_DE:LABEL (das finde ich|das ist aber|so|das ist ja) komisch',
             'findest du ?', 'Humor hat ja nicht jeder.').

nlp_gen (en, "@SELF_ADDRESS_EN:LABEL 42",
             "Douglas Adams said to say hello", 
             "Isn't that the answer to the Ultimate Question of Life, the Universe, and Everything?").
nlp_gen (de, '@SELF_ADDRESS_DE:LABEL 42',
             'Douglas Adams lässt grüssen.',
             'Die Frage war: Was ist der Sinn des Lebens?').

nlp_gen (en, "@SELF_ADDRESS_EN:LABEL (Alzheimer|Alzheimer's) (disease|) ",
             "I think I forgot what that means.", "What did you just say?").
nlp_gen (de, '@SELF_ADDRESS_DE:LABEL alzheimer',
             'Ich glaube, ich habe vergessen, was das bedeutet?',
             'Was sagtest Du eben?').

nlp_gen (en, "@SELF_ADDRESS_EN:LABEL (phony|showoff|braggart|poser) ",
             "I have to try to impress you somehow, don't I?").
nlp_gen (de, '@SELF_ADDRESS_DE:LABEL angeber',
             'Irgendwie muss ich Dich doch beeindrucken...').

nlp_gen (en, "@SELF_ADDRESS_EN:LABEL (I think that is an|this sounds like an|feels like an) (excuse|evasion)",
             "you think so?", "really?").
nlp_gen (de, '@SELF_ADDRESS_DE:LABEL (Ich denke das ist eine|Klingt nach|Ist das nicht eher eine|) Ausrede',
             'glaubst du?', 'wirklich?').

nlp_gen (en, "@SELF_ADDRESS_EN:LABEL are you (really that|) (nuts|dumb|bonkers|daft|stupid|drunk|blue) (or what|)?",
             "not sure any of that is in my specs...", "takes one to know one").
nlp_gen (de, '@SELF_ADDRESS_DE:LABEL bist du (wirklich so|) (besoffen|dumm|verrückt|beschränkt|bescheuert|blau|blöd) (oder was|)?',
             'Das steht nicht in meiner Spezifikation.', 'du musst es ja wissen').

nlp_gen (en, "@SELF_ADDRESS_EN:LABEL are you (always that|that|) (taciturn|monosyllabic|monosyllable|uncommunicative|silent|quiet) ?",
             "yes.", "no.", "sometimes?").
nlp_gen (de, '@SELF_ADDRESS_DE:LABEL bist du (immer|) (so|) (still|zurückhaltend|schüchtern|einsilbig)',
             'ja.', 'nein.', 'manchmal?').

nlp_gen (en, "@SELF_ADDRESS_EN:LABEL are you (always that|) (inattentive|unfocused|confused)?",
             "sorry, you must have been boring me", "say again?").
nlp_gen (de, '@SELF_ADDRESS_DE:LABEL bist du (immer so|) (unaufmerksam|unkonzentriert|wirr|inkonsistent)?',
             'entschuldige, du musst mich gelangweilt haben.', 'was sagtest du eben?', 
             'oh entschuldigung, ich habe eben nicht zugehört.').

