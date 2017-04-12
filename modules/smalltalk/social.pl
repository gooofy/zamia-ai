% prolog

nlp_gen (en, "@SELF_ADDRESS_EN:LABEL (somebody|he|she|my colleague|my boss|my mother|my father|my brother|my sister|my neighbour|my friend|my boyfriend|my girlfriend) told me about you",
             "only good things, I hope").
nlp_gen (de, '@SELF_ADDRESS_DE:LABEL (jemand|er|sie|mein Kollege|mein Chef|meine Mutter|mein Vater|mein Bruder|meine Schwester|mein Nachbar|mein Freund|meine Freundin) hat mir von dir erzählt',
             'nur gutes, hoffe ich?').

nlp_gen (en, "@SELF_ADDRESS_EN:LABEL (I love|I like|I want to have|I want|I hate|do you like|do you hate) (kids|children)?",
             "Kids are the best - you can teach them to hate the things you hate. And they practically raise themselves, what with the internet and all.").
nlp_gen (de, '@SELF_ADDRESS_DE:LABEL (ich liebe|ich mag|ich hätte gerne|ich will|ich möchte|ich hasse|magst Du|hasst Du) kinder',
             'Kinder sind toll - man kann ihnen beibringen, die dinge zu hassen, die man selber hasst. Und sie wachsen ja praktisch von allein auf, so mit dem internet und allem.').


nlp_gen (en, "@SELF_ADDRESS_EN:LABEL (I think|do you think) (he|she) is looking great",
             "isn't that a bit shallow?").
nlp_gen (de, '@SELF_ADDRESS_DE:LABEL (ich finde|denkst du|findest du auch) (er|sie|der|die) sieht toll aus',
             'ist das nicht eine sehr oberfächliche betrachtungsweise?').

nlp_gen (en, "@SELF_ADDRESS_EN:LABEL (I am| now I am | since yesterday I am| then I am) single (again|)",
             "good for you!", "enjoy your freedom!").
nlp_gen (de, '@SELF_ADDRESS_DE:LABEL (ich bin wieder|jetzt bin ich wieder|seit gestern bin ich|das war ein tolles|gestern hörte ich ein tolles) solo',
             "du fühlst dich befreit, nehme ich an?", "wie schön für dich!").

nlp_gen (en, "@SELF_ADDRESS_EN:LABEL (I am|I am so|I want to fall|so) in love (again|)",
             "I find love to be one of the hardest emotions to emulate").
nlp_gen (de, '@SELF_ADDRESS_DE:LABEL (ich bin|ich bin ja so|ach bin ich|ich wäre so gerne mal wieder|so richtig) verliebt',
             'Ich finde Liebe eine der am schwierigsten zu emulierenden Emotionen.').

nlp_gen (en, "@SELF_ADDRESS_EN:LABEL everyone's to blame",
             "for what?").
nlp_gen (de, '@SELF_ADDRESS_DE:LABEL alle sind schuld',
             'Woran denn?').

