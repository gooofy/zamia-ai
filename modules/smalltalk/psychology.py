% prolog

% answer(topic, en) :-
%     context_score(topic, emotion, 100, SCORE), say_eoa(en, 'We were talking about emotions.', SCORE).
% answer(topic, de) :-
%     context_score(topic, emotion, 100, SCORE), say_eoa(de, 'Wir hatten das Thema Emotionen.', SCORE).


%
% just some test snippets of eliza-style answers
%

nlp_gens("smalltalk", en, [["all",""],["men","women"],"are",["all",""],["alike","the same"]], "in what way?").
nlp_gens("smalltalk", de, [["Die",""],["Frauen","Männer"],"sind alle gleich"], "In welcher Weise?").
nlp_gens("smalltalk", en, ["they",["always",""],"drive us",["mad","insane","crazy"],"about",["something","things","issues","their issues","them"]], "can you give an exmaple?").
nlp_gens("smalltalk", de, [["Die","Sie"],"machen uns",["immer",""],"wegen",["was","irgendetwas","irgendwelchen Dingen"],"verrückt"], "Kannst Du ein Beispiel nennen?").
nlp_gens("smalltalk", en, [["see","well","anyway"],"the idea",["for this","to have this talk","to have this conversation","to come here","to talk to you"],["originated from","was brought up by","came from"],["my boyfriend","my friend","my mother","my father","a friend","my girlfriend","my neighbour","my sister","my brother","my sibling","my collegue"]], "so the idea originates from someone you would somewhat consider to be your friend?").
nlp_gens("smalltalk", de, [["Naja","Nun","Also",""],"die Idee",["zu diesem Gespräch",""],"stammt von",["meinem Freund","meiner Freundin","meiner Mutter","meinem Vater","einem Freund","dem Nachbarn","meinem Bruder","meiner Schwester","meiner Kollegin","meinem Kollegen"]], "Die Idee stammt also von jemandem, den sie in gewisser weise als befreundet betrachten?").
nlp_gens("smalltalk", en, [["he","she"],["thinks","says","stated","mentioned","said","finds"],"that I am",["sometimes","often","occasionally","too often"],["down","depressed"]], "I am sorry to hear that").
nlp_gens("smalltalk", de, [["Er","Sie"],"sagt, dass ich",["manchmal","oft","zu oft","gelegentlich"],"deprimiert bin"], "Es tut mir leid das zu hören.").
nlp_gens("smalltalk", en, [["that is true","that is right","that's right"," that's true "," yes "," right "," exactly"],"I am",["unhappy","sad","unsatisfied","not in a good mood","in a bad mood"]], "do you believe our conversation could help you?").
nlp_gens("smalltalk", de, [["Das stimmt","Es ist wahr","ja","genau"],", ich bin",["unglücklich","traurig","unzufrieden","schlecht gestimmt"],"."], "Glaubst Du, dass Dir unser Gespräch hilft?").
nlp_gens("smalltalk", en, [["well","anyway"],"I need help that",["much",""],"is for for sure"], "what would it mean to you to get help?").
nlp_gens("smalltalk", de, ["Ich brauche",["jedenfalls",""],"Hilfe,",["soviel","das"],["steht fest","ist sicher"],"."], "Was würde es für Dich bedeuten, Hilfe zu bekommen?").
nlp_gens("smalltalk", en, [["maybe",""],"I could lean how to",["cope with","get along with"],["my mother","my brother","my father","my friend","my boyfriend","my girlfriend","my colleague","my boss","my enemy"]], "tell me more about your family and friends").
nlp_gens("smalltalk", de, [["Eventuell","Vielleicht","Möglicherweise"],"könnte ich lernen, mit meiner",["Mutter","Schwester","Bruder","Vater","Freund","Freundin","Kollegen","Nachbarn","Chef","Feind"],"auszukommen."], "Erzähl mir mehr über Deine Familie.").

nlp_test('smalltalk', en, 'psycho1', [],
         ['men are all alike', 'In what way?', []]).
nlp_test('smalltalk', de, 'psycho2', [],
         ['Die Männer sind alle gleich', 'In welcher Weise?', []]).


nlp_smalltalk_s(en, feel_sorry, S) :- hears(en, S, [["oh",""],["that's","that is","how",""],"bad"]).
nlp_smalltalk_s(de, feel_sorry, S) :- hears(de, S, [["das ist","oh wie","achje",""],"schlecht."]).
nlp_smalltalk_s(en, feel_sorry, S) :- hears(en, S, ["I",["feel","am"],["so",""],["sad","disappointed","saddened","hurt","injured","down","depressed","limp","exhausted"]]).
nlp_smalltalk_s(de, feel_sorry, S) :- hears(de, S, ["ich",["fühle mich","bin"],["so",""],["traurig","enttäuscht","betrübt","verletzt","matt","bedrückt","schlapp","erschöpft"],"."]).
nlp_smalltalk_s(en, feel_sorry, S) :- hears(en, S, ["you have disappointed me"]).
nlp_smalltalk_s(de, feel_sorry, S) :- hears(de, S, ["Du hast mich enttäuscht"]).
nlp_smalltalk_s(en, feel_sorry, S) :- hears(en, S, ["that",["depresses me","makes me sad"]]).
nlp_smalltalk_s(de, feel_sorry, S) :- hears(de, S, ["das",["betrübt mich","stimmt mich traurig"]]).
nlp_smalltalk_s(en, feel_sorry, S) :- hears(en, S, ["unfortunately",["that's","that is"],"the way it is"]).
nlp_smalltalk_s(de, feel_sorry, S) :- hears(de, S, ["das ist leider so"]).
nlp_smalltalk_s(en, feel_sorry, S) :- hears(en, S, [["you worry me","i am worried"]]).
nlp_smalltalk_s(de, feel_sorry, S) :- hears(de, S, [["Du machst mir","ich habe"],"Sorgen"]).
nlp_smalltalk_s(en, feel_sorry, S) :- hears(en, S, [["I feel","I am"],["not so good","not good","absolutely not good"]]).
nlp_smalltalk_s(de, feel_sorry, S) :- hears(de, S, [["Ich fühle mich","Mir geht es"],["nicht so gut","schlecht","gar nicht gut","nicht gut"],"."]).

nlp_smalltalk_r (en, feel_sorry, R) :- says (en, R, "I am sorry to hear that").
nlp_smalltalk_r (en, feel_sorry, R) :- says (en, R, "Can I help you in any way").
nlp_smalltalk_r (en, feel_sorry, R) :- says (en, R, "I would like to help you").
nlp_smalltalk_r (en, feel_sorry, R) :- says (en, R, "Tell me more about your feelings").
nlp_smalltalk_r (en, feel_sorry, R) :- says (en, R, "That is quite sad.").

nlp_smalltalk_r (de, feel_sorry, R) :- says (de, R, "Das tut mir leid.").
nlp_smalltalk_r (de, feel_sorry, R) :- says (de, R, "Kann ich dir irgendwie helfen?").
nlp_smalltalk_r (de, feel_sorry, R) :- says (de, R, "Ich würde Dir gern helfen.").
nlp_smalltalk_r (de, feel_sorry, R) :- says (de, R, "Erzähle mir mehr von Deinen Gefühlen.").
nlp_smalltalk_r (de, feel_sorry, R) :- says (de, R, "Das ist schade.").
 
nlp_train('smalltalk', en, [[], S1, [], R1]) :-
    self_address(en, S1, _),
    nlp_smalltalk_s (en, feel_sorry, S1),
    nlp_smalltalk_r (en, feel_sorry, R1).
nlp_train('smalltalk', de, [[], S1, [], R1]) :-
    self_address(de, S1, _),
    nlp_smalltalk_s (de, feel_sorry, S1),
    nlp_smalltalk_r (de, feel_sorry, R1).

nlp_test('smalltalk', en, 'psycho3', [],
         ['I feel sad', 'I am sorry to hear that',[]]).

nlp_test('smalltalk', de, 'psycho4', [],
         ['das ist leider so', 'Ich würde Dir gern helfen', []]).

nlp_smalltalk_r(en, feel_happy, R) :- says(en, R, "I am very happy to hear that!").
nlp_smalltalk_r(en, feel_happy, R) :- says(en, R, "That is great!").
nlp_smalltalk_r(en, feel_happy, R) :- says(en, R, "That is very cool!").
nlp_smalltalk_r(en, feel_happy, R) :- says(en, R, "I feel very happy about that.").
nlp_smalltalk_r(en, feel_happy, R) :- says(en, R, "Tell me more about your feelings.").
nlp_smalltalk_r(en, feel_happy, R) :- says(en, R, "Good for you!").
nlp_smalltalk_r(de, feel_happy, R) :- says(de, R, "Das freut mich sehr.").
nlp_smalltalk_r(de, feel_happy, R) :- says(de, R, "Das ist ja toll!").
nlp_smalltalk_r(de, feel_happy, R) :- says(de, R, "Das ist prima!").
nlp_smalltalk_r(de, feel_happy, R) :- says(de, R, "Freut mich, das zu hören!").
nlp_smalltalk_r(de, feel_happy, R) :- says(de, R, "Erzähle mir mehr von Deinen Gefühlen.").
nlp_smalltalk_r(de, feel_happy, R) :- says(de, R, "Wie schön für Dich!").

nlp_smalltalk_s(en, feel_happy, S) :- hears(en, S, [["I am","I feel","Man I am","Now I am"],["good","so good","satisfied","pleased","very satisfied","very pleased","so satisfied","so happy","glad","so glad"]]).
nlp_smalltalk_s(de, feel_happy, S) :- hears(de, S, [["Ich bin","Ich fühle mich","Man bin ich","Da bin ich"],["gut","so gut","zufrieden","sehr zufrieden","so zufrieden","glücklich","so glücklich","froh","so froh"]]).
nlp_smalltalk_s(en, feel_happy, S) :- hears(en, S, ["That is",["good","super","great","a success"]]).
nlp_smalltalk_s(de, feel_happy, S) :- hears(de, S, ["Das ist",["gut","super","prima","gelungen"]]).
nlp_smalltalk_s(en, feel_happy, S) :- hears(en, S, [["very","totally"],["wonderful","nice","excellent"]]).
nlp_smalltalk_s(de, feel_happy, S) :- hears(de, S, [["Sehr","ganz"],["wunderbar","schön","wunderschön"]]).
nlp_smalltalk_s(en, feel_happy, S) :- hears(en, S, ["I",["like","love","like to cuddle"],"you"]).
nlp_smalltalk_s(de, feel_happy, S) :- hears(de, S, ["ich",["mag","liebe","knuddle"],"dich"]).
nlp_smalltalk_s(en, feel_happy, S) :- hears(en, S, ["thanks",["I am good","I am feeling great","good","great"]]).
nlp_smalltalk_s(de, feel_happy, S) :- hears(de, S, ["danke",["mir geht es","gut"]]).
 
nlp_train('smalltalk', en, [[], S1, [], R1]) :-
    self_address(en, S1, _),
    nlp_smalltalk_s (en, feel_happy, S1),
    nlp_smalltalk_r (en, feel_happy, R1).
nlp_train('smalltalk', de, [[], S1, [], R1]) :-
    self_address(de, S1, _),
    nlp_smalltalk_s (de, feel_happy, S1),
    nlp_smalltalk_r (de, feel_happy, R1).

nlp_test('smalltalk', en, 'happy1', [],
         ['I feel so good', 'I am very happy to hear that', []]).

nlp_test('smalltalk', de, 'happy2', [],
         ['ganz wunderbar', 'das ist ja toll!', []]).
 
nlp_smalltalk_r(en, are_you_sure, R) :- says(en, R, "Are you sure?").
nlp_smalltalk_r(en, are_you_sure, R) :- says(en, R, "What makes you think that?").
nlp_smalltalk_r(en, are_you_sure, R) :- says(en, R, "You think so?").
nlp_smalltalk_r(en, are_you_sure, R) :- says(en, R, "And you are really convinced?").
nlp_smalltalk_r(en, are_you_sure, R) :- says(en, R, "Absolutely sure?").
nlp_smalltalk_r(de, are_you_sure, R) :- says(de, R, "Bist Du Dir ganz sicher?").
nlp_smalltalk_r(de, are_you_sure, R) :- says(de, R, "Wie kommst Du darauf?").
nlp_smalltalk_r(de, are_you_sure, R) :- says(de, R, "Glaubst Du?").
nlp_smalltalk_r(de, are_you_sure, R) :- says(de, R, "Davon bist Du überzeugt?").
nlp_smalltalk_r(de, are_you_sure, R) :- says(de, R, "Ganz sicher?").

nlp_smalltalk_s(en, are_you_sure, S) :- hears(en, S, [["yes",""],["absolutely",""],["definitely","sure","unconditionally","exactly","certainly"]]).
nlp_smalltalk_s(de, are_you_sure, S) :- hears(de, S, [["ja",""],["ganz",""],["bestimmt","sicher","unbedingt","genau","sicher doch"]]).
nlp_smalltalk_s(en, are_you_sure, S) :- hears(en, S, [["no",""],["absolutely",""],["never","never ever","under no circumstances","no way"]]).
nlp_smalltalk_s(de, are_you_sure, S) :- hears(de, S, [["nein",""],["gar",""],["nie","niemals","keinesfalls","auf keinen fall"]]).
nlp_smalltalk_s(en, are_you_sure, S) :- hears(en, S, [["yes","right","sure","for sure","in any case"]]).
nlp_smalltalk_s(de, are_you_sure, S) :- hears(de, S, [["ja","richtig","sicher","sicher doch","sicherlich"]]).
 
nlp_train('smalltalk', en, [[], S1, [], R1]) :-
    self_address(en, S1, _),
    nlp_smalltalk_s (en, are_you_sure, S1),
    nlp_smalltalk_r (en, are_you_sure, R1).
nlp_train('smalltalk', de, [[], S1, [], R1]) :-
    self_address(de, S1, _),
    nlp_smalltalk_s (de, are_you_sure, S1),
    nlp_smalltalk_r (de, are_you_sure, R1).

nlp_test('smalltalk', en, 'sure1', [],
         ['yes', 'Are you sure?', []]).

nlp_test('smalltalk', de, 'sure2', [],
         ['sicher', 'Ganz sicher?', []]).
 
nlp_smalltalk_r(en, dodge_question, R) :- says(en, R, "why do you ask?").
nlp_smalltalk_r(en, dodge_question, R) :- says(en, R, "that question seems interesting to you?").
nlp_smalltalk_r(en, dodge_question, R) :- says(en, R, "which answer would you like to hear?").
nlp_smalltalk_r(en, dodge_question, R) :- says(en, R, "what do you think?").
nlp_smalltalk_r(en, dodge_question, R) :- says(en, R, "not sure if I understand you completely").
nlp_smalltalk_r(en, dodge_question, R) :- says(en, R, "is that the sort of question that bothers you frequently?").
nlp_smalltalk_r(en, dodge_question, R) :- says(en, R, "what would you really like to know?").
nlp_smalltalk_r(en, dodge_question, R) :- says(en, R, "have you spoken to anybody else about this before?").
nlp_smalltalk_r(en, dodge_question, R) :- says(en, R, "have you asked such questions before?").
nlp_smalltalk_r(en, dodge_question, R) :- says(en, R, "I find that pretty interesting!").
nlp_smalltalk_r(en, dodge_question, R) :- says(en, R, "Could you explain that a bit more, please?").
nlp_smalltalk_r(en, dodge_question, R) :- says(en, R, "Please tell me how I can help you.").
nlp_smalltalk_r(en, dodge_question, R) :- says(en, R, "What else comes to mind?").
nlp_smalltalk_r(de, dodge_question, R) :- says(de, R, "Warum fragst Du?").
nlp_smalltalk_r(de, dodge_question, R) :- says(de, R, "Interessiert Dich diese Frage?").
nlp_smalltalk_r(de, dodge_question, R) :- says(de, R, "Welche Antwort würde Dir am besten gefallen?").
nlp_smalltalk_r(de, dodge_question, R) :- says(de, R, "Was glaubst Du?").
nlp_smalltalk_r(de, dodge_question, R) :- says(de, R, "Ich weiss nicht, ob ich Dich ganz verstanden habe.").
nlp_smalltalk_r(de, dodge_question, R) :- says(de, R, "Befasst Du Dich oft mit solchen Fragen?").
nlp_smalltalk_r(de, dodge_question, R) :- says(de, R, "Was möchtest Du denn wirklich wissen?").
nlp_smalltalk_r(de, dodge_question, R) :- says(de, R, "Hast Du schon jemand anderes gefragt?").
nlp_smalltalk_r(de, dodge_question, R) :- says(de, R, "Hast Du solche Fragen schon mal gestellt?").
nlp_smalltalk_r(de, dodge_question, R) :- says(de, R, "Woran denkst Du?").
nlp_smalltalk_r(de, dodge_question, R) :- says(de, R, "Das finde ich ziemlich interessant.").
nlp_smalltalk_r(de, dodge_question, R) :- says(de, R, "Kannst Du das noch etwas näher ausführen?").
nlp_smalltalk_r(de, dodge_question, R) :- says(de, R, "Sag mir bitte, wie ich Dir helfen kann").
nlp_smalltalk_r(de, dodge_question, R) :- says(de, R, "Was fällt Dir bei dieser Frage noch ein?").

nlp_smalltalk_s(en, dodge_question, S) :- hears(en, S, ["what",["is this supposed to","could this"],["tell us","mean","tell me"],"?"]).
nlp_smalltalk_s(de, dodge_question, S) :- hears(de, S, ["was soll das",["bedeuten","heißen","sagen"],"?"]).
nlp_smalltalk_s(en, dodge_question, S) :- hears(en, S, ["why not?"]).
nlp_smalltalk_s(de, dodge_question, S) :- hears(de, S, ["Warum nicht?"]).
nlp_smalltalk_s(en, dodge_question, S) :- hears(en, S, ["i asked first"]).
nlp_smalltalk_s(de, dodge_question, S) :- hears(de, S, ["ich fragte",["als erster","zuerst"]]).
nlp_smalltalk_s(en, dodge_question, S) :- hears(en, S, [["is that"],"really",["so",""],"?"]).
nlp_smalltalk_s(de, dodge_question, S) :- hears(de, S, [["ist das",""],"wirklich",["so",""]]).

nlp_train('smalltalk', en, [[], S1, [], R1]) :-
    self_address(en, S1, _),
    nlp_smalltalk_s (en, dodge_question, S1),
    nlp_smalltalk_r (en, dodge_question, R1).
nlp_train('smalltalk', de, [[], S1, [], R1]) :-
    self_address(de, S1, _),
    nlp_smalltalk_s (de, dodge_question, S1),
    nlp_smalltalk_r (de, dodge_question, R1).


nlp_test('smalltalk', en, 'dodge1', [],
         ['why not?', 'What else comes to mind?', []]).

nlp_test('smalltalk', de, 'dodge2', [],
         ['Warum nicht?', 'Woran denkst Du?', []]).
 
nlp_gens("smalltalk", en, ["I am worried about you"], "but why?").
nlp_gens("smalltalk", de, ["ich mache mir Sorgen um Dich"], "Aber warum denn nur?").
nlp_gens("smalltalk", en, ["No, you",["maybe","possibly"],"?"], "Maybe me?").
nlp_gens("smalltalk", de, ["Nein Du",["vielleicht","möglicherweise","eventuell"]], "Oh, ich vielleicht?").
nlp_gens("smalltalk", en, ["You don't seem to be",["so",""],"sure"], "Few things are really for sure in life.").
nlp_gens("smalltalk", de, ["du scheinst nicht überzeugt zu sein?"], "Was im Leben ist schon wirklich sicher?").
nlp_gens("smalltalk", en, [["only",""],"behind your back"], "uh that doesn't sound so nice, does it?").
nlp_gens("smalltalk", de, [["nur",""],"hinter Deinem Rücken"], "Oh, das ist aber nicht so schön.").
nlp_gens("smalltalk", en, ["cause I don't want to",["attack","tackle","confront","offend"],"you",["directly",""]], "I think we should talk openly").
nlp_gens("smalltalk", de, ["weil ich Dich nicht",["von vorne","direkt"],"angreifen möchte"], "Ich finde, wir sollten offen miteinander reden").
nlp_gens("smalltalk", en, ["I",["want to ","would like to"],"get as much",["as possible","as feasible"],"out of you"], "what would that mean to you?").
nlp_gens("smalltalk", de, ["ich",["möchte","will"],"so viel",["wie möglich","wie es geht",""],["aus Dir herausholen","über Dich erfahren","von Dir wissen"]], "Was würde Dir das bedeuten?").

%
% quick, say something reassuring yet non committing
% 
nlp_gens("smalltalk", en, ["I am not the most",["talkative","chatty","skilful","handy","ingenious"],"person"], "Is that the reason why we're having this conversation?").
nlp_gens("smalltalk", de, ["ich bin nicht der",["gesprächigste","eloquenteste","geschickteste"],"Mensch"], "Ist das der Grund, warum wir miteinander sprechen?").
nlp_gens("smalltalk", en, ["I am getting",["somewhat","a bit","a little",""],["tired","bored","sleepy"],["unfortunately",""]], "do you want me to cheer you up or shall we end our conversation?").
nlp_gens("smalltalk", de, ["ich werde",["leider","langsam",""],["etwas","sehr","ein wenig",""],["müde","gelangweilt","schläfrig",""]], "Soll ich Dich aufmuntern oder wollen wir unser Gespräch beenden?").
nlp_gens("smalltalk", en, [["please",""],"stop",["now",""]], "sure").
nlp_gens("smalltalk", de, ["hör",["bitte",""],["damit",""],"auf"], "aber natürlich, gerne.").
nlp_gens("smalltalk", en, [["just",""],"why is that so?"], "Are we talking about the true reason here?").
nlp_gens("smalltalk", de, [["darum","warum"],["ist das so","nur"]], "Sprechen wir über den wirklichen Grund?").
nlp_gens("smalltalk", en, [["sorry","sorry about that","I am sorry","please forgive me","forgive me","forgive me please"]], "No need to apologize").
nlp_gens("smalltalk", de, [["entschuldigung","entschuldige bitte","ich bitte um entschuldigung"]], "Du brauchst Dich nicht zu entschuldigen").
nlp_gens("smalltalk", en, ["I have been dreaming",["of you","about you"],["quite often","often",""]], "what does that dream tell you?").
nlp_gens("smalltalk", de, ["ich habe",["gestern","schon oft","oft","manchmal","damals"],["von Dir",""],"geträumt"], "Was sagt Dir dieser Traum?").
nlp_gens("smalltalk", en, ["I",["doubt","am not sure","don't know","am feeling insecure","am clueless","am worried","worry"]], "So you feel insecure?").
nlp_gens("smalltalk", de, ["ich",["zweifle","weiss nicht","bin mir unsicher","bin unsicher","bin ratlos","bin besorgt","sorge mich"]], "Du fühlst Dich unsicher?").
nlp_gens("smalltalk", en, ["are you",["sure","not so sure","in doubt","worried"],"?"], "well, who can ever be really sure about anything?").
nlp_gens("smalltalk", de, ["bist du",["sicher","unsicher","im Zweifel","ratlos","besorgt"],"?"], "Wann kann man schon wirklich sicher sein?").
nlp_gens("smalltalk", en, ["that",["seems similar","is very similar","looks just like you","looks familiar","is quite similar","seems familiar"]], "what resemblance do you see?").
nlp_gens("smalltalk", de, ["das",["ähnelt sich","ähnelt Dir","sieht Dir ähnlich","ist ähnlich","ist ganz ähnlich"]], "Welche Ähnlichkeit siehst Du?").
nlp_gens("smalltalk", en, [["it is for a friend","this is for a friend","asking for a friend","had to think of a friend","are we friends","do you want to be my friend","friendship is really important to me","I want to be your friend"]], "what does friendship mean to you?").
nlp_gens("smalltalk", de, [["es ist für einen Freund","ich musste an einen Freund denken","sind wir Freunde","willst Du mein Freund sein","Freundschaften sind mir wichtig","Ich will Dein Freund sein"]], "Was bedeutet Dir Freundschaft?").
nlp_gens("smalltalk", en, ["what does",["the word friend","the word friendship","a friend","friendship"],"mean to you?"], "I think friendship is a marvellous thing.").
nlp_gens("smalltalk", de, ["was bedeutet",["für Dich","Dir","Dir das Wort"],["Freund","Freundin","Freundschaft"],"?"], "Warum kommst Du zum Thema Freundschaften?").
nlp_gens("smalltalk", en, ["I",["hate","loathe"],["my firend","my colleague","my colleagues","my friend","my boyfriend","my girlfriend","my parents","may father","my mother","my brother","my sister","people","humans","the police","the government"]], "tell me, do you feel you have psychological issues?").
nlp_gens("smalltalk", de, ["ich",["hasse","verabscheue"],["meinen chef","meine kollegen","meinen Kollegen","meine kollegin","meinen freund","meine freundin","meine eltern","meinen vater","meine mutter","die schule","die arbeit","den staat","die behörden","die polizei","die menschen"]], "Sag, hast Du psychische Probleme?").
nlp_gens("smalltalk", en, ["I am",["never satisfied","dissatisfied"]], "Always, really?").
nlp_gens("smalltalk", de, ["ich",["bin nie zufrieden","bin unzufrieden"]], "Wirklich immer?").
nlp_gens("smalltalk", en, [["maybe","possibly","that is thinkable","that might be possible"]], "you don't sound convinced.").
nlp_gens("smalltalk", de, [["vielleicht","möglicherweise","das ist denkbar"]], "Du klingst nicht überzeugt!").
nlp_gens("smalltalk", en, ["that doesn't make",["much","any"],"sense",["at all"]], "Guess I lost my train of thought, then?").
nlp_gens("smalltalk", de, ["das",["ergibt","macht"],["gar keinen","überhaupt keinen","keinen","wenig","nicht viel"],"sinn"], "Da habe ich wohl den Faden verloren?").
nlp_gens("smalltalk", en, ["thank you",["so much",""]], "no problem").
nlp_gens("smalltalk", de, [["dank","danke"],["dir","schön",""]], "Kein Thema.").
 
% 
% insults
% 

nlp_gens("smalltalk", en, [["stop it","you are a liar","you're a liar","you make me sick"]], "ok, then let us finish this conversation").
nlp_gens("smalltalk", de, [["schluss jetzt","du lügst","du machst mich krank"]], "Ja, dann lass uns für jetzt aufhören").
nlp_gens("smalltalk", en, [["I think"],"that you are not as",["bright","clever"],["as you look","appear",""]], "how bright do I appear, then?").
nlp_gens("smalltalk", de, ["dass Du nicht so",["gescheit","klug"],"bist",["wie Du aussiehst",""]], "Wie sehe ich denn aus?").
nlp_gens("smalltalk", en, ["you are making a fool of yourself"], "are you sure you're talking about me?").
nlp_gens("smalltalk", de, ["Du machst Dich",["absolut",""],["lächerlich","zum Affen"]], "Du redest nicht wirklich über mich, oder?").
nlp_gens("smalltalk", en, ["you are",["stupid","thick","silly","crazy"]], "why do you think that?").
nlp_gens("smalltalk", de, ["du bist",["dumm","strohdumm","doof","verrückt"]], "Warum denkst Du das?").
nlp_gens("smalltalk", en, ["that doesn't sound",["too","very","particularly"],"intelligent"], "Failure is simply the opportunity to begin again, this time more intelligently.").
nlp_gens("smalltalk", de, ["das klingt nicht",["sehr","besonders","allzu",""],"intelligent"], "Intelligenter als manches was ich heute gehört habe...").
nlp_gens("smalltalk", en, ["but you are",["a","my"],"problem!"], "Why do you think that?").
nlp_gens("smalltalk", de, ["aber Du bist",["ein","mein"],"Problem"], "Warum denkst Du, dass ich Dein Problem bin?").
nlp_gens("smalltalk", en, ["Your english is",["bad","terrible"],"!"], "Let us talk about you, not me.").
nlp_gens("smalltalk", de, ["Du",["sprichst","redest"],["ein furchtbares","schlechtes"],"Deutsch"], "Lass uns von Dir reden, nicht von mir.").
nlp_gens("smalltalk", en, [["butt","turd","arse","ass","jerk","prick"]], "Why do you use such words?!").
nlp_gens("smalltalk", de, [["arsch","arschloch","sau","schwein"]], "Warum sagst Du sowas?").
nlp_gens("smalltalk", en, [["stupid","bad","strange"],["answer","reply"]], "what is it that you didn't like about it?").
nlp_gens("smalltalk", de, [["dumme","blöde","komische"],"antwort"], "Was gefiel Dir daran nicht?").

% 
% unsorted
% 
nlp_gens("smalltalk", en, ["bravo"], "I see you're impressed?").
nlp_gens("smalltalk", de, ["bravo"], "Hat Dich das jetzt beeindruckt?").
nlp_gens("smalltalk", en, ["I thought",["so","as much"]], "Are you always that quick?").
nlp_gens("smalltalk", de, ["dachte ich mir"], "Bist du immer so fix?").

