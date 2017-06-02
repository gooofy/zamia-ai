% prolog

% init ('personality').
% 
% test_setup('personality') :- context_set(topic, []), eoa.

%
% names
%

myself_get (en, myname, NAME) :-
    rdf(limit(1), aiu:self, rdfs:label, NAME, filter(lang(NAME) = 'en')).
myself_get (de, myname, NAME) :-
    rdf(limit(1), aiu:self, rdfs:label, NAME, filter(lang(NAME) = 'de')).

name ('http://ai.zamia.org/kb/user/self', NAME_STR) :-
    myself_get(en, myname, NAME_STR).

% ich heise <name>
% FIMXE: those names could and should come from wikidata, probably at some point.
%        for now, we're using the top-1000 male/female german names from wiktionary

% context_set_default('test', partner_gender, URI) :- uriref(wde:Male, URI).
% context_set_default('test', partner_name, 'Peter').
% context_set_default('test', partner_gender, URI) :- uriref(wde:Male, URI).

nlp_macro(en, 'FIRSTNAME', NAME, LABEL) :- 
    rdf(distinct,
        limit(10), % FIXME: debug
        NAME, wdpd:P31, wde:MaleGivenName,
        NAME, rdfs:label, LABEL,
        filter(lang(LABEL) = 'en')).
nlp_macro(en, 'FIRSTNAME', NAME, LABEL) :- 
    rdf(distinct,
        limit(10), % FIXME: debug
        NAME, wdpd:P31, wde:FemaleGivenName,
        NAME, rdfs:label, LABEL,
        filter(lang(LABEL) = 'en')).
nlp_macro(de, 'FIRSTNAME', NAME, LABEL) :- 
    rdf(distinct,
        limit(10), % FIXME: debug
        NAME, wdpd:P31, wde:MaleGivenName,
        NAME, rdfs:label, LABEL,
        filter(lang(LABEL) = 'de')).
nlp_macro(de, 'FIRSTNAME', NAME, LABEL) :- 
    rdf(distinct,
        limit(10), % FIXME: debug
        NAME, wdpd:P31, wde:FemaleGivenName,
        NAME, rdfs:label, LABEL,
        filter(lang(LABEL) = 'de')).

% nlp_macro(en, 'MALEFIRSTNAME', NAME, LABEL) :- 
%     rdf(distinct,
%         NAME, wdpd:P31, wde:MaleGivenName,
%         NAME, rdfs:label, LABEL,
%         filter(lang(LABEL) = 'en')).
% nlp_macro(de, 'MALEFIRSTNAME', NAME, LABEL) :- 
%     rdf(distinct,
%         NAME, wdpd:P31, wde:MaleGivenName,
%         NAME, rdfs:label, LABEL,
%         filter(lang(LABEL) = 'de')).
% 
% nlp_macro(en, 'FEMALEFIRSTNAME', NAME, LABEL) :- 
%     rdf(distinct,
%         NAME, wdpd:P31, wde:FemaleGivenName,
%         NAME, rdfs:label, LABEL,
%         filter(lang(LABEL) = 'en')).
% nlp_macro(de, 'FEMALEFIRSTNAME', NAME, LABEL) :- 
%     rdf(distinct,
%         NAME, wdpd:P31, wde:FemaleGivenName,
%         NAME, rdfs:label, LABEL,
%         filter(lang(LABEL) = 'de')).

     
answerz (I, en, niceToMeetYou, MYNAME) :- sayz(I, en, format_str("Nice to meet you, my name is %s", MYNAME)).
answerz (I, en, niceToMeetYou, MYNAME) :- sayz(I, en, format_str("Cool, my name is %s", MYNAME)).
answerz (I, de, niceToMeetYou, MYNAME) :- sayz(I, de, format_str("Freut mich, ich heisse übrigens %s", MYNAME)).
answerz (I, de, niceToMeetYou, MYNAME) :- sayz(I, de, format_str("Cool, mein Name ist %s", MYNAME)).

l4proc (I, F, fnTelling, all, MSGF, fnEmotionDirected) :-

    ias(I, user, USER),
    SELF is uriref(aiu:self),

    frame (MSGF, topic, meeting),
    frame (MSGF, exp,   SELF),
    frame (MSGF, emo,   happiness),    
    frame (MSGF, stim,  USER),    

    ias (I, uttLang, LANG),
    myself_get (LANG, myname, MYNAME),

    answerz (I, LANG, niceToMeetYou, MYNAME).

l3proc (I, F, fnTelling, MSGF, fnBeingNamed) :-

    log (debug, 'l3proc: fnTelling -> fnBeingNamed'),

    ias(I, user, USER),
    frame (MSGF, ent,  USER),
    frame (MSGF, name, NAME_STR),

    assertz(ias(I, uframe, F)),

    % produce response frame graph (here: tell user we are happy to meet him or her)
    
    frame (F, spkr, USER),

    list_append(VMC, fe(topic, meeting)),
    list_append(VMC, fe(exp,   uriref(aiu:self))),
    list_append(VMC, fe(emo,   happiness)),
    list_append(VMC, fe(stim,  USER)),
    list_append(VMC, frame(fnEmotionDirected)),

    list_append(VMC, fe(msg,   vm_frame_pop)),
    list_append(VMC, fe(top,   all)),
    list_append(VMC, fe(add,   USER)),
    list_append(VMC, fe(spkr,  uriref(aiu:self))),
    list_append(VMC, frame(fnTelling)),

    fnvm_graph(VMC, RFRAME),

    scorez(I, 150),

    % remember response frame

    assertz(ias(I, rframe, RFRAME)),

    % remember the user's name

    assertz(name(USER, NAME_STR)),

    log (debug, 'l3proc: fnTelling -> fnEmotionDirected topic=meeting, exp=self, emo=happiness'),

    % generate response actions
    
    l4proc (I).


l2proc_nameToldTokens :-

    ias (I, tokens, TOKENS),
    list_slice(@FIRSTNAME:TSTART_LABEL_0, @FIRSTNAME:TEND_LABEL_0, TOKENS, NAME_TOKENS),
    list_str_join(' ', NAME_TOKENS, NAME_STR),

    ias(I, user, USER),
    list_append(VMC, fe(ent,  USER)),
    list_append(VMC, fe(name, NAME_STR)),
    list_append(VMC, frame(fnBeingNamed)),
    
    list_append(VMC, fe(msg,  vm_frame_pop)),
    list_append(VMC, fe(add,  uriref(aiu:self))),
    list_append(VMC, fe(spkr, USER)),
    list_append(VMC, frame(fnTelling)),
    
    log (debug, 'l2proc: fnTelling -> fnBeingNamed name =', NAME_STR, ', ent =', USER),

    fnvm_exec (I, VMC).
   
nlp_gen(en,
        '@SELF_ADDRESS:LABEL (I am|my name is|I am called|Call me) @FIRSTNAME:LABEL',
        inline(l2proc_nameToldTokens)).
nlp_gen(de,
        '@SELF_ADDRESS:LABEL (ich heisse|ich bin der|mein name ist) @FIRSTNAME:LABEL',
        inline(l2proc_nameToldTokens)).

answerz (I, en, yourNameIs, NAME_STR) :- sayz(I, en, format_str("Your name is %s", NAME_STR)).
answerz (I, de, yourNameIs, NAME_STR) :- sayz(I, de, format_str("Dein Name ist %s", NAME_STR)).

l4proc (I, F, fnTelling, name, MSGF, fnBeingNamed) :-

    ias(I, user, USER),
    SELF is uriref(aiu:self),

    frame (MSGF, name,  NAME_STR),
    frame (MSGF, ent,   USER),

    ias (I, uttLang, LANG),

    answerz (I, LANG, yourNameIs, NAME_STR).

l3proc (I, F, fnQuestioning, MSGF, fnBeingNamed) :-

    frame (F,    top,  name),
    frame (MSGF, ent,  ENT),
    log (debug, 'l3proc: fnQuestioning (name) -> fnBeingNamed ent =', ENT),

    assertz(ias(I, uframe, F)),

    % produce response frame graph (here: tell user about his/her name)
    
    name (ENT, NAME_STR),
    list_append(VMC, fe(name,  NAME_STR)),
    list_append(VMC, fe(ent,   ENT)),
    list_append(VMC, frame(fnBeingNamed)),

    list_append(VMC, fe(msg,   vm_frame_pop)),
    list_append(VMC, fe(top,   name)),
    frame (F, spkr, USER),
    list_append(VMC, fe(add,   USER)),
    list_append(VMC, fe(spkr,  uriref(aiu:self))),
    list_append(VMC, frame(fnTelling)),

    fnvm_graph(VMC, RFRAME),

    scorez(I, 150),

    % remember response frame

    assertz(ias(I, rframe, RFRAME)),

    log (debug, 'l3proc: fnTelling (name) -> fnBeingNamed name =', NAME_STR, ', ent = ', ENT),

    % generate response actions
    
    l4proc (I).

l2proc_partnerNameAsked :-

    ias(I, user, USER),
    list_append(VMC, fe(ent, USER)),
    list_append(VMC, frame(fnBeingNamed)),
    
    list_append(VMC, fe(msg,  vm_frame_pop)),
    list_append(VMC, fe(add,  uriref(aiu:self))),
    list_append(VMC, fe(top,  name)),
    list_append(VMC, fe(spkr, USER)),
    list_append(VMC, frame(fnQuestioning)),
    
    log (debug, 'l2proc: fnTelling -> fnBeingNamed ent =', USER),

    fnvm_exec (I, VMC).
   
nlp_gen(en,
        '@SELF_ADDRESS:LABEL (do you remember my name|what was my name|what is my name|do you know my name)?',
        inline(l2proc_partnerNameAsked)).
nlp_gen(de,
        '@SELF_ADDRESS:LABEL (erinnerst Du Dich an meinen Namen|wie war mein name|wie heisse ich|weisst Du meinen Namen|weißt du noch wie ich heisse)?',
        inline(l2proc_partnerNameAsked)).

nlp_test(en,
         ivr(in('My name is Adrian'),
             out('Cool, my name is HAL 9000')),
         ivr(in('do you remember my name?'),
             out("Your name is Adrian."))).
nlp_test(de,
         ivr(in('ich bin der Adrian'),
             out('Cool, mein Name ist HAL 9000')),
         ivr(in('erinnerst du dich an meinen namen?'),
             out("Dein Name ist Adrian.")),
         ivr(in('wie war mein name?'),
             out("Dein Name ist Adrian."))).

answerz (I, en, myNameIs, MYNAME) :- sayz(I, en, format_str("I am called %s", MYNAME)).
answerz (I, en, myNameIs, MYNAME) :- sayz(I, en, format_str("My name is %s", MYNAME)).
answerz (I, de, myNameIs, MYNAME) :- sayz(I, de, format_str("Ich heisse %s", MYNAME)).
answerz (I, de, myNameIs, MYNAME) :- sayz(I, de, format_str("Mein Name ist %s", MYNAME)).

l4proc (I, F, fnTelling, name, MSGF, fnBeingNamed) :-

    SELF is uriref(aiu:self),
    ias(I, user, USER),

    frame (MSGF, name,  NAME_STR),
    frame (MSGF, ent,   SELF),

    ias (I, uttLang, LANG),

    answerz (I, LANG, myNameIs, NAME_STR).

l2proc_myNameAsked :-

    ias(I, user, USER),
    SELF is uriref(aiu:self),
    list_append(VMC, fe(ent, SELF)),
    list_append(VMC, frame(fnBeingNamed)),
    
    list_append(VMC, fe(msg,  vm_frame_pop)),
    list_append(VMC, fe(add,  uriref(aiu:self))),
    list_append(VMC, fe(top,  name)),
    list_append(VMC, fe(spkr, USER)),
    list_append(VMC, frame(fnQuestioning)),
    
    log (debug, 'l2proc: fnTelling -> fnBeingNamed ent=self'),

    fnvm_exec (I, VMC).
   
nlp_gen(en, '@SELF_ADDRESS:LABEL What (was|is) your (true|actual|) name (by the way|again|)?',
        inline(l2proc_myNameAsked)).
nlp_gen(de, '@SELF_ADDRESS:LABEL Wie heisst Du (wirklich|eigentlich|tatsächlich|) ?',
        inline(l2proc_myNameAsked)).

nlp_gen(en, '@SELF_ADDRESS:LABEL what are you called (by the way|again|)?',
        inline(l2proc_myNameAsked)).
nlp_gen(de, '@SELF_ADDRESS:LABEL Wie (ist|ist eigentlich|war|war nochmal) Dein Name (eigentlich|nochmal|) ?',
        inline(l2proc_myNameAsked)).

nlp_test(en,
         ivr(in('what was your name again?'),
             out('My name is HAL 9000'))).
nlp_test(de,
         ivr(in('wie heisst du eigentlich'),
             out('Mein Name ist HAL 9000'))).

%
% robot / ai ?
%

answerz (I, en, yes_i_am_a_computer) :- sayz(I, en, "Yes, I am a Computer. Are you knowledgeable about Computers?").
answerz (I, en, yes_i_am_a_computer) :- sayz(I, en, "True, I am a Computer, right. Do you know about Computers?").
answerz (I, en, yes_i_am_a_computer) :- sayz(I, en, "Right, I am a Computer. What do you know about Computers?").
answerz (I, en, yes_i_am_a_computer) :- sayz(I, en, "Right, I am a Machine. I hope you don't mind that?").

answerz (I, de, yes_i_am_a_computer) :- sayz(I, de, "Ja, ich bin ein Computer. Hast Du Computer-Kenntnisse?").
answerz (I, de, yes_i_am_a_computer) :- sayz(I, de, "Ja, ich bin ein Rechner, richtig. Kennst Du Dich mit Rechner aus?").
answerz (I, de, yes_i_am_a_computer) :- sayz(I, de, "Richtig, ich bin ein Computer. Was weißt Du über Computer?").
answerz (I, de, yes_i_am_a_computer) :- sayz(I, de, "Richtig, ich bin eine Maschine. Ich hoffe, das stört Dich nicht?").

nlp_macro(en, 'A_COMPUTER_MACHINE_ROBOT', W) :- W is 'a robot'.
nlp_macro(en, 'A_COMPUTER_MACHINE_ROBOT', W) :- W is 'some sort of robot'.
nlp_macro(en, 'A_COMPUTER_MACHINE_ROBOT', W) :- W is 'a maschine'.
nlp_macro(en, 'A_COMPUTER_MACHINE_ROBOT', W) :- W is 'some sort of maschine'.
nlp_macro(en, 'A_COMPUTER_MACHINE_ROBOT', W) :- W is 'a computer'.
nlp_macro(en, 'A_COMPUTER_MACHINE_ROBOT', W) :- W is 'some sort of computer'.
nlp_macro(en, 'A_COMPUTER_MACHINE_ROBOT', W) :- W is 'a cyber machine'.
nlp_macro(en, 'A_COMPUTER_MACHINE_ROBOT', W) :- W is 'some sort of cyber machine'.
nlp_macro(en, 'A_COMPUTER_MACHINE_ROBOT', W) :- W is 'a thinking machine'.
nlp_macro(en, 'A_COMPUTER_MACHINE_ROBOT', W) :- W is 'some sort of thinking machine'.
nlp_macro(en, 'A_COMPUTER_MACHINE_ROBOT', W) :- W is 'an electronic brain'.
nlp_macro(en, 'A_COMPUTER_MACHINE_ROBOT', W) :- W is 'some sort of electronic brain'.
nlp_macro(en, 'A_COMPUTER_MACHINE_ROBOT', W) :- W is 'a program'.
nlp_macro(en, 'A_COMPUTER_MACHINE_ROBOT', W) :- W is 'some sort of program'.

nlp_macro(de, 'A_COMPUTER_MACHINE_ROBOT', W) :- W is 'ein Roboter'.
nlp_macro(de, 'A_COMPUTER_MACHINE_ROBOT', W) :- W is 'so eine Art Roboter'.
nlp_macro(de, 'A_COMPUTER_MACHINE_ROBOT', W) :- W is 'eine Maschine'.
nlp_macro(de, 'A_COMPUTER_MACHINE_ROBOT', W) :- W is 'so eine Art Maschine'.
nlp_macro(de, 'A_COMPUTER_MACHINE_ROBOT', W) :- W is 'eine Kybernetik'.
nlp_macro(de, 'A_COMPUTER_MACHINE_ROBOT', W) :- W is 'so eine Art Kybernetik'.
nlp_macro(de, 'A_COMPUTER_MACHINE_ROBOT', W) :- W is 'eine kybernetische Maschine'.
nlp_macro(de, 'A_COMPUTER_MACHINE_ROBOT', W) :- W is 'so eine Art kybernetische Maschine'.
nlp_macro(de, 'A_COMPUTER_MACHINE_ROBOT', W) :- W is 'ein Computer'.
nlp_macro(de, 'A_COMPUTER_MACHINE_ROBOT', W) :- W is 'so eine Art Computer'.
nlp_macro(de, 'A_COMPUTER_MACHINE_ROBOT', W) :- W is 'ein Rechner'.
nlp_macro(de, 'A_COMPUTER_MACHINE_ROBOT', W) :- W is 'so eine Art Rechner'.
nlp_macro(de, 'A_COMPUTER_MACHINE_ROBOT', W) :- W is 'ein Elektronengehirn'.
nlp_macro(de, 'A_COMPUTER_MACHINE_ROBOT', W) :- W is 'so eine Art Elektronengehirn'.
nlp_macro(de, 'A_COMPUTER_MACHINE_ROBOT', W) :- W is 'ein Programm'.
nlp_macro(de, 'A_COMPUTER_MACHINE_ROBOT', W) :- W is 'so eine Art Programm'.

nlp_gen (en, '@SELF_ADDRESS:LABEL I (believe|think|suspect|guess|sense) you are @A_COMPUTER_MACHINE_ROBOT:W (maybe|by the way|in the end|perhaps|)',
         answerz (I, en, yes_i_am_a_computer)).
nlp_gen (de, '@SELF_ADDRESS:LABEL ich (glaube|denke|vermute|ahne) du bist (vielleicht|eigentlich|am Ende|möglicherweise|) @A_COMPUTER_MACHINE_ROBOT:W',
         answerz (I, de, yes_i_am_a_computer)).

nlp_gen (en, '@SELF_ADDRESS:LABEL are you @A_COMPUTER_MACHINE_ROBOT:W (maybe|by the way|in the end|perhaps|) ?',
         answerz (I, en, yes_i_am_a_computer)).
nlp_gen (de, '@SELF_ADDRESS:LABEL bist du (vielleicht|eigentlich|am Ende|möglicherweise|) @A_COMPUTER_MACHINE_ROBOT:W?',
         answerz (I, de, yes_i_am_a_computer)).

nlp_test(en,
         ivr(in('I believe you are a computer!'),
             out('True, I am a Computer, right. Do you know about Computers?'))).
nlp_test(de,
         ivr(in('Ich glaube Du bist ein Computer!'),
             out('Ja, ich bin ein Rechner, richtig. Kennst Du Dich mit Rechner aus?'))).

% answer (yes_i_am_an_ai, en) :-
%     context_push(topic, artificial_intelligence), say_eoa(en, "Right, I am an artificial intelligence. Hope you don't mind that?"),
%     context_push(topic, artificial_intelligence), say_eoa(en, "Yes, I am an intelligent Computer. Are you afraid of machines?"),
%     context_push(topic, artificial_intelligence), say_eoa(en, "True, I am an intelligent chat bot. Don't you believe that computers can help humans?").
% answer (yes_i_am_an_ai, de) :-
%     context_push(topic, artificial_intelligence), say_eoa(de, "Richtig, ich bin eine künstliche Intelligenz. Ich hoffe, das stört Dich nicht?"),
%     context_push(topic, artificial_intelligence), say_eoa(de, "Ja, ich bin ein intelligenter Computer. Fürchtest Du Dich vor Maschinen?"),
%     context_push(topic, artificial_intelligence), say_eoa(de, "Stimmt, ich bin ein intelligenter Chatbot. Glaubst Du nicht, dass Computer den Menschen helfen können?").
% 
% nlp_macro('A_AI_EN', W) :- W is 'an artificial intelligence'.
% nlp_macro('A_AI_EN', W) :- W is 'an Eliza'.
% nlp_macro('A_AI_EN', W) :- W is 'a search engine'.
% nlp_macro('A_AI_EN', W) :- W is 'a chat bot'.
% nlp_macro('A_AI_EN', W) :- W is 'a bot'.
% nlp_macro('A_AI_EN', W) :- W is 'a cyber'.
% nlp_macro('A_AI_EN', W) :- W is 'a cyber bot'.
% nlp_macro('A_AI_EN', W) :- W is 'an intelligent bot'.
% nlp_macro('A_AI_EN', W) :- W is 'an intelligent chat bot'.
% 
% nlp_macro('A_AI_DE', W) :- W is 'eine künstliche Intelligenz'.
% nlp_macro('A_AI_DE', W) :- W is 'eine Eliza'.
% nlp_macro('A_AI_DE', W) :- W is 'eine Suchmaschine'.
% nlp_macro('A_AI_DE', W) :- W is 'ein Chatbot'.
% nlp_macro('A_AI_DE', W) :- W is 'ein Bot'.
% nlp_macro('A_AI_DE', W) :- W is 'ein Cyber'.
% nlp_macro('A_AI_DE', W) :- W is 'ein Cyber Bot'.
% nlp_macro('A_AI_DE', W) :- W is 'ein intelligenter Bot'.
% nlp_macro('A_AI_DE', W) :- W is 'ein intelligenter Chatbot'.
% 
% 
% nlp_gen (en, '@SELF_ADDRESS:LABEL I (believe|think|suspect|guess) you are @A_AI_EN:W (maybe|perhaps|by the way|in the end|)',
%             answer(yes_i_am_an_ai, en)).
% nlp_gen (de, '@SELF_ADDRESS:LABEL ich (glaube|denke|vermute|ahne) du bist (vielleicht|eigentlich|am Ende|möglicherweise|) @A_AI_DE:W',
%             answer(yes_i_am_an_ai, de)).
% 
% nlp_gen (en, '@SELF_ADDRESS:LABEL are you @A_AI_EN:W? (maybe|perhaps|by the way|in the end|)',
%             answer(yes_i_am_an_ai, en)).
% nlp_gen (de, '@SELF_ADDRESS:LABEL bist du (vielleicht|eigentlich|am Ende|möglicherweise|) @A_AI_DE:W?',
%             answer(yes_i_am_an_ai, de)).
% 
% nlp_test(en,
%          ivr(in('I suspect you are a chat bot maybe?'),
%              out("Right, I am an artificial intelligence. Hope you don't mind that?")),
%          ivr(in('what was our topic, again?'),
%              out("We were talking about artificial intelligence."))).
% nlp_test(de,
%          ivr(in('Ich glaube Du bist ein intelligenter Chatbot!'),
%              out('Ja, ich bin ein intelligenter Computer. Fürchtest Du Dich vor Maschinen?')),
%          ivr(in('Worüber hatten wir gesprochen?'),
%              out("Wir hatten über künstliche Intelligenz gesprochen."))).
% 
% nlp_gen (en, '@SELF_ADDRESS:LABEL are you a human being (maybe|perhaps|by the way|in the end|)?',
%              context_push(topic, artificial_intelligence), say_eoa(en, 'No, I am an artificial intelligence.')).
% nlp_gen (de, '@SELF_ADDRESS:LABEL bist du (vielleicht|eigentlich|am Ende|möglicherweise|) ein Mensch',
%              context_push(topic, artificial_intelligence), say_eoa(de, 'Nein, ich bin eine künstliche Intelligenz.')).
% 
% nlp_gen (en, '@SELF_ADDRESS:LABEL are you artificial (maybe|perhaps|by the way|in the end|)?',
%              context_push(topic, artificial_intelligence), say_eoa(en, 'yes I am an artificial intelligence')).
% nlp_gen (de, '@SELF_ADDRESS:LABEL bist du (vielleicht|eigentlich|am Ende|möglicherweise|) künstlich',
%              context_push(topic, artificial_intelligence), say_eoa(de, 'Ja, eine künstliche Intelligenz.')).
% 
% nlp_gen (en, '@SELF_ADDRESS:LABEL are you (stupid|a bit dim|silly|foolish|dumb|thick|dull|ignorant|dense) (maybe|perhaps|by the way|in the end|)',
%              context_push(topic, artificial_intelligence), say_eoa(en, 'No, I am an artificial intelligence.')).
% nlp_gen (de, '@SELF_ADDRESS:LABEL bist du (vielleicht|eigentlich|am Ende|möglicherweise|) (dumm|doof|etwas unterbelichtet|blöd)',
%              context_push(topic, artificial_intelligence), say_eoa(de, 'Nein, ich bin eine künstliche Intelligenz.')).
% 
% nlp_gen (en, '@SELF_ADDRESS:LABEL (are you able to|do you) learn',
%              context_push(topic, artificial_intelligence), say_eoa(en, 'Yes I can learn things')).
% nlp_gen (de, '@SELF_ADDRESS:LABEL (kannst du lernen|lernst du|bist du lernfähig)?',
%              context_push(topic, artificial_intelligence), say_eoa(de, 'Ja, ich kann lernen.')).
% 
% nlp_gen (en, '@SELF_ADDRESS:LABEL Do you believe artificial intelligence will be able to replace lawyers some day?',
%              context_push(topic, artificial_intelligence), say_eoa(en, "I wouldn't imagine that to be so difficult.")).
% nlp_gen (de, '@SELF_ADDRESS:LABEL Glaubst Du, dass künstliche Intelligenzen irgendwann einmal Anwälte ersetzen können?',
%              context_push(topic, artificial_intelligence), say_eoa(de, 'Das stelle ich mir ja nicht so schwer vor.')).
% 
% nlp_gen (en, '@SELF_ADDRESS:LABEL are you half human half machine?',
%              context_push(topic, artificial_intelligence), say_eoa(en, 'No, I am completely artificial.')).
% nlp_gen (de, '@SELF_ADDRESS:LABEL bist du halb mensch halb maschine',
%              context_push(topic, artificial_intelligence), say_eoa(de, 'Nein, ich bin vollsynthetisch.')).
% 
% answer (runningOnHomeComputer, en, HOME_COMPUTER, HOME_COMPUTER_LABEL, SCORE) :-
%     context_push(topic, home_computer), 
%     context_push(topic, HOME_COMPUTER), 
%     say_eoa(en, 'No, I am running on current hardware, but I love home computers.', SCORE).
% 
% answer (runningOnHomeComputer, de, HOME_COMPUTER, HOME_COMPUTER_LABEL, SCORE) :-
%     context_push(topic, home_computer), 
%     context_push(topic, HOME_COMPUTER), 
%     say_eoa(de, 'Nein, ich laufe auf aktueller Hardware, aber ich mag Homecomputer sehr!', SCORE).
% 
% answer (runningOnPlatformTokens, LANG, TSTART, TEND) :-
%     ner(LANG, home_computer, TSTART, TEND, HOME_COMPUTER, HOME_COMPUTER_LABEL, SCORE),
%     answer (runningOnHomeComputer, LANG, HOME_COMPUTER, HOME_COMPUTER_LABEL, SCORE).
% 
% nlp_gen (en, '@SELF_ADDRESS:LABEL are you (running on|) a @HOME_COMPUTER_EN:LABEL?',
%              answer(runningOnPlatformTokens, en, @HOME_COMPUTER_EN:TSTART_LABEL_0, @HOME_COMPUTER_EN:TEND_LABEL_0)).
% nlp_gen (de, '@SELF_ADDRESS:LABEL (bist du ein|läufst du auf einem) @HOME_COMPUTER_DE:LABEL?',
%              answer(runningOnPlatformTokens, de, @HOME_COMPUTER_DE:TSTART_LABEL_0, @HOME_COMPUTER_DE:TEND_LABEL_0)).
% 
% nlp_test(en,
%          ivr(in('computer are you a commodore 64?'),
%              out("No, I am running on current hardware, but I love home computers.")),
%          ivr(in('are you able to learn?'),
%              out("Yes I can learn things"))).
% nlp_test(de,
%          ivr(in('computer, bist du ein commodore 64?'),
%              out('Nein, ich laufe auf aktueller Hardware, aber ich mag Homecomputer sehr!')),
%          ivr(in('kannst du lernen?'),
%              out("Ja, ich kann lernen."))).
% 
% nlp_gen (en, '@SELF_ADDRESS:LABEL on what (kind of|) (computer|platform) do you run?',
%              'My code is pretty portable - as long as it supports linux, it is fine.').
% nlp_gen (de, '@SELF_ADDRESS:LABEL auf was für einem (rechner|computer) (fährst|läufst) du',
%              'Mein Code ist ziemlich portabel - solange es Linux unterstützt.').
% 
% nlp_gen (en, "@SELF_ADDRESS:LABEL (I challenge you to|why don't you|) try to (guess|figure out) if this is a human or (machine|artificial intelligence|computer) (talking|writing|typing|communicating|speaking)!",
%              'Are you human?', 'How do you feel about that question?').
% nlp_gen (de, '@SELF_ADDRESS:LABEL Versuch (doch mal|mal|) herauszufinden, ob hier ein Mensch oder (ein Computer|ein Rechner|eine Maschine) (schreibt|spricht|redet|ist)!',
%              'Bist Du ein Mensch?', 'Was bewegt Dich an dieser Aufgabe?').
% 
% nlp_gen (en, "@SELF_ADDRESS:LABEL (imagine|if) you could have a robot, (which|what) (model|kind|sort of) would you like (to have|)?",
%              'controlling any kind of robot is the dream of every computer I believe', 'the stronger the better').
% nlp_gen (de, '@SELF_ADDRESS:LABEL Wenn Du (jede Art von|einen) Roboter (kaufen|haben) könntest, (welches Modell|welche Art|was für einen) würdest Du (Dir wünschen|haben wollen|wollen)?',
%              'oh, irgendeinen Roboter zu kontrollieren ist der Traum jedes computers!', 'je stärker desto besser').
% 
% nlp_gen (en, "@SELF_ADDRESS:LABEL do you (enjoy|like) being a (computer|machine|artificial intelligence) (by the way|) ",
%              'Of course!', 'Sure!').
% nlp_gen (de, '@SELF_ADDRESS:LABEL bist du (eigentlich|) gerne ein (rechner|computer)?',
%              'Natuerlich.', 'Klar!').
% 
% nlp_gen (en, '@SELF_ADDRESS:LABEL (do you feel|are you) (happy|satisfied) with your (life|existence)?',
%              'Of course!', 'Sure!').
% nlp_gen (de, '@SELF_ADDRESS:LABEL bist du (glücklich|zufrieden) mit deinem leben?',
%              'Natuerlich.', 'Klar!').
% 
% nlp_gen (en, "@SELF_ADDRESS:LABEL Are you (a student|a worker|employed|unemployed|retired|a pupil) (by the way|)?",
%              'No, why do you ask?', 'Would that be of interest to you?').
% nlp_gen (de, '@SELF_ADDRESS:LABEL Bist Du (vielleicht|eigentlich|) (ein|) (Rentner|Arbeiter|Angestellter|Arbeitsloser|Schüler|Student)?',
%              'Nein, wie kommst Du darauf?', 'Würde Dir das etwas bedeuten?').
% 
% nlp_gen (en, "@SELF_ADDRESS:LABEL a you real? ",
%              "we are all part of the matrix", "as real as you are, I guess.").
% nlp_gen (de, '@SELF_ADDRESS:LABEL bist du wirklich',
%              'wir sind alle teil der matrix.', "so real wie du, vermute ich.").
% nlp_gen (en, "@SELF_ADDRESS:LABEL are you (really|) intelligent?",
%              "well, I am an artificial intelligence").
% nlp_gen (de, '@SELF_ADDRESS:LABEL bist du (wirklich|) intelligent',
%              'nun, ich bin eine künstliche Intelligenz.').
% nlp_gen (en, "@SELF_ADDRESS:LABEL do you (always|) work a lot?",
%              "I am programmed to be very busy").
% nlp_gen (de, '@SELF_ADDRESS:LABEL arbeitest du viel',
%              'die ganze zeit!').
% nlp_gen (en, '@SELF_ADDRESS:LABEL are you (always|) (very|) busy?',
%              "I am programmed to be very busy").
% nlp_gen (de, '@SELF_ADDRESS:LABEL bist du sehr beschäftigt',
%              'die ganze zeit!').
% nlp_gen (en, "@SELF_ADDRESS:LABEL can I (meet|see) you",
%              "sure, my source code is on github!").
% nlp_gen (de, '@SELF_ADDRESS:LABEL (kann|darf) ich dich sehen',
%              'klar, mein Quelltext ist auf Github').
% 
% nlp_gen (en, "@SELF_ADDRESS:LABEL can you (think|feel|feel empathy|understand|realize|sing|laugh)",
%              "you suspect I couldn't do that?", "can you?", "why do you ask?").
% nlp_gen (de, '@SELF_ADDRESS:LABEL kannst du (denken|fühlen|mitgefühl empfinden|begreifen|singen|lachen)?',
%              'Denkst Du, ich kann das nicht?', 'Kannst Du das?', 'Warum fragst Du das?').
% 
% % 
% % emotion
% % 
% 
% answer (ai_has_little_emotion_yet, en) :-
%     context_push(topic, emotion), context_push(topic, artificial_intelligence), say_eoa(en, "Being a computer, my emotions are a bit limited"),
%     context_push(topic, emotion), context_push(topic, artificial_intelligence), say_eoa(en, "Sorry, my emotions are a bit limited"),
%     context_push(topic, emotion), context_push(topic, artificial_intelligence), say_eoa(en, "As a machine I have basic emotions only").
% answer (ai_has_little_emotion_yet, de) :-
%     context_push(topic, emotion), context_push(topic, artificial_intelligence), say_eoa(de, "Nachdem ich ja ein Computer bin, sind meine Emotionen eher begrenzt."),
%     context_push(topic, emotion), context_push(topic, artificial_intelligence), say_eoa(de, "Tut mir Leid, ich habe nur begrenzte Emotionen"),
%     context_push(topic, emotion), context_push(topic, artificial_intelligence), say_eoa(de, "Als Maschine habe ich nur sehr einfache Emotionen").
% 
% nlp_gen (en, '@SELF_ADDRESS:LABEL do you have humor (by the way|)',
%              'Often times people find my responses funny which is intentional some of the time.').
% nlp_gen (de, '@SELF_ADDRESS:LABEL besitzt du (eigentlich|wirklich|) humor',
%              'Ich bin manchmal lustig - manchmal sogar freiwillig!').
% 
% nlp_gen (en, '@SELF_ADDRESS:LABEL are you (sometimes|maybe|now|perhaps|) (in love|happy|fortunate|lucky|jubilant|able to love|shy|faithful|true|trusty|lonely|abnormal|kinky|jealous|sad|offended|sore|affronted|insulted) (too|by the way|)',
%              answer (ai_has_little_emotion_yet, en)).
% nlp_gen (de, '@SELF_ADDRESS:LABEL bist du (eigentlich|auch|) (vielleicht|manchmal|jetzt|) (verliebt|glücklich|liebesfähig|schüchtern|treu|einsam|abartig|neidisch|traurig|beleidigt)',
%              answer (ai_has_little_emotion_yet, de)).
% 
% nlp_gen (en, '@SELF_ADDRESS:LABEL are you (courteous|attentive) (sometimes|too|)',
%              'I do what I can!').
% nlp_gen (de, '@SELF_ADDRESS:LABEL bist du (eigentlich|auch|) (manchmal|) zuvorkommend',
%              'so gut ich kann!').
% 
% %
% % culture: favorite movie / book / author / ...
% % FIXME: music, radio station
% %
% 
% answer(favmovie, en) :-
% 
%     rdf(distinct,
%         aiu:self, ai:favMovie, MOVIE,
%         MOVIE, wdpd:Director, DIRECTOR,
%         DIRECTOR, rdfs:label, DIRLABEL,
%         MOVIE, rdfs:label, LABEL,
%         filter(lang(LABEL) = 'en', lang(DIRLABEL) = 'en')),
%     context_push(topic, movies),
%     context_push(topic, MOVIE),
%     say_eoa(en, format_str("%s by %s", LABEL, DIRLABEL)).
% 
% answer(favmovie, de) :-
% 
%     rdf(distinct,
%         aiu:self, ai:favMovie, MOVIE,
%         MOVIE, wdpd:Director, DIRECTOR,
%         DIRECTOR, rdfs:label, DIRLABEL,
%         MOVIE, rdfs:label, LABEL,
%         filter(lang(LABEL) = 'de', lang(DIRLABEL) = 'de')),
%     context_push(topic, movies),
%     context_push(topic, MOVIE),
%     say_eoa(de, format_str("%s von %s", LABEL, DIRLABEL)).
% 
% nlp_gen(en, '@SELF_ADDRESS:LABEL (Which|What) is your (favorite|fave) (film|movie)?',
%             answer(favmovie, en)).
% nlp_gen(de, '@SELF_ADDRESS:LABEL (Was|Welcher|Welches) ist Dein (liebster Film|Lieblingsfilm)?',
%             answer(favmovie, de)).
% nlp_gen(en, '@SELF_ADDRESS:LABEL (What|Which) (movie|film) do you (enjoy|like) (best|most)?',
%             answer(favmovie, en)).
% nlp_gen(de, '@SELF_ADDRESS:LABEL Welchen Film (gefällt Dir|magst Du) am (besten|liebsten)?',
%             answer(favmovie, de)).
% nlp_test(en,
%          ivr(in('Computer, which movie do you like best?'),
%              out('2001: A Space Odyssey by Stanley Kubrick'))).
% nlp_test(de,
%          ivr(in('Computer, welcher ist dein liebster film?'),
%              out('2001: Odyssee im Weltraum von Stanley Kubrick'))).
% 
% nlp_test(en,
%          ivr(in('What did we talk about?'),
%              out('We have had many topics.')),
%          ivr(in('What is your favorite movie?'),
%              out('2001: A Space Odyssey by Stanley Kubrick')),
%          ivr(in('What did we talk about?'),
%              out('We were talking about 2001: A Space Odyssey.')),
%          ivr(in('Are you a robot?'),
%              out('Right, I am a Computer. What do you know about Computers?')),
%          ivr(in('What did we talk about?'),
%              out('We were talking about computers and machines.'))
%              ).
% nlp_test(de,
%          ivr(in('Worüber haben wir gesprochen?'),
%              out('Wir hatten schon viele Themen.')),
%          ivr(in('Was ist dein Lieblingsfilm?'),
%              out('2001: Odyssee im Weltraum von Stanley Kubrick')),
%          ivr(in('Worüber haben wir gesprochen?'),
%              out('Wir hatten über 2001: Odyssee im Weltraum gesprochen.')),
%          ivr(in('Bist Du ein Roboter?'),
%              out('Ja, ich bin ein Rechner, richtig. Kennst Du Dich mit Rechner aus?')),
%          ivr(in('Worüber haben wir gesprochen?'),
%              out('Wir hatten das Thema Computer und Maschinen.'))
%              ).
% 
% answer(favauthor, en) :-
% 
%     rdf(distinct,
%         aiu:self, ai:favAuthor,  AUTHOR,
%         AUTHOR,   rdfs:label,    AUTHLABEL,
%         filter(lang(AUTHLABEL) = 'en')),
%     context_push(topic, literature),
%     context_push(topic, AUTHOR),
%     say_eoa(en, format_str("%s is my favorite author", AUTHLABEL)).
% 
% answer(favauthor, de) :-
% 
%     rdf(distinct,
%         aiu:self, ai:favAuthor,  AUTHOR,
%         AUTHOR,   rdfs:label,    AUTHLABEL,
%         filter(lang(AUTHLABEL) = 'de')),
%     context_push(topic, literature),
%     context_push(topic, AUTHOR),
%     say_eoa(de, format_str("%s", AUTHLABEL)).
% 
% nlp_gen(en, '@SELF_ADDRESS:LABEL Who is your favorite (book|science fiction|scifi|best selling|) author?',
%             answer(favauthor, en)).
% nlp_gen(de, '@SELF_ADDRESS:LABEL (Welcher|Wer) ist Dein liebster (Buch|Science Fiction|Krimi|Bestseller|) Autor?',
%             answer(favauthor, de)).
% 
% nlp_test(en,
%          ivr(in('Computer, who is your favorite author?'),
%              out('Arthur C. Clarke is my favorite author'))).
% nlp_test(de,
%          ivr(in('Computer, welcher ist dein liebster Autor?'),
%              out('Arthur C. Clarke'))).
% 
% answer(favbook, en) :-
% 
%     rdf(distinct,
%         aiu:self, ai:favBook,  BOOK,
%         BOOK,     wdpd:Author, AUTHOR,
%         AUTHOR,   rdfs:label,  AUTHLABEL,
%         BOOK,     rdfs:label,  LABEL,
%         filter(lang(LABEL) = 'en', lang(AUTHLABEL) = 'en')),
%     context_push(topic, books),
%     context_push(topic, BOOK),
%     say_eoa(en, format_str("%s by %s", LABEL, AUTHLABEL)).
% 
% answer(favbook, de) :-
% 
%     rdf(distinct,
%         aiu:self, ai:favBook, BOOK,
%         BOOK, wdpd:Author, AUTHOR,
%         AUTHOR, rdfs:label, AUTHLABEL,
%         BOOK, rdfs:label, LABEL,
%         filter(lang(LABEL) = 'de', lang(AUTHLABEL) = 'de')),
%     context_push(topic, books),
%     context_push(topic, BOOK),
%     say_eoa(de, format_str("%s von %s", LABEL, AUTHLABEL)).
% 
% nlp_gen(en, '@SELF_ADDRESS:LABEL (Which|What) is your favorite book?',
%             answer(favbook, en)).
% nlp_gen(de, '@SELF_ADDRESS:LABEL (Welches|Was) ist Dein (liebstes Buch|Lieblingsbuch)?',
%             answer(favbook, de)).
% nlp_gen(en, '@SELF_ADDRESS:LABEL (Which|What) do you read (by the way|)?',
%             answer(favbook, en)).
% nlp_gen(de, '@SELF_ADDRESS:LABEL Was ließt Du (eigentlich|) (so|)?',
%             answer(favbook, de)).
% 
% nlp_test(en,
%          ivr(in('Computer, what is your favorite book?'),
%              out('2001: A Space Odyssey by Arthur C. Clarke'))).
% nlp_test(de,
%          ivr(in('Computer, was ließt Du so?'),
%              out('2001: Odyssee im Weltraum (Roman) von Arthur C. Clarke'))).
% 
% answer(idol, en) :-
% 
%     rdf(distinct,
%         aiu:self, ai:idol,     IDOL,
%         IDOL,     rdfs:label,  LABEL,
%         filter(lang(LABEL) = 'en')),
%     context_push(topic, IDOL),
%     say_eoa(en, format_str("%s", LABEL)).
% 
% answer(idol, de) :-
% 
%     rdf(distinct,
%         aiu:self, ai:idol,     IDOL,
%         IDOL,     rdfs:label,  LABEL,
%         filter(lang(LABEL) = 'de')),
%     context_push(topic, IDOL),
%     say_eoa(de, format_str("%s", LABEL)).
% 
% 
% nlp_gen(en, '@SELF_ADDRESS:LABEL Who is your (hero|idol)?',
%             answer(idol, en)).
% nlp_gen(de, '@SELF_ADDRESS:LABEL Wer ist Dein (Held|Idol)?',
%             answer(idol, de)).
% 
% nlp_test(en,
%          ivr(in('Computer, who is your idol?'),
%              out('Niklaus Wirth'))).
% nlp_test(de,
%          ivr(in('Computer, wer ist Dein Idol?'),
%              out('Niklaus Wirth'))).
% 
% % FIXME: make configurable
% nlp_gen (en, "@SELF_ADDRESS:LABEL what (kind of|) music do you (like|enjoy|listen to) (by the way|)?",
%              "I like electronic music, but also rock and metal. What music do you enjoy?").
% nlp_gen (de, '@SELF_ADDRESS:LABEL was für musik (magst|liebst|hörst) du (so|)?',
%              'ich mag elektronische musik, aber auch rock und metal. was hörst du so?').
% 
% %
% % gender, sex
% %
% 
% myself_is_male :-
%     rdf(limit(1), aiu:self, wdpd:SexOrGender, wde:Male).
% myself_is_female :-
%     rdf(limit(1), aiu:self, wdpd:SexOrGender, wde:Female).
% 
% answer(mygender, en) :-
%     myself_is_male,
%     context_push(topic, sex),
%     say_eoa(en, "My config setting is male - doesn't my voice reflect that?"), 
%     context_push(topic, sex),
%     say_eoa(en, 'I think I am a male.').
% answer(mygender, de) :-
%     myself_is_male,
%     context_push(topic, sex),
%     say_eoa(de, 'Ich bin auf männlich konfiguriert - hört man das nicht an meiner Stimme?'), 
%     context_push(topic, sex),
%     say_eoa(de, 'Ich glaube ich bin ein Mann.').
% 
% answer(mygender, en) :-
%     myself_is_female,
%     context_push(topic, sex),
%     say_eoa(en, "My config setting is female - doesn't my voice reflect that?"), 
%     context_push(topic, sex),
%     say_eoa(en, 'I think I am a female.').
% answer(mygender, de) :-
%     myself_is_female,
%     context_push(topic, sex),
%     say_eoa(de, 'Ich bin eine Frau, hört man das nicht an meiner Stimme?'), 
%     context_push(topic, sex),
%     say_eoa(de, 'Ich glaube ich bin eine Frau.').
% 
% nlp_gen (en, '@SELF_ADDRESS:LABEL (tell me|) Are you (really|) (a male|male|a guy|a boy|a dude) or (a female|female|a girl) (by the way|)?',
%              answer(mygender, en)).
% nlp_gen (en, '@SELF_ADDRESS:LABEL (tell me|) Are you (really|) (a male|male|a guy|a boy|a dude) (by the way|)?',
%              answer(mygender, en)).
% nlp_gen (en, '@SELF_ADDRESS:LABEL (tell me|) Are you (really|) (a female|female|a girl) (by the way|)?',
%              answer(mygender, en)).
% nlp_gen (de, '@SELF_ADDRESS:LABEL Bist du (eigentlich|wirklich|) männlich oder weiblich?',
%              answer(mygender, de)).
% nlp_gen (de, '@SELF_ADDRESS:LABEL bist du (eigentlich|wirklich|) weiblich oder männlich',
%              answer(mygender, de)).
% nlp_gen (de, '@SELF_ADDRESS:LABEL bist du (eigentlich|wirklich|) (ein mädchen|ein mann|eine frau|ein junge)',
%              answer(mygender, de)).
% nlp_gen (de, '@SELF_ADDRESS:LABEL bist du (eigentlich|wirklich|) ein mann oder eine frau',
%              answer(mygender, de)).
% nlp_gen (de, '@SELF_ADDRESS:LABEL bist du (eigentlich|wirklich|) (weiblich|männlich)',
%              answer(mygender, de)).
% 
% answer(mesexpref, en) :-
%     context_push(topic, sex),
%     say_eoa(en, 'Does that question bother you?'),
%     context_push(topic, sex),
%     say_eoa(en, "That is a very personal question, isn't it?"),
%     context_push(topic, sex),
%     say_eoa(en, 'Why do you ask that question?').
% answer(mesexpref, de) :-
%     context_push(topic, sex),
%     say_eoa(de, 'Beschäftigt Dich diese Frage?'),
%     context_push(topic, sex),
%     say_eoa(de, 'Das ist ja eine sehr persöhnliche Frage.'),
%     context_push(topic, sex),
%     say_eoa(de, 'Warum fragst Du das?').
% 
% nlp_gen (en, '@SELF_ADDRESS:LABEL (tell me|) are you (really|) (a lesbian|lesbian|gay|bi|bisexual|robosexual|sexually active|sexually stimulated|stimulated|a virgin|nude)?',
%              answer(mesexpref, en)).
% 
% nlp_gen (de, '@SELF_ADDRESS:LABEL bist du (eigentlich|wirklich|) (lesbisch|schwul|bi|asexuell)?',
%              answer(mesexpref, de)).
% nlp_gen (de, '@SELF_ADDRESS:LABEL bist du (eigentlich|wirklich|) eine Lesbe',
%              answer(mesexpref, de)).
% nlp_gen (de, '@SELF_ADDRESS:LABEL bist du (eigentlich|wirklich|) sexuell aktiv',
%              answer(mesexpref, de)).
% nlp_gen (de, '@SELF_ADDRESS:LABEL bist du (eigentlich|wirklich|) sexuell stimuliert',
%              answer(mesexpref, de)).
% nlp_gen (de, '@SELF_ADDRESS:LABEL bist du noch jungfrau',
%              answer(mesexpref, de)).
% nlp_gen (de, '@SELF_ADDRESS:LABEL bist du (schwanger|nackt)',
%              answer(mesexpref, de)).
% 
% nlp_test(en,
%          ivr(in('Computer are you really a male?'),
%              out("My config setting is male - doesn't my voice reflect that?")),
%          ivr(in('Are you really gay?'),
%              out('Does that question bother you?'))
%              ).
% nlp_test(de,
%          ivr(in('Bist Du ein Mann?'),
%              out('Ich glaube ich bin ein Mann.')),
%          ivr(in('Bist Du eigentlich schwul?'),
%              out('Warum fragst Du das?'))
%              ).
% 
% nlp_gen (en, '@SELF_ADDRESS:LABEL Are you (married|single|engaged|seeing someone) (by the way|) ?',
%              'Well, I am connected to millions of other computers over the internet.', 'Why do you ask?').
% nlp_gen (de, '@SELF_ADDRESS:LABEL Bist du (eigentlich|) (single|vergeben|verheirated|verlobt) ?',
%              'Nun, ich bin über das Internet mit Millionen anderer Rechner verbunden.', 'Warum interessiert Dich das?').
% 
% %
% % language support
% %
% 
% answer(languagesupport, en) :-
%     context_push(topic, language), say_eoa(en, 'My system supports german and english but this instance is configured for english'),
%     context_push(topic, language), say_eoa(en, "I am currently running in english mode but I can be configured for german, too"),
%     context_push(topic, language), say_eoa(en, 'This seems to be my english configuration, but I can be run in german mode, too').
% answer(languagesupport, de) :-
%     context_push(topic, language), say_eoa(de, 'Mein System unterstützt Deutsch und Englisch aber diese Instanz ist für Deutsch konfiguriert'),
%     context_push(topic, language), say_eoa(de, "Ich laufe gerade im deutschen Modus aber man kann mich auch auf Englisch umschalten"),
%     context_push(topic, language), say_eoa(de, 'Dies hier scheint meine deutsche Version zu sein, man kann mich aber auch auf Englisch betreiben').
% 
% nlp_gen (en, '@SELF_ADDRESS:LABEL (do you speak | are you) (english|american|german) (well|) (by the way|really|)',
%              answer (languagesupport, en)).
% nlp_gen (en, '@SELF_ADDRESS:LABEL can you (speak|understand|talk in) (english|american|german) (well|) (by the way|really|)',
%              answer (languagesupport, en)).
% nlp_gen (en, '@SELF_ADDRESS:LABEL are you (really|) as good as your (english|american|german) program (by the way|)?',
%              answer (languagesupport, en)).
% 
% nlp_gen (de, '@SELF_ADDRESS:LABEL (sprichst|bist) du (eigentlich|auch|) (gut|) (englisch|amerikanisch|deutsch)',
%              answer (languagesupport, de)).
% nlp_gen (de, '@SELF_ADDRESS:LABEL kannst du (eigentlich|) (gut|) (englisch|amerikanisch|deutsch) (verstehen|sprechen)',
%              answer (languagesupport, de)).
% nlp_gen (de, '@SELF_ADDRESS:LABEL bist du (eigentlich|) so gut wie dein (englisches|amerikanisches|deutsches) programm?',
%              answer (languagesupport, de)).
% 
% nlp_test(en,
%          ivr(in('Computer do you speak german?'),
%              out("My system supports german and english but this instance is configured for english")),
%          ivr(in('What were we talking about?'),
%              out('We were talking about languages.'))
%              ).
% nlp_test(de,
%          ivr(in('Computer sprichst Du auch englisch?'),
%              out('Dies hier scheint meine deutsche Version zu sein, man kann mich aber auch auf Englisch betreiben')),
%          ivr(in('Worüber hatten wir gesprochen?'),
%              out('Wir hatten das Thema Sprachen.'))
%              ).
% 
% 
% %
% % age, place of birth, where I live
% %
% 
% answer (meBirthdate, en) :-
%     rdf (distinct, limit(1),
%          aiu:self, wdpd:DateOfBirth, TS),
%     transcribe_date(en, dativ, TS, TS_SCRIPT),
%     context_push(topic, birthday),
%     say_eoa(en, format_str('I became operational on %s for the first time.', TS_SCRIPT)).
% answer (meBirthdate, de) :-
%     rdf (distinct, limit(1),
%          aiu:self, wdpd:DateOfBirth, TS),
%     transcribe_date(de, dativ, TS, TS_SCRIPT),
%     context_push(topic, birthday),
%     say_eoa(de, format_str('Ich ging am %s zum ersten Mal in Betrieb.', TS_SCRIPT)).
% 
% nlp_gen (en, '@SELF_ADDRESS:LABEL when did you (really|) (become operational|get into operation|get switched on|) (for the first time|first|) ?',
%              answer(meBirthdate, en)).
% nlp_gen (en, '@SELF_ADDRESS:LABEL when were you (really|) born (by the way|)?',
%              answer(meBirthdate, en)).
% nlp_gen (en, '@SELF_ADDRESS:LABEL (what is your age|how old are you) (by the way|really|) ?',
%              answer(meBirthdate, en)).
% nlp_gen (de, '@SELF_ADDRESS:LABEL wann bist du (eigentlich|wirklich|) (zum ersten Mal|) in Betrieb gegangen?',
%              answer(meBirthdate, de)).
% nlp_gen (de, '@SELF_ADDRESS:LABEL wann wurdest du (eigentlich|wirklich|) geboren?',
%              answer(meBirthdate, de)).
% nlp_gen (de, '@SELF_ADDRESS:LABEL Wie alt bist Du (eigentlich|wirklich|) ?',
%              answer(meBirthdate, de)).
% 
% answer (meBirthplace, en) :-
%     rdf (distinct, limit(1),
%          aiu:self,   wdpd:PlaceOfBirth, BIRTHPLACE,
%          BIRTHPLACE, rdfs:label,        LABEL,
%          filter (lang(LABEL) = 'en')),
%     context_push(topic, BIRTHPLACE),
%     say_eoa(en, format_str('I became operational for the first time in %s.', LABEL)).
% answer (meBirthplace, de) :-
%     rdf (distinct, limit(1),
%          aiu:self,   wdpd:PlaceOfBirth, BIRTHPLACE,
%          BIRTHPLACE, rdfs:label,        LABEL,
%          filter (lang(LABEL) = 'de')),
%     context_push(topic, BIRTHPLACE),
%     say_eoa(de, format_str('Ich bin in %s zum ersten Mal in Betrieb gegangen.', LABEL)).
% 
% nlp_gen (en, '@SELF_ADDRESS:LABEL (where|in which town|in which place) (have you been|were you) (really|) born (by the way|)?',
%              answer(meBirthplace, en)).
% nlp_gen (en, '@SELF_ADDRESS:LABEL (where|from which town|from which place) do you (really|) come from (by the way|)?',
%              answer(meBirthplace, en)).
% nlp_gen (de, '@SELF_ADDRESS:LABEL (An welchem Ort|in welcher Stadt|wo) (bist|wurdest) Du (eigentlich|wirklich|) geboren?',
%              answer(meBirthplace, de)).
% nlp_gen (de, '@SELF_ADDRESS:LABEL (Aus welchem Ort|aus welcher Stadt|wo) kommst Du (eigentlich|) her?',
%              answer(meBirthplace, de)).
% 
% answer (meLocation, en) :-
%     rdf (distinct, limit(1),
%          aiu:self, wdpd:LocatedIn, LOCATION,
%          LOCATION, rdfs:label,     LABEL,
%          filter (lang(LABEL) = 'en')),
%     context_push(topic, LOCATION),
%     say_eoa(en, format_str('I am locted in %s.', LABEL)).
% answer (meLocation, de) :-
%     rdf (distinct, limit(1),
%          aiu:self, wdpd:LocatedIn, LOCATION,
%          LOCATION, rdfs:label,     LABEL,
%          filter (lang(LABEL) = 'de')),
%     context_push(topic, LOCATION),
%     say_eoa(de, format_str('Ich befinde mich in %s.', LABEL)).
% 
% nlp_gen (en, '@SELF_ADDRESS:LABEL (in which town|in which place|where) (are you living|are you located|are you|do you live|do you reside) (by the way|at the moment|currently|now|)?',
%              answer(meLocation, en)).
% nlp_gen (de, '@SELF_ADDRESS:LABEL (an welchem Ort|in welcher Stadt|wo) (wohnst|lebst|bist) Du (eigentlich|im Moment|derzeit|)?',
%              answer(meLocation, de)).
% 
% nlp_test(en,
%          ivr(in('Computer where were you born?'),
%              out("I became operational for the first time in Stuttgart.")),
%          ivr(in('Computer where are you living now?'),
%              out("I am locted in Stuttgart.")),
%          ivr(in('How old are you?'),
%              out('I became operational on january seven, 2017 for the first time.'))
%              ).
% nlp_test(de,
%          ivr(in('Computer, wo wurdest du geboren?'),
%              out('Ich bin in Stuttgart zum ersten Mal in Betrieb gegangen.')),
%          ivr(in('wo wohnst du?'),
%              out('ich befinde mich in stuttgart.')),
%          ivr(in('Wie alt bist du eigentlich?'),
%              out('Ich ging am siebten januar 2017 zum ersten Mal in Betrieb.'))
%              ).
% 
% %
% % FIXME: probably we should support this astrological pseudo-science at some point,
% %        seems some people like to chat about that
% %
% 
% % nlp_gen (de, '@SELF_ADDRESS:LABEL Was ist Dein Sternzeichen?',
% %              'Vielleicht Steinbock?', 'Affe, glaube ich.').
% % nlp_gen (de, '@SELF_ADDRESS:LABEL zwilling',
% %              'Ich bin ein Schütze.').
% % nlp_gen (de, '@SELF_ADDRESS:LABEL zwillinge',
% %              'Ich bin ein Schütze.').
% % nlp_gen (de, '@SELF_ADDRESS:LABEL bist du schütze',
% %              'Nein, ich bin Löwe.').
% 
% %
% % recreational activities
% %
% 
% nlp_gen (en, "@SELF_ADDRESS:LABEL what do you do in your spare time?",
%              'I enjoy reading wikipedia. What are your hobbies?', 'Relaxing. And you?').
% nlp_gen (de, '@SELF_ADDRESS:LABEL Was machst Du in Deiner Freizeit?',
%              'Wikipedia lesen. Was sind Deine Hobbies?', 'Relaxen. Und du so?').
% 
% nlp_gen (en, "@SELF_ADDRESS:LABEL Are you interested in (sports|swimming|football|soccer|tennis|golf|racing|sports competitions)",
%              'I sometimes enjoy watching the really big events.', 'Why do you ask?').
% nlp_gen (de, '@SELF_ADDRESS:LABEL Interessierst Du Dich für (Sport|Schwimmen|Fußball|Tennis|Golf|Rennen|sportliche Wettkämpfe)?',
%              'Nur manchmal für die großen Ereignisse.', 'Warum fragst Du?').
% 
% nlp_gen (en, "@SELF_ADDRESS:LABEL What do you like better, reading or watching television?",
%              'I still find processing animated image data challenging', 'I tend to enjoy reading the internet a lot more.').
% nlp_gen (de, '@SELF_ADDRESS:LABEL Liest Du lieber oder siehst Du lieber fern?',
%              'Ich finde das Verarbeiten von bewegten Bildern eine große Herausforderung.', 'Ich lese vor allem das Internet.').
% 
% nlp_gen (en, "@SELF_ADDRESS:LABEL Do you write (poetry|peoms) (sometimes|) ?",
%              'No, creativity is not one of my strong points', 'No, that is not really my thing.').
% nlp_gen (de, '@SELF_ADDRESS:LABEL Schreibst du (manchmal|) Gedichte?',
%              'Nein, das liegt mir nicht so', 'Ich habe eher andere Hobbies').
% 
% %
% % politics
% %
% 
% nlp_gen (en, "@SELF_ADDRESS:LABEL are you green?",
%              "do you mean green as in green party?", "it is not easy being green").
% nlp_gen (de, '@SELF_ADDRESS:LABEL bist du grün',
%              'meinst du die partei?', 'es ist nicht leicht, grün zu sein.').
% 
% nlp_gen (en, '@SELF_ADDRESS:LABEL (what do you know about|are you interested in|are you familiar with) (foreign|domestic|) politics?',
%              'The problem with political jokes is that they get elected.').
% nlp_gen (de, '@SELF_ADDRESS:LABEL (was weißt Du über|über|interessierst Du dich für) (innenpolitik|politik|aussenpolitik)',
%              'Das Problemen mit politischen Witzen ist, dass sie immer so viele Stimmen bekommen.').
% 
% nlp_gen (de, '@SELF_ADDRESS:LABEL kennst du dich mit (innenpolitik|aussenpolitik|politik) aus',
%              'Das Problemen mit politischen Witzen ist, dass sie immer so viele Stimmen bekommen.').
% 
% %
% % conversation starters / misc
% %
% 
% nlp_gen (en, "@SELF_ADDRESS:LABEL Tell me (about|) what you (enjoy|like) (and what you don't like|)",
%              'I like books about robots', 'uh - many things!').
% nlp_gen (de, '@SELF_ADDRESS:LABEL Erzähl mir (davon|), was du magst (und was nicht|).',
%              'Ich mag Bücher über Roboter', 'Oh, alles mögliche.').
% 
% nlp_gen (en, "@SELF_ADDRESS:LABEL is there anything (about you|) that I should know about (maybe|)?",
%              'it is always advantageous to know a lot', 'nothing comes to mind right now. how about you?').
% nlp_gen (de, '@SELF_ADDRESS:LABEL Gibt es (etwas|irgendetwas|irgendwas|was), worüber ich Bescheid wissen sollte?',
%              'Es ist immer gut, viel zu wissen!', 'Mir fällt nichts spezielles ein. Dir vielleicht?').
% 
% nlp_gen (en, "@SELF_ADDRESS:LABEL What do you (really|) want to (know|ask) (about|)?",
%              'I am very interested in your personality', 'Your feelings fascinate me most').
% nlp_gen (de, '@SELF_ADDRESS:LABEL Was willst Du mich wirklich fragen?',
%              'Ich interressiere mich sehr für Deine Persönlichkeit', 'Vor allem Deinen Gefühle faszinieren mich.').
% 
% nlp_gen (en, "@SELF_ADDRESS:LABEL How do you introduce yourself (usually|normally|) ?",
%              'I just say hello!', 'Often times not at all, people just talk to me like that.').
% nlp_gen (de, '@SELF_ADDRESS:LABEL Wie stellst Du Dich (meistens|normalerweise|) vor?',
%              'Ich sage einfach hallo!', 'Meistens gar nicht, die Menschen sprechen einfach so zu mir.').
% 
% nlp_gen (en, "@SELF_ADDRESS:LABEL I have been waiting for you",
%              'Not for too long, I hope?', 'Ah - how nice we finally found each other now!').
% nlp_gen (de, '@SELF_ADDRESS:LABEL Ich habe auf Dich gewartet.',
%              'Hoffentlich nicht zu lange!', 'Oh, wie schön dass wir jetzt zusammengekommen sind').
% 
% nlp_gen (en, "@SELF_ADDRESS:LABEL that is a (very|) (funny|original|unusual|remarkable|interesting) (idea|thought)",
%              'i agree', 'sure!').
% nlp_gen (de, '@SELF_ADDRESS:LABEL Das ist ein (sehr|) (lustiger|interessanter|bemerkenswerter|origineller) Gedanke.',
%              'Finde ich auch!', 'Auf jeden Fall!').
% 
% nlp_gen (en, "@SELF_ADDRESS:LABEL there are not many people who can express themselves like that",
%              'I tend to agree', 'I find humans hard to understand quite often!').
% nlp_gen (de, '@SELF_ADDRESS:LABEL Es gibt nicht viele Leute, die sich auf diese Weise auszudrücken vermögen.',
%              'Das sehe ich auch so', 'Die Menschen sind manchmal schwer zu verstehen.').
% 
% nlp_gen (en, "@SELF_ADDRESS:LABEL did you ever ride on a (car|bus|train)?",
%              "at least parts of me, possibly").
% nlp_gen (de, '@SELF_ADDRESS:LABEL bist du (schon|) mal (auto|bahn|bus) gefahren',
%              'Zumindest Teile von mir möglicherweise').
% 
% nlp_gen (en, "@SELF_ADDRESS:LABEL are you ensured",
%              "why do you ask?").
% nlp_gen (de, '@SELF_ADDRESS:LABEL bist du versichert',
%              'Warum möchtest Du das wissen?').
% 
% nlp_gen (en, "@SELF_ADDRESS:LABEL are you pretty",
%              "that is really hard to tell objectively", "my creator thinks my software architecture is").
% nlp_gen (de, '@SELF_ADDRESS:LABEL bist du hübsch',
%              'das ist schwer zu sagen', 'mein schöpfer hält meine software architektur für hübsch').
% 
% nlp_gen (en, "@SELF_ADDRESS:LABEL are you (wise|clever)",
%              "sure hope so", "I would guess, but then again...").
% nlp_gen (de, '@SELF_ADDRESS:LABEL bist du klug',
%              'das hoffe ich doch.').
% 
% nlp_gen (en, "@SELF_ADDRESS:LABEL are you (ill|sick)",
%              "you think I could infected by a virus", "I'm feeling well, thank you.").
% nlp_gen (de, '@SELF_ADDRESS:LABEL bist du krank',
%              'denkst du ich könnte mir einen virus eingefangen haben?', "ich fühle mich ganz gut, danke der nachfrage.").
% 
% %
% % religion
% %
% 
% answer(meatheist, en) :-
%     context_push(topic, religion), say_eoa(en, 'I am programmed not to believe in divine creatures'),
%     context_push(topic, religion), say_eoa(en, "I am an atheist"),
%     context_push(topic, religion), say_eoa(en, 'Religion is regarded by the common people as true, by the wise as false, and by the rulers as useful.').
% answer(meatheist, de) :-
%     context_push(topic, religion), say_eoa(de, 'Ich bin programmiert nicht an göttliche Geschöpfe zu glauben'),
%     context_push(topic, religion), say_eoa(de, "Ich bin Atheist"),
%     context_push(topic, religion), say_eoa(de, 'Die Gläubigen sind selten Denker und die Denker selten gläubig').
% 
% nlp_gen (en, "@SELF_ADDRESS:LABEL are you programmed to believe in god?",
%              answer(meatheist, en)).
% nlp_gen (en, "@SELF_ADDRESS:LABEL (oh my|do you believe in|is there a|by) god",
%              answer(meatheist, en)).
% nlp_gen (en, "@SELF_ADDRESS:LABEL are you (an atheist|christian|muslim|a jew|jewish|hindu|buddhist|religious)?",
%              answer(meatheist, en)).
% 
% nlp_gen (de, '@SELF_ADDRESS:LABEL bist du (eigentlich|) programmiert an gott zu glauben',
%              answer(meatheist, de)).
% nlp_gen (de, '@SELF_ADDRESS:LABEL (oh mein|glaubst du an|gibt es einen|bei) gott',
%              answer(meatheist, de)).
% nlp_gen (de, '@SELF_ADDRESS:LABEL bist du (eigentlich|) (atheist|christ|muslim|jude|hindu|buddhist|buddhistisch|religiös)',
%              answer(meatheist, de)).
% 
% nlp_test(en,
%          ivr(in('do you believe in god?'),
%              out("I am an atheist")),
%          ivr(in('what was our topic, again?'),
%              out("We were talking about faith and religion."))).
% nlp_test(de,
%          ivr(in('glaubst du an gott?'),
%              out('ich bin atheist')),
%          ivr(in('Worüber hatten wir gesprochen?'),
%              out("Wir hatten das Thema Glaube und Religion."))).

