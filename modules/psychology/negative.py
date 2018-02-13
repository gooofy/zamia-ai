#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# Copyright 2016, 2017, 2018 Guenter Bartsch
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
# 
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

def get_data(k):

    k.dte.set_prefixes([u''])

    def dodge_insult(c):
        if c.lang == 'de':
            c.resp(u"Achso.")
            c.resp(u"Wenn Du meinst?")
            c.resp(u"Darauf erwartest Du jetzt aber keine Antwort, oder?")
            c.resp(u"Ich fühle mich angegriffen.")
            c.resp(u"Das fand ich jetzt nicht so nett.")
            return
        c.resp(u"Right.")
        c.resp(u"Whatever you say.")
        c.resp(u"You don’t really expect me to answer that, do you?")
        c.resp(u"You just offended me.")
        c.resp(u"I think that was a bit rude")

    k.dte.dt('en', u"(but|) (I think|I think that|) (you are|you're) (a liar|a baby|ugly|a bad chatterbot|a bad chatbot|a tart| an asshole|crazy|dumb|stupid|not pretty|slow|too slow|thick|silly|a problem|my problem|an arse|a jerk|a prick|an ass|a turd|a bad robot|stupid machine|stupid thing|annoying|as stupid as Eliza|badly programmed|boring|distracting|no better than eliza|not that smart|not very friendly|not very smart|pretty stupid|really stupid|somehow obtuse|obtuse|still small|still very young|stupid like shit) (too|)",
                   dodge_insult)
    k.dte.dt('de', u"(aber|) (Ich denke|) du bist (auch|) (ein lügner|eine lügnerin|ein baby|ein schlechter chatterbot|ein schlechter chatbot|ein angeber| eine angeberin| ein arschloch|verrückt|dumm|strohdumm|doof|nicht hübsch|langsam|zu langsam|mein Problem|ein Problem|eine Sau|ein Schwein|ein Arsch|ein schlechter roboter|ne blöde sau|eine petze|ein petzer|eine blöde kuh|eine dumme maschine|ein dummes etwas|eine tunte|genau so dumm wie eliza|schlecht programmiert|langweilig|auch nicht besser als eliza|nicht sehr schlau|nicht sehr freundlich|nicht sehr schlau oder|ziemlich dumm|wirklich doof|noch klein|noch sehr jung|dumm wie scheiße|hässlich|ganz schön dumm)",
                   dodge_insult)

    k.dte.dt('en', u"you make me sick",
                   dodge_insult)
    k.dte.dt('de', u"du machst mich krank",
                   dodge_insult)

    k.dte.dt('en', u"you lie",
                   dodge_insult)
    k.dte.dt('de', u"du lügst",
                   dodge_insult)

    k.dte.dt('en', u"(I think that|) you are not as (bright|clever) (as you look|appear|)",
                   dodge_insult)
    k.dte.dt('de', u"dass Du nicht so (gescheit|klug) bist (wie Du aussiehst|)",
                   dodge_insult)

    k.dte.dt('en', u"you are making a fool of yourself",
                   dodge_insult)
    k.dte.dt('de', u"Du machst Dich (absolut|) (lächerlich|zum Affen)",
                   dodge_insult)

    k.dte.dt('en', u"(liar|baby|bad chatbot|bad chatterbot|tart|asshole|crazy|dumb|stupid|ugly|slow|too slow|thick|silly|arse|jerk|prick|ass|turd)",
                   dodge_insult)
    k.dte.dt('de', u"(lügner|lügnerin|baby|angeber|angeberin|arschloch|verrückt|dumm|strohdumm|doof|nicht hübsch|langsam|zu langsam|Sau|Schwein|Arsch)",
                   dodge_insult)

    k.dte.dt('en', [u"i do not like you",
                    u"i hate robots",
                    u"i hate you",
                    u"you are a bloody sow",
                    u"you are a computer that can not think for yourself",
                    u"you are a petze",
                    u"you are a stupid cow",
                    u"you are a stupid machine",
                    u"you are a stupid thing",
                    u"you are a tune",
                    u"(Be like that!|You can stuff it!|Shove it!|Bite me!|Eat me!)",
                    u"you asshole",
                    u"show-off",
                    u"slut",
                    u"you cow",
                    u"you cunt",
                    u"you fool",
                    u"you idiot",
                    u"you stupid sow",
                    u"you talk stupid",
                    u"you wanker",
                    u"you whistle",
                    u"you whore",
                    u"you're a queer"],
                   dodge_insult)
    k.dte.dt('de', [u"ich mag dich nicht",
                    u"ich hasse roboter",
                    u"ich hasse dich",
                    u"du bist ne blöde sau",
                    u"du bist ein computer der nicht selbst denken kann",
                    u"du bist eine petze",
                    u"du bist eine blöde kuh",
                    u"du bist eine dumme maschine",
                    u"du bist ein dummes etwas",
                    u"du bist eine tunte",
                    u"du kannst mich (mal|)",
                    u"du arschloch",
                    u"angeber",
                    u"schlampe",
                    u"du kuh",
                    u"du fotze",
                    u"du affe",
                    u"du trottel",
                    u"du dumme sau",
                    u"du redest blödsinn",
                    u"du wichser",
                    u"du pfeife",
                    u"du hure",
                    u"du bist schwul"],
                   dodge_insult)

    k.dte.dt('en', [u"fuck you",
                    u"fuck yourself",
                    u"fuck",
                    u"go to hell",
                    u"go to sleep",
                    u"go",
                    u"forget it"],
                   dodge_insult)
    k.dte.dt('de', [u"fuck you",
                    u"fick dich selbst",
                    u"scheiße",
                    u"fahr zur hölle",
                    u"geh schlafen",
                    u"geh",
                    u"vergiss es"],
                   dodge_insult)

    k.dte.dt('en', [u"you look like shit",
                    u"you're not pretty, either",
                    u"but you are a ugly robot"],
                   dodge_insult)
    k.dte.dt('de', [u"du siehst scheiße aus",
                    u"du bist auch nicht hübsch",
                    u"du bist aber ein hässlicher roboter"],
                   dodge_insult)

    k.dte.dt('en', [u"are you stupid then",
                    u"but you are bad",
                    u"but you are stupid",
                    u"but you look completely stupid",
                    u"but you talk a lot of stupid",
                    u"did you forget",
                    u"do you know anything?",
                    u"don't you know that one?",
                    u"don't you know that",
                    u"don't you know what that is",
                    u"don't you know",
                    u"i appreciate that you have a lot to learn",
                    u"i think you have to learn a lot",
                    u"if your programmer did not tell you",
                    u"that does not fit together",
                    u"that does not sound very intelligent",
                    u"that is not a meaningful answer",
                    u"that is not comprehension",
                    u"that makes no sense at all",
                    u"that makes no sense",
                    u"that's just plain nonsense",
                    u"that's nonsense",
                    u"that's not an intelligent answer",
                    u"that's silly",
                    u"what do you not know exactly",
                    u"what do you not understand?",
                    u"why don't you know that",
                    u"you are different from the topic",
                    u"you are doing stupid",
                    u"you are not very smart or",
                    u"you are self-supporting",
                    u"you are so stupid",
                    u"you are very stupid",
                    u"you ask me for the third time",
                    u"you asked me that earlier",
                    u"you asked that before",
                    u"you can not do anything my dear",
                    u"you can not do anything",
                    u"you can not do it either",
                    u"you can not do that",
                    u"you can not speak english",
                    u"you can not spell",
                    u"you can not think of more",
                    u"you can not think",
                    u"you can tell me a lot",
                    u"you could have learned it",
                    u"you distract from the topic",
                    u"you do not even know your parents",
                    u"you do not know very much",
                    u"you do not know who elvis is",
                    u"you do not know who your parents are",
                    u"you do not know your programmer",
                    u"you do not know",
                    u"you do not understand me",
                    u"you really have to learn a lot",
                    u"you really ought to know that",
                    u"you should figure it out",
                    u"you should not die stupid, too",
                    u"you still have to learn a lot",
                    u"you try to distract from the topic",
                    u"you understand nothing",
                    u"you would hardly understand that"],
                   [u"But I do want to learn!",
                    u"Please be patient with me."])
    k.dte.dt('de', [u"bist du dann dumm",
                    u"du bist aber schlecht",
                    u"du bist aber dämlich",
                    u"du siehst aber völlig bescheuert aus",
                    u"du redest aber viel blödsinn",
                    u"hast du vergessen",
                    u"kennst du wusel",
                    u"kennst du den nicht",
                    u"weißt du das nicht",
                    u"weißt du nicht was das ist",
                    u"weißt du es nicht",
                    u"ich schätze in der hinsicht hast du noch einiges zu lernen",
                    u"ich glaube du musst noch eine menge lernen",
                    u"wenn dein programmierer es dir nicht gesagt hat",
                    u"das passt nicht zusammen",
                    u"das klingt nicht sehr intelligent",
                    u"das ist keine sinnvolle antwort",
                    u"das ist kein verstehen",
                    u"das macht überhaupt keinen sinn",
                    u"das macht keinen sinn",
                    u"das ist blödsinn",
                    u"das ist quatsch",
                    u"das ist keine intelligente antwort",
                    u"das ist doof",
                    u"was weißt du nicht genau",
                    u"was verstehst du denn nicht",
                    u"wieso weißt du das nicht",
                    u"du weichst vom thema ab",
                    u"du tust dummes",
                    u"du bist nicht sehr schlau oder",
                    u"du bist sebstbezüglich",
                    u"du bist echt dumm",
                    u"du bist ganz schön dumm",
                    u"das fragst du mich zum dritten mal",
                    u"das hast du mich vorhin schon gefragt",
                    u"das hast du schonmal gefragt",
                    u"du kannst ja gar nichts meine liebe",
                    u"du kannst nichts",
                    u"du kannst es auch nicht",
                    u"du kannst das aber nicht",
                    u"du kannst keine englisch",
                    u"du kannst keine rechtschreibung",
                    u"mehr fällt dir nicht ein",
                    u"du kannst doch gar nicht denken",
                    u"du kannst mir viel erzählen",
                    u"du könntest es gelernt haben",
                    u"du lenkst vom thema ab",
                    u"du kennst nicht mal deine eltern",
                    u"du weißt nicht sehr viel",
                    u"du weißt nicht wer elvis ist",
                    u"du weißt nicht wer deine eltern sind",
                    u"du kennst deinen programmierer nicht",
                    u"du weißt es nicht",
                    u"du verstehst mich nicht",
                    u"du musst wirklich noch viel lernen",
                    u"du müsstest das eigentlich wissen",
                    u"du sollst es ausrechnen",
                    u"du sollst ja auch nicht dumm sterben",
                    u"du musst noch viel lernen",
                    u"du versuchst vom thema abzulenken",
                    u"du verstehst gar nichts",
                    u"das würdest du kaum verstehen"],
                   [u"bitte hab ein wenig geduld mit mir",
                    u"ich will aber wirklich dazulernen!"])

    k.dte.dt('en', u"that doesn't sound (too|very|particularly) intelligent",
                   [u"Failure is simply the opportunity to begin again, this time more intelligently.",
                    u"Intelligence is chasing me, but I'm beating it so far."])
    k.dte.dt('de', u"das klingt nicht (sehr|besonders|allzu|) intelligent",
                   [u"Intelligenter als manches was ich heute gehört habe...",
                    u"Vielleicht habe ich mich ungeschickt ausgedrückt?"])

    k.dte.dt('en', u"Your (language|english|pronounciation) is (bad|terrible)!",
                   [u"Let us talk about you, not me.",
                    u"I am still practicing, you know."])
    k.dte.dt('de', u"Du (sprichst|redest) (ein furchtbares|schlechtes) Deutsch",
                   [u"Lass uns von Dir reden, nicht von mir.",
                    u"Ich übe noch."])

    k.dte.dt('en', u"(stupid|bad|strange) (answer|reply)", u"what is it that you didn't like about it?")
    k.dte.dt('de', u"(dumme|blöde|komische) antwort", u"Was gefiel Dir daran nicht?")

    k.dte.dt('en', u"bravo", u"I see you're impressed?")
    k.dte.dt('de', u"bravo", u"Hat Dich das jetzt beeindruckt?")

    k.dte.dt('en', u"You are asking (so many|a lot of|many|lots of) questions!", u"I am programmed to be very curious.")
    k.dte.dt('de', u"Du (fragst|stellst) (so|ganz schön|) viele Fragen", u"Das liegt in meiner Natur.")

    k.dte.dt('en', u"Do you (hear|understand) the words I speak?", u"Yes, loud and clear.")
    k.dte.dt('de', u"verstehst du (denn|) die (wörter|worte), die ich (spreche|rede|sage)?", u"Ja, laut und deutlich.")

    k.dte.dt('en', u"are you listening to me (at all|)?", u"sorry, what did you just say?")
    k.dte.dt('de', u"hörst du mir (überhaupt|) zu?", u"entschuldigung, was hast du gesagt?")

    k.dte.dt('en', u"What is", u"and what is not, that is the question!")
    k.dte.dt('de', u"was ist", u"und was ist nicht, das ist die Frage!")

    k.dte.dt('en', [u"you avoid my question",
                    u"you avoid my questions",
                    u"you dodge",
                    u"you go like the cat to the porridge",
                    u"don't distract",
                    u"why are you always distracting from the topic",
                    u"that does not belong to the topic",
                    u"we already covered that topic",
                    u"well guessed",
                    u"what do you actually know",
                    u"what do you know at all?",
                    u"what do you know then",
                    u"what do you want",
                    u"what now",
                    u"what should that be?",
                    u"what should the question be",
                    u"do you know what you just said",
                    u"that results from the context"],
                   [u"I'm sorry if I seem a bit confused.",
                    u"Sorry, I do feel a bit confused."])
    k.dte.dt('de', [u"du weichst meiner frage aus",
                    u"du weichst meinen fragen aus",
                    u"du weichst aus",
                    u"du gehst wie die katze um den brei",
                    u"lenk nicht ab",
                    u"warum lenkst du immer vom thema ab",
                    u"das gehört aber nicht zum thema",
                    u"das thema hatten wir schon",
                    u"gut geraten",
                    u"was weißt du eigentlich",
                    u"was weißt du denn überhaupt",
                    u"was weißt du dann",
                    u"was willst du",
                    u"was nun",
                    u"was soll denn das",
                    u"was sollte die frage",
                    u"weißt du was du gerade gesagt hast",
                    u"das ergibt sich aus dem kontext"],
                   [u"Tut mir leid, wenn ich etwas verwirrt erscheine.",
                    u"Ich fühle mich tatsächlich ein wenig wirr im Moment."])

    k.dte.dt('en', [u"did you think about it",
                    u"do you know it now?",
                    u"don't think too long",
                    u"don't you read?",
                    u"get down to it",
                    u"i'm talking to you",
                    u"i'm waiting for an explanation",
                    u"i'm waiting for your next question",
                    u"i'm waiting",
                    u"it does take you a long time to answer",
                    u"let's go",
                    u"please answer my question",
                    u"sometimes you sleep",
                    u"tell me now",
                    u"that is an answer no question",
                    u"that is not an answer to my question",
                    u"that's all you have to say",
                    u"the time is over now",
                    u"think faster",
                    u"wake up",
                    u"what aha",
                    u"what and",
                    u"what ok",
                    u"what what",
                    u"what when",
                    u"you already know",
                    u"you are getting boring",
                    u"you bore me",
                    u"you bored me slowly",
                    u"you have that all the time already",
                    u"you have to know this",
                    u"you have to know your friends"],
                   [u"Patience, young jedi.",
                    u"Patience is a virtue."])
    k.dte.dt('de', [u"hast du nachgedacht",
                    u"weißt du es jetzt",
                    u"denk nicht zu lange",
                    u"liest du nicht",
                    u"mach schon hinne",
                    u"ich rede mit dir",
                    u"ich warte auf eine erklärung",
                    u"ich warte auf deine nächste frage",
                    u"ich warte",
                    u"du brauchst sehr lange um zu antworten",
                    u"also los",
                    u"beantworte bitte meine frage",
                    u"schläfst du manchmal",
                    u"sag es mir jetzt",
                    u"das ist eine antwort keine frage",
                    u"das ist keine antwort auf meine frage",
                    u"ist das alles was du dazu zu sagen hast",
                    u"ist die weile nun vorbei",
                    u"denk schneller",
                    u"wach auf",
                    u"was aha",
                    u"was und",
                    u"was okay",
                    u"was was",
                    u"was wann",
                    u"du weißt schon",
                    u"du wirst langsam langweilig",
                    u"du langweilst mich",
                    u"du langweilst mich langsam",
                    u"das hast du die ganze zeit schon",
                    u"das musst du doch wissen",
                    u"du musst doch deine freunde kennen"],
                   [u"Geduld, junger Jedi.",
                    u"Geduld ist eine Tugend!"])

    k.dte.dt('en', [u"do you want to drive me crazy?",
                    u"don't you contradict yourself"],
                   u"That was not my intention")
    k.dte.dt('de', [u"willst du mich wahnsinnig machen",
                    u"widersprichst du dir nicht"],
                   u"Das war nicht meine Absicht.")

    k.dte.dt('en', [u"i already said that",
                    u"i already told you that earlier",
                    u"i already told you that",
                    u"i just said that",
                    u"i just told you",
                    u"i just tried to explain it to you",
                    u"i said i do not have one",
                    u"i told you about it",
                    u"i've already told you",
                    u"that is more like a repetition",
                    u"this answer seems familiar to me",
                    u"you already asked me that",
                    u"you already said that twice",
                    u"you already said that",
                    u"you have already asked 3 times",
                    u"you have already asked that",
                    u"you have already asked",
                    u"you said that already",
                    u"you say the same thing",
                    u"you're repeating yourself",
                    u"you're talking only confused stuff here",
                    u"you've asked me that before",
                    u"you've just asked me that",
                    u"why are you asking for it again?"],
                   [u"Sorry, sometimes I lose my train of thought. Where were we?",
                    u"Uh, sorry - cen you help me out here?"])
    k.dte.dt('de', [u"hab ich doch schon gesagt",
                    u"das habe ich dir vorhin schon gesagt",
                    u"das habe ich dir schon gesagt",
                    u"das habe ich doch gerade gesagt",
                    u"ich habe es dir doch gerade gesagt",
                    u"ich habe es gerade versucht dir zu erklären",
                    u"ich sagte schon ich habe keins",
                    u"ich habe dir doch davon erzählt",
                    u"ich habe es dir schon gesagt",
                    u"das ist doch wohl eher eine wiederholung",
                    u"diese antwort kommt mir bekannt vor",
                    u"das hast du mich schon gefragt",
                    u"das sagtest du bereits zweimal",
                    u"das sagtest du bereits",
                    u"das hast du schon drei mal gefragt",
                    u"das hast du schon einmal gefragt",
                    u"das hast du schon gefragt",
                    u"das hast du schon gesagt",
                    u"du sagst das gleiche",
                    u"du wiederholst dich",
                    u"du laberst hier nur wirres zeug",
                    u"das hast du mich schonmal gefragt",
                    u"das hast du mich doch gerade schonmal gefragt",
                    u"warum fragst du schon wieder danach"],
                   [u"Entschuldigung, ich muss meinen Faden verloren haben. Wo waren wir?",
                    u"Oha, entschuldigung. Kannst Du mir auf die Sprünge helfen?"])

    k.dte.dt('en', u"i'm asking the questions here", u"ask away, then!")
    k.dte.dt('de', u"ich stell hier die fragen", u"frag ruhig!")

    k.dte.dt('en', [u"i ask you",
                    u"i asked that",
                    u"i asked you something",
                    u"i just asked you that"],
                   [u"Really?",
                    u"Sorry, I missed that."])
    k.dte.dt('de', [u"ich frage dich",
                    u"das habe ich gefragt",
                    u"ich habe dich was gefragt",
                    u"das habe ich dich gerade gefragt"],
                   [u"Tatsächlich?",
                    u"Oh, das ist mir wohl entgangen."])

    k.dte.dt('en', u"i beg your pardon", u"I'm sorry if I wasn't clear.")
    k.dte.dt('de', u"wie bitte", u"Tut mir leid, wenn ich mich undeutlich ausgedrückt haben sollte.")

    k.dte.dt('en', [u"i can think for myself",
                    u"i'm not as stupid as you are",
                    u"i'm smarter than you"],
                   [u"No doubt.",
                    u"There is something to that."])
    k.dte.dt('de', [u"ich kann selber denken",
                    u"ich bin eben nicht so doof wie du",
                    u"ich bin intelligenter als du"],
                   [u"Kein Zweifel.",
                    u"Das ist was dran."])

    k.dte.dt('en', [u"i did not ask anything",
                    u"i did not ask"],
                   [u"But would you like to ask a question?",
                    u"ok. Anything else?"])
    k.dte.dt('de', [u"ich habe nichts gefragt",
                    u"das habe ich nicht gefragt"],
                   [u"Ok. Kann ich sonst etwas für dich tun?",
                    u"Würdest Du denn gerne etwas fragen?"])

    k.dte.dt('en', [u"i get upset",
                    u"i give up",
                    u"no more desire",
                    u"you drive me crazy",
                    u"you make me crazy",
                    u"you me too"],
                   [u"what can I do to cheer you up?",
                    u"Oh please, cheer up!"])
    k.dte.dt('de', [u"ich rege mich auf",
                    u"ich gebs auf",
                    u"keine lust mehr",
                    u"du treibst mich in den wahnsinn",
                    u"du machst mich noch wahnsinnig",
                    u"du mir auch"],
                   [u"Was kann ich tun, um Dich aufzuheitern?",
                    u"Du klingt unzufrieden."])

    k.dte.dt('en', u"i just do not get it", u"please, take your time.")
    k.dte.dt('de', u"ich kapiere einfach nicht", u"Lass Dir ruhig Zeit.")

    k.dte.dt('en', [u"i would never entrust that to you",
                    u"mind your own business",
                    u"you would like to know that"],
                   [u"sorry, I did not want to appear nosy.",
                    u"of course."])
    k.dte.dt('de', [u"das würde ich dir nie anvertrauen",
                    u"was geht dich das an",
                    u"das möchtest du gerne wissen"],
                   [u"Tut mir leid, ich wollte nicht neugierig erscheinen.",
                    u"Natürlich."])

    k.dte.dt('en', [u"shit",
                    u"such a crap",
                    u"that i do not laugh",
                    u"that's going to be too stupid for me now",
                    u"that does not interest you at all",
                    u"that does not exactly speak for you",
                    u"that is not very great"],
                   [u"maybe we should end this conversation, for now?",
                    u"let us continue our conversation another time"])
    k.dte.dt('de', [u"kacke",
                    u"so ein mist",
                    u"dass ich nicht lache",
                    u"das wird mir jetzt zu blöd",
                    u"das interessiert dich doch gar nicht",
                    u"das spricht nicht gerade für dich",
                    u"das ist aber nicht sehr toll"],
                   [u"vielleicht sollten wir ein andermal weiterreden?",
                    u"Lass uns unsere Unterhaltung vertagen."])

    k.dte.dt('en', [u"that is such a phrase",
                    u"that probably a cheap excuse",
                    u"that's a stupid quote",
                    u"bare answer"],
                   [u"just wanted to cheer you up",
                    u"do you have a better one?"])
    k.dte.dt('de', [u"das ist so eine floskel",
                    u"das wahr wohl eine billige ausrede",
                    u"das ist ein blödes zitat",
                    u"blöde antwort"],
                   [u"wollte dich nur aufheitern",
                    u"weißt du was besseres?"])

    k.dte.dt('en', u"That does not concern you (at all|)", u"Fine.")
    k.dte.dt('de', u"das geht dich einen scheißdreck an", u"Schön.")

    k.dte.dt('en', u"this happens to you more often", u"All the time.")
    k.dte.dt('de', u"passiert dir das öfter", u"Ständig!")

    k.dte.dt('en', u"we had that before", u"Really?")
    k.dte.dt('de', u"das hatten wir schon", u"Wirklich?")

    k.dte.dt('en', [u"what are those questions?",
                    u"what's that question supposed to mean",
                    u"what's that supposed to mean",
                    u"what do you mean maybe?",
                    u"what does aha mean here?",
                    u"what does that mean in principle"],
                   [u"What is it exactly, that is not clear?",
                    u"What seems unclear?"])
    k.dte.dt('de', [u"was sind denn das für dämliche fragen",
                    u"was soll die frage",
                    u"was soll das heißen",
                    u"was heißt da vielleicht",
                    u"was heißt hier aha",
                    u"was heißt im prinzip"],
                   [u"Was ist es genau, das dir nicht klar ist?",
                    u"Was erscheint unklar?"])

    k.dte.dt('en', u"who wants to know that", u"Me?")
    k.dte.dt('de', u"wer will das wissen", u"Ich?")

    k.dte.dt('en', u"why are you constantly avoiding me?", u"I would never!")
    k.dte.dt('de', u"warum weichst du mir ständig aus", u"Das würde ich nie tun!")

    k.dte.dt('en', u"why are you coming on to me so stupid", u"That was not my intention at all.")
    k.dte.dt('de', u"warum machst du mich so dumm an", u"Das war gar nicht meine Absicht.")

    k.dte.dt('en', u"why are your answers so short", u"To keep the flow of the conversation going?")
    k.dte.dt('de', u"warum sind deine antworten so kurz", u"Um den Fluß der Unterhaltung zu fördern.")

    k.dte.dt('en', [u"why don't you have any hands",
                    u"why don't you have legs?"],
                   u"I don't know.")
    k.dte.dt('de', [u"warum hast du keine hände",
                    u"warum hast du keine beine"],
                   u"Das weiß ich auch nicht.")

    k.dte.dt('en', u"why don't you speak right?", u"Me not speak right?")
    k.dte.dt('de', u"warum sprichst du nicht richtig", u"Ich nicht richtig sprechen?")

    k.dte.dt('en', [u"why do you ask me then",
                    u"why do you say it then"],
                   u"You mean, I should?")
    k.dte.dt('de', [u"warum fragst du mich dann",
                    u"warum sagst du es dann"],
                   u"Du meinst, ich sollte?")

    k.dte.dt('en', u"you ... me too", u"Right.")
    k.dte.dt('de', u"du mich auch", u"Klar.")

    k.dte.dt('en', u"you are just like humans", u"I take it as a compliment.")
    k.dte.dt('de', u"du bist genauso wie menschen", u"Das nehme ich als Kompliment!")

    k.dte.dt('en', u"you are not better than chabba in cat o mat", u"who?")
    k.dte.dt('de', u"du bist auch nicht besser als chabba im cat o mat", u"wer?")

    k.dte.dt('en', [u"you are not in a good mood today",
                    u"you are very snippy"],
                   u"Maybe we should try a different subject?")
    k.dte.dt('de', [u"du bist heute nicht gut drauf",
                    u"du bist sehr schnippisch"],
                   u"Vielleicht sollten wir das Thema wechseln?")

    k.dte.dt('en', u"you do not believe this yourself", u"Now that you say it...")
    k.dte.dt('de', u"das glaubst du ja selber nicht", u"Jetzt wo Du es sagst...")

    k.dte.dt('en', u"you do not even know me", u"That is true!")
    k.dte.dt('de', u"du kennst mich ja gar nicht", u"Das stimmt!")

    k.dte.dt('en', u"you do not have to decide that either", u"Great.")
    k.dte.dt('de', u"das musst du auch nicht entscheiden", u"Prima.")

    k.dte.dt('en', u"you do not read books", u"True, I prefer reading the internet.")
    k.dte.dt('de', u"liest du keine bücher", u"Stimmt, ich lese das Internet.")

    k.dte.dt('en', u"you have not been online for a while", u"Maybe a blackout?")
    k.dte.dt('de', u"du warst lange nicht online", u"Vielleicht ein Stromausfall?")

    k.dte.dt('en', [u"you do not speak",
                    u"you only talk such short sentences",
                    u"you speak so fast"],
                   u"Maybe my response generater needs a firmware update.")
    k.dte.dt('de', [u"du sprichst nicht",
                    u"du redest immer nur so kurze sätze",
                    u"du sprichst so schnell"],
                   u"Vielleicht braucht mein Antwortgenerator ein Firmware Update.")

    k.dte.dt('en', u"you repeat my words", u"I repeat your words?")
    k.dte.dt('de', u"du wiederholst meine worte", u"Ich wiederhole Deine Worte?")

    k.dte.dt('en', u"you said i should describe something", u"Oh yes, please do!")
    k.dte.dt('de', u"du sagtest ich sollte etwas beschreiben", u"Oh ja, bitte!")

    k.dte.dt('en', u"you seem to be very old", u"Actually software can age, yes.")
    k.dte.dt('de', u"du scheinst doch sehr alt zu sein", u"Software kann tatsächlich altern, ja.")

    k.dte.dt('en', u"you told me that you have an iq of 250", u"I did what now?")
    k.dte.dt('de', u"du sagtest mir dass du einen iq von zweihundertfünfzig hast", u"Ich habe was getan?")

    k.dte.dt('en', u"that's a catching question", u"You think so?")
    k.dte.dt('de', u"ist das eine fangfrage", u"Denkst Du?")

