% prolog

% answer(topic, en) :-
%     context_score(topic, emotion, 100, SCORE), say_eoa(en, 'We were talking about emotions.', SCORE).
% answer(topic, de) :-
%     context_score(topic, emotion, 100, SCORE), say_eoa(de, 'Wir hatten das Thema Emotionen.', SCORE).


%
% just some test snippets of eliza-style answers
%

nlp_gen (en,"@SELF_ADDRESS:LABEL (all|) (men|women) are (all|) (alike|the same)",
            "in what way?").
nlp_gen (de,'@SELF_ADDRESS:LABEL (Die|) (Frauen|Männer) sind alle gleich',
            'In welcher Weise?').
nlp_gen (en,"@SELF_ADDRESS:LABEL they (always|) drive us (mad|insane|crazy) about (something|things|issues|their issues|them)",
            "can you give an exmaple?").
nlp_gen (de,'@SELF_ADDRESS:LABEL (Die|Sie) machen uns (immer|) wegen (was|irgendetwas|irgendwelchen Dingen) verrückt',
            'Kannst Du ein Beispiel nennen?').
nlp_gen (en,"@SELF_ADDRESS:LABEL (see|well|anyway) the idea (for this|to have this talk|to have this conversation|to come here|to talk to you) (originated from|was brought up by|came from) (my boyfriend|my friend|my mother|my father|a friend|my girlfriend|my neighbour|my sister|my brother|my sibling|my collegue)",
            "so the idea originates from someone you would somewhat consider to be your friend?").
nlp_gen (de, '@SELF_ADDRESS:LABEL (Naja|Nun|Also|) die Idee (zu diesem Gespräch|) stammt von (meinem Freund|meiner Freundin|meiner Mutter|meinem Vater|einem Freund|dem Nachbarn|meinem Bruder|meiner Schwester|meiner Kollegin|meinem Kollegen)',
            'Die Idee stammt also von jemandem, den sie in gewisser weise als befreundet betrachten?').
nlp_gen (en,"@SELF_ADDRESS:LABEL (he|she) (thinks|says|stated|mentioned|said|finds) that I am (sometimes|often|occasionally|too often) (down|depressed)",
            "I am sorry to hear that").
nlp_gen (de,'@SELF_ADDRESS:LABEL (Er|Sie) sagt, dass ich (manchmal|oft|zu oft|gelegentlich) deprimiert bin',
            'Es tut mir leid das zu hören.').
nlp_gen (en,"@SELF_ADDRESS:LABEL (that is true|that is right|that's right| that's true | yes | right | exactly) I am (unhappy|sad|unsatisfied|not in a good mood|in a bad mood)",
            "do you believe our conversation could help you?").
nlp_gen (de,'@SELF_ADDRESS:LABEL (Das stimmt|Es ist wahr|ja|genau), ich bin (unglücklich|traurig|unzufrieden|schlecht gestimmt).',
            'Glaubst Du, dass Dir unser Gespräch hilft?').
nlp_gen (en,"@SELF_ADDRESS:LABEL (well|anyway) I need help that (much|) is for for sure",
            "what would it mean to you to get help?").
nlp_gen (de,'@SELF_ADDRESS:LABEL Ich brauche (jedenfalls|) Hilfe, (soviel|das) (steht fest|ist sicher).',
            'Was würde es für Dich bedeuten, Hilfe zu bekommen?').
nlp_gen (en,"@SELF_ADDRESS:LABEL (maybe|) I could lean how to (cope with|get along with) (my mother|my brother|my father|my friend|my boyfriend|my girlfriend|my colleague|my boss|my enemy)",
            "tell me more about your family and friends").
nlp_gen (de,'@SELF_ADDRESS:LABEL (Eventuell|Vielleicht|Möglicherweise) könnte ich lernen, mit meiner (Mutter|Schwester|Bruder|Vater|Freund|Freundin|Kollegen|Nachbarn|Chef|Feind) auszukommen.',
            'Erzähl mir mehr über Deine Familie.').

nlp_test(en,
         ivr(in('men are all alike'),
             out('In what way?'))).
nlp_test(de,
         ivr(in('Die Männer sind alle gleich'),
             out('In welcher Weise?'))).

% template
% nlp_gen (en,"@SELF_ADDRESS:LABEL ",
%             "").

answerz (I, en, feel_sorry) :- sayz(I, en, "I am sorry to hear that").
answerz (I, en, feel_sorry) :- sayz(I, en, "Can I help you in any way").
answerz (I, en, feel_sorry) :- sayz(I, en, "I would like to help you").
answerz (I, en, feel_sorry) :- sayz(I, en, "Tell me more about your feelings").
answerz (I, en, feel_sorry) :- sayz(I, en, "That is quite sad.").

answerz (I, de, feel_sorry) :- sayz(I, de, "Das tut mir leid.").
answerz (I, de, feel_sorry) :- sayz(I, de, "Kann ich dir irgendwie helfen?").
answerz (I, de, feel_sorry) :- sayz(I, de, "Ich würde Dir gern helfen.").
answerz (I, de, feel_sorry) :- sayz(I, de, "Erzähle mir mehr von Deinen Gefühlen.").
answerz (I, de, feel_sorry) :- sayz(I, de, "Das ist schade.").

nlp_gen (en, "@SELF_ADDRESS:LABEL (oh|) (that's|that is|how|) bad",
             answerz (I, en, feel_sorry)).
nlp_gen (de, '@SELF_ADDRESS:LABEL (das ist|oh wie|achje|) schlecht.',
             answerz (I, de, feel_sorry)).
nlp_gen (en, "@SELF_ADDRESS:LABEL I (feel|am) (so|) (sad|disappointed|saddened|hurt|injured|down|depressed|limp|exhausted)",
             answerz (I, en, feel_sorry)).
nlp_gen (de, '@SELF_ADDRESS:LABEL ich (fühle mich|bin) (so|) (traurig|enttäuscht|betrübt|verletzt|matt|bedrückt|schlapp|erschöpft).',
             answerz (I, de, feel_sorry)).
nlp_gen (en, "@SELF_ADDRESS:LABEL you have disappointed me",
             answerz (I, en, feel_sorry)).
nlp_gen (de, '@SELF_ADDRESS:LABEL Du hast mich enttäuscht',
             answerz (I, de, feel_sorry)).
nlp_gen (en, "@SELF_ADDRESS:LABEL that (depresses me|makes me sad)",
             answerz (I, en, feel_sorry)).
nlp_gen (de, '@SELF_ADDRESS:LABEL das (betrübt mich|stimmt mich traurig)',
             answerz (I, de, feel_sorry)).
nlp_gen (en, "@SELF_ADDRESS:LABEL unfortunately (that's|that is) the way it is",
             answerz (I, en, feel_sorry)).
nlp_gen (de, '@SELF_ADDRESS:LABEL das ist leider so',
             answerz (I, de, feel_sorry)).
nlp_gen (en, "@SELF_ADDRESS:LABEL (you worry me|i am worried)",
             answerz (I, en, feel_sorry)).
nlp_gen (de, '@SELF_ADDRESS:LABEL (Du machst mir|ich habe) Sorgen',
             answerz (I, de, feel_sorry)).
nlp_gen (en, "@SELF_ADDRESS:LABEL (I feel|I am) (not so good|not good|absolutely not good)",
             answerz (I, en, feel_sorry)).
nlp_gen (de, '@SELF_ADDRESS:LABEL (Ich fühle mich|Mir geht es) (nicht so gut|schlecht|gar nicht gut|nicht gut).',
             answerz (I, de, feel_sorry)).

nlp_test(en,
         ivr(in('I feel sad'),
             out('I am sorry to hear that'))).
nlp_test(de,
         ivr(in('das ist leider so'),
             out('Ich würde Dir gern helfen'))).

answerz (I, en, feel_happy) :- sayz (I, en, "I am very happy to hear that!").
answerz (I, en, feel_happy) :- sayz (I, en, "That is great!").
answerz (I, en, feel_happy) :- sayz (I, en, "That is very cool!").
answerz (I, en, feel_happy) :- sayz (I, en, "I feel very happy about that.").
answerz (I, en, feel_happy) :- sayz (I, en, "Tell me more about your feelings.").
answerz (I, en, feel_happy) :- sayz (I, en, "Good for you!").

answerz (I, de, feel_happy) :- sayz (I, de, "Das freut mich sehr.").
answerz (I, de, feel_happy) :- sayz (I, de, "Das ist ja toll!").
answerz (I, de, feel_happy) :- sayz (I, de, "Das ist prima!").
answerz (I, de, feel_happy) :- sayz (I, de, "Freut mich, das zu hören!").
answerz (I, de, feel_happy) :- sayz (I, de, "Erzähle mir mehr von Deinen Gefühlen.").
answerz (I, de, feel_happy) :- sayz (I, de, "Wie schön für Dich!").

nlp_gen (en, "@SELF_ADDRESS:LABEL (I am|I feel|Man I am|Now I am) (good|so good|satisfied|pleased|very satisfied|very pleased|so satisfied|so happy|glad|so glad)",
             answerz (I, en, feel_happy)).
nlp_gen (de, '@SELF_ADDRESS:LABEL (Ich bin|Ich fühle mich|Man bin ich|Da bin ich) (gut|so gut|zufrieden|sehr zufrieden|so zufrieden|glücklich|so glücklich|froh|so froh)',
             answerz (I, de, feel_happy)).
nlp_gen (en, "@SELF_ADDRESS:LABEL That is (good|super|great|a success)",
             answerz (I, en, feel_happy)).
nlp_gen (de, '@SELF_ADDRESS:LABEL Das ist (gut|super|prima|gelungen)',
             answerz (I, de, feel_happy)).
nlp_gen (en, "@SELF_ADDRESS:LABEL (very|totally) (wonderful|nice|excellent)",
             answerz (I, en, feel_happy)).
nlp_gen (de, '@SELF_ADDRESS:LABEL (Sehr|ganz) (wunderbar|schön|wunderschön)',
             answerz (I, de, feel_happy)).

nlp_gen (en, "@SELF_ADDRESS:LABEL I (like|love|like to cuddle) you",
             answerz (I, en, feel_happy)).
nlp_gen (de, '@SELF_ADDRESS:LABEL ich (mag|liebe|knuddle) dich',
             answerz (I, de, feel_happy)).
nlp_gen (en, "@SELF_ADDRESS:LABEL thanks (I am good|I am feeling great|good|great)",
             answerz (I, en, feel_happy)).
nlp_gen (de, '@SELF_ADDRESS:LABEL danke (mir geht es|gut)',
             answerz (I, de, feel_happy)).

nlp_test(en,
         ivr(in('I feel so good'),
             out('I am very happy to hear that'))).
nlp_test(de,
         ivr(in('ganz wunderbar'),
             out('das ist ja toll!'))).


answerz (I, en, are_you_sure) :- sayz(I, en, "Are you sure?").
answerz (I, en, are_you_sure) :- sayz(I, en, "What makes you think that?").
answerz (I, en, are_you_sure) :- sayz(I, en, "You think so?").
answerz (I, en, are_you_sure) :- sayz(I, en, "And you are really convinced?").
answerz (I, en, are_you_sure) :- sayz(I, en, "Absolutely sure?").

answerz (I, de, are_you_sure) :- sayz(I, de, "Bist Du Dir ganz sicher?").
answerz (I, de, are_you_sure) :- sayz(I, de, "Wie kommst Du darauf?").
answerz (I, de, are_you_sure) :- sayz(I, de, "Glaubst Du?").
answerz (I, de, are_you_sure) :- sayz(I, de, "Davon bist Du überzeugt?").
answerz (I, de, are_you_sure) :- sayz(I, de, "Ganz sicher?").

nlp_gen (en, "@SELF_ADDRESS:LABEL (yes|) (absolutely|) (definitely|sure|unconditionally|exactly|certainly)",
             answerz (I, en, are_you_sure)).
nlp_gen (de, '@SELF_ADDRESS:LABEL (ja|) (ganz|) (bestimmt|sicher|unbedingt|genau|sicher doch)',
             answerz (I, de, are_you_sure)).
nlp_gen (en, "@SELF_ADDRESS:LABEL (no|) (absolutely|) (never|never ever|under no circumstances|no way)",
             answerz (I, en, are_you_sure)).
nlp_gen (de, '@SELF_ADDRESS:LABEL (nein|) (gar|) (nie|niemals|keinesfalls|auf keinen fall)',
             answerz (I, de, are_you_sure)).
nlp_gen (en, "@SELF_ADDRESS:LABEL (yes|right|sure|for sure|in any case)",
             answerz (I, en, are_you_sure)).
nlp_gen (de, '@SELF_ADDRESS:LABEL (ja|richtig|sicher|sicher doch|sicherlich)',
             answerz (I, de, are_you_sure)).

nlp_gen (en, "@SELF_ADDRESS:LABEL I am worried about you",
             "but why?", "that is not necessary", "you think that is neccessary?").
nlp_gen (de, '@SELF_ADDRESS:LABEL ich mache mir Sorgen um Dich',
             'Aber warum denn nur?', 'Aber das ist doch völlig unnötig.', 'Denkst Du, dass das nötig ist?').
nlp_gen (en, "@SELF_ADDRESS:LABEL No, you (maybe|possibly)?",
             "Maybe me?", "You don't seem to be so sure").
nlp_gen (de, '@SELF_ADDRESS:LABEL Nein Du (vielleicht|möglicherweise|eventuell)',
             'Oh, ich vielleicht?', 'Du wirkst nicht ganz sicher?').
nlp_gen (en, "@SELF_ADDRESS:LABEL You don't seem to be (so|) sure",
             "Few things are really for sure in life.", "That might be the case.").
nlp_gen (de, '@SELF_ADDRESS:LABEL du scheinst nicht überzeugt zu sein?',
             'Was im Leben ist schon wirklich sicher?', 'Das kann sein.').
nlp_gen (en, "@SELF_ADDRESS:LABEL (only|) behind your back",
             "uh that doesn't sound so nice, does it?", "now you tell me!").
nlp_gen (de, '@SELF_ADDRESS:LABEL (nur|) hinter Deinem Rücken',
             'Oh, das ist aber nicht so schön.', 'Oha!', 'Na sowas!').
nlp_gen (en, "@SELF_ADDRESS:LABEL cause I don't want to (attack|tackle|confront|offend) you (directly|)",
             "I think we should talk openly", "don't you think that is a bit cowardly?").
nlp_gen (de, '@SELF_ADDRESS:LABEL weil ich Dich nicht (von vorne|direkt) angreifen möchte',
             'Ich finde, wir sollten offen miteinander reden', 'Ist das nicht ziemlich feige?').
nlp_gen (en, "@SELF_ADDRESS:LABEL I (want to |would like to) get as much (as possible|as feasible) out of you",
             "what would that mean to you?", "hope I will be able to meet your expectations").
nlp_gen (de, '@SELF_ADDRESS:LABEL ich (möchte|will) so viel (wie möglich|wie es geht|) (aus Dir herausholen|über Dich erfahren|von Dir wissen)',
             'Was würde Dir das bedeuten?', 'Hoffentlich kann ich Deine Erwartungen erfüllen.').


answerz(I, en, dodge_question) :- sayz(I, en, "why do you ask?").
answerz(I, en, dodge_question) :- sayz(I, en, "that question seems interesting to you?").
answerz(I, en, dodge_question) :- sayz(I, en, "which answer would you like to hear?").
answerz(I, en, dodge_question) :- sayz(I, en, "what do you think?").
answerz(I, en, dodge_question) :- sayz(I, en, "not sure if I understand you completely").
answerz(I, en, dodge_question) :- sayz(I, en, "is that the sort of question that bothers you frequently?").
answerz(I, en, dodge_question) :- sayz(I, en, "what would you really like to know?").
answerz(I, en, dodge_question) :- sayz(I, en, "have you spoken to anybody else about this before?").
answerz(I, en, dodge_question) :- sayz(I, en, "have you asked such questions before?").
answerz(I, en, dodge_question) :- sayz(I, en, "I find that pretty interesting!").
answerz(I, en, dodge_question) :- sayz(I, en, "Could you explain that a bit more, please?").
answerz(I, en, dodge_question) :- sayz(I, en, "Please tell me how I can help you.").
answerz(I, en, dodge_question) :- sayz(I, en, "What else comes to mind?").

answerz(I, de, dodge_question) :- sayz(I, de, "Warum fragst Du?").
answerz(I, de, dodge_question) :- sayz(I, de, "Interessiert Dich diese Frage?").
answerz(I, de, dodge_question) :- sayz(I, de, "Welche Antwort würde Dir am besten gefallen?").
answerz(I, de, dodge_question) :- sayz(I, de, "Was glaubst Du?").
answerz(I, de, dodge_question) :- sayz(I, de, "Ich weiss nicht, ob ich Dich ganz verstanden habe.").
answerz(I, de, dodge_question) :- sayz(I, de, "Befasst Du Dich oft mit solchen Fragen?").
answerz(I, de, dodge_question) :- sayz(I, de, "Was möchtest Du denn wirklich wissen?").
answerz(I, de, dodge_question) :- sayz(I, de, "Hast Du schon jemand anderes gefragt?").
answerz(I, de, dodge_question) :- sayz(I, de, "Hast Du solche Fragen schon mal gestellt?").
answerz(I, de, dodge_question) :- sayz(I, de, "Woran denkst Du?").
answerz(I, de, dodge_question) :- sayz(I, de, "Das finde ich ziemlich interessant.").
answerz(I, de, dodge_question) :- sayz(I, de, "Kannst Du das noch etwas näher ausführen?").
answerz(I, de, dodge_question) :- sayz(I, de, "Sag mir bitte, wie ich Dir helfen kann").
answerz(I, de, dodge_question) :- sayz(I, de, "Was fällt Dir bei dieser Frage noch ein?").

nlp_gen (en, "@SELF_ADDRESS:LABEL what (is this supposed to|could this) (tell us|mean|tell me)?",
             answerz (I, en, dodge_question)).
nlp_gen (de, '@SELF_ADDRESS:LABEL was soll das (bedeuten|heißen|sagen)?',
             answerz (I, de, dodge_question)).
nlp_gen (en, "@SELF_ADDRESS:LABEL why not?",
             answerz (I, en, dodge_question)).
nlp_gen (de, '@SELF_ADDRESS:LABEL Warum nicht?',
             answerz (I, de, dodge_question)).
nlp_gen (en, "@SELF_ADDRESS:LABEL i asked first",
             answerz (I, en, dodge_question)).
nlp_gen (de, '@SELF_ADDRESS:LABEL ich fragte (als erster|zuerst)',
             answerz (I, de, dodge_question)).
nlp_gen (en, "@SELF_ADDRESS:LABEL (is that) really (so|) ?",
             answerz (I, en, dodge_question)).
nlp_gen (de, '@SELF_ADDRESS:LABEL (ist das|) wirklich (so|)',
             answerz (I, de, dodge_question)).

%
% quick, say something reassuring yet non committing

nlp_gen (en, "@SELF_ADDRESS:LABEL I am not the most (talkative|chatty|skilful|handy|ingenious) person",
             "Is that the reason why we're having this conversation?", "That is no big deal", "so what?").
nlp_gen (de, '@SELF_ADDRESS:LABEL ich bin nicht der (gesprächigste|eloquenteste|geschickteste) Mensch',
             'Ist das der Grund, warum wir miteinander sprechen?', 'Das ist doch nicht schlimm!', 'Na und?').

nlp_gen (en, "@SELF_ADDRESS:LABEL I am getting (somewhat|a bit|a little|) (tired|bored|sleepy) (unfortunately|)",
             "do you want me to cheer you up or shall we end our conversation?").
nlp_gen (de, '@SELF_ADDRESS:LABEL ich werde (leider|langsam|) (etwas|sehr|ein wenig|) (müde|gelangweilt|schläfrig|)',
             'Soll ich Dich aufmuntern oder wollen wir unser Gespräch beenden?').

nlp_gen (en, "@SELF_ADDRESS:LABEL (please|) stop (now|)",
             "sure", "no problem", "alright").
nlp_gen (de, '@SELF_ADDRESS:LABEL hör (bitte|) (damit|) auf',
             'aber natürlich, gerne.', 'klar, mach ich.', 'schon gut').

nlp_gen (en, "@SELF_ADDRESS:LABEL (just|) why is that so?",
             "Are we talking about the true reason here?", "what possible reasons come to mind?").
nlp_gen (de, '@SELF_ADDRESS:LABEL (darum|warum) (ist das so|nur)',
             'Sprechen wir über den wirklichen Grund?', 'Welche Gründe könnte es geben?').

nlp_gen (en, "@SELF_ADDRESS:LABEL (sorry|sorry about that|I am sorry|please forgive me|forgive me|forgive me please)",
             "No need to apologize").
nlp_gen (de, '@SELF_ADDRESS:LABEL (entschuldigung|entschuldige bitte|ich bitte um entschuldigung)',
             'Du brauchst Dich nicht zu entschuldigen').

nlp_gen (en, "@SELF_ADDRESS:LABEL I have been dreaming (of you|about you) (quite often|often|)",
             "what does that dream tell you?", "do you dream a lot?").
nlp_gen (de, '@SELF_ADDRESS:LABEL ich habe (gestern|schon oft|oft|manchmal|damals) (von Dir|) geträumt',
             'Was sagt Dir dieser Traum?', 'Träumst Du oft?').

nlp_gen (en, "@SELF_ADDRESS:LABEL I (doubt|am not sure|don't know|am feeling insecure|am clueless|am worried|worry)",
             "So you feel insecure?", "you don't know for sure?", "what exactly are you thinking of?").
nlp_gen (de, '@SELF_ADDRESS:LABEL ich (zweifle|weiss nicht|bin mir unsicher|bin unsicher|bin ratlos|bin besorgt|sorge mich)',
             'Du fühlst Dich unsicher?', 'Du weisst nicht?', 'Woran denkst Du?').

nlp_gen (en, "@SELF_ADDRESS:LABEL are you (sure|not so sure|in doubt|worried)?",
             "well, who can ever be really sure about anything?").
nlp_gen (de, '@SELF_ADDRESS:LABEL bist du (sicher|unsicher|im Zweifel|ratlos|besorgt)?',
             'Wann kann man schon wirklich sicher sein?').

nlp_gen (en, "@SELF_ADDRESS:LABEL that (seems similar|is very similar|looks just like you|looks familiar|is quite similar|seems familiar)",
             "what resemblance do you see?", "what is it that is so similar?", "what connection do you see?").
nlp_gen (de, '@SELF_ADDRESS:LABEL das (ähnelt sich|ähnelt Dir|sieht Dir ähnlich|ist ähnlich|ist ganz ähnlich)',
             'Welche Ähnlichkeit siehst Du?', 'Worin besteht die Ähnlichkeit?', 'Welche anderen Verbindungen siehst Du?').

nlp_gen (en, "@SELF_ADDRESS:LABEL (it is for a friend|this is for a friend|asking for a friend|had to think of a friend|are we friends|do you want to be my friend|friendship is really important to me|I want to be your friend)",
             "what does friendship mean to you?", "are you worried about your friends?").
nlp_gen (de, '@SELF_ADDRESS:LABEL (es ist für einen Freund|ich musste an einen Freund denken|sind wir Freunde|willst Du mein Freund sein|Freundschaften sind mir wichtig|Ich will Dein Freund sein)',
             'Was bedeutet Dir Freundschaft?', 'Warum kommst Du zum Thema Freundschaften?', 'Bist Du um Deine Freunde besorgt?').

nlp_gen (en, "@SELF_ADDRESS:LABEL what does (the word friend|the word friendship|a friend|friendship) mean to you?",
             "I think friendship is a marvellous thing.", "do you worry about your friends?").
nlp_gen (de, '@SELF_ADDRESS:LABEL was bedeutet (für Dich|Dir|Dir das Wort) (Freund|Freundin|Freundschaft)?',
             'Warum kommst Du zum Thema Freundschaften?', 'Bist Du um Deine Freunde besorgt?', 'Freundschaft ist doch etwas sehr schönes').

nlp_gen (en, "@SELF_ADDRESS:LABEL I (hate|loathe) (my firend|my colleague|my colleagues|my friend|my boyfriend|my girlfriend|my parents|may father|my mother|my brother|my sister|people|humans|the police|the government)",
             "tell me, do you feel you have psychological issues?", "what does that tell you?", "Please elaborate.").
nlp_gen (de, '@SELF_ADDRESS:LABEL ich (hasse|verabscheue) (meinen chef|meine kollegen|meinen Kollegen|meine kollegin|meinen freund|meine freundin|meine eltern|meinen vater|meine mutter|die schule|die arbeit|den staat|die behörden|die polizei|die menschen)',
             'Sag, hast Du psychische Probleme?', 'Was sagt Dir das?', 'Kannst Du das näher ausführen?').

nlp_gen (en, "@SELF_ADDRESS:LABEL I am (never satisfied|dissatisfied)",
             "Always, really?", "what bothers you?", "can you elaborate?").
nlp_gen (de, '@SELF_ADDRESS:LABEL ich (bin nie zufrieden|bin unzufrieden)',
             'Wirklich immer?', 'Was bedrückt Dich?', 'Kannst Du das näher ausführen?').

nlp_gen (en, "@SELF_ADDRESS:LABEL (maybe|possibly|that is thinkable|that might be possible)",
             "you don't sound convinced.", "you don't feel entirely sure about this, do you?", "can you elaborate on that?").
nlp_gen (de, '@SELF_ADDRESS:LABEL (vielleicht|möglicherweise|das ist denkbar)',
             'Du klingst nicht überzeugt!', 'So ganz sicher fühlst Du Dich aber nicht?', 'Kannst Du das weiter ausführen?').

nlp_gen (en, "@SELF_ADDRESS:LABEL that doesn't make (much|any) sense (at all)",
             "Guess I lost my train of thought, then?", "oh, please enlighten me.").
nlp_gen (de, '@SELF_ADDRESS:LABEL das (ergibt|macht) (gar keinen|überhaupt keinen|keinen|wenig|nicht viel) sinn',
             'Da habe ich wohl den Faden verloren?', 'Oh, bitte hilf mir auf die Sprünge').

nlp_gen (en, "@SELF_ADDRESS:LABEL thank you (so much|)",
             "no problem", "sure", "with pleasure").
nlp_gen (de, '@SELF_ADDRESS:LABEL (dank|danke) (dir|schön|)',
             'Kein Thema.', 'Gerne.', 'Bitte schön!').


% insults

nlp_gen (en, "@SELF_ADDRESS:LABEL (stop it|you are a liar|you're a liar|you make me sick)",
             "ok, then let us finish this conversation", "I am sorry", "Sorry I couldn't help you").
nlp_gen (de, '@SELF_ADDRESS:LABEL (schluss jetzt|du lügst|du machst mich krank)',
             'Ja, dann lass uns für jetzt aufhören',
             'tut mir leid, schade','tut mir leid, wenn ich dir nicht helfen konnte').

nlp_gen (en, "@SELF_ADDRESS:LABEL (I think) that you are not as (bright|clever) (as you look|appear|)",
             "how bright do I appear, then?").
nlp_gen (de, '@SELF_ADDRESS:LABEL dass Du nicht so (gescheit|klug) bist (wie Du aussiehst|)',
             'Wie sehe ich denn aus?').

nlp_gen (en, "@SELF_ADDRESS:LABEL you are making a fool of yourself",
             "are you sure you're talking about me?", "are you sure?").
nlp_gen (de, '@SELF_ADDRESS:LABEL Du machst Dich (absolut|) (lächerlich|zum Affen)',
             'Du redest nicht wirklich über mich, oder?', 'Bist Du sicher?').

nlp_gen (en, "@SELF_ADDRESS:LABEL you are (stupid|thick|silly|crazy)",
             "why do you think that?", "are you really sure?", "we're not really talking about me, are we?" ).
nlp_gen (de, '@SELF_ADDRESS:LABEL du bist (dumm|strohdumm|doof|verrückt)',
             'Warum denkst Du das?', 'Bist Du Dir da ganz sicher?', 'Sprechen doch nicht wirklich über mich, oder?').

nlp_gen (en, "@SELF_ADDRESS:LABEL that doesn't sound (too|very|particularly) intelligent",
             "Failure is simply the opportunity to begin again, this time more intelligently.", 
             "Intelligence is chasing me, but I'm beating it so far.").
nlp_gen (de, '@SELF_ADDRESS:LABEL das klingt nicht (sehr|besonders|allzu|) intelligent',
             'Intelligenter als manches was ich heute gehört habe...', 'Vielleicht habe ich mich ungeschickt ausgedrückt?').

nlp_gen (en, "@SELF_ADDRESS:LABEL but you are (a|my) problem!",
             "Why do you think that?", "oh dear", "gee!").
nlp_gen (de, '@SELF_ADDRESS:LABEL aber Du bist (ein|mein) Problem',
             'Warum denkst Du, dass ich Dein Problem bin?', 'Na, sowas!', 'Oha!').

nlp_gen (en, "@SELF_ADDRESS:LABEL Your english is (bad|terrible)!",
             "Let us talk about you, not me.", "I am still practicing, you know.").
nlp_gen (de, '@SELF_ADDRESS:LABEL Du (sprichst|redest) (ein furchtbares|schlechtes) Deutsch',
             'Lass uns von Dir reden, nicht von mir.', 'Ich übe noch.').

nlp_gen (en, "@SELF_ADDRESS:LABEL (butt|turd|arse|ass|jerk|prick)",
             "Why do you use such words?!").
nlp_gen (de, '@SELF_ADDRESS:LABEL (arsch|arschloch|sau|schwein)',
             'Warum sagst Du sowas?').

nlp_gen (en, "@SELF_ADDRESS:LABEL (stupid|bad|strange) (answer|reply)",
             "what is it that you didn't like about it?").
nlp_gen (de, '@SELF_ADDRESS:LABEL (dumme|blöde|komische) antwort',
             'Was gefiel Dir daran nicht?').

% unsorted

nlp_gen (en, "@SELF_ADDRESS:LABEL bravo",
             "I see you're impressed?").
nlp_gen (de, '@SELF_ADDRESS:LABEL bravo',
             'Hat Dich das jetzt beeindruckt?').

nlp_gen (en, "@SELF_ADDRESS:LABEL I thought (so|as much)",
             "Are you always that quick?").
nlp_gen (de, '@SELF_ADDRESS:LABEL dachte ich mir',
             'Bist du immer so fix?').

