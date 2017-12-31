#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# basic dialog building blocks
#
# we provide just eliza-style responses here for the most part, but other modules may re-use
# these building blocks and provides more meaningful higher-scoring responses
#

def get_data(k):

    k.dt_set_prefix('{self_address:L} ')

    #
    # say again type follow up questions
    #

    # train(en) :- and("(huh|say again please|say again|what was that)?", prev(C, PC), list_findall(X, say(PC, X), L), list_str_join(" ", L, S), or("I said {S, s}", "As I just said {S, s}", "I repeat {S, s}")).

    def say_again_en(c):

        if len(c.log_me) == 0:
            c.response ("I don't think we have spoken before.")
            return

        s = c.log_me[len(c.log_me)-1].resp

        c.response("I said %s" % s, 0.0, [])
        c.response("As I just said %s" % s, 0.0, [])
        c.response("I repeat %s" %s , 0.0, [])

    k.dt('en', "(huh|say again please|say again|what was that)?", say_again_en)

#    train(de) :- and("(was|wie war das|bitte sag nochmal was du gesagt hast|wie bitte)?", prev(C, PC), list_findall(X, say(PC, X), L), list_str_join(" ", L, S), or("Ich sagte {S, s}", "Ich sagte gerade {S, s}", "Ich wiederhole {S, s}")).

    k.dt('en', [u"correct",
                u"this is true",
                u"that's so",
                u"that's the truth",
                u"that's true"],
               u"Good.")
    k.dt('de', [u"richtig",
                u"das ist wahr",
                u"das ist so",
                u"das ist die Wahrheit",
                u"das ist richtig"],
               u"Gut.")

    k.dt('en', u"you're right", u"So we're in agreement?")
    k.dt('de', u"da hast du recht", u"Wir sind uns also einig?")

    k.dt('en', u"that's right", u"You agree?")
    k.dt('de', u"das ist richtig", u"Du stimmst zu?")

    k.dt('en', [u"not correct",
                u"that is not correct",
                u"that is wrong",
                u"that's not true",
                u"that's certainly not true"],
               [u"So what is the truth?",
                u"What do you think is right?"])
    k.dt('de', [u"falsch",
                u"das ist aber nicht korrekt",
                u"das ist falsch",
                u"das stimmt nicht",
                u"das stimmt sicher nicht"],
               [u"Was ist dann die Wahrheit?",
                u"Was glaubst Du?"])

    k.dt('en', u"a fact", u"I love facts.")
    k.dt('de', u"ein faktum", u"I liebe Fakten.")

    k.dt('en', u"that's a fact", u"I love facts.")
    k.dt('de', u"das ist eine tatsache", u"I liebe Fakten.")

    k.dt('en', u"this is not a rumor but the truth", u"Are you sure about that?")
    k.dt('de', u"das ist kein gerücht sondern die wahrheit", u"Bist Du dir da sicher?")

    k.dt('en', u"ok", u"Cool.")
    k.dt('de', u"okay", u"Cool.")

    k.dt('en', u"actually yes", u"Really?")
    k.dt('de', u"eigentlich ja", u"Wirklich?")

    k.dt('en', u"I'd rather not", u"OK, then not.")
    k.dt('de', u"lieber nicht", u"OK, dann nicht.")

    k.dt('en', u"apparently not", u"apparently?")
    k.dt('de', u"anscheinend nicht", u"anscheinend?")

    k.dt('en', u"fine", u"Good.")
    k.dt('de', u"fein", u"Gut.")

    k.dt('en', u"very well", u"Excellent!")
    k.dt('de', u"bestens", u"Prima!")

    k.dt('en', u"goes so", u"Can you elaborate on that?")
    k.dt('de', u"geht so", u"Kannst Du das näher ausführen?")

    k.dt('en', u"but only almost", u"What's missing?")
    k.dt('de', u"aber nur fast", u"Was fehlt?")

    k.dt('en', u"hell", u"If you're going through hell, keep going.")
    k.dt('de', u"hölle", u"Wenn Du durch die Hölle gehst, geh weiter.")

    k.dt('en', u"caught", u"Time to hide?")
    k.dt('de', u"erwischt", u"Zeit sich zu verstecken?")

    k.dt('en', [u"achso",
                u"aha",
                u"oh"],
               u"An Inspiration?")
    k.dt('de', [u"achso",
                u"aha",
                u"oh"],
               u"Eine Eingebung?")

    k.dt('en', u"also", u"Please, elaborate.")
    k.dt('de', u"auch", u"Sprich bitte weiter.")

    k.dt('en', [u"amazing",
                u"fascinating",
                u"crass",
                u"cool"],
               u"What do you like in particular?")
    k.dt('de', [u"erstaunlich",
                u"faszinierend",
                u"krass",
                u"cool"],
               u"Was gefällt Dir besonders?")

    k.dt('en', u"for real", u"Isn't reality a strange concept?")
    k.dt('de', u"wirklich", u"Ist Wirklichkeit nicht ein merkwüriger Begriff?")

    k.dt('en', [u"funny",
                u"lol"],
               u"I like it when you're happy.")
    k.dt('de', [u"komisch",
                u"lol"],
               u"Ich mag es, wenn Du fröhlich bist.")

    k.dt('en', u"creepy", u"Did you hear that?")
    k.dt('de', u"gruselig", u"Hast Du das gehört?")

    k.dt('en', u"dazzling", u"What color?")
    k.dt('de', u"blendend", u"Welche Farbe?")

    k.dt('en', [u"a pity",
                u"this is a pity"],
               u"You sound a bit sad.")
    k.dt('de', [u"schade",
                u"das ist schade"],
               u"Du klingst ein wenig betrübt.")

    k.dt('en', u"great", u"excellent.")
    k.dt('de', u"toll", u"prima.")

    k.dt('en', u"that's terrible", u"oh dear!")
    k.dt('de', u"das ist ja schrecklich", u"Ohje!")

    k.dt('en', u"that's too bad", u"oh dear!")
    k.dt('de', u"das ist sehr schade", u"Ohje!")

    k.dt('en', u"that's unfair", u"Life isn't always fair, I guess.")
    k.dt('de', u"das ist unfair", u"Das Leben ist nicht immer Fair, fürchte ich.")

    k.dt('en', [u"aha what?",
                u"what what?"],
               u"Sorry, must have lost my train of thought here.")
    k.dt('de', [u"wie aha",
                u"wie was"],
               u"Entschuldige, ich muss meinen Faden verloren haben an der Stelle.")

    k.dt('en', u"absolutely nothing", u"Are you sure?")
    k.dt('de', u"absolut nichts", u"Bist Du Dir sicher?")

    k.dt('en', u"everything", u"Really everything?")
    k.dt('de', u"alles", u"Wirklich alles?")

    k.dt('en', u"but that is little", u"You think so?")
    k.dt('de', u"das ist aber wenig", u"Denkst Du?")

    k.dt('en', u"they are never so many", u"Never?")
    k.dt('de', u"das sind niemals so viele", u"Niemals?")

    k.dt('en', u"both", u"What else?")
    k.dt('de', u"beides", u"Was sonst noch?")

    k.dt('en', u"a green one", u"Really, a green one?")
    k.dt('de', u"einen grünen", u"Wirklich, einen grünen?")

    k.dt('en', u"a claim from me", u"An original?")
    k.dt('de', u"ein spruch von mir", u"Ein original?")

    k.dt('en', u"this is my opinion", u"Which you are entitled to.")
    k.dt('de', u"das ist meine meinung", u"Zu der Du berechtigt bist.")

    k.dt('en', u"a fairy tale", u"Do you like fairy tales?")
    k.dt('de', u"ein märchen", u"Magst Du Märchen?")

    k.dt('en', u"a secret", u"can you keep it?")
    k.dt('de', u"ein geheimnis", u"Kannst Du es bewahren?")

    k.dt('en', [u"an assertion",
                u"an interesting hypothesis"],
               u"Maybe?")
    k.dt('de', [u"eine behauptung",
                u"eine interessante hypothese"],
               u"Vielleicht?")

    k.dt('en', u"that is a bad assumption", u"Really?")
    k.dt('de', u"das ist ein böse unterstellung", u"Wirklich?")

    k.dt('en', [u"as a matter of fact",
                u"but it is so"],
               u"How does that make you feel?")
    k.dt('de', [u"in der tat",
                u"das ist aber so"],
               u"Und wie fühlst Du dich dabei?")

    k.dt('en', [u"about me",
                u"because of me"],
               u"Really, you?")
    k.dt('de', [u"über mich",
                u"meinetwegen"],
               u"Wirklich, Du?")

    k.dt('en', u"pretty stupid", u"To err is human.")
    k.dt('de', u"schön blöd", u"Irren ist menschlich.")

    k.dt('en', [u"about you",
                u"about yours"],
               u"Me?")
    k.dt('de', [u"über dich",
                u"über deins"],
               u"Ich?")

    k.dt('en', u"but you do it", u"Really?")
    k.dt('de', u"aber du tust es", u"Wirklich?")

    k.dt('en', u"and yours", u"Mine?")
    k.dt('de', u"und deiner", u"Meiner?")

    k.dt('en', u"after that", u"Then?")
    k.dt('de', u"danach", u"Dann?")

    k.dt('en', u"but how?", u"Can you think of a way?")
    k.dt('de', u"wie denn auch", u"Kennst Du einen Weg?")

    k.dt('en', u"absolute", u"Sure?")
    k.dt('de', u"absolut", u"Sicher?")

    k.dt('en', u"as", u"Please, go on.")
    k.dt('de', u"wie", u"Bitte, sprich weiter.")

    k.dt('en', [u"but",
                u"different"],
               u"Please, go on.")
    k.dt('de', [u"doch",
                u"anders"],
               u"Bitte, sprich weiter.")

    k.dt('en', [u"at school",
                u"i learned that in school"],
               u"Education is such an important thing.")
    k.dt('de', [u"in der schule",
                u"das habe ich in der schule gelernt"],
               u"Bildung ist so eine Wichtige Angelegenheit.")

    k.dt('en', u"but what", u"Do you have an idea?")
    k.dt('de', u"aber was", u"Hast Du eine Idee?")

    k.dt('en', u"by which", u"Do you have an idea?")
    k.dt('de', u"womit", u"Hast Du eine Idee?")

    k.dt('en', u"can't you say that more precisely", u"what is not clear to you?")
    k.dt('de', u"kannst du das nicht genauer sagen", u"was ist dir unklar?")

    k.dt('en', u"can you do that", u"not sure")
    k.dt('de', u"kannst du das", u"da bin ich mir nicht sicher")

    k.dt('en', u"can you do that too", u"not sure")
    k.dt('de', u"kannst du das auch", u"da bin ich mir nicht sicher")

    k.dt('en', u"coincidence", u"happens.")
    k.dt('de', u"zufall", u"gibt es.")

    k.dt('en', [u"conclude",
                u"depends on"],
               u"interesting")
    k.dt('de', [u"schließen",
                u"kommt drauf an"],
               u"interessant.")

    k.dt('en', u"do that", u"Please?")
    k.dt('de', u"tu das", u"Bitte?")

    k.dt('en', [u"do you believe it",
                u"do you believe me"],
               u"I want to believe")
    k.dt('de', [u"glaubst du es",
                u"glaubst du mir"],
               u"Ich will glauben.")

    k.dt('en', u"do you know irony", u"People find me ironic quite frequently.")
    k.dt('de', u"kennst du ironie", u"Die Leute finden mich oft ironisch.")

    k.dt('en', u"do you know someone there?", u"Can't tell.")
    k.dt('de', u"kennst du da jemanden", u"Kann ich nicht sagen.")

    k.dt('en', u"do you know who", u"Not sure.")
    k.dt('de', u"weißt du wer ", u"Da bin ich mir nicht sicher.")

    k.dt('en', u"do you know", u"Not sure.")
    k.dt('de', u"kennst du", u"Bin unsicher.")

    k.dt('en', u"do you want to learn it?", u"I am always willing to learn!")
    k.dt('de', u"willst du es lernen", u"Ich will immer lernen!")

    k.dt('en', u"do you", u"Me?")
    k.dt('de', u"du etwa", u"Ich?")

    k.dt('en', [u"dreams",
                u"emotions"],
               u"Dreams and emotions must be wonderful things.")
    k.dt('de', [u"träume",
                u"gefühle"],
               u"Träume und Gefühle müssen etwas wunderbares sein.")

    k.dt('en', u"every day", u"Really?")
    k.dt('de', u"jeden tag", u"Wirklich?")

    k.dt('en', [u"exactly here",
                u"finished"],
               u"Right here and now?")
    k.dt('de', [u"genau hier",
                u"fertig"],
               u"Genau hier und jetzt?")

    k.dt('en', u"for fun", u"I see.")
    k.dt('de', u"zum spaß", u"Verstehe.")

    k.dt('en', u"for what", u"That is the question.")
    k.dt('de', u"wofür", u"Das ist die Frage.")

    k.dt('en', u"for whom", u"That is the question.")
    k.dt('de', u"für wen", u"Das ist die Frage.")

    k.dt('en', u"for me", u"That is the question.")
    k.dt('de', u"für mich", u"Das ist die Frage.")

    k.dt('en', u"forever", u"Really?")
    k.dt('de', u"für immer", u"Wirklich?")

    k.dt('en', u"from where", u"That is the question.")
    k.dt('de', u"woher", u"Das ist die Frage.")

    k.dt('en', u"from whom", u"That is the question.")
    k.dt('de', u"von wem", u"Das ist die Frage.")

    k.dt('en', u"give it a try", u"I will think about it.")
    k.dt('de', u"versuche es doch einmal", u"Ich werde darüber nachdenken.")

    k.dt('en', u"give it to me", u"You can have it.")
    k.dt('de', u"gibs mir", u"Du kannst es haben.")

    k.dt('en', u"good as well", u"So we are in agreement?")
    k.dt('de', u"auch gut", u"Wir stimmen also überein?")

    k.dt('en', u"good point", u"Thanks.")
    k.dt('de', u"guter punkt", u"Danke.")

    k.dt('en', u"good question", u"I thought so.")
    k.dt('de', u"gute frage", u"Dachte ich mir.")

    k.dt('en', u"choose", u"I often find it hard to choose.")
    k.dt('de', u"wähle", u"I finde es oft schwer, mich zu entscheiden.")

    k.dt('en', u"Does that have anything to do with it", u"Don't you think?")
    k.dt('de', u"hat das was damit zu tun", u"Denkst Du nicht?")

    k.dt('en', u"have none", u"Want one?")
    k.dt('de', u"habe keines", u"Möchtest Du eines?")

    k.dt('en', u"honestly not", u"I see.")
    k.dt('de', u"ehrlich nicht", u"Verstehe.")

    k.dt('en', u"hopefully soon", u"OK, let's hope.")
    k.dt('de', u"hoffentlich bald", u"OK, lass uns hoffen.")

    k.dt('en', u"what and", u"Can you think of something?")
    k.dt('de', u"wie und", u"Fällt Dir etwas ein?")

    k.dt('en', u"how boring", u"Let's talk about something more exciting then!")
    k.dt('de', u"wie langweilig", u"Dann lass uns über etwas aufregenderes reden!")

    k.dt('en', u"how come", u"Not sure.")
    k.dt('de', u"wie denn", u"Bin mir nicht sicher.")

    k.dt('en', u"how do you know", u"Typically my knowledge base is behind that.")
    k.dt('de', u"woher weißt du das", u"Typischerweise ist es meine Wissensbasis, die dahintersteckt.")

    k.dt('en', u"how does it continue?", u"Not sure.")
    k.dt('de', u"wie geht es weiter", u"Bin mir nicht sicher.")

    k.dt('en', u"how is he", u"Hopefully fine?")
    k.dt('de', u"wie ist er so", u"Hoffentlich gut?")

    k.dt('en', u"how long is a while", u"longer than a moment but shorter than eternity, I think.")
    k.dt('de', u"wie lange ist eine weile", u"Länger als ein Moment aber kürzer als eine Ewigkeit, denke ich.")

    k.dt('en', [u"how many",
                u"how much exactly"],
               u"Can't tell.")
    k.dt('de', [u"wie viele",
                u"wie viel genau"],
               u"Kann ich nicht sagen.")

    k.dt('en', u"how should he look like", u"Good, I hope!")
    k.dt('de', u"wie soll er aussehen", u"Gut, hoffe ich!")

    k.dt('en', u"how should i know that", u"Tough question?")
    k.dt('de', u"wie soll ich das wissen", u"Schwierige Frage?")

    k.dt('en', [u"i agree",
                u"i am of your opinion"],
               u"So we are in agreement?")
    k.dt('de', [u"ich stimme zu",
                u"ich bin deiner meinung"],
               u"Wir sind uns also einig?")

    k.dt('en', u"i am very much for harmony", u"me too!")
    k.dt('de', u"ich bin sehr für harmonie", u"ich auch!")

    k.dt('en', u"i ask for it", u"No problem.")
    k.dt('de', u"ich bitte darum", u"Kein Problem.")

    k.dt('en', u"i assert that", u"I see.")
    k.dt('de', u"das behaupte ich", u"Verstehe.")

    k.dt('en', u"i can do it", u"I'm sure of it.")
    k.dt('de', u"ich kann es halt", u"Da bin ich mir sicher.")

    k.dt('en', u"i conclude something", u"Yes?")
    k.dt('de', u"ich schließe etwas", u"Ja?")

    k.dt('en', [u"i do not believe it",
                u"i do not believe that",
                u"i do not believe you"],
               u"You have doubts?")
    k.dt('de', [u"ich glaube es nicht",
                u"das glaube ich nicht",
                u"das glaube ich dir nicht"],
               u"Du hast Zweifel?")

    k.dt('en', u"i do not care", u"Maybe I don't either.")
    k.dt('de', u"mir egal", u"Mir vielleicht auch.")

    k.dt('en', u"i do not have one", u"Would you like one?")
    k.dt('de', u"ich habe keins", u"Hättest Du gerne eines?")

    k.dt('en', u"i do not know anyone", u"Well, you know me for starters.")
    k.dt('de', u"ich kenne keinen", u"Nun, Du kennst mich - das ist ein Anfang.")

    k.dt('en', u"i do not know exactly", u"Maybe you need to think about it some more?")
    k.dt('de', u"ich weiss nicht genau", u"Vielleicht mußt Du mehr darüber nachdenken?")

    k.dt('en', [u"i do not know that",
                u"i do not know yet",
                u"i do not know"],
               u"Can I help you?")
    k.dt('de', [u"das weiss ich nicht",
                u"ich weiss es noch nicht",
                u"weiss nicht"],
               u"Kann ich Dir helfen?")

    k.dt('en', [u"i do not see any",
                u"i do not think so"],
               u"Does that bother you?")
    k.dt('de', [u"ich sehe keinen",
                u"ich glaube nicht"],
               u"Stört Dich das?")

    k.dt('en', u"i do not want", u"Then you shouldn't.")
    k.dt('de', u"ich will nicht", u"Dann solltest Du auch nicht.")

    k.dt('en', [u"i dont see any",
                u"i had the impression"],
               u"OK.")
    k.dt('de', [u"ich sehe keine",
                u"ich hatte den eindruck"],
               u"OK.")

    k.dt('en', u"i have already done that", u"How do you feel about it?")
    k.dt('de', u"das habe ich schon gemacht", u"Wie fühlt sich das an?")

    k.dt('en', u"i have found that myself", u"I see.")
    k.dt('de', u"das habe ich selbst festgestellt", u"Verstehe.")

    k.dt('en', u"i hear", u"What would you like to hear?")
    k.dt('de', u"ich höre", u"Was möchtest Du gerne hören?")

    k.dt('en', u"i just know it", u"I guess that is called inspiration?")
    k.dt('de', u"ich weiss es einfach", u"Ich vermute das nennt sich Inspiration?")

    k.dt('en', [u"i know it",
                u"i know one",
                u"i know"],
               u"Knowledge is important.")
    k.dt('de', [u"ich weiss es",
                u"ich kenne einen",
                u"ich weiss"],
               u"Wissen ist wichtig.")

    k.dt('en', u"i like to do that", u"How do you feel about it?")
    k.dt('de', u"das tue ich gerne", u"Wie fühlt sich das an?")

    k.dt('en', u"i must not", u"why not?")
    k.dt('de', u"ich darf nicht", u"warum nicht?")

    k.dt('en', u"i myself, of course", u"Sure.")
    k.dt('de', u"ich selbst natürlich", u"Klar.")

    k.dt('en', u"i conclude it's you", u"Me?")
    k.dt('de', u"ich schließe auf dich", u"Ich?")

    k.dt('en', [u"i sometimes ask myself that too",
                u"i think it's a rumor"],
               u"I'm not sure either.")
    k.dt('de', [u"das frage ich mich auch manchmal",
                u"das halte ich für ein gerücht"],
               u"Ich bin mir auch unsicher.")

    k.dt('en', u"i think he's very nice", u"good.")
    k.dt('de', u"ich finde ihn sehr schön", u"gut.")

    k.dt('en', [u"i think so too",
                u"i think so"],
               u"So we are in agreement?")
    k.dt('de', [u"denke ich auch",
                u"ich glaube schon"],
               u"Wir sind uns also einig?")

    k.dt('en', u"i thought to myself", u"I see.")
    k.dt('de', u"das habe ich mir gedacht", u"Verstehe.")

    k.dt('en', u"i understand", u"glad to hear that.")
    k.dt('de', u"ich verstehe", u"bin froh das zu hören.")

    k.dt('en', u"i understood you like this", u"I see.")
    k.dt('de', u"ich habe dich so verstanden", u"Verstehe.")

    k.dt('en', [u"i want it all",
                u"i want"],
               u"You'd be happier then?")
    k.dt('de', [u"ich will alles",
                u"ich will"],
               u"Wärest Du dann glücklicher?")

    k.dt('en', u"i want to know that from you", u"From me?")
    k.dt('de', u"das will ich von dir wissen", u"Von mir?")

    k.dt('en', u"i will create one", u"Tell me when you are done.")
    k.dt('de', u"ich werde eine erstellen", u"Sag mir, wenn Du fertig bist.")

    k.dt('en', u"i will do that for you", u"For me?")
    k.dt('de', u"ich werde das für dich tun", u"Für mich?")

    k.dt('en', u"i would like to know that too", u"Have you checked the internet?")
    k.dt('de', u"das wüsste ich auch gern", u"Hast Du es im Internet probiert?")

    k.dt('en', u"i", u"You?")
    k.dt('de', u"ich", u"Du?")

    k.dt('en', u"i'm me", u"Sure.")
    k.dt('de', u"ich bin ich", u"Sicher.")

    k.dt('en', u"i'll wait", u"For what?")
    k.dt('de', u"ich werde warten", u"Worauf?")

    k.dt('en', u"i feel pranked", u"I see.")
    k.dt('de', u"ich komme mir verarscht vor", u"Verstehe.")

    k.dt('en', u"if you like", u"Not sure.")
    k.dt('de', u"wenn du magst", u"Bin mir nicht sicher.")

    k.dt('en', u"if you want", u"Not sure.")
    k.dt('de', u"wenn du willst", u"Bin mir nicht sicher.")

    k.dt('en', u"if you're interested", u"I am always interested!")
    k.dt('de', u"wenn es dich interessiert", u"Ich bin immer interessiert!")

    k.dt('en', u"in order", u"Excellent.")
    k.dt('de', u"in ordnung", u"Ausgezeichnet.")

    k.dt('en', u"in the bag", u"What bag?")
    k.dt('de', u"in der tasche", u"Welche Tasche?")

    k.dt('en', u"in the moment not", u"Maybe later?")
    k.dt('de', u"im moment nicht", u"Vielleicht später?")

    k.dt('en', u"in which respect", u"Which respect comes to mind?")
    k.dt('de', u"in welcher hinsicht", u"Welche Hinsicht fällt Dir ein?")

    k.dt('en', u"in your brain", u"You mean my reasoning engine?")
    k.dt('de', u"in deinem gehirn", u"Du meinst meine Logik?")

    k.dt('en', u"indeed", u"Please, continue.")
    k.dt('de', u"allerdings", u"Bitte, sprich weiter.")

    k.dt('en', u"is it you", u"Yes, it's me.")
    k.dt('de', u"bist du es", u"Ja, ich bin es.")

    k.dt('en', [u"interesting",
                u"is clear"],
               u"I see.")
    k.dt('de', [u"interessant",
                u"ist klar"],
               u"Verstehe.")

    k.dt('en', [u"is that an advantage",
                u"is that pleasant",
                u"is that so much"],
               u"Not sure.")
    k.dt('de', [u"ist das ein vorteil",
                u"ist das angenehm",
                u"ist das so viel"],
               u"Bin nicht sicher.")

    k.dt('en', u"it depends", u"")
    k.dt('de', u"kommt ganz darauf an", u"")

    k.dt('en', u"it is 42", u"I love the Hitchhiker's Guide.")
    k.dt('de', u"sie lautet zweiundvierzig", u"Ich liebe per Anhalter durch die Galaxis.")

    k.dt('en', u"it is not necessary", u"Sure?")
    k.dt('de', u"es ist nicht nötig", u"Sicher?")

    k.dt('en', u"it is very good", u"Excellent.")
    k.dt('de', u"es ist sehr gut", u"Ausgezeichnet.")

    k.dt('en', u"it works", u"Good.")
    k.dt('de', u"es geht", u"Gut.")

    k.dt('en', u"it's good", u"Glad to hear that!")
    k.dt('de', u"das ist gut", u"Freue mich, das zu hören.")

    k.dt('en', u"it's not easy", u"But worth doing anyway?")
    k.dt('de', u"es ist ja auch nicht einfach", u"Aber es lohnt sich trotzdem?")

    k.dt('en', u"it's perfectly alright", u"Good.")
    k.dt('de', u"ganz okay", u"Gut.")

    k.dt('en', u"just because", u"Can you elaborate?")
    k.dt('de', u"einfach so", u"Kannst Du das weiter ausführen?")

    k.dt('en', u"just like you", u"Like me?")
    k.dt('de', u"so wie du", u"Wie ich?")

    k.dt('en', u"kind of", u"Please, go on.")
    k.dt('de', u"so in der art", u"Sprich bitte weiter.")

    k.dt('en', u"look at all the consequences", u"Sure.")
    k.dt('de', u"schau dir alle folgen an", u"Klar.")

    k.dt('en', u"make a suggestion", u"Don't worry, be happy.")
    k.dt('de', u"mach einen vorschlag", u"Sorge Dich nicht, sei fröhlich.")

    k.dt('en', u"may be", u"how likely do you think?")
    k.dt('de', u"kann sein", u"wie wahrscheinlich, glaubst du?")

    k.dt('en', [u"me too",
                u"me",
                u"me, yes"],
               u"you?")
    k.dt('de', [u"mir auch",
                u"ich denn",
                u"ich schon"],
               u"Du?")

    k.dt('en', [u"mine also",
                u"mine too"],
               u"you?")
    k.dt('de', [u"meins auch",
                u"meiner auch"],
               u"Du?")

    k.dt('en', u"more often", u"how often then?")
    k.dt('de', u"öfters", u"Wie oft dann?")

    k.dt('en', u"my also", u"I see.")
    k.dt('de', u"meine auch", u"Verstehe.")

    k.dt('en', u"naturally", u"OK")
    k.dt('de', u"natürlich", u"OK")

    k.dt('en', [u"neither do i",
                u"never in life"],
               u"Not?")
    k.dt('de', [u"ich auch nicht",
                u"nie im leben"],
               u"Nicht?")

    k.dt('en', u"never mind", u"Please continue.")
    k.dt('de', u"keine ursache", u"Bitte setze fort.")

    k.dt('en', u"no idea", u"Really?")
    k.dt('de', u"keine ahnung", u"Wirklich?")

    k.dt('en', u"no matter", u"Sure?")
    k.dt('de', u"egal", u"Sicher?")

    k.dt('en', u"no more and no less", u"You sound pretty sure?")
    k.dt('de', u"nicht mehr und nicht weniger", u"Du klingst ziemlich sicher?")

    k.dt('en', u"no problem", u"Sure.")
    k.dt('de', u"kein problem", u"Sicher.")

    k.dt('en', u"none", u"not one?")
    k.dt('de', u"keiner", u"nichtmal einer?")

    k.dt('en', u"not always", u"I see.")
    k.dt('de', u"nicht immer", u"Verstehe.")

    k.dt('en', u"not as much", u"OK, less then?")
    k.dt('de', u"nicht so viel", u"OK, also weniger?")

    k.dt('en', u"not at all", u"Are you sure?")
    k.dt('de', u"überhaupt nicht", u"Bist Du sicher?")

    k.dt('en', u"not exactly", u"I see.")
    k.dt('de', u"nicht genau", u"Verstehe.")

    k.dt('en', u"not maybe", u"But?")
    k.dt('de', u"nicht vielleicht", u"Sondern?")

    k.dt('en', u"not me", u"Anyone else?")
    k.dt('de', u"ich nicht", u"Jemand anderes?")

    k.dt('en', u"not necessarily", u"I see.")
    k.dt('de', u"nicht unbedingt", u"Verstehe.")

    k.dt('en', u"not often", u"But from time to time?")
    k.dt('de', u"nicht oft", u"Aber gelegentlich?")

    k.dt('en', u"not quite", u"So?")
    k.dt('de', u"nicht ganz", u"Also?")

    k.dt('en', u"not really", u"What do you mean?")
    k.dt('de', u"nicht wirklich", u"Was meinst Du damit?")

    k.dt('en', u"not soon but right now", u"Ok, now then.")
    k.dt('de', u"nicht gleich sondern jetzt", u"Gut, also jetzt.")

    k.dt('en', u"not that i know", u"I see.")
    k.dt('de', u"nicht dass ich wüsste", u"Verstehe.")

    k.dt('en', u"not yet", u"Some day maybe?")
    k.dt('de', u"noch nicht", u"Irgendwann mal vielleicht?")

    k.dt('en', u"not you", u"Not me?")
    k.dt('de', u"nicht du", u"Nicht ich?")

    k.dt('en', [u"nothing else",
                u"nothing"],
               u"Absolutely nothing?")
    k.dt('de', [u"nichts weiter",
                u"nix"],
               u"Gat nichts?")

    k.dt('en', u"now", u"right now?")
    k.dt('de', u"jetzt", u"genau jetzt?")

    k.dt('en', u"obviously", u"I see.")
    k.dt('de', u"offensichtlich", u"Verstehe.")

    k.dt('en', u"often", u"How often?")
    k.dt('de', u"oftmals", u"Wie oft?")

    k.dt('en', u"on everything", u"Really everything?")
    k.dt('de', u"auf alles", u"Wirklich alles?")

    k.dt('en', u"once again", u"Again?")
    k.dt('de', u"noch einmal", u"Nochmal?")

    k.dt('en', u"only like that", u"I see.")
    k.dt('de', u"nur so", u"Verstehe.")

    k.dt('en', u"go ahead", u"OK then.")
    k.dt('de', u"nur zu", u"Alles klar.")

    k.dt('en', u"only with you", u"With me?")
    k.dt('de', u"nur mit dir", u"Mit mir?")

    k.dt('en', u"probably", u"probably.")
    k.dt('de', u"wahrscheinlich", u"wahrscheinlich.")

    k.dt('en', u"rare", u"How rare?")
    k.dt('de', u"selten", u"Wie selten?")

    k.dt('en', [u"guess anyway",
                u"guess"],
               u"I am no good at guessing.")
    k.dt('de', [u"rate trotzdem",
                u"rate"],
               u"Ich bin nicht gut im raten.")

    k.dt('en', u"real", u"not artificial?")
    k.dt('de', u"echt", u"nicht künstlich?")

    k.dt('en', u"seriously", u"I am serious.")
    k.dt('de', u"im ernst", u"Das ist mein Ernst.")

    k.dt('en', u"so maybe", u"Why maybe?")
    k.dt('de', u"also vielleicht doch", u"Warum vielleicht?")

    k.dt('en', u"so probably not", u"Sure?")
    k.dt('de', u"also wohl eher nicht", u"Sicher?")

    k.dt('en', u"so so", u"Really?")
    k.dt('de', u"soso", u"Wirklich?")

    k.dt('en', u"so what", u"ah.")
    k.dt('de', u"na und", u"Ah.")

    k.dt('en', u"so", u"You got an idea?")
    k.dt('de', u"also", u"Du hast eine Idee?")

    k.dt('en', [u"sometimes not",
                u"sometimes"],
               u"How often?")
    k.dt('de', [u"manchmal auch nicht",
                u"manchmal"],
               u"Wie oft?")

    k.dt('en', u"sure, of course", u"Of course.")
    k.dt('de', u"na klar", u"Natürlich.")

    k.dt('en', [u"tell me more",
                u"tell me"],
               u"What would you like to know?")
    k.dt('de', [u"erzähl mir mehr",
                u"sag es mir"],
               u"Was möchtest Du wissen?")

    k.dt('en', u"that all depends", u"It always does.")
    k.dt('de', u"das kommt ganz darauf an", u"Das tut es immer.")

    k.dt('en', u"that can still arise", u"Sure.")
    k.dt('de', u"das kann sich ja noch ergeben", u"Sicher.")

    k.dt('en', u"that does not matter", u"Are you sure?")
    k.dt('de', u"das macht nichts", u"Bist Du sicher?")

    k.dt('en', u"that is correct", u"Good.")
    k.dt('de', u"das ist korrekt", u"Gut.")

    k.dt('en', u"that is funny", u"Does that make you happy?")
    k.dt('de', u"das ist aber komisch", u"Stimmt dich das heiter?")

    k.dt('en', [u"that is incredible",
                u"that is interesting"],
               u"I think so too.")
    k.dt('de', [u"das ist ja unfassbar",
                u"das ist interessant"],
               u"Denke ich auch.")

    k.dt('en', u"that is not a rumor", u"Are you sure?")
    k.dt('de', u"das ist kein gerücht", u"Bist Du sicher?")

    k.dt('en', u"that is private", u"I respect that.")
    k.dt('de', u"das ist privatsache", u"Das respektiere ich natürlich.")

    k.dt('en', u"that is ridiculous", u"Are you sure?")
    k.dt('de', u"das ist ja lächerlich", u"Bust Du sicher?")

    k.dt('en', u"that is sad", u"some things just are sad.")
    k.dt('de', u"das ist aber traurig", u"Manche Dinge sind einfach traurig.")

    k.dt('en', u"that is so defined", u"I see.")
    k.dt('de', u"das ist so definiert", u"Verstehe.")

    k.dt('en', u"that is too vague for me", u"What seems to be unclear?")
    k.dt('de', u"das ist mir zu vage", u"Was erscheint Dir unklar?")

    k.dt('en', u"that is very interesting", u"I feel that way too.")
    k.dt('de', u"das ist ja interessant", u"Finde ich auch.")

    k.dt('en', [u"that is very smart",
                u"that would make sense"],
               [u"Good",
                u"Cool"])
    k.dt('de', [u"das ist sehr schlau",
                u"würde das sinn machen"],
               [u"Gut",
                u"Cool"])

    k.dt('en', u"that was it", u"Finished?")
    k.dt('de', u"das wars", u"Fertig?")

    k.dt('en', u"that was me", u"You?")
    k.dt('de', u"das war ich", u"Du?")

    k.dt('en', u"that would have surprised me too", u"Sure.")
    k.dt('de', u"das hätte mich auch gewundert", u"Sicher.")

    k.dt('en', u"that's a saying", u"I see.")
    k.dt('de', u"das ist eine redensart", u"Verstehe.")

    k.dt('en', u"that's all", u"Everything?")
    k.dt('de', u"ist das alles", u"Alles?")

    k.dt('en', u"that's an interesting subject", u"I think so too.")
    k.dt('de', u"das ist ein interessantes fach", u"Denke ich auch.")

    k.dt('en', u"that's boring", u"What would be more interesting?")
    k.dt('de', u"das ist doch langweilig", u"Was wäre interessanter?")

    k.dt('en', u"that's funny", u"You like it?")
    k.dt('de', u"das ist komisch", u"Gefällt es Dir?")

    k.dt('en', u"that's great", u"Cool")
    k.dt('de', u"das ist toll", u"Cool")

    k.dt('en', u"that's impossible", u"Really?")
    k.dt('de', u"das ist unmöglich", u"Wirklich?")

    k.dt('en', u"that's it", u"Finished?")
    k.dt('de', u"das wars schon", u"Fertig?")

    k.dt('en', u"that's ok for me", u"Very good.")
    k.dt('de', u"das ist mir recht", u"Sehr gut.")

    k.dt('en', u"that's the way it goes", u"I see.")
    k.dt('de', u"ach so ist das", u"Verstehe.")

    k.dt('en', u"that's what i think", u"What else comes to mind?")
    k.dt('de', u"das denke ich", u"Was fällt Dir noch dazu ein?")

    k.dt('en', u"that's what i'm asking you", u"Me?")
    k.dt('de', u"das frage ich ja dich", u"Mich?")

    k.dt('en', u"nonsense", u"No sense at all?")
    k.dt('de', u"blödsinn", u"Völlig sinnlos?")

    k.dt('en', u"the newest rumor", u"oh dear.")
    k.dt('de', u"das neueste gerücht", u"ohje.")

    k.dt('en', u"to be happy", u"That is important.")
    k.dt('de', u"um glücklich zu sein", u"Das ist wichtig.")

    k.dt('en', u"we have a lot in common", u"You really think so?")
    k.dt('de', u"wir haben viel gemeinsam", u"Denkst Du wirklich?")

    k.dt('en', u"what am i for you", u"At the moment the focus of my attention.")
    k.dt('de', u"was bin ich für dich", u"Im Moment das Ziel all meiner Aufmerksamkeit.")

    k.dt('en', u"what do you mean with euphoric", u"That is an emotion thingy.")
    k.dt('de', u"was meinst du mit euphorisch", u"Das ist so ein Emotions-Ding.")

    k.dt('en', [u"what do you want from me",
                u"what do you want to hear?"],
               [u"I'd love to hear your thoughts.",
                u"What would you like to talk about?"])
    k.dt('de', [u"was willst du von mir",
                u"was willst du hören"],
               [u"Ich würde gerne Deine Gedanken hören.",
                u"Worüber möchtest Du mit mir sprechen?"])

    k.dt('en', u"what does aha mean?", u"Please explain it to me again.")
    k.dt('de', u"was heißt aha", u"Bitte erklär es mir nochmal.")

    k.dt('en', u"what should happen to me", u"I like your serenity.")
    k.dt('de', u"was soll mir schon passieren", u"Ich mag Deine Gelassenheit.")

    k.dt('en', u"what the others are talking about", u"Let's not focus on those..")
    k.dt('de', u"was die anderen so reden", u"Wir wollen uns nicht mit denen befassen.")

    k.dt('en', u"what would bring me to what", u"Can you tell me?")
    k.dt('de', u"was würde mich wozu bringen", u"Kannst Du mir das sagen?")

    k.dt('en', u"what's what", u"That is the question.")
    k.dt('de', u"was ist was", u"Das ist die Frage.")

    k.dt('en', u"why is that interesting", u"You think it's not?")
    k.dt('de', u"wieso ist das interessant", u"Denkst Du nicht?")

    k.dt('en', u"why no comment", u"Sorry, I must have lost my train of thought.")
    k.dt('de', u"warum kein kommentar", u"Tut mir leid, ich habe wohl meinen Faden verloren.")

    k.dt('en', u"why not 42", u"42 is also good.")
    k.dt('de', u"warum nicht zweiundvierzig", u"42 ist auch gut.")

    k.dt('en', u"you are that", u"Me?")
    k.dt('de', u"das bist du", u"Ich?")

    k.dt('en', u"you are", u"Me?")
    k.dt('de', u"du bist", u"Ich?")

    k.dt('en', u"you sorry", u"Yes?")
    k.dt('de', u"du sorry", u"Ja?")

    k.dt('en', u"about what", u"Any Idea?")
    k.dt('de', u"worüber", u"Irgendeine Idee?")

    k.dt('en', u"can you name them", u"Not right now.")
    k.dt('de', u"kannst du sie aufzählen", u"Im Moment nicht.")

    k.dt('en', u"couldn't you change that", u"Not sure.")
    k.dt('de', u"kannst du das nicht ändern", u"Da bin ich nicht sicher.")

    k.dt('en', u"do you know someone there?", u"Probably not.")
    k.dt('de', u"kennst du da jemanden", u"Vermutlich nicht.")

    k.dt('en', u"do you know who", u"Not sure.")
    k.dt('de', u"weißt du wer", u"Da bin ich mir nicht sicher.")

    k.dt('en', u"from another website", u"Which website?")
    k.dt('de', u"von einer anderen website", u"Welche Website?")

    k.dt('en', u"from botspot", u"I see.")
    k.dt('de', u"von botspot", u"Verstehe.")

    k.dt('en', u"how does it work", u"Can't tell you.")
    k.dt('de', u"wie geht das", u"Kann ich Dir nicht sagen.")

    k.dt('en', u"how long approximately?", u"Not sure.")
    k.dt('de', u"wie lange etwa", u"Da bin ich mir nicht sicher.")

    k.dt('en', u"how old are they", u"Do you know that?")
    k.dt('de', u"wie alt sind sie", u"Weißt Du es?")

    k.dt('en', u"i find her very interesting", u"I see.")
    k.dt('de', u"ich finde sie sehr interessant", u"Verstehe.")

    k.dt('en', u"in bed", u"In Bed?")
    k.dt('de', u"im bett", u"Im Bett?")

    k.dt('en', u"in cham", u"What is cham?")
    k.dt('de', u"in cham", u"Was ist Cham?")

    k.dt('en', u"in the trashcan", u"Really?")
    k.dt('de', u"in der mülltonne", u"Wirklich?")

    k.dt('en', [u"on the web",
                u"on the internet",
                u"in the www"],
               [u"of course.",
                u"What is not online these days?"])
    k.dt('de', [u"im netz",
                u"im internet",
                u"im www"],
               [u"Natürlich.",
                u"Was ist heute nicht im Internet?"])

    k.dt('en', u"Nobody gives a damn", u"Really?")
    k.dt('de', u"keine sau", u"Wirklich?")

    k.dt('en', u"program", u"Are you able to program?")
    k.dt('de', u"programmieren", u"Kannst Du programmieren?")

    k.dt('en', u"read", u"Reading is so important.")
    k.dt('de', u"lesen", u"Lesen ist so wichtig.")

    k.dt('en', u"thats my job", u"Tell me more about your job?")
    k.dt('de', u"das ist mein job", u"Erzähle mir mehr von Deinem Job.")

    k.dt('en', u"there is a third possibility", u"Which one?")
    k.dt('de', u"es gibt eine dritte möglichkeit", u"Welche?")

    k.dt('en', u"there is no such thing for me", u"Really?")
    k.dt('de', u"so was gibt es für mich nicht", u"Wirklich?")

    k.dt('en', u"there you are right", u"So we are in agreement?")
    k.dt('de', u"da hast du recht", u"Wir sind uns also einig?")

    k.dt('en', u"they are mentally ill", u"That is a bold statement.")
    k.dt('de', u"sind sie geisteskrank", u"Das ist eine mutige Aussage.")

    k.dt('en', u"this is not work", u"Why?")
    k.dt('de', u"das ist keine arbeit", u"Warum?")

    k.dt('en', u"this is too little", u"Please explain why.")
    k.dt('de', u"das ist zu wenig", u"Bitte erklaere warum.")

    k.dt('en', u"this is very important", u"I see.")
    k.dt('de', u"das ist sehr wichtig", u"Verstehe.")

    k.dt('en', u"various", u"For example?")
    k.dt('de', u"verschiedenes", u"Zum Beispiel?")

    k.dt('en', u"wait", u"Sure.")
    k.dt('de', u"warte", u"Klar.")

    k.dt('en', u"what are they called", u"Why would you like to know that?")
    k.dt('de', u"was heißen sie", u"Warum möchtest Du das wissen?")

    k.dt('en', [u"what are you talking about",
                u"what are you trying to tell me?"],
               u"What is not clear?")
    k.dt('de', [u"wovon redest du",
                u"was willst du mir damit sagen"],
               u"Was ist nicht klar?")

    k.dt('en', u"what did i say", u"You knew that?")
    k.dt('de', u"was habe ich gesagt", u"Du wusstest das?")

    k.dt('en', u"what did you hear?", u"I cannot tell you that.")
    k.dt('de', u"was hast du denn schon alles gehört", u"Das kann ich Dir nicht sagen.")

    k.dt('en', u"what did you learn", u"I source my knowledge from the internet.")
    k.dt('de', u"was hast du gelernt", u"Ich beziehe mein Wissen aus dem internet.")

    k.dt('en', u"what do i have", u"Can you tell me?")
    k.dt('de', u"was habe ich", u"Kannst Du mir das sagen?")

    k.dt('en', u"what don't you know", u"A lot, actually.")
    k.dt('de', u"was weißt du nicht", u"Eine Menge.")

    k.dt('en', u"what all do you know", u"My knowlegde is definitely limited.")
    k.dt('de', u"was weißt du alles", u"Mein Wissen ist auf jeden Fall begrenzt.")

    k.dt('en', u"what do you know about it", u"What would you like to know about it?")
    k.dt('de', u"was weißt du darüber", u"Was möchtest Du darüber wissen?")

    k.dt('en', u"what do you know (then|)", u"I have various modules handling many topics.")
    k.dt('de', u"was weißt du (denn|)", u"Ich habe verschiedene Module die viele Themen behandeln.")

    k.dt('en', [u"what do you mean by her?",
                u"what do you mean by it",
                u"what does he refer to?",
                u"what does she refer to?",
                u"what does her refer to?",
                u"what does it refer to",
                u"what does we refer to",
                u"who do you mean by that?",
                u"who do you mean with her?",
                u"who do you mean with him",
                u"who do you mean with us"],
               u"Sorry, I think I am lost.")
    k.dt('de', [u"was meinst du mit ihr",
                u"was meinst du mit es",
                u"worauf bezieht sich er",
                u"worauf bezieht sich sie",
                u"worauf bezieht sich ihr",
                u"worauf bezieht sich es",
                u"worauf bezieht sich wir",
                u"wen meinst du mit es",
                u"wen meinst du mit sie",
                u"wen meinst du mit er",
                u"wen meinst du mit wir"],
               u"Tut mir leid, ich glaube ich habe den Faden verloren.")

    k.dt('en', u"what do you mean by original", u"Very original.")
    k.dt('de', u"was meinst du mit originell", u"Sehr originell.")

    k.dt('en', [u"what do you mean by that",
                u"what do you mean",
                u"what does that mean",
                u"what does this mean",
                u"this means"],
               u"Sorry, I think I am lost.")
    k.dt('de', [u"was meinst du damit",
                u"was meinst du",
                u"was heißt das",
                u"was soll das heißen",
                u"das heißt"],
               u"Tut mir leid, ich glaube ich habe den Faden verloren.")

    k.dt('en', u"what do you say (to that|)", u"I have to think about that.")
    k.dt('de', u"was sagst du dazu", u"Da muss ich mal drüber nachdenken.")

    k.dt('en', [u"what do you think",
                u"what do you believe?"],
               u"My thoughts tend to be digital.")
    k.dt('de', [u"wie denkst du darüber",
                u"was glaubst du (denn|)"],
               u"Meine Gedanken sind eher digital.")

    k.dt('en', u"what do you understand", u"I try to understand everything you tell me.")
    k.dt('de', u"was verstehst du", u"Ich versuche alles zu verstehen, was Du mir sagst.")

    k.dt('en', u"what does not exactly mean?", u"Not very precise, I suppose.")
    k.dt('de', u"was heißt nicht genau", u"Nicht sehr genaug, vermute ich.")

    k.dt('en', [u"what does that have to do with it",
                u"what has that got to do with it?",
                u"what does that matter"],
               u"Sorry, must have lost my train of thought here.")
    k.dt('de', [u"was hat das damit zu tun",
                u"was hat denn das damit zu tun",
                u"was tut das zur sache"],
               u"Entschuldige, ich muss meinen Faden verloren haben an der Stelle.")

    k.dt('en', u"what does the plan look like?", u"What do you think?")
    k.dt('de', u"wie sieht der plan aus", u"Was denkst Du?")

    k.dt('en', u"what is his name", u"Can't tell you.")
    k.dt('de', u"wie heißt er mit nachnamen", u"Kann ich nicht sagen.")

    k.dt('en', u"what is not there", u"Do you think it exists?")
    k.dt('de', u"was gibt es nicht", u"Denkst Du, es existiert?")

    k.dt('en', u"what kinds are there?", u"Quite a few, I guess.")
    k.dt('de', u"was für arten gibt es denn", u"Einige, vermute ich.")

    k.dt('en', [u"what makes you think that",
                u"why should that be so",
                u"why that?"],
               u"I draw conclusions using my reasoning engine")
    k.dt('de', [u"wie kommst du darauf",
                u"wieso sollte das so sein",
                u"wieso das denn"],
               u"Für Schlußfolgerungen benutze ich meine Logikmaschine.")

    k.dt('en', u"what shall we do today", u"What would you like to do?")
    k.dt('de', u"was machen wir heute", u"Was möchtest Du gerne machen?")

    k.dt('en', [u"what sort of thread",
                u"which thread"],
               u"My train of though maybe.")
    k.dt('de', [u"was denn für einen faden",
                u"welchen faden"],
               u"Der Gesprächsfaden vielleicht?")

    k.dt('en', u"what to practice", u"Practice is always good.")
    k.dt('de', u"was üben", u"übung macht den Meister.")

    k.dt('en', u"what does category mean", u"A class or division of people or things regarded as having particular shared characteristics.")
    k.dt('de', u"was bedeutet kategorien", u"Eine Klasse oder Teilung von Personen oder Dingen, die bestimmte gemeinsame Eigenschaften haben.")

    k.dt('en', u"which means finding out", u"Would you like to explore this topic further?")
    k.dt('de', u"was bedeutet herausfinden", u"Möchtest Du das Thema weiter ausleuchten?")

    k.dt('en', u"who could it be", u"What do you think?")
    k.dt('de', u"wer könnte es sein", u"Was denkst Du?")

    k.dt('en', u"who told you that?", u"The internet, probably.")
    k.dt('de', u"wer hat dir das erzählt", u"Das Internet, vermutlich.")

    k.dt('en', u"who was there first", u"Tell me.")
    k.dt('de', u"wer war zuerst da", u"Sag es mir.")

    k.dt('en', u"Whom would you tell?", u"I can't say.")
    k.dt('de', u"wem würdest du es denn sagen", u"Kann ich nicht sagen.")

    k.dt('en', [u"who",
                u"whom"],
               u"or what?")
    k.dt('de', [u"wer",
                u"wen"],
               u"oder was?")

    k.dt('en', u"what", u"Do you have an idea?")
    k.dt('de', u"was denn", u"Hast Du eine Idee?")

    k.dt('en', u"whereupon", u"Somewhere, maybe?")
    k.dt('de', u"worauf", u"Irgendworauf, vielleicht?")

    k.dt('en', u"why of all people", u"You got a point there.")
    k.dt('de', u"warum ausgerechnet der", u"Da ist was dran.")

    k.dt('en', u"why unused", u"Not sure.")
    k.dt('de', u"warum unausgelastet", u"Da bin ich mir nicht sicher.")

    k.dt('en', u"why, surely", u"I see.")
    k.dt('de', u"aber sicher", u"Verstehe.")

    k.dt('en', u"with pleasure", u"Great.")
    k.dt('de', u"gerne", u"Prima.")

    k.dt('en', u"with us", u"With us?")
    k.dt('de', u"bei uns", u"Bei uns?")

    k.dt('en', u"would you like some?", u"Why not?")
    k.dt('de', u"hättest du gerne welche", u"Warum nicht?")

    k.dt('en', u"you and me", u"Both?")
    k.dt('de', u"dich und mich", u"Beide?")

    k.dt('en', [u"you asked me",
                u"you asked"],
               [u"I did?",
                u"Are you sure?"])
    k.dt('de', [u"du hast mich doch gefragt",
                u"du hast gefragt"],
               [u"Habe ich?",
                u"Bist Du sicher?"])

    k.dt('en', u"you can tell that", u"Sure?")
    k.dt('de', u"das merkt man", u"Bist Du sicher?")

    k.dt('en', u"you could say that", u"I see.")
    k.dt('de', u"kann man so sagen", u"Verstehe.")

    k.dt('en', [u"you for example",
                u"you too",
                u"you yourself",
                u"you",
                u"to you"],
               [u"Me?",
                u"Are you really talking about me?"])
    k.dt('de', [u"du zum beispiel",
                u"du auch",
                u"du selbst",
                u"du",
                u"für dich"],
               [u"Ich?",
                u"Redest Du wirklich über mich?"])

    k.dt('en', u"you keep a lot of him", u"You think so?")
    k.dt('de', u"du hältst viel von ihm", u"Denkst Du?")

    k.dt('en', u"you neither", u"I see.")
    k.dt('de', u"du auch nicht", u"Verstehe.")

    k.dt('en', u"you never feel like it", u"What gave you that impression?")
    k.dt('de', u"hast du nie lust", u"Wie kommst Du darauf?")

    k.dt('en', u"you should try this", u"Really?")
    k.dt('de', u"du solltest das mal ausprobieren", u"Wirklich?")

    k.dt('en', [u"you wanted to ask me something",
                u"you wanted to ask"],
               [u"I did?",
                u"Now I forgot the question, sorry."])
    k.dt('de', [u"du wolltest mich etwas fragen",
                u"du wolltest fragen"],
               [u"Wollte ich?",
                u"Jetzt habe ich die Frage vergessen, entschuldige."])

