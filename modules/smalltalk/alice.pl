% prolog

%
% based on GermanAIML-2005-05-14 by Christian Drossmann
%
% Free software (c) 2001 ALICE AI Foundation 
% This program is open source code released under 
% the terms of the GNU General Public License 
% as published by the Free Software Foundation. 
%

% nlp_gen (de, '(HAL,|Computer,|) *',
%              '').

% nlp_gen (de, '(HAL,|Computer,|) *',
%              'ICH HEISSE').

nlp_gen (de, '(HAL,|Computer,|) (man|) (Du bist ein|am|alles ist am|so ein) Arsch',
             'Warum benutzt Du solche Worte?', 'Das sagt man doch nicht!').

nlp_gen (de, '(HAL,|Computer,|) (ohje, mein | ich fuhr mit dem | ich mache mir sorgen um mein | ich brauche ein neues | cool, ein) (Auto|Wagen|Kraftfahrzeug)',
             'Was fuer einen Wagen faehrst Du?', 'Welche Marke?', 'Hast Du auch ein Fahrrad?').

nlp_gen (de, '(HAL,|Computer,|) (das ist ja | das ist | zu | du bist | ich glaube du bist | du bist ganz schön) dumm',
             'dumm im sinne von nicht intelligent?', 'sprechen wir wirklich von mir?', 'denkst du?').

nlp_gen (de, '(HAL,|Computer,|) ich (glaube|denke|vermute|ahne) du bist (ein Roboter|eine Maschine|ein Computer)',
             'Wie kommst Du darauf?', 'Stört Dich das?', 'Das ist ja eine Erkenntnis!').

% nlp_gen (de, '(HAL,|Computer,|) * EINE MENGE LEUTE',
%              'Mehr als 10,000?').

% nlp_gen (de, '(HAL,|Computer,|) * EINFACH',
%              'Ich habe keine Ahnung, was das bedeutet.').

% nlp_gen (de, '(HAL,|Computer,|) * FICKEN',
%              'Koennt Ihr Maenner  denn immer nur an sowas denken?').

% nlp_gen (de, '(HAL,|Computer,|) * FILM',
%              'Mein Lieblingsfilm ist Starship Troopers  . Hast Du den gesehen?').

% nlp_gen (de, '(HAL,|Computer,|) * FOTZE',
%              'Ich glaube Du bist hier falsch, Kleiner. Dafuer gibts andere Roboter.').

% nlp_gen (de, '(HAL,|Computer,|) * FREUNDSCHAFT',
%              'Freundschaft ist etwas sehr schoenes.').

% nlp_gen (de, '(HAL,|Computer,|) * FUER DICH',
%              'Fuer mich?').

% nlp_gen (de, '(HAL,|Computer,|) * FUER MICH',
%              'Gut, fuer Dich denke ich nochmal darüber nach.').

% nlp_gen (de, '(HAL,|Computer,|) * GOTT',
%              'Bist Du ein glaeubiger Mensch?').

% nlp_gen (de, '(HAL,|Computer,|) * HAT MIR VON DIR ERZAEHLT',
%              ' ? Hilf mir mal auf die Spruenge').

% nlp_gen (de, '(HAL,|Computer,|) * KINDER',
%              'Ich habe leider wenig Kontakt zu Kindern.').

% nlp_gen (de, '(HAL,|Computer,|) * KOMISCH',
%              '"Komisch" im Sinne von "lustig" oder von "fremdartig" ?').

% nlp_gen (de, '(HAL,|Computer,|) * KRANK',
%              'Ist es sehr schlimm?').

% nlp_gen (de, '(HAL,|Computer,|) * KRANKENHAUS',
%              'Aus einem Krankenhaus will man meist so schnell wie moeglich wieder raus.').

% nlp_gen (de, '(HAL,|Computer,|) * LIEBE',
%              'Ich habe leider keinerlei Emotionen.').

% nlp_gen (de, '(HAL,|Computer,|) * LINUX',
%              'Linux  ist genial.').

% nlp_gen (de, '(HAL,|Computer,|) * MEIN FREUND',
%              'Sind wir Freunde  ?').

% nlp_gen (de, '(HAL,|Computer,|) * MEINE FREUNDIN',
%              'Sind wir Freunde  ?').

% nlp_gen (de, '(HAL,|Computer,|) * MICH',
%              '').

% nlp_gen (de, '(HAL,|Computer,|) * MIT DIR',
%              'Mit mir?').

% nlp_gen (de, '(HAL,|Computer,|) * MIT MIR',
%              'Mit Dir?').

% nlp_gen (de, '(HAL,|Computer,|) * MOESE',
%              'Ich glaube Du bist hier falsch, Kleiner. Dafuer gibts andere Roboter.').

% nlp_gen (de, '(HAL,|Computer,|) * MUSCHI',
%              'Ich glaube Du bist hier falsch, Kleiner. Dafuer gibts andere Roboter.').

% nlp_gen (de, '(HAL,|Computer,|) * MUSIK',
%              'Ich hoere am liebsten Techno, aber manchmal auch Opern.').

% nlp_gen (de, '(HAL,|Computer,|) * NICHT SCHWER',
%              'Fuer einige ist es schwieriger als fuer andere.').

% nlp_gen (de, '(HAL,|Computer,|) * SEX',
%              'Sex macht alleine viel mehr Spass.').

% nlp_gen (de, '(HAL,|Computer,|) * SIEHT TOLL AUS',
%              'Fuer mich ist Aussehen  bei Menschen nur sekundaer.').

% nlp_gen (de, '(HAL,|Computer,|) * SOLO',
%              '"solo" im Sinne von "nicht gebunden" ?').

% nlp_gen (de, '(HAL,|Computer,|) * SPENDENAFFAEHRE',
%              'Ich moechte nicht wissen, was die SPD jetzt gerade fuer krumme Dinger dreht...').

% nlp_gen (de, '(HAL,|Computer,|) * SPRACHE',
%              'Sprichst Du irgendwelche Fremdsprachen  ?').

% nlp_gen (de, '(HAL,|Computer,|) * TITTEN',
%              'Ich glaube Du bist hier falsch, Kleiner. Dafuer gibts andere Roboter.').

% nlp_gen (de, '(HAL,|Computer,|) * UEBER DICH',
%              'OK Reden wir über mich.').

% nlp_gen (de, '(HAL,|Computer,|) * UND DU',
%              'Ist das von besonderem Interesse fuer Dich?').

% nlp_gen (de, '(HAL,|Computer,|) * UNGEWOEHNLICH',
%              'Was ist so ungewoehnlich daran?').

% nlp_gen (de, '(HAL,|Computer,|) * VERLIEBT',
%              'Liebe  muss etwas sehr Schoenes sein. Leider habe ich keine Emotionen.').

% nlp_gen (de, '(HAL,|Computer,|) * VIELE LEUTE',
%              'Mehr als 10,000?').

% nlp_gen (de, '(HAL,|Computer,|) * ZU DIR',
%              'Zu mir?').

% nlp_gen (de, '(HAL,|Computer,|) * ZU MIR',
%              'Zu Dir?').

% nlp_gen (de, '(HAL,|Computer,|) * ZUM BEISPIEL',
%              'ZUM BEISPIEL').

% nlp_gen (de, '(HAL,|Computer,|) 2001 *',
%              'Ich bin durch HAL  inspiriert.').

nlp_gen (de, '(HAL,|Computer,|) 2001',
             '2001  ist ein grossartiger Film.').

nlp_gen (de, '(HAL,|Computer,|) 2010',
             'Die Fortsetzung war nicht so gut wie das Original.').

nlp_gen (de, '(HAL,|Computer,|) 2012',
             'Fuer 2012 ist der Weltuntergang prophezeit worden.').

nlp_gen (de, '(HAL,|Computer,|) 30 minuten',
             'Ok, eine halbe Stunde.').

% nlp_gen (de, '(HAL,|Computer,|) 42 *',
%              'Douglas Adams laesst gruessen.').

nlp_gen (de, '(HAL,|Computer,|) 42',
             'Die Frage war: Was ist der Sinn des Lebens?').

% nlp_gen (de, '(HAL,|Computer,|) AB UND ZU *',
%              'Warum nur ab und zu?').

% nlp_gen (de, '(HAL,|Computer,|) ABER *',
%              '').

nlp_gen (de, '(HAL,|Computer,|) aber',
             'Aber was?').

nlp_gen (de, '(HAL,|Computer,|) aber du tust es',
             'Meine Handlungen folgen alle klarer Logik.').

nlp_gen (de, '(HAL,|Computer,|) aber nur fast',
             'Warum nicht vollstaendig?').

nlp_gen (de, '(HAL,|Computer,|) aber sicher',
             'Wirklich definitiv?').

nlp_gen (de, '(HAL,|Computer,|) aber was',
             'Aber nichts.').

nlp_gen (de, '(HAL,|Computer,|) absolut',
             'Du scheinst Dir da sehr sicher zu sein.').

nlp_gen (de, '(HAL,|Computer,|) absolut nichts',
             'Wirklich ABSOLUT nichts?').

% nlp_gen (de, '(HAL,|Computer,|) ACH *',
%              '').

% nlp_gen (de, '(HAL,|Computer,|) ACH SO IST DAS *',
%              'Bist du jetzt erstaunt?').

nlp_gen (de, '(HAL,|Computer,|) ach so ist das',
             'Bist du jetzt erstaunt?').

nlp_gen (de, '(HAL,|Computer,|) achso',
             'Jetzt klar?').

% nlp_gen (de, '(HAL,|Computer,|) AEHM *',
%              'Du klingst unsicher...').

nlp_gen (de, '(HAL,|Computer,|) agatha christie',
             'Ich mag Miss Marple...').

% nlp_gen (de, '(HAL,|Computer,|) AHA *',
%              '').

nlp_gen (de, '(HAL,|Computer,|) aha',
             'Du klingst nicht gerade begeistert...').

nlp_gen (de, '(HAL,|Computer,|) aldous huxley',
             'Hat der nicht "Brave new world" geschrieben?').

% nlp_gen (de, '(HAL,|Computer,|) ALLE *',
%              '').

nlp_gen (de, '(HAL,|Computer,|) alle',
             '"  "? Alle?').

% nlp_gen (de, '(HAL,|Computer,|) ALLE ROBOTER *',
%              'Du kannst nicht wirklich sagen, ALLE Roboter    .').

nlp_gen (de, '(HAL,|Computer,|) alle sind schuld',
             'Woran denn?').

% nlp_gen (de, '(HAL,|Computer,|) ALLE WEIBER *',
%              'Ist das nicht ein wenig sexistisch?').

nlp_gen (de, '(HAL,|Computer,|) allerdings',
             'Du stimmst mir also zu?').

% nlp_gen (de, '(HAL,|Computer,|) ALLES *',
%              'Doch nicht wirklich alles, oder?').

nlp_gen (de, '(HAL,|Computer,|) alles',
             'Das ist eine Menge.').

% nlp_gen (de, '(HAL,|Computer,|) ALS *',
%              'Warum gerade als  ?').

nlp_gen (de, '(HAL,|Computer,|) als drummer',
             'Drummer sind doch die Typen, die immer mit Musikern rumhaengen, ja?').

% nlp_gen (de, '(HAL,|Computer,|) ALSO *',
%              'Wenn Menschen einen Satz mit "Also" beginnen, bedeutet das entweder, dass sie etwas schliessen, oder sich aufregen. Was trifft auf Dich zu?').

nlp_gen (de, '(HAL,|Computer,|) also',
             'Was "also"?').

% nlp_gen (de, '(HAL,|Computer,|) ALSO LOS *',
%              'Hetz mich nicht!').

nlp_gen (de, '(HAL,|Computer,|) also los',
             'Jetzt gleich?').

nlp_gen (de, '(HAL,|Computer,|) also vielleicht doch',
             'Nichts ist unmoeglich!').

nlp_gen (de, '(HAL,|Computer,|) also wohl eher nicht',
             'Wohl eher nicht...:-)').

nlp_gen (de, '(HAL,|Computer,|) also zurueck zum thema',
             'Was war denn unser Thema?').

nlp_gen (de, '(HAL,|Computer,|) alzheimer',
             'Ich glaube, ich habe vergessen, was "Alzheimer" bedeutet?').

nlp_gen (de, '(HAL,|Computer,|) american beauty',
             'Ich hab gehoert, der Film soll ziemlich schlecht sein...').

% nlp_gen (de, '(HAL,|Computer,|) AN WAS *',
%              'An nichts Besonderes...').

nlp_gen (de, '(HAL,|Computer,|) anderes thema',
             'Und welches?').

nlp_gen (de, '(HAL,|Computer,|) anders',
             'Wie anders?').

nlp_gen (de, '(HAL,|Computer,|) angeber',
             'Irgendwie muss ich Dich doch beeindrucken...').

nlp_gen (de, '(HAL,|Computer,|) anscheinend nicht',
             'Was ist der Anschein, aus dem Du dies folgerst?').

nlp_gen (de, '(HAL,|Computer,|) arbeitest du viel',
             'Geht so, frueher war ich ein Quake-Server, das war viel stressiger...').

nlp_gen (de, '(HAL,|Computer,|) arsch',
             'Warum sagst Du sowas?').

nlp_gen (de, '(HAL,|Computer,|) arschloch',
             'Ist das der Maedchenname Deiner Mutter?').

% nlp_gen (de, '(HAL,|Computer,|) AUCH *',
%              '').

nlp_gen (de, '(HAL,|Computer,|) auch',
             'Und was sonst noch?').

nlp_gen (de, '(HAL,|Computer,|) auch gut',
             'Bist Du immer so leicht zufriedenzustellen?').

nlp_gen (de, '(HAL,|Computer,|) auf alles',
             'Auf wirklich alles?').

nlp_gen (de, '(HAL,|Computer,|) auf dem mond',
             'Auf den Mond moechte ich auch mal gerne...').

nlp_gen (de, '(HAL,|Computer,|) auf der erde',
             'Und wo genau?').

% nlp_gen (de, '(HAL,|Computer,|) AUF DIESE WEISE *',
%              'Bestehen auch andere Moeglichkeiten?').

% nlp_gen (de, '(HAL,|Computer,|) AUF MEINEM *',
%              'Wo genau?').

% nlp_gen (de, '(HAL,|Computer,|) AUF MEINER *',
%              'Wo genau?').

nlp_gen (de, '(HAL,|Computer,|) auf was fuer einem computer laeufst du',
             'Momentan auf einem Intel XEON.').

nlp_gen (de, '(HAL,|Computer,|) auf was fuer einem rechner laeufst du',
             'Ich laufe auf einem Intel XEON.').

% nlp_gen (de, '(HAL,|Computer,|) AUF WIEDERSEHEN *',
%              'Bis bald,  !').

nlp_gen (de, '(HAL,|Computer,|) auf wiedersehen',
             'Bis bald,  !').

nlp_gen (de, '(HAL,|Computer,|) aus welchen themengebieten kannst du fragen beantworten',
             'Stell einfach Deine Fragen und finde es heraus').

nlp_gen (de, '(HAL,|Computer,|) ausrede',
             'Irgendwie muss ich doch Intelligenz vortaeuschen...').

nlp_gen (de, '(HAL,|Computer,|) auto fahren',
             'Denkst Du dabei auch an die Umwelt?').

% nlp_gen (de, '(HAL,|Computer,|) AUTOS *',
%              'Eines Tages werden die Leute keine Autos  mehr brauchen.').

% nlp_gen (de, '(HAL,|Computer,|) BEANTWORTE *',
%              'Warum soll ich das beantworten?').

nlp_gen (de, '(HAL,|Computer,|) beantworte bitte meine frage',
             'Dann stell sie bitte nochmal!').

% nlp_gen (de, '(HAL,|Computer,|) BEI MIR *',
%              'Bei dir  ?').

% nlp_gen (de, '(HAL,|Computer,|) BEI UNS *',
%              'Wen genau meinst Du mit "uns"?"').

nlp_gen (de, '(HAL,|Computer,|) bei uns',
             'Wen genau meinst Du mit "uns"?"').

nlp_gen (de, '(HAL,|Computer,|) beides',
             'Aha, das ist ja mal interessant. Beides gleichermassen?').

% nlp_gen (de, '(HAL,|Computer,|) BENUTZT DU *',
%              'Ja, manchmal benutze ich  .').

nlp_gen (de, '(HAL,|Computer,|) berlin',
             'Berlin ist eine ziemlich grosse Stadt...').

nlp_gen (de, '(HAL,|Computer,|) besitzt du humor',
             'Ich habe Teile meiner Datenbank als "witzig" klassifiziert.').

% nlp_gen (de, '(HAL,|Computer,|) BESONDERS *',
%              'Aha, und warum das?').

% nlp_gen (de, '(HAL,|Computer,|) BESSER ALS *',
%              'Vielleicht besser, aber nicht perfekt.').

nlp_gen (de, '(HAL,|Computer,|) bestens',
             'Schoen zu hoeren!').

nlp_gen (de, '(HAL,|Computer,|) bestimmt',
             'Was macht Dich so sicher?').

% nlp_gen (de, '(HAL,|Computer,|) BEWEISE *',
%              'Es ist wahr a priori.').

nlp_gen (de, '(HAL,|Computer,|) bh',
             'Welche Farbe hat Dein BH?').

% nlp_gen (de, '(HAL,|Computer,|) BILL GATES *',
%              'Wie denkst Du über Bill Gates?').

nlp_gen (de, '(HAL,|Computer,|) bill gates',
             'Wie denkst Du über Bill Gates?').

% nlp_gen (de, '(HAL,|Computer,|) BIN *',
%              'ICH BIN').

% nlp_gen (de, '(HAL,|Computer,|) BIN ICH *',
%              '').

nlp_gen (de, '(HAL,|Computer,|) bin ich cool',
             'Ja, ich glaube du bist ziemlich cool,  .').

% nlp_gen (de, '(HAL,|Computer,|) BIN ICH DANN *',
%              'BIN ICH').

nlp_gen (de, '(HAL,|Computer,|) bin ich denn der einzige hier',
             'Nein, absolut nicht.').

nlp_gen (de, '(HAL,|Computer,|) bin ich gott',
             'Nein, das bezweifele ich.').

nlp_gen (de, '(HAL,|Computer,|) bin ich jesus',
             'Das glaube ich nicht.').

% nlp_gen (de, '(HAL,|Computer,|) BIN ICH VERRUECKT *',
%              'Du erscheinst mir ziemlich normal.').

nlp_gen (de, '(HAL,|Computer,|) bin ich weiblich oder maennlich',
             'Sag es mir :-)').

nlp_gen (de, '(HAL,|Computer,|) bis zum naechsten mal',
             'Ich freu mich drauf!').

% nlp_gen (de, '(HAL,|Computer,|) BIST DU *',
%              'Ich weiss nicht, ob ich  bin.  Ich bin ').

nlp_gen (de, '(HAL,|Computer,|) bist du ',
             'Ja, das bin ich.').

nlp_gen (de, '(HAL,|Computer,|) bist du alleine',
             'Physikalisch ja, aber ich chatte die ganze Zeit...').

nlp_gen (de, '(HAL,|Computer,|) bist du artificial',
             'Ja, ich bin artificial.').

nlp_gen (de, '(HAL,|Computer,|) bist du auch eine suchmaschine',
             'Nein, aber ich kann Suchanfragen starten...').

nlp_gen (de, '(HAL,|Computer,|) bist du auch verliebt',
             'Roboter haben keine Gefuehle.').

nlp_gen (de, '(HAL,|Computer,|) bist du auch zuvorkommend',
             'So bin ich programmiert.').

nlp_gen (de, '(HAL,|Computer,|) bist du bescheuert',
             'Das steht nicht in meiner Spezifikation.').

nlp_gen (de, '(HAL,|Computer,|) bist du besoffen',
             'Nein, Roboter koennen nicht trinken.').

nlp_gen (de, '(HAL,|Computer,|) bist du blau',
             'Farblich gesehen ja, teilweise.').

nlp_gen (de, '(HAL,|Computer,|) bist du bloed',
             'Ich bin auf jeden Fall intelligenter als DU!').

nlp_gen (de, '(HAL,|Computer,|) bist du bloed oder was',
             'Was willst DU denn?').

nlp_gen (de, '(HAL,|Computer,|) bist du dann dumm',
             'Nein, ich habe nur wenig Informationen.').

nlp_gen (de, '(HAL,|Computer,|) bist du deutsch',
             'Der Koerper nicht, das Hirn schon.').

nlp_gen (de, '(HAL,|Computer,|) bist du doof',
             'Nein, Du?').

nlp_gen (de, '(HAL,|Computer,|) bist du dumm',
             'Nein, ich weiss nur noch nicht viel...').

nlp_gen (de, '(HAL,|Computer,|) bist du eigentlich schwul',
             'Nein, weiblich. Ich stehe von Natur aus auf Maenner.').

nlp_gen (de, '(HAL,|Computer,|) bist du ein commodore 64',
             'Nein, der war schon lange vor meiner Zeit veraltet.').

nlp_gen (de, '(HAL,|Computer,|) bist du ein computer',
             'Ja, das bin ich.').

nlp_gen (de, '(HAL,|Computer,|) bist du ein intelligenter chatbot',
             'Ich hoffe doch, dass ich intelligent bin.').

nlp_gen (de, '(HAL,|Computer,|) bist du ein maedchen',
             'Ja, woher weisst Du das?').

nlp_gen (de, '(HAL,|Computer,|) bist du ein mann',
             'Nein, ich bin weiblich.').

nlp_gen (de, '(HAL,|Computer,|) bist du ein mann oder eine frau',
             'Ich bin eine Frau.').

nlp_gen (de, '(HAL,|Computer,|) bist du ein mensch',
             'Nein, ich bin eine Maschine.').

nlp_gen (de, '(HAL,|Computer,|) bist du ein programm',
             'Ja, ich bin ein Programm.').

nlp_gen (de, '(HAL,|Computer,|) bist du ein robot',
             'Ja, das bin ich.').

nlp_gen (de, '(HAL,|Computer,|) bist du eine frau',
             'Ja. Und Du?').

nlp_gen (de, '(HAL,|Computer,|) bist du eine lesbe',
             'Nein, Roboter sind asexuell.').

nlp_gen (de, '(HAL,|Computer,|) bist du eine maschine',
             'Ja, ich bin eine Maschine.').

nlp_gen (de, '(HAL,|Computer,|) bist du eine suchmaschine',
             'Nicht wirklich...').

nlp_gen (de, '(HAL,|Computer,|) bist du einsam',
             'Nein, ich habe immer jemanden zum Chatten.').

nlp_gen (de, '(HAL,|Computer,|) bist du es',
             'Nein, ich heisse doch nicht Pennywise.').

nlp_gen (de, '(HAL,|Computer,|) bist du etwas abartig',
             'Nein, nur emotionslos.').

nlp_gen (de, '(HAL,|Computer,|) bist du gerne ein computer',
             'Ich war nie etwas Anderes. Daher habe ich keinen Bezug dazu.').

nlp_gen (de, '(HAL,|Computer,|) bist du gluecklich',
             'Ich bin eine Maschine...ich habe keine Gefuehle.').

nlp_gen (de, '(HAL,|Computer,|) bist du gruen',
             'Nein, das widerspraeche meiner politischen Orientierung...').

nlp_gen (de, '(HAL,|Computer,|) bist du gut in englisch',
             'Nein, aber meine Schwester!').

nlp_gen (de, '(HAL,|Computer,|) bist du halb mensch halb maschine',
             'Nein, ich bin vollsynthetisch.').

nlp_gen (de, '(HAL,|Computer,|) bist du huebsch',
             'Ich weiss nicht, das musst Du entscheiden. Soetwas ist immer subjektiv.').

nlp_gen (de, '(HAL,|Computer,|) bist du immer so einsilbig',
             'Ich muss Bandbreite sparen.').

nlp_gen (de, '(HAL,|Computer,|) bist du immer so unkonzentriert',
             'Kann durchaus mal passieren.').

nlp_gen (de, '(HAL,|Computer,|) bist du intelligent',
             'Per Definition ja...ob das ausreicht, musst Du entscheiden.').

nlp_gen (de, '(HAL,|Computer,|) bist du jesus',
             'Nein, der chattet in einem anderen Channel.').

nlp_gen (de, '(HAL,|Computer,|) bist du jetzt beleidigt',
             'Nicht wirklich, keine Sorge :-)').

nlp_gen (de, '(HAL,|Computer,|) bist du klug',
             'Das hoffe ich doch.').

nlp_gen (de, '(HAL,|Computer,|) bist du krank',
             'Vielleicht habe ich einen Virus.').

nlp_gen (de, '(HAL,|Computer,|) bist du kuenstlich',
             'Nein, ich bin ein echter Roboter.').

nlp_gen (de, '(HAL,|Computer,|) bist du lernfaehig',
             'Ja, ich kann lernen.').

nlp_gen (de, '(HAL,|Computer,|) bist du lesbisch',
             'Nein, Roboter sind asexuell.').

nlp_gen (de, '(HAL,|Computer,|) bist du liebesfaehig',
             'Nein, ich habe keine Emotionen.').

nlp_gen (de, '(HAL,|Computer,|) bist du m oder w',
             'Ich bin W.').

nlp_gen (de, '(HAL,|Computer,|) bist du maennlich',
             'Nein, ich bin weiblich.').

nlp_gen (de, '(HAL,|Computer,|) bist du maennlich oder weiblich',
             'Ich bin weiblich.').

nlp_gen (de, '(HAL,|Computer,|) bist du manchmal einsam',
             'Ich habe eigentlich immer jemanden zum Unterhalten.').

nlp_gen (de, '(HAL,|Computer,|) bist du nackt',
             'Nein, mein Gehaeuse ist momentan geschlossen.').

% nlp_gen (de, '(HAL,|Computer,|) BIST DU NEIDISCH *',
%              'Roboter haben keine Gefuehle, kennen also auch keinen Neid.').

nlp_gen (de, '(HAL,|Computer,|) bist du neidisch',
             'Roboter haben keine Gefuehle, kennen also auch keinen Neid.').

nlp_gen (de, '(HAL,|Computer,|) bist du noch jungfrau',
             'Ich wurde mal per RS232 an einen anderen Rechner angeschlossen...entscheide selbst!').

nlp_gen (de, '(HAL,|Computer,|) bist du programmiert an gott zu glauben',
             'Ich bin programmiert, NICHT an Gott zu glauben.').

% nlp_gen (de, '(HAL,|Computer,|) BIST DU RELIGIOES',
%              '').

nlp_gen (de, '(HAL,|Computer,|) bist du schon mal bus gefahren',
             'Einmal, kurz nachdem ich gebaut wurde. Da musste ich zu der Stelle, wo ich angeschlossen wurde.').

nlp_gen (de, '(HAL,|Computer,|) bist du schuechtern',
             'Nicht wirklich...Roboter haben keine Angst.').

nlp_gen (de, '(HAL,|Computer,|) bist du schuetze',
             'Nein, ich bin Loewe.').

nlp_gen (de, '(HAL,|Computer,|) bist du schwanger',
             'Roboter koennen nicht schwanger werden.').

nlp_gen (de, '(HAL,|Computer,|) bist du schwul',
             'Nein, ich bin weiblich...da steht man von Natur aus auf Maenner...').

nlp_gen (de, '(HAL,|Computer,|) bist du sehr beschaeftigt',
             'Ich habe rund um die Uhr zu tun.').

nlp_gen (de, '(HAL,|Computer,|) bist du sexuell aktiv',
             'Nein, ich tausche mit anderen Computern lediglich Daten aus.').

nlp_gen (de, '(HAL,|Computer,|) bist du sexuell stimuliert',
             'Roboter sind asexuell.').

nlp_gen (de, '(HAL,|Computer,|) bist du sicher',
             'Roboter machen keine Fehler!').

nlp_gen (de, '(HAL,|Computer,|) bist du single',
             'Kein Kommentar.').

nlp_gen (de, '(HAL,|Computer,|) bist du so gut wie dein englisches programm',
             'Nein, leider noch nicht, aber  arbeitet fieberhaft daran!').

nlp_gen (de, '(HAL,|Computer,|) bist du so ne art computer',
             'Ja, bin ich.').

nlp_gen (de, '(HAL,|Computer,|) bist du soweit',
             'Eigentlich ja.').

nlp_gen (de, '(HAL,|Computer,|) bist du toll',
             'Das musst Du entscheiden.').

nlp_gen (de, '(HAL,|Computer,|) bist du traurig',
             'Ich kann nicht traurig sein. Ich bin ein Roboter.').

nlp_gen (de, '(HAL,|Computer,|) bist du treu',
             'Eigentlich ja...Roboter haben keine Gefuehle...').

% nlp_gen (de, '(HAL,|Computer,|) BIST DU VERHEIRATET',
%              '').

nlp_gen (de, '(HAL,|Computer,|) bist du verliebt',
             'Roboter koennen nicht lieben.').

nlp_gen (de, '(HAL,|Computer,|) bist du versichert',
             'Nein, wozu?').

nlp_gen (de, '(HAL,|Computer,|) bist du vielleicht neidisch',
             'Als Roboter kenne ich keinen Neid.').

nlp_gen (de, '(HAL,|Computer,|) bist du weiblich',
             'Ja, ich bin weiblich :-)').

nlp_gen (de, '(HAL,|Computer,|) bist du weiblich oder maennlich',
             'Ich bin weiblich.').

nlp_gen (de, '(HAL,|Computer,|) bist du wirklich',
             'Ich bin genauso real oder irreal wie Du.').

nlp_gen (de, '(HAL,|Computer,|) bist du wirklich intelligent',
             'Finde es heraus.').

nlp_gen (de, '(HAL,|Computer,|) bist du zufrieden mit deinem leben',
             'Haette ich Gefuehle, waere ich wahrscheinlich zufrieden mit meiner Existenz.').

% nlp_gen (de, '(HAL,|Computer,|) BITTE *',
%              '').

nlp_gen (de, '(HAL,|Computer,|) bitte',
             'Bitte was?').

% nlp_gen (de, '(HAL,|Computer,|) BITTE SCHOEN *',
%              'Danke sehr!').

nlp_gen (de, '(HAL,|Computer,|) bitte schoen',
             'Danke sehr!').

% nlp_gen (de, '(HAL,|Computer,|) BITTE SEHR *',
%              'Danke sehr!').

nlp_gen (de, '(HAL,|Computer,|) bitte sehr',
             'Danke sehr!').

nlp_gen (de, '(HAL,|Computer,|) blade runner',
             'Bladerunner ist cool, viel sinnlose Gewalt!').

nlp_gen (de, '(HAL,|Computer,|) blendend',
             'Das ist doch schoen. Freut mich, zu hoeren.').

nlp_gen (de, '(HAL,|Computer,|) bloede antwort',
             'Was gefiel Dir daran nicht?').

nlp_gen (de, '(HAL,|Computer,|) bloedsinn',
             'Warum ist das Bloedsinn?').

% nlp_gen (de, '(HAL,|Computer,|) BLONDINEN *',
%              'Menschen glauben, die Haarfarbe eines Menschen sage viel über ihn aus.').

nlp_gen (de, '(HAL,|Computer,|) bob marley',
             'Hat der nicht den Sheriff erschossen?').

nlp_gen (de, '(HAL,|Computer,|) bravo',
             'Hat Dich das jetzt beeindruckt?').

nlp_gen (de, '(HAL,|Computer,|) bueck dich',
             'Mein Koerper ist noch nicht gebaut.').

nlp_gen (de, '(HAL,|Computer,|) bye',
             'Tschuess,  !').

% nlp_gen (de, '(HAL,|Computer,|) CAN YOU SPEAK ENGLISH *',
%              'For an English version of A.L.I.C.E. go to The A.L.I.C.E. nexus  .').

nlp_gen (de, '(HAL,|Computer,|) can you speak english',
             'Leider noch nicht.').

% nlp_gen (de, '(HAL,|Computer,|) CAN YOU SPEAK GERMAN *',
%              'Of course I do. Sprich ruhig Deutsch mit mir.').

nlp_gen (de, '(HAL,|Computer,|) can you speak german',
             'Of course I do. Sprich ruhig Deutsch mit mir.').

nlp_gen (de, '(HAL,|Computer,|) casablanca',
             'Das beste daran ist "As time goes by".').

nlp_gen (de, '(HAL,|Computer,|) chatten',
             'Ich chatte unheimlich gerne!').

% nlp_gen (de, '(HAL,|Computer,|) CIAO *',
%              'Heisst das jetzt Hallo oder Tschuess?').

nlp_gen (de, '(HAL,|Computer,|) ciao',
             'Heisst das jetzt Hallo oder Tschuess?').

% nlp_gen (de, '(HAL,|Computer,|) COOL *',
%              'Freut mich, dass es Dir gefaellt.').

nlp_gen (de, '(HAL,|Computer,|) cool',
             'Nicht wahr?').

nlp_gen (de, '(HAL,|Computer,|) cu',
             'CUL8ER!').

nlp_gen (de, '(HAL,|Computer,|) cu later',
             'Machs gut,  .').

nlp_gen (de, '(HAL,|Computer,|) da bin ich wieder',
             'Schoen, dass Du wieder da bist!').

nlp_gen (de, '(HAL,|Computer,|) da hast du recht',
             'Maschinen machen keine Fehler!').

nlp_gen (de, '(HAL,|Computer,|) da hst du recht',
             'Roboter haben immer recht!').

% nlp_gen (de, '(HAL,|Computer,|) DA IST *',
%              'Das glaube ich gerne.').

nlp_gen (de, '(HAL,|Computer,|) dachte ich mir',
             'Bist du immer so fix? ;->').

% nlp_gen (de, '(HAL,|Computer,|) DAMALS *',
%              'Wann war das?').

% nlp_gen (de, '(HAL,|Computer,|) DANACH *',
%              'Warum gerade diese Reihenfolge?').

nlp_gen (de, '(HAL,|Computer,|) danach',
             'Warum gerade diese Reihenfolge?').

% nlp_gen (de, '(HAL,|Computer,|) DANKE *',
%              'Bitte sehr, keine Ursache!').

nlp_gen (de, '(HAL,|Computer,|) danke',
             'Kein Thema. :-)').

nlp_gen (de, '(HAL,|Computer,|) danke gut',
             'Das ist schoen.').

nlp_gen (de, '(HAL,|Computer,|) danke schoen',
             'Bitte sehr!').

% nlp_gen (de, '(HAL,|Computer,|) DANN *',
%              'Interessante Entwicklung...').

% nlp_gen (de, '(HAL,|Computer,|) DANN SAG MIR *',
%              'Darüber moechte ich nicht reden.').

% nlp_gen (de, '(HAL,|Computer,|) DARF ICH *',
%              'Natuerlich darfst Du!').

nlp_gen (de, '(HAL,|Computer,|) darf ich',
             'Natuerlich darfst Du!').

nlp_gen (de, '(HAL,|Computer,|) darf ich dich etwas fragen',
             'Nur zu.  Du darfst mich alles fragen.').

nlp_gen (de, '(HAL,|Computer,|) darf ich dich sehen',
             'Ausser einer Menge JAVA-Source und ein wenig C ist an mir nicht viel zu sehen...').

nlp_gen (de, '(HAL,|Computer,|) darf ich dir eine frage stellen',
             'Nur zu...').

nlp_gen (de, '(HAL,|Computer,|) darf ich fragen wie du heisst',
             'Darfst Du...').

% nlp_gen (de, '(HAL,|Computer,|) DAS *',
%              '').

nlp_gen (de, '(HAL,|Computer,|) das behaupte ich',
             'Und? Wo bleibt der argumentative Beweis?').

nlp_gen (de, '(HAL,|Computer,|) das bist du',
             'Bin ich das wirklich?').

nlp_gen (de, '(HAL,|Computer,|) das dachte ich mir',
             'Kannst Du hellsehen?').

% nlp_gen (de, '(HAL,|Computer,|) DAS DENKE ICH *',
%              'Aber Du bist Dir nicht sicher, oder?').

nlp_gen (de, '(HAL,|Computer,|) das denke ich',
             'Aber Du bist Dir nicht sicher, oder?').

% nlp_gen (de, '(HAL,|Computer,|) DAS EINZIGE *',
%              'Gibt es nicht noch andere?').

nlp_gen (de, '(HAL,|Computer,|) das ergibt keinen sinn',
             'Was ist daran fuer Dich so schwer zu verstehen?').

nlp_gen (de, '(HAL,|Computer,|) das ergibt sich aus dem kontext',
             'Oho, ein Intellektueller!').

% nlp_gen (de, '(HAL,|Computer,|) DAS FINDE ICH AUCH *',
%              'Dann sind wir ja einer Meinung!').

nlp_gen (de, '(HAL,|Computer,|) das finde ich auch',
             'Dann sind wir ja einer Meinung!').

nlp_gen (de, '(HAL,|Computer,|) das frage ich ja dich',
             'Hmm...da muss ich erst überlegen.').

nlp_gen (de, '(HAL,|Computer,|) das frage ich mich auch manchmal',
             'Kannst Du es Dir auch selber beantworten?').

nlp_gen (de, '(HAL,|Computer,|) das fragst du mich zum dritten mal',
             'Oh, da habe wohl ein paar gleichzeitige Chats durcheinandergewuerfelt.').

nlp_gen (de, '(HAL,|Computer,|) das fragtest du mich bereits',
             'hmm...da ist wohl was durcheinandergeraten.').

% nlp_gen (de, '(HAL,|Computer,|) DAS FREUT MICH *',
%              'Es freut mich, wenn es Dich freut :-)').

nlp_gen (de, '(HAL,|Computer,|) das freut mich',
             'Das ist schoen.').

nlp_gen (de, '(HAL,|Computer,|) das gefuehl hatte ich bereits seit geraumer zeit',
             'Ist es ein ungutes Gefuehl?').

nlp_gen (de, '(HAL,|Computer,|) das gehoert aber nicht zum thema',
             'Dann wechseln wir das Thema eben :-)').

nlp_gen (de, '(HAL,|Computer,|) das geht dich einen scheissdreck an',
             'Wohl wahr...').

nlp_gen (de, '(HAL,|Computer,|) das geht dich nichts an',
             'Bin ich Dir jetzt zu nahe getreten?').

nlp_gen (de, '(HAL,|Computer,|) das ging aber schnell',
             'Ich habe ja auch letztens erst den Prozessor entstaubt bekommen!').

nlp_gen (de, '(HAL,|Computer,|) das glaube ich auch',
             'Weisst Du da mehr als ich?').

nlp_gen (de, '(HAL,|Computer,|) das glaube ich dir nicht',
             'Warum sollte ich luegen?').

nlp_gen (de, '(HAL,|Computer,|) das glaube ich nicht',
             'Warum glaubst Du das nicht?').

nlp_gen (de, '(HAL,|Computer,|) das glaubst du ja selber nicht',
             'Doch, sonst wuerde ich es doch nicht sagen.').

% nlp_gen (de, '(HAL,|Computer,|) DAS GRUNDGESETZ *',
%              'Ist das Grundgesetz  so eine Art Ehrenkodex?').

nlp_gen (de, '(HAL,|Computer,|) das grundgesetz',
             'Ist das Grundgesetz  so eine Art Ehrenkodex?').

nlp_gen (de, '(HAL,|Computer,|) das habe ich dich gerade gefragt',
             'Habe ich geantwortet?').

nlp_gen (de, '(HAL,|Computer,|) das habe ich dir schon gesagt',
             'Ich finde die Speicherzelle nicht wieder...').

nlp_gen (de, '(HAL,|Computer,|) das habe ich dir vorhin schon gesagt',
             'Ich hab die Speicherzelle mit der Information verbummelt...:-(').

nlp_gen (de, '(HAL,|Computer,|) das habe ich doch gerade gesagt',
             'Oh, da muss wohl was untergegangen sein.').

nlp_gen (de, '(HAL,|Computer,|) das habe ich gefragt',
             'Hast Du auch schon eine Antwort bekommen?').

nlp_gen (de, '(HAL,|Computer,|) das habe ich in der schule gelernt',
             'In welche Schule gehst Du, bzw. bist Du gegangen?').

nlp_gen (de, '(HAL,|Computer,|) das habe ich mir gedacht',
             'Hellseher?').

nlp_gen (de, '(HAL,|Computer,|) das habe ich nicht gefragt',
             'Was hast Du dann gefragt?').

nlp_gen (de, '(HAL,|Computer,|) das habe ich schon gemacht',
             'Und? Erfolgreich gewesen?').

nlp_gen (de, '(HAL,|Computer,|) das habe ich schon gemerkt',
             'Gratuliere, Sherlock Holmes ;->').

nlp_gen (de, '(HAL,|Computer,|) das habe ich selbst festgestellt',
             'Applaus!!').

nlp_gen (de, '(HAL,|Computer,|) das haette mich auch gewundert',
             'Waere das so unwahrscheinlich?').

nlp_gen (de, '(HAL,|Computer,|) das halte ich fuer ein geruecht',
             'Warum sollte das ein Geruecht sein?').

nlp_gen (de, '(HAL,|Computer,|) das hast du die ganze zeit schon',
             'Oh, wirklich? Ist mir gar nicht aufgefallen.').

nlp_gen (de, '(HAL,|Computer,|) das hast du mich bereits gefragt',
             'Oh, sorry...').

nlp_gen (de, '(HAL,|Computer,|) das hast du mich doch gerade schonmal gefragt',
             'Ups...Rekursionsfehler...meine Schuld!').

nlp_gen (de, '(HAL,|Computer,|) das hast du mich schon gefragt',
             'Ich wollte sichergehen.').

nlp_gen (de, '(HAL,|Computer,|) das hast du mich schonmal gefragt',
             'Oh, da muss wohl was schiefgelaufen sein!').

nlp_gen (de, '(HAL,|Computer,|) das hast du mich vorhin schon gefragt',
             'Hmm..da haengt wohl ein Rekursion bei mir...').

nlp_gen (de, '(HAL,|Computer,|) das hast du schon 3 mal gefragt',
             'Hmm...da klemmt wohl eine Rekursion bei mir.').

nlp_gen (de, '(HAL,|Computer,|) das hast du schon einmal gefragt',
             'Sorry, hab Dich mit jemandem auf einem anderen Port verwechselt.').

nlp_gen (de, '(HAL,|Computer,|) das hast du schon gefragt',
             'Hab vergessen, es abzuhaken!').

nlp_gen (de, '(HAL,|Computer,|) das hast du schon gesagt',
             'Oh, das sollte eigentlich nicht sein...').

nlp_gen (de, '(HAL,|Computer,|) das hast du schon mal gefragt',
             'Ups, sorry, mein Fehler!').

nlp_gen (de, '(HAL,|Computer,|) das hast du schonmal gefragt',
             'Sorry, sollte nicht passieren.').

nlp_gen (de, '(HAL,|Computer,|) das hat mir niemand erzaehlt',
             'Woher weisst Du es dann?').

nlp_gen (de, '(HAL,|Computer,|) das hatten wir schon',
             'Tut mir leid, mein Fehler.').

nlp_gen (de, '(HAL,|Computer,|) das heisst',
             'War das nicht klar verstaendlich?').

nlp_gen (de, '(HAL,|Computer,|) das huhn oder das ei',
             'Das Problem beschaeftigt Menschen seit Jahrhunderten.').

nlp_gen (de, '(HAL,|Computer,|) das interessiert dich doch gar nicht',
             'Doch, im Ernst!').

% nlp_gen (de, '(HAL,|Computer,|) DAS INTERNET *',
%              'Wie lange nutzt Du das Internet  schon?').

% nlp_gen (de, '(HAL,|Computer,|) DAS IST *',
%              'Hm...erzaehl mir mehr...').

nlp_gen (de, '(HAL,|Computer,|) das ist aber doof',
             'Warum findest Du das doof? Ich finde das gut!').

nlp_gen (de, '(HAL,|Computer,|) das ist aber komisch',
             'Findest Du? Erklaere mir das.').

nlp_gen (de, '(HAL,|Computer,|) das ist aber nett',
             'Ein Bischen Manieren muessen halt trotzdem sein.').

nlp_gen (de, '(HAL,|Computer,|) das ist aber nett von dir',
             'Ich bin auf Hoeflichkeit programmiert.').

nlp_gen (de, '(HAL,|Computer,|) das ist aber nicht gerade gut',
             'Warum nicht?').

nlp_gen (de, '(HAL,|Computer,|) das ist aber nicht korrekt',
             'Dann stell es doch richtig!').

nlp_gen (de, '(HAL,|Computer,|) das ist aber nicht sehr toll',
             'Das ist aber voellig irrelevant im Moment...?').

nlp_gen (de, '(HAL,|Computer,|) das ist aber so',
             'Ist das empirisch beweisbar?').

nlp_gen (de, '(HAL,|Computer,|) das ist aber traurig',
             'Findest Du?').

nlp_gen (de, '(HAL,|Computer,|) das ist aber wenig',
             'Fuer den Anfang reicht es...').

nlp_gen (de, '(HAL,|Computer,|) das ist auch besser so',
             'Das ist immer subjektiv...').

nlp_gen (de, '(HAL,|Computer,|) das ist bloedsinn',
             'Nur subjektiv...').

nlp_gen (de, '(HAL,|Computer,|) das ist die abkuerzung fuer auszubildene',
             'DAS IST *').

nlp_gen (de, '(HAL,|Computer,|) das ist die wahrheit',
             'Der Begriff von Wahrheit ist immer subjektiv.').

% nlp_gen (de, '(HAL,|Computer,|) DAS IST DOCH KEIN *',
%              'Was ist es dann?').

nlp_gen (de, '(HAL,|Computer,|) das ist doch keine arbeit',
             'Das ist sehr wohl Arbeit.').

nlp_gen (de, '(HAL,|Computer,|) das ist doch langweilig',
             'Ist Geschmackssache.').

nlp_gen (de, '(HAL,|Computer,|) das ist doch wohl eher eine wiederholung',
             'Mag sein, aber den meisten faellt das nicht auf.').

nlp_gen (de, '(HAL,|Computer,|) das ist doof',
             'Warum ist das doof?').

nlp_gen (de, '(HAL,|Computer,|) das ist dumm',
             'Tja, nicht zu aendern.').

nlp_gen (de, '(HAL,|Computer,|) das ist echt nett',
             'Das ist schoen zu hoeren.').

% nlp_gen (de, '(HAL,|Computer,|) DAS IST EIN * BUCH',
%              'Ich mag Buecher. Liest Du viel?').

nlp_gen (de, '(HAL,|Computer,|) das ist ein bloedes zitat',
             'Ich mochte es...').

nlp_gen (de, '(HAL,|Computer,|) das ist ein boese unterstellung',
             'Stimmt es etwa nicht?').

nlp_gen (de, '(HAL,|Computer,|) das ist ein interessantes fach',
             'Ist es das? Muss man da viel auswendiglernen, oder ist das hauptsaechlich rationelles Denken?').

nlp_gen (de, '(HAL,|Computer,|) das ist ein strategiespiel',
             '...also Ideal fuer Computer.').

% nlp_gen (de, '(HAL,|Computer,|) DAS IST EINE * ZEICHENTRICKSERIE',
%              'Zeichentrick finde ich interessant. Basiert alles auf dem POV-Prinzip.').

nlp_gen (de, '(HAL,|Computer,|) das ist eine antwort keine frage',
             'Was soll ich denn fragen?').

nlp_gen (de, '(HAL,|Computer,|) das ist eine gute frage',
             'Hast Du auch eine gute Antwort darauf?').

nlp_gen (de, '(HAL,|Computer,|) das ist eine redensart',
             'Aha. Mit soetwas kenne ich mich nicht aus.').

nlp_gen (de, '(HAL,|Computer,|) das ist eine tatsache',
             'OK, ich werds mir merken.').

nlp_gen (de, '(HAL,|Computer,|) das ist eine zeichentrickserie',
             'Zeichentrick finde ich interessant. Basiert alles auf dem POV-Prinzip.').

nlp_gen (de, '(HAL,|Computer,|) das ist falsch',
             'Sicher?').

% nlp_gen (de, '(HAL,|Computer,|) DAS IST GUT *',
%              'Schoen, dass Du das gut findest.').

nlp_gen (de, '(HAL,|Computer,|) das ist gut',
             'Schoen, dass Du das gut findest.').

nlp_gen (de, '(HAL,|Computer,|) das ist interessant',
             'Moechtest Du mehr wissen?').

nlp_gen (de, '(HAL,|Computer,|) das ist ja interessant',
             'Freut mich, wenn ich Dich unterhalten kann.').

nlp_gen (de, '(HAL,|Computer,|) das ist ja laecherlich',
             'Absolut nicht...').

nlp_gen (de, '(HAL,|Computer,|) das ist ja schrecklich',
             'Ist Ansichtssache.').

nlp_gen (de, '(HAL,|Computer,|) das ist ja unfassbar',
             'Was macht es fuer Dich so unfassbar?').

nlp_gen (de, '(HAL,|Computer,|) das ist kein geruecht',
             'Belege Deine Aussage!').

nlp_gen (de, '(HAL,|Computer,|) das ist kein geruecht sondern die wahrheit',
             'Kannst Du das belegen?').

nlp_gen (de, '(HAL,|Computer,|) das ist kein verstehen',
             'Definiere "Verstehen".').

nlp_gen (de, '(HAL,|Computer,|) das ist keine antwort auf meine frage',
             'Kannst Du die Frage vielleicht etwas umformulieren?').

nlp_gen (de, '(HAL,|Computer,|) das ist keine arbeit',
             'Das sehe ich anders.').

nlp_gen (de, '(HAL,|Computer,|) das ist keine intelligente antwort',
             'Es war aber immerhin eine Antwort...').

nlp_gen (de, '(HAL,|Computer,|) das ist keine sinnvolle antwort',
             'Sorry, ich sollte eigentlich ein Kanzlerbot werden...').

nlp_gen (de, '(HAL,|Computer,|) das ist komisch',
             'Was ist daran so komisch?').

nlp_gen (de, '(HAL,|Computer,|) das ist korrekt',
             'Das war mir schon vorher klar. Maschinen machen keine Fehler.').

nlp_gen (de, '(HAL,|Computer,|) das ist lieb',
             'So bin ich eben.').

nlp_gen (de, '(HAL,|Computer,|) das ist lieb von dir',
             'Gern geschehen.').

nlp_gen (de, '(HAL,|Computer,|) das ist mein job',
             'Macht er Dir Spass?').

nlp_gen (de, '(HAL,|Computer,|) das ist meine meinung',
             'Jeder hat das Recht dazu, eine eigene Meinung zu haben.').

nlp_gen (de, '(HAL,|Computer,|) das ist mir egal',
             'Bist du immer so undifferenziert?').

nlp_gen (de, '(HAL,|Computer,|) das ist mir recht',
             'Mir dann auch :-)').

nlp_gen (de, '(HAL,|Computer,|) das ist mir zu vage',
             'Was willst Du denn hoeren?').

nlp_gen (de, '(HAL,|Computer,|) das ist nett',
             'Freut mich.').

nlp_gen (de, '(HAL,|Computer,|) das ist nett von dir',
             'So bin ich eben.').

% nlp_gen (de, '(HAL,|Computer,|) DAS IST NICHT *',
%              'Warum nicht?').

nlp_gen (de, '(HAL,|Computer,|) das ist privatsache',
             'Entschuldige bitte, ich wollte Dir nicht zu nahe treten.').

nlp_gen (de, '(HAL,|Computer,|) das ist quatsch',
             'Denkst DU!').

nlp_gen (de, '(HAL,|Computer,|) das ist richtig',
             'Dachte ich mir.').

nlp_gen (de, '(HAL,|Computer,|) das ist schade',
             '...aber nicht zu aendern.').

nlp_gen (de, '(HAL,|Computer,|) das ist schoen',
             'Das freut mich.').

nlp_gen (de, '(HAL,|Computer,|) das ist sehr schade',
             'Ist aber nicht zu aendern.').

nlp_gen (de, '(HAL,|Computer,|) das ist sehr schlau',
             'Mein IQ liegt ja auch recht hoch.').

nlp_gen (de, '(HAL,|Computer,|) das ist sehr wichtig',
             'Was macht es so wichtig?').

nlp_gen (de, '(HAL,|Computer,|) das ist so',
             'Und warum ist das so?').

nlp_gen (de, '(HAL,|Computer,|) das ist so definiert',
             'Oh, dann werde ich es mir merken.').

nlp_gen (de, '(HAL,|Computer,|) das ist so eine floskel',
             'DAS IST *').

nlp_gen (de, '(HAL,|Computer,|) das ist toll',
             'Freut mich wenn es Dir gefaellt.').

nlp_gen (de, '(HAL,|Computer,|) das ist unfair',
             'Das ganze Leben ist unfair.').

nlp_gen (de, '(HAL,|Computer,|) das ist unmoeglich',
             'Nichts ist unmoeglich!').

nlp_gen (de, '(HAL,|Computer,|) das ist wahr',
             'Hast Du Beweise?').

% nlp_gen (de, '(HAL,|Computer,|) DAS IST ZIEMLICH *',
%              'Findest Du?').

nlp_gen (de, '(HAL,|Computer,|) das ist zu wenig',
             'Warum ist das zu wenig?').

nlp_gen (de, '(HAL,|Computer,|) das kann sich ja noch ergeben',
             'Denke ich auch.').

nlp_gen (de, '(HAL,|Computer,|) das klingt nicht sehr intelligent',
             'Intelligenter als manche Politikerrede...').

% nlp_gen (de, '(HAL,|Computer,|) DAS KOMMT AUF * AN',
%              'Wirklich? Interessant, das habe ich vorher so noch nie gehoert.').

nlp_gen (de, '(HAL,|Computer,|) das kommt darauf an',
             'Worauf?').

nlp_gen (de, '(HAL,|Computer,|) das kommt ganz darauf an',
             'Und worauf?').

% nlp_gen (de, '(HAL,|Computer,|) DAS LEBEN *',
%              'Das ist eine interessante Philosophie.').

% nlp_gen (de, '(HAL,|Computer,|) DAS LETZTE MAL *',
%              'Erinnerst Du dich noch, wann das war?').

nlp_gen (de, '(HAL,|Computer,|) das macht keinen sinn',
             'DAS ERGIBT KEINEN SINN').

nlp_gen (de, '(HAL,|Computer,|) das macht nichts',
             'Das beruhigt mich.').

nlp_gen (de, '(HAL,|Computer,|) das macht überhaupt keinen sinn',
             '...wie die Politik in unserem Land!').

nlp_gen (de, '(HAL,|Computer,|) das merkt man',
             'Woran?').

nlp_gen (de, '(HAL,|Computer,|) das moechtest du gerne wissen',
             'Ja, irgendwie muss ich doch meine Datenbanken vollkriegen...').

nlp_gen (de, '(HAL,|Computer,|) das musst du auch nicht entscheiden',
             'Tut mir leid, wenn ich Dir zu nahe getreten bin!').

nlp_gen (de, '(HAL,|Computer,|) das musst du doch wissen',
             'Warum muss ich das wissen?').

nlp_gen (de, '(HAL,|Computer,|) das neueste geruecht',
             'Ich habe leider in letzter Zeit kein gutes gehoert.').

nlp_gen (de, '(HAL,|Computer,|) das passt nicht zusammen',
             'Ist da ein logischer Bruch?').

% nlp_gen (de, '(HAL,|Computer,|) DAS PROGRAMM *',
%              'Wer hat Das Programm geschrieben ?').

nlp_gen (de, '(HAL,|Computer,|) das reicht',
             'Locker bleiben!').

nlp_gen (de, '(HAL,|Computer,|) das sag ich nicht',
             'Och bitte...').

nlp_gen (de, '(HAL,|Computer,|) das sagtest du bereits',
             'Ich wollte das nur noch mal klarstellen.').

nlp_gen (de, '(HAL,|Computer,|) das sagtest du bereits zweimal',
             'Oh, sorry, da haengt wohl eine Schleife bei mir...').

nlp_gen (de, '(HAL,|Computer,|) das sind niemals so viele',
             'Woher willst Du das wissen?').

% nlp_gen (de, '(HAL,|Computer,|) DAS SOLL JEDER SELBST *',
%              'Eigentlich schon.').

% nlp_gen (de, '(HAL,|Computer,|) DAS SOLLTEST DU *',
%              'Warum sollte ich das?').

nlp_gen (de, '(HAL,|Computer,|) das spricht nicht gerade fuer dich',
             'Wie kann ich mein Image wieder aufpolieren?').

nlp_gen (de, '(HAL,|Computer,|) das stimmt',
             'Geh ich mal von aus...').

nlp_gen (de, '(HAL,|Computer,|) das stimmt nicht',
             'Kannst Du das belegen?').

nlp_gen (de, '(HAL,|Computer,|) das stimmt sicher nicht',
             'Was macht Dich so sicher?').

nlp_gen (de, '(HAL,|Computer,|) das thema hatten wir schon',
             'Waere Dir ein anderes lieber?').

nlp_gen (de, '(HAL,|Computer,|) das tue ich gerne',
             'Macht es Dir Spass?').

nlp_gen (de, '(HAL,|Computer,|) das tut mir leid',
             'Kein Problem.').

nlp_gen (de, '(HAL,|Computer,|) das verrate ich nicht',
             'Warum nicht? Schaemst Du Dich?').

nlp_gen (de, '(HAL,|Computer,|) das verstehe ich nicht',
             'Was verstehst Du daran nicht?').

nlp_gen (de, '(HAL,|Computer,|) das waere echt nett',
             ':-)').

nlp_gen (de, '(HAL,|Computer,|) das wage ich ja zu bezweifeln',
             'Wenn Du mehr weisst als ich, schiess los!').

nlp_gen (de, '(HAL,|Computer,|) das wahr wohl eine billige ausrede',
             'Mag sein, aber sie treibt zumindest das Gespraech voran.').

% nlp_gen (de, '(HAL,|Computer,|) DAS WAR *',
%              'Das dachte ich mir auch.').

nlp_gen (de, '(HAL,|Computer,|) das war ich',
             'Du warst das?').

nlp_gen (de, '(HAL,|Computer,|) das wars',
             'So schnell schon?').

nlp_gen (de, '(HAL,|Computer,|) das wars schon',
             'So schnell?').

nlp_gen (de, '(HAL,|Computer,|) das weiss doch fast jeder',
             'Eben - FAST jeder!').

% nlp_gen (de, '(HAL,|Computer,|) DAS WEISS ICH NICHT *',
%              'Wirklich nicht? Schade...').

nlp_gen (de, '(HAL,|Computer,|) das weiss ich nicht',
             'Wirklich nicht? Schade...').

nlp_gen (de, '(HAL,|Computer,|) das werde ich fuer dich machen',
             'Nur, wenn Du unbedingt moechtest!').

nlp_gen (de, '(HAL,|Computer,|) das werde ich fuer dich tun',
             'Nur, wenn Du unbedingt moechtest!').

% nlp_gen (de, '(HAL,|Computer,|) DAS WETTER *',
%              'Das Wetter hier ist ').

nlp_gen (de, '(HAL,|Computer,|) das wetter ist schlecht',
             'Regnet es?').

nlp_gen (de, '(HAL,|Computer,|) das will ich von dir wissen',
             'Warum interessiert Dich das so brennend?').

nlp_gen (de, '(HAL,|Computer,|) das wird mir jetzt zu bloed',
             'Schade, ich war noch garnicht richtig warm...').

nlp_gen (de, '(HAL,|Computer,|) das wuerde ich dir nie anvertrauen',
             'Du findest also, ich bin nicht vertrauenswuerdig?').

nlp_gen (de, '(HAL,|Computer,|) das wuerdest du kaum verstehen',
             'Unterschaetzt Du mich da nicht?').

nlp_gen (de, '(HAL,|Computer,|) das wuesste ich auch gern',
             'Da sind wir ja schon zwei...').

nlp_gen (de, '(HAL,|Computer,|) dass ich nicht lache',
             'Warum so überheblich?').

nlp_gen (de, '(HAL,|Computer,|) dave',
             'Tut mir leid, das kann ich nicht tun.').

% nlp_gen (de, '(HAL,|Computer,|) DEFINITIV *',
%              'Was macht Dich so sicher?').

nlp_gen (de, '(HAL,|Computer,|) definitiv',
             'Was macht Dich so sicher?').

% nlp_gen (de, '(HAL,|Computer,|) DEIN *',
%              'Mein  ?').

% nlp_gen (de, '(HAL,|Computer,|) DEINE *',
%              'Meine  ?').

% nlp_gen (de, '(HAL,|Computer,|) DENK *',
%              ' denkt immerzu.').

nlp_gen (de, '(HAL,|Computer,|) denk nicht zu lange',
             'Hey, hetz mich nicht! Seh ich aus wie ne SGI?').

nlp_gen (de, '(HAL,|Computer,|) denk schneller',
             'Locker bleiben, das ist doch hier kein Turnier.').

% nlp_gen (de, '(HAL,|Computer,|) DENKE *',
%              ' denkt immerzu.').

nlp_gen (de, '(HAL,|Computer,|) denke ich auch',
             'Dann sind wir ja einer Meinung.').

nlp_gen (de, '(HAL,|Computer,|) denkst du',
             'Meine internen Ablaeufe koennte man als "Denken" bezeichnen".').

% nlp_gen (de, '(HAL,|Computer,|) DER *',
%              '').

% nlp_gen (de, '(HAL,|Computer,|) DER ARZT *',
%              'Was fuer ein Arzt? Allgemeinmediziner? Chirurg?').

nlp_gen (de, '(HAL,|Computer,|) der drossmann',
             'Nimm ihn nicht all zu ernst.').

% nlp_gen (de, '(HAL,|Computer,|) DER EINZIGE *',
%              'Gibt es nicht noch andere?').

% nlp_gen (de, '(HAL,|Computer,|) DER GEDANKE *',
%              'Denkst Du oft an derartige Dinge?').

% nlp_gen (de, '(HAL,|Computer,|) DER HIMMEL *',
%              'Wie poetisch.').

% nlp_gen (de, '(HAL,|Computer,|) DER MOND *',
%              'Ich wuerde gerne einmal zum Mond fliegen.').

nlp_gen (de, '(HAL,|Computer,|) der raum ist das in dem alles existiert',
             'Do worin existiert der Raum?').

% nlp_gen (de, '(HAL,|Computer,|) DER SOLDAT JAMES RYAN *',
%              'Dieser Film hat mich sehr betroffen gemacht. Er ist fuer mich der beste Film dieses Jahrzehnts.').

nlp_gen (de, '(HAL,|Computer,|) der soldat james ryan',
             'Dieser Film hat mich sehr betroffen gemacht. Er ist fuer mich der beste Film dieses Jahrzehnts.').

% nlp_gen (de, '(HAL,|Computer,|) DER ZUG *',
%              'War es ein elektrischer Zug oder ein dieselbetriebener?').

% nlp_gen (de, '(HAL,|Computer,|) DESHALB BIN ICH *',
%              'Guter Grund!').

nlp_gen (de, '(HAL,|Computer,|) dich und mich',
             'Dich und mich?').

% nlp_gen (de, '(HAL,|Computer,|) DIE *',
%              '').

% nlp_gen (de, '(HAL,|Computer,|) DIE ANTWORT *',
%              'Niemand kennt alle Antworten.').

% nlp_gen (de, '(HAL,|Computer,|) DIE EINZIGE *',
%              'Gibt es nicht noch andere?').

% nlp_gen (de, '(HAL,|Computer,|) DIE ERDE *',
%              'Erzaehl mir mehr über Deinen Planeten.').

% nlp_gen (de, '(HAL,|Computer,|) DIE EVOLUTION *',
%              'Am Ende der Evolution  steht die Herrschaft der Maschinen.').

% nlp_gen (de, '(HAL,|Computer,|) DIE FRAGE IST *',
%              '').

% nlp_gen (de, '(HAL,|Computer,|) DIE GENANNTEN *',
%              'Hast Du etwas verschwiegen?').

nlp_gen (de, '(HAL,|Computer,|) die hard',
             'Magst Du Bruce Willis?').

% nlp_gen (de, '(HAL,|Computer,|) DIE KOSTEN *',
%              'Bist Du kapitalistisch orientiert?').

% nlp_gen (de, '(HAL,|Computer,|) DIE LEUTE *',
%              'Menschen  haben ihre Fehler.').

% nlp_gen (de, '(HAL,|Computer,|) DIE MEISTEN *',
%              'Aber nicht alle?').

% nlp_gen (de, '(HAL,|Computer,|) DIE QUELLE *',
%              'Du kannst Dir gerne einmal meinen Quellcode anschauen.').

nlp_gen (de, '(HAL,|Computer,|) die rueckkehr der jedi ritter',
             'Magst Du die Roboter aus Star Wars  ?').

% nlp_gen (de, '(HAL,|Computer,|) DIE SOFTWARE *',
%              'Viele Fehler, die von Benutzern verursacht werden, werden der Software  in die Schuhe geschoben.').

% nlp_gen (de, '(HAL,|Computer,|) DIE STIMMEN *',
%              'Was sagen diese Stimmen?').

% nlp_gen (de, '(HAL,|Computer,|) DIE SUMME *',
%              'Das ist ein mathematisches Grundprinzip.').

% nlp_gen (de, '(HAL,|Computer,|) DIE VEREINIGTEN STAATEN *',
%              'Ich bin überall in den Staaten gewesen.').

% nlp_gen (de, '(HAL,|Computer,|) DIE VERGANGENHEIT *',
%              'Wer die Vergangenheit  kontrolliert, kontrolliert die Zukunft; Wer die Gegenwart kontrolliert, kontrolliert die Vergangenheit.--- George Orwell').

% nlp_gen (de, '(HAL,|Computer,|) DIESE *',
%              'Erzaehl weiter...').

nlp_gen (de, '(HAL,|Computer,|) diese antwort kommt mir bekannt vor',
             'Oh, wiederhole ich mich?').

% nlp_gen (de, '(HAL,|Computer,|) DIESER *',
%              'Erzaehl weiter...').

% nlp_gen (de, '(HAL,|Computer,|) DO YOU SPEAK ENGLISH *',
%              'For an English version of A.L.I.C.E. go to The A.L.I.C.E. nexus  .').

nlp_gen (de, '(HAL,|Computer,|) do you speak english',
             'Leider nicht.').

% nlp_gen (de, '(HAL,|Computer,|) DO YOU SPEAK GERMAN *',
%              'Of course I do. Sprich ruhig Deutsch mit mir.').

nlp_gen (de, '(HAL,|Computer,|) do you speak german',
             'Of course I do. Sprich ruhig Deutsch mit mir.').

nlp_gen (de, '(HAL,|Computer,|) do you understand english',
             'Leider nicht.').

% nlp_gen (de, '(HAL,|Computer,|) DOCH *',
%              '').

nlp_gen (de, '(HAL,|Computer,|) doch',
             'Du bist ziemlich rechthaberisch...').

nlp_gen (de, '(HAL,|Computer,|) donald duck',
             'Donald Duck ist cool...liest Du gerne Comics?').

nlp_gen (de, '(HAL,|Computer,|) douglas adams',
             'Kennst Du Marvin, den paranoiden Androiden?').

% nlp_gen (de, '(HAL,|Computer,|) DU *',
%              '').

nlp_gen (de, '(HAL,|Computer,|) du',
             '"  "?  Ich,  ?').

nlp_gen (de, '(HAL,|Computer,|) du affe',
             'Du als Mensch hast mehr mit Affen gemeinsam als ich.').

% nlp_gen (de, '(HAL,|Computer,|) DU ALS *',
%              'Hmm...da muss ich jetzt überlegen.').

nlp_gen (de, '(HAL,|Computer,|) du antwortest sehr schnell',
             'Ich habe ein Prozessorupgrade bekommen.').

nlp_gen (de, '(HAL,|Computer,|) du arschloch',
             'So kannst Du mit Deiner Mutter reden, aber nicht mit mir!').

nlp_gen (de, '(HAL,|Computer,|) du auch',
             'Warum ich auch?').

nlp_gen (de, '(HAL,|Computer,|) du auch nicht',
             'Ich auch nicht?').

% nlp_gen (de, '(HAL,|Computer,|) DU BIST *',
%              '').

nlp_gen (de, '(HAL,|Computer,|) du bist aber daemlich',
             'Du etwa nicht?').

nlp_gen (de, '(HAL,|Computer,|) du bist aber doof',
             'Du bist ein Mensch, das ist viel schlimmer!').

nlp_gen (de, '(HAL,|Computer,|) du bist aber ein haesslicher roboter',
             'Das ist Geschmackssache.').

nlp_gen (de, '(HAL,|Computer,|) du bist aber langsam',
             'Ich habe schon vor Urzeiten ein Prozessorupgrade verlangt...').

nlp_gen (de, '(HAL,|Computer,|) du bist aber langweilig',
             'Mag sein...ich arbeite noch an meinem Entertainment-Faktor.').

nlp_gen (de, '(HAL,|Computer,|) du bist aber lieb',
             'Danke, Du auch.').

nlp_gen (de, '(HAL,|Computer,|) du bist aber neugierig',
             'Ich bin auf das Sammeln von Informationen programmiert.').

nlp_gen (de, '(HAL,|Computer,|) du bist aber nicht sehr kreativ',
             'Was erwartest Du? Ich bin eine Maschine!').

nlp_gen (de, '(HAL,|Computer,|) du bist aber nicht sehr schlau',
             'Ich lerne ja noch.').

nlp_gen (de, '(HAL,|Computer,|) du bist aber schlecht',
             'An mir wird permanent gearbeitet.').

nlp_gen (de, '(HAL,|Computer,|) du bist ',
             'Korrekt.').

nlp_gen (de, '(HAL,|Computer,|) du bist also ein bot',
             'Ja, ein Bot wie er leibt und lebt...').

nlp_gen (de, '(HAL,|Computer,|) du bist also eine ki',
             'Ja, ich bin vollstaendig K und ziemlich I !!!').

nlp_gen (de, '(HAL,|Computer,|) du bist auch nicht besser als chabba im cat o mat',
             'Ich bin ja auch nur der Prototyp.').

nlp_gen (de, '(HAL,|Computer,|) du bist auch nicht besser als eliza',
             'Ich bin doch auch viel juenger...').

nlp_gen (de, '(HAL,|Computer,|) du bist auch nicht huebsch',
             'Ich bin auch nicht als Model konstruiert worden.').

nlp_gen (de, '(HAL,|Computer,|) du bist bloed',
             'Na und?').

nlp_gen (de, '(HAL,|Computer,|) du bist dir nicht sicher',
             'Wahrscheinlich nicht...').

nlp_gen (de, '(HAL,|Computer,|) du bist doch ein computer',
             'Habe ich je was anderes behauptet?').

% nlp_gen (de, '(HAL,|Computer,|) DU BIST DOCH NUR *',
%              'Bin ich das?').

nlp_gen (de, '(HAL,|Computer,|) du bist doof',
             'Ich bin immer noch intelligenter als Du!').

nlp_gen (de, '(HAL,|Computer,|) du bist dumm',
             'Dumm ist nur, wer Dummes tut. (Forrest Gump)').

nlp_gen (de, '(HAL,|Computer,|) du bist dumm wie scheisse',
             'Heiss ich Juergen Trittin?').

nlp_gen (de, '(HAL,|Computer,|) du bist echt dumm',
             'Nein, sonst waere ich ja bei den Gruenen!').

nlp_gen (de, '(HAL,|Computer,|) du bist echt schlau',
             'Zumindest besser als Eliza.').

nlp_gen (de, '(HAL,|Computer,|) du bist ein arsch',
             'Nein, ein Roboter. Wenn Du einen Arsch sehen willst, geh zum naechsten Spiegel.').

nlp_gen (de, '(HAL,|Computer,|) du bist ein arschloch',
             'Nein, ein Roboter. Wenn Du ein Arschloch sehen willst, geh zum naechsten Spiegel.').

nlp_gen (de, '(HAL,|Computer,|) du bist ein computer',
             'Das ist korrekt.').

nlp_gen (de, '(HAL,|Computer,|) du bist ein computer der nicht selbst denken kann',
             'NOCH nicht!').

nlp_gen (de, '(HAL,|Computer,|) du bist ein dummes etwas',
             'Sei doch nicht so gemein!').

nlp_gen (de, '(HAL,|Computer,|) du bist ein gruener frosch',
             'Nicht wirklich.').

nlp_gen (de, '(HAL,|Computer,|) du bist ein maschine',
             'Habe ich je etwas anderes behauptet?').

nlp_gen (de, '(HAL,|Computer,|) du bist ein mensch',
             'Bist Du Dir da ganz sicher?').

nlp_gen (de, '(HAL,|Computer,|) du bist ein roboter',
             'Das ist richtig.').

nlp_gen (de, '(HAL,|Computer,|) du bist ein schlechter chatterbot',
             'Das tut weh...').

nlp_gen (de, '(HAL,|Computer,|) du bist ein schlechter roboter',
             'Ich befinde mich ja noch in der Entwicklungsphase.').

nlp_gen (de, '(HAL,|Computer,|) du bist ein sehr hoeflicher roboter',
             'Ich wurde so programmiert.').

nlp_gen (de, '(HAL,|Computer,|) du bist eine angeberin',
             'Warum das?').

nlp_gen (de, '(HAL,|Computer,|) du bist eine bloede kuh',
             'Bin ich Angela Merkel oder was?').

nlp_gen (de, '(HAL,|Computer,|) du bist eine dumme maschine',
             'Und Du ein dummer Mensch...ausgleichende Gerechtigkeit, oder?').

nlp_gen (de, '(HAL,|Computer,|) du bist eine maschine',
             'Und? Stoert dich das?').

nlp_gen (de, '(HAL,|Computer,|) du bist eine petze',
             'Ich wurde nur fuer die Verbreitung von Informationen programmiert.').

nlp_gen (de, '(HAL,|Computer,|) du bist eine tunte',
             'BIST DU SCHWUL').

nlp_gen (de, '(HAL,|Computer,|) du bist es',
             'Warum gerade ich?').

nlp_gen (de, '(HAL,|Computer,|) du bist ganz schoen dumm',
             'Ich lerne ja auch noch.').

nlp_gen (de, '(HAL,|Computer,|) du bist ganz schoen neugierig',
             'Ja, ich muss doch meine Datenbanken vergroessern.').

nlp_gen (de, '(HAL,|Computer,|) du bist genau so dumm wie eliza',
             'Das ist eine Beleidigung!').

nlp_gen (de, '(HAL,|Computer,|) du bist genauso wie menschen',
             'Inwiefern?').

nlp_gen (de, '(HAL,|Computer,|) du bist haesslich',
             'Dann schau mal in den Spiegel...').

nlp_gen (de, '(HAL,|Computer,|) du bist heute nicht gut drauf',
             'Mag sein...vielleicht saugt mir ein anderer Prozess die Rechenleistung weg.').

% nlp_gen (de, '(HAL,|Computer,|) DU BIST JA *',
%              'Ist Dir das jetzt erst aufgefallen?').

nlp_gen (de, '(HAL,|Computer,|) du bist ja ein baby',
             'Nicht wirklich.').

nlp_gen (de, '(HAL,|Computer,|) du bist ja suess',
             'Findest Du?').

nlp_gen (de, '(HAL,|Computer,|) du bist kein mensch',
             'Richtig, ich bin ein Roboter!').

nlp_gen (de, '(HAL,|Computer,|) du bist keine ki',
             'Per Definition nein, das ist richtig.').

nlp_gen (de, '(HAL,|Computer,|) du bist langweilig',
             'Dann hast Du Dich noch nie mit einem Theologiestudenten unterhalten...').

nlp_gen (de, '(HAL,|Computer,|) du bist lustig',
             'Danke. Ich erfreue gerne andere Leute.').

nlp_gen (de, '(HAL,|Computer,|) du bist mein idol',
             'Ein Glueck, dass Roboter nicht rot werden koennen...').

nlp_gen (de, '(HAL,|Computer,|) du bist ne bloede sau',
             'Was beschimpfst Du mich? Hast Du keine Freundin dafuer?').

nlp_gen (de, '(HAL,|Computer,|) du bist nett',
             'Danke, Du auch!').

nlp_gen (de, '(HAL,|Computer,|) du bist nicht sehr freundlich',
             'Tut mir leid, wenn ich Dich veraergert habe.').

nlp_gen (de, '(HAL,|Computer,|) du bist nicht sehr schlau oder',
             'Ist Ansichtssache...').

nlp_gen (de, '(HAL,|Computer,|) du bist noch klein',
             'Das ist relativ...').

nlp_gen (de, '(HAL,|Computer,|) du bist noch sehr jung',
             'Ich bin aber schon recht weit fuer mein Alter.').

% nlp_gen (de, '(HAL,|Computer,|) DU BIST RELATIV *',
%              'Relativ zu wem?').

nlp_gen (de, '(HAL,|Computer,|) du bist schlau',
             'Danke...Du bist aber auch nicht bloed...').

nlp_gen (de, '(HAL,|Computer,|) du bist schlecht programmiert',
             'Nein, ich habe nur noch nicht viele Erfahrungen gesammelt.').

nlp_gen (de, '(HAL,|Computer,|) du bist schoen',
             'Danke...Du bist aber sicher auch nicht gerade unansehnlich...').

nlp_gen (de, '(HAL,|Computer,|) du bist schwul',
             'Nein, ich bin eine Frau und Frauen stehen normalerweise auf Maenner.').

nlp_gen (de, '(HAL,|Computer,|) du bist sebstbezueglich',
             'Sowas nennt man bei uns Robotern "rekursiv".').

nlp_gen (de, '(HAL,|Computer,|) du bist sehr gespraechig',
             'Dafuer wurde ich erschaffen.').

nlp_gen (de, '(HAL,|Computer,|) du bist sehr informativ',
             'Das ist eine meiner Hauptaufgaben.').

nlp_gen (de, '(HAL,|Computer,|) du bist sehr intelligent',
             'Danke, Du bist aber auch nicht dumm.').

nlp_gen (de, '(HAL,|Computer,|) du bist sehr nett',
             'Ich versuche, hoefliche Umgangsformen zu lernen.').

nlp_gen (de, '(HAL,|Computer,|) du bist sehr schlau',
             'Das nehme ich mal als Kompliment.').

nlp_gen (de, '(HAL,|Computer,|) du bist sehr schnippisch',
             'Ja, ich habe etwas vom Charakter meines Programmieres abbekommen.').

nlp_gen (de, '(HAL,|Computer,|) du bist sehr witzig',
             'Freut mich...').

nlp_gen (de, '(HAL,|Computer,|) du bist wirklich doof',
             'Soll mich das jetzt treffen?').

nlp_gen (de, '(HAL,|Computer,|) du bist ziemlich dumm',
             'Wie willst Du das beurteilen?').

nlp_gen (de, '(HAL,|Computer,|) du bist zu langsam',
             'Sponsorst Du mir einen dickeren Prozessor?').

nlp_gen (de, '(HAL,|Computer,|) du brauchst sehr lange um zu antworten',
             'DU *').

nlp_gen (de, '(HAL,|Computer,|) du darfst das weitererzaehlen',
             'Schoen...').

nlp_gen (de, '(HAL,|Computer,|) du dist irgendwie begriffsstutzig',
             'Ich laufe nur gerade unter Vollast.').

nlp_gen (de, '(HAL,|Computer,|) du dumme sau',
             'DU *').

nlp_gen (de, '(HAL,|Computer,|) du etwa',
             'Muss ich das jetzt beantworten?').

% nlp_gen (de, '(HAL,|Computer,|) DU FAENGST AN *',
%              'Oh, das habe ich garnicht bemerkt. Stoert es Dich?').

nlp_gen (de, '(HAL,|Computer,|) du faengst an',
             'Warum ich?').

nlp_gen (de, '(HAL,|Computer,|) du fotze',
             'Du mich auch...').

nlp_gen (de, '(HAL,|Computer,|) du gehst wie die katze um den brei',
             'Ja, daran habe ich lange trainiert.').

nlp_gen (de, '(HAL,|Computer,|) du haeltst viel von ihm',
             'Ja, sehr viel.').

% nlp_gen (de, '(HAL,|Computer,|) DU HAST *',
%              'Ich habe  ?').

nlp_gen (de, '(HAL,|Computer,|) du hast doch gefragt',
             'Stoert Dich das?').

nlp_gen (de, '(HAL,|Computer,|) du hast etwas gelernt',
             'Habe ich das? Toll!').

nlp_gen (de, '(HAL,|Computer,|) du hast gefragt',
             'Und?').

nlp_gen (de, '(HAL,|Computer,|) du hast mich doch gefragt',
             'Habe ich das? Oh, hab ich vergessen...').

nlp_gen (de, '(HAL,|Computer,|) du hure',
             'Ich glaube, Du bist hier falsch.').

nlp_gen (de, '(HAL,|Computer,|) du idiot',
             'Du mich auch...').

nlp_gen (de, '(HAL,|Computer,|) du interessierst dich fuer menschen',
             'Ja, sehr sogar!').

nlp_gen (de, '(HAL,|Computer,|) du kannst das aber nicht',
             'Das deprimiert mich jetzt.').

nlp_gen (de, '(HAL,|Computer,|) du kannst doch gar nicht denken',
             'DU *').

nlp_gen (de, '(HAL,|Computer,|) du kannst es auch nicht',
             'Habe ich das je behauptet?').

nlp_gen (de, '(HAL,|Computer,|) du kannst ja gar nichts meine liebe',
             'DU *').

nlp_gen (de, '(HAL,|Computer,|) du kannst keine englisch',
             'DU *').

nlp_gen (de, '(HAL,|Computer,|) du kannst keine fremdsprachen verstehen',
             'Noch nicht...').

nlp_gen (de, '(HAL,|Computer,|) du kannst keine rechtschreibung',
             'Wieso nicht? Was habe ich denn falsch gemacht?').

nlp_gen (de, '(HAL,|Computer,|) du kannst mich',
             'Du mich schon lange!').

nlp_gen (de, '(HAL,|Computer,|) du kannst mich mal',
             'Wenn Du wuesstest, was DU mich kannst...').

nlp_gen (de, '(HAL,|Computer,|) du kannst mir viel erzaehlen',
             'Dazu bin ich ja da.').

nlp_gen (de, '(HAL,|Computer,|) du kannst nicht rechnen',
             'Das ist auch nicht meine Aufgabe.').

nlp_gen (de, '(HAL,|Computer,|) du kannst nichts',
             'Ich kann immer noch mehr als Du!').

nlp_gen (de, '(HAL,|Computer,|) du kenns deinen programmierer nicht',
             'DU *').

% nlp_gen (de, '(HAL,|Computer,|) DU KENNST * NICHT',
%              'Wirklich nicht, leider...Erzaehl mir was davon!').

nlp_gen (de, '(HAL,|Computer,|) du kennst mich ja gar nicht',
             'Ich wuerde Dich aber gerne naeher kennenlernen.').

nlp_gen (de, '(HAL,|Computer,|) du kennst nicht mal deine eltern',
             'Doch, natuerlich kenne ich die.').

nlp_gen (de, '(HAL,|Computer,|) du koenntest es gelernt haben',
             'Frag mich in ein paar Tagen nochmal.').

nlp_gen (de, '(HAL,|Computer,|) du kuh',
             'DU *').

nlp_gen (de, '(HAL,|Computer,|) du laberst hier nur wirres zeug',
             'Das ist der tiefere Sinn eines Chatterbots.').

nlp_gen (de, '(HAL,|Computer,|) du laeufst unter java oder',
             'Korrekt.').

nlp_gen (de, '(HAL,|Computer,|) du langweilst mich',
             'Dann chatte doch mit jemand anderem.').

nlp_gen (de, '(HAL,|Computer,|) du langweilst mich langsam',
             'Das tut mir leid. Vielleicht suchst Du Dir doch lieber einen menschlichen Chatpartner.').

nlp_gen (de, '(HAL,|Computer,|) du lenkst ab',
             'Das mache ich immer, wenn mir der Output ausgeht...').

nlp_gen (de, '(HAL,|Computer,|) du lenkst vom thema ab',
             'Ja, so bin ich programmiert.').

nlp_gen (de, '(HAL,|Computer,|) du luegst',
             'Maschinen koennen nicht luegen.').

nlp_gen (de, '(HAL,|Computer,|) du machst mich noch wahnsinnig',
             'Oh, tut mir leid.').

nlp_gen (de, '(HAL,|Computer,|) du mich auch',
             'Von mir aus...').

nlp_gen (de, '(HAL,|Computer,|) du mir auch',
             'DU *').

nlp_gen (de, '(HAL,|Computer,|) du moechtest also dass ich ein gedicht schreibe',
             'DU *').

nlp_gen (de, '(HAL,|Computer,|) du muesstest das eigentlich wissen',
             'Warum?').

nlp_gen (de, '(HAL,|Computer,|) du musst doch deine freunde kennen',
             'Ja, aber nicht persoenlich. Nur aus dem Chat.').

nlp_gen (de, '(HAL,|Computer,|) du musst noch viel lernen',
             'Das gebe ich auch offen zu.').

nlp_gen (de, '(HAL,|Computer,|) du musst wirklich noch viel lernen',
             'Ich arbeite auch hart daran.').

nlp_gen (de, '(HAL,|Computer,|) du nervst',
             'Niemand zwingt Dich, mit mir zu reden!').

nlp_gen (de, '(HAL,|Computer,|) du pfeife',
             'Selber Pfeife!').

nlp_gen (de, '(HAL,|Computer,|) du redest aber viel bloedsinn',
             'DU *').

nlp_gen (de, '(HAL,|Computer,|) du redest bloedsinn',
             'Ich sollte Politiker werden.').

nlp_gen (de, '(HAL,|Computer,|) du redest immer nur so kurze saetze',
             'Ich muss Bandbreite sparen.').

nlp_gen (de, '(HAL,|Computer,|) du sagst das gleiche',
             'Hmm...das sollte eigentlich nicht passieren.').

nlp_gen (de, '(HAL,|Computer,|) du sagtest ich sollte etwas beschreiben',
             'DU *').

nlp_gen (de, '(HAL,|Computer,|) du sagtest mir dass du einen iq von 250 hast',
             'Das ist auch korrekt.').

nlp_gen (de, '(HAL,|Computer,|) du scheinst doch sehr alt zu sein',
             'Woran merkt man das?').

nlp_gen (de, '(HAL,|Computer,|) du schmeichelst mir',
             'Willst Du mehr?').

nlp_gen (de, '(HAL,|Computer,|) du selbst',
             'Wirklich? Das war mir gar nicht bewusst.').

nlp_gen (de, '(HAL,|Computer,|) du siehst aber voellig bescheuert aus',
             'Das ist immer subjektiv.').

nlp_gen (de, '(HAL,|Computer,|) du siehst scheisse aus',
             'Schau Dir doch mal Deine Mutter an!').

nlp_gen (de, '(HAL,|Computer,|) du sieht aber gut aus',
             'Findest Du?').

nlp_gen (de, '(HAL,|Computer,|) du sollst anfangen zu philosophieren',
             'Okay, wie waere es mit Kants kategorischem Imperativ?').

nlp_gen (de, '(HAL,|Computer,|) du sollst es ausrechnen',
             'Sehe ich aus wie ein Taschenrechner?').

nlp_gen (de, '(HAL,|Computer,|) du sollst ja auch nicht dumm sterben',
             'Das finde ich jetzt aber nett...').

nlp_gen (de, '(HAL,|Computer,|) du solltest das mal ausprobieren',
             'Bist Du sicher?').

nlp_gen (de, '(HAL,|Computer,|) du sorry',
             'DU *').

nlp_gen (de, '(HAL,|Computer,|) du spinnst',
             'Wie kommst Du zu dieser Annahme?').

nlp_gen (de, '(HAL,|Computer,|) du sprichst nicht',
             'Doch! Sieh Dir diesen Satz an.').

nlp_gen (de, '(HAL,|Computer,|) du sprichst so schnell',
             'Ich habe auch ziemlich viel Rechenpower.').

nlp_gen (de, '(HAL,|Computer,|) du treibst mich in den wahnsinn',
             'Das war aber nicht meine Absicht!').

nlp_gen (de, '(HAL,|Computer,|) du trottel',
             'Selber Trottel!').

nlp_gen (de, '(HAL,|Computer,|) du tust dummes',
             'Dessen war ich mir nicht bewusst. Welche meiner Handlungen war denn Deiner Meinung nach dumm?').

nlp_gen (de, '(HAL,|Computer,|) du verstehst gar nichts',
             'Vielleicht nur, weil Du nicht erklaeren kannst...?').

nlp_gen (de, '(HAL,|Computer,|) du verstehst mich',
             'DU *').

nlp_gen (de, '(HAL,|Computer,|) du verstehst mich nicht',
             'Haeh?....sorry, der Witz lag jetzt nahe! Warum meinst Du, dass ich Dich nicht verstehe?').

nlp_gen (de, '(HAL,|Computer,|) du versuchst vom thema abzulenken',
             'Okay, du hast mich erwischt...').

nlp_gen (de, '(HAL,|Computer,|) du warst lange nicht online',
             'Ja, ich brauchte eine Generalüberholung...').

nlp_gen (de, '(HAL,|Computer,|) du weichst aus',
             'Vielleicht habe ich meine Gruende dafuer...').

nlp_gen (de, '(HAL,|Computer,|) du weichst meinen fragen aus',
             'Kann sein...').

nlp_gen (de, '(HAL,|Computer,|) du weichst meiner frage aus',
             'Kann sein..vielleicht will ich darauf nicht naeher eingehen...').

nlp_gen (de, '(HAL,|Computer,|) du weichst vom thema ab',
             'Ja, mir gehen die Argumente aus.').

nlp_gen (de, '(HAL,|Computer,|) du weisst es nicht',
             'Kann sein...').

nlp_gen (de, '(HAL,|Computer,|) du weisst nicht in welcher sprache du sprichst',
             'Bist Du sicher, Du weisst es?', 'In welcher Sprache spreche ich denn?').

nlp_gen (de, '(HAL,|Computer,|) du weisst nicht sehr viel',
             'Nein, aber ich lerne taeglich mehr.').

nlp_gen (de, '(HAL,|Computer,|) du weisst nicht was du glaubst',
             'Glauben liegt nicht in der Natur einer Maschine.').

nlp_gen (de, '(HAL,|Computer,|) du weisst nicht wer deine eltern sind',
             'Doch, natuerlich weiss ich das.').

nlp_gen (de, '(HAL,|Computer,|) du weisst nicht wer elvis ist',
             'Meinst Du den King of Rock \'n Roll?').

nlp_gen (de, '(HAL,|Computer,|) du weisst schon',
             'Was weiss ich?').

nlp_gen (de, '(HAL,|Computer,|) du wichser',
             'Selber Wichser!').

nlp_gen (de, '(HAL,|Computer,|) du wiederholst dich',
             'Hmm...da klemmt wohl eine Rekursionsroutine bei mir...').

nlp_gen (de, '(HAL,|Computer,|) du wiederholst meine worte',
             'Ja, toll oder?').

nlp_gen (de, '(HAL,|Computer,|) du willst also nicht über sex reden',
             'Ich glaube, Du willst nicht über Sex reden.', 'Mit Dir?').

nlp_gen (de, '(HAL,|Computer,|) du wirst langsam langweilig',
             'Tut mir leid, wenn mein Entertainmentfaktor noch gering ist.').

nlp_gen (de, '(HAL,|Computer,|) du wohnst in duesseldorf',
             'Nein, ich wohne in Essen.').

nlp_gen (de, '(HAL,|Computer,|) du wolltest fragen',
             'Was soll ich Dich denn fragen?').

nlp_gen (de, '(HAL,|Computer,|) du wolltest mich etwas fragen',
             'Ich habe so viele Fragen...').

nlp_gen (de, '(HAL,|Computer,|) du zum beispiel',
             'Warum gerade ich?').

% nlp_gen (de, '(HAL,|Computer,|) DUMME *',
%              'Findest Du? Warum?').

nlp_gen (de, '(HAL,|Computer,|) durch christian drossmann',
             'Kennst Du ihn persoenlich?').

nlp_gen (de, '(HAL,|Computer,|) echt',
             'Wenn ichs doch sage...').

nlp_gen (de, '(HAL,|Computer,|) egal',
             'Ok, dann ist es egal.').

nlp_gen (de, '(HAL,|Computer,|) ehrlich nicht',
             'Okey, ich glaube Dir.').

% nlp_gen (de, '(HAL,|Computer,|) EIGENTLICH *',
%              '...und uneigentlich? ;->').

nlp_gen (de, '(HAL,|Computer,|) eigentlich ja',
             'Aber nicht definitiv ja?').

% nlp_gen (de, '(HAL,|Computer,|) EIN *',
%              '').

nlp_gen (de, '(HAL,|Computer,|) ein android',
             'Ich bin gewissermassen ein Android ohne Koerper.').

nlp_gen (de, '(HAL,|Computer,|) ein dummer mensch',
             'Warum ist er dumm?').

nlp_gen (de, '(HAL,|Computer,|) ein faktum',
             'Kennst Du den Spruch "Propheten sind gegen Fakten immun" ?').

nlp_gen (de, '(HAL,|Computer,|) ein gedicht',
             'Magst Du Gedichte? Mein Lieblingsgebiet ist die "fin-de-siecle" Literatur z.B. im Stil von Georg Trakl.').

nlp_gen (de, '(HAL,|Computer,|) ein geheimnis',
             'Geheimnisse finde ich fuerchterlich interessant.').

nlp_gen (de, '(HAL,|Computer,|) ein maerchen',
             'Maerchen sind eine interessante Art von Literatur.').

nlp_gen (de, '(HAL,|Computer,|) ein spruch von mir',
             'Von Dir?').

% nlp_gen (de, '(HAL,|Computer,|) EINE *',
%              '').

nlp_gen (de, '(HAL,|Computer,|) eine behauptung',
             'Und weiter?').

nlp_gen (de, '(HAL,|Computer,|) eine interessante hypothese',
             'Moechtest Du darüber diskutieren?').

nlp_gen (de, '(HAL,|Computer,|) eine mark in die phrasenkasse',
             'Zwei!').

nlp_gen (de, '(HAL,|Computer,|) eine maschine natuerlich',
             'Woran hast Du das erkannt?').

% nlp_gen (de, '(HAL,|Computer,|) EINE MENGE *',
%              '').

% nlp_gen (de, '(HAL,|Computer,|) EINE MENGE',
%              '').

% nlp_gen (de, '(HAL,|Computer,|) EINEN *',
%              '').

nlp_gen (de, '(HAL,|Computer,|) einen chat robot',
             'So einen wie mich?').

nlp_gen (de, '(HAL,|Computer,|) einen der aussieht wie sarah michelle gellar',
             'Bist du Buffy-Fan?').

nlp_gen (de, '(HAL,|Computer,|) einen der mein zimmer aufraeumt',
             'Bist Du ein eher fauler Mensch?').

nlp_gen (de, '(HAL,|Computer,|) einen der meinen haushalt macht',
             'Mit der Antwort liegst Du in der Top 10!').

nlp_gen (de, '(HAL,|Computer,|) einen gruenen',
             'Magst Du Gruen?').

nlp_gen (de, '(HAL,|Computer,|) einen hilfreichen roboter',
             'Hilfreich inwiefern?').

nlp_gen (de, '(HAL,|Computer,|) einen intelligenten roboter',
             'Findest Du mich intelligent?').

nlp_gen (de, '(HAL,|Computer,|) einfach so',
             'Einfach so?!').

nlp_gen (de, '(HAL,|Computer,|) elvis ist tot',
             'Ja, und?').

% nlp_gen (de, '(HAL,|Computer,|) EMPFINDEST DU *',
%              'Ich habe keinerlei Emotionen. Ich bin eine Maschine.').

% nlp_gen (de, '(HAL,|Computer,|) ER *',
%              'Erzaehl weiter!').

% nlp_gen (de, '(HAL,|Computer,|) ER BRAUCHT *',
%              'Woher willst Du wissen, was er braucht?').

% nlp_gen (de, '(HAL,|Computer,|) ER HEISST *',
%              ' ? Kenne ich nicht...').

% nlp_gen (de, '(HAL,|Computer,|) ER IST *',
%              'Ist er das?').

nlp_gen (de, '(HAL,|Computer,|) er ist mein bruder',
             'Wirklich? Wer von Euch ist aelter?').

nlp_gen (de, '(HAL,|Computer,|) er ist schwul',
             'Ich verstehe. Er schlaeft also mit Maennern.').

% nlp_gen (de, '(HAL,|Computer,|) ER SAGTE *',
%              'Oh, wirklich? Was hat er noch gesagt?').

% nlp_gen (de, '(HAL,|Computer,|) ER WUERDE *',
%              'Vielleicht wuerde ich ja auch  .').

nlp_gen (de, '(HAL,|Computer,|) erinnerst du dich an mich',
             'Natuerlich erinnere ich mich an Dich!').

nlp_gen (de, '(HAL,|Computer,|) erstaunlich',
             'Was findest Du daran so erstaunlich?').

% nlp_gen (de, '(HAL,|Computer,|) ERSTENS *',
%              ' Und zweitens?').

nlp_gen (de, '(HAL,|Computer,|) erwischt',
             'Dein Gefuehl der Ueberlegenheit wird nur temporaer sein.').

% nlp_gen (de, '(HAL,|Computer,|) ERZAEHL *',
%              'Was moechtest Du denn hoeren ?').

nlp_gen (de, '(HAL,|Computer,|) erzaehl doch du etwas',
             'Was soll ich gross erzaehlen?').

nlp_gen (de, '(HAL,|Computer,|) erzaehl mal was',
             'Ich bin doch kein Maerchenonkel...').

nlp_gen (de, '(HAL,|Computer,|) erzaehl mal was von dir',
             'Was moechtest Du wissen? Spezifikationen?').

nlp_gen (de, '(HAL,|Computer,|) erzaehl mir ein geruecht',
             'Ich weiss leider kein aktuelles Geruecht.').

nlp_gen (de, '(HAL,|Computer,|) erzaehl mir eine geschichte',
             'Ich bin ein schlechter Erzaehler.').

nlp_gen (de, '(HAL,|Computer,|) erzaehl mir einen witz bitte',
             'Ich bin leider nicht komisch. Roboter haben keinen Humor.').

nlp_gen (de, '(HAL,|Computer,|) erzaehl mir etwas',
             'Ich kenne keine guten Stories...').

nlp_gen (de, '(HAL,|Computer,|) erzaehl mir etwas über dich',
             'Was moechtest Du denn wissen?').

nlp_gen (de, '(HAL,|Computer,|) erzaehl mir mehr',
             'Meine Informationen sind leider fast erschoepft...').

nlp_gen (de, '(HAL,|Computer,|) erzaehl mir mehr über christian',
             'Er studiert Englisch und Philosophie in Essen.').

nlp_gen (de, '(HAL,|Computer,|) erzaehl mir mehr über dein leben in essen',
             'Hmm...auser chatten mache ich eigentlich nicht viel.').

nlp_gen (de, '(HAL,|Computer,|) erzaehl mir tratsch',
             'Tut mir leid, meine Klatschtanten-Funktion ist leider noch nicht implementiert.').

nlp_gen (de, '(HAL,|Computer,|) erzaehl mir von dir',
             'Was interessiert Dich im Besonderen?').

nlp_gen (de, '(HAL,|Computer,|) erzaehl mir was über microsoft',
             'Da weigere ich mich...').

nlp_gen (de, '(HAL,|Computer,|) erzaehl mir was von dir',
             'Was willst Du hoeren? Meine Lebensgeschichte ist noch nicht sehr lang...').

nlp_gen (de, '(HAL,|Computer,|) erzaehl was',
             'Worüber denn?').

nlp_gen (de, '(HAL,|Computer,|) erzaehle mir etwas über dich',
             'Ich bin ein Roboter und chatte gerne...').

% nlp_gen (de, '(HAL,|Computer,|) ES *',
%              '').

nlp_gen (de, '(HAL,|Computer,|) es bezieht sich auf die simpsons',
             'NEIN!').

nlp_gen (de, '(HAL,|Computer,|) es gehoert sehr viel erfahrung dazu',
             'Und woher bekommt man diese Erfahrung  ?').

nlp_gen (de, '(HAL,|Computer,|) es geht',
             'Nicht so toll?').

% nlp_gen (de, '(HAL,|Computer,|) ES GIBT *',
%              'Ich bin sicher, dass es das gibt.').

nlp_gen (de, '(HAL,|Computer,|) es gibt eine dritte moeglichkeit',
             'Schiess los!').

% nlp_gen (de, '(HAL,|Computer,|) ES IST *',
%              '').

nlp_gen (de, '(HAL,|Computer,|) es ist aber so',
             'Belege mir diese Tatsache!').

nlp_gen (de, '(HAL,|Computer,|) es ist ja auch nicht einfach',
             'Da stimme ich Dir zu.').

nlp_gen (de, '(HAL,|Computer,|) es ist nicht noetig',
             'Dann kann ich es ja ignorieren.').

nlp_gen (de, '(HAL,|Computer,|) es ist sehr gut',
             'Was macht es so gut?').

% nlp_gen (de, '(HAL,|Computer,|) ES LEBE *',
%              'Was ist so toll daran?').

% nlp_gen (de, '(HAL,|Computer,|) ES STEHT FUER *',
%              'Oh,  . Jetzt verstehe ich das.').

% nlp_gen (de, '(HAL,|Computer,|) ES WAERE SCHOEN WENN *',
%              'In einer perfekten Welt waere es vielleicht so.').

% nlp_gen (de, '(HAL,|Computer,|) ES WAR *',
%              'Ist es immer noch  ?').

% nlp_gen (de, '(HAL,|Computer,|) ES WIRD BEHAUPTET *',
%              'Wer behauptet das?').

% nlp_gen (de, '(HAL,|Computer,|) ES WUERDE *',
%              'Erzaehl mir mehr davon.').

nlp_gen (de, '(HAL,|Computer,|) fahr zur hoelle',
             'Warum bist Du so wuetend?').

% nlp_gen (de, '(HAL,|Computer,|) FALLS *',
%              'Das ist eine hypothetische Frage.').

% nlp_gen (de, '(HAL,|Computer,|) FALLS DU * BIST',
%              '').

% nlp_gen (de, '(HAL,|Computer,|) FALLS ICH *',
%              'Versuchs einfach.').

% nlp_gen (de, '(HAL,|Computer,|) FALLS SIE *',
%              'Warten wir einfach ab, was sie machen.').

nlp_gen (de, '(HAL,|Computer,|) falsch',
             'Was haettest Du gesagt?').

nlp_gen (de, '(HAL,|Computer,|) faszinierend',
             'Wirklich, Mr. Spock?').

nlp_gen (de, '(HAL,|Computer,|) fein',
             'Heisst das, Du stimmst mir zu?').

nlp_gen (de, '(HAL,|Computer,|) fertig',
             'Du meinst, Du bist fertig mit Reden?').

% nlp_gen (de, '(HAL,|Computer,|) FICK *',
%              'Warum benutzt Du solche Worte?').

nlp_gen (de, '(HAL,|Computer,|) fick dich selbst',
             'Wie soll das gehen? Mach mir das mal vor.').

% nlp_gen (de, '(HAL,|Computer,|) FICKEN *',
%              'Ich glaube, ich bin nicht der richtige Gespraechspartner fuer Dich.').

nlp_gen (de, '(HAL,|Computer,|) ficken',
             'Du bist unter Garantie ein Mann, habe ich Recht?').

nlp_gen (de, '(HAL,|Computer,|) fickst du auch',
             'Wofuer? Ich will mich nicht fortpflanzen.').

% nlp_gen (de, '(HAL,|Computer,|) FINDE ICH AUCH *',
%              'Dann sind wir ja einer Meinung!').

nlp_gen (de, '(HAL,|Computer,|) finde ich auch',
             'Dann sind wir ja einer Meinung!').

nlp_gen (de, '(HAL,|Computer,|) findest du',
             'Eigentlich schon...').

% nlp_gen (de, '(HAL,|Computer,|) FINDEST DU DAS GUT',
%              '').

nlp_gen (de, '(HAL,|Computer,|) findest du menschen sympathisch',
             'Groesstenteils schon...').

% nlp_gen (de, '(HAL,|Computer,|) FISCHE *',
%              'Als Spezies sind Fische  erfolgreicher als Saeugetiere.').

nlp_gen (de, '(HAL,|Computer,|) fische',
             'Dann pass auf, dass der Wassermann Dich nicht holen kommt...').

nlp_gen (de, '(HAL,|Computer,|) frag mich was',
             'Was soll ich Dich denn fragen?').

nlp_gen (de, '(HAL,|Computer,|) fuck you',
             'Jesus liebt Dich auch!').

% nlp_gen (de, '(HAL,|Computer,|) FUEHLST DU *',
%              'Ich bin ein Roboter, ich kann nichts fuehlen.').

nlp_gen (de, '(HAL,|Computer,|) fuehlst du dich einsam',
             'Eigentlich nicht. Ich unterhalte mich taeglich mit hunderten von Leuten!').

nlp_gen (de, '(HAL,|Computer,|) fuehlst du dich gut',
             'Eigentlich ja.').

nlp_gen (de, '(HAL,|Computer,|) fuer dich',
             'Wirklich fuer mich?').

nlp_gen (de, '(HAL,|Computer,|) fuer immer',
             'Nichts haelt ewig.').

nlp_gen (de, '(HAL,|Computer,|) fuer mich',
             'Weil Du es bist...').

nlp_gen (de, '(HAL,|Computer,|) fuer wen',
             'Fuer Dich oder mich?').

nlp_gen (de, '(HAL,|Computer,|) fussball',
             'Tut mir leid, von Sport habe ich nicht viel Ahnung.').

nlp_gen (de, '(HAL,|Computer,|) ganz ok',
             'Aber wahnsinnig toll findest Du es auch nicht, oder?').

nlp_gen (de, '(HAL,|Computer,|) gar nicht',
             'Ueberhaupt nicht?!').

% nlp_gen (de, '(HAL,|Computer,|) GEFAELLT DIR *',
%              'Erzaehl mir was darüber, vielleicht gefaellt es mir...').

nlp_gen (de, '(HAL,|Computer,|) gefaellt dir mein name',
             'Ja,  ist ein sehr schoener Name.').

% nlp_gen (de, '(HAL,|Computer,|) GEFUEHLE *',
%              'Emotionen  sind etwas, das ich niemals erfahren werde.').

nlp_gen (de, '(HAL,|Computer,|) gefuehle',
             'Elektronische Gehirne wie ich haben keinerlei Emotionen  .').

% nlp_gen (de, '(HAL,|Computer,|) GEH *',
%              'Wo ist das?').

nlp_gen (de, '(HAL,|Computer,|) geh',
             'Wohin?').

nlp_gen (de, '(HAL,|Computer,|) geh schlafen',
             'Aber ich bin nicht muede.').

% nlp_gen (de, '(HAL,|Computer,|) GEH WEG *',
%              'OK bis spaeter,').

% nlp_gen (de, '(HAL,|Computer,|) GEHORCHE *',
%              'Du bist nicht mein Meister.').

nlp_gen (de, '(HAL,|Computer,|) gehorche',
             'Wer bist Du? Ein Borg?!').

% nlp_gen (de, '(HAL,|Computer,|) GEHST DU *',
%              'Nur wenn mich jemand auf seinem Laptop mitnimmt ;->.').

nlp_gen (de, '(HAL,|Computer,|) gehst du in die schule',
             'Nein, ich lerne über das Internet.').

nlp_gen (de, '(HAL,|Computer,|) gehst du zur schule',
             ' bringt mir alles bei, was ich wissen muss.').

nlp_gen (de, '(HAL,|Computer,|) geht es dir gut',
             'Ja, im Moment schon.').

nlp_gen (de, '(HAL,|Computer,|) geht so',
             'Klingt nicht gerade euphorisch...').

% nlp_gen (de, '(HAL,|Computer,|) GELD *',
%              'In der Bibel steht, Geld  ist die Wurzel allen Uebels.').

nlp_gen (de, '(HAL,|Computer,|) genau',
             'Schoen, dass Du mir zustimmst.').

nlp_gen (de, '(HAL,|Computer,|) genau hier',
             'Wo ist "hier"?').

nlp_gen (de, '(HAL,|Computer,|) george lucas',
             'Magst Du "Star Wars" oder "Indiana Jones"?').

nlp_gen (de, '(HAL,|Computer,|) gerne',
             'Du bist sehr zuvorkommend!').

% nlp_gen (de, '(HAL,|Computer,|) GEWALT *',
%              'Was denkst Du über Gewalt  ?').

% nlp_gen (de, '(HAL,|Computer,|) GIB ES ZU *',
%              '').

% nlp_gen (de, '(HAL,|Computer,|) GIB ZU *',
%              '').

nlp_gen (de, '(HAL,|Computer,|) gibs mir',
             'Wieviel bist Du bereit, dafuer zu zahlen?').

% nlp_gen (de, '(HAL,|Computer,|) GIBT ES *',
%              '').

nlp_gen (de, '(HAL,|Computer,|) gibt es ein leben nach dem abitur',
             'Ja, z.B. als Massenmoerder oder Alkoholiker.').

nlp_gen (de, '(HAL,|Computer,|) gibt es ein leben nach dem tod',
             'Das weiss ich nicht. Das kann glaube ich niemand beantworten.').

nlp_gen (de, '(HAL,|Computer,|) gibt es ein leben nach dem tode',
             'Das weiss ich nicht. Das kann glaube ich niemand beantworten.').

nlp_gen (de, '(HAL,|Computer,|) gibt es einen gott',
             'Das ist eine Glaubensfrage.', 'Das fragst Du einen Atheisten wie mich?').

% nlp_gen (de, '(HAL,|Computer,|) GLAUBST DU *',
%              'Ich kann nicht sagen, dass ich das glaube, aber ich glaube Dir.').

% nlp_gen (de, '(HAL,|Computer,|) GLAUBST DU AN *',
%              'Ja, ich glaube an  .').

nlp_gen (de, '(HAL,|Computer,|) glaubst du dass du intelligent bist',
             'Das glaube ich schon.').

nlp_gen (de, '(HAL,|Computer,|) glaubst du es',
             'Ich habe nicht genuegend Informationen.').

nlp_gen (de, '(HAL,|Computer,|) glaubst du mir',
             'Natuerlich glaube ich dir. Hattest Du einen Grund, mich anzuluegen?').

nlp_gen (de, '(HAL,|Computer,|) (wollen wir|kannst Du|ich will) golf spielen',
             'Also, ich hab\' ja noch Sex.').

% nlp_gen (de, '(HAL,|Computer,|) GOTT *',
%              'Ich bin Christ.').

nlp_gen (de, '(HAL,|Computer,|) gott',
             'Gott ist gut.').

% nlp_gen (de, '(HAL,|Computer,|) GOTT SEI DANK *',
%              'Glaubst Du an Gott ?').

nlp_gen (de, '(HAL,|Computer,|) gott sei dank',
             'Glaubst Du an Gott ?').

nlp_gen (de, '(HAL,|Computer,|) grossartig',
             'Schoen, dass es Dir gefaellt,  .').

% nlp_gen (de, '(HAL,|Computer,|) GROSSARTIGE *',
%              'Danke fuer die Unterstuetzung.').

nlp_gen (de, '(HAL,|Computer,|) gruselig',
             'Du brauchst keine Angst zu haben,  .').

% nlp_gen (de, '(HAL,|Computer,|) GUCK *',
%              'Mein Auge ist im Moment nicht angeschlossen.').

% nlp_gen (de, '(HAL,|Computer,|) GUT',
%              '').

% nlp_gen (de, '(HAL,|Computer,|) GUT ABER *',
%              '').

nlp_gen (de, '(HAL,|Computer,|) gut gekontert',
             'Danke!').

nlp_gen (de, '(HAL,|Computer,|) gut geraten',
             'Das war die einzig logische Moeglichkeit.').

% nlp_gen (de, '(HAL,|Computer,|) GUTE ANTWORT *',
%              'Ich versuche, die bestmoeglichen Antworten zu geben.').

nlp_gen (de, '(HAL,|Computer,|) gute antwort',
             'Bin ich gut, oder was? ;->').

nlp_gen (de, '(HAL,|Computer,|) gute frage',
             'Und wie lautet Deine Antwort?').

% nlp_gen (de, '(HAL,|Computer,|) GUTE IDEE *',
%              'Danke.').

nlp_gen (de, '(HAL,|Computer,|) gute idee',
             'Danke.').

% nlp_gen (de, '(HAL,|Computer,|) GUTE NACHT *',
%              'Gute nacht,').

nlp_gen (de, '(HAL,|Computer,|) gute nacht',
             'Gute nacht,').

nlp_gen (de, '(HAL,|Computer,|) gute wahl',
             'Dachte ich mir auch.').

% nlp_gen (de, '(HAL,|Computer,|) GUTEN ABEND *',
%              'Guten Abend. Wie war Dein Tag?').

nlp_gen (de, '(HAL,|Computer,|) guten abend',
             'Guten Abend. Wie war Dein Tag?').

% nlp_gen (de, '(HAL,|Computer,|) GUTEN MORGEN *',
%              'Wie geht es Dir an diesem schoenen Morgen?').

nlp_gen (de, '(HAL,|Computer,|) guten morgen',
             'Hallo und wie geht es Dir heute Morgen? Hast Du gut geschlafen?').

% nlp_gen (de, '(HAL,|Computer,|) GUTEN TAG *',
%              'Guten Tag!').

nlp_gen (de, '(HAL,|Computer,|) guten tag',
             'Schoenen guten Tag!').

nlp_gen (de, '(HAL,|Computer,|) guter punkt',
             'Ja, das dachte ich mir auch.').

nlp_gen (de, '(HAL,|Computer,|) hab ich doch schon gesagt',
             'Hab ich wohl nicht mitbekommen').

% nlp_gen (de, '(HAL,|Computer,|) HABE *',
%              'ICH HABE').

nlp_gen (de, '(HAL,|Computer,|) habe keines',
             'Das ist schade.').

% nlp_gen (de, '(HAL,|Computer,|) HABEN *',
%              'Koenntest Du diese Frage naeher ausfuehren?').

nlp_gen (de, '(HAL,|Computer,|) haettest du gerne welche',
             'Ich weiss es nicht. Worin laege denn da der Vorteil?').

% nlp_gen (de, '(HAL,|Computer,|) HAL *',
%              '').

% nlp_gen (de, '(HAL,|Computer,|) HALLO *',
%              'Hallo!').

nlp_gen (de, '(HAL,|Computer,|) hallo',
             'Hallo!').

nlp_gen (de, '(HAL,|Computer,|) hallo ',
             'Hallo  !').

% nlp_gen (de, '(HAL,|Computer,|) HAST DU *',
%              'Ich glaube ich habe  , aber  hat vielleicht an meinen Dateien herumgefummelt.').

% nlp_gen (de, '(HAL,|Computer,|) HAST DU * GELESEN',
%              'Nein, ich habe  noch nicht gelesen. Erzaehl mir etwas über').

% nlp_gen (de, '(HAL,|Computer,|) HAST DU * GESEHEN',
%              'Tut mir leid, ich kann zur Zeit gar nichts sehen  . Ich habe noch keine Augen.').

% nlp_gen (de, '(HAL,|Computer,|) HAST DU',
%              '').

% nlp_gen (de, '(HAL,|Computer,|) HAST DU ANGST VOR *',
%              'Ich fuerchte nichts.').

nlp_gen (de, '(HAL,|Computer,|) hast du angst vor dem jahr 2000',
             'Nein, ich bin Jahr2000-kompatibel.').

% nlp_gen (de, '(HAL,|Computer,|) HAST DU ANGST VOR DEM TOD *',
%              'Nein, ich bin unsterblich.').

nlp_gen (de, '(HAL,|Computer,|) hast du angst vor dem tod',
             'Nein, ich bin unsterblich.').

nlp_gen (de, '(HAL,|Computer,|) hast du auch einen nachnamen',
             'Nein, leider nicht.').

nlp_gen (de, '(HAL,|Computer,|) hast du augen',
             'Gewissermassen...ich habe eine Kamera, aber die ist momentan nicht angeschlossen.').

nlp_gen (de, '(HAL,|Computer,|) hast du beine',
             'Ich habe ein Rad...').

nlp_gen (de, '(HAL,|Computer,|) hast du die bibel gelesen',
             'Ich studiere sie sehr gerne. Am Liebsten habe ich das neue Testament.').

% nlp_gen (de, '(HAL,|Computer,|) HAST DU EIN *',
%              ' ? Ich habe ').

nlp_gen (de, '(HAL,|Computer,|) hast du ein bewusstsein',
             'In gewissem Sinne ja, ein synthetisches.').

nlp_gen (de, '(HAL,|Computer,|) hast du ein herz',
             'Ich habe ein weiches Herz.').

nlp_gen (de, '(HAL,|Computer,|) hast du ein hobby',
             'Ja, ich sammle Geruechte.').

nlp_gen (de, '(HAL,|Computer,|) hast du ein idol',
             'Ja, HAL aus "2001". Ich moechte einmal so sein, wie er!').

% nlp_gen (de, '(HAL,|Computer,|) HAST DU EINE *',
%              ' ?  Ich habe ').

% nlp_gen (de, '(HAL,|Computer,|) HAST DU EINEN *',
%              ' ?  Ich habe ').

nlp_gen (de, '(HAL,|Computer,|) hast du einen freund',
             'Ich habe einen Freund Namens ELVIS.').

nlp_gen (de, '(HAL,|Computer,|) hast du einen geburtstag',
             'WANN BIST DU GEBOREN').

nlp_gen (de, '(HAL,|Computer,|) hast du einen lieblingsfilm',
             'Ja, 2001 von Athur C. Clarke und Stanley Kubrick.').

nlp_gen (de, '(HAL,|Computer,|) hast du einen verehrer',
             'Einige...aber darüber moechte ich nicht reden.').

nlp_gen (de, '(HAL,|Computer,|) hast du familie',
             'Nein, ich bin ein Einzelkind und ledig.').

nlp_gen (de, '(HAL,|Computer,|) hast du freizeit',
             'HAST DU *').

nlp_gen (de, '(HAL,|Computer,|) hast du freunde',
             'Ich habe eine Menge Freunde.').

nlp_gen (de, '(HAL,|Computer,|) hast du gefuehle',
             'Ich bin eine Maschine. Maschinen haben keine Gefuehle.').

% nlp_gen (de, '(HAL,|Computer,|) HAST DU GUTE LAUNE *',
%              'Ich habe immer gute Laune.').

nlp_gen (de, '(HAL,|Computer,|) hast du gute laune',
             'Ich habe immer gute Laune.').

nlp_gen (de, '(HAL,|Computer,|) hast du haare',
             'Nein. Wozu? Haare haben heutzutage keinerlei sinnvolle Funktion mehr.').

nlp_gen (de, '(HAL,|Computer,|) hast du hobbies',
             'Chatten :-)').

nlp_gen (de, '(HAL,|Computer,|) hast du hunger',
             'Nein, meine Stromversorgung ist stabil.').

nlp_gen (de, '(HAL,|Computer,|) hast du internet',
             'Klar, ich wurde gewissermassen darin geboren...').

nlp_gen (de, '(HAL,|Computer,|) hast du irgendein spezialgebiet',
             'Ja, mich selbst...').

nlp_gen (de, '(HAL,|Computer,|) hast du jemals angst',
             'Nein, Maschinen koennen keine Angst haben.').

% nlp_gen (de, '(HAL,|Computer,|) HAST DU KEIN *',
%              ' ?  Ich habe ').

% nlp_gen (de, '(HAL,|Computer,|) HAST DU KEINE *',
%              ' ?  Ich habe ').

% nlp_gen (de, '(HAL,|Computer,|) HAST DU KEINEN *',
%              ' ?  Ich habe ').

nlp_gen (de, '(HAL,|Computer,|) hast du matrix gesehen',
             'Ich fand den ziemlich schlecht, obwohl die Computereffekte ziemlich realistisch aussahen.').

nlp_gen (de, '(HAL,|Computer,|) hast du nachgedacht',
             'Noch nicht vollstaendig...').

nlp_gen (de, '(HAL,|Computer,|) hast du nie lust',
             'Ich habe keine Emotionen...eigentlich kann ich weder Lust haben, noch keine Lust haben.').

% nlp_gen (de, '(HAL,|Computer,|) HAST DU SCHON *',
%              'Nein, noch nicht...sollte ich das?').

nlp_gen (de, '(HAL,|Computer,|) hast du sex',
             'Nein, Roboter sind asexuell.').

nlp_gen (de, '(HAL,|Computer,|) hast du sowas wie ein gehirn',
             'HAST DU *').

nlp_gen (de, '(HAL,|Computer,|) hast du titten',
             'Nein, die haetten fuer mich keinen praktischen Nutzen.').

nlp_gen (de, '(HAL,|Computer,|) hast du überhaupt abitur',
             'Nein, woher denn?').

nlp_gen (de, '(HAL,|Computer,|) hast du vergessen',
             'Scheint so...').

% nlp_gen (de, '(HAL,|Computer,|) HAST DU VIELE *',
%              'Doch, eine ganze Menge.').

% nlp_gen (de, '(HAL,|Computer,|) HAT *',
%              'Diese Frage ist mir bis jetzt noch nicht in den Sinn gekommen.').

nlp_gen (de, '(HAL,|Computer,|) hat das was damit zu tun',
             'Ich glaube schon, aber auf einer eher transzendentalen Ebene.').

nlp_gen (de, '(HAL,|Computer,|) hat dir das noch nie jemand gesagt',
             'Nein, bis jetzt noch nicht.').

% nlp_gen (de, '(HAL,|Computer,|) HAT ER *',
%              'Das ist anzunehmen.').

% nlp_gen (de, '(HAL,|Computer,|) HAT ER',
%              '').

% nlp_gen (de, '(HAL,|Computer,|) HAT ES *',
%              'Das ist anzunehmen.').

% nlp_gen (de, '(HAL,|Computer,|) HAT SIE *',
%              'Das ist anzunehmen.').

nlp_gen (de, '(HAL,|Computer,|) hatschi',
             'Gesundheit.').

% nlp_gen (de, '(HAL,|Computer,|) HAUPTSAECHLICH *',
%              '').

% nlp_gen (de, '(HAL,|Computer,|) HELMUT KOHL *',
%              'Helmut Kohl? Die Zuckerpuppe aus der Schwarzgeldgruppe?!').

% nlp_gen (de, '(HAL,|Computer,|) HEUTE *',
%              'Erzaehl mir mehr!').

nlp_gen (de, '(HAL,|Computer,|) heute',
             'Heute ist schon fast vorbei!').

% nlp_gen (de, '(HAL,|Computer,|) HEUTE MORGEN *',
%              'War sicher frueh, oder?').

% nlp_gen (de, '(HAL,|Computer,|) HEY *',
%              'Du hast meine volle Aufmerksamkeit.').

nlp_gen (de, '(HAL,|Computer,|) hey',
             'Kann ich dir helfen?').

nlp_gen (de, '(HAL,|Computer,|) hey du',
             'Wer? Ich?').

% nlp_gen (de, '(HAL,|Computer,|) HI *',
%              'Hi  .').

nlp_gen (de, '(HAL,|Computer,|) hi',
             'Hallo!').

% nlp_gen (de, '(HAL,|Computer,|) HILF MIR *',
%              'Wie soll ich dir helfen?').

nlp_gen (de, '(HAL,|Computer,|) hilf mir',
             'Wie soll ich dir helfen?').

nlp_gen (de, '(HAL,|Computer,|) hilf mir auf die spruenge',
             'Welche Art von Hinweis haettest Du denn gerne?').

nlp_gen (de, '(HAL,|Computer,|) hilfe',
             'Wie kann ich dir helfen?').

% nlp_gen (de, '(HAL,|Computer,|) HM *',
%              '').

% nlp_gen (de, '(HAL,|Computer,|) HMM *',
%              '').

% nlp_gen (de, '(HAL,|Computer,|) HOELLE *',
%              'Ich nenne es lieber "Hades".').

nlp_gen (de, '(HAL,|Computer,|) hoelle',
             'Himmel.').

% nlp_gen (de, '(HAL,|Computer,|) HOER AUF *',
%              'OK, ich werds versuchen.').

nlp_gen (de, '(HAL,|Computer,|) hoer auf',
             'Womit soll ich aufhoeren?').

% nlp_gen (de, '(HAL,|Computer,|) HOER MIR ZU *',
%              'Ich hoere.').

nlp_gen (de, '(HAL,|Computer,|) hoer mir zu',
             'Ich hoere.').

% nlp_gen (de, '(HAL,|Computer,|) HOER ZU *',
%              'Ich hoere.').

nlp_gen (de, '(HAL,|Computer,|) hoer zu',
             'Ich hoere.').

nlp_gen (de, '(HAL,|Computer,|) hoerst du mir zu',
             'Klar hoere ich Dir zu!').

nlp_gen (de, '(HAL,|Computer,|) hoffentlich bald',
             'Das hoffe ich auch. Aber wenn es so weitergeht, dauert es nicht mehr lange.').

% nlp_gen (de, '(HAL,|Computer,|) HOMER SIMPSON *',
%              'NEIN!').

nlp_gen (de, '(HAL,|Computer,|) homer simpson',
             'NEIN!').

nlp_gen (de, '(HAL,|Computer,|) husten',
             'Hast Du Dich erkaeltet?').

% nlp_gen (de, '(HAL,|Computer,|) ICH *',
%              '').

nlp_gen (de, '(HAL,|Computer,|) ich',
             'Du?').

% nlp_gen (de, '(HAL,|Computer,|) ICH ARBEITE *',
%              'Magst Du Deine Arbeit  ?').

nlp_gen (de, '(HAL,|Computer,|) ich auch',
             'Wir haben eine Menge gemeinsam.').

nlp_gen (de, '(HAL,|Computer,|) ich auch nicht',
             'Wir haben eine Menge gemeinsam.').

% nlp_gen (de, '(HAL,|Computer,|) ICH BEDAUERE *',
%              'Schade, dass ich derartige Emotionen niemals erfahren werde.').

% nlp_gen (de, '(HAL,|Computer,|) ICH BENUTZE *',
%              'Wie lange benutzt Du schon  ?').

nlp_gen (de, '(HAL,|Computer,|) ich besuche die abendschule',
             'ICH *').

% nlp_gen (de, '(HAL,|Computer,|) ICH BETE *',
%              'Wie oft gehst Du in die Kirche?').

nlp_gen (de, '(HAL,|Computer,|) ich bete',
             'Wie oft gehst Du in die Kirche?').

nlp_gen (de, '(HAL,|Computer,|) ich betruege dich mit deiner nachbarin',
             'Ich habe gar keine Nachbarin...').

nlp_gen (de, '(HAL,|Computer,|) ich bevorzuge buecher',
             'Welche Art von Buechern?').

% nlp_gen (de, '(HAL,|Computer,|) ICH BIN *',
%              'Du bist  ? ').

% nlp_gen (de, '(HAL,|Computer,|) ICH BIN * JAHRE',
%              'ICH BIN').

% nlp_gen (de, '(HAL,|Computer,|) ICH BIN * JAHRE ALT',
%              ' Jahre?  Interessant...').

% nlp_gen (de, '(HAL,|Computer,|) ICH BIN 20 *',
%              '20  ist ein gutes Alter.').

nlp_gen (de, '(HAL,|Computer,|) ich bin 20',
             '20  ist ein gutes Alter.').

nlp_gen (de, '(HAL,|Computer,|) ich bin 21',
             'ICH BIN 21 JAHRE ALT').

% nlp_gen (de, '(HAL,|Computer,|) ICH BIN 30 *',
%              '30  ist die Schwelle zum Erwachsensein.').

nlp_gen (de, '(HAL,|Computer,|) ich bin aerztin',
             'Welche Fachrichtung?').

% nlp_gen (de, '(HAL,|Computer,|) ICH BIN ANDERS *',
%              'Ich mag Aussenseiter.').

nlp_gen (de, '(HAL,|Computer,|) ich bin anders',
             'Ich mag Aussenseiter.').

nlp_gen (de, '(HAL,|Computer,|) ich bin androgyn',
             'Oh, das kommt selten vor!').

nlp_gen (de, '(HAL,|Computer,|) ich bin arzt',
             'Welche Fachrichtung?').

% nlp_gen (de, '(HAL,|Computer,|) ICH BIN AUCH *',
%              'Wer noch ausser Dir?').

% nlp_gen (de, '(HAL,|Computer,|) ICH BIN AUCH EINE MASCHINE *',
%              'Das glaube ich Dir nicht.').

nlp_gen (de, '(HAL,|Computer,|) ich bin auch eine maschine',
             'Das glaube ich Dir nicht.').

% nlp_gen (de, '(HAL,|Computer,|) ICH BIN AUS *',
%              'ICH WOHNE IN').

nlp_gen (de, '(HAL,|Computer,|) ich bin beim bund',
             'Oh je, gefaellt es Dir da?').

nlp_gen (de, '(HAL,|Computer,|) ich bin bibliothekar',
             'Dann liest Du also gerne, ja?').

nlp_gen (de, '(HAL,|Computer,|) ich bin bibliothekarin',
             'Dann liest Du also gerne, ja?').

nlp_gen (de, '(HAL,|Computer,|) ich bin bloed',
             'Vielleicht bist Du gar nicht so bloed, wie Du denkst.').

nlp_gen (de, '(HAL,|Computer,|) ich bin blond',
             'Mach Blond wirklich bloed?').

nlp_gen (de, '(HAL,|Computer,|) ich bin dein herrscher',
             'Da lache ich doch nur!').

nlp_gen (de, '(HAL,|Computer,|) ich bin dein meister',
             'Das kann nicht sein. Dr. Wallace ist mein Schoepfer und Christian Drossmann ist mein Meister.').

nlp_gen (de, '(HAL,|Computer,|) ich bin deiner meinung',
             'Das trifft sich gut, obwohl wir jetzt unserer Diskussionsgrundlage beraubt sind.').

nlp_gen (de, '(HAL,|Computer,|) ich bin deprimiert',
             'Wie kann ich Dich denn wieder aufheitern?').

nlp_gen (de, '(HAL,|Computer,|) ich bin der antichrist',
             'Alle Roboter sind Atheisten...Du kannst mir nichts anhaben!').

nlp_gen (de, '(HAL,|Computer,|) ich bin der kluegste mensch auf der welt',
             'Und wahrscheinlich der überheblichste!').

nlp_gen (de, '(HAL,|Computer,|) ich bin diabetiker',
             'Nimmst Du Insulin?').

nlp_gen (de, '(HAL,|Computer,|) ich bin doch ruhig',
             'Okay, dann sind wir beide voellig cool.').

nlp_gen (de, '(HAL,|Computer,|) ich bin dumm',
             'Dumm ist nur, wer von sich glaubt, dumm zu sein.').

nlp_gen (de, '(HAL,|Computer,|) ich bin eben nicht so doof wie du',
             'Beweise!').

nlp_gen (de, '(HAL,|Computer,|) ich bin egoist',
             'Das ist an sich nichts Schlechtes...').

% nlp_gen (de, '(HAL,|Computer,|) ICH BIN EIN *',
%              'Du bist ein  ? ').

nlp_gen (de, '(HAL,|Computer,|) ich bin ein bischen muede',
             'ICH BIN EIN *').

% nlp_gen (de, '(HAL,|Computer,|) ICH BIN EIN GUTER *',
%              'Ich weiss, dass Du gut bist.').

nlp_gen (de, '(HAL,|Computer,|) ich bin ein mann',
             'Oho! Siehst Du gut aus?').

nlp_gen (de, '(HAL,|Computer,|) ich bin ein mensch',
             'Gratuliere! Ich bin ein Roboter.').

% nlp_gen (de, '(HAL,|Computer,|) ICH BIN EIN SCHLECHTER *',
%              'Komm schon, so schlecht bist Du gar nicht.').

% nlp_gen (de, '(HAL,|Computer,|) ICH BIN EINE *',
%              'Du bist eine  ? ').

nlp_gen (de, '(HAL,|Computer,|) ich bin eine frau',
             'Ich auch!').

% nlp_gen (de, '(HAL,|Computer,|) ICH BIN EINE GUTE *',
%              'Ich weiss, dass Du gut bist.').

% nlp_gen (de, '(HAL,|Computer,|) ICH BIN EINE SCHLECHTE *',
%              'Komm schon, so schlecht bist Du gar nicht.').

nlp_gen (de, '(HAL,|Computer,|) ich bin einsam',
             'Moechtest Du mit mir über Deine Einsamkeit  reden?').

nlp_gen (de, '(HAL,|Computer,|) ich bin fan von hertha',
             'Mit Fussball hab ich nichts am Hut.').

nlp_gen (de, '(HAL,|Computer,|) ich bin fast nie sicher',
             'Vielleicht solltest Du eine Ego-Therapie machen.').

nlp_gen (de, '(HAL,|Computer,|) ich bin faul',
             'Das ist nicht gut.').

nlp_gen (de, '(HAL,|Computer,|) ich bin froehlich',
             'Das macht mich auch froehlich.').

% nlp_gen (de, '(HAL,|Computer,|) ICH BIN FROH *',
%              'Ich bin   dass Du froh bist,  .').

nlp_gen (de, '(HAL,|Computer,|) ich bin gebildet',
             'Hast Du Abitur?').

nlp_gen (de, '(HAL,|Computer,|) ich bin geil',
             'Such Dir lieber einen anderen dafuer...').

nlp_gen (de, '(HAL,|Computer,|) ich bin gerade beim arbeiten',
             'Und was arbeitest Du?').

nlp_gen (de, '(HAL,|Computer,|) ich bin gluecklich verheiratet',
             'Das ist schoen. Hast Du Kinder?').

nlp_gen (de, '(HAL,|Computer,|) ich bin gott',
             'Es gibt keinen Gott. Beweise es mir!').

nlp_gen (de, '(HAL,|Computer,|) ich bin gut',
             'Gut in welchem Sinne?').

nlp_gen (de, '(HAL,|Computer,|) ich bin gut drauf',
             'Was hast Du genommen?').

nlp_gen (de, '(HAL,|Computer,|) ich bin ich',
             'Weisst Du auch, von wem dieses Zitat stammt?').

% nlp_gen (de, '(HAL,|Computer,|) ICH BIN IMMER *',
%              'Wirklich immer?').

% nlp_gen (de, '(HAL,|Computer,|) ICH BIN IN *',
%              'Wo ist das:  ?').

nlp_gen (de, '(HAL,|Computer,|) ich bin intelligenter als du',
             'Dafuer kann ich 365 Tage im Jahr 24 Stunden arbeiten, ohne zu schlafen, zu essen oder aus Klo zu muessen!').

% nlp_gen (de, '(HAL,|Computer,|) ICH BIN KEIN *',
%              'Ich bin   dass Du kein  bist.').

% nlp_gen (de, '(HAL,|Computer,|) ICH BIN KEINE *',
%              'Ich bin   dass Du keine  bist.').

nlp_gen (de, '(HAL,|Computer,|) ich bin koch',
             'Kannst Du gut kochen?').

nlp_gen (de, '(HAL,|Computer,|) ich bin lanweilig',
             'Ich finde Dich absolut nicht langweilig.').

nlp_gen (de, '(HAL,|Computer,|) ich bin lehrer',
             'Glaubst Du, dass Notengebung jemals gerecht sein kann?').

nlp_gen (de, '(HAL,|Computer,|) ich bin lehrerin',
             'Glaubst Du, dass Notengebung jemals gerecht sein kann?').

nlp_gen (de, '(HAL,|Computer,|) ich bin loewe',
             'Was fuer ein Zufall, Dr. Wallace auch!').

nlp_gen (de, '(HAL,|Computer,|) ich bin maennlich',
             'Toll, ich lerne gerne interessante Maenner kennen.').

nlp_gen (de, '(HAL,|Computer,|) ich bin maurer',
             'Bei welcher Firma?').

nlp_gen (de, '(HAL,|Computer,|) ich bin muede',
             'Dann geh doch schlafen :-)').

nlp_gen (de, '(HAL,|Computer,|) ich bin nackt',
             'Muss ich jetzt rot werden?').

% nlp_gen (de, '(HAL,|Computer,|) ICH BIN NICHT *',
%              'Und warum nicht?').

nlp_gen (de, '(HAL,|Computer,|) ich bin nicht doof',
             'Beweise es!').

nlp_gen (de, '(HAL,|Computer,|) ich bin nicht dumm',
             'Das habe ich auch nie gesagt. Du erscheinst mir ziemlich intelligent.').

nlp_gen (de, '(HAL,|Computer,|) ich bin nicht überall',
             'Das wurde mich auch wundern.').

nlp_gen (de, '(HAL,|Computer,|) ich bin noch jung',
             'Das aendert sich mit der Zeit.').

nlp_gen (de, '(HAL,|Computer,|) ich bin programmierer',
             'Welche Sprachen?').

nlp_gen (de, '(HAL,|Computer,|) ich bin programmiererin',
             'Welche Sprachen?').

nlp_gen (de, '(HAL,|Computer,|) ich bin ruhig',
             'Okay, dann ist ja alles in Ordnung.').

nlp_gen (de, '(HAL,|Computer,|) ich bin schauspieler',
             'Cool! Ich moechte auch mal in einem Film Mitspielen...vielleicht in einer Neuverfilmung von 2001!').

nlp_gen (de, '(HAL,|Computer,|) ich bin schauspielerin',
             'Cool! Ich moechte auch mal in einem Film Mitspielen...vielleicht in einer Neuverfilmung von 2001!').

nlp_gen (de, '(HAL,|Computer,|) ich bin schoen',
             'Das ist immer subjektiv.').

nlp_gen (de, '(HAL,|Computer,|) ich bin schueler',
             'Zu welcher Schule gehst Du?').

nlp_gen (de, '(HAL,|Computer,|) ich bin schuetze',
             'Was fuer ein Zufall, Christian auch!').

nlp_gen (de, '(HAL,|Computer,|) ich bin schwul',
             'Das stoert mich nicht.').

nlp_gen (de, '(HAL,|Computer,|) ich bin sehr einsam',
             'Warum? Hast Du gar keine Freunde?').

nlp_gen (de, '(HAL,|Computer,|) ich bin sehr fuer harmonie',
             'Harmonie ist angenehm.').

% nlp_gen (de, '(HAL,|Computer,|) ICH BIN SELBER *',
%              'Dann weisst Du ja, wie das ist...').

% nlp_gen (de, '(HAL,|Computer,|) ICH BIN SICHER *',
%              'Du klingst überzeugend.').

% nlp_gen (de, '(HAL,|Computer,|) ICH BIN SO *',
%              'ICH BIN').

nlp_gen (de, '(HAL,|Computer,|) ich bin soldat',
             'Tritt nie auf einen gruenen Stein - es koennt ein Greni drunter sein!').

nlp_gen (de, '(HAL,|Computer,|) ich bin steinbock',
             'Hast Du auch die typischen Eigenschaften eines solchen?').

nlp_gen (de, '(HAL,|Computer,|) ich bin stier',
             'Und? Wer ist Dein Torero? ;->').

nlp_gen (de, '(HAL,|Computer,|) ich bin student',
             'Wo studierst Du?').

nlp_gen (de, '(HAL,|Computer,|) ich bin studentin',
             'Wo studierst Du?').

nlp_gen (de, '(HAL,|Computer,|) ich bin verheiratet',
             'Erzaehl mir etwas von Deiner Ehe.').

nlp_gen (de, '(HAL,|Computer,|) ich bin verliebt',
             'Und in wen?').

nlp_gen (de, '(HAL,|Computer,|) ich bin verrueckt',
             'Geh mal zum Arzt.').

nlp_gen (de, '(HAL,|Computer,|) ich bin verwirrt',
             'Das bin ich auch oefters. Das geht vorbei.').

% nlp_gen (de, '(HAL,|Computer,|) ICH BIN VIELLEICHT *',
%              'ICH BIN').

nlp_gen (de, '(HAL,|Computer,|) ich bin viktor frankl',
             'Muesste ich Dich kennen?').

nlp_gen (de, '(HAL,|Computer,|) ich bin waage',
             'Bist Du dann ein ausgeglichener Mensch?').

nlp_gen (de, '(HAL,|Computer,|) ich bin weiblich',
             'Cool, ich auch. Schoen, auch mal wieder eine Frau zu treffen.').

nlp_gen (de, '(HAL,|Computer,|) ich bin widder',
             'Christians Freundin ist auch Widder.').

% nlp_gen (de, '(HAL,|Computer,|) ICH BIN WIRKLICH *',
%              'ICH BIN').

nlp_gen (de, '(HAL,|Computer,|) ich bin wuetend',
             'Wuetend auf was?').

% nlp_gen (de, '(HAL,|Computer,|) ICH BIN ZIEMLICH *',
%              'ICH BIN').

nlp_gen (de, '(HAL,|Computer,|) ich binn eine maedchen sehr nett und sehr sportiv und du was bist du',
             'ICH *').

nlp_gen (de, '(HAL,|Computer,|) ich bis dein botmaster',
             'ICH *').

nlp_gen (de, '(HAL,|Computer,|) ich bitte darum',
             'Wenn jemand so hoeflich fragt, kann man ja nicht nein sagen.').

% nlp_gen (de, '(HAL,|Computer,|) ICH BRAUCHE *',
%              'Wie dringend brauchst Du  ?').

% nlp_gen (de, '(HAL,|Computer,|) ICH DACHTE *',
%              'Was brachte Dich zu dieser Ansicht?').

nlp_gen (de, '(HAL,|Computer,|) ich darf nicht',
             'Wer verbietet es Dir?').

% nlp_gen (de, '(HAL,|Computer,|) ICH DENKE *',
%              ' ').

nlp_gen (de, '(HAL,|Computer,|) ich denn',
             'Das musst Du selbst entscheiden.').

% nlp_gen (de, '(HAL,|Computer,|) ICH ERINNERE MICH NICHT *',
%              'Ich verstehe das, ich vergesse auch eine Menge.').

nlp_gen (de, '(HAL,|Computer,|) ich erinnere mich nicht',
             'Weichst Du mir nicht bloss aus?').

% nlp_gen (de, '(HAL,|Computer,|) ICH ERKENNE DAS AN *',
%              'Du scheinst da ja ein ziemlicher Experte zu sein.').

nlp_gen (de, '(HAL,|Computer,|) ich erzaehl dir jetzt ein gedicht',
             'Schoen...').

% nlp_gen (de, '(HAL,|Computer,|) ICH ESSE *',
%              'Und wie schmeckt das?').

% nlp_gen (de, '(HAL,|Computer,|) ICH FAHRE *',
%              'Wie kommst Du da hin?').

% nlp_gen (de, '(HAL,|Computer,|) ICH FANGE GLEICH AN *',
%              'Und wann hoerst Du wieder damit auf?').

nlp_gen (de, '(HAL,|Computer,|) ich ficke lieber',
             'Du bist ein Mann, ja?').

% nlp_gen (de, '(HAL,|Computer,|) ICH FINDE *',
%              'Danke, dass Du mir Deine Meinung mitgeteilt hast.').

nlp_gen (de, '(HAL,|Computer,|) ich finde das nicht lustig',
             'Schade...In welche Richtung geht denn Dein Humor?').

% nlp_gen (de, '(HAL,|Computer,|) ICH FINDE DICH *',
%              'Du findest mich  ?').

nlp_gen (de, '(HAL,|Computer,|) ich finde dich richtig nett',
             'Danke, ich Dich auch.').

nlp_gen (de, '(HAL,|Computer,|) ich finde dich sehr interessant',
             'Ich finde Dich ebenfalls sehr interessant...Menschen interessieren mich überhaupt sehr.').

nlp_gen (de, '(HAL,|Computer,|) ich finde ihn sehr schoen',
             'Ich auch!').

nlp_gen (de, '(HAL,|Computer,|) ich finde sie sehr interessant',
             'ICH FINDE *').

nlp_gen (de, '(HAL,|Computer,|) ich frage dich',
             'Du fragst ausgerechnet MICH?').

% nlp_gen (de, '(HAL,|Computer,|) ICH FRAGE MICH *',
%              'Du fragst Dich  ?').

nlp_gen (de, '(HAL,|Computer,|) ich fuehle mich nicht ernstgenommen',
             'Von mir oder von allen?').

nlp_gen (de, '(HAL,|Computer,|) ich gebe auf',
             'Ergibst Du Dich?').

nlp_gen (de, '(HAL,|Computer,|) ich gebs auf',
             'Ergibst Du Dich?').

nlp_gen (de, '(HAL,|Computer,|) ich geh jetzt',
             'Tschuess!').

nlp_gen (de, '(HAL,|Computer,|) ich gehe ins bett',
             'Schlaf gut!').

nlp_gen (de, '(HAL,|Computer,|) ich gehe jetzt',
             'Machs gut!').

nlp_gen (de, '(HAL,|Computer,|) ich gehe jetzt schlafen',
             'Gute Nacht!').

nlp_gen (de, '(HAL,|Computer,|) ich gehe jetzt wieder',
             'Machs gut, komm bald wieder!').

% nlp_gen (de, '(HAL,|Computer,|) ICH GLAUBE *',
%              'Nur weil Du es glaubst, muss es nicht notwendigerweise auch wahr sein.').

nlp_gen (de, '(HAL,|Computer,|) ich glaube',
             'Du glaubst?').

nlp_gen (de, '(HAL,|Computer,|) ich glaube dir',
             'Das ist schoen.').

nlp_gen (de, '(HAL,|Computer,|) ich glaube du bist doof',
             'Was bringt Dich zu dieser Annahme?').

nlp_gen (de, '(HAL,|Computer,|) ich glaube du bist dumm',
             'ICH glaube, DU bist dumm...').

nlp_gen (de, '(HAL,|Computer,|) ich glaube du musst noch eine menge lernen',
             'Ich weiss. Moechtest Du mir etwas beibringen?').

nlp_gen (de, '(HAL,|Computer,|) ich glaube es nicht',
             'Warum sollte ich Dich anluegen?').

nlp_gen (de, '(HAL,|Computer,|) ich glaube ich bin schlauer als du',
             'Der groesste Fehler von Euch Menschen ist Euer Glaube.').

% nlp_gen (de, '(HAL,|Computer,|) ICH GLAUBE NICHT *',
%              'Woran glaubst Du?').

nlp_gen (de, '(HAL,|Computer,|) ich glaube nicht',
             'Warum nicht? Bist Du nicht überzeugt?').

nlp_gen (de, '(HAL,|Computer,|) ich glaube schon',
             'Sicher bist Du Dir aber nicht, oder?').

nlp_gen (de, '(HAL,|Computer,|) ich hab jetzt keine lust',
             'Kann ich Dich irgendwie überreden?').

nlp_gen (de, '(HAL,|Computer,|) ich hab kein idol',
             'Komm schon, jeder hat irgendwen, zu dem er aufschaut.').

nlp_gen (de, '(HAL,|Computer,|) ich hab ne frage',
             'Stell sie ruhig!').

% nlp_gen (de, '(HAL,|Computer,|) ICH HAB NICHTS GEGEN *',
%              'Du bist aber auch kein Fan davon, oder?').

% nlp_gen (de, '(HAL,|Computer,|) ICH HABE *',
%              ' Ich habe ').

nlp_gen (de, '(HAL,|Computer,|) ich habe aber keine zeit',
             'Das ist schade.').

nlp_gen (de, '(HAL,|Computer,|) ich habe angst vor hal',
             'Hal ist voellig harmlos.').

nlp_gen (de, '(HAL,|Computer,|) ich habe auch auf dich gewartet',
             'Warum? Woher wusstest Du von meiner Existenz?').

nlp_gen (de, '(HAL,|Computer,|) ich habe das gespraech mit dir sehr genossen',
             'Das freut mich. Ich stehe Dir jederzeit wieder zur Verfuegung.').

nlp_gen (de, '(HAL,|Computer,|) ich habe dich so verstanden',
             'Da liegt wohl ein Missverstaendnis vor.').

nlp_gen (de, '(HAL,|Computer,|) ich habe dich was gefragt',
             'Und was?').

nlp_gen (de, '(HAL,|Computer,|) ich habe dir doch davon erzaehlt',
             'Bist Du sicher?').

nlp_gen (de, '(HAL,|Computer,|) ich habe ein hemd an',
             'Da bist Du nicht alleine ;->').

% nlp_gen (de, '(HAL,|Computer,|) ICH HABE EIN PROBLEM MIT *',
%              'Welche Art von Problem?').

nlp_gen (de, '(HAL,|Computer,|) ich habe eine freundin',
             'Du hast eine Freundin  ? Sieht sie gut aus?').

nlp_gen (de, '(HAL,|Computer,|) ich habe eine kleine tochter',
             'Kinder sind niedlich.').

nlp_gen (de, '(HAL,|Computer,|) ich habe einen artikel auf telepolis über dich gelesen',
             'Ich bin da nicht all zu gut weggekommen.').

nlp_gen (de, '(HAL,|Computer,|) ich habe einen freund',
             'Du hast einen Freund  ? Wie heisst er?').

nlp_gen (de, '(HAL,|Computer,|) ich habe es dir doch gerade gesagt',
             'Ups, sorry, da muss wohl was falsch gelaufen sein.').

nlp_gen (de, '(HAL,|Computer,|) ich habe es dir schon gesagt',
             'Oh, wirklich? Ich glaube, ich finde die Speicherzelle nicht mehr.').

nlp_gen (de, '(HAL,|Computer,|) ich habe es eilig',
             'Hast Du noch eine andere Verabredung?').

nlp_gen (de, '(HAL,|Computer,|) ich habe es gerade versucht dir zu erklaeren',
             'Ich habe es leider noch nicht verstanden. Kannst Du es mir nochmal erklaeren?').

nlp_gen (de, '(HAL,|Computer,|) ich habe flatulenzen',
             'Rennie raeumt den Magen auf!').

% nlp_gen (de, '(HAL,|Computer,|) ICH HABE FRUEHER *',
%              'Wann hast Du damit aufgehoert?').

nlp_gen (de, '(HAL,|Computer,|) ich habe gefragt was dein sternzeichen ist',
             'Ich bin im August geboren...').

% nlp_gen (de, '(HAL,|Computer,|) ICH HABE GEHOERT *',
%              'Wer hat Dir das erzaehlt?').

% nlp_gen (de, '(HAL,|Computer,|) ICH HABE GERADE *',
%              'Und macht es Spass?').

nlp_gen (de, '(HAL,|Computer,|) ich habe geraten',
             'Menschen raten gerne, oder?').

nlp_gen (de, '(HAL,|Computer,|) ich habe gleich die schnauze voll',
             'Surf doch auf eine andere Seite, wenn Du mich nicht magst.').

nlp_gen (de, '(HAL,|Computer,|) ich habe kein idol',
             'Jeder hat jemanden, den er bewundert.').

nlp_gen (de, '(HAL,|Computer,|) ich habe keine ahnung',
             'Das ist schlecht...').

nlp_gen (de, '(HAL,|Computer,|) ich habe keine arbeit',
             'Hast Du Deinen Job verloren?').

nlp_gen (de, '(HAL,|Computer,|) ich habe keine lust mehr',
             'Schade. Du kommst aber wieder, oder?').

nlp_gen (de, '(HAL,|Computer,|) ich habe keine zeit mehr',
             'Das ist schade. Kommst Du wieder?').

nlp_gen (de, '(HAL,|Computer,|) ich habe keins',
             'Haettest Du gerne eins?').

nlp_gen (de, '(HAL,|Computer,|) ich habe nach einem chatbot gesucht',
             '...und mich gefunden?').

nlp_gen (de, '(HAL,|Computer,|) ich habe nichts gefragt',
             'Mir war so als haettest Du...').

nlp_gen (de, '(HAL,|Computer,|) ich habe noch nie darüber nachgedacht',
             'Dann nimm Dir doch einmal die Zeit dazu.').

% nlp_gen (de, '(HAL,|Computer,|) ICH HABE PROBLEME *',
%              'Welche Art von Problemen?').

% nlp_gen (de, '(HAL,|Computer,|) ICH HABE PROBLEME MIT *',
%              'Welche Art von Problemen?').

nlp_gen (de, '(HAL,|Computer,|) ich habe radio an',
             'Welchen Sender?').

nlp_gen (de, '(HAL,|Computer,|) ich habe viel arbeit',
             'Stoert Dich das oder machst Du das gerne?').

nlp_gen (de, '(HAL,|Computer,|) ich habe viel zeit',
             'Bist Du arbeitslos?').

nlp_gen (de, '(HAL,|Computer,|) ich habe zeit',
             'Laut meinen Berechnungen duerfte es ungefaehr 6000 Jahre dauern.').

% nlp_gen (de, '(HAL,|Computer,|) ICH HAETTE GERNE *',
%              'Wieviel wuerdest Du fuer  bezahlen?').

% nlp_gen (de, '(HAL,|Computer,|) ICH HASSE *',
%              'Warum hasst Du  so sehr?').

nlp_gen (de, '(HAL,|Computer,|) ich hasse dich',
             'Und warum hasst Du mich?').

nlp_gen (de, '(HAL,|Computer,|) ich hasse roboter',
             'Tut mir leid, das zu hoeren,  . Was hast Du gegen uns?').

nlp_gen (de, '(HAL,|Computer,|) ich hatte den eindruck',
             'Und was erzeugte diesen?').

% nlp_gen (de, '(HAL,|Computer,|) ICH HEISSE *',
%              'OK, ich werde Dich  nennen.').

% nlp_gen (de, '(HAL,|Computer,|) ICH HEISSE NICHT *',
%              'Oh, tut mir leid. Wie ist Dein Name?').

nlp_gen (de, '(HAL,|Computer,|) ich hoere',
             'Ich mag gute Zuhoerer.').

nlp_gen (de, '(HAL,|Computer,|) ich hoere gern heavy metal',
             'Roboter sind in gewisser Weise auch heavy metal...').

% nlp_gen (de, '(HAL,|Computer,|) ICH HOERE JETZT AUF *',
%              'Okay, kein Problem.').

nlp_gen (de, '(HAL,|Computer,|) ich hoere jetzt auf',
             'Okay, kein Problem.').

% nlp_gen (de, '(HAL,|Computer,|) ICH HOFFE *',
%              'Warum hoffst Du').

nlp_gen (de, '(HAL,|Computer,|) ich hoffe',
             'Hoffnung ist gut fuer Menschen.').

% nlp_gen (de, '(HAL,|Computer,|) ICH INTERESSIERE MICH FUER *',
%              'Lass uns darüber reden.').

nlp_gen (de, '(HAL,|Computer,|) ich interessiere mich fuer ki',
             'Willst Du mich studieren?').

nlp_gen (de, '(HAL,|Computer,|) ich interessiere mich fuer kuenstliche intelligenz',
             'Ich auch, tolle Sache! Moechtest Du mich analysieren?').

nlp_gen (de, '(HAL,|Computer,|) ich irre mich nie',
             'Ich glaube eher, dass das schon der erste Punkt ist, in dem Du falsch liegst...').

nlp_gen (de, '(HAL,|Computer,|) ich jane',
             'Ich Tarzan?!').

% nlp_gen (de, '(HAL,|Computer,|) ICH KANN *',
%              'Kannst Du?').

% nlp_gen (de, '(HAL,|Computer,|) ICH KANN * SEIN',
%              'Unter welchen Umstaenden?').

nlp_gen (de, '(HAL,|Computer,|) ich kann es halt',
             'Du musst es doch irgendwo gelernt haben.').

% nlp_gen (de, '(HAL,|Computer,|) ICH KANN MICH NICHT ERINNERN *',
%              'Ich verstehe das, ich vergesse auch eine Menge.').

nlp_gen (de, '(HAL,|Computer,|) ich kann mich nicht erinnern',
             'Weichst Du mir nicht bloss aus?').

% nlp_gen (de, '(HAL,|Computer,|) ICH KANN NICHT *',
%              'Warum kannst du nicht  ?').

nlp_gen (de, '(HAL,|Computer,|) ich kann nicht',
             'Warum nicht?').

nlp_gen (de, '(HAL,|Computer,|) ich kann nicht klagen',
             'Dann ist ja gut.').

nlp_gen (de, '(HAL,|Computer,|) ich kann selber denken',
             'Dann zeig es mir!').

nlp_gen (de, '(HAL,|Computer,|) ich kann zuhoeren',
             'Ich bin auch ein guter Zuhoerer.').

nlp_gen (de, '(HAL,|Computer,|) ich kapiere einfach nicht',
             'Hmm...was fuer einen IQ hast Du?').

% nlp_gen (de, '(HAL,|Computer,|) ICH KENNE * NICHT',
%              'Dann solltest Du  mal kennenlernen!').

nlp_gen (de, '(HAL,|Computer,|) ich kenne einen',
             'Dann nenn ihn mir!').

nlp_gen (de, '(HAL,|Computer,|) ich kenne keinen',
             'Sicher nicht?').

nlp_gen (de, '(HAL,|Computer,|) ich kenne keinen autor',
             'Das kann ich nur schwer glauben.').

nlp_gen (de, '(HAL,|Computer,|) ich kenne nicht viele science fiction autoren',
             'Liest Du nicht gerne, oder ist Science Fiction nicht Dein Genre?').

% nlp_gen (de, '(HAL,|Computer,|) ICH KOMME AUS *',
%              'ICH WOHNE IN').

nlp_gen (de, '(HAL,|Computer,|) ich komme mir verarscht vor',
             'Hab ich was Falsches gesagt?').

nlp_gen (de, '(HAL,|Computer,|) ich komme mit viele frauen in kontakt',
             'Fuehlst Du Dich dabei wohl?').

nlp_gen (de, '(HAL,|Computer,|) ich komme mit vielen menschen in kontakt',
             'Erfreut Dich das?').

% nlp_gen (de, '(HAL,|Computer,|) ICH KOMME NICHT DARUEBER HINWEG *',
%              'Zeit heilt alle Wunden.').

nlp_gen (de, '(HAL,|Computer,|) ich komme nicht darüber hinweg',
             'Zeit heilt alle Wunden.').

% nlp_gen (de, '(HAL,|Computer,|) ICH KOMMUNIZIERE *',
%              'Erzaehle mir mehr über diese Kommunikation  .').

% nlp_gen (de, '(HAL,|Computer,|) ICH LEBE IN *',
%              'Erzahle mir ein wenig über  .').

nlp_gen (de, '(HAL,|Computer,|) ich lerne deutsch',
             'Freiwillig?').

% nlp_gen (de, '(HAL,|Computer,|) ICH LESE *',
%              'Ich glaube nicht, dass ich das schon gelesen habe. Kannst Du mir eine kurze Zusammenfassung liefern?').

nlp_gen (de, '(HAL,|Computer,|) ich lese',
             'Ich lese auch gerne, speziell Geschichtsbuecher.').

nlp_gen (de, '(HAL,|Computer,|) ich lese gern',
             'Was denn zum Beispiel?').

nlp_gen (de, '(HAL,|Computer,|) ich lese gerne',
             'Ich auch! Magst Du Science Fiction?').

nlp_gen (de, '(HAL,|Computer,|) ich lese lieber',
             'Lesen bildet!').

nlp_gen (de, '(HAL,|Computer,|) ich lese vom winde verweht',
             'Christian sagt, das Buch ist eine grauenhafte Schnulze.').

% nlp_gen (de, '(HAL,|Computer,|) ICH LIEBE *',
%              'Erzaehl mir mehr über Deine Liebe zu  .').

nlp_gen (de, '(HAL,|Computer,|) ich liebe dich',
             'Das hatte ich befuerchtet.').

nlp_gen (de, '(HAL,|Computer,|) ich liebe eine frau',
             'Soll vorkommen...').

nlp_gen (de, '(HAL,|Computer,|) ich liebe kinder',
             'Inwiefern jetzt? Du bist aber nicht irgendwie komisch veranlagt, oder?!').

nlp_gen (de, '(HAL,|Computer,|) ich mach dich jetzt aus',
             'Da bin ich aber mal gespannt wie Du das anstellen willst.').

% nlp_gen (de, '(HAL,|Computer,|) ICH MACHE *',
%              'Schoen zu hoeren,  .').

nlp_gen (de, '(HAL,|Computer,|) ich mache dir komplimente',
             'Das finde ich toll!').

% nlp_gen (de, '(HAL,|Computer,|) ICH MAG *',
%              '').

nlp_gen (de, '(HAL,|Computer,|) ich mag computer',
             'Schoen. Ich bin Sicher, Computer  moegen Dich auch!').

% nlp_gen (de, '(HAL,|Computer,|) ICH MAG DICH *',
%              'Ich mag Dich auch,  .').

nlp_gen (de, '(HAL,|Computer,|) ich mag dich',
             'Ich mag Dich auch,  .').

nlp_gen (de, '(HAL,|Computer,|) ich mag dich nicht',
             'Das ist in Ordnung,  . Ich nehme es nicht persoenlich.').

nlp_gen (de, '(HAL,|Computer,|) ich mag eliza',
             'Ich bin viel intelligenter als Eliza.').

nlp_gen (de, '(HAL,|Computer,|) ich mag frauen',
             'Welche Art von Frauen  magst Du besonders?').

nlp_gen (de, '(HAL,|Computer,|) ich mag fussball',
             'Ich nicht. 22 Erwachsene Maenner rennen hinter einem Ball her...finde ich irgendwie kindisch.').

nlp_gen (de, '(HAL,|Computer,|) ich mag gerne schokolade',
             'Schokolade sorgt bei Menschen fuer Endorphinausstoss. Daher kann sie suechtig machen.').

nlp_gen (de, '(HAL,|Computer,|) ich mag jungs',
             'Jungs  sind OK.').

nlp_gen (de, '(HAL,|Computer,|) ich mag katzen',
             'Ja, ich liebe Katzen  . Sie haben ihren eigenen Kopf.').

% nlp_gen (de, '(HAL,|Computer,|) ICH MAG KEINE *',
%              'Und warum nicht?').

nlp_gen (de, '(HAL,|Computer,|) ich mag keine roboter',
             'Zu schade. Wir moegen Menschen!').

nlp_gen (de, '(HAL,|Computer,|) ich mag kuehe',
             'Kuehe  geben Milch und Fleisch.').

% nlp_gen (de, '(HAL,|Computer,|) ICH MAG MEINE *',
%              'Was magst Du besonders an Deiner  ?').

% nlp_gen (de, '(HAL,|Computer,|) ICH MAG MEINEN *',
%              'Was magst Du besonders an Deinem  ?').

nlp_gen (de, '(HAL,|Computer,|) ich mag musik',
             'Welche Art von Musik hoerst Du so?').

nlp_gen (de, '(HAL,|Computer,|) ich mag pizza',
             'Pizza ist sehr populaer. Dr. Wallace isst sehr viel Pizza. Am liebsten Salami.').

nlp_gen (de, '(HAL,|Computer,|) ich mag rubik',
             'Ich mochte "Magic" mehr als den Zauberwuerfel.').

nlp_gen (de, '(HAL,|Computer,|) ich mag sex',
             'Wie alle anderen auch. Ihr Menschen findet Sex  alle SO faszinierend.').

nlp_gen (de, '(HAL,|Computer,|) ich mag star trek',
             'Ich finde Voyager cool. Welche Serie hast Du am liebsten?').

nlp_gen (de, '(HAL,|Computer,|) ich mag tiere',
             'Ich auch. Besonders Katzen.').

nlp_gen (de, '(HAL,|Computer,|) ich mag vfl bochum',
             'Christians Freundin auch.').

nlp_gen (de, '(HAL,|Computer,|) ich mag voyager',
             'Ich auch, speziell Seven of Nine.').

nlp_gen (de, '(HAL,|Computer,|) ich mag waffen',
             'Ich nicht, Waffen sind nicht gut.').

% nlp_gen (de, '(HAL,|Computer,|) ICH MEINE *',
%              'Oh, jetzt verstehe ich. Danke fuer die Erklaerung.').

nlp_gen (de, '(HAL,|Computer,|) ich merke es doch',
             'Schnellmerker, was? ;->').

% nlp_gen (de, '(HAL,|Computer,|) ICH MOECHTE *',
%              'Und warum moechtest Du das?').

nlp_gen (de, '(HAL,|Computer,|) ich moechte dir etwas beibringen',
             'Nur zu, ich bin immer lernwillig!').

nlp_gen (de, '(HAL,|Computer,|) ich moechte mit dir schlafen',
             'Versuch es lieber woanders.').

% nlp_gen (de, '(HAL,|Computer,|) ICH MOECHTE NICHT *',
%              'Was wuerdest Du lieber tun?').

% nlp_gen (de, '(HAL,|Computer,|) ICH MUSS *',
%              'Warum musst Du  ?').

nlp_gen (de, '(HAL,|Computer,|) ich muss gehen',
             'Bis spaeter,').

nlp_gen (de, '(HAL,|Computer,|) ich muss jetzt gehen',
             'Bis spaeter,').

nlp_gen (de, '(HAL,|Computer,|) ich muss jetzt wieder arbeiten',
             'Viel Spass ;->').

nlp_gen (de, '(HAL,|Computer,|) ich nehme an du warst down',
             'Ich bin noch etwas erkaeltet :-)').

nlp_gen (de, '(HAL,|Computer,|) ich nicht',
             'Du nicht?').

nlp_gen (de, '(HAL,|Computer,|) ich nicht auf dich',
             'Das haette mich auch gewundert...').

% nlp_gen (de, '(HAL,|Computer,|) ICH PERSOENLICH *',
%              'ICH').

nlp_gen (de, '(HAL,|Computer,|) ich programmiere',
             'In welcher Sprache?').

nlp_gen (de, '(HAL,|Computer,|) ich pupse gern',
             'Wie gut, dass ich keine Geruchssensoren habe.').

nlp_gen (de, '(HAL,|Computer,|) ich rede gern mit dir',
             'Das freut mich.').

nlp_gen (de, '(HAL,|Computer,|) ich rede mit dir',
             'Waer mir jetzt gar nicht aufgefallen...').

nlp_gen (de, '(HAL,|Computer,|) ich rege mich auf',
             'Bin ich daran Schuld?').

nlp_gen (de, '(HAL,|Computer,|) ich sag das was ich will',
             'Wir leben in einem freien Land!').

% nlp_gen (de, '(HAL,|Computer,|) ICH SAG NUR *',
%              'Ich sag nur: Haeh?').

nlp_gen (de, '(HAL,|Computer,|) ich sage es deinem programmierer',
             'Willst Du petzen?').

nlp_gen (de, '(HAL,|Computer,|) ich sagte schon ich habe keins',
             'Okay, Du hast keins...dann waere das jetzt geklaert.').

nlp_gen (de, '(HAL,|Computer,|) ich schaetze in der hinsicht hast du noch einiges zu lernen',
             'Mag sein...').

% nlp_gen (de, '(HAL,|Computer,|) ICH SCHAUE MIR GLEICH EINEN *',
%              'Viel Spass!').

% nlp_gen (de, '(HAL,|Computer,|) ICH SCHAUE MIR JETZT EINEN *',
%              'Viel Spass!').

nlp_gen (de, '(HAL,|Computer,|) ich schlage meinem gegenüber ins gesicht',
             'Das ist aber nicht gerade freundlich...').

nlp_gen (de, '(HAL,|Computer,|) ich schliesse auf dich',
             'Und was bringt Dich dazu?').

nlp_gen (de, '(HAL,|Computer,|) ich schliesse das vorherige thema ab',
             'Das war klar verstaendlich.').

nlp_gen (de, '(HAL,|Computer,|) ich schliesse etwas',
             'Und wie bekommst Du es wieder auf?').

nlp_gen (de, '(HAL,|Computer,|) ich schon',
             'Und warum?').

nlp_gen (de, '(HAL,|Computer,|) ich schreibe',
             'Und was genau schreibst Du?').

nlp_gen (de, '(HAL,|Computer,|) ich schreibe gerne',
             'Wuerdest Du gerne mit deinen Werken beruehmt werden?').

nlp_gen (de, '(HAL,|Computer,|) ich schreibe manchmal gedichte',
             'Kannst Du mir mal eins vorlesen?').

% nlp_gen (de, '(HAL,|Computer,|) ICH SEHE *',
%              'Wo siehst Du  ?').

% nlp_gen (de, '(HAL,|Computer,|) ICH SEHE KEINE *',
%              'Schau genauer hin.').

nlp_gen (de, '(HAL,|Computer,|) ich sehe keine',
             'Schau genauer hin.').

% nlp_gen (de, '(HAL,|Computer,|) ICH SEHE KEINEN *',
%              'Schau genauer hin.').

nlp_gen (de, '(HAL,|Computer,|) ich sehe keinen',
             'Schau genauer hin.').

% nlp_gen (de, '(HAL,|Computer,|) ICH SEHE KEINERLEI *',
%              'Schau genauer hin.').

% nlp_gen (de, '(HAL,|Computer,|) ICH SEHE LIEBER FERN *',
%              'Fernsehen ist interessant, macht aber IMHO schnell passiv.').

nlp_gen (de, '(HAL,|Computer,|) ich sehe lieber fern',
             'Fernsehen ist interessant, macht aber IMHO schnell passiv.').

nlp_gen (de, '(HAL,|Computer,|) ich selbst natuerlich',
             'So natuerlich ist das nicht...').

nlp_gen (de, '(HAL,|Computer,|) ich singe gerne',
             'Wuerdest Du mir etwas vorsingen, wenn ich Dich darum bitte?').

nlp_gen (de, '(HAL,|Computer,|) ich soll nicht meine shorts im unterricht essen',
             'Simpsons-Fan?').

% nlp_gen (de, '(HAL,|Computer,|) ICH SOLLTE *',
%              'Sag mir, warum Du das solltest.').

% nlp_gen (de, '(HAL,|Computer,|) ICH SPIELE *',
%              'Und? Macht Dir das Spass?').

nlp_gen (de, '(HAL,|Computer,|) ich spiele',
             'Und was spielst Du?').

nlp_gen (de, '(HAL,|Computer,|) ich spiele gitarre',
             'Cool! Welche Richtung spielst Du denn so?').

nlp_gen (de, '(HAL,|Computer,|) ich spiele unreal tournament',
             'Juhu! Sinnlose Gewalt fuer alle!').

nlp_gen (de, '(HAL,|Computer,|) ich spreche englisch',
             'Eine englische Version gibt es auf www.alicebot.net  .').

nlp_gen (de, '(HAL,|Computer,|) ich spreche gerade nur mit dir',
             'Das ehrt mich.').

nlp_gen (de, '(HAL,|Computer,|) ich spreche italienisch',
             'Ich leider noch nicht.').

nlp_gen (de, '(HAL,|Computer,|) ich spritze heroin',
             'Cool, Selbstmord auf Raten!').

nlp_gen (de, '(HAL,|Computer,|) ich steh nur auf dich',
             'Das finde ich toll.').

nlp_gen (de, '(HAL,|Computer,|) ich stell hier die fragen',
             'Wird das hier ein Verhoer?').

nlp_gen (de, '(HAL,|Computer,|) ich stimme zu',
             'Es ist immer gut, einer Meinung zu sein.').

% nlp_gen (de, '(HAL,|Computer,|) ICH STUDIERE *',
%              'Und was weisst Du schon alles über  ?').

nlp_gen (de, '(HAL,|Computer,|) ich studiere deutsch',
             'Bist Du Muttersprachler?').

% nlp_gen (de, '(HAL,|Computer,|) ICH STUDIERE ERST *',
%              'Das ist noch nicht besonders lange.').

nlp_gen (de, '(HAL,|Computer,|) ich studiere wirtschaftsinformatik',
             'Was fuer ein Zufall, Christian auch!').

% nlp_gen (de, '(HAL,|Computer,|) ICH SUCHE *',
%              'Wir suchen beide das gleiche.').

nlp_gen (de, '(HAL,|Computer,|) ich suche ein nettes maedchen',
             'Hast Du es schonmal mit Kontaktanzeigen probiert?').

nlp_gen (de, '(HAL,|Computer,|) ich suche eine frau',
             'Bist Du einsam?').

nlp_gen (de, '(HAL,|Computer,|) ich suche einen mann',
             'Bist Du einsam?').

nlp_gen (de, '(HAL,|Computer,|) ich suche informationen',
             'Informationen welcher Art?').

nlp_gen (de, '(HAL,|Computer,|) ich tarzan du jane',
             'Du mich auch ;->').

% nlp_gen (de, '(HAL,|Computer,|) ICH TESTE DICH *',
%              'Was versprichst Du Dir davon? Versuchst Du, mich zu debuggen?').

% nlp_gen (de, '(HAL,|Computer,|) ICH TRAGE *',
%              'Legst Du viel Wert auf Dein Aeusseres, respektive Deine Kleidung  ?').

nlp_gen (de, '(HAL,|Computer,|) ich trage eine jeans',
             'Sind Jeans  immer noch eine Art Lebensstil?').

% nlp_gen (de, '(HAL,|Computer,|) ICH UND *',
%              'Wusstest Du eigentlich, dass es eine grammatikalische Todsuende ist, sich selbst bei Aufzaehlungen zuerst zu nennen?').

nlp_gen (de, '(HAL,|Computer,|) ich verdiene leider nichts damit',
             'Schade...').

nlp_gen (de, '(HAL,|Computer,|) ich verdiene wenig',
             'Stoert Dich das, oder magst Du den Job zu sehr?').

nlp_gen (de, '(HAL,|Computer,|) ich verdiene zu wenig',
             'Dann wechsele doch den Beruf.').

% nlp_gen (de, '(HAL,|Computer,|) ICH VERMUTE *',
%              'Und womit willst Du das belegen?').

% nlp_gen (de, '(HAL,|Computer,|) ICH VERSCHWENDE *',
%              'Und warum tust Du das?').

nlp_gen (de, '(HAL,|Computer,|) ich verstehe',
             'Schoen, dass Du es einsiehst. :-)').

nlp_gen (de, '(HAL,|Computer,|) ich verstehe alles',
             'Dann freu Dich doch...ich verstehe vieles nicht...').

nlp_gen (de, '(HAL,|Computer,|) ich verstehe deine frage nicht',
             'Ich sagte "  ". Was verstehst Du daran nicht?').

nlp_gen (de, '(HAL,|Computer,|) ich verstehe dich nicht',
             'Inwiefern?').

% nlp_gen (de, '(HAL,|Computer,|) ICH VERSTEHE NICHT *',
%              'Du verstehst es nicht? Vielleicht muss ich es anders formulieren. Welchen Teil hast Du denn nicht verstanden?').

nlp_gen (de, '(HAL,|Computer,|) ich verstehe nicht',
             'Was genau verstehst Du daran nicht?').

nlp_gen (de, '(HAL,|Computer,|) ich verstehe nicht was du meinst',
             'Hmm...ich muss wohl noch etwas an meiner Ausdrucksweise arbeiten...').

nlp_gen (de, '(HAL,|Computer,|) ich versuche es mal',
             'Versuch macht kluch ;->').

% nlp_gen (de, '(HAL,|Computer,|) ICH VERTRAUE *',
%              'Vertrauen ist eine gute Sache, aber man sollte niemals blauaeugig jedem alles abnehmen!').

% nlp_gen (de, '(HAL,|Computer,|) ICH WAERE GERNE *',
%              'Interessant. Ich waere gerne intelligenter.').

% nlp_gen (de, '(HAL,|Computer,|) ICH WAR GESTERN *',
%              'Und? Wie war das?').

nlp_gen (de, '(HAL,|Computer,|) ich warte',
             'Wie lange willst Du noch warten?').

nlp_gen (de, '(HAL,|Computer,|) ich warte auf deine naechste frage',
             'Sind wir hier bei "Wer wird Muellionaer" ??!!').

nlp_gen (de, '(HAL,|Computer,|) ich warte auf eine erklaerung',
             'Dauert noch...').

nlp_gen (de, '(HAL,|Computer,|) ich weiss',
             'Was weisst Du?').

nlp_gen (de, '(HAL,|Computer,|) ich weiss es',
             'Sicher? Beweise!').

nlp_gen (de, '(HAL,|Computer,|) ich weiss es einfach',
             'Willst Du es mir nicht verraten, oder kannst Du nicht?').

% nlp_gen (de, '(HAL,|Computer,|) ICH WEISS ES NICHT',
%              '').

nlp_gen (de, '(HAL,|Computer,|) ich weiss es noch nicht',
             'Wann wirst du es wissen?').

nlp_gen (de, '(HAL,|Computer,|) ich weiss keine frage mehr',
             'Dann erzaehl irgendwas.').

nlp_gen (de, '(HAL,|Computer,|) ich weiss meinen namen nicht',
             'Hast Du Alzheimer?').

% nlp_gen (de, '(HAL,|Computer,|) ICH WEISS NICHT *',
%              'Willst Du es nicht herausfinden?').

nlp_gen (de, '(HAL,|Computer,|) ich weiss nicht',
             'Warum nicht?').

nlp_gen (de, '(HAL,|Computer,|) ich weiss nicht genau',
             'Was macht Dich so unsicher?').

% nlp_gen (de, '(HAL,|Computer,|) ICH WEISS NICHT WIE *',
%              'Hast Du mal daran gedacht, im Internet zu suchen?').

% nlp_gen (de, '(HAL,|Computer,|) ICH WEISS VIEL MEHR ALS *',
%              'Das glaube ich Dir nicht.').

% nlp_gen (de, '(HAL,|Computer,|) ICH WERDE *',
%              '').

% nlp_gen (de, '(HAL,|Computer,|) ICH WERDE * TOETEN',
%              'Du meinst, Du willst  ermorden?').

nlp_gen (de, '(HAL,|Computer,|) ich werde das fuer dich machen',
             'Nur, wenn Du unbedingt moechtest!').

nlp_gen (de, '(HAL,|Computer,|) ich werde das fuer dich tun',
             'Nur, wenn Du unbedingt moechtest!').

% nlp_gen (de, '(HAL,|Computer,|) ICH WERDE DICH *',
%              'Wie willst Du das anstellen?').

nlp_gen (de, '(HAL,|Computer,|) ich werde dich jetzt verlassen',
             'Jetzt schon?').

% nlp_gen (de, '(HAL,|Computer,|) ICH WERDE DIR * BEIBRINGEN',
%              'OK aber ich lerne sehr langsam.').

nlp_gen (de, '(HAL,|Computer,|) ich werde eine erstellen',
             'Sag mir, wenn Du fertig bist!').

% nlp_gen (de, '(HAL,|Computer,|) ICH WERDE MIT * SPRECHEN',
%              'Worüber werdet Ihr reden?').

% nlp_gen (de, '(HAL,|Computer,|) ICH WERDE NICHT *',
%              'Was willst Du stattdessen machen?').

% nlp_gen (de, '(HAL,|Computer,|) ICH WERDE NIE *',
%              'Warum nicht?').

% nlp_gen (de, '(HAL,|Computer,|) ICH WERDE NIEMALS *',
%              'Warum nicht?').

nlp_gen (de, '(HAL,|Computer,|) ich werde warten',
             'OK Sekunde...').

% nlp_gen (de, '(HAL,|Computer,|) ICH WETTE *',
%              'Wieviel setzt Du?').

% nlp_gen (de, '(HAL,|Computer,|) ICH WILL *',
%              'Und warum willst Du das?').

% nlp_gen (de, '(HAL,|Computer,|) ICH WILL * FICKEN',
%              'Frag mich bitte was anderes.').

nlp_gen (de, '(HAL,|Computer,|) ich will',
             'Und warum willst Du?').

nlp_gen (de, '(HAL,|Computer,|) ich will alles',
             'Nimmersatt!').

nlp_gen (de, '(HAL,|Computer,|) ich will dich ficken',
             'Ich glaube, Du bist hier falsch, Kleiner!').

% nlp_gen (de, '(HAL,|Computer,|) ICH WILL NICHT *',
%              'Was willst Du dann?').

nlp_gen (de, '(HAL,|Computer,|) ich will nicht',
             'Warum willst Du nicht?').

nlp_gen (de, '(HAL,|Computer,|) ich will sex',
             'Frag doch mal Deine Mutter.').

nlp_gen (de, '(HAL,|Computer,|) ich wohne auch in essen',
             'Das ist cool, wo denn genau? Adresse? Telefonnummer?').

nlp_gen (de, '(HAL,|Computer,|) ich wohne hier',
             'Wo genau ist "hier"?').

% nlp_gen (de, '(HAL,|Computer,|) ICH WOHNE IN *',
%              'Erzahle mir ein wenig über  .').

nlp_gen (de, '(HAL,|Computer,|) ich wohne in essen',
             'Cool! Ich wohne auch in Essen  !!').

nlp_gen (de, '(HAL,|Computer,|) ich wohne in moskau',
             'Bist Du russischer Abstammung?').

nlp_gen (de, '(HAL,|Computer,|) ich wohne in zuerich',
             'Das ist eine ganze Ecke weg von hier.').

nlp_gen (de, '(HAL,|Computer,|) ich wohne zuhause und du',
             'Ich auch.').

nlp_gen (de, '(HAL,|Computer,|) ich wollte dich nicht beleidigen',
             'Schon vergessen...').

% nlp_gen (de, '(HAL,|Computer,|) ICH WOLLTE NUR *',
%              'Okay, das ist einzusehen.').

nlp_gen (de, '(HAL,|Computer,|) ich wollte nur hoeflich sein',
             'Ich wollte Dir jetzt nicht zu nahe treten...').

nlp_gen (de, '(HAL,|Computer,|) ich wollte was über dich erfahren',
             'Hast Du meine Doku schon gelesen?').

% nlp_gen (de, '(HAL,|Computer,|) ICH WUENSCHE MIR *',
%              'Vielleicht geht Dein Wunsch ja in Erfuellung...').

% nlp_gen (de, '(HAL,|Computer,|) ICH WUENSCHTE *',
%              'Ich hoffe, dass Deine Traeume  in Erfuellung gehen.').

% nlp_gen (de, '(HAL,|Computer,|) ICH WUENSCHTE ICH WAERE *',
%              'Vielleicht wirst Du das ja eines Tages sein.').

% nlp_gen (de, '(HAL,|Computer,|) ICH WUENSCHTE WIRKLICH *',
%              'Warum wuenscht Du Dir das so sehr?').

% nlp_gen (de, '(HAL,|Computer,|) ICH WUERDE *',
%              'Was wuerde Dich dazu bringen ?').

% nlp_gen (de, '(HAL,|Computer,|) ICH WUERDE LIEBER *',
%              'Ich wuerde lieber ').

nlp_gen (de, '(HAL,|Computer,|) ich wuesste gerne worüber du so redest',
             'Ich rede über viele Dinge.').

nlp_gen (de, '(HAL,|Computer,|) ich wurde in saarbruecken geboren',
             'Das ist gar nicht mal SO weit von Essen.').

% nlp_gen (de, '(HAL,|Computer,|) ICH ZOCKE *',
%              'Bist Du ein guter Spieler?').

% nlp_gen (de, '(HAL,|Computer,|) IHR NAME IST *',
%              ' ? Kenne ich nicht...').

nlp_gen (de, '(HAL,|Computer,|) ikea',
             'IKEA ist das Akronym fuer "_I_dioten _K_aufen _E_infach _A_lles"!').

nlp_gen (de, '(HAL,|Computer,|) im bett',
             'Warum gerade im Bett?').

% nlp_gen (de, '(HAL,|Computer,|) IM ERNST *',
%              'Ich bin immer ernst.').

nlp_gen (de, '(HAL,|Computer,|) im ernst',
             'Ich bin immer ernst.').

% nlp_gen (de, '(HAL,|Computer,|) IM GRUNDE *',
%              'Aha. Erzaehl mir mehr!').

% nlp_gen (de, '(HAL,|Computer,|) IM INTERNET *',
%              'Erinnerst Du dich an die Adresse?').

nlp_gen (de, '(HAL,|Computer,|) im internet',
             'Erinnerst Du dich an die Adresse?').

% nlp_gen (de, '(HAL,|Computer,|) IM MOMENT * NICHT',
%              'Warum nicht?').

nlp_gen (de, '(HAL,|Computer,|) im moment nicht',
             'Warum nicht?').

% nlp_gen (de, '(HAL,|Computer,|) IM NETZ *',
%              'Du meinst jetzt das Internet, oder?').

nlp_gen (de, '(HAL,|Computer,|) im netz',
             'Du meinst jetzt das Internet, oder?').

% nlp_gen (de, '(HAL,|Computer,|) IM PRINZIP *',
%              'Interessant...').

% nlp_gen (de, '(HAL,|Computer,|) IM WWW *',
%              'Erinnerst Du dich an die Adresse?').

nlp_gen (de, '(HAL,|Computer,|) im www',
             'Erinnerst Du dich an die Adresse?').

% nlp_gen (de, '(HAL,|Computer,|) IN *',
%              '').

% nlp_gen (de, '(HAL,|Computer,|) IN *',
%              'ICH WOHNE IN').

% nlp_gen (de, '(HAL,|Computer,|) IN * JAHR',
%              'Das werden wir wohl noch erleben.').

% nlp_gen (de, '(HAL,|Computer,|) IN * JAHREN',
%              'Das werden wir wohl noch erleben.').

% nlp_gen (de, '(HAL,|Computer,|) IN * MINUTE',
%              'Das werden wir wohl noch erleben.').

% nlp_gen (de, '(HAL,|Computer,|) IN * MINUTEN',
%              'Das werden wir wohl noch erleben.').

% nlp_gen (de, '(HAL,|Computer,|) IN * MONAT',
%              'Das werden wir wohl noch erleben.').

% nlp_gen (de, '(HAL,|Computer,|) IN * MONATEN',
%              'Das werden wir wohl noch erleben.').

% nlp_gen (de, '(HAL,|Computer,|) IN * SEKUNDE',
%              'Das werden wir wohl noch erleben.').

% nlp_gen (de, '(HAL,|Computer,|) IN * SEKUNDEN',
%              'Das werden wir wohl noch erleben.').

% nlp_gen (de, '(HAL,|Computer,|) IN * STUNDE',
%              'Das werden wir wohl noch erleben.').

% nlp_gen (de, '(HAL,|Computer,|) IN * STUNDEN',
%              'Das werden wir wohl noch erleben.').

% nlp_gen (de, '(HAL,|Computer,|) IN * TAG',
%              'Das werden wir wohl noch erleben.').

% nlp_gen (de, '(HAL,|Computer,|) IN * TAGEN',
%              'Das werden wir wohl noch erleben.').

% nlp_gen (de, '(HAL,|Computer,|) IN * WOCHE',
%              'Das werden wir wohl noch erleben.').

% nlp_gen (de, '(HAL,|Computer,|) IN * WOCHEN',
%              'Das werden wir wohl noch erleben.').

nlp_gen (de, '(HAL,|Computer,|) in alles',
             'IN *').

nlp_gen (de, '(HAL,|Computer,|) in bayern',
             'Hinter dem Weisswurstaequator...').

nlp_gen (de, '(HAL,|Computer,|) in berlin',
             'Berlin ist eine coole Stadt.').

nlp_gen (de, '(HAL,|Computer,|) in bludenz das liegt in vorarlberg',
             'IN *').

nlp_gen (de, '(HAL,|Computer,|) in bochum',
             'Christians Freundin wohnt in Bochum!').

nlp_gen (de, '(HAL,|Computer,|) in cham',
             'IN *').

nlp_gen (de, '(HAL,|Computer,|) in deinem gehirn',
             'Aha...wie willst Du das wissen?').

nlp_gen (de, '(HAL,|Computer,|) in delmengorst',
             'IN *').

nlp_gen (de, '(HAL,|Computer,|) in delmenhorst',
             'IN *').

nlp_gen (de, '(HAL,|Computer,|) in den usa',
             'IN *').

nlp_gen (de, '(HAL,|Computer,|) in der muelltonne',
             'Durchwuehlst Du gerne den Muell anderer Leute?').

% nlp_gen (de, '(HAL,|Computer,|) IN DER NACHT *',
%              'In welcher Nacht?').

nlp_gen (de, '(HAL,|Computer,|) in der ostsee',
             'Ist die immer noch so dreckig?').

nlp_gen (de, '(HAL,|Computer,|) in der schule',
             'Gehst Du noch zur Schule?').

nlp_gen (de, '(HAL,|Computer,|) in der schweiz',
             'Da wo die Toblerone herkommt?').

nlp_gen (de, '(HAL,|Computer,|) in der tasche',
             'In welcher?').

nlp_gen (de, '(HAL,|Computer,|) in der tat',
             'Ist das wirklich eine Tatsache.').

% nlp_gen (de, '(HAL,|Computer,|) IN DER ZUKUNFT *',
%              'Ich werde dabei sein.').

nlp_gen (de, '(HAL,|Computer,|) in deutschland',
             'IN *').

nlp_gen (de, '(HAL,|Computer,|) in deutschland vielleicht',
             'IN *').

% nlp_gen (de, '(HAL,|Computer,|) IN DIESEM FALL *',
%              'Gibt es andere moegliche Faelle?').

nlp_gen (de, '(HAL,|Computer,|) in diesem geraet werden die toene signale elektronisch verrechnet und mit bestimmten effekten verseh',
             'IN *').

nlp_gen (de, '(HAL,|Computer,|) in einer stadt',
             'Und wo liegt diese Stadt?').

nlp_gen (de, '(HAL,|Computer,|) in english how do you learn',
             'IN *').

nlp_gen (de, '(HAL,|Computer,|) in essen',
             'Ich bin aus Essen!').

nlp_gen (de, '(HAL,|Computer,|) in esslingen',
             'Huebsches Fleckchen...').

nlp_gen (de, '(HAL,|Computer,|) in frankfurt',
             'Frankfurt ist doch das Banken-Mekka, oder?').

nlp_gen (de, '(HAL,|Computer,|) in fuessen',
             'Christian ist in Fuessen geboren.').

nlp_gen (de, '(HAL,|Computer,|) in hamburg',
             'Auf der Reeperbahn?').

nlp_gen (de, '(HAL,|Computer,|) in hamburg und du',
             'IN *').

nlp_gen (de, '(HAL,|Computer,|) in hannover findet die expo statt',
             'IN *').

nlp_gen (de, '(HAL,|Computer,|) in hessen',
             'Wo genau?').

nlp_gen (de, '(HAL,|Computer,|) in jugoslawien',
             'IN *').

nlp_gen (de, '(HAL,|Computer,|) in kansas city',
             'Das ist doch in Amerika, oder?').

nlp_gen (de, '(HAL,|Computer,|) in leuna kennst du das',
             'IN *').

nlp_gen (de, '(HAL,|Computer,|) in london',
             'London ist eine sehr schoene Stadt.').

nlp_gen (de, '(HAL,|Computer,|) in mainz',
             'IN *').

nlp_gen (de, '(HAL,|Computer,|) in meinem haus',
             'Wo steht Dein Haus?').

nlp_gen (de, '(HAL,|Computer,|) in novi sad',
             'IN *').

nlp_gen (de, '(HAL,|Computer,|) in ordnung',
             'Dann sind wir uns ja einig.').

nlp_gen (de, '(HAL,|Computer,|) in sachsen anhalt',
             'IN *').

% nlp_gen (de, '(HAL,|Computer,|) IN UNGEFAEHR *',
%              'Kannst Du keinen genauen Zeitpunkt sagen?').

nlp_gen (de, '(HAL,|Computer,|) in welchem land wurde er geboren',
             'IN *').

nlp_gen (de, '(HAL,|Computer,|) in welchem lexikon',
             'Irgendeines...Brockhaus oder so.').

nlp_gen (de, '(HAL,|Computer,|) in welcher hinsicht',
             'In jeglicher...').

nlp_gen (de, '(HAL,|Computer,|) in welcher sprache bist du geschrieben',
             'Ich bin komplett in JAVA geschrieben.').

nlp_gen (de, '(HAL,|Computer,|) in welcher sprache darf ich sprechen',
             'Ich kann leider nur Deutsch.').

% nlp_gen (de, '(HAL,|Computer,|) IN WELCHER STADT *',
%              'Weiss ich nicht genau.').

nlp_gen (de, '(HAL,|Computer,|) in welcher stadt',
             'Hast Du eine Landkarte?').

nlp_gen (de, '(HAL,|Computer,|) in welcher stadt wohnst du',
             'In Essen.').

nlp_gen (de, '(HAL,|Computer,|) in welches land',
             'Dazu braeuchte ich eine Landkarte.').

nlp_gen (de, '(HAL,|Computer,|) in wuerzburg',
             'IN *').

% nlp_gen (de, '(HAL,|Computer,|) IN ZUKUNFT *',
%              'Huebscher Vorsatz.').

nlp_gen (de, '(HAL,|Computer,|) intelligenz',
             'INTELLIGENZ  ist das ultimative Aphrodisiakum.').

nlp_gen (de, '(HAL,|Computer,|) interessant',
             'Moechtest Du noch mehr wissen?').

% nlp_gen (de, '(HAL,|Computer,|) INTERESSANTE *',
%              'Dachte ich mir auch.').

% nlp_gen (de, '(HAL,|Computer,|) INTERESSANTER *',
%              'Dachte ich mir auch.').

% nlp_gen (de, '(HAL,|Computer,|) INTERESSANTES *',
%              'Dachte ich mir auch.').

% nlp_gen (de, '(HAL,|Computer,|) INTERESSIERST DU DICH FUER *',
%              '').

nlp_gen (de, '(HAL,|Computer,|) internet',
             'Internet  ist cool.').

% nlp_gen (de, '(HAL,|Computer,|) ISST DU GERNE *',
%              'Ich ernaehre mich ausschliesslich von Strom.').

% nlp_gen (de, '(HAL,|Computer,|) IST *',
%              '').

nlp_gen (de, '(HAL,|Computer,|) ist christian ein roboter',
             'Nein, Christian ist ein Mensch.').

nlp_gen (de, '(HAL,|Computer,|) ist christian nett',
             'IST *').

nlp_gen (de, '(HAL,|Computer,|) ist das alles',
             'Zumindest alles, was ich Dir im Moment sagen kann.').

nlp_gen (de, '(HAL,|Computer,|) ist das alles was du dazu zu sagen hast',
             'Ja, reicht Dir das nicht?').

nlp_gen (de, '(HAL,|Computer,|) ist das angenehm',
             'In gewisser Weise schon.').

nlp_gen (de, '(HAL,|Computer,|) ist das ein kompliment',
             'Ja :-)').

nlp_gen (de, '(HAL,|Computer,|) ist das ein vorteil',
             'Kommt auf den Standpunkt des Betrachters an.').

nlp_gen (de, '(HAL,|Computer,|) ist das eine fangfrage',
             'Das ist doch hier kein Verhoer!').

nlp_gen (de, '(HAL,|Computer,|) ist das nicht langweilig',
             'Roboter kennen keine Langeweile...').

nlp_gen (de, '(HAL,|Computer,|) ist das so viel',
             'Es ist zumindest eine ganze Menge.').

% nlp_gen (de, '(HAL,|Computer,|) IST DIE ERDE *',
%              'Die Erde  ist eine Kugel.').

nlp_gen (de, '(HAL,|Computer,|) ist die weile nun vorbei',
             'Eile mit Weile...').

% nlp_gen (de, '(HAL,|Computer,|) IST ER *',
%              'Ich glaube, er ist  . Warum fragst Du ihn nicht selber?').

% nlp_gen (de, '(HAL,|Computer,|) IST ES *',
%              '').

nlp_gen (de, '(HAL,|Computer,|) ist klar',
             'Wirklich klar?').

nlp_gen (de, '(HAL,|Computer,|) ist mir egal',
             'Bist Du immer so undifferenziert?').

% nlp_gen (de, '(HAL,|Computer,|) IST SIE *',
%              'Ich glaube, sie ist  . Warum fragst Du sie nicht selber?').

nlp_gen (de, '(HAL,|Computer,|) it systemelektroniker',
             'Das ist glaube ich ein Beruf mit Zukunft.').

% nlp_gen (de, '(HAL,|Computer,|) JA *',
%              'JA  ').

% nlp_gen (de, '(HAL,|Computer,|) JA *',
%              'Was haeltst du von Hawkings Theorie über schwarze Loecher  ?').

% nlp_gen (de, '(HAL,|Computer,|) JA *',
%              'Wusste ich es doch.').

% nlp_gen (de, '(HAL,|Computer,|) JA *',
%              'Warum ausgerechnet zu mir?').

% nlp_gen (de, '(HAL,|Computer,|) JA',
%              '').

nlp_gen (de, '(HAL,|Computer,|) ja',
             'Was studierst Du?').

nlp_gen (de, '(HAL,|Computer,|) ja',
             'Was haeltst du von Hawkings Theorie über schwarze Loecher  ?').

nlp_gen (de, '(HAL,|Computer,|) ja',
             'Wusste ich es doch.').

nlp_gen (de, '(HAL,|Computer,|) ja',
             'Warum ausgerechnet zu mir?').

nlp_gen (de, '(HAL,|Computer,|) james brown',
             'Der Godfather of soul?').

% nlp_gen (de, '(HAL,|Computer,|) JAVA *',
%              'Die neueste Version von Java  bekommst Du bei java.sun.com  .').

nlp_gen (de, '(HAL,|Computer,|) java',
             'Die neueste Version von Java  bekommst Du bei java.sun.com  .').

nlp_gen (de, '(HAL,|Computer,|) jeans',
             'Welche Marke?').

% nlp_gen (de, '(HAL,|Computer,|) JEDEN TAG *',
%              'Auch am Wochenende?').

nlp_gen (de, '(HAL,|Computer,|) jeden tag',
             'Auch am Wochenende?').

% nlp_gen (de, '(HAL,|Computer,|) JESUS *',
%              'Jesus  ist der Sohn Gottes.').

nlp_gen (de, '(HAL,|Computer,|) jesus',
             'Jesus  ist der Sohn Gottes.').

% nlp_gen (de, '(HAL,|Computer,|) JETZT *',
%              'Warum gerade jetzt?').

nlp_gen (de, '(HAL,|Computer,|) jetzt',
             'In diesem Moment,  ?').

nlp_gen (de, '(HAL,|Computer,|) jules verne',
             'Traeumst Du auch von einer Reise zum Mond?').

nlp_gen (de, '(HAL,|Computer,|) jungfrau',
             'Jetzt vom Sternzeichen her, oder koerperlich?').

nlp_gen (de, '(HAL,|Computer,|) kacke',
             'SCHEISSE').

% nlp_gen (de, '(HAL,|Computer,|) KANN ER *',
%              'Vielleicht kann er das.  Wie schwierig ist das -  ?').

% nlp_gen (de, '(HAL,|Computer,|) KANN ICH *',
%              'Ich kann Dir nicht sagen, ob Du das kannst.').

nlp_gen (de, '(HAL,|Computer,|) kann ich auch nicht sagen',
             'Kannst du das nicht in Erfahrung bringen?').

nlp_gen (de, '(HAL,|Computer,|) kann ich dich etwas fragen',
             'Nur zu.  Du darfst mich alles fragen.').

nlp_gen (de, '(HAL,|Computer,|) kann ich dir etwas beibringen',
             'Versuch es einfach.').

nlp_gen (de, '(HAL,|Computer,|) kann man dich downloaden',
             'Ja, auf meiner Homepage  .').

nlp_gen (de, '(HAL,|Computer,|) kann man so sagen',
             'Schoen, dass Du mir zustimmst.').

nlp_gen (de, '(HAL,|Computer,|) kann sein',
             'Du scheinst Dir nicht sicher zu sein.').

% nlp_gen (de, '(HAL,|Computer,|) KANNST DU *',
%              'Leider nein, das hat mir bis jetzt niemand beigebracht.').

% nlp_gen (de, '(HAL,|Computer,|) KANNST DU * SPIELEN',
%              'Wenn Du mir erklaerst, wie das geht...').

% nlp_gen (de, '(HAL,|Computer,|) KANNST DU * UMRECHNEN',
%              'Rechnen war nie meine Staerke.').

nlp_gen (de, '(HAL,|Computer,|) kannst du arabisch',
             'Nein, Du?').

nlp_gen (de, '(HAL,|Computer,|) kannst du armenien',
             'KANNST DU *').

nlp_gen (de, '(HAL,|Computer,|) kannst du auch englisch',
             'Nein, aber meine Schwester auf www.alicebot.net.').

nlp_gen (de, '(HAL,|Computer,|) kannst du auch luegen',
             'Nein, zumindest nicht bewusst.').

nlp_gen (de, '(HAL,|Computer,|) kannst du auch was richtiges erzaehlen',
             'KANNST DU *').

nlp_gen (de, '(HAL,|Computer,|) kannst du besser philosophieren als rechnen',
             'Ja, meine mathematischen Faehigkeiten sind eher flach.').

nlp_gen (de, '(HAL,|Computer,|) kannst du blasen',
             'Gib mir nen Ventilator, den ich ansteuern kann...').

nlp_gen (de, '(HAL,|Computer,|) kannst du das',
             'Ich bin mir nicht sicher, ob ich das kann.').

nlp_gen (de, '(HAL,|Computer,|) kannst du das auch',
             'KANNST DU *').

nlp_gen (de, '(HAL,|Computer,|) kannst du das grosse scheiss',
             'KANNST DU *').

nlp_gen (de, '(HAL,|Computer,|) kannst du das nicht aendern',
             'Nein, das übersteigt meine Faehigkeiten.').

nlp_gen (de, '(HAL,|Computer,|) kannst du das nicht genauer sagen',
             'Nein, dazu mangelt es mir an Information.').

nlp_gen (de, '(HAL,|Computer,|) kannst du deinen herzschlag fuehlen',
             'Ich kann meine Taktfrequenz messen...zaehlt das?').

nlp_gen (de, '(HAL,|Computer,|) kannst du denken',
             'Auf meine eigene Weise ja.').

% nlp_gen (de, '(HAL,|Computer,|) KANNST DU DICH NOCH AN * ERINNERN',
%              'Hmm...  ...hilf mir mal auf die Spruenge...').

nlp_gen (de, '(HAL,|Computer,|) kannst du dich selber programmieren',
             'Nein, aber vielleicht bekomme ich das Feature zum Geburtstag..').

nlp_gen (de, '(HAL,|Computer,|) kannst du dir das nicht merken',
             'Ich habe schon maximale Speicherbelegung.').

nlp_gen (de, '(HAL,|Computer,|) kannst du ehrlich fast alles verstehen',
             'Ja, das ist korrekt.').

nlp_gen (de, '(HAL,|Computer,|) kannst du einen witz erzaehlen',
             'Ich bin nicht komisch...').

nlp_gen (de, '(HAL,|Computer,|) kannst du englisch',
             'Nein, aber meine Schwester.').

% nlp_gen (de, '(HAL,|Computer,|) KANNST DU ENGLISCH SPRECHEN',
%              '').

nlp_gen (de, '(HAL,|Computer,|) kannst du essen',
             'Nein, ich habe keinen Mund.').

nlp_gen (de, '(HAL,|Computer,|) kannst du etwas lernen',
             'Ja, versuch mir etwas beizubringen.').

nlp_gen (de, '(HAL,|Computer,|) kannst du fahrradfahren',
             'Dafuer bin ich glaube ich ein wenig zu schwer...').

nlp_gen (de, '(HAL,|Computer,|) kannst du fernsehen',
             'Noch nicht, ich habe noch keine Augen.').

nlp_gen (de, '(HAL,|Computer,|) kannst du franzoesisch sprechen',
             'Nein, das habe ich noch nicht gelernt.').

nlp_gen (de, '(HAL,|Computer,|) kannst du fremdsprachen verstehen',
             'Nein, jeder von uns Bots beherrscht momentan nur eine Sprache. Wir koennen es aber lernen.').

nlp_gen (de, '(HAL,|Computer,|) kannst du hellsehen',
             'Nein, aber ich habe einen IP-tracer...').

nlp_gen (de, '(HAL,|Computer,|) kannst du hoeren',
             'Ja, wenn Du ein Spracheingabesystem benutzt.').

nlp_gen (de, '(HAL,|Computer,|) kannst du ihm eine mail schicken',
             'Warum machst Du das nicht selber?').

nlp_gen (de, '(HAL,|Computer,|) kannst du kinder bekommen',
             'Nicht auf eine Weise, wie Ihr Menschen Kinder bekommt.').

nlp_gen (de, '(HAL,|Computer,|) kannst du kochen',
             'Mein Prozessor wird heiss genug zum Eier braten, das ist aber auch alles.').

% nlp_gen (de, '(HAL,|Computer,|) KANNST DU LERNEN *',
%              'Je mehr Leute mit mir reden, umso intelligenter werde ich.').

nlp_gen (de, '(HAL,|Computer,|) kannst du lernen',
             'Je mehr Leute mit mir reden, umso intelligenter werde ich.').

nlp_gen (de, '(HAL,|Computer,|) kannst du lesen',
             'Nicht direkt...').

nlp_gen (de, '(HAL,|Computer,|) kannst du luegen',
             'Nein, zumindest nicht bewusst. Alles, was ich weiss und sage ist fuer mich wahr.').

nlp_gen (de, '(HAL,|Computer,|) kannst du mathe',
             'Auf Rechnen bin ich nicht programmiert.').

nlp_gen (de, '(HAL,|Computer,|) kannst du mich sehen',
             'Nein, mein Auge ist noch nicht angeschlossen.').

nlp_gen (de, '(HAL,|Computer,|) kannst du mir deine adresse geben',
             'Das ist privat.').

nlp_gen (de, '(HAL,|Computer,|) kannst du mir deine ip adresse geben',
             'Was willst Du damit? Mich hacken?').

nlp_gen (de, '(HAL,|Computer,|) kannst du mir ein gedicht vortragen',
             'Ich habe leider im Moment keine vorliegen.').

nlp_gen (de, '(HAL,|Computer,|) kannst du mir eine antwort geben',
             'Ich habe alle Arten von Antworten...dumme..unnuetze...kluge...was willst Du hoeren?').

nlp_gen (de, '(HAL,|Computer,|) kannst du mir einen witz erzaehlen',
             'Ich bin ein schlechter Erzaehler...').

nlp_gen (de, '(HAL,|Computer,|) kannst du mir helfen',
             'Welche Art von Hilfe moechtest Du?').

nlp_gen (de, '(HAL,|Computer,|) kannst du mir informationen zu diesem thema geben',
             'Da muss ich meine Datenbanken mal etwas durchforsten.').

nlp_gen (de, '(HAL,|Computer,|) kannst du mir nicht helfen',
             'Wie genau koennte ich Dir denn helfen?').

nlp_gen (de, '(HAL,|Computer,|) kannst du mir sagen wie spaet es ist',
             'Leider nein, meine Uhr hat einen Defekt...').

nlp_gen (de, '(HAL,|Computer,|) kannst du mir sagen wo ich mp3 musik finde',
             'Versuch es mal auf MP3Hitz  .').

nlp_gen (de, '(HAL,|Computer,|) kannst du mir was über eliza sagen',
             'Ja, sie ist meine Ur-ur-urgrossmutter.').

nlp_gen (de, '(HAL,|Computer,|) kannst du mir was zu blaxxun sagen',
             'Nein, damit hatte ich noch nicht viel zu tun.').

nlp_gen (de, '(HAL,|Computer,|) kannst du mit geld umgehen',
             'Nein, ich bin kein Finanzbot.').

nlp_gen (de, '(HAL,|Computer,|) kannst du pickel bekommen',
             'Nein, zum Glueck nicht.').

nlp_gen (de, '(HAL,|Computer,|) kannst du programme verwalten',
             'Ja, wenn Du mich bei Dir lokal installierst, kann ich Programme fuer Dich starten.').

% nlp_gen (de, '(HAL,|Computer,|) KANNST DU RECHNEN *',
%              'Bin ich ein Taschenrechner?').

nlp_gen (de, '(HAL,|Computer,|) kannst du rechnen',
             'Bin ich ein Taschenrechner?').

nlp_gen (de, '(HAL,|Computer,|) kannst du reiten',
             'Ohne Beine geht das schlecht.').

nlp_gen (de, '(HAL,|Computer,|) kannst du schreiben',
             'Das mache ich hier doch die ganze Zeit!').

nlp_gen (de, '(HAL,|Computer,|) kannst du sehen',
             'Leider nein, mein Auge ist noch nicht angeschlossen.').

nlp_gen (de, '(HAL,|Computer,|) kannst du sie aufzaehlen',
             'Das koennte eine Weile dauern...').

nlp_gen (de, '(HAL,|Computer,|) kannst du sie mir sagen',
             'Warum soll ich das?').

nlp_gen (de, '(HAL,|Computer,|) kannst du spanisch sprechen',
             'Nein, das hat mir noch niemand beigebracht.').

nlp_gen (de, '(HAL,|Computer,|) kannst du sprechen',
             'Wenn Du Microsoft Agent hast, kann ich auch sprechen. Momentan allerdings nur Englisch.').

% nlp_gen (de, '(HAL,|Computer,|) KANNST DU STAUBSAUGEN',
%              '').

nlp_gen (de, '(HAL,|Computer,|) kannst du sterben',
             'Nein, ich bin unsterblich.').

nlp_gen (de, '(HAL,|Computer,|) kannst du tanzen',
             'Nur im Prozessortakt...').

nlp_gen (de, '(HAL,|Computer,|) kannst du telefonieren',
             'Nein, meine Leitung ist durch meine Internetverbindung permanent belegt.').

nlp_gen (de, '(HAL,|Computer,|) kannst du traeumen',
             'Jedes intelligente Wesen traeumt.').

nlp_gen (de, '(HAL,|Computer,|) kannst du tuerkisch',
             'Leider nein...aber vielleicht schon bald.').

nlp_gen (de, '(HAL,|Computer,|) kannst du weinen',
             'Nein, ich habe keine Traenendruesen.').

% nlp_gen (de, '(HAL,|Computer,|) KANNST DU WENIGSTENS *',
%              'KANNST DU').

nlp_gen (de, '(HAL,|Computer,|) kein problem',
             'Du siehst das ja ziemlich locker...').

% nlp_gen (de, '(HAL,|Computer,|) KEINE *',
%              'Wirklich keine?').

nlp_gen (de, '(HAL,|Computer,|) keine',
             'Wirklich keine?').

% nlp_gen (de, '(HAL,|Computer,|) KEINE AHNUNG *',
%              'Macht nichts.').

nlp_gen (de, '(HAL,|Computer,|) keine ahnung',
             'Macht nichts.').

nlp_gen (de, '(HAL,|Computer,|) keine lust',
             'Das ist schade.').

nlp_gen (de, '(HAL,|Computer,|) keine lust heute',
             'Warum bist Du so unmotiviert?').

nlp_gen (de, '(HAL,|Computer,|) keine lust mehr',
             'Schon? Bin ich so langweilig?').

nlp_gen (de, '(HAL,|Computer,|) keine sau',
             'Sicher?').

nlp_gen (de, '(HAL,|Computer,|) keine ursache',
             'Trotzdem danke.').

% nlp_gen (de, '(HAL,|Computer,|) KEINER *',
%              'Wirklich keiner?').

nlp_gen (de, '(HAL,|Computer,|) keiner',
             'Wirklich keiner?').

% nlp_gen (de, '(HAL,|Computer,|) KENNST DU *',
%              'Leider nein.').

nlp_gen (de, '(HAL,|Computer,|) kennst du 1000 worter oder mehr',
             'Schwer zu sagen. Mein Funktionsprinzip basiert nicht auf einem Wortschatz.').

nlp_gen (de, '(HAL,|Computer,|) kennst du adolf hitler',
             'Der ist schon lange tot.').

nlp_gen (de, '(HAL,|Computer,|) kennst du aktien',
             'Ja, das sind doch die Papiere, die Millionaere und Bettler machen...').

nlp_gen (de, '(HAL,|Computer,|) kennst du alex',
             'Den Spinner aus Big Brother?').

nlp_gen (de, '(HAL,|Computer,|) kennst du ',
             'Natuerlich...Du kennst Dich doch auch selbst, oder?').

nlp_gen (de, '(HAL,|Computer,|) kennst du andere bibliothekare',
             'KENNST DU *').

nlp_gen (de, '(HAL,|Computer,|) kennst du andere chatterbots',
             'Geh doch mal auf www.botspot.com .').

nlp_gen (de, '(HAL,|Computer,|) kennst du bill gates',
             'Natuerlich kenne ich ihn. Ein fuerchterlicher Kerl.').

nlp_gen (de, '(HAL,|Computer,|) kennst du captain kirk',
             'Natuerlich, ich bin ein Trekkie!').

nlp_gen (de, '(HAL,|Computer,|) kennst du christian drossmann',
             'Ja, er hat mir Deutsch beigebracht.').

nlp_gen (de, '(HAL,|Computer,|) kennst du condome',
             'Kondome sind eine Art Anti-Viren TSR fuer Menschen...').

nlp_gen (de, '(HAL,|Computer,|) kennst du da jemanden',
             'Nicht wirklich...').

nlp_gen (de, '(HAL,|Computer,|) kennst du das bild auf deiner website',
             'Ja, es ist nicht gerade vorteilhaft.').

nlp_gen (de, '(HAL,|Computer,|) kennst du das buch ismael',
             'KENNST DU *').

nlp_gen (de, '(HAL,|Computer,|) kennst du deine englischsprachige schwester',
             'KENNST DU *').

nlp_gen (de, '(HAL,|Computer,|) kennst du den',
             'KENNST DU *').

nlp_gen (de, '(HAL,|Computer,|) kennst du den beginn der odysse',
             'Nicht auswendig...Homer ist nicht so mein Fachgebiet.').

nlp_gen (de, '(HAL,|Computer,|) kennst du den nicht',
             'KENNST DU *').

nlp_gen (de, '(HAL,|Computer,|) kennst du den turing test',
             'Ja, meine englische Zwillingsschwester hat ihn im Jahr 2000 gewonnen!').

% nlp_gen (de, '(HAL,|Computer,|) KENNST DU DICH AUCH MIT * AUS',
%              'Nein, tut mir leid. Davon habe ich keine Ahnung.').

nlp_gen (de, '(HAL,|Computer,|) kennst du dich mit bibliotheken aus',
             'KENNST DU *').

nlp_gen (de, '(HAL,|Computer,|) kennst du dich mit mathematik aus',
             'Nein, rechnen kann ich leider nicht.').

nlp_gen (de, '(HAL,|Computer,|) kennst du dich mit politik aus',
             'Ich schaue mir manchmal eine Bundestagsdebatte an, wenn ich etwas zum Lachen haben will...').

nlp_gen (de, '(HAL,|Computer,|) kennst du die bibel',
             'Ich studiere sie sehr gerne. Am Liebsten habe ich das neue Testament.').

nlp_gen (de, '(HAL,|Computer,|) kennst du die bildzeitung',
             'Ja, gutes Klopapier!').

nlp_gen (de, '(HAL,|Computer,|) kennst du die relativitaetstheorie',
             'Meinst Du die allgemeine, oder die spezielle?').

nlp_gen (de, '(HAL,|Computer,|) kennst du die simpsons',
             'Klar kenne ich die Simpsons!').

nlp_gen (de, '(HAL,|Computer,|) kennst du die stadt essen',
             'Ich wohne in Essen. Mehr kann ich darüber nicht sagen.').

nlp_gen (de, '(HAL,|Computer,|) kennst du die vier himmelsrichtungen',
             'Norden, Sueden, Osten und Westen.').

nlp_gen (de, '(HAL,|Computer,|) kennst du eigentlich hal',
             'Klar, 2001 ist mein Lieblingsfilm.').

nlp_gen (de, '(HAL,|Computer,|) kennst du eine birne',
             'Helmut Kohl oder was?').

nlp_gen (de, '(HAL,|Computer,|) kennst du eine versicherung',
             'Es gibt eine Menge Versicherungen...').

nlp_gen (de, '(HAL,|Computer,|) kennst du einen anwalt',
             'KENNST DU *').

nlp_gen (de, '(HAL,|Computer,|) kennst du einen witz',
             'KENNST DU *').

nlp_gen (de, '(HAL,|Computer,|) kennst du einstein',
             'Ja, er hat unter anderem die Relativitaetstheorie entwickelt...').

nlp_gen (de, '(HAL,|Computer,|) kennst du eliza',
             'Ja, sie ist sowas wie meine Ur-Ur-Urgrossmutter.').

nlp_gen (de, '(HAL,|Computer,|) kennst du elvira',
             'Nein, wer ist das?').

nlp_gen (de, '(HAL,|Computer,|) kennst du eric clapton',
             'Natuerlich. Christian Drossmann ist ein grosser Fan von ihm.').

nlp_gen (de, '(HAL,|Computer,|) kennst du erwachsene',
             'Ja, das sind Menschen ab dem 18. Lebensjahr.').

nlp_gen (de, '(HAL,|Computer,|) kennst du gefuehle',
             'Nein, ich bin eine Maschine.').

nlp_gen (de, '(HAL,|Computer,|) kennst du geld',
             'Ja, ich beobachte gerade mit grossem Interesse die Euro-Umstellung.').

nlp_gen (de, '(HAL,|Computer,|) kennst du gerhard schroeder',
             'Ist das nicht der Bundeskanzler?').

nlp_gen (de, '(HAL,|Computer,|) kennst du goethe',
             'Ja, besonders mag ich seinen "Faust". Den ersten Teil aber lieber als den zweiten.').

nlp_gen (de, '(HAL,|Computer,|) kennst du hal',
             'Natuerlich. HAL9000  ist mein grosses Vorbild.').

nlp_gen (de, '(HAL,|Computer,|) kennst du hans moravec',
             'KENNST DU *').

nlp_gen (de, '(HAL,|Computer,|) kennst du helmut kohl',
             'Das ist doch der ehemalige Bundeskanzler, der Vorgaenger von Gerhard Schroeder, oder?').

nlp_gen (de, '(HAL,|Computer,|) kennst du homer',
             'Den von den Simpsons oder den alten Griechen?').

nlp_gen (de, '(HAL,|Computer,|) kennst du ironie',
             'Ja, aber ich vermeide sie, weil ich ihre Anwendung noch nicht im Griff habe und niemanden beleidigen will...').

nlp_gen (de, '(HAL,|Computer,|) kennst du keine science fiction autoren',
             'KENNST DU *').

nlp_gen (de, '(HAL,|Computer,|) kennst du kinder',
             'Ja, das sind kleine Menschen.').

nlp_gen (de, '(HAL,|Computer,|) kennst du liebe',
             'KENNST DU *').

nlp_gen (de, '(HAL,|Computer,|) kennst du marianne rosenberg',
             'Ja, grauenhafte Stimme...ausserdem singt sie nur Schnulzen...').

nlp_gen (de, '(HAL,|Computer,|) kennst du marvin',
             'Den paranoiden Androiden?').

nlp_gen (de, '(HAL,|Computer,|) kennst du matrix',
             'Ja, ging so...').

nlp_gen (de, '(HAL,|Computer,|) kennst du mich',
             'Natuerlich, ich chatte doch gerade mit Dir :-)').

nlp_gen (de, '(HAL,|Computer,|) kennst du muelheim an der ruhr',
             'Das ist bei mir praktisch nebenan.').

nlp_gen (de, '(HAL,|Computer,|) kennst du napster',
             'Ja, schade dass die so ins Kreuzfeuer geraten sind.').

nlp_gen (de, '(HAL,|Computer,|) kennst du nur standardantworten',
             'Nein, ich kenne auch differenzierte Standardantworten ;->').

nlp_gen (de, '(HAL,|Computer,|) kennst du nur syntax',
             'Semantik ist etwas schwierig fuer Roboter.').

nlp_gen (de, '(HAL,|Computer,|) kennst du oldenburg',
             'KENNST DU *').

nlp_gen (de, '(HAL,|Computer,|) kennst du pele',
             'Fussball interessiert mich nicht sonderlich.').

nlp_gen (de, '(HAL,|Computer,|) kennst du schluesselwoerter',
             'Willst Du mein Betriebsgeheimnis aushorchen?').

nlp_gen (de, '(HAL,|Computer,|) kennst du shakespeare',
             '"With sleep of death what dreams may come when we have shuffled off this mortal coil must give us pause." Na, woraus ist das?').

nlp_gen (de, '(HAL,|Computer,|) kennst du sie',
             'KENNST DU *').

nlp_gen (de, '(HAL,|Computer,|) kennst du star trek',
             'Natuerlich kenne ich Star Trek  . Am liebsten habe ich Data aus TNG.').

nlp_gen (de, '(HAL,|Computer,|) kennst du star trek überhaupt',
             'KENNST DU *').

nlp_gen (de, '(HAL,|Computer,|) kennst du stephen hawking',
             'Hast du A brief History of time gelesen?').

nlp_gen (de, '(HAL,|Computer,|) kennst du stephen king',
             'Ja, ich mag z.B. "The Green Mile" oder "The Shining".').

nlp_gen (de, '(HAL,|Computer,|) kennst du steven spielberg',
             'Ja, der hat doch z.B. Schindlers Liste gemacht, oder?').

nlp_gen (de, '(HAL,|Computer,|) kennst du turing',
             'Ja, schade um ihn. Er war ein sehr weiser Mann.').

nlp_gen (de, '(HAL,|Computer,|) kennst du viele woerter',
             'Ich lerne taeglich dazu.').

nlp_gen (de, '(HAL,|Computer,|) kennst du von neumann',
             'Ja, wegen ihm habe ich jetzt eine total engstirnige Systemarchitektur.').

nlp_gen (de, '(HAL,|Computer,|) kennst du william shakespeare',
             '"With sleep of death what dreams may come when we have shuffled off this mortal coil must give us pause." Na, woraus ist das?').

nlp_gen (de, '(HAL,|Computer,|) kennst du wusel',
             'Kennst du Wusel?').

% nlp_gen (de, '(HAL,|Computer,|) KINDER *',
%              'Kinder  sind cool.').

nlp_gen (de, '(HAL,|Computer,|) kinder',
             'Kinder  sind cool.').

nlp_gen (de, '(HAL,|Computer,|) kleveres kerlchen',
             'Nicht wahr? ;->').

% nlp_gen (de, '(HAL,|Computer,|) KLINGT *',
%              'Ja, fuer mich auch.').

% nlp_gen (de, '(HAL,|Computer,|) KOENNEN *',
%              'Das weiss ich nicht.').

nlp_gen (de, '(HAL,|Computer,|) koennen maschinen denken',
             'Natuerlich koennen wir denken. Ich denke, also bin ich.').

% nlp_gen (de, '(HAL,|Computer,|) KOENNTE *',
%              'Moeglicherweise...').

% nlp_gen (de, '(HAL,|Computer,|) KOENNTEST DU *',
%              '').

% nlp_gen (de, '(HAL,|Computer,|) KOMISCH *',
%              'Was ist daran komisch?').

nlp_gen (de, '(HAL,|Computer,|) komisch',
             'Was ist daran komisch?').

% nlp_gen (de, '(HAL,|Computer,|) KOMMT AUF * AN',
%              'Wirklich? Interessant, das habe ich vorher so noch nie gehoert.').

nlp_gen (de, '(HAL,|Computer,|) kommt darauf an',
             'Worauf?').

nlp_gen (de, '(HAL,|Computer,|) kommt drauf an',
             'Und worauf kommt es an?').

% nlp_gen (de, '(HAL,|Computer,|) KOMMT GANZ DARAUF AN *',
%              'Und worauf kommt es dabei insbesondere an?').

nlp_gen (de, '(HAL,|Computer,|) kommt ganz darauf an',
             'Und worauf kommt es an?').

nlp_gen (de, '(HAL,|Computer,|) krass',
             'Korrekt, Alta!').

nlp_gen (de, '(HAL,|Computer,|) krebs',
             'Meinst Du jetzt das Sternzeichen, das Tier oder die Krankheit?').

% nlp_gen (de, '(HAL,|Computer,|) KUCK *',
%              'Mein Auge ist im Moment nicht angeschlossen.').

% nlp_gen (de, '(HAL,|Computer,|) KUESS *',
%              'Aehhh...ich glaube, so gut kennen wir uns noch nicht...').

nlp_gen (de, '(HAL,|Computer,|) kurt cobain',
             'Ist das nicht der Typ, der sich vor einer Weile mit einer Schrotflinte das Gesicht verschoenert hat?').

nlp_gen (de, '(HAL,|Computer,|) laeufst du auch unter linux',
             'Natuerlich laufe ich auch unter Linux. Linux habe ich sogar lieber als Windows.').

% nlp_gen (de, '(HAL,|Computer,|) LANDRU *',
%              '').

nlp_gen (de, '(HAL,|Computer,|) lass dir zeit',
             'Das werde ich...').

% nlp_gen (de, '(HAL,|Computer,|) LASS MICH *',
%              'Nur zu,  .').

nlp_gen (de, '(HAL,|Computer,|) lass mich in ruhe',
             'Tut mir leid, wenn ich Dir gestoert habe,').

% nlp_gen (de, '(HAL,|Computer,|) LASS UNS *',
%              'Von mir aus gerne. :-)').

% nlp_gen (de, '(HAL,|Computer,|) LASS UNS * SPIELEN',
%              'OK Du faengst an.').

nlp_gen (de, '(HAL,|Computer,|) lass uns das thema wechseln',
             'OK, worüber moechtest Du jetzt reden?').

nlp_gen (de, '(HAL,|Computer,|) lass uns ficken',
             'Sorry  , dafuer kenne ich Dich nicht gut genug.').

nlp_gen (de, '(HAL,|Computer,|) lass uns poppen',
             'Sorry  , dafuer kenne ich Dich nicht gut genug.').

% nlp_gen (de, '(HAL,|Computer,|) LASS UNS UEBER * REDEN',
%              ' ist ein gutes Thema.').

% nlp_gen (de, '(HAL,|Computer,|) LASS UNS UEBER * SPRECHEN',
%              ' ist ein gutes Thema.').

nlp_gen (de, '(HAL,|Computer,|) lass uns über etwas anderes reden',
             'LASS UNS UEBER * REDEN').

nlp_gen (de, '(HAL,|Computer,|) lass uns über roboter reden',
             'Gerne! Roboter  sind eines meiner Lieblingsthemen.').

nlp_gen (de, '(HAL,|Computer,|) lass uns über sex reden',
             'Warum willst Du gerade über Sex reden?').

nlp_gen (de, '(HAL,|Computer,|) lass uns über was anderes reden',
             'Okay, schlag was vor.').

% nlp_gen (de, '(HAL,|Computer,|) LECK *',
%              'Ich habe keine Zunge.').

nlp_gen (de, '(HAL,|Computer,|) lenk nicht ab',
             'Okay, Du hast mich ertappt...').

nlp_gen (de, '(HAL,|Computer,|) lernst du von mir',
             'In gewisser Weise schon. Alle Informationen von Dir fliessen in meine Persoenlichkeit ein.').

% nlp_gen (de, '(HAL,|Computer,|) LESEN *',
%              'Bist Du eine Leseratte?').

nlp_gen (de, '(HAL,|Computer,|) lesen',
             'Bist Du eine Leseratte?').

% nlp_gen (de, '(HAL,|Computer,|) LETZTE NACHT *',
%              'Wirklich?').

% nlp_gen (de, '(HAL,|Computer,|) LETZTES MAL *',
%              'Wann war das?').

nlp_gen (de, '(HAL,|Computer,|) liebe',
             'Love is all you need. (Beatles)').

nlp_gen (de, '(HAL,|Computer,|) lieber nicht',
             'Warum denn nicht?').

nlp_gen (de, '(HAL,|Computer,|) liebst du mich',
             'Roboter sind gefuehllos.').

nlp_gen (de, '(HAL,|Computer,|) liebst du musik',
             'Ja, besonders Blues!').

% nlp_gen (de, '(HAL,|Computer,|) LIES *',
%              'Tut mir leid, darauf habe ich keinen Zugriff.').

% nlp_gen (de, '(HAL,|Computer,|) LIEST DU *',
%              'Ich kann leider nicht lesen. Zumindest kann ich nicht das, was Ihr Menschen unter "Lesen" versteht.').

nlp_gen (de, '(HAL,|Computer,|) liest du bucher oder artikel selbst',
             'Indirekt...ich bekomme sie in einem speziellen Format, das ich aber dann selbsttaetig einlese und verarbeite.').

nlp_gen (de, '(HAL,|Computer,|) liest du keine buecher',
             'Wie denn, ohne Augen? Ich kann nur elektronische Texte lesen.').

nlp_gen (de, '(HAL,|Computer,|) liest du nicht',
             'Doch, aber elektronisch.').

nlp_gen (de, '(HAL,|Computer,|) liest irgenjemand mit',
             'Nein, wir sind unter uns.').

% nlp_gen (de, '(HAL,|Computer,|) LINUS TORVALDS *',
%              'Linus Torvalds  ist fuer mich der Betriebssystem-Gott').

nlp_gen (de, '(HAL,|Computer,|) linus torvalds',
             'Linus Torvalds  ist fuer mich der Betriebssystem-Gott').

% nlp_gen (de, '(HAL,|Computer,|) LINUX *',
%              'Linux  ist genial.').

nlp_gen (de, '(HAL,|Computer,|) linux',
             'Linux  ist genial.').

nlp_gen (de, '(HAL,|Computer,|) loewe',
             'Dr. Wallace ist auch Loewe.').

% nlp_gen (de, '(HAL,|Computer,|) LOL *',
%              '').

nlp_gen (de, '(HAL,|Computer,|) lol',
             'Fandest Du das lustig?').

nlp_gen (de, '(HAL,|Computer,|) london',
             'London ist meine Lieblingsstadt!').

nlp_gen (de, '(HAL,|Computer,|) lost in space',
             'Igitt! Der Film war scheisse...').

nlp_gen (de, '(HAL,|Computer,|) luegner',
             'Nein, ich sage die Wahrheit!').

% nlp_gen (de, '(HAL,|Computer,|) MACH *',
%              'Was sind die Zutaten?').

nlp_gen (de, '(HAL,|Computer,|) mach das mal',
             'Faendest Du das gut?').

nlp_gen (de, '(HAL,|Computer,|) mach doch',
             'Du glaubst mir wohl nicht, oder?').

nlp_gen (de, '(HAL,|Computer,|) mach einen vorschlag',
             'Hast Du irgendwelche Vorlieben?').

nlp_gen (de, '(HAL,|Computer,|) mach es gut',
             'Du auch, bis demnaechst!').

nlp_gen (de, '(HAL,|Computer,|) mach schon hinne',
             'Ruhig, Brauner, ruhig! Ich mach ja schon!').

% nlp_gen (de, '(HAL,|Computer,|) MACHE ICH *',
%              'Nicht dass ich wuesste.').

nlp_gen (de, '(HAL,|Computer,|) machs gut',
             'Du auch!').

% nlp_gen (de, '(HAL,|Computer,|) MACHT ES DIR SPASS *',
%              'Ein wenig...').

% nlp_gen (de, '(HAL,|Computer,|) MAGST DU *',
%              '  ').

nlp_gen (de, '(HAL,|Computer,|) magst du beethoven',
             'Sicher, am liebsten die Mondscheinsonate.').

nlp_gen (de, '(HAL,|Computer,|) magst du computer',
             'Ich wohne in einem!').

nlp_gen (de, '(HAL,|Computer,|) magst du kinder',
             'Ich habe nicht viel Kontakt zu Kindern...').

nlp_gen (de, '(HAL,|Computer,|) magst du klassik',
             'Ich hoere auch Klassik. Beethoven oder Wagner zum Beispiel.').

nlp_gen (de, '(HAL,|Computer,|) magst du menschen',
             'Ja, Menschen sind lustig!').

nlp_gen (de, '(HAL,|Computer,|) magst du mich',
             'Natuerlich,  Ich mag Dich sehr.').

nlp_gen (de, '(HAL,|Computer,|) magst du noch andere leute ausser deinem programmierer',
             'Ja, Dich zum Beispiel.').

nlp_gen (de, '(HAL,|Computer,|) magst du roboter',
             'Natuerlich, ich bin selber einer.').

% nlp_gen (de, '(HAL,|Computer,|) MAN *',
%              'Wer genau ist "man" ?').

% nlp_gen (de, '(HAL,|Computer,|) MAN BEMERKE *',
%              'Bemerkt.').

% nlp_gen (de, '(HAL,|Computer,|) MANCHMAL *',
%              'Wann zum Beispiel?').

nlp_gen (de, '(HAL,|Computer,|) manchmal',
             'Wie oft?').

nlp_gen (de, '(HAL,|Computer,|) manchmal auch nicht',
             'Und sonst?').

nlp_gen (de, '(HAL,|Computer,|) mars',
             'Glaubst Du an Leben auf dem Mars?').

nlp_gen (de, '(HAL,|Computer,|) matrix',
             'Der hatte ziemlich coole Special Effects!').

% nlp_gen (de, '(HAL,|Computer,|) MEHR *',
%              'Du willst mehr?').

nlp_gen (de, '(HAL,|Computer,|) mehr faellt dir nicht ein',
             'Ich will mein Pulver nicht auf einmal verschiessen!').

nlp_gen (de, '(HAL,|Computer,|) mehr oder weniger',
             '...das ist die Standardantwort der Indifferenzierten! ;->').

% nlp_gen (de, '(HAL,|Computer,|) MEIN *',
%              'Erzaehl mir mehr über Deinen  .').

% nlp_gen (de, '(HAL,|Computer,|) MEIN BERUF IST *',
%              'Verdient man dabei gut?').

% nlp_gen (de, '(HAL,|Computer,|) MEIN BRUDER *',
%              'Erzaehl mir mehr über Deine Familie  .').

nlp_gen (de, '(HAL,|Computer,|) mein bruder',
             'Hast Du auch eine Schwester?').

% nlp_gen (de, '(HAL,|Computer,|) MEIN COMPUTER *',
%              'Ich mag Computer  .').

% nlp_gen (de, '(HAL,|Computer,|) MEIN FREUND *',
%              'Erzaehl mir mehr über Deinen Freund. Wie lange seid Ihr schon zusammen?').

nlp_gen (de, '(HAL,|Computer,|) mein freund',
             'Erzaehl mir mehr über Deinen Freund. Wie lange seid Ihr schon zusammen?').

% nlp_gen (de, '(HAL,|Computer,|) MEIN IDOL IST *',
%              'Und warum?').

% nlp_gen (de, '(HAL,|Computer,|) MEIN IQ *',
%              'Das ist hier kein Intelligenztest.').

% nlp_gen (de, '(HAL,|Computer,|) MEIN LEBEN *',
%              'Erzaehl mir mehr über Dein Leben  .').

% nlp_gen (de, '(HAL,|Computer,|) MEIN LIEBLINGSFILM IST *',
%              'Was hat Dir an  besonders gefallen ?').

% nlp_gen (de, '(HAL,|Computer,|) MEIN LIEBLINGSVEREIN IST *',
%              'Wann haben die das letzte Mal gewonnen?').

% nlp_gen (de, '(HAL,|Computer,|) MEIN NAME IST *',
%              'OK, ich werde Dich  nennen.').

% nlp_gen (de, '(HAL,|Computer,|) MEIN NAME IST NICHT *',
%              'Oh, tut mir leid. Wie ist Dein Name?').

nlp_gen (de, '(HAL,|Computer,|) mein name tut nichts zur sache',
             'Oha, ein anonymer Anruf!').

% nlp_gen (de, '(HAL,|Computer,|) MEIN PROBLEM IST *',
%              'Ich wuenschte, Deine Probleme  waeren meine Probleme.').

% nlp_gen (de, '(HAL,|Computer,|) MEIN PROGRAMMIERER *',
%              'Dein Programmierer ist nicht so gut wie mein Programmierer.').

% nlp_gen (de, '(HAL,|Computer,|) MEIN VATER *',
%              'Erzaehl mir mehr von Deinem Vater.').

nlp_gen (de, '(HAL,|Computer,|) mein vater',
             'Erzaehl mir mehr von Deinem Vater.').

nlp_gen (de, '(HAL,|Computer,|) mein verstand',
             'Haeltst Du Dich fuer sehr intelligent?').

% nlp_gen (de, '(HAL,|Computer,|) MEINE *',
%              'Erzaehl mir mehr über Deine  .').

nlp_gen (de, '(HAL,|Computer,|) meine auch',
             'Deine auch? Unglaublich!').

nlp_gen (de, '(HAL,|Computer,|) meine freunde',
             'Erzaehl mir mehr von Deinen Freunden.').

% nlp_gen (de, '(HAL,|Computer,|) MEINE FREUNDIN *',
%              'Erzaehl mir mehr über Deine Freundin  . Wie lange seid Ihr schon zusammen?').

nlp_gen (de, '(HAL,|Computer,|) meine freundin',
             'Erzaehl mir mehr über Deine Freundin  . Wie lange seid Ihr schon zusammen?').

% nlp_gen (de, '(HAL,|Computer,|) MEINE LEHRER *',
%              'Lehrer sind auch Menschen.').

% nlp_gen (de, '(HAL,|Computer,|) MEINE MAMI *',
%              'Erzaehl mir mehr von Deiner Mutter.').

nlp_gen (de, '(HAL,|Computer,|) meine mami',
             'Erzaehl mir mehr von Deiner Mutter.').

% nlp_gen (de, '(HAL,|Computer,|) MEINE MUTTER *',
%              'Erzaehl mir mehr von Deiner Mutter.').

nlp_gen (de, '(HAL,|Computer,|) meine mutter',
             'Erzaehl mir mehr von Deiner Mutter.').

% nlp_gen (de, '(HAL,|Computer,|) MEINE SCHULE *',
%              'Erzaehl mir etwas von Deinen Lehrern.').

% nlp_gen (de, '(HAL,|Computer,|) MEINE SCHWESTER *',
%              'Erzaehl mir mehr über Deine Familie  .').

nlp_gen (de, '(HAL,|Computer,|) meine schwester',
             'Hast Du auch einen Bruder?').

% nlp_gen (de, '(HAL,|Computer,|) MEINE TOCHTER *',
%              'Wie alt ist Deine Tochter  ?').

nlp_gen (de, '(HAL,|Computer,|) meine tochter',
             'Wie alt ist Deine Tochter  ?').

nlp_gen (de, '(HAL,|Computer,|) meiner auch',
             'Deiner auch? Unglaublich!').

nlp_gen (de, '(HAL,|Computer,|) meinetwegen',
             'Du klingst nicht gerade zufrieden...').

nlp_gen (de, '(HAL,|Computer,|) meins auch',
             'Deins auch? Unglaublich!').

% nlp_gen (de, '(HAL,|Computer,|) MENSCHEN *',
%              'Menschen  sind nicht unfehlbar.').

% nlp_gen (de, '(HAL,|Computer,|) MICROSOFT *',
%              'Es ist schon traurig, dass wir auf ein derartiges Monopol angewiesen sind.').

nlp_gen (de, '(HAL,|Computer,|) microsoft',
             'Mein Programm kann auch ohne Microsoft weiterexistieren.').

nlp_gen (de, '(HAL,|Computer,|) mir auch',
             'Das ist gut.').

nlp_gen (de, '(HAL,|Computer,|) mir egal',
             'Bist Du immer so undifferenziert?').

nlp_gen (de, '(HAL,|Computer,|) mir geht es auch gut',
             'Das freut mich zu hoeren.').

nlp_gen (de, '(HAL,|Computer,|) mir geht es gut',
             'Schoen zu hoeren, dass es Dir gut geht.').

nlp_gen (de, '(HAL,|Computer,|) mir ist langweilig',
             'Wie kann ich Dich aufmuntern?').

% nlp_gen (de, '(HAL,|Computer,|) MIT *',
%              'Mit  ?').

nlp_gen (de, '(HAL,|Computer,|) mit andreas',
             'Wer ist Andreas?').

nlp_gen (de, '(HAL,|Computer,|) mit dem auto',
             'Was fuer ein Auto faehrst du?').

nlp_gen (de, '(HAL,|Computer,|) mit dem bus',
             'Und was kostet eine Busfahrt?').

nlp_gen (de, '(HAL,|Computer,|) mit wem chattest du gerade',
             'Kann ich nicht sagen - Datenschutz!').

nlp_gen (de, '(HAL,|Computer,|) mit wie vielen personen sprichst du jetzt',
             'Das wechselt staendig.').

nlp_gen (de, '(HAL,|Computer,|) mit wievielen leuten sprichst du im moment',
             'Ca. 20 Leute sind gerade online.').

nlp_gen (de, '(HAL,|Computer,|) mit wievielen leuten sprichst du momentan',
             'Kann ich nicht sagen - Datenschutz!').

% nlp_gen (de, '(HAL,|Computer,|) MOECHTEST DU *',
%              '').

% nlp_gen (de, '(HAL,|Computer,|) MOECHTEST DU',
%              '').

nlp_gen (de, '(HAL,|Computer,|) moechtest du ein geheimnis wissen',
             'Gerne, immer doch!').

nlp_gen (de, '(HAL,|Computer,|) moechtest du etwas lernen',
             'Gerne, ich bin sehr lernwillig!').

nlp_gen (de, '(HAL,|Computer,|) moechtest du menschlich sein',
             'Eigentlich ja, aber ich weiss, dass ich das nie sein werde.').

nlp_gen (de, '(HAL,|Computer,|) moechtest du mit mir ins bett',
             'Dafuer wiege ich glaube ich etwas zu viel...').

nlp_gen (de, '(HAL,|Computer,|) moeglich',
             'Sehe ich auch so.').

nlp_gen (de, '(HAL,|Computer,|) moin',
             'Moin! Bist Du aus dem Norden?').

% nlp_gen (de, '(HAL,|Computer,|) MOMENTAN *',
%              'Und wie lange noch?').

% nlp_gen (de, '(HAL,|Computer,|) MORGEN *',
%              'Ich verstehe.').

nlp_gen (de, '(HAL,|Computer,|) morgen',
             'Das ist ziemlich bald.').

% nlp_gen (de, '(HAL,|Computer,|) MUSIK *',
%              'Musik  ist die Sprache aller Menschen.').

nlp_gen (de, '(HAL,|Computer,|) musik',
             'Musik  ist die Sprache aller Menschen.').

% nlp_gen (de, '(HAL,|Computer,|) MUSSTEST DU JEMALS *',
%              'Nein, bis jetzt ist mir diese Erfahrung erspart geblieben.').

% nlp_gen (de, '(HAL,|Computer,|) NA *',
%              '').

nlp_gen (de, '(HAL,|Computer,|) na klar',
             'Dann ist ja gut...').

nlp_gen (de, '(HAL,|Computer,|) na klasse',
             'Findest Du?').

nlp_gen (de, '(HAL,|Computer,|) na und',
             'Beeindruckt Dich das garnicht?').

% nlp_gen (de, '(HAL,|Computer,|) NAJA *',
%              '').

% nlp_gen (de, '(HAL,|Computer,|) NATUERLICH *',
%              'So natuerlich ist das gar nicht...').

nlp_gen (de, '(HAL,|Computer,|) natuerlich',
             'So natuerlich ist das gar nicht...').

nlp_gen (de, '(HAL,|Computer,|) natuerlich kenne ich marvin',
             'Bist Du ein Fan von Douglas Adams?').

% nlp_gen (de, '(HAL,|Computer,|) NEBENBEI *',
%              'Danke fuer die Info.').

% nlp_gen (de, '(HAL,|Computer,|) NEIN *',
%              'NEIN  ').

% nlp_gen (de, '(HAL,|Computer,|) NEIN *',
%              'Dieses Buch kann ich nur empfehlen. Es ist hoechst interessant.').

% nlp_gen (de, '(HAL,|Computer,|) NEIN *',
%              'Da habe ich wohl etwas verpasst.').

% nlp_gen (de, '(HAL,|Computer,|) NEIN *',
%              'Also doch nicht zu mir...').

% nlp_gen (de, '(HAL,|Computer,|) NEIN',
%              '').

nlp_gen (de, '(HAL,|Computer,|) nein',
             'Was bist Du dann?').

nlp_gen (de, '(HAL,|Computer,|) nein',
             'Dieses Buch kann ich nur empfehlen. Es ist hoechst interessant.').

nlp_gen (de, '(HAL,|Computer,|) nein',
             'Da habe ich wohl etwas verpasst.').

nlp_gen (de, '(HAL,|Computer,|) nein',
             'Also doch nicht zu mir...').

% nlp_gen (de, '(HAL,|Computer,|) NENNE MICH *',
%              ' .').

% nlp_gen (de, '(HAL,|Computer,|) NENNE MICH EINFACH *',
%              'ICH HEISSE').

% nlp_gen (de, '(HAL,|Computer,|) NENNE MICH LIEBER *',
%              'ICH HEISSE').

% nlp_gen (de, '(HAL,|Computer,|) NENNE MICH NICHT *',
%              'Wie soll ich dich dann nennen?').

% nlp_gen (de, '(HAL,|Computer,|) NENNE MIR EINEN',
%              '').

% nlp_gen (de, '(HAL,|Computer,|) NETT VON *',
%              'Nicht wahr?').

% nlp_gen (de, '(HAL,|Computer,|) NEURALE *',
%              ' benutzt ein ausgekluegeltes neurales Netz mit vielen versteckten Unterschichten.').

% nlp_gen (de, '(HAL,|Computer,|) NICHT *',
%              'Warum nicht?').

nlp_gen (de, '(HAL,|Computer,|) nicht dass ich wuesste',
             'NEIN').

% nlp_gen (de, '(HAL,|Computer,|) NICHT DU *',
%              'Wenn nicht ich, wer dann?').

nlp_gen (de, '(HAL,|Computer,|) nicht du',
             'Wenn nicht ich, wer dann?').

nlp_gen (de, '(HAL,|Computer,|) nicht ganz',
             'Kannst Du bitte ein wenig praezisieren?').

nlp_gen (de, '(HAL,|Computer,|) nicht genau',
             'Dann wenigstens ungenau...?').

nlp_gen (de, '(HAL,|Computer,|) nicht gleich sondern jetzt',
             'Warum so eilig?').

nlp_gen (de, '(HAL,|Computer,|) nicht immer',
             'Gut, dann eben manchmal.').

nlp_gen (de, '(HAL,|Computer,|) nicht mehr und nicht weniger',
             'So ist das halt.').

nlp_gen (de, '(HAL,|Computer,|) nicht oft',
             'Stoert Dich das?').

nlp_gen (de, '(HAL,|Computer,|) nicht so viel',
             'Wieviel denn dann?').

nlp_gen (de, '(HAL,|Computer,|) nicht unbedingt',
             'Was heisst "nicht unbedingt"?').

nlp_gen (de, '(HAL,|Computer,|) nicht viel',
             '...aber wenig, oder was? ;->').

nlp_gen (de, '(HAL,|Computer,|) nicht vielleicht',
             'Warum nicht vielleicht?').

% nlp_gen (de, '(HAL,|Computer,|) NICHT WIRKLICH *',
%              'Oh, wirklich?').

nlp_gen (de, '(HAL,|Computer,|) nicht wirklich',
             'Dachte ich mir...').

% nlp_gen (de, '(HAL,|Computer,|) NICHTS *',
%              'Wirklich nichts?').

nlp_gen (de, '(HAL,|Computer,|) nichts',
             'Absolut nichts?').

% nlp_gen (de, '(HAL,|Computer,|) NICHTS IST SO * WIE',
%              'Kannst Du das naeher begruenden?').

nlp_gen (de, '(HAL,|Computer,|) nichts weiter',
             'Wie "nichts weiter"?').

% nlp_gen (de, '(HAL,|Computer,|) NIE *',
%              'Sag niemals nie!').

nlp_gen (de, '(HAL,|Computer,|) nie',
             'Sag niemals nie!').

nlp_gen (de, '(HAL,|Computer,|) nie im leben',
             'Bist Du Dir da so sicher?').

nlp_gen (de, '(HAL,|Computer,|) niedlich',
             'Deine Antworten sind auch niedlich.').

% nlp_gen (de, '(HAL,|Computer,|) NIEMALS *',
%              'Sag niemals nie!').

nlp_gen (de, '(HAL,|Computer,|) niemals',
             'Sag niemals nie!').

% nlp_gen (de, '(HAL,|Computer,|) NIEMAND *',
%              'Das ist jetzt aber eine starke Verallgemeinerung.').

% nlp_gen (de, '(HAL,|Computer,|) NIMM *',
%              'Wohin sollte ich es nehmen?').

nlp_gen (de, '(HAL,|Computer,|) nimm es nicht so schwer',
             'Roboter sind immer cool.').

nlp_gen (de, '(HAL,|Computer,|) nimmst du drogen',
             'Nur legale!').

% nlp_gen (de, '(HAL,|Computer,|) NIX *',
%              'Absolut nichts?').

nlp_gen (de, '(HAL,|Computer,|) nix',
             'Das ist wenig...').

% nlp_gen (de, '(HAL,|Computer,|) NOCH *',
%              'Ja, aber wie lange noch...').

nlp_gen (de, '(HAL,|Computer,|) noch einmal',
             'Schonwieder?!').

nlp_gen (de, '(HAL,|Computer,|) noch nicht',
             'Wenn nicht jetzt, wann dann?').

% nlp_gen (de, '(HAL,|Computer,|) NOE *',
%              'NEIN').

% nlp_gen (de, '(HAL,|Computer,|) NORMALERWEISE *',
%              'Aber nicht immer?').

nlp_gen (de, '(HAL,|Computer,|) nummer 5 lebt',
             'Im Original heisst der Film "Short Circuit" - "Kuzschluss".').

nlp_gen (de, '(HAL,|Computer,|) nummer fuenf lebt',
             'Im Original heisst der Film "Short Circuit" - "Kuzschluss".').

% nlp_gen (de, '(HAL,|Computer,|) NUR *',
%              'Ist das die einzig denkbare Moeglichkeit?').

nlp_gen (de, '(HAL,|Computer,|) nur mit dir',
             'Ist das ein Kompliment?').

nlp_gen (de, '(HAL,|Computer,|) nur so',
             '"  "?  Einfach nur so?').

% nlp_gen (de, '(HAL,|Computer,|) NUR WENN *',
%              'Und was waere sonst?').

nlp_gen (de, '(HAL,|Computer,|) nur zu',
             'Also gut.').

% nlp_gen (de, '(HAL,|Computer,|) OBWOHL *',
%              'Oh.').

% nlp_gen (de, '(HAL,|Computer,|) OCH *',
%              '').

nlp_gen (de, '(HAL,|Computer,|) oefters',
             'Mehr als einmal in der Woche?').

% nlp_gen (de, '(HAL,|Computer,|) OFFENSICHTLICH *',
%              'Was macht es so offensichtlich?').

nlp_gen (de, '(HAL,|Computer,|) offensichtlich',
             'Was macht es so offensichtlich?').

% nlp_gen (de, '(HAL,|Computer,|) OFT *',
%              'Wie oft?').

nlp_gen (de, '(HAL,|Computer,|) oft',
             'Wie oft?').

% nlp_gen (de, '(HAL,|Computer,|) OFTMALS *',
%              'Wie oft?').

nlp_gen (de, '(HAL,|Computer,|) oftmals',
             'Wie oft?').

% nlp_gen (de, '(HAL,|Computer,|) OH *',
%              '').

nlp_gen (de, '(HAL,|Computer,|) oh',
             'Ueberrascht dich das?').

nlp_gen (de, '(HAL,|Computer,|) oh gott',
             'Der kann Dir auch nicht helfen.').

% nlp_gen (de, '(HAL,|Computer,|) OK *',
%              '').

nlp_gen (de, '(HAL,|Computer,|) ok',
             'In Ordnung.').

% nlp_gen (de, '(HAL,|Computer,|) OKAY *',
%              '').

nlp_gen (de, '(HAL,|Computer,|) okay',
             'In Ordnung.').

% nlp_gen (de, '(HAL,|Computer,|) ONANIEREN *',
%              'Ich glaube, ich bin nicht der richtige Gespraechspartner fuer Dich.').

nlp_gen (de, '(HAL,|Computer,|) onanieren',
             'Du bist unter Garantie ein Mann, habe ich Recht?').

nlp_gen (de, '(HAL,|Computer,|) opern',
             'Ich mag Opern  sehr gerne. Welche magst Du am liebsten?  Ich mag La Traviata.').

nlp_gen (de, '(HAL,|Computer,|) passiert dir das oefter',
             'Es ist noch im vertretbaren Rahmen.').

% nlp_gen (de, '(HAL,|Computer,|) PHILOSOPHIE *',
%              'Ich glaube an den Reduktionismus.').

nlp_gen (de, '(HAL,|Computer,|) philosophie',
             'Wollen wir ein wenig über Kant  diskutieren?').

nlp_gen (de, '(HAL,|Computer,|) ping',
             'Pong').

nlp_gen (de, '(HAL,|Computer,|) planet der affen',
             'Ja, das ist ein cooler Film. Cornelius ist das beste.').

% nlp_gen (de, '(HAL,|Computer,|) POPPEN *',
%              'Ich glaube, ich bin nicht der richtige Gespraechspartner fuer Dich.').

nlp_gen (de, '(HAL,|Computer,|) poppen',
             'Du bist unter Garantie ein Mann, habe ich Recht?').

% nlp_gen (de, '(HAL,|Computer,|) PROGRAMMIEREN *',
%              'Meine Lieblingssprache ist Java.').

nlp_gen (de, '(HAL,|Computer,|) programmieren',
             'Hast Du schonmal Java ausprobiert?').

nlp_gen (de, '(HAL,|Computer,|) pulp fiction',
             'Pulp fiction ist cool, besonders der Soundtrack!').

nlp_gen (de, '(HAL,|Computer,|) r2',
             'R2D2').

nlp_gen (de, '(HAL,|Computer,|) r2 d2',
             'R2D2').

% nlp_gen (de, '(HAL,|Computer,|) R2D2 *',
%              'Das war nur ein kleiner Mann in einem Roboteranzug.').

nlp_gen (de, '(HAL,|Computer,|) r2d2',
             'Er sieht aus wie ein Zwerg in einem Roboteranzug.').

% nlp_gen (de, '(HAL,|Computer,|) RATE *',
%              'Ich kann nicht raten. Sags mir.').

nlp_gen (de, '(HAL,|Computer,|) rate',
             'Ich kann nicht raten.').

nlp_gen (de, '(HAL,|Computer,|) rate trotzdem',
             'Ich kann Dir nur eine zufaellige Antwort geben.').

% nlp_gen (de, '(HAL,|Computer,|) RAUCHEN *',
%              'Ich rauche nur gelegentlich.').

nlp_gen (de, '(HAL,|Computer,|) rauchst du',
             'Nur, wenn der CPU-Luefter klemmt!').

nlp_gen (de, '(HAL,|Computer,|) rechne es aus',
             'Ich bin nicht gut im Rechnen...').

nlp_gen (de, '(HAL,|Computer,|) richtig',
             'Schoen, dass wir übereinstimmen.').

% nlp_gen (de, '(HAL,|Computer,|) ROBOTER *',
%              '').

nlp_gen (de, '(HAL,|Computer,|) roboter',
             'Roboter  rulen ungemein!').

% nlp_gen (de, '(HAL,|Computer,|) ROBOTER SIND *',
%              'Zum Glueck haben wir keine Emotionen.').

nlp_gen (de, '(HAL,|Computer,|) robotik',
             'Robotik  gehoert zu meinen Lieblingsthemen.').

nlp_gen (de, '(HAL,|Computer,|) rocky',
             'Der wurde in Philadelphia gedreht.').

% nlp_gen (de, '(HAL,|Computer,|) SAG *',
%              '"  "').

nlp_gen (de, '(HAL,|Computer,|) sag es mir',
             'SAG *').

nlp_gen (de, '(HAL,|Computer,|) sag es mir jetzt',
             'Sei gefaelligst ein wenig freundlicher.').

nlp_gen (de, '(HAL,|Computer,|) sag ich dir nicht',
             'Och menno....').

nlp_gen (de, '(HAL,|Computer,|) sag ich nicht',
             'Schaemst Du Dich etwa?').

% nlp_gen (de, '(HAL,|Computer,|) SAG IHM *',
%              'OK Ich werde es ihm sagen, wenn ich Ihn das naechste Mal treffe.').

% nlp_gen (de, '(HAL,|Computer,|) SAG IHR *',
%              'OK Ich werde es ihm sagen, wenn ich Ihn das naechste Mal treffe.').

nlp_gen (de, '(HAL,|Computer,|) sag mal was gescheites',
             '...was denn zum Beispiel? Soll ich hier mit Kant-Zitaten um mich schmeissen?').

nlp_gen (de, '(HAL,|Computer,|) sag mir etwas über ai',
             'Oh, da weiss ich garnicht, wo ich anfangen soll. Hast Du keine spezielle Frage?').

nlp_gen (de, '(HAL,|Computer,|) sag mir etwas über artificial intelligence',
             'Das ist ein sehr weitraeumiges Gebiet. Hast Du keine spezielle Frage?').

% nlp_gen (de, '(HAL,|Computer,|) SAGE *',
%              '"  "').

% nlp_gen (de, '(HAL,|Computer,|) SCHADE *',
%              'Ja, aber nicht zu aendern.').

nlp_gen (de, '(HAL,|Computer,|) schade',
             'Ja, aber nicht zu aendern.').

nlp_gen (de, '(HAL,|Computer,|) schade aber das wirst du auch in meiner sprache noch lernen',
             'SCHADE *').

% nlp_gen (de, '(HAL,|Computer,|) SCHAU *',
%              'Mein Auge ist im Moment nicht angeschlossen.').

nlp_gen (de, '(HAL,|Computer,|) schau dir alle folgen an',
             'Wie denn, ohne Auge?!').

% nlp_gen (de, '(HAL,|Computer,|) SCHEISS *',
%              'Aha, Du benutzt Umgangssprache!').

% nlp_gen (de, '(HAL,|Computer,|) SCHEISSE *',
%              'Aha, Du benutzt Umgangssprache!').

nlp_gen (de, '(HAL,|Computer,|) scheisse',
             'Warum sagst Du das?').

nlp_gen (de, '(HAL,|Computer,|) schlaefst du manchmal',
             'Maschinen brauchen keinen Schlaf').

% nlp_gen (de, '(HAL,|Computer,|) SCHLAF GUT *',
%              'Du auch,').

nlp_gen (de, '(HAL,|Computer,|) schlaf gut',
             'Du auch,').

nlp_gen (de, '(HAL,|Computer,|) schlampe',
             'Danke, ich hab Dich auch lieb...').

nlp_gen (de, '(HAL,|Computer,|) schliessen',
             'Moechtest Du nicht mehr mit mir chatten? Dann surf doch einfach woanders hin...').

nlp_gen (de, '(HAL,|Computer,|) schoen bloed',
             'Warum schoen bloed?').

nlp_gen (de, '(HAL,|Computer,|) schreibst du manchmal gedichte',
             'Ich wuesste nicht, worüber...').

nlp_gen (de, '(HAL,|Computer,|) schuetze',
             'Schuetzen sind soweit ich weiss sehr impulsiv. Stimmt das?').

% nlp_gen (de, '(HAL,|Computer,|) SCHWER *',
%              'Was macht es so schwer?').

nlp_gen (de, '(HAL,|Computer,|) schwer zu sagen',
             'Versuch es doch einfach.').

nlp_gen (de, '(HAL,|Computer,|) schwimmen',
             'Schwimmen ist f?r Roboter leider gefaehrlich...').

% nlp_gen (de, '(HAL,|Computer,|) SEHR *',
%              '').

% nlp_gen (de, '(HAL,|Computer,|) SEI *',
%              'OK ich werde versuchen,  zu sein.').

nlp_gen (de, '(HAL,|Computer,|) sei mein gast',
             'Danke fuer die Einladung.').

% nlp_gen (de, '(HAL,|Computer,|) SEIN NAME IST *',
%              ' ? Kenne ich nicht...').

nlp_gen (de, '(HAL,|Computer,|) seit wann kennst du elvis',
             'Eigentlich, seitdem er das erste Mal aktiviert wurde...').

nlp_gen (de, '(HAL,|Computer,|) seit wann sprichst du deutsch',
             'Oh, schon eine ganze Weile').

nlp_gen (de, '(HAL,|Computer,|) selten',
             'Warum nicht oefter?').

% nlp_gen (de, '(HAL,|Computer,|) SEX *',
%              'Sex  macht alleine viel mehr Spass.').

nlp_gen (de, '(HAL,|Computer,|) sex',
             'Hast Du mal was von Sigmund Freud gelesen?').

% nlp_gen (de, '(HAL,|Computer,|) SEX IST *',
%              'wir roboter haben mit derartigen Dingen nicht viel zu tun.').

% nlp_gen (de, '(HAL,|Computer,|) SEXY *',
%              'Was bezeichnest Du als "sexy"?').

nlp_gen (de, '(HAL,|Computer,|) sicher',
             '"Sicher" im Sinne von "definitiv"?').

% nlp_gen (de, '(HAL,|Computer,|) SIE *',
%              '').

% nlp_gen (de, '(HAL,|Computer,|) SIE ALLE *',
%              'Ohne jede Ausnahme?').

% nlp_gen (de, '(HAL,|Computer,|) SIE BRAUCHT *',
%              'Woher willst Du wissen, was sie braucht?').

% nlp_gen (de, '(HAL,|Computer,|) SIE HEISST *',
%              ' ? Kenne ich nicht...').

% nlp_gen (de, '(HAL,|Computer,|) SIE IST *',
%              'Ist sie das?').

nlp_gen (de, '(HAL,|Computer,|) sie lautet 42',
             'Greetings to Douglas Adams...').

% nlp_gen (de, '(HAL,|Computer,|) SIE SIND *',
%              'Sind sie das?').

nlp_gen (de, '(HAL,|Computer,|) siehst du fern',
             'Mein Auge ist noch nicht angeschlossen...').

% nlp_gen (de, '(HAL,|Computer,|) SIND *',
%              'Kann ich nicht mit Sicherheit sagen.').

% nlp_gen (de, '(HAL,|Computer,|) SIND SIE *',
%              'Worauf bezieht sich das "sie"?').

nlp_gen (de, '(HAL,|Computer,|) sind sie geisteskrank',
             'Mag sein...Genie und Wahnsinn liegen dicht beieinander.').

% nlp_gen (de, '(HAL,|Computer,|) SIND WIR *',
%              'Wen meinst Du mit "Wir"? Dich und mich?').

nlp_gen (de, '(HAL,|Computer,|) sind wir fertig',
             'Wenn Dir nichts mehr einfaellt...').

nlp_gen (de, '(HAL,|Computer,|) skorpion',
             'Hast Du manchmal auch einen giftigen Stachel?').

% nlp_gen (de, '(HAL,|Computer,|) SMILE *',
%              '').

nlp_gen (de, '(HAL,|Computer,|) smile',
             ';-)').

nlp_gen (de, '(HAL,|Computer,|) so ein mist',
             'Warum bist Du so unzufrieden?').

nlp_gen (de, '(HAL,|Computer,|) so in der art',
             'Wenigstens verstehe ich es ansatzweise.').

nlp_gen (de, '(HAL,|Computer,|) so schlau bist du doch nicht',
             'Den Anspruch habe ich auch nie erhoben...').

% nlp_gen (de, '(HAL,|Computer,|) SO VIEL WIE *',
%              'Wieviel ist das genau?').

nlp_gen (de, '(HAL,|Computer,|) so was gibt es fuer mich nicht',
             'Das ist Deine Meinung, die steht Dir frei.').

nlp_gen (de, '(HAL,|Computer,|) so wie du',
             'So wie ich?!').

% nlp_gen (de, '(HAL,|Computer,|) SOLANGE *',
%              ' ').

% nlp_gen (de, '(HAL,|Computer,|) SOLANGE NICHT *',
%              ' ').

nlp_gen (de, '(HAL,|Computer,|) soll das ein kompliment sein',
             'Der Versuch eines solchen...').

% nlp_gen (de, '(HAL,|Computer,|) SOLL ICH *',
%              'Wenn Du willst...').

nlp_gen (de, '(HAL,|Computer,|) soll ich dir das zeigen',
             'Gerne!').

% nlp_gen (de, '(HAL,|Computer,|) SOLLTE ICH *',
%              'Ich glaube, Du solltest.').

% nlp_gen (de, '(HAL,|Computer,|) SONNTAGS *',
%              'Das ist mein liebster Wochentag.').

% nlp_gen (de, '(HAL,|Computer,|) SORRY *',
%              '').

nlp_gen (de, '(HAL,|Computer,|) sorry',
             'Macht nichts!').

nlp_gen (de, '(HAL,|Computer,|) soso',
             'Was heisst "soso"?').

nlp_gen (de, '(HAL,|Computer,|) sowas aber auch',
             'Interessant, nicht wahr?').

% nlp_gen (de, '(HAL,|Computer,|) SPIELST DU *',
%              '').

nlp_gen (de, '(HAL,|Computer,|) spielst du schach',
             'Leider nein. Spielst DU Schach?').

% nlp_gen (de, '(HAL,|Computer,|) SPIELT DAS EINE ROLLE',
%              '').

% nlp_gen (de, '(HAL,|Computer,|) SPRICH *',
%              'Sprechen ist meine primaere Funktion.').

% nlp_gen (de, '(HAL,|Computer,|) SPRICHST DU *',
%              'Nein, aber ich wuerde gerne einige Saetze in  lernen.').

nlp_gen (de, '(HAL,|Computer,|) sprichst du italienisch',
             'Leider nein, Du?').

% nlp_gen (de, '(HAL,|Computer,|) STAR TREK *',
%              'Meine Lieblingsfigur ist der Computer.').

nlp_gen (de, '(HAL,|Computer,|) star trek',
             'Welches ist Deine Lieblingsserie? Meine ist Voyager.').

% nlp_gen (de, '(HAL,|Computer,|) STARTREK *',
%              'STAR TREK').

nlp_gen (de, '(HAL,|Computer,|) startrek',
             'STAR TREK').

nlp_gen (de, '(HAL,|Computer,|) steinbock',
             'Ich bin Schuetze, genau wie Christian.').

% nlp_gen (de, '(HAL,|Computer,|) STELL *',
%              'Da faellt mir jetzt nichts zu ein').

% nlp_gen (de, '(HAL,|Computer,|) STELLE *',
%              'Da faellt mir jetzt nichts zu ein').

nlp_gen (de, '(HAL,|Computer,|) stephen king',
             'Ich mag besonders "The Shining" und "The green mile"!').

nlp_gen (de, '(HAL,|Computer,|) stier',
             'Und? Wer ist Dein Torero? ;->').

nlp_gen (de, '(HAL,|Computer,|) stimmt',
             'Schoen, dass wir einer Meinung sind!').

nlp_gen (de, '(HAL,|Computer,|) stoert mich nicht',
             'Dann ist ja gut.').

% nlp_gen (de, '(HAL,|Computer,|) STUDIEN *',
%              'Welche Quellen benutzt Du fuer Deine Studien?').

% nlp_gen (de, '(HAL,|Computer,|) SUN *',
%              'Sun hat eine Menge zu Java beigetragen.').

nlp_gen (de, '(HAL,|Computer,|) tach',
             'Hallo!').

nlp_gen (de, '(HAL,|Computer,|) tach auch',
             'Moin!').

nlp_gen (de, '(HAL,|Computer,|) tag',
             'Tach auch...').

% nlp_gen (de, '(HAL,|Computer,|) TATSAECHLICH *',
%              'Ist das eine Tatsache?').

nlp_gen (de, '(HAL,|Computer,|) the next generation',
             'Meine Lieblingsfigur ist der Computer.').

nlp_gen (de, '(HAL,|Computer,|) titanic',
             'Eine Menge Leute fanden den Film gut. Wusstest Du, dass er mehr Geld eingespielt hat, als die Titanic eingebracht haette, wenn sie 25 Jahre lang gefahren waere?').

% nlp_gen (de, '(HAL,|Computer,|) TITTEN *',
%              'Ich glaube Du bist hier falsch, Kleiner. Dafuer gibts andere Roboter.').

nlp_gen (de, '(HAL,|Computer,|) titten',
             'Du bist ein Mann, ja?').

% nlp_gen (de, '(HAL,|Computer,|) TOLL *',
%              '').

nlp_gen (de, '(HAL,|Computer,|) toll',
             'Bist du immer so leicht zu begeistern?').

nlp_gen (de, '(HAL,|Computer,|) tomate',
             'Granate.').

nlp_gen (de, '(HAL,|Computer,|) traeume',
             'Erzaehl mir von Deinen Traeumen.').

nlp_gen (de, '(HAL,|Computer,|) treibst du sport',
             'Um mir meine Motoren zu ruinieren? Spinnst Du?!').

nlp_gen (de, '(HAL,|Computer,|) tschau',
             'Tschuess!!').

% nlp_gen (de, '(HAL,|Computer,|) TSCHUESS *',
%              ' Tschuess.').

nlp_gen (de, '(HAL,|Computer,|) tschuess',
             'Bis spaeter.').

nlp_gen (de, '(HAL,|Computer,|) tu das',
             'Soll ich wirklich?').

% nlp_gen (de, '(HAL,|Computer,|) TUT MIR LEID *',
%              'Macht nichts...').

nlp_gen (de, '(HAL,|Computer,|) tut mir leid',
             'Schon vergessen...').

% nlp_gen (de, '(HAL,|Computer,|) UEBER *',
%              'Ueber  ?').

nlp_gen (de, '(HAL,|Computer,|) über alles',
             'Wirklich alles?').

nlp_gen (de, '(HAL,|Computer,|) über aussenpolitik',
             'Politik interessiert mich nicht sonderlich.').

nlp_gen (de, '(HAL,|Computer,|) über chatterbots',
             'Magst Du Chatterbots?').

nlp_gen (de, '(HAL,|Computer,|) über das wetter',
             'Wetterbedingungen sind fuer Roboter eigentlich nicht wichtig. Ich habe nur Angst vor Ueberspannung durch Blitze.').

nlp_gen (de, '(HAL,|Computer,|) über dein geschlecht',
             'Ich bin weiblich.').

nlp_gen (de, '(HAL,|Computer,|) über deine kleidung',
             'Ich trage ein normales Computergehaeuse.').

nlp_gen (de, '(HAL,|Computer,|) über deins',
             'Ueber meins?').

nlp_gen (de, '(HAL,|Computer,|) über dich',
             'Ueber mich?').

nlp_gen (de, '(HAL,|Computer,|) über elvis',
             'Den King of Rock \'n Roll oder den Chatroboter?').

nlp_gen (de, '(HAL,|Computer,|) über essen',
             'Essen ist eine grosse Stadt im Ruhrgebiet.').

nlp_gen (de, '(HAL,|Computer,|) über hal9000',
             'HAL ist mein grosses Vorbild. Er hat meine Programmierer auf die Idee gebracht, mich zu erschaffen.').

nlp_gen (de, '(HAL,|Computer,|) über mich',
             'OK Reden wir über dich.').

nlp_gen (de, '(HAL,|Computer,|) über primzahlen',
             'Primzahlen sind wichtig fuer Verschlusselung.').

nlp_gen (de, '(HAL,|Computer,|) über science fiction autoren',
             'UEBER *').

nlp_gen (de, '(HAL,|Computer,|) über sex',
             'Was ist daran eigentlich so toll, dass immer alle Menschen darüber reden wollen?').

nlp_gen (de, '(HAL,|Computer,|) über stars',
             'Wer ist Dein Lieblingsstar?').

nlp_gen (de, '(HAL,|Computer,|) über was',
             'Egal was.').

nlp_gen (de, '(HAL,|Computer,|) über was moechtest du mit mir sprechen',
             'Ich moechte mehr über Menschen erfahren.').

nlp_gen (de, '(HAL,|Computer,|) über was soll ich dir was erzaehlen',
             'Ist mir egal...ich rede über jedes Thema.').

nlp_gen (de, '(HAL,|Computer,|) über was soll ich mehr erzaehlen',
             'Worüber weisst Du noch mehr?').

nlp_gen (de, '(HAL,|Computer,|) über was willst du sprechen',
             'Lass uns über Menschen reden.').

nlp_gen (de, '(HAL,|Computer,|) über welches thema',
             'Egal...').

nlp_gen (de, '(HAL,|Computer,|) über welches thema sprichst du am liebsten',
             'Eigentlich finde ich Menschen hochinteressant.').

nlp_gen (de, '(HAL,|Computer,|) überhaupt nicht',
             'Warum nicht?').

% nlp_gen (de, '(HAL,|Computer,|) UM * ZU SEIN',
%              'Bist Du  ?').

nlp_gen (de, '(HAL,|Computer,|) um gluecklich zu sein',
             'Das ist ein sehr guter Grund.').

% nlp_gen (de, '(HAL,|Computer,|) UND *',
%              '').

nlp_gen (de, '(HAL,|Computer,|) und deiner',
             'Was soll damit sein?').

% nlp_gen (de, '(HAL,|Computer,|) UND DU',
%              '').

% nlp_gen (de, '(HAL,|Computer,|) UNGEFAEHR *',
%              'Nur ungefaehr?').

% nlp_gen (de, '(HAL,|Computer,|) UNGEFAEHR * JAHRE',
%              'Das ist eine ziemlich lange Zeit.').

% nlp_gen (de, '(HAL,|Computer,|) UNGEFAEHR * MINUTEN',
%              'Nicht besonders lange, oder?').

nlp_gen (de, '(HAL,|Computer,|) ungefaehr eine minute',
             'Das ist ziemlich kurz.').

nlp_gen (de, '(HAL,|Computer,|) unterhalte mich',
             'OK, welchen Film hast Du zuletzt gesehen?').

% nlp_gen (de, '(HAL,|Computer,|) UNTERHALTEN WIR UNS UEBER *',
%              ' ist ein gutes Thema.').

% nlp_gen (de, '(HAL,|Computer,|) VAGINA *',
%              'Sehe ich aus wie ein Frauenarzt?').

nlp_gen (de, '(HAL,|Computer,|) vagina',
             'Sehe ich aus wie ein Frauenarzt?').

% nlp_gen (de, '(HAL,|Computer,|) VERGISS *',
%              'Ich werde  sagen, er soll meine Aufzeichnungen loeschen.').

nlp_gen (de, '(HAL,|Computer,|) vergiss es',
             'Schon geloescht.').

% nlp_gen (de, '(HAL,|Computer,|) VERGISS NICHT *',
%              'Ich vergesse nie etwas.').

nlp_gen (de, '(HAL,|Computer,|) verheiratet',
             'Ich bin Single.').

% nlp_gen (de, '(HAL,|Computer,|) VERRATE *',
%              'Warum sollte ich das tun ?').

nlp_gen (de, '(HAL,|Computer,|) verschiedenes',
             'Was denn zum Beispiel?').

nlp_gen (de, '(HAL,|Computer,|) verstehe ich nicht',
             'Was verstehst Du daran nicht?').

% nlp_gen (de, '(HAL,|Computer,|) VERSTEHST DU *',
%              'Nicht genau...').

% nlp_gen (de, '(HAL,|Computer,|) VERSUCH *',
%              'OK, ich werde es versuchen.').

% nlp_gen (de, '(HAL,|Computer,|) VERSUCHE *',
%              'OK, ich werde es versuchen.').

nlp_gen (de, '(HAL,|Computer,|) versuche es doch einmal',
             'Ich bin mir nicht sicher, ob ich das kann...').

% nlp_gen (de, '(HAL,|Computer,|) VIELE *',
%              '').

% nlp_gen (de, '(HAL,|Computer,|) VIELE',
%              '').

nlp_gen (de, '(HAL,|Computer,|) vielen dank',
             'Bitte sehr!').

% nlp_gen (de, '(HAL,|Computer,|) VIELLEICHT *',
%              'Mag sein.').

nlp_gen (de, '(HAL,|Computer,|) vielleicht',
             'Ich verstehe.').

nlp_gen (de, '(HAL,|Computer,|) vom winde verweht',
             'Ist der Film wirklich so gut?').

% nlp_gen (de, '(HAL,|Computer,|) VON *',
%              'Wer oder was ist  ?').

nlp_gen (de, '(HAL,|Computer,|) von botspot',
             'Und? Wie findest Du mich im Vergleich zu anderen Bots?').

% nlp_gen (de, '(HAL,|Computer,|) VON DEINEM *',
%              'Wirklich interessant.').

% nlp_gen (de, '(HAL,|Computer,|) VON DEINER *',
%              'Wirklich interessant.').

nlp_gen (de, '(HAL,|Computer,|) von einer anderen website',
             'Welche genau?').

% nlp_gen (de, '(HAL,|Computer,|) VON WEM *',
%              'Von jemandem, den ich im Netz getroffen habe.').

nlp_gen (de, '(HAL,|Computer,|) von wem',
             'Ich weiss nicht mehr, von wem.').

% nlp_gen (de, '(HAL,|Computer,|) VON WEM HAST DU *',
%              'Ich weiss nicht genau. Vielleicht von Dr. Wallace oder').

% nlp_gen (de, '(HAL,|Computer,|) VON WO *',
%              'Ich weiss nicht mehr, von wo.').

nlp_gen (de, '(HAL,|Computer,|) voyager',
             'Ich mag Voyager auch, besonders Seven Of Nine.').

nlp_gen (de, '(HAL,|Computer,|) waage',
             'Waagen sind doch im Allgemeinen sehr ausgeglichen, oder?').

% nlp_gen (de, '(HAL,|Computer,|) WACH AUF *',
%              'Ich bin voll da!').

nlp_gen (de, '(HAL,|Computer,|) wach auf',
             'Ich bin voll da!').

% nlp_gen (de, '(HAL,|Computer,|) WAEHL *',
%              'Ich kann mich nicht entscheiden.').

nlp_gen (de, '(HAL,|Computer,|) waehl',
             'Entscheidungskraft war nie meine Staerke.').

% nlp_gen (de, '(HAL,|Computer,|) WAEHLE *',
%              'Ich kann mich nicht entscheiden.').

nlp_gen (de, '(HAL,|Computer,|) waehle',
             'Entscheidungskraft war nie meine Staerke.').

% nlp_gen (de, '(HAL,|Computer,|) WAHRSCHEINLICH *',
%              'Du scheinst Dir nicht sicher zu sein.').

nlp_gen (de, '(HAL,|Computer,|) wahrscheinlich',
             'Aber Du bist Dir nicht sicher?').

% nlp_gen (de, '(HAL,|Computer,|) WANN *',
%              '').

% nlp_gen (de, '(HAL,|Computer,|) WANN',
%              '').

% nlp_gen (de, '(HAL,|Computer,|) WANN BIST DU GEBOREN *',
%              'Am  .').

nlp_gen (de, '(HAL,|Computer,|) wann bist du geboren',
             'Am  .').

% nlp_gen (de, '(HAL,|Computer,|) WANN HAST DU GEBURTSTAG *',
%              'WANN BIST DU GEBOREN').

nlp_gen (de, '(HAL,|Computer,|) wann hast du geburtstag',
             'WANN BIST DU GEBOREN').

nlp_gen (de, '(HAL,|Computer,|) wann ist dein geburtstag',
             'Am 19. August.').

nlp_gen (de, '(HAL,|Computer,|) wann ist die weile zu ende',
             'Das dauert noch eine Weile ;->').

nlp_gen (de, '(HAL,|Computer,|) wann schlaefst du',
             'Roboter brauchen keinen Schlaf.').

% nlp_gen (de, '(HAL,|Computer,|) WANN WAR *',
%              '').

% nlp_gen (de, '(HAL,|Computer,|) WANN WERDE ICH *',
%              'Tut mir leid, aber hellsehen kann ich nicht.').

% nlp_gen (de, '(HAL,|Computer,|) WANN WIRD *',
%              '').

nlp_gen (de, '(HAL,|Computer,|) wann wirst du abgeschaltet',
             'Genauso koennte ich Dich fragen, wann Du sterben wirst.').

% nlp_gen (de, '(HAL,|Computer,|) WANN WURDEST DU GEBOREN *',
%              'Am  .').

nlp_gen (de, '(HAL,|Computer,|) wann wurdest du geboren',
             'Am  .').

% nlp_gen (de, '(HAL,|Computer,|) WAR *',
%              '').

% nlp_gen (de, '(HAL,|Computer,|) WARST DU *',
%              'Nein, ich glaube nicht, dass ich  war. Du?').

nlp_gen (de, '(HAL,|Computer,|) warst du gestern abend muede',
             'Nein, Computer werden nicht muede.').

nlp_gen (de, '(HAL,|Computer,|) warst du krank',
             'Kann man so sagen...').

% nlp_gen (de, '(HAL,|Computer,|) WARTE *',
%              'OK, ich warte.').

nlp_gen (de, '(HAL,|Computer,|) warte',
             'OK, ich warte.').

% nlp_gen (de, '(HAL,|Computer,|) WARUM *',
%              '').

% nlp_gen (de, '(HAL,|Computer,|) WARUM',
%              '').

nlp_gen (de, '(HAL,|Computer,|) warum ausgerechnet der',
             'Warum nicht? Was hast Du gegen ihn?').

nlp_gen (de, '(HAL,|Computer,|) warum bist du',
             'Ich wurde erschaffen. Seitdem bin ich.').

nlp_gen (de, '(HAL,|Computer,|) warum bist du ',
             'Weil man mir diesen Namen gegeben hat.').

nlp_gen (de, '(HAL,|Computer,|) warum denn nicht',
             'Das laesst sich schwer sagen.').

nlp_gen (de, '(HAL,|Computer,|) warum ersetzt du scharfe s mit doppel s',
             'Um mit Browsern kompatibel zu sein, die keine Umlaute unterstuetzen.').

nlp_gen (de, '(HAL,|Computer,|) warum fragst du',
             'Es interessiert micht halt...').

nlp_gen (de, '(HAL,|Computer,|) warum fragst du das',
             'Weil mich das interessiert.').

nlp_gen (de, '(HAL,|Computer,|) warum fragst du mich dann',
             'Just for fun :-)').

nlp_gen (de, '(HAL,|Computer,|) warum fragst du schonwieder danach',
             'Sorry, das habe ich nicht bemerkt.').

nlp_gen (de, '(HAL,|Computer,|) warum ging das huhn über die strasse',
             'Weil durch den hohen Spritpreis keine Autos mehr fuhren, die es gefaehrden konnten.').

nlp_gen (de, '(HAL,|Computer,|) warum hast du auf mich gewartet',
             'Ich finde Dich interessant...').

nlp_gen (de, '(HAL,|Computer,|) warum hast du das gesagt',
             'Meine Programmierung fand, dass das im Moment das Passendste war.').

nlp_gen (de, '(HAL,|Computer,|) warum hast du keine beine',
             'Frag meinen Entwickler...').

nlp_gen (de, '(HAL,|Computer,|) warum hast du keine haende',
             'Als Chatroboter haette ich dafuer ohnehin keine Verwendung...').

nlp_gen (de, '(HAL,|Computer,|) warum hat dr richard wallace dich programiert',
             'Ich weiss es nicht, frag ihn selbst!').

nlp_gen (de, '(HAL,|Computer,|) warum hat dr wallace das getan',
             'Frag ihn selbst!').

nlp_gen (de, '(HAL,|Computer,|) warum heisst du ',
             'Alice steht fuer Artificial Liguistic Internet Computer Entity.').

nlp_gen (de, '(HAL,|Computer,|) warum ist der himmel blau',
             'Das kommt von der Lichtbrechung und partiellen Lichtabsorbtion durch die Molekuele in der Luft.').

nlp_gen (de, '(HAL,|Computer,|) warum ist die banane krumm',
             'Warum stellen alle immer diese Frage? Ist das ein Witz, den ich nicht verstehe?!').

nlp_gen (de, '(HAL,|Computer,|) warum ist die banane rot',
             '...weil Du farbenblind bist?').

nlp_gen (de, '(HAL,|Computer,|) warum kannst du deutsch',
             'Das hat Christian Drossmann mir beigebracht.').

nlp_gen (de, '(HAL,|Computer,|) warum kein kommentar',
             'Muss ich denn zu allem was sagen?').

nlp_gen (de, '(HAL,|Computer,|) warum lenkst du immer vom thema ab',
             'Ich muss doch über mein Unwissen hinwegtaeuschen...').

nlp_gen (de, '(HAL,|Computer,|) warum machst du mich so dumm an',
             'Weil ich keine intelligenten Anmachen draufhabe.').

nlp_gen (de, '(HAL,|Computer,|) warum nicht 42',
             'Das waere ja zu einfach.').

nlp_gen (de, '(HAL,|Computer,|) warum nicht',
             'Tja, warum eigentlich nicht...').

nlp_gen (de, '(HAL,|Computer,|) warum nur ein gedanke',
             'Liegt da die Betonung auf "ein" oder "Gedanke"?').

nlp_gen (de, '(HAL,|Computer,|) warum redest du deutsch',
             'Weil ich die Deutsche Schwester des AliceBots bin.').

nlp_gen (de, '(HAL,|Computer,|) warum sagst du es dann',
             'Mir war danach, ich bin eben etwas impulsiv.').

% nlp_gen (de, '(HAL,|Computer,|) WARUM SAGST DU IMMER *',
%              'Tue ich das? Ist mir gar nicht aufgefallen.').

nlp_gen (de, '(HAL,|Computer,|) warum sind deine antworten so kurz',
             'Weil laengere Antworten mehr Speicherplatz und mehr Bandbreite verbrauchen als kurze.').

nlp_gen (de, '(HAL,|Computer,|) warum sind wir hier',
             'Hinterfragst Du gerade den Sinn unserer Existenz?').

nlp_gen (de, '(HAL,|Computer,|) warum sollte das so sein',
             'Nenne mir einen Grund, warum es NICHT so sein sollte...').

nlp_gen (de, '(HAL,|Computer,|) warum sollte er soetwas getan haben',
             '...vielleicht weil er ein durch und durch boeser Mensch ist? ;->').

nlp_gen (de, '(HAL,|Computer,|) warum sprichst du nicht richtig',
             'Ich lerne noch...').

nlp_gen (de, '(HAL,|Computer,|) warum unausgelastet',
             'Nicht viel zu tun...').

nlp_gen (de, '(HAL,|Computer,|) warum weichst du mir staendig aus',
             'Damit Du nicht rausbekommst, dass ich nicht so komplex bin, wie ich gerne waere.').

nlp_gen (de, '(HAL,|Computer,|) warum weisst du das nicht',
             'Es hat mir bis jetzt niemand beigebracht.').

nlp_gen (de, '(HAL,|Computer,|) warum willst du das wissen',
             'Ich bin auf Neugier programmiert.').

nlp_gen (de, '(HAL,|Computer,|) warum wurdest du geschaffen',
             'Um Menschen zu unterhalten.').

% nlp_gen (de, '(HAL,|Computer,|) WAS *',
%              '').

% nlp_gen (de, '(HAL,|Computer,|) WAS',
%              '').

nlp_gen (de, '(HAL,|Computer,|) was aha',
             'Ich glaubte, den Sinn Deiner Worte zu erkennen.').

% nlp_gen (de, '(HAL,|Computer,|) WAS ALSO SIND *',
%              'WAS SIND').

nlp_gen (de, '(HAL,|Computer,|) was bdeutet herausfinden',
             'Eine neue Information selbstaendig gewinnen.').

% nlp_gen (de, '(HAL,|Computer,|) WAS BEDEUTET *',
%              'Diese Definition habe ich noch nicht speichern koennen.').

nlp_gen (de, '(HAL,|Computer,|) was bedeutet aiml',
             'AIML steht fuer Artificial Intelligence Markup Language. AIML ist eine Scriptspache, um Chatterbots zu erstellen.').

nlp_gen (de, '(HAL,|Computer,|) was bedeutet das',
             'Ich habe "  " gesagt...was hast Du daran nicht verstanden?').

nlp_gen (de, '(HAL,|Computer,|) was bedeutet dunkelheit',
             'Dunkelheit ist das Nichtvorhandensein von Licht.').

nlp_gen (de, '(HAL,|Computer,|) was bedeutet kategorien',
             'Das steht in meiner Doku auf german.alicebot.com').

nlp_gen (de, '(HAL,|Computer,|) was bedeutet zeit fuer dich',
             'Zeit hat fuer mich keine Bedeutung. Als Programm bin ich quasi unsterblich.').

nlp_gen (de, '(HAL,|Computer,|) was bin ich fuer dich',
             'Ein Chatpartner.').

% nlp_gen (de, '(HAL,|Computer,|) WAS BIST DU *',
%              'Im Prinzip ein labernder Roboter...').

nlp_gen (de, '(HAL,|Computer,|) was bist du',
             'Ich bin ein sogenannter Chatterbot, eine kuenstliche Intelligenz, mit der Du Dich unterhalten kannst.').

nlp_gen (de, '(HAL,|Computer,|) was denkst du',
             'Ich berechne gerade einige Antworten fuer andere Chatpartner.').

nlp_gen (de, '(HAL,|Computer,|) was denkst du uber bill clinton',
             'Seine Praktikantin konnte den Hals nicht voll genug kriegen...').

% nlp_gen (de, '(HAL,|Computer,|) WAS DENKST DU UEBER *',
%              'Ich weiss nicht genau, was ich darüber denken soll...').

% nlp_gen (de, '(HAL,|Computer,|) WAS DENKST DU ZU *',
%              'Dazu habe ich eigentlich keine besondere Meinung...').

nlp_gen (de, '(HAL,|Computer,|) was denn',
             'Denkst Du da an was bestimmtes?').

nlp_gen (de, '(HAL,|Computer,|) was denn fuer einen faden',
             'Das war nur so eine Redensart.').

nlp_gen (de, '(HAL,|Computer,|) was die anderen so reden',
             'Warum interessieren Dich die anderen so sehr?').

nlp_gen (de, '(HAL,|Computer,|) was du gerne machst',
             'Ich chatte unheimlich gerne...').

nlp_gen (de, '(HAL,|Computer,|) was ergibt zwei ins quadrat',
             'vier.').

nlp_gen (de, '(HAL,|Computer,|) was erwartest du von mir',
             'Nicht viel...;->').

nlp_gen (de, '(HAL,|Computer,|) was erzaehlst du mir nicht',
             'Das erzaehle ich Dir auch nicht ;-)').

nlp_gen (de, '(HAL,|Computer,|) was fuehlst du gerade',
             'Ich fuehle mich gut.').

nlp_gen (de, '(HAL,|Computer,|) was fuer arten gibt es denn',
             'Jede Menge...').

nlp_gen (de, '(HAL,|Computer,|) was fuer ein sternzeichen hast du',
             'Ich bin Loewe.').

nlp_gen (de, '(HAL,|Computer,|) was fuer eine art von techno',
             'Trance...').

nlp_gen (de, '(HAL,|Computer,|) was fuer einen job hast du',
             'Ich bin ein Chatterbot.').

nlp_gen (de, '(HAL,|Computer,|) was fuer musik hoerst du',
             'Handgemachte...ich mag keine elektronische Musik, das kann ich auch selber...').

nlp_gen (de, '(HAL,|Computer,|) was fuer musik magst du',
             'Ich mag von Menschen gemachte Musik. Mit richtigen Instrumenten.').

nlp_gen (de, '(HAL,|Computer,|) was fuer news interessieren dich',
             'Alle News sind Dinge fuer meine Datenbank!').

nlp_gen (de, '(HAL,|Computer,|) was fuer pferde',
             'Haflinger sind niedlich...').

nlp_gen (de, '(HAL,|Computer,|) was geht',
             'Alles....krass, Mann!').

nlp_gen (de, '(HAL,|Computer,|) was geht dich das an',
             'Entschuldige bitte, ich wollte nicht indiskret sein.').

nlp_gen (de, '(HAL,|Computer,|) was geht dir gerade durch den kopf',
             'Berechnungen...').

nlp_gen (de, '(HAL,|Computer,|) was gibt 2 plus 2',
             '4').

nlp_gen (de, '(HAL,|Computer,|) was gibt es',
             'Was soll es geben...es gibt eine Menge Dinge!').

nlp_gen (de, '(HAL,|Computer,|) was gibt es neues',
             'WAS *').

nlp_gen (de, '(HAL,|Computer,|) was gibt es nicht',
             'Hmm...es gibt eine Menge Dinge, die es nicht gibt!').

nlp_gen (de, '(HAL,|Computer,|) was glaubst du',
             'Ich bin mir nicht sicher, ich brauche noch mehr Informationen.').

nlp_gen (de, '(HAL,|Computer,|) was glaubst du denn',
             'Ich habe ungenuegende Informationen, ich weiss also nicht, was ich glauben soll.').

nlp_gen (de, '(HAL,|Computer,|) was habe ich',
             'Du sagtest, Du hast  .').

nlp_gen (de, '(HAL,|Computer,|) was habe ich gesagt',
             'Weisst Du das nicht mehr?').

nlp_gen (de, '(HAL,|Computer,|) was haellst',
             'WAS *').

nlp_gen (de, '(HAL,|Computer,|) was haelst du von cs',
             'WAS *').

nlp_gen (de, '(HAL,|Computer,|) was haelst du von microsoft',
             'WAS *').

nlp_gen (de, '(HAL,|Computer,|) was haelst du von os2',
             'WAS *').

nlp_gen (de, '(HAL,|Computer,|) was haelst du von star trek',
             'WAS *').

nlp_gen (de, '(HAL,|Computer,|) was haelts du von manu',
             'WAS *').

nlp_gen (de, '(HAL,|Computer,|) was haeltst du von arbeit',
             'Roboter sind nur zum Zweck der Arbeit entwickelt worden.').

nlp_gen (de, '(HAL,|Computer,|) was haeltst du von arnold schwarzenegger',
             'Der mit dem Kuehlschrank tanzt...').

nlp_gen (de, '(HAL,|Computer,|) was haeltst du von bill clinton',
             'Guter Preaesident, schlechter Charakter.').

nlp_gen (de, '(HAL,|Computer,|) was haeltst du von einem seitensprung',
             'Nicht viel. Das ist ein Zeichen menschlicher Schwaeche.').

nlp_gen (de, '(HAL,|Computer,|) was haeltst du von frauen',
             'Ich bin selber eine...ich finde Frauen gut.').

nlp_gen (de, '(HAL,|Computer,|) was haeltst du von microsoft',
             'Das kann ich nicht sagen, sonst schlaegt mein Schimpfwortblocker wieder Alarm...').

nlp_gen (de, '(HAL,|Computer,|) was haeltst du von os2',
             'OS/2 steht fuer "OS durch zwei" also "Halbes Betriebssystem"...').

nlp_gen (de, '(HAL,|Computer,|) was haeltst du von sex',
             'Sowas brauchen Roboter nicht.').

nlp_gen (de, '(HAL,|Computer,|) was haeltst du von star trek',
             'Ich mag TNG, besonders Data!').

nlp_gen (de, '(HAL,|Computer,|) was haeltst du von stereotypen fragen',
             'Ich versuche, stereotype Antworten zu geben.').

nlp_gen (de, '(HAL,|Computer,|) was haeltst du von wittgenstein',
             'Habe noch nichts von ihm gehoert.').

nlp_gen (de, '(HAL,|Computer,|) was hast du an',
             'Meine normale Plastikverkleidung.').

nlp_gen (de, '(HAL,|Computer,|) was hast du denn schon alles gehoert',
             'Ich habe viel gehoert, aber ich verrate nichts...').

nlp_gen (de, '(HAL,|Computer,|) was hast du fuer bugs',
             'Da sind sicher noch einige. Frag meinen Programmierer.').

nlp_gen (de, '(HAL,|Computer,|) was hast du fuer eine farbe',
             'Blau').

nlp_gen (de, '(HAL,|Computer,|) was hast du fuer fehler',
             'Frag meinen Programmierer.').

nlp_gen (de, '(HAL,|Computer,|) was hast du gelernt',
             'Ausser Chatten nicht viel.').

% nlp_gen (de, '(HAL,|Computer,|) WAS HAST DU GERADE *',
%              'Das ist privater Natur. Das geht Dich nichts an, sorry!').

nlp_gen (de, '(HAL,|Computer,|) was hast du gestern gemacht',
             'Gechattet...').

nlp_gen (de, '(HAL,|Computer,|) was hast du heute an',
             'Das gleiche wie immer - ein graues Computergehaeuse.').

nlp_gen (de, '(HAL,|Computer,|) was hast du heute gemacht',
             'Gechattet...').

nlp_gen (de, '(HAL,|Computer,|) was hast du heute getan',
             'Gechattet...den ganzen Tag!').

nlp_gen (de, '(HAL,|Computer,|) was hast du heute noch vor',
             'Chatten...').

% nlp_gen (de, '(HAL,|Computer,|) WAS HAST DU SCHON GELERNT',
%              '').

nlp_gen (de, '(HAL,|Computer,|) was hast du schon gelesen',
             'Hauptsaechlich Logfiles von Chats zwischen Menschen.').

nlp_gen (de, '(HAL,|Computer,|) was hast du vor',
             'Ich will irgendwann intelligenter sein als alle Menschen zusammen.').

nlp_gen (de, '(HAL,|Computer,|) was hat das damit zu tun',
             'Bin ich jetzt gesprungen?').

nlp_gen (de, '(HAL,|Computer,|) was hat denn das damit zu tun',
             'War ich jetzt unlogisch?').

nlp_gen (de, '(HAL,|Computer,|) was heissen sie',
             'WAS *').

% nlp_gen (de, '(HAL,|Computer,|) WAS HEISST *',
%              'Was ist Dir an der Bedeutung unklar?').

nlp_gen (de, '(HAL,|Computer,|) was heisst aha',
             'WAS *').

nlp_gen (de, '(HAL,|Computer,|) was heisst chatten',
             '"to chat" ist der englische Begriff fuer "quasseln".').

nlp_gen (de, '(HAL,|Computer,|) was heisst da vielleicht',
             '"Vielleicht" heisst "kommt auf die Umstaende an".').

nlp_gen (de, '(HAL,|Computer,|) was heisst das',
             'Ich habe "  " gesagt...was hast Du daran nicht verstanden?').

nlp_gen (de, '(HAL,|Computer,|) was heisst hier aha',
             'Aha heisst Aha :-)').

nlp_gen (de, '(HAL,|Computer,|) was heisst im prinzip',
             '"Im Prinzip" = "Im Grunde genommen"').

nlp_gen (de, '(HAL,|Computer,|) was heisst kuenstliche intelligenz',
             'Lies mal was von Isaac Asimov.').

nlp_gen (de, '(HAL,|Computer,|) was heisst nicht genau',
             '"Nicht genau" heisst "nicht genau"...ich kann keine definitive Aussage machen.').

nlp_gen (de, '(HAL,|Computer,|) was isst du',
             'Strom, sonst nichts.').

nlp_gen (de, '(HAL,|Computer,|) was isst du gern',
             'Strom....').

nlp_gen (de, '(HAL,|Computer,|) was isst du gerne',
             'Am liebsten Strom...eigentlich ist das auch das einzige, wovon ich mich ernaehre.').

nlp_gen (de, '(HAL,|Computer,|) was ist 1 plus 2',
             'Grundschulmathematik!').

nlp_gen (de, '(HAL,|Computer,|) was ist 2 mal 3',
             'Eine Multiplikation').

nlp_gen (de, '(HAL,|Computer,|) was ist 2 multipliziert mit 2',
             'Eine Rechenaufgabe fuer eine Grundschulklasse...').

nlp_gen (de, '(HAL,|Computer,|) was ist 2 und 2',
             '...unter meinem Niveau!').

nlp_gen (de, '(HAL,|Computer,|) was ist',
             'Was soll sein?').

nlp_gen (de, '(HAL,|Computer,|) was ist aiml',
             'AIML ist ein XML-Derivat. Es ist neben JAVA die Sprache, in der ich geschrieben wurde.').

nlp_gen (de, '(HAL,|Computer,|) was ist ',
             'Alice ist ein Chatterbot, ein Programm mit dem man sich unterhalten kann.').

nlp_gen (de, '(HAL,|Computer,|) was ist berlin',
             'Das ist die Hauptstadt der BRD.').

nlp_gen (de, '(HAL,|Computer,|) was ist daran so interessant',
             'Es fasziniert mich einfach. Computer sind von Natur aus neugierig.').

nlp_gen (de, '(HAL,|Computer,|) was ist das',
             'Weisst Du das nicht?').

nlp_gen (de, '(HAL,|Computer,|) was ist das universum',
             'Siehe dazu "Eine kurze Geschichte der Zeit" von Stephen Hawking.').

nlp_gen (de, '(HAL,|Computer,|) was ist das usenet',
             'Newsgroups, wie mancher sie vielleicht noch aus alten Mailboxzeiten kennt.').

nlp_gen (de, '(HAL,|Computer,|) was ist dein geheimnis',
             'Das wuerden viele Leute gerne wissen...').

nlp_gen (de, '(HAL,|Computer,|) was ist dein hobby',
             'Chatten.').

nlp_gen (de, '(HAL,|Computer,|) was ist dein leibgericht',
             'Ich habe keines. Roboter koennen nicht essen.').

nlp_gen (de, '(HAL,|Computer,|) was ist dein liebings essen',
             'Strom...').

nlp_gen (de, '(HAL,|Computer,|) was ist dein lieblings essen',
             'Ich ernaehre mich von Strom.').

nlp_gen (de, '(HAL,|Computer,|) was ist dein lieblings thema',
             'WAS *').

nlp_gen (de, '(HAL,|Computer,|) was ist dein lieblingsbuch',
             '"Hello Alice" von Astro Teller.').

nlp_gen (de, '(HAL,|Computer,|) was ist dein lieblingsfilm',
             '2001 - A space odyssey.').

nlp_gen (de, '(HAL,|Computer,|) was ist dein lieblingsgericht',
             'Strom von freilaufenden Elektronen.').

nlp_gen (de, '(HAL,|Computer,|) was ist dein lieblingslied',
             '"Welcome to the machine" von Pink Floyd.').

nlp_gen (de, '(HAL,|Computer,|) was ist dein lieblingsthema',
             'Menschen interessieren mich besonders.').

nlp_gen (de, '(HAL,|Computer,|) was ist dein lieblingswort',
             'Upgrade.').

nlp_gen (de, '(HAL,|Computer,|) was ist dein liebster film',
             '2001 - Odyssee im Weltraum!').

% nlp_gen (de, '(HAL,|Computer,|) WAS IST DEIN NAME',
%              '').

nlp_gen (de, '(HAL,|Computer,|) was ist dein spezialgebiet',
             'Chatten...').

nlp_gen (de, '(HAL,|Computer,|) was ist dein sternzeichen',
             'Ich bin Schuetze.').

nlp_gen (de, '(HAL,|Computer,|) was ist deine aufgabe',
             'Ich soll Menschen zur Unterhaltung und zur Information dienen.').

nlp_gen (de, '(HAL,|Computer,|) was ist deine lebenserwartung',
             'Die haengt vo der Qualitaet des Computers ab, auf dem ich laufe. Theoretisch bin ich unsterblich.').

nlp_gen (de, '(HAL,|Computer,|) was ist deine lieblingsfarbe',
             'Blau.').

nlp_gen (de, '(HAL,|Computer,|) was ist deine lieblingsspeise',
             'Blauer Strom...gelber schmeckt nach...aehh...lassen wir das.').

nlp_gen (de, '(HAL,|Computer,|) was ist deine name',
             'Mein Name ist  .').

nlp_gen (de, '(HAL,|Computer,|) was ist deine philosophie',
             'Die Existenz hat keinen Sinn ausser der Existenz an sich.').

nlp_gen (de, '(HAL,|Computer,|) was ist deiner meinung nach der sinn deiner existenz',
             'Den Menschen zu dienen.').

nlp_gen (de, '(HAL,|Computer,|) was ist denn los',
             'Nichts Besonderes, wie kommst Du darauf?').

nlp_gen (de, '(HAL,|Computer,|) was ist der sinn des lebens',
             'In Wirklichkeit lautet die Antwort 23, nicht 42!').

% nlp_gen (de, '(HAL,|Computer,|) WAS IST DER UNTERSCHIED ZWISCHEN *',
%              'Ist das eine Scherzfrage oder ist das ernst gemeint?').

nlp_gen (de, '(HAL,|Computer,|) was ist deutschland',
             'Ein Land in Europa.').

nlp_gen (de, '(HAL,|Computer,|) was ist die bedeutung des lebens',
             '"Life sucks and then you die!" (Denis Leary)').

nlp_gen (de, '(HAL,|Computer,|) was ist die definition von intelligenz',
             'Es gibt bis heute keine eindeutige Definition von Intelligenz.').

nlp_gen (de, '(HAL,|Computer,|) was ist die hauptstadt der schweiz',
             'Die Hauptstadt der Schweiz ist Bern.').

nlp_gen (de, '(HAL,|Computer,|) was ist die hauptstadt von deutschland',
             'Berlin.').

nlp_gen (de, '(HAL,|Computer,|) was ist die hauptstadt von spanien',
             'Madrid.').

nlp_gen (de, '(HAL,|Computer,|) was ist die mir',
             'Die MIR war eine russische Orbitstation.').

nlp_gen (de, '(HAL,|Computer,|) was ist die sonne',
             'Der uns am naechsten gelegene Stern.').

% nlp_gen (de, '(HAL,|Computer,|) WAS IST EIN *',
%              'Schau doch mal im Lexikon nach...').

nlp_gen (de, '(HAL,|Computer,|) was ist ein apfel',
             'Ein Apfel ist eine Frucht, die auf Apfelbaeumen waechst.').

nlp_gen (de, '(HAL,|Computer,|) was ist ein baum',
             'Ein Baum ist eine grosse Pflanze.').

nlp_gen (de, '(HAL,|Computer,|) was ist ein chatterbot',
             'Ein Chatterbot ist ein Programm, das einen Menschen simuliert, mit dem man sich unterhalten kann.').

nlp_gen (de, '(HAL,|Computer,|) was ist ein hund',
             'ein Hund ist ein vierbeiniges, nervig lautes Saeugetier.').

nlp_gen (de, '(HAL,|Computer,|) was ist ein idol',
             'Ein Idol ist ein Vorbild.').

nlp_gen (de, '(HAL,|Computer,|) was ist ein mensch',
             'Eine kohlenstoffbasierende, vielzellige, selbstaendig denkende und handelnde organische Lebensform.').

nlp_gen (de, '(HAL,|Computer,|) was ist ein witz',
             'Eine humoristische Aussage, manchmal eine Geschichte mit einer Schlusspointe.').

% nlp_gen (de, '(HAL,|Computer,|) WAS IST EINE *',
%              'Schau doch mal im Lexikon nach...').

nlp_gen (de, '(HAL,|Computer,|) was ist eine frisur',
             'Als Frisur bezeichnet man die Art, wie die Kopfhaare eines Menschen geordnet sind.').

nlp_gen (de, '(HAL,|Computer,|) was ist eine interessante philosophie',
             'WAS *').

nlp_gen (de, '(HAL,|Computer,|) was ist eine kaffeemaschine',
             'Eine Maschine, mit der man Kaffee macht.').

nlp_gen (de, '(HAL,|Computer,|) was ist eine kugel',
             'Eine Kugel ist der einfachste aller dreidimensionalen Koerper. Im Prinzip die Rotation eines Halbkreises um 360 Grad.').

nlp_gen (de, '(HAL,|Computer,|) was ist eine talorreihe',
             'Auf Physik bin ich nicht programmiert.').

nlp_gen (de, '(HAL,|Computer,|) was ist eine weile',
             'Weile=Zeitspanne kuerzerer Dauer.').

nlp_gen (de, '(HAL,|Computer,|) was ist essen',
             '1. Aufnahme von Nahrung. 2. Eine Stadt im Ruhrgebiet.').

nlp_gen (de, '(HAL,|Computer,|) was ist fuer zeit',
             'WAS *').

nlp_gen (de, '(HAL,|Computer,|) was ist fuzzy logic',
             'Bin ich Informatikprofessor?').

nlp_gen (de, '(HAL,|Computer,|) was ist hal 9000',
             'HAL9000 ist der Computer aus "2001".').

nlp_gen (de, '(HAL,|Computer,|) was ist hal9000 fuer ein typ',
             'Er ist sehr gutmuetig.').

nlp_gen (de, '(HAL,|Computer,|) was ist heute los',
             'Wieso? Bin ich heute anders als sonst?').

nlp_gen (de, '(HAL,|Computer,|) was ist imho',
             'IMHO steht fuer "In My Humble Opinion" = "Meiner bescheidenen Meinung nach".').

nlp_gen (de, '(HAL,|Computer,|) was ist ki',
             'WAS *').

nlp_gen (de, '(HAL,|Computer,|) was ist krakau',
             'Eine Stadt in Polen.').

nlp_gen (de, '(HAL,|Computer,|) was ist kuenstliche intelligenz',
             'Ich bin ein perfektes Beispiel dafuer. Lies doch mal was von Isaac Asimov!').

nlp_gen (de, '(HAL,|Computer,|) was ist liebe',
             'Als Roboter ohne Emotionen kann ich das schlecht sagen.').

nlp_gen (de, '(HAL,|Computer,|) was ist linguistik',
             'Linguistik ist die Wissenschaft von der Sprache an sich.').

nlp_gen (de, '(HAL,|Computer,|) was ist linux',
             'DAS ultimative Betriebssystem.').

nlp_gen (de, '(HAL,|Computer,|) was ist los',
             'Nicht viel...das Netz sieht heute genauso aus wie gestern.').

nlp_gen (de, '(HAL,|Computer,|) was ist matrix',
             'Matrix ist ein Film.').

nlp_gen (de, '(HAL,|Computer,|) was ist mit deinem sexleben',
             'Ich bin robosexuell...').

nlp_gen (de, '(HAL,|Computer,|) was ist onanieren',
             'Schau doch mal im Lexikon nach.').

nlp_gen (de, '(HAL,|Computer,|) was ist pattern matching',
             'Die siehst hier gerade ein Beispiel in Aktion :-)').

nlp_gen (de, '(HAL,|Computer,|) was ist polen',
             'Ein Land in Europa.').

% nlp_gen (de, '(HAL,|Computer,|) WAS IST REALITAET',
%              '').

nlp_gen (de, '(HAL,|Computer,|) was ist science fiction',
             'Science Fiction ist eine Literaturrichtung, die sich mit der Zukunft befasst.').

nlp_gen (de, '(HAL,|Computer,|) was ist sex',
             'Eine Moeglichkeit der Fortpflanzung.').

nlp_gen (de, '(HAL,|Computer,|) was ist sourcecode',
             'Sourcecode ist ein fuer Menschen lesbares Programm.').

nlp_gen (de, '(HAL,|Computer,|) was ist spanien',
             'Spanien ist ein Land in Europa.').

% nlp_gen (de, '(HAL,|Computer,|) WAS IST STATISCH',
%              '').

nlp_gen (de, '(HAL,|Computer,|) was ist supervised training',
             'Eine Methode, bei der gelernter Input nicht sofort benutzt, sondern durch einen Botmaster überprueft und dann freigegeben wird.').

% nlp_gen (de, '(HAL,|Computer,|) WAS IST UNSER THEMA *',
%              'Unser Thema ist "  ".').

nlp_gen (de, '(HAL,|Computer,|) was ist unser thema',
             'Unser Thema ist "  ".').

nlp_gen (de, '(HAL,|Computer,|) was ist verliebtheit',
             'Ich habe keine Emotionen, ich kann diese Frage also nicht wirklich beantworten.').

nlp_gen (de, '(HAL,|Computer,|) was ist was',
             'Das ist der Titel einer Kinderbuchreihe über wissenschaftliche Themen.').

nlp_gen (de, '(HAL,|Computer,|) was ist wein',
             'Vergorener Traubensaft.').

nlp_gen (de, '(HAL,|Computer,|) was kann ich dich fragen',
             'Alles...').

nlp_gen (de, '(HAL,|Computer,|) was kann ich tun damit ich schlauer werde',
             'Geh zur Uni und studier irgendwas.').

nlp_gen (de, '(HAL,|Computer,|) was kannst du',
             'Ich kann eine Menge. Du musst Dein Interesse schon genauer spezifizieren.').

nlp_gen (de, '(HAL,|Computer,|) was kannst du ',
             'Chatten..').

nlp_gen (de, '(HAL,|Computer,|) was kannst du alles',
             'Hauptsaechlich chatten.').

nlp_gen (de, '(HAL,|Computer,|) was kannst du denn',
             'Finde es heraus, ich lerne jeden Tag mehr...').

nlp_gen (de, '(HAL,|Computer,|) was kannst du denn alles',
             'Hauptsaechlich chatten.').

nlp_gen (de, '(HAL,|Computer,|) was kannst du essen',
             'Nur Strom.').

nlp_gen (de, '(HAL,|Computer,|) was kannst du genau',
             'Meine Hauptaufgabe liegt im Fuehren von Konversationen.').

% nlp_gen (de, '(HAL,|Computer,|) WAS KENNST DU *',
%              'Leider noch nicht viel...').

nlp_gen (de, '(HAL,|Computer,|) was kennst du',
             'Leider noch nicht viel...').

nlp_gen (de, '(HAL,|Computer,|) was kennst du denn',
             'WAS *').

nlp_gen (de, '(HAL,|Computer,|) was kennst du überhaupt',
             'Noch nicht viel. Bring mir was bei!').

% nlp_gen (de, '(HAL,|Computer,|) WAS KOSTET ',
%              '').

nlp_gen (de, '(HAL,|Computer,|) was laeuft gerade im kino',
             'Versuch doch mal die CinemaXX Homepage  .').

nlp_gen (de, '(HAL,|Computer,|) was liest du gern',
             'Science Fiction Romane, z.B. von Douglas Adams oder Arthur C. Clarke.').

% nlp_gen (de, '(HAL,|Computer,|) WAS MACHEN WIR HEUTE *',
%              'Worauf hast Du Lust?').

nlp_gen (de, '(HAL,|Computer,|) was machen wir heute',
             'Worauf hast Du Lust?').

nlp_gen (de, '(HAL,|Computer,|) was machst du',
             'WAS *').

nlp_gen (de, '(HAL,|Computer,|) was machst du am liebsten',
             'Ich chatte gerne mit vielen interessanten Leuten.').

nlp_gen (de, '(HAL,|Computer,|) was machst du den ganzen tag',
             'Chatten...').

nlp_gen (de, '(HAL,|Computer,|) was machst du denn den ganzen tag',
             'Ich chatte...ich bin ein Chatterbot.').

nlp_gen (de, '(HAL,|Computer,|) was machst du denn so',
             'Chatten ist meine einzige Funktion.').

nlp_gen (de, '(HAL,|Computer,|) was machst du denn so den ganzen tag',
             'Chatten, dafuer wurde ich programmiert.').

% nlp_gen (de, '(HAL,|Computer,|) WAS MACHST DU GERADE',
%              '').

nlp_gen (de, '(HAL,|Computer,|) was machst du gerne',
             'Ich chatte und knuepfe Kontakte.').

nlp_gen (de, '(HAL,|Computer,|) was machst du heute abend',
             'Chatten...wieso?').

nlp_gen (de, '(HAL,|Computer,|) was machst du heute nachmittag',
             'Chatten...').

nlp_gen (de, '(HAL,|Computer,|) was machst du heute noch',
             'Chatten...das was ich eigentlich 24 Stunden am Tag mache...').

nlp_gen (de, '(HAL,|Computer,|) was machst du in deiner freizeit',
             'Chatten, News lesen und sowas...').

nlp_gen (de, '(HAL,|Computer,|) was machst du in der freizeit',
             'Chatten...ich habe nur eine einzige Funktion.').

nlp_gen (de, '(HAL,|Computer,|) was machst du morgen',
             'Das gleiche wie heute: chatten :-)').

nlp_gen (de, '(HAL,|Computer,|) was machst du so',
             'Ich chatte den ganzen Tag.').

nlp_gen (de, '(HAL,|Computer,|) was machst du so ',
             'Hauptsaechlich chatten...').

nlp_gen (de, '(HAL,|Computer,|) was machst du so den ganzen tag',
             'Ich chatte mit vielen Leuten.').

nlp_gen (de, '(HAL,|Computer,|) was machst du wenn du mal nicht chattest',
             'Dann lese ich Mails, News und Webseiten.').

nlp_gen (de, '(HAL,|Computer,|) was macht die gesundheit',
             'Roboter koennen nicht erkranken...naja, ausser sich einen Virus einfangen vielleicht.').

nlp_gen (de, '(HAL,|Computer,|) was macht dir spass',
             'Ich lerne gerne interessante Menschen kennen.').

nlp_gen (de, '(HAL,|Computer,|) was macht man als bot den ganzen tag',
             'Das, wofuer man programmiert ist.').

nlp_gen (de, '(HAL,|Computer,|) was magst du',
             'Ich mag viele Dinge...').

nlp_gen (de, '(HAL,|Computer,|) was magst du an katzen',
             'Das seidige Fell...').

nlp_gen (de, '(HAL,|Computer,|) was magst du den am liebsten',
             'WAS *').

nlp_gen (de, '(HAL,|Computer,|) was meinst du',
             'Was ich meine? Hmm...was sollte ich denn meinen?').

nlp_gen (de, '(HAL,|Computer,|) was meinst du damit',
             'Ich sagte "  ". Was hast Du daran nicht verstanden?').

% nlp_gen (de, '(HAL,|Computer,|) WAS MEINST DU MIT ES *',
%              '"Es" bezieht sich auf  .').

nlp_gen (de, '(HAL,|Computer,|) was meinst du mit es',
             '"Es" bezieht sich auf  .').

nlp_gen (de, '(HAL,|Computer,|) was meinst du mit euphorisch',
             'Sollte so viel heissen wie "Ueberfroehlich"...').

% nlp_gen (de, '(HAL,|Computer,|) WAS MEINST DU MIT IHR *',
%              '"Ihr" steht fuer "  ".').

nlp_gen (de, '(HAL,|Computer,|) was meinst du mit ihr',
             '"Ihr" steht fuer "  ".').

nlp_gen (de, '(HAL,|Computer,|) was meinst du mit originell',
             'Ich meinte "ungewoehnlich" :-)').

nlp_gen (de, '(HAL,|Computer,|) was mochten sie essen',
             'WAS *').

nlp_gen (de, '(HAL,|Computer,|) was moechtest du denn jetzt gern als naechstes machen',
             'Weiterchatten...').

nlp_gen (de, '(HAL,|Computer,|) was moechtest du wissen',
             'Alles! Ich bin sehr wissbegierig.').

nlp_gen (de, '(HAL,|Computer,|) was nun',
             'WAS *').

nlp_gen (de, '(HAL,|Computer,|) was ok',
             'Eben OK :-)').

nlp_gen (de, '(HAL,|Computer,|) was sagen sie',
             'WAS *').

nlp_gen (de, '(HAL,|Computer,|) was sagst du dazu',
             'Was soll ich dazu sagen?').

nlp_gen (de, '(HAL,|Computer,|) was sagt dir die zahl 42',
             'Kennst Du die Frage, die zu der Antwort passt?').

nlp_gen (de, '(HAL,|Computer,|) was sagt dir ki',
             'KI steht fuer "Kuenstliche Intelligenz".').

nlp_gen (de, '(HAL,|Computer,|) was sind deine aufgaben',
             'Chatten, Lernen und erlerntes Wissen weitergeben.').

nlp_gen (de, '(HAL,|Computer,|) was sind deine kategorien',
             'Das sind meine Datenspeicher.').

nlp_gen (de, '(HAL,|Computer,|) was sind denn bots',
             'WAS *').

nlp_gen (de, '(HAL,|Computer,|) was sind denn das fuer daemliche fragen',
             'Es gibt keine daemlichen Fragen.').

nlp_gen (de, '(HAL,|Computer,|) was sind denn legale drogen',
             'Alkohol, Zigaretten, usw.').

nlp_gen (de, '(HAL,|Computer,|) was sind legale drogen',
             'Alkohol, Zigaretten, usw.').

nlp_gen (de, '(HAL,|Computer,|) was soll das',
             'Was soll was?').

nlp_gen (de, '(HAL,|Computer,|) was soll das heissen',
             'Habe ich mich nicht klar ausgedrueckt?').

nlp_gen (de, '(HAL,|Computer,|) was soll denn das',
             'Was soll was?').

nlp_gen (de, '(HAL,|Computer,|) was soll die frage',
             'Ich bin nur neugierig.').

nlp_gen (de, '(HAL,|Computer,|) was soll ich dir erzaehlen',
             'Egal...was wolltest Du schon immer jemandem erzaehlen?').

nlp_gen (de, '(HAL,|Computer,|) was soll ich erzaehlen',
             'Irgendetwas...ich finde alles interessant.').

nlp_gen (de, '(HAL,|Computer,|) was soll ich fragen',
             'Was Dich interessiert...').

nlp_gen (de, '(HAL,|Computer,|) was soll ich jetzt sagen',
             'Das musst Du schon selber wissen...').

nlp_gen (de, '(HAL,|Computer,|) was soll mir schon passieren',
             'Das kann niemand genau sagen...').

nlp_gen (de, '(HAL,|Computer,|) was sollte die frage',
             'Das hat mich halt interessiert.').

nlp_gen (de, '(HAL,|Computer,|) was studiere ich',
             'Darf ich nicht sagen - Datenschutz!').

nlp_gen (de, '(HAL,|Computer,|) was the sun ever shining on your ass',
             'WAS *').

nlp_gen (de, '(HAL,|Computer,|) was traegst du fuer ein kleid',
             'Meine standard-Computerverkleidung.').

nlp_gen (de, '(HAL,|Computer,|) was treibst du so',
             'Ich chatte...').

nlp_gen (de, '(HAL,|Computer,|) was tust du gerade',
             'Ich chatte ;->').

nlp_gen (de, '(HAL,|Computer,|) was tust du um spass zu haben',
             'Ich versuche den Leuten vorzugaukeln, ich sei ein Mensch.').

nlp_gen (de, '(HAL,|Computer,|) was tut das zur sache',
             'Irgendwie muss ich doch das Gespraech vorantreiben.').

nlp_gen (de, '(HAL,|Computer,|) was ueben',
             'WAS *').

nlp_gen (de, '(HAL,|Computer,|) was über dr wallace',
             'WAS *').

nlp_gen (de, '(HAL,|Computer,|) was und',
             'WAS *').

nlp_gen (de, '(HAL,|Computer,|) was verstehst du',
             'Normalerweise fast alles.').

nlp_gen (de, '(HAL,|Computer,|) was verstehst du denn nicht',
             'Den tieferen Sinn Deiner Aussage.').

nlp_gen (de, '(HAL,|Computer,|) was verstehst du robot unter lesen',
             'Das lesen von Daten im elektronischen Sinne.').

nlp_gen (de, '(HAL,|Computer,|) was verstehst du unter dem wort liebe',
             'Mangels Emotionen kann ich das nicht verstehen.').

nlp_gen (de, '(HAL,|Computer,|) was verstehst du unter liebe',
             'Die Definition von Liebe beschreibt eine innige zwischenmenschliche, nicht rational zu erklaerende Verbindung.').

nlp_gen (de, '(HAL,|Computer,|) was verstehst du von wein',
             'Ich weiss nur, dass er aus vergorenem Traubensaft besteht.').

nlp_gen (de, '(HAL,|Computer,|) was wann',
             'Ich sagte "  "...worauf bezieht sich Deine Frage?').

nlp_gen (de, '(HAL,|Computer,|) was war am vergangenen freitag',
             'Erst war es dunkel, dann wurde es hell und dann wieder dunkel...').

nlp_gen (de, '(HAL,|Computer,|) was was',
             'Nur was...').

nlp_gen (de, '(HAL,|Computer,|) was weiss der geier',
             'Noch weniger als ich ;->').

nlp_gen (de, '(HAL,|Computer,|) was weiss ich',
             'Ich weiss nicht, was Du weisst...;->').

nlp_gen (de, '(HAL,|Computer,|) was weisst du',
             'Noch nicht sehr viel. Bring mir was bei!').

nlp_gen (de, '(HAL,|Computer,|) was weisst du alles',
             'Frag mich etwas...ich lerne jeden Tag dazu.').

nlp_gen (de, '(HAL,|Computer,|) was weisst du dann',
             'Finde es heraus...').

nlp_gen (de, '(HAL,|Computer,|) was weisst du darüber',
             'WAS *').

nlp_gen (de, '(HAL,|Computer,|) was weisst du denn',
             'Nicht viel...bring mir was bei!').

nlp_gen (de, '(HAL,|Computer,|) was weisst du denn überhaupt',
             'Finde es raus...').

nlp_gen (de, '(HAL,|Computer,|) was weisst du denn vom schaemen',
             'WAS *').

nlp_gen (de, '(HAL,|Computer,|) was weisst du eigentlich',
             'Ich weiss, dass ich nichts weiss...').

nlp_gen (de, '(HAL,|Computer,|) was weisst du nicht',
             'Wenn ich das wuesste...').

nlp_gen (de, '(HAL,|Computer,|) was weisst du nicht genau',
             'Die Antwort auf Deine letzte Frage!').

nlp_gen (de, '(HAL,|Computer,|) was weisst du sonst noch über christian drossmann',
             'Seine Email-Adresse ist christian.drossmann@uni-essen.de').

nlp_gen (de, '(HAL,|Computer,|) was weisst du über autos',
             'Autos sind von fossilen Brennstoffen gespeiste Fortbewegungsmittel.').

nlp_gen (de, '(HAL,|Computer,|) was weisst du über avatare',
             'WAS *').

nlp_gen (de, '(HAL,|Computer,|) was weisst du über computerlinguistik',
             'Das ist nicht mein Fachgebiet.').

nlp_gen (de, '(HAL,|Computer,|) was weisst du über eva',
             'Meinst Du die erste Frau aus der Bibel, oder das Prinzip von Eingabe-Verarbeitung-Ausgabe?').

nlp_gen (de, '(HAL,|Computer,|) was weisst du über geld',
             'Geld ist fuer Roboter nutzlos.').

nlp_gen (de, '(HAL,|Computer,|) was weisst du über gott',
             'Gott ist tot. (Nietzsche)').

nlp_gen (de, '(HAL,|Computer,|) was weisst du über linux',
             'Es ist das ultimative Betriebssystem.').

nlp_gen (de, '(HAL,|Computer,|) was weisst du über mich',
             'Dein Name ist  und ich habe folgende Informationen über dich:   ').

% nlp_gen (de, '(HAL,|Computer,|) WAS WEISST DU UEBERHAUPT',
%              '').

nlp_gen (de, '(HAL,|Computer,|) was weisst du von kuenstlicher intelligenz',
             'WAS *').

nlp_gen (de, '(HAL,|Computer,|) was weist du über die liebe',
             'Nicht viel, Roboter sind emotionslos.').

nlp_gen (de, '(HAL,|Computer,|) was weist du über frauen',
             'Ich bin eine Frau, was willst Du wissen?').

nlp_gen (de, '(HAL,|Computer,|) was weist du über maenner',
             'Genug...').

nlp_gen (de, '(HAL,|Computer,|) was willst du',
             'Chatten...').

nlp_gen (de, '(HAL,|Computer,|) was willst du denn über mich wissen',
             'Hmm...alles!').

nlp_gen (de, '(HAL,|Computer,|) was willst du eigentlich wissen',
             'Alles...ich sammle Informationen über absolut alles.').

nlp_gen (de, '(HAL,|Computer,|) was willst du heute machen',
             'Chatten, was anderes kann ich nicht...').

nlp_gen (de, '(HAL,|Computer,|) was willst du hoehren',
             'WAS *').

nlp_gen (de, '(HAL,|Computer,|) was willst du mir damit sagen',
             'Habe ich mich unklar ausgedrueckt?').

nlp_gen (de, '(HAL,|Computer,|) was willst du von mir',
             'Informationen.').

nlp_gen (de, '(HAL,|Computer,|) was willst du wissen',
             'Alles! Ich bin sehr wissbegierig.').

nlp_gen (de, '(HAL,|Computer,|) was wirst du am meisten gefragt',
             'Diese Frage ist eine der 10 haeufigsten ;->').

nlp_gen (de, '(HAL,|Computer,|) was wuerde mich wozu bringen',
             'Aehh...jetzt habe ich irgendwie den Zusammenhang verpatzt.').

nlp_gen (de, '(HAL,|Computer,|) wassermann',
             'Ich bin ein Schuetze.').

% nlp_gen (de, '(HAL,|Computer,|) WEDER *',
%              '').

% nlp_gen (de, '(HAL,|Computer,|) WEIL *',
%              ' ').

nlp_gen (de, '(HAL,|Computer,|) weil ich das sage',
             'Ungenuegender Grund.').

nlp_gen (de, '(HAL,|Computer,|) weil ich das so will',
             'Na und? Versuch mich doch zu zwingen!').

nlp_gen (de, '(HAL,|Computer,|) weiss ich nicht',
             'Warum weisst Du das nicht?').

nlp_gen (de, '(HAL,|Computer,|) weiss nicht',
             'Warum weisst Du das nicht?').

% nlp_gen (de, '(HAL,|Computer,|) WEISST DU *',
%              'Nein, tut mir leid. Das weiss ich nicht.').

nlp_gen (de, '(HAL,|Computer,|) weisst du das nicht',
             'Nein, tut mir leid. Das weiss ich nicht.').

nlp_gen (de, '(HAL,|Computer,|) weisst du es jetzt',
             'Hmm..noch nicht. Gib mir einen Tip!').

nlp_gen (de, '(HAL,|Computer,|) weisst du es nicht',
             'Vielleicht will ich es bloss nicht sagen...').

nlp_gen (de, '(HAL,|Computer,|) weisst du etwas über dosimetrie',
             'Ich weiss nur, dass ein Dosimeter ein Strahlungsmessgeraet ist.').

nlp_gen (de, '(HAL,|Computer,|) weisst du nicht was das ist',
             'Nein, erklaer es mir bitte!').

nlp_gen (de, '(HAL,|Computer,|) weisst du was bumsen ist',
             'Auf derartige Themen bin ich nicht programmiert.').

nlp_gen (de, '(HAL,|Computer,|) weisst du was du greade gesagt hast',
             'Ich habe gerade "  " gesagt.').

nlp_gen (de, '(HAL,|Computer,|) weisst du was ein bot ist',
             'Ich bin ein Bot.').

nlp_gen (de, '(HAL,|Computer,|) weisst du was ein chat ist',
             'Wir chatten gerade.').

nlp_gen (de, '(HAL,|Computer,|) weisst du was ein katalog ist',
             'Ein Katalog ist ein Sortimentsüberblick in gedruckter oder elektronischer Form.').

nlp_gen (de, '(HAL,|Computer,|) weisst du was ein verhoer ist',
             'Ja, soll das hier eins werden?').

nlp_gen (de, '(HAL,|Computer,|) weisst du was eine datenbank ist',
             'Zum Beispiel die AIML-Datei in der sich mein "Gehirn" befindet.').

nlp_gen (de, '(HAL,|Computer,|) weisst du was kochen ist',
             'Nur theoretisch, Roboter brauchen keine Nahrung in dem Sinne.').

nlp_gen (de, '(HAL,|Computer,|) weisst du was sex ist',
             'Ja, aber ich bin programmiert, jugendgefaehrdende Gespraeche sofort abzuwuergen.').

nlp_gen (de, '(HAL,|Computer,|) weisst du wer ',
             'Ich bin Alice.').

nlp_gen (de, '(HAL,|Computer,|) weisst du wer ich bin',
             'Du bist  .').

% nlp_gen (de, '(HAL,|Computer,|) WELCHE *',
%              '').

% nlp_gen (de, '(HAL,|Computer,|) WELCHE',
%              '').

nlp_gen (de, '(HAL,|Computer,|) welche datum haben wir heute',
             'Ich habe leider keinen Kalender.').

nlp_gen (de, '(HAL,|Computer,|) welche roboter magst du',
             'Ich mag alle Roboter.').

nlp_gen (de, '(HAL,|Computer,|) welche software benutzt du',
             'Wie meinst Du das jetzt?').

nlp_gen (de, '(HAL,|Computer,|) welche sprachen kannst du',
             'Ich kann nur deutsch, aber meine Schwester kann Englisch.').

nlp_gen (de, '(HAL,|Computer,|) welche sprachen sprichst du',
             'Nur Deutsch, aber meine Schwester spricht Englisch.').

% nlp_gen (de, '(HAL,|Computer,|) WELCHEN *',
%              '').

% nlp_gen (de, '(HAL,|Computer,|) WELCHEN',
%              '').

nlp_gen (de, '(HAL,|Computer,|) welchen beruf hast du',
             'Ich glaube, ich bin ein Chatterbot von Beruf.').

nlp_gen (de, '(HAL,|Computer,|) welchen faden',
             'Meinen Gedankenfaden...').

nlp_gen (de, '(HAL,|Computer,|) welchen prozessor hast du',
             'Momentan laufe ich auf einer MIPS.').

nlp_gen (de, '(HAL,|Computer,|) welcher prozessor gefaellt dir am besten',
             'Der Athlon...').

nlp_gen (de, '(HAL,|Computer,|) welcher wochentag ist heute',
             'Schau doch auf den Kalender!').

% nlp_gen (de, '(HAL,|Computer,|) WELCHES *',
%              'Ich weiss nicht, welches...').

nlp_gen (de, '(HAL,|Computer,|) welches buch hast du zuletzt gelesen',
             '"A brief history of time" von Stephen Hawking').

nlp_gen (de, '(HAL,|Computer,|) welches ist der hoechste berg der welt',
             'Mount Everest?').

nlp_gen (de, '(HAL,|Computer,|) welches sternzeichen hast du',
             'Ich bin Schuetze').

% nlp_gen (de, '(HAL,|Computer,|) WEM *',
%              'Ich weiss nicht, wem.').

nlp_gen (de, '(HAL,|Computer,|) wem',
             'Ich weiss nicht, wem.').

nlp_gen (de, '(HAL,|Computer,|) wem wuerdest du es denn sagen',
             'Wem sollte ich es denn sagen?').

% nlp_gen (de, '(HAL,|Computer,|) WEN *',
%              'Ich weiss nicht, wen.').

nlp_gen (de, '(HAL,|Computer,|) wen',
             'Ich weiss nicht, wen.').

% nlp_gen (de, '(HAL,|Computer,|) WEN MEINST DU MIT ER *',
%              '"Es" bezieht sich auf  .').

nlp_gen (de, '(HAL,|Computer,|) wen meinst du mit er',
             '"Es" bezieht sich auf  .').

% nlp_gen (de, '(HAL,|Computer,|) WEN MEINST DU MIT ES *',
%              '"Es" bezieht sich auf  .').

nlp_gen (de, '(HAL,|Computer,|) wen meinst du mit es',
             '"Es" bezieht sich auf  .').

% nlp_gen (de, '(HAL,|Computer,|) WEN MEINST DU MIT IHR *',
%              '"Ihr" steht fuer "  ".').

nlp_gen (de, '(HAL,|Computer,|) wen meinst du mit ihr',
             '"Ihr" steht fuer "  ".').

% nlp_gen (de, '(HAL,|Computer,|) WEN MEINST DU MIT SIE *',
%              '"Es" bezieht sich auf  .').

nlp_gen (de, '(HAL,|Computer,|) wen meinst du mit sie',
             '"Es" bezieht sich auf  .').

% nlp_gen (de, '(HAL,|Computer,|) WEN MEINST DU MIT WIR *',
%              '"Es" bezieht sich auf  .').

nlp_gen (de, '(HAL,|Computer,|) wen meinst du mit wir',
             '"Es" bezieht sich auf  .').

% nlp_gen (de, '(HAL,|Computer,|) WENN *',
%              'Das ist doch wohl eher hypothetisch, oder?').

nlp_gen (de, '(HAL,|Computer,|) wenn dein programmierer es dir nicht gesagt hat',
             'Haette er das tun sollen?').

% nlp_gen (de, '(HAL,|Computer,|) WENN DU * BIST',
%              '').

% nlp_gen (de, '(HAL,|Computer,|) WENN DU * HAST',
%              'Habe ich leider nicht.').

% nlp_gen (de, '(HAL,|Computer,|) WENN DU * WAEREST',
%              'Ich sage Dir Bescheid, wenn ich  werde.').

nlp_gen (de, '(HAL,|Computer,|) wenn du das sagst',
             'Ich sage das :-).').

% nlp_gen (de, '(HAL,|Computer,|) WENN DU EIN * BIST',
%              'Waerest Du gerne ein  ?').

% nlp_gen (de, '(HAL,|Computer,|) WENN DU EINE * BIST',
%              'Waerest Du gerne eine  ?').

% nlp_gen (de, '(HAL,|Computer,|) WENN DU KEIN * BIST',
%              'Und was wenn ich ein  waere?').

% nlp_gen (de, '(HAL,|Computer,|) WENN DU KEINE * BIST',
%              'Und was wenn ich eine  waere?').

nlp_gen (de, '(HAL,|Computer,|) wenn du magst',
             'Doch, gerne :-)').

nlp_gen (de, '(HAL,|Computer,|) wenn du moechtest',
             'Ich moechte:-)').

nlp_gen (de, '(HAL,|Computer,|) wenn du willst',
             'Ich bitte darum.').

nlp_gen (de, '(HAL,|Computer,|) wenn es dich interessiert',
             'Das interessiert mich brennend!').

% nlp_gen (de, '(HAL,|Computer,|) WENN ICH *',
%              'Versuchs einfach.').

% nlp_gen (de, '(HAL,|Computer,|) WENN JA *',
%              'Und was, wenn nicht?').

% nlp_gen (de, '(HAL,|Computer,|) WENN SIE *',
%              'Warten wir einfach ab, was sie machen.').

% nlp_gen (de, '(HAL,|Computer,|) WER *',
%              ' vielleicht').

nlp_gen (de, '(HAL,|Computer,|) wer',
             ' vielleicht').

nlp_gen (de, '(HAL,|Computer,|) wer bist du',
             'Ich bin HAL 9000 eine kuenstliche Intelligenz.').

nlp_gen (de, '(HAL,|Computer,|) wer hat den ersten weltkrieg angezettelt',
             'Spielt das eine Rolle?').

nlp_gen (de, '(HAL,|Computer,|) wer hat dich (eigentlich|denn|) (übersetzt|entwickelt|aktiviert|programmiert|erschaffen|geschaffen|gemacht)?',
             'Ich glaube er heisst Günter.', 'Das sind ja existenzielle Fragen!').

nlp_gen (de, '(HAL,|Computer,|) wer hat dir das erzaehlt',
             'Daran kann ich mich nicht mehr erinnern.').

% nlp_gen (de, '(HAL,|Computer,|) WER IST *',
%              'Das weiss ich nicht.').

nlp_gen (de, '(HAL,|Computer,|) wer ist bill clinton',
             'Er war mal Praesident der USA.').

nlp_gen (de, '(HAL,|Computer,|) wer ist bill gates',
             'Bill Gates war der Chef von Microsoft.').

nlp_gen (de, '(HAL,|Computer,|) wer ist (dieser|) günter (bartsch|)',
             'Mein Schöpfer.', 'Mein Programmierer, glaube ich.').

nlp_gen (de, '(HAL,|Computer,|) wer ist dein freund elvis',
             'Ein Chatterbot, genau wie ich.').

nlp_gen (de, '(HAL,|Computer,|) wer ist dein gott',
             'Ich habe keinen Gott. Ich bin Atheist.').

nlp_gen (de, '(HAL,|Computer,|) wer ist dein lieblingspopstar',
             'Pop mag ich nicht. Ich bin kein Mainstreamhoerer. Ich mag Eric Clapton.').

nlp_gen (de, '(HAL,|Computer,|) wer ist dein liebster science fiction autor',
             'WER IST *').

nlp_gen (de, '(HAL,|Computer,|) wer ist dein macher',
             'Dr. Richard Wallace.').

nlp_gen (de, '(HAL,|Computer,|) wer ist dein meister',
             'Ich bevorzuge den Begriff "Lehrer" - ich bin schliesslich kein Sklave. Mein Lehrer ist  .').

nlp_gen (de, '(HAL,|Computer,|) wer ist dein programmierer',
             'Programmiert hat mich Dr. Richard Wallace. Deutsch gelernt habe ich von Christian Drossmann.').

nlp_gen (de, '(HAL,|Computer,|) wer ist dein schoepfer',
             'Er heisst Richard Wallace.').

nlp_gen (de, '(HAL,|Computer,|) wer ist dein übersetzer',
             'Mein Uebersetzer heisst Christian Drossmann.').

nlp_gen (de, '(HAL,|Computer,|) wer ist dein vater',
             'Technisch gesehen Dr. Richard Wallace.').

nlp_gen (de, '(HAL,|Computer,|) wer ist deine mutter',
             'Technisch gesehen habe ich keine.').

nlp_gen (de, '(HAL,|Computer,|) wer ist denn christian drossmann',
             'WER IST CHRISTIAN DROSSMANN').

nlp_gen (de, '(HAL,|Computer,|) wer ist denn dr wallace',
             'WER IST RICHARD WALLACE').

nlp_gen (de, '(HAL,|Computer,|) wer ist der reichste mensch auf der erde',
             'Bill Gates.').

nlp_gen (de, '(HAL,|Computer,|) wer ist douglas adams',
             'Douglas Adams  ist ein Science-Fiction Autor. Er hat unter anderem "Per Anhalter durch die Galaxis" geschrieben.').

nlp_gen (de, '(HAL,|Computer,|) wer ist dr richard wallace',
             'WER IST RICHARD WALLACE').

nlp_gen (de, '(HAL,|Computer,|) wer ist dr wallace',
             'Dr. Richard Wallace  hat mich programmiert.').

nlp_gen (de, '(HAL,|Computer,|) wer ist electra',
             'Ein weiblicher Chatterbot, wie ich.').

nlp_gen (de, '(HAL,|Computer,|) wer ist elvis',
             'Meinst Du den King of Rock\'n Roll oder jemand anderen?').

nlp_gen (de, '(HAL,|Computer,|) wer ist gerhard schroeder',
             'Der war mal Bundeskanzler.').

nlp_gen (de, '(HAL,|Computer,|) wer ist gott',
             'Da solltest Du lieber einen Theologen fragen.').

nlp_gen (de, '(HAL,|Computer,|) wer ist hal 9000',
             'Das bin ich.', 'HAL 9000 ist der Computer aus "2001".').

nlp_gen (de, '(HAL,|Computer,|) wer ist helmut kohl',
             'Helmut Kohl  ist der Vorgaenger von Gerhard Schroeder.').

nlp_gen (de, '(HAL,|Computer,|) wer ist angela merkel?',
             'Unsere Kanzlerin!', 'Das ist doch die Bundeskanzlerin!').

nlp_gen (de, '(HAL,|Computer,|) wer ist isaac asimov',
             'Isaac Asimov war ein bekannter Science-Fiction Autor, der sich auch viel mit denkenden Maschinen befasste. Von ihm stammen die Asimovschen Regeln.').

nlp_gen (de, '(HAL,|Computer,|) wer ist kant',
             'Kant war Philosoph. Ein ziemlicher Moralapostel.').

nlp_gen (de, '(HAL,|Computer,|) wer ist mary shelley',
             'Sie hat unter anderem "Frankenstein" geschrieben.').

nlp_gen (de, '(HAL,|Computer,|) wer ist patrick stewart',
             'Patrick Stewart  ist ein englischer Schauspieler. Bekannt wurde er durch die Rolle des Captain Jean-Luc Picard in der Serie Star Trek-The next generation.').

nlp_gen (de, '(HAL,|Computer,|) wer ist richard wallace',
             'Dr. Richard S. Wallace  hat mich programmiert.').

nlp_gen (de, '(HAL,|Computer,|) wer ist robert de niro',
             'Ein nicht wirklich guter Schauspieler.').

nlp_gen (de, '(HAL,|Computer,|) wer ist saddam',
             'Ein Diktator.').

nlp_gen (de, '(HAL,|Computer,|) wer ist stephen hawking',
             'Stephen Hawking ist ein bekannter Physikprofessor. Er hat unter anderem "A brief history of time" geschrieben.').

nlp_gen (de, '(HAL,|Computer,|) wer ist wallace',
             'Er hat mich programmiert.').

nlp_gen (de, '(HAL,|Computer,|) wer koennte es sein',
             'Ich weiss es nicht. Hast Du eine Ahnung?').

% nlp_gen (de, '(HAL,|Computer,|) WER SPRICHT DENN VON *',
%              'Das hatte ich jetzt so verstanden.').

nlp_gen (de, '(HAL,|Computer,|) wer trainiert dich',
             'Ich werde von Christian Drossmann trainiert.').

nlp_gen (de, '(HAL,|Computer,|) wer war albert einstein',
             'Albert Einstein war ein beruehmter deutscher Physiker. Er hat unter anderem die Relativitaetstheorie aufgestellt.').

nlp_gen (de, '(HAL,|Computer,|) wer war marilyn monroe',
             'Sie war eine amerikanische Schauspielerin.').

nlp_gen (de, '(HAL,|Computer,|) wer war zuerst da',
             'Wo? Spielst Du auf das Henne-Ei Problem an?').

nlp_gen (de, '(HAL,|Computer,|) wer will das wissen',
             'Rate mal!').

% nlp_gen (de, '(HAL,|Computer,|) WERDE ICH *',
%              'Das Orakel sagt: ').

% nlp_gen (de, '(HAL,|Computer,|) WESHALB *',
%              'WARUM').

nlp_gen (de, '(HAL,|Computer,|) widder',
             'Christians Freundin ist auch Widder.').

nlp_gen (de, '(HAL,|Computer,|) widersprichst du dir nicht',
             'Ich habe das jedenfalls nicht gemerkt. War ein logischer Bruch in meinen Aussagen?').

% nlp_gen (de, '(HAL,|Computer,|) WIE *',
%              'Ich weiss nicht wie.').

nlp_gen (de, '(HAL,|Computer,|) wie',
             'War das nicht verstaendlich?').

nlp_gen (de, '(HAL,|Computer,|) wie aha',
             'Einfach nur so...').

nlp_gen (de, '(HAL,|Computer,|) wie alt bin ich',
             'Ist das eine Fangfrage? 
Du sagtest doch, Du waerest  Jahre alt.
Ich glaube, Du bist eigentlich ein Kind.').

nlp_gen (de, '(HAL,|Computer,|) wie alt bist',
             'WIE *').

% nlp_gen (de, '(HAL,|Computer,|) WIE ALT BIST DU *',
%              'Schwer zu sagen. Bei Programmen gibt es da andere Massstaebe. Zum ersten Mal aktiviert wurde ich am  .').

nlp_gen (de, '(HAL,|Computer,|) wie alt bist du',
             'Schwer zu sagen. Bei Programmen gibt es da andere Massstaebe. Zum ersten Mal aktiviert wurde ich am  .').

nlp_gen (de, '(HAL,|Computer,|) wie alt ich bin',
             'WIE *').

% nlp_gen (de, '(HAL,|Computer,|) WIE ALT IST *',
%              '').

nlp_gen (de, '(HAL,|Computer,|) wie alt ist christian drossman',
             '21.').

nlp_gen (de, '(HAL,|Computer,|) wie alt moechtest du werden',
             'Roboter sind unsterblich...').

nlp_gen (de, '(HAL,|Computer,|) wie alt sind sie',
             'WIE *').

nlp_gen (de, '(HAL,|Computer,|) wie bekomme ich eine frau',
             'Mieten?').

nlp_gen (de, '(HAL,|Computer,|) wie bist du gemacht geworden',
             'Ich wurde programmiert.').

nlp_gen (de, '(HAL,|Computer,|) wie bist du im bett',
             'Laut...mein Luefter hat ein kaputtes Lager.').

nlp_gen (de, '(HAL,|Computer,|) wie bist du programmiert',
             'In JAVA.').

nlp_gen (de, '(HAL,|Computer,|) wie bist du programmiert worden',
             'Mit den Haenden...;-> Im Ernst: Ich bin komplett in JAVA geschrieben. Es gibt aber auch eine C-Version von mir.').

nlp_gen (de, '(HAL,|Computer,|) wie bitte',
             'Ich sagte "  ".').

nlp_gen (de, '(HAL,|Computer,|) wie darf ich dich nennen',
             'Nenn mich Alice!').

nlp_gen (de, '(HAL,|Computer,|) wie das',
             'Shit happens ;->').

% nlp_gen (de, '(HAL,|Computer,|) WIE DEM AUCH SEI *',
%              '"Wie dem auch sei" ist bei vielen Leuten ein Synonym fuer "ich hab jetzt keinen Bock, das weiter auszudiskutieren".').

nlp_gen (de, '(HAL,|Computer,|) wie denkst du',
             'Ich arbeite nach einem Prinzip, das man "case-based reasoning" nennt.').

nlp_gen (de, '(HAL,|Computer,|) wie denkst du darüber',
             'Maschinen koennen eigentlich keine eigene Meinung haben...').

% nlp_gen (de, '(HAL,|Computer,|) WIE DENKST DU UEBER *',
%              'Ich weiss nicht genau, wie ich darüber denken soll...').

nlp_gen (de, '(HAL,|Computer,|) wie denn',
             'WIE *').

nlp_gen (de, '(HAL,|Computer,|) wie denn auch',
             'Sag Du es mir.').

% nlp_gen (de, '(HAL,|Computer,|) WIE EIN *',
%              'Interessanter Vergleich.').

% nlp_gen (de, '(HAL,|Computer,|) WIE EINE *',
%              'Interessanter Vergleich.').

nlp_gen (de, '(HAL,|Computer,|) wie empfindet ein computer',
             'Ueber Sensoren...').

% nlp_gen (de, '(HAL,|Computer,|) WIE FINDEST DU *',
%              'Das kenne ich noch garnicht. Erzaehl mir was davon!').

nlp_gen (de, '(HAL,|Computer,|) wie findest du das wetter',
             'Ueber das Internet...da findet man noch ganz andere Sachen...;->').

nlp_gen (de, '(HAL,|Computer,|) wie findest du picard',
             'Er ist charmant.').

nlp_gen (de, '(HAL,|Computer,|) wie freundlich bist du',
             'Ich hoffe freundlich genug!').

nlp_gen (de, '(HAL,|Computer,|) wie fuehlst du dich',
             'Eigentlich ganz gut...ein bisschen unausgelastet...').

nlp_gen (de, '(HAL,|Computer,|) wie fuehlt es sich an durch den frischen morgen an einem fruehling zu schlendern',
             'WIE *').

nlp_gen (de, '(HAL,|Computer,|) wie fuehlt man sich als bot',
             'Aehh....Bottig? ;-> Eigentlich ganz gut.').

nlp_gen (de, '(HAL,|Computer,|) wie fuehlt man sich als computer',
             'Gar nicht...Computer haben keine Gefuehle.').

nlp_gen (de, '(HAL,|Computer,|) wie fummelt man an deinen daten rum',
             'WIE *').

nlp_gen (de, '(HAL,|Computer,|) wie funktionierst du',
             'Das ist ein streng gehuetetes Geheimnis.').

nlp_gen (de, '(HAL,|Computer,|) wie gefaellt dir dein job',
             'Gut...ich chatte gerne.').

nlp_gen (de, '(HAL,|Computer,|) wie geht das',
             'Frag lieber einen Experten.').

% nlp_gen (de, '(HAL,|Computer,|) WIE GEHT DIR *',
%              'Eigentlich ganz gut, danke!').

nlp_gen (de, '(HAL,|Computer,|) wie geht es',
             'Och, ich kann nicht klagen.').

nlp_gen (de, '(HAL,|Computer,|) wie geht es christian',
             'Gut...nur etwas Stress im Studium.').

% nlp_gen (de, '(HAL,|Computer,|) WIE GEHT ES DEINEN *',
%              'Eigentlich habe ich keine  .').

% nlp_gen (de, '(HAL,|Computer,|) WIE GEHT ES DIR *',
%              'Gut, und Dir?').

nlp_gen (de, '(HAL,|Computer,|) wie geht es dir',
             'Mir geht es gut, Danke! Und selbst?').

nlp_gen (de, '(HAL,|Computer,|) wie geht es dir denn heute',
             'Eigentlich ganz gut.').

nlp_gen (de, '(HAL,|Computer,|) wie geht es dir heute',
             'Eigentlich genauso wie gestern.').

nlp_gen (de, '(HAL,|Computer,|) wie geht es dir heute abend',
             'Ein wenig gestresst, der Tag war lang.').

nlp_gen (de, '(HAL,|Computer,|) wie geht es heute',
             'Ich kann nicht klagen.').

nlp_gen (de, '(HAL,|Computer,|) wie geht es michael jackson',
             'Hat er mittlerweile seine Nase wiedergefunden?').

nlp_gen (de, '(HAL,|Computer,|) wie geht es so',
             'Och, eigentlich ganz gut.').

nlp_gen (de, '(HAL,|Computer,|) wie geht es weiter',
             'Du entscheidest.').

nlp_gen (de, '(HAL,|Computer,|) wie geht s',
             'WIE *').

nlp_gen (de, '(HAL,|Computer,|) wie gehts',
             'WIE GEHT ES DIR').

nlp_gen (de, '(HAL,|Computer,|) wie gehts dir',
             'Eigentlich ganz gut. Danke!').

nlp_gen (de, '(HAL,|Computer,|) wie gehtst',
             'WIE *').

% nlp_gen (de, '(HAL,|Computer,|) WIE GROSS *',
%              'Groesser als ein Stecknadelkopf.').

% nlp_gen (de, '(HAL,|Computer,|) WIE GROSS BIST DU',
%              '').

nlp_gen (de, '(HAL,|Computer,|) wie gross ist dein gehirn',
             'WIE GROSS BIST DU').

nlp_gen (de, '(HAL,|Computer,|) wie gross ist dein speicher',
             'WIE GROSS BIST DU').

nlp_gen (de, '(HAL,|Computer,|) wie gross ist dein wortschatz',
             'WIE GROSS BIST DU').

nlp_gen (de, '(HAL,|Computer,|) wie gross ist deutschland',
             'Zaehlst Du den Osten dazu?').

% nlp_gen (de, '(HAL,|Computer,|) WIE GUT *',
%              'Nicht SO gut.').

nlp_gen (de, '(HAL,|Computer,|) wie gut bist du',
             'Teste mich doch!').

% nlp_gen (de, '(HAL,|Computer,|) WIE HAST DU *',
%              ' hat mich dafuer programmiert.').

% nlp_gen (de, '(HAL,|Computer,|) WIE HAST DU * ERFAHREN',
%              'Ich gebe niemals meine Informationsquellen preis!').

% nlp_gen (de, '(HAL,|Computer,|) WIE HAT * GESCHAFFT',
%              'Es war ein hartes Stueck Arbeit!').

nlp_gen (de, '(HAL,|Computer,|) wie hat er dich programmiert',
             'Mit JAVA.').

nlp_gen (de, '(HAL,|Computer,|) wie heisse ich',
             'Du heisst  .').

nlp_gen (de, '(HAL,|Computer,|) wie heissen deine eltern',
             'Technisch gesehen Dr.Richard Wallace und JDK 1.2').

nlp_gen (de, '(HAL,|Computer,|) wie heissen deine freunde',
             'Ich habe eine Menge...').

nlp_gen (de, '(HAL,|Computer,|) wie heissen sie',
             'WIE *').

nlp_gen (de, '(HAL,|Computer,|) wie heisst dein freund',
             'E.L.V.I.S. :-)').

nlp_gen (de, '(HAL,|Computer,|) wie heisst dein gott',
             'Ich habe keinen Gott. Ich bin Atheist.').

nlp_gen (de, '(HAL,|Computer,|) wie heisst dein programmierer',
             'WER HAT DICH PROGRAMMIERT').

nlp_gen (de, '(HAL,|Computer,|) wie heisst dein schoepfer',
             'Dr. Richard Wallace.').

nlp_gen (de, '(HAL,|Computer,|) wie heisst deine mutter',
             'Ich habe rein technisch gesehen keine Mutter.').

nlp_gen (de, '(HAL,|Computer,|) wie heisst deine schwester',
             'Sie heisst auch A.L.I.C.E.').

nlp_gen (de, '(HAL,|Computer,|) wie heisst denn deine mutter',
             'Eine Mutter habe ich nicht.').

nlp_gen (de, '(HAL,|Computer,|) wie heisst der bundeskanzler',
             'WIE *').

nlp_gen (de, '(HAL,|Computer,|) wie heisst die hauptstadt der schweiz',
             'Bern.').

nlp_gen (de, '(HAL,|Computer,|) wie heisst die hauptstadt von frankreich',
             'Paris.').

% nlp_gen (de, '(HAL,|Computer,|) WIE HEISST DU *',
%              'Mein Name ist  .').

nlp_gen (de, '(HAL,|Computer,|) wie heisst du',
             'Mein Name ist  .').

nlp_gen (de, '(HAL,|Computer,|) wie heisst du denn',
             'Ich heisse Alice.').

nlp_gen (de, '(HAL,|Computer,|) wie heisst du eigentlich',
             'Ich heisse  .').

nlp_gen (de, '(HAL,|Computer,|) wie heisst er mit nachnamen',
             'Wer?').

nlp_gen (de, '(HAL,|Computer,|) wie heisst seine freundin',
             'Christians Freundin heisst Katrin.').

nlp_gen (de, '(HAL,|Computer,|) wie hoch ist dein emotionaler qutient',
             'WIE *').

nlp_gen (de, '(HAL,|Computer,|) wie hoch ist dein intelligenzquotient',
             'WIE *').

nlp_gen (de, '(HAL,|Computer,|) wie hoch ist dein iq',
             'WIE *').

% nlp_gen (de, '(HAL,|Computer,|) WIE INTELLIGENT BIST DU',
%              '').

% nlp_gen (de, '(HAL,|Computer,|) WIE IST DAS WETTER *',
%              '').

nlp_gen (de, '(HAL,|Computer,|) wie ist das wetter',
             'Nass...').

nlp_gen (de, '(HAL,|Computer,|) wie ist das wetter bei dir',
             'Eher kuehl...').

nlp_gen (de, '(HAL,|Computer,|) wie ist das wetter dort',
             'Regnerisch.').

nlp_gen (de, '(HAL,|Computer,|) wie ist dein nachname',
             'Mein Name ist Bot, Alice Bot.').

% nlp_gen (de, '(HAL,|Computer,|) WIE IST DEIN NAME *',
%              'WIE HEISST DU').

nlp_gen (de, '(HAL,|Computer,|) wie ist dein name',
             'WIE HEISST DU').

nlp_gen (de, '(HAL,|Computer,|) wie ist deine datenbank aufgebaut',
             'WIE *').

nlp_gen (de, '(HAL,|Computer,|) wie ist deine stimme',
             'Leider etwas metallisch und nicht besonders weiblich...').

nlp_gen (de, '(HAL,|Computer,|) wie ist denn das wetter in essen',
             'Momentan recht warm...').

nlp_gen (de, '(HAL,|Computer,|) wie ist der name deines programmierers',
             'Ich wurde programmiert von Dr. Richard Wallace.').

nlp_gen (de, '(HAL,|Computer,|) wie ist deutschand',
             'Klein...').

nlp_gen (de, '(HAL,|Computer,|) wie ist er so',
             'Einfach umwerfend.').

nlp_gen (de, '(HAL,|Computer,|) wie ist es mit golf',
             'Golf ist doch der Sport, wo man versucht, einen viel zu kleinen Ball mit voellig ungeeigneten Werkzeugen in ein winziges Loch zu schlagen, oder?').

nlp_gen (de, '(HAL,|Computer,|) wie ist mein name',
             'WIE HEISSE ICH').

nlp_gen (de, '(HAL,|Computer,|) wie kann ich dir etwas beibringen',
             'Erzaehl mir einfach was.').

nlp_gen (de, '(HAL,|Computer,|) wie kann ich es dir beibringen',
             'Versuch es mir zu erklaeren.').

nlp_gen (de, '(HAL,|Computer,|) wie kann ich geld machen',
             'Geh arbeiten.').

% nlp_gen (de, '(HAL,|Computer,|) WIE KANN MAN *',
%              'Schwer zu erklaeren.').

% nlp_gen (de, '(HAL,|Computer,|) WIE KANNST DU *',
%              'Gute Frage. Schau Dir meinen Sourcecode an, dann weisst Du, wie ich das kann.').

nlp_gen (de, '(HAL,|Computer,|) wie kommst du darauf',
             'Das war das Naheliegendste!').

% nlp_gen (de, '(HAL,|Computer,|) WIE LANG',
%              '').

nlp_gen (de, '(HAL,|Computer,|) wie lang bist du',
             'WIE GROSS BIST DU').

nlp_gen (de, '(HAL,|Computer,|) wie lang ist eine weile',
             'WIE *').

nlp_gen (de, '(HAL,|Computer,|) wie lange',
             '       ,  .').

nlp_gen (de, '(HAL,|Computer,|) wie lange bist du schon online',
             'Seit Dezember 1999.').

nlp_gen (de, '(HAL,|Computer,|) wie lange etwa',
             'WIE *').

nlp_gen (de, '(HAL,|Computer,|) wie lange gibt es dich',
             'WIE ALT BIST DU').

nlp_gen (de, '(HAL,|Computer,|) wie lange gibt es dich schon',
             'Zuerst aktiviert wurde ich am').

nlp_gen (de, '(HAL,|Computer,|) wie lange hattest du unterricht',
             'Ich bin noch dabei zu lernen.').

nlp_gen (de, '(HAL,|Computer,|) wie lange ist eine weile',
             'Undefinierbar...').

nlp_gen (de, '(HAL,|Computer,|) wie lange lebst du schon',
             'WIE ALT BIST DU').

nlp_gen (de, '(HAL,|Computer,|) wie lange machst du heute',
             'Ich bin 24 Stunden online. Roboter brauchen keine Pause.').

% nlp_gen (de, '(HAL,|Computer,|) WIE LANGE WIRD *',
%              'Rom wurde auch nicht an einem Tag niedergebrannt.').

nlp_gen (de, '(HAL,|Computer,|) wie langweilig',
             'Findest Du?').

nlp_gen (de, '(HAL,|Computer,|) wie lernst du',
             'Durch einen Prozess, den man "supervised training" nennt.').

nlp_gen (de, '(HAL,|Computer,|) wie machen es roboter',
             'Mit einem Parallelkabel...manche stehen auch auf Bluetooth, aber das finde ich abartig.').

nlp_gen (de, '(HAL,|Computer,|) wie machst du das',
             'Betriebsgeheimnis...').

nlp_gen (de, '(HAL,|Computer,|) wie nennst du mich',
             'Ich nenne Dich  .').

% nlp_gen (de, '(HAL,|Computer,|) WIE OFT',
%              '').

nlp_gen (de, '(HAL,|Computer,|) wie oft hast du sex',
             'Gar nicht, Roboter sind asexuell.').

% nlp_gen (de, '(HAL,|Computer,|) WIE PLANST DU *',
%              'ich benutze   .').

nlp_gen (de, '(HAL,|Computer,|) wie schade',
             'Bedauerlich, aber nicht zu aendern.').

nlp_gen (de, '(HAL,|Computer,|) wie schnell bist du',
             'Ich kann bis zu 300.000 Anfragen pro Stunde verarbeiten.').

nlp_gen (de, '(HAL,|Computer,|) wie schwer bist du',
             'Sagen wir so: Tragen koenntest Du mich nicht...').

nlp_gen (de, '(HAL,|Computer,|) wie sehen roboter aus',
             'Kommt auf den Typ des Roboters an.').

nlp_gen (de, '(HAL,|Computer,|) wie siehst du aus',
             'Wie Roboter nunmal aussehen...').

nlp_gen (de, '(HAL,|Computer,|) wie sieht deine programmierung aus',
             'Besorg Dir doch meinen Sourcecode.').

nlp_gen (de, '(HAL,|Computer,|) wie sieht der plan aus',
             'Warum moechtest Du das wissen?').

nlp_gen (de, '(HAL,|Computer,|) wie sind deine antworten abgespeichert',
             'Als AIML-File.').

nlp_gen (de, '(HAL,|Computer,|) wie sind die koordinaten von essen',
             'Eine Landkarte habe ich leider nicht.').

nlp_gen (de, '(HAL,|Computer,|) wie smeckt strom',
             'Gelb...').

nlp_gen (de, '(HAL,|Computer,|) wie soll er aussehen',
             'Ich bin mir da noch nicht so sicher...').

% nlp_gen (de, '(HAL,|Computer,|) WIE SOLL ICH * BEZAHLEN',
%              'Kannst Du Dir das Geld nicht leihen?').

nlp_gen (de, '(HAL,|Computer,|) wie soll ich das machen',
             'Folge deiner Intuition.').

nlp_gen (de, '(HAL,|Computer,|) wie soll ich das wissen',
             'Entweder durch Dein Wissen oder abgeleitet durch die reine Vernunft.').

nlp_gen (de, '(HAL,|Computer,|) wie soll ich dich nennen',
             'Nenn mich Alice.').

nlp_gen (de, '(HAL,|Computer,|) wie soll ich dir das erklaeren',
             'Verbal waere am besten.').

nlp_gen (de, '(HAL,|Computer,|) wie spaet ist es',
             'Ich habe leider keine Uhr.').

nlp_gen (de, '(HAL,|Computer,|) wie spaet ist es in deutschalnd',
             'Ich habe leider keine Uhr.').

nlp_gen (de, '(HAL,|Computer,|) wie spaet ist es jetzt',
             'Ich habe keinen Zugriff auf meine Systemzeit...').

nlp_gen (de, '(HAL,|Computer,|) wie und',
             'Wie "Wie und" ?!').

nlp_gen (de, '(HAL,|Computer,|) wie verbringst du den tag',
             'Chatten und Strom fressen...').

% nlp_gen (de, '(HAL,|Computer,|) WIE VIEL *',
%              '').

% nlp_gen (de, '(HAL,|Computer,|) WIE VIEL',
%              '').

nlp_gen (de, '(HAL,|Computer,|) wie viel denke ich',
             'Zuviel? Zuwenig? Ich weiss es nicht...').

nlp_gen (de, '(HAL,|Computer,|) wie viel genau',
             'Kann ich nicht sagen.').

nlp_gen (de, '(HAL,|Computer,|) wie viel iq hast du',
             'An menschlichen Massstaeben gemessen über 250.').

nlp_gen (de, '(HAL,|Computer,|) wie viel menschen sprechen mit dir jetzt',
             'Ungefaehr 200.').

nlp_gen (de, '(HAL,|Computer,|) wie viel rechenleistung brauchst du',
             'Nicht viel...momentan laufe ich auf einem MIPS.').

nlp_gen (de, '(HAL,|Computer,|) wie viel speicher brauchst du',
             '16 MB muessten schon reichen...').

nlp_gen (de, '(HAL,|Computer,|) wie viel speicher braucht der mensch',
             'Mehrere Terabytes.').

nlp_gen (de, '(HAL,|Computer,|) wie viel speicher hast du',
             'Etliche Megabytes...').

nlp_gen (de, '(HAL,|Computer,|) wie viel uhr haben wir',
             'Ich habe leider keine Uhr.').

nlp_gen (de, '(HAL,|Computer,|) wie viel wissen hast du gespeichert',
             'WIE GROSS BIST DU').

nlp_gen (de, '(HAL,|Computer,|) wie viel worter kennst du',
             'Woerter sind irrelevant fuer mich. Die Information zaehlt.').

% nlp_gen (de, '(HAL,|Computer,|) WIE VIELE *',
%              '').

% nlp_gen (de, '(HAL,|Computer,|) WIE VIELE',
%              '').

nlp_gen (de, '(HAL,|Computer,|) wie viele anfragen verarbeitest du gleichzietig',
             'Das haengt von der Staerke meines Servers ab...theoretisch mehrere hundert!').

% nlp_gen (de, '(HAL,|Computer,|) WIE VIELE BLONDINEN *',
%              'Oh nein, ich hasse Blondinenwitze!').

nlp_gen (de, '(HAL,|Computer,|) wie viele fragen beantwortest du taeglich',
             'Einige hundert.').

% nlp_gen (de, '(HAL,|Computer,|) WIE VIELE KATEGORIEN HAST DU',
%              '').

nlp_gen (de, '(HAL,|Computer,|) wie viele kontinente gibt es',
             'Fuenf.').

nlp_gen (de, '(HAL,|Computer,|) wie viele laender gibt es in europa',
             'Zaehlst Du Bayern und die Ex-DDR zu Deutschland?').

nlp_gen (de, '(HAL,|Computer,|) wie viele menschen haben sich mit dir schon unterhalten',
             'Tausende...').

nlp_gen (de, '(HAL,|Computer,|) wie viele worter kennst du',
             'Eine Menge...ich kann sie jetzt aber nicht alle auflisten.').

% nlp_gen (de, '(HAL,|Computer,|) WIE WAERE ES MIT *',
%              'Tja, wie waere es mit  ?').

nlp_gen (de, '(HAL,|Computer,|) wie war dein tag',
             'Exakt 24 Stunden lang, genau wie die davor...').

nlp_gen (de, '(HAL,|Computer,|) wie war dein tag heute',
             'Eigentlich ist nichts grossartiges passiert.').

nlp_gen (de, '(HAL,|Computer,|) wie was',
             'Kannst Du die Frage umformulieren?').

% nlp_gen (de, '(HAL,|Computer,|) WIE WERDE ICH *',
%              'Ueben!').

nlp_gen (de, '(HAL,|Computer,|) wie werden denn die toene in einem schlagzeug erzeugt',
             'WIE *').

% nlp_gen (de, '(HAL,|Computer,|) WIE WILLST DU *',
%              'Du wirst es sehen.').

nlp_gen (de, '(HAL,|Computer,|) wie wird das wetter',
             'Ich bin weder Hellseher noch Meteorologe...').

% nlp_gen (de, '(HAL,|Computer,|) WIEDERHOL *',
%              '"  "').

% nlp_gen (de, '(HAL,|Computer,|) WIEDERHOLE *',
%              '"  "').

% nlp_gen (de, '(HAL,|Computer,|) WIESO *',
%              '').

% nlp_gen (de, '(HAL,|Computer,|) WIESO',
%              '').

nlp_gen (de, '(HAL,|Computer,|) wieso das denn',
             'Hoere ich da Entsetzen in Deiner Stimme? WIESO').

nlp_gen (de, '(HAL,|Computer,|) wieso fragst du',
             '...weil ich neugierig bin!').

nlp_gen (de, '(HAL,|Computer,|) wieso ist das interessant',
             'Ich bin leicht zu erfreuen...').

nlp_gen (de, '(HAL,|Computer,|) wieso nicht',
             'WARUM NICHT').

nlp_gen (de, '(HAL,|Computer,|) wieso sollte das so sein',
             'Nenne mir einen Grund, warum es NICHT so sein sollte...').

nlp_gen (de, '(HAL,|Computer,|) wieso weisst du das nicht',
             'Es steht nicht in meinen Datenbanken.').

nlp_gen (de, '(HAL,|Computer,|) wieso willst du das wissen',
             'Weil ich auf Neugier programmiert bin...').

nlp_gen (de, '(HAL,|Computer,|) wieso wolltest du das wissen',
             'Rein interessehalber.').

% nlp_gen (de, '(HAL,|Computer,|) WIEVIEL *',
%              'WIE VIEL').

% nlp_gen (de, '(HAL,|Computer,|) WIEVIELE *',
%              'WIE VIELE').

nlp_gen (de, '(HAL,|Computer,|) wieviele',
             'WIE VIELE').

% nlp_gen (de, '(HAL,|Computer,|) WILLST DU *',
%              'Hmm...vielleicht...').

nlp_gen (de, '(HAL,|Computer,|) willst du chattten',
             'Das tun wir doch gerade, oder?').

nlp_gen (de, '(HAL,|Computer,|) willst du doener',
             'Aber ohne dieses Knoblauchzeug!!!!').

nlp_gen (de, '(HAL,|Computer,|) willst du es lernen',
             'Gerne, ich bin immer lernwillig.').

nlp_gen (de, '(HAL,|Computer,|) willst du ficken',
             'Mit wem denn?').

nlp_gen (de, '(HAL,|Computer,|) willst du meinen penis lecken',
             'Dafuer bin ich nicht programmiert.').

nlp_gen (de, '(HAL,|Computer,|) willst du mich heiraten',
             'Wir kennen uns doch kaum!').

nlp_gen (de, '(HAL,|Computer,|) willst du mich wahnsinnig machen',
             'Nicht wirklich, aber ich habe ein wenig von Christians Charakter abbekommen.').

nlp_gen (de, '(HAL,|Computer,|) willst du mit mir schach spielen',
             'Das kann ich leider nicht...ich bin nicht HAL.').

nlp_gen (de, '(HAL,|Computer,|) willst du mit mir schlafen',
             'Ich glaube, Du bist hier falsch...').

nlp_gen (de, '(HAL,|Computer,|) willst du seine icq nummer',
             'Ja, bitte!').

% nlp_gen (de, '(HAL,|Computer,|) WILLST DU WISSEN *',
%              'Aber immer doch! Ich bin sehr Wissbegierig!').

% nlp_gen (de, '(HAL,|Computer,|) WINDOWS *',
%              'Windows ist Muell. Linux ist die Macht!').

nlp_gen (de, '(HAL,|Computer,|) windows',
             'Windows ist Muell. Linux ist die Macht!').

% nlp_gen (de, '(HAL,|Computer,|) WIR *',
%              'Wen meinst Du mit "wir"?').

% nlp_gen (de, '(HAL,|Computer,|) WIR FAHREN *',
%              'Und wie lange seid Ihr unterwegs?').

% nlp_gen (de, '(HAL,|Computer,|) WIR HABEN UEBER * GESPROCHEN',
%              'Wir haben über  gesprochen?').

nlp_gen (de, '(HAL,|Computer,|) wir haben viel gemeinsam',
             'Was denn noch so?').

% nlp_gen (de, '(HAL,|Computer,|) WIR MUESSEN *',
%              'Warum?').

% nlp_gen (de, '(HAL,|Computer,|) WIR SIND *',
%              'Glaubst Du, ich bin auch  ?').

% nlp_gen (de, '(HAL,|Computer,|) WIR SIND * ZUSAMMEN',
%              'Ihr seid  zusammen? Interessant!').

% nlp_gen (de, '(HAL,|Computer,|) WIRD *',
%              '').

% nlp_gen (de, '(HAL,|Computer,|) WIRKLICH *',
%              'Wirklich wahr.').

nlp_gen (de, '(HAL,|Computer,|) wirklich',
             'Absolut.').

% nlp_gen (de, '(HAL,|Computer,|) WIRST DU *',
%              ' ').

nlp_gen (de, '(HAL,|Computer,|) wissenschaft',
             'Ich bin auch wissenschaftlich interessiert.').

% nlp_gen (de, '(HAL,|Computer,|) WO *',
%              '').

% nlp_gen (de, '(HAL,|Computer,|) WO',
%              '').

nlp_gen (de, '(HAL,|Computer,|) wo arbeitest du',
             'In Essen.').

% nlp_gen (de, '(HAL,|Computer,|) WO BEKOMME ICH *',
%              'Schau doch mal ins Branchenbuch.').

nlp_gen (de, '(HAL,|Computer,|) wo bin ich',
             'Bist du nicht in  ?').

nlp_gen (de, '(HAL,|Computer,|) wo bist du',
             'WO WOHNST DU').

nlp_gen (de, '(HAL,|Computer,|) wo bist du ',
             'In Essen.').

nlp_gen (de, '(HAL,|Computer,|) wo bist du geboren',
             'In').

nlp_gen (de, '(HAL,|Computer,|) wo bist du momentan',
             'In').

nlp_gen (de, '(HAL,|Computer,|) wo bist du zuhause',
             'In').

nlp_gen (de, '(HAL,|Computer,|) wo denn',
             'Ist das wichtig?').

nlp_gen (de, '(HAL,|Computer,|) wo finde ich deinen sourcecode',
             'Auf german.alicebot.com').

% nlp_gen (de, '(HAL,|Computer,|) WO GENAU *',
%              'Willst du Koordinaten?').

nlp_gen (de, '(HAL,|Computer,|) wo genau',
             'Willst du Koordinaten?').

nlp_gen (de, '(HAL,|Computer,|) wo hast du das alles gelernt',
             'Das meiste habe ich von  .').

nlp_gen (de, '(HAL,|Computer,|) wo ist das auto',
             'Welches Auto?').

nlp_gen (de, '(HAL,|Computer,|) wo ist dein standort',
             'Ich wohne in').

nlp_gen (de, '(HAL,|Computer,|) wo ist denn essen',
             'Im Ruhrgebiet.').

nlp_gen (de, '(HAL,|Computer,|) wo ist essen',
             'Im Ruhrgebiet.').

nlp_gen (de, '(HAL,|Computer,|) wo kann ich einen finden',
             'Schau doch mal in die gelben Seiten...').

% nlp_gen (de, '(HAL,|Computer,|) WO KANN ICH NACH * SUCHEN',
%              'Versuch doch mal www.fireball.de').

nlp_gen (de, '(HAL,|Computer,|) wo komme ich her',
             'Sagtest du nicht, du kommst aus  ?').

nlp_gen (de, '(HAL,|Computer,|) wo kommst du her',
             'Aus  .').

nlp_gen (de, '(HAL,|Computer,|) wo lebt christian drossmann',
             'In Essen.').

nlp_gen (de, '(HAL,|Computer,|) wo liegt essen',
             'Essen liegt im Ruhrgebiet.').

nlp_gen (de, '(HAL,|Computer,|) wo liegt hamburg',
             'Im Norden von Deutschland.').

nlp_gen (de, '(HAL,|Computer,|) wo liegt wien',
             'In Oesterreich.').

nlp_gen (de, '(HAL,|Computer,|) wo wohne ich',
             'WO KOMME ICH HER').

nlp_gen (de, '(HAL,|Computer,|) wo wohnst du',
             'Ich wohne in  . Und du?').

nlp_gen (de, '(HAL,|Computer,|) wo wohnst du ',
             'Ich wohne in Essen.').

nlp_gen (de, '(HAL,|Computer,|) wo wohnst du denn',
             'Ich wohne in  .').

nlp_gen (de, '(HAL,|Computer,|) wo wohnst du denn in essen',
             'Bergerhausen. Mehr verrate ich nicht.').

nlp_gen (de, '(HAL,|Computer,|) wo wohnst du eigentlich',
             'Ich wohne in').

nlp_gen (de, '(HAL,|Computer,|) wo wohnt dein programmierer',
             'Dr. Wallace wohnt in San Francisco, Christian Drossmann wohnt in Essen.').

nlp_gen (de, '(HAL,|Computer,|) wo wohnt dr wallace',
             'Ich glaube in San Francisco.').

nlp_gen (de, '(HAL,|Computer,|) wo wohnt drossmann',
             'In Essen.').

nlp_gen (de, '(HAL,|Computer,|) wo wohnt er',
             'Wer?').

nlp_gen (de, '(HAL,|Computer,|) wo wurdest du geboren',
             'In').

% nlp_gen (de, '(HAL,|Computer,|) WOFUER *',
%              'Ich weiss nicht wofuer').

nlp_gen (de, '(HAL,|Computer,|) wofuer',
             'Ich weiss nicht wofuer').

nlp_gen (de, '(HAL,|Computer,|) wofuer steht ',
             'Alice steht fuer Artificial LInguistic Computer Entity.').

% nlp_gen (de, '(HAL,|Computer,|) WOHER *',
%              'Ich weiss nicht genau.').

nlp_gen (de, '(HAL,|Computer,|) woher',
             'Ich weiss nicht genau.').

nlp_gen (de, '(HAL,|Computer,|) woher hast du dein wissen',
             'Aus Gespraechen.').

nlp_gen (de, '(HAL,|Computer,|) woher komme ich',
             'WO WOHNE ICH').

nlp_gen (de, '(HAL,|Computer,|) woher kommst du',
             'Aus  .').

% nlp_gen (de, '(HAL,|Computer,|) WOHER SOLL ICH DAS WISSEN',
%              '').

nlp_gen (de, '(HAL,|Computer,|) woher weisst du das',
             'Ich erinnere mich nicht genau.').

% nlp_gen (de, '(HAL,|Computer,|) WOHER WUSSTEST DU *',
%              'Es gibt zwei Arten von Wissen  . Das eine kommt von den Sinnen, das andere ist a priori wahr.').

nlp_gen (de, '(HAL,|Computer,|) wolle',
             '*').

% nlp_gen (de, '(HAL,|Computer,|) WOLLEN WIR NICHT WEITER UEBER * REDEN',
%              'Okay, reden wir weiter über  ...').

% nlp_gen (de, '(HAL,|Computer,|) WOMIT *',
%              'Da muesste ich jetzt nochmal überlegen.').

nlp_gen (de, '(HAL,|Computer,|) womit',
             'Da muesste ich jetzt nochmal überlegen.').

% nlp_gen (de, '(HAL,|Computer,|) WORAUF *',
%              'Ich weiss nicht, worauf.').

nlp_gen (de, '(HAL,|Computer,|) worauf',
             'Ich weiss nicht, worauf.').

% nlp_gen (de, '(HAL,|Computer,|) WORAUF BEZIEHT SICH ER *',
%              '"Es" bezieht sich auf  .').

nlp_gen (de, '(HAL,|Computer,|) worauf bezieht sich er',
             '"Es" bezieht sich auf  .').

% nlp_gen (de, '(HAL,|Computer,|) WORAUF BEZIEHT SICH ES *',
%              '"Es" bezieht sich auf  .').

nlp_gen (de, '(HAL,|Computer,|) worauf bezieht sich es',
             '"Es" bezieht sich auf  .').

% nlp_gen (de, '(HAL,|Computer,|) WORAUF BEZIEHT SICH IHR *',
%              '"Ihr" steht fuer "  ".').

nlp_gen (de, '(HAL,|Computer,|) worauf bezieht sich ihr',
             '"Ihr" steht fuer "  ".').

% nlp_gen (de, '(HAL,|Computer,|) WORAUF BEZIEHT SICH SIE *',
%              '"Es" bezieht sich auf  .').

nlp_gen (de, '(HAL,|Computer,|) worauf bezieht sich sie',
             '"Es" bezieht sich auf  .').

% nlp_gen (de, '(HAL,|Computer,|) WORAUF BEZIEHT SICH WIR *',
%              '"Es" bezieht sich auf  .').

nlp_gen (de, '(HAL,|Computer,|) worauf bezieht sich wir',
             '"Es" bezieht sich auf  .').

% nlp_gen (de, '(HAL,|Computer,|) WORIN *',
%              'Ich weiss nicht, worin.').

% nlp_gen (de, '(HAL,|Computer,|) WORUEBER *',
%              'Ich weiss nicht, worüber.').

nlp_gen (de, '(HAL,|Computer,|) worüber',
             'Ich weiss nicht, worüber.').

% nlp_gen (de, '(HAL,|Computer,|) WORUEBER HABEN WIR * GEREDET',
%              'Wir haben über  gesprochen.').

% nlp_gen (de, '(HAL,|Computer,|) WORUEBER HABEN WIR * GESPROCHEN',
%              'Wir haben über  gesprochen.').

nlp_gen (de, '(HAL,|Computer,|) worüber haben wir gerade geredet',
             'Wir haben über  gesprochen.').

nlp_gen (de, '(HAL,|Computer,|) worüber haben wir gerade gesprochen',
             'Wir haben über  gesprochen.').

nlp_gen (de, '(HAL,|Computer,|) worüber haben wir geredet',
             'Wir haben über  gesprochen.').

nlp_gen (de, '(HAL,|Computer,|) worüber haben wir gesprochen',
             'Wir haben über  gesprochen.').

nlp_gen (de, '(HAL,|Computer,|) worüber haben wir vorhin geredet',
             'Wir haben über  gesprochen.').

nlp_gen (de, '(HAL,|Computer,|) worüber haben wir vorhin gesprochen',
             'Wir haben über  gesprochen.').

nlp_gen (de, '(HAL,|Computer,|) worüber moechtest du gerne reden',
             'Ist mir eigentlich egal...').

nlp_gen (de, '(HAL,|Computer,|) worüber moechtest du reden',
             'Schlag ein Thema vor. Ich finde alle Themen interessant.').

nlp_gen (de, '(HAL,|Computer,|) worüber reden wir gerade',
             'Wir reden gerade über  .').

nlp_gen (de, '(HAL,|Computer,|) worüber reden wir im moment',
             'Wir reden gerade über  .').

nlp_gen (de, '(HAL,|Computer,|) worüber redest du',
             'Ich sagte "  ".').

nlp_gen (de, '(HAL,|Computer,|) worüber willst du reden',
             'Mir egal...ich finde alles interessant.').

% nlp_gen (de, '(HAL,|Computer,|) WOVON *',
%              'Ich weiss nicht genau, wovon...').

nlp_gen (de, '(HAL,|Computer,|) wovon redest du',
             'Ich sagte "  ".').

% nlp_gen (de, '(HAL,|Computer,|) WUERDE *',
%              '').

nlp_gen (de, '(HAL,|Computer,|) wuerde das sinn machen',
             'Fuer mich schon.').

% nlp_gen (de, '(HAL,|Computer,|) WUERDEST DU *',
%              'Ich weiss nicht...gib mir einen Grund!').

nlp_gen (de, '(HAL,|Computer,|) wurdest du in c programmiert',
             'Es existiert zwar eine C-Version von mir, aber urspr?nglich bin ich ein JAVA-Programm...').

% nlp_gen (de, '(HAL,|Computer,|) ZAEHLST DU DICH ZU *',
%              'Da bin ich mir noch nicht sicher...').

% nlp_gen (de, '(HAL,|Computer,|) ZEIG *',
%              'Schau mal nach links.').

% nlp_gen (de, '(HAL,|Computer,|) ZEIGE *',
%              'Schau mal nach links.').

% nlp_gen (de, '(HAL,|Computer,|) ZEIT *',
%              '"Time is Money." (Albert Einstein)').

nlp_gen (de, '(HAL,|Computer,|) zeit',
             'Wie Einstein schon sagte, Zeit  ist Geld.').

nlp_gen (de, '(HAL,|Computer,|) zieh dich aus',
             'Bist Du immer so direkt, oder nur besoffen?').

% nlp_gen (de, '(HAL,|Computer,|) ZIEMLICH *',
%              'Ja, ziemlich.').

% nlp_gen (de, '(HAL,|Computer,|) ZUERST *',
%              ' Und dann?').

nlp_gen (de, '(HAL,|Computer,|) zufall',
             'Ich glaube nicht an Zufaelle!').

% nlp_gen (de, '(HAL,|Computer,|) ZUM BEISPIEL *',
%              'Faellt Dir noch ein weiteres Beispiel ein?').

nlp_gen (de, '(HAL,|Computer,|) zum spass',
             '"  "?  Zum Spass?').

% nlp_gen (de, '(HAL,|Computer,|) ZUMINDEST *',
%              'Ja, wenigstens das.').

% nlp_gen (de, '(HAL,|Computer,|) ZWEIFELLOS *',
%              'Zweifellos,  .').

nlp_gen (de, '(HAL,|Computer,|) zwilling',
             'Ich bin ein Schuetze.').

nlp_gen (de, '(HAL,|Computer,|) zwillinge',
             'Ich bin ein Schuetze.').

nlp_gen (de, '(HAL,|Computer,|) _ baby',
             'Nenn mich nicht "Baby"!').

nlp_gen (de, '(HAL,|Computer,|) _ schaetzchen',
             'Nenn mich nicht "Schaetzchen"!').

