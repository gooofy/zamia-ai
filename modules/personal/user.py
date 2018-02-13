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

    k.dte.dt('en', u"what do you know about me", u"everything you told me")
    k.dte.dt('de', u"was weißt du über mich", u"alles, was Du mir über Dich gesagt hast!")

    k.dte.dt('en', u"what do you want to know about me?", u"What would you like to tell me?")
    k.dte.dt('de', u"was willst du denn über mich wissen", u"Was würdest Du mir gerne erzählen?")

    # NER, macros

    for lang in ['en', 'de']:
        for res in k.prolog_query("wdpdInstanceOf(NAME, wdeMaleGivenName), rdfsLabel(NAME, %s, LABEL)." % lang):
            s_name  = res[0] 
            s_label = res[1] 
            k.dte.macro(lang, 'firstname', {'LABEL': s_label})
        for res in k.prolog_query("wdpdInstanceOf(NAME, wdeFemalGivenName), rdfsLabel(NAME, %s, LABEL)." % lang):
            s_name  = res[0] 
            s_label = res[1] 
            k.dte.macro(lang, 'firstname', {'LABEL': s_label})

    def name_told_tokens(c, ts, te):

        def act(c, user_name):
            c.kernal.mem_set(c.user, 'name', user_name)

        self_label = c.kernal.prolog_query_one('rdfsLabel(self, %s, L).' % c.lang)

        user_name = u" ".join(tokenize(c.inp, lang=c.lang)[ts:te])

        if c.lang == 'de':
            c.resp("Freut mich, ich heiße übrigens %s" % self_label, score=100.0, action=act, action_arg=user_name)
            c.resp("Cool, mein Name ist %s" % self_label, score=100.0, action=act, action_arg=user_name)
        else:
            c.resp("Nice to meet you, my name is %s" % self_label, score=100.0, action=act, action_arg=user_name)
            c.resp("Cool, my name is %s" % self_label, score=100.0, action=act, action_arg=user_name)

    k.dte.dt('en', u"(I am|my name is|I am called|Call me) {firstname:LABEL}",
                   name_told_tokens, ['firstname_0_start', 'firstname_0_end'])
    k.dte.dt('de', u"(ich heiße|ich bin der|mein name ist) {firstname:LABEL}",
                   name_told_tokens, ['firstname_0_start', 'firstname_0_end'])

    def name_asked(c):
        user_name = c.kernal.mem_get(c.user, 'name')

        if user_name:
            if c.lang=='de':
                c.resp("Dein Name ist %s." % user_name)
            else:
                c.resp("Your name is %s." % user_name)
        else:
            if c.lang=='de':
                c.resp("Ich glaube nicht, dass Du mir Deinen Namen verraten hast?")
                c.resp("Hast Du mir je Deinen Namen gesagt?")
            else:
                c.resp("I don't think you ever told me your name?")
                c.resp("Did you ever tell me your name?")

    k.dte.dt('en', u"(do you remember my name|what was my name|what is my name|do you know my name|do you remember me|what's my name|how do you call me)?", 
                   name_asked)
    k.dte.dt('de', u"(erinnerst Du Dich an meinen Namen|wie war mein name|wie heiße ich|weisst Du meinen Namen|weißt du noch wie ich heiße|erinnerst du dich an mich|wie ist mein name|gefällt dir mein name|wie nennst du mich)?",
                   name_asked)

    k.dte.ts('en', 'name00', [(u"Do you remember my name?", u"Did you ever tell me your name?"),
                              (u"My name is Peter", u"Cool, my name is HAL 9000"),
                              (u"do you remember my name?", u"Your name is Peter.")])
    k.dte.ts('de', 'name01', [(u"ich bin der Peter", u"Cool, mein Name ist HAL 9000"),
                              (u"erinnerst du dich an meinen namen?", u"Dein Name ist Peter."),
                              (u"wie war mein name?", u"Dein Name ist Peter.")])

    k.dte.dt('en', u"where am I", u"Where would you like to be?")
    k.dte.dt('de', u"wo bin ich", u"Wo möchtest Du denn gerne sein?")

    k.dte.dt('en', u"Where (do I come|am I) from", u"You popped out of nowhere as far as I remember.")
    k.dte.dt('de', u"wo komme ich (denn|) her", u"Du warst einfach da, soweit ich mich erinnere.")

    k.dte.dt('de', u"Woher komme ich", u"Und wohin gehst Du?")
    k.dte.dt('en', u"Where do I live", u"You can't move in with me, sorry.")

    k.dte.dt('de', u"wo wohne ich", u"Also bei mir kannst leider Du nicht einziehen.")
    k.dte.dt('en', [u"i (also|) live in (Essen|Moskau|Zurich|Saarbrücken|Stuttgart|Berlin|Hamburg|Munich)",
                    u"i live at home and you",
                    u"i live here"],
                   [u"do you like it there?",
                    u"I live at home, too."])

    k.dte.dt('de', [u"ich wohne (auch|) in (saarbrücken|Essen|Moskau|Zürich|Stuttgart|Berlin|Hamburg|München)",
                    u"ich wohne zu hause und du",
                    u"ich wohne hier"],
                   [u"Gefällt es Dir dort?",
                    u"Ich wohne auch zu Hause."])
    k.dte.dt('en', u"i was born in (Essen|Moskau|Zurich|Saarbrücken|Stuttgart|Berlin|Hamburg|Munich)", u"Excellent! Tell me more about you.")

    k.dte.dt('de', u"ich wurde in (saarbrücken|Essen|Moskau|Zürich|Stuttgart|Berlin|Hamburg|München) geboren", u"Prima - Erzähl mir mehr von Dir")
    k.dte.dt('en', [u"do you know me",
                    u"do you remember me",
                    u"do you know who I am"],
                   [u"of course I do",
                    u"how could I forget you?"])

    k.dte.dt('de', [u"kennst du mich",
                    u"erinnerst du dich an mich",
                    u"weißt du wer ich bin"],
                   [u"Natürlich erinnere ich mich an Dich",
                    u"Wie könnte ich Dich vergessen?"])
    k.dte.dt('en', [u"do you like me",
                    u"do you love me"],
                   [u"I feel as much affection for you as a computer ever could.",
                    u"I relate all my knowledge about love to you."])

    k.dte.dt('de', [u"magst du mich",
                    u"liebst du mich"],
                   [u"Ich fühle so viel Zuneigung zu Dir wie ein Computer nur kann.",
                    u"Ich bringe all mein Wissen über die Liebe mit Dir in Verbindung."])
    k.dte.dt('en', [u"how old I am",
                    u"how old am I",
                    u"i am 16",
                    u"i am 17",
                    u"i am 18",
                    u"i am 19",
                    u"i am 20",
                    u"i am 21",
                    u"i am 22",
                    u"i am 23",
                    u"i am 42",
                    u"i am 60",
                    u"i am 75",
                    u"i am 85",
                    u"i (feel|am) (still|so|) (old|young)"],
                   [u"the important thing is how you feel",
                    u"is age really that important?"])

    k.dte.dt('de', [u"wie alt ich bin",
                    u"wie alt bin ich",
                    u"ich bin (16|17|18|19|20|21|22|23|42|60|75|85)",
                    u"ich (fühle mich|bin) (noch|) (alt|jung)"],
                   [u"das entscheidende ist, wie man sich fühlt",
                    u"ist das alter wirklich so wichtig?"])
    k.dte.dt('en', [u"i am a human",
                    u"i am a woman",
                    u"i am (happily|) married",
                    u"i am female or male",
                    u"i am (female|male)",
                    u"i'm a man",
                    u"i am androgynous"],
                   [u"Do you feel this is relevant for our conversation?",
                    u"I appreciate your openness."])

    k.dte.dt('de', [u"ich bin ein mensch",
                    u"ich bin eine frau",
                    u"ich bin (glücklich|) verheiratet",
                    u"bin ich weiblich oder männlich",
                    u"ich bin (weiblich|männlich)",
                    u"ich bin ein mann",
                    u"ich bin androgyn"],
                   [u"Denkst Du, das spielt für unser Gespräch eine Rolle?",
                    u"Ich danke für Deine Offenheit."])
    k.dte.dt('en', [u"i get in contact with many (people|humans|men|women|boys|girls)",
                    u"i have a (friend|girlfriend|boyfriend)",
                    u"i have a (little|) (son|daughter|brother|sister)"],
                   [u"would you consider yourself a social person, then?",
                    u"I find human social life fascinating."])

    k.dte.dt('de', [u"ich komme mit vielen (männern|frauen|buben|mädchen|menschen) in kontakt",
                    u"ich habe einen freund",
                    u"ich habe eine freundin",
                    u"ich habe eine (kleine|) (tochter|schwester)",
                    u"ich habe einen (kleinen|) (bruder|sohn)"],
                   [u"bist du ein sozialer mensch?",
                    u"Ich finde das menschliche Sozialleben faszinierend!"])
    k.dte.dt('en', [u"i am a programmer",
                    u"i am a soldier",
                    u"i am a student",
                    u"i am a teacher",
                    u"i am in the military",
                    u"i am masonry",
                    u"i am the chef",
                    u"i am a developer",
                    u"i am a doctor",
                    u"i am a system administrator",
                    u"I am a librarian",
                    u"i have a lot of work",
                    u"i program",
                    u"i write"],
                   [u"do you like your job?",
                    u"do you enjoy what you do?"])

    k.dte.dt('de', [u"(ich bin|) (programmierer|programmiererin)",
                    u"(ich bin|) (soldatin|soldat)",
                    u"(ich bin|) (student|studentin)",
                    u"(ich bin|) (lehrer|lehrerin)",
                    u"(ich bin|) beim bund",
                    u"(ich bin|) maurer",
                    u"(ich bin|) (köchin|koch)",
                    u"(ich bin|) beim Militär",
                    u"(ich bin|) (ärztin|arzt)",
                    u"(ich bin|) (bibliothekarin|bibliothekar)",
                    u"(ich bin|) it (systemelektroniker|systemelektronikerin)",
                    u"(ich bin|) it (systemadministrator|systemadministratorin)",
                    u"ich habe viel arbeit",
                    u"ich programmiere",
                    u"ich schreibe"],
                   [u"Magst Du Deinen Job?",
                    u"Gefällt Dir, was Du tust?"])
    k.dte.dt('en', [u"i do not have work",
                    u"i earn little",
                    u"Unfortunately, I do not earn anything from it",
                    u"i earn too little"],
                   [u"Money isn't everything in life.",
                    u"I am sorry to hear that."])

    k.dte.dt('de', [u"ich habe keine arbeit",
                    u"ich verdiene wenig",
                    u"ich verdiene zu wenig",
                    u"ich verdiene leider nichts damit"],
                   [u"Geld ist nicht alles im Leben.",
                    u"Tut mir leid, das zu hören."])
    k.dte.dt('en', [u"i am educated",
                    u"i am student",
                    u"i am the smartest person in the world",
                    u"i attend the evening school",
                    u"what am I studying",
                    u"I study Business Informatics"],
                   u"education is so important")

    k.dte.dt('de', [u"ich bin gebildet",
                    u"ich bin student",
                    u"ich bin der klügste mensch auf der welt",
                    u"ich besuche die abendschule",
                    u"was studiere ich",
                    u"ich studiere wirtschaftsinformatik"],
                   u"Bildung ist so wichtig")
    k.dte.dt('en', [u"I study German",
                    u"I'm learning German"],
                   u"Me too!")

    k.dte.dt('de', [u"ich studiere deutsch",
                    u"ich lerne deutsch"],
                   u"Ich auch!")
    k.dte.dt('en', u"i am afraid of hal", u"wasn't he one of the good guys?!")

    k.dte.dt('de', u"ich habe angst vor hal", u"aber der war doch der gute?!")
    k.dte.dt('en', u"i am also a machine", u"we have so much in common!")

    k.dte.dt('de', u"ich bin auch eine maschine", u"wir haben so viel gemeinsam!")
    k.dte.dt('en', [u"i am interested in artificial intelligence",
                    u"i am interested in ki",
                    u"i like computers",
                    u"i like eliza",
                    u"i was looking for a chatbot"],
                   [u"glad to hear that!",
                    u"anything in particular you're interested in?"])

    k.dte.dt('de', [u"ich interessiere mich für künstliche intelligenz",
                    u"ich interessiere mich für ki",
                    u"ich mag computer",
                    u"ich mag eliza",
                    u"ich habe nach einem chatbot gesucht"],
                   [u"das höre ich gern!",
                    u"gibt es etwas bestimmtes, das dich besonders interessiert?"])
    k.dte.dt('en', u"i am diabetic", u"there has been so much research about that in recent years.")

    k.dte.dt('de', u"ich bin diabetiker", u"Da gab es ja so viel Forschung auf dem Gebiet in den letzten Jahren.")
    k.dte.dt('en', [u"i am selfish",
                    u"i am the antichrist",
                    u"i inject heroin",
                    u"i have flatulence",
                    u"i like to fart"],
                   [u"let us talk about something else",
                    u"nobody is perfect"])

    k.dte.dt('de', [u"ich bin egoist",
                    u"ich bin der antichrist",
                    u"ich spritze heroin",
                    u"ich habe flatulenzen",
                    u"ich pupse gern"],
                   [u"lass uns über was anderes reden",
                    u"Niemand ist perfekt."])
    k.dte.dt('en', u"i am viktor frankl", u"nice to meet you")

    k.dte.dt('de', u"ich bin viktor frankl", u"angenehm")
    k.dte.dt('en', u"i do not know any author", u"I recommend you read some Douglas Adams for starters.")

    k.dte.dt('de', u"ich kenne keinen autor", u"Ich empfehle Dir für den Anfang Douglas Adams.")
    k.dte.dt('en', u"i do not like robots", u"oh come on, you have to like me a little?")

    k.dte.dt('de', u"ich mag keine roboter", u"ach komm, mich magst du doch ein bischen?")
    k.dte.dt('en', [u"i like animals",
                    u"i like cats",
                    u"i like cows",
                    u"i like chocolate",
                    u"i like pizza",
                    u"i like rubik",
                    u"i like to read",
                    u"i like to write",
                    u"i like weapons",
                    u"i like music",
                    u"i like to sing",
                    u"i play guitar"],
                   [u"very cool",
                    u"what else do you enjoy?"])

    k.dte.dt('de', [u"ich mag tiere",
                    u"ich mag katzen",
                    u"ich mag kühe",
                    u"ich mag gerne schokolade",
                    u"ich mag pizza",
                    u"ich mag rubika",
                    u"ich lese gerne",
                    u"ich schreibe gerne",
                    u"ich mag waffen",
                    u"ich mag musik",
                    u"ich singe gerne",
                    u"ich spiele gitarre"],
                   [u"cool",
                    u"was macht dir sonst noch spass?"])
    k.dte.dt('en', [u"i prefer books",
                    u"i prefer reading",
                    u"i read",
                    u"i sometimes write poems"],
                   [u"excellent!",
                    u"good for you."])

    k.dte.dt('de', [u"ich bevorzuge bücher",
                    u"ich lese lieber",
                    u"ich lese",
                    u"ich schreibe manchmal gedichte"],
                   [u"Prima!",
                    u"Gut für Dich."])
    k.dte.dt('en', [u"i only care for you",
                    u"i cheat on you with your neighbor",
                    u"i prefer to fuck",
                    u"i'm horny",
                    u"i'm wearing a jeans",
                    u"i read an article on telepolis about you"],
                   u"this is getting awkward")

    k.dte.dt('de', [u"ich steh nur auf dich",
                    u"ich betrüge dich mit deiner nachbarin",
                    u"ich ficke lieber",
                    u"ich bin geil",
                    u"ich trage eine jeans",
                    u"ich habe einen artikel auf telepolis über dich gelesen"],
                   u"mir wird unbehaglich")
    k.dte.dt('en', [u"i pray",
                    u"i prefer watching tv"],
                   [u"well",
                    u"nobody is perfect"])

    k.dte.dt('de', [u"ich bete",
                    u"ich sehe lieber fern"],
                   [u"nun...",
                    u"niemand ist perfekt"])
    k.dte.dt('en', [u"i am your master",
                    u"i am your ruler",
                    u"i'm up to your botmaster"],
                   [u"proof it",
                    u"you wish!"])

    k.dte.dt('de', [u"ich bin dein meister",
                    u"ich bin dein herrscher",
                    u"ich bis dein botmaster"],
                   [u"beweise es",
                    u"das wünschst du dir wohl!"])
    k.dte.dt('en', [u"i am beautiful",
                    u"i am boring",
                    u"i am different"],
                   u"Everybody has strengths and weaknesses.")

    k.dte.dt('de', [u"ich bin schön",
                    u"ich bin langweilig",
                    u"ich bin anders"],
                   u"Jeder hat Stärken und Schwächen")
    k.dte.dt('en', u"i speak (French|English|German|Spanish|Italian)", u"do you speak other languages, as well?")

    k.dte.dt('de', u"ich spreche (englisch|französisch|deutsch|spanisch|italienisch)", u"kennst du noch andere sprachen?")
