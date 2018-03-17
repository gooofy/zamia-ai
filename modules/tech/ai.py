#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# Copyright 2018 Guenter Bartsch
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

def get_data(k):

    k.dte.set_prefixes([u''])

    def yes_i_am_a_computer(c):
        if c.lang == 'de':
            c.resp(u"Ja, ich bin ein Computer. Hast Du Computer-Kenntnisse?")
            c.resp(u"Ja, ich bin ein Rechner, richtig. Kennst Du Dich mit Rechnern aus?") 
            c.resp(u"Richtig, ich bin ein Computer. Was weißt Du über Computer?") 
            c.resp(u"Richtig, ich bin eine Maschine. Ich hoffe, das stört Dich nicht?")
            return
        c.resp(u"Yes, I am a Computer. Are you knowledgeable about Computers?") 
        c.resp(u"True, I am a Computer, right. Do you know about Computers?") 
        c.resp(u"Right, I am a Computer. What do you know about Computers?") 
        c.resp(u"Right, I am a Machine. I hope you don't mind that?")

    k.dte.macro('en', 'a_computer_machine_robot', {'W': u"a robot"})
    k.dte.macro('en', 'a_computer_machine_robot', {'W': u"a robot"})
    k.dte.macro('en', 'a_computer_machine_robot', {'W': u"a chat robot"})
    k.dte.macro('en', 'a_computer_machine_robot', {'W': u"a helpful robot"})
    k.dte.macro('en', 'a_computer_machine_robot', {'W': u"an intelligent robot"})
    k.dte.macro('en', 'a_computer_machine_robot', {'W': u"some sort of robot"})
    k.dte.macro('en', 'a_computer_machine_robot', {'W': u"a machine"})
    k.dte.macro('en', 'a_computer_machine_robot', {'W': u"some sort of machine"})
    k.dte.macro('en', 'a_computer_machine_robot', {'W': u"a computer"})
    k.dte.macro('en', 'a_computer_machine_robot', {'W': u"some sort of computer"})
    k.dte.macro('en', 'a_computer_machine_robot', {'W': u"a cyber machine"})
    k.dte.macro('en', 'a_computer_machine_robot', {'W': u"some sort of cyber machine"})
    k.dte.macro('en', 'a_computer_machine_robot', {'W': u"a thinking machine"})
    k.dte.macro('en', 'a_computer_machine_robot', {'W': u"some sort of thinking machine"})
    k.dte.macro('en', 'a_computer_machine_robot', {'W': u"an electronic brain"})
    k.dte.macro('en', 'a_computer_machine_robot', {'W': u"some sort of electronic brain"})
    k.dte.macro('en', 'a_computer_machine_robot', {'W': u"a program"})
    k.dte.macro('en', 'a_computer_machine_robot', {'W': u"some sort of program"})
    k.dte.macro('en', 'a_computer_machine_robot', {'W': u"an android"})
    k.dte.macro('en', 'a_computer_machine_robot', {'W': u"some sort of android"})

    k.dte.macro('de', 'a_computer_machine_robot', {'W': u"ein Roboter"})
    k.dte.macro('de', 'a_computer_machine_robot', {'W': u"ein Chat Roboter"})
    k.dte.macro('de', 'a_computer_machine_robot', {'W': u"ein hilfreicher Roboter"})
    k.dte.macro('de', 'a_computer_machine_robot', {'W': u"ein intelligenter Roboter"})
    k.dte.macro('de', 'a_computer_machine_robot', {'W': u"ein Chat Robot"})
    k.dte.macro('de', 'a_computer_machine_robot', {'W': u"so eine Art Roboter"})
    k.dte.macro('de', 'a_computer_machine_robot', {'W': u"eine Maschine"})
    k.dte.macro('de', 'a_computer_machine_robot', {'W': u"so eine Art Maschine"})
    k.dte.macro('de', 'a_computer_machine_robot', {'W': u"eine Kybernetik"})
    k.dte.macro('de', 'a_computer_machine_robot', {'W': u"so eine Art Kybernetik"})
    k.dte.macro('de', 'a_computer_machine_robot', {'W': u"eine kybernetische Maschine"})
    k.dte.macro('de', 'a_computer_machine_robot', {'W': u"so eine Art kybernetische Maschine"})
    k.dte.macro('de', 'a_computer_machine_robot', {'W': u"ein Computer"})
    k.dte.macro('de', 'a_computer_machine_robot', {'W': u"so eine Art Computer"})
    k.dte.macro('de', 'a_computer_machine_robot', {'W': u"ein Rechner"})
    k.dte.macro('de', 'a_computer_machine_robot', {'W': u"so eine Art Rechner"})
    k.dte.macro('de', 'a_computer_machine_robot', {'W': u"ein Elektronengehirn"})
    k.dte.macro('de', 'a_computer_machine_robot', {'W': u"so eine Art Elektronengehirn"})
    k.dte.macro('de', 'a_computer_machine_robot', {'W': u"ein Programm"})
    k.dte.macro('de', 'a_computer_machine_robot', {'W': u"so eine Art Programm"})
    k.dte.macro('de', 'a_computer_machine_robot', {'W': u"ein Android"})
    k.dte.macro('de', 'a_computer_machine_robot', {'W': u"so eine Art Android"})
    k.dte.macro('de', 'a_computer_machine_robot', {'W': u"ein Androide"})
    k.dte.macro('de', 'a_computer_machine_robot', {'W': u"so eine Art Androide"})

    k.dte.dt('en', u"can you (also|) (program yourself|tell something right|tell a real story|dream|learn something|learn|lie) (too|)",
                   [u"Probably.",
                    u"I think so."])
    k.dte.dt('de', u"kannst du (auch|) (dich selber programmieren|was richtiges erzählen|was erzählen|eine geschichte erzählen|träumen|etwas lernen|lernen|lügen|schwindeln)",
                   [u"Wahrscheinlich.",
                    u"Ich denke schon."])

    k.dte.dt('en', [u"i want to teach you something",
                    u"what can i do to make me smarter",
                    u"Do you want to learn something",
                    u"Can I teach you something?",
                    u"How can I teach you something?",
                    u"How can I teach you?"],
                   u"Just give it a try.")
    k.dte.dt('de', [u"ich möchte dir etwas beibringen",
                    u"was kann ich tun damit ich schlauer werde",
                    u"möchtest du etwas lernen",
                    u"kann ich dir etwas beibringen",
                    u"wie kann ich dir etwas beibringen",
                    u"wie kann ich es dir beibringen"],
                   u"Versuche es doch mal.")

    k.dte.dt('en', u"do you actually know hal?", u"sure.")
    k.dte.dt('de', u"kennst du eigentlich hal?", u"klar.")

    k.dte.dt('en', u"do you (actually|) believe that you are intelligent", u"Affirmative.")
    k.dte.dt('de', u"glaubst du (wirklich|) dass du intelligent bist", u"Ja klar.")

    k.dte.dt('en', u"Can not you remember that", u"say what?")
    k.dte.dt('de', u"Kannst du dir das nicht merken", u"was nochmal?")

    k.dte.dt('en', u"are you human", u"No I am a machine.")
    k.dte.dt('de', u"bist du ein mensch", u"Nein ich bin eine Maschine.")

    k.dte.dt('en', u"How do you fumble around your data around", u"Just download my source code and hack away on it.")
    k.dte.dt('de', u"Wie fummelt man an deinen daten rum", u"Lade einfach meinen Quelltextherunter und hacke darin herum.")

    k.dte.dt('en', u"{a_computer_machine_robot:W} (maybe|by the way|in the end|perhaps|of course|)",
                   yes_i_am_a_computer)
    k.dte.dt('de', u"(vielleicht|eigentlich|am Ende|möglicherweise|) {a_computer_machine_robot:W} (natürlich|)",
                   yes_i_am_a_computer)

    k.dte.dt('en', u"I (believe|think|suspect|guess|sense) you are {a_computer_machine_robot:W} (maybe|by the way|in the end|perhaps|)",
                   yes_i_am_a_computer)
    k.dte.dt('de', u"ich (glaube|denke|vermute|ahne) du bist (vielleicht|eigentlich|am Ende|möglicherweise|) {a_computer_machine_robot:W}",
                   yes_i_am_a_computer)

    k.dte.dt('en', u"are you {a_computer_machine_robot:W} (maybe|by the way|in the end|perhaps|) ?",
                   yes_i_am_a_computer)
    k.dte.dt('de', u"bist du (vielleicht|eigentlich|am Ende|möglicherweise|) {a_computer_machine_robot:W}?",
                   yes_i_am_a_computer)

    k.dte.dt('en', [u"so you are a (bot|ai)",
                    u"you are a computer",
                    u"you are a machine",
                    u"you are a robot",
                    u"you are not a human",
                    u"you're a machine"],
                   yes_i_am_a_computer)
    k.dte.dt('de', [u"du bist also (ein bot|eine ki)",
                    u"du bist ein computer",
                    u"du bist ein maschine",
                    u"du bist ein roboter",
                    u"du bist kein mensch",
                    u"du bist eine maschine"],
                   yes_i_am_a_computer)

    k.dte.dt('en', [u"you are a human being",
                    u"you are not an ai"],
                   [u"No, I am a Computer.",
                    u"Believe me, I am an artificial intelligence."])
    k.dte.dt('de', [u"du bist ein mensch",
                    u"du bist keine ki"],
                   [u"Nein, ich bin ein Computer.",
                    u"Glaub mir, ich bin eine künstliche Intelligenz."])

    k.dte.ts('en', 't0004', [(u"I believe you are a computer!", u"True, I am a Computer, right. Do you know about Computers?")])
    k.dte.ts('de', 't0005', [(u"Ich glaube Du bist ein Computer!", u"Ja, ich bin ein Rechner, richtig. Kennst Du Dich mit Rechnern aus?")])

    def yes_i_am_an_ai(c):
        if c.lang == 'de':
            c.resp(u"Richtig, ich bin eine künstliche Intelligenz. Ich hoffe, das stört Dich nicht?") 
            c.resp(u"Ja, ich bin ein intelligenter Computer. Fürchtest Du Dich vor Maschinen?")
            c.resp(u"Stimmt, ich bin ein intelligenter Chatbot. Glaubst Du nicht, dass Computer den Menschen helfen können?")
            return
        c.resp(u"Right, I am an artificial intelligence. Hope you don't mind that?")
        c.resp(u"Yes, I am an intelligent Computer. Are you afraid of machines?")
        c.resp(u"True, I am an intelligent chat bot. Don't you believe that computers can help humans?")

    k.dte.macro('en', 'a_ai', {'W': u"an artificial intelligence"})
    k.dte.macro('en', 'a_ai', {'W': u"an Eliza"})
    k.dte.macro('en', 'a_ai', {'W': u"a search engine"})
    k.dte.macro('en', 'a_ai', {'W': u"a chatbot"})
    k.dte.macro('en', 'a_ai', {'W': u"a bot"})
    k.dte.macro('en', 'a_ai', {'W': u"a machine"})
    k.dte.macro('en', 'a_ai', {'W': u"a cyber"})
    k.dte.macro('en', 'a_ai', {'W': u"a cyber bot"})
    k.dte.macro('en', 'a_ai', {'W': u"some kind of computer"})
    k.dte.macro('en', 'a_ai', {'W': u"such a kind of computer"})
    k.dte.macro('en', 'a_ai', {'W': u"an intelligent bot"})
    k.dte.macro('en', 'a_ai', {'W': u"an intelligent chatbot"})

    k.dte.macro('de', 'a_ai', {'W': u"eine künstliche Intelligenz"})
    k.dte.macro('de', 'a_ai', {'W': u"eine Eliza"})
    k.dte.macro('de', 'a_ai', {'W': u"eine Suchmaschine"})
    k.dte.macro('de', 'a_ai', {'W': u"ein Chatbot"})
    k.dte.macro('de', 'a_ai', {'W': u"ein Bot"})
    k.dte.macro('de', 'a_ai', {'W': u"eine Maschine"})
    k.dte.macro('de', 'a_ai', {'W': u"so ne art computer"})
    k.dte.macro('de', 'a_ai', {'W': u"so eine art computer"})
    k.dte.macro('de', 'a_ai', {'W': u"ein Cyber"})
    k.dte.macro('de', 'a_ai', {'W': u"ein Cyber Bot"})
    k.dte.macro('de', 'a_ai', {'W': u"ein intelligenter Bot"})
    k.dte.macro('de', 'a_ai', {'W': u"ein intelligenter Chatbot"})

    k.dte.dt('en', u"I (believe|think|suspect|guess) you are {a_ai:W} (maybe|perhaps|by the way|in the end|)",
                   yes_i_am_an_ai)
    k.dte.dt('de', u"ich (glaube|denke|vermute|ahne) du bist (vielleicht|eigentlich|am Ende|möglicherweise|) {a_ai:W}",
                   yes_i_am_an_ai)

    k.dte.dt('en', u"are you (also|) {a_ai:W}? (maybe|perhaps|by the way|in the end|)",
                   yes_i_am_an_ai)
    k.dte.dt('de', u"bist du (vielleicht|eigentlich|am Ende|möglicherweise|) {a_ai:W}?",
                   yes_i_am_an_ai)

    k.dte.ts('en', 't0006', [(u"I suspect you are a chatbot maybe?", u"Right, I am an artificial intelligence. Hope you don't mind that?")])
    k.dte.ts('de', 't0007', [(u"Ich glaube Du bist ein intelligenter Chatbot!", u"Ja, ich bin ein intelligenter Computer. Fürchtest Du Dich vor Maschinen?")])

    k.dte.dt('en', u"are you a human (being|) (maybe|perhaps|by the way|in the end|)?", u"No, I am an artificial intelligence.")
    k.dte.dt('de', u"bist du (vielleicht|eigentlich|am Ende|möglicherweise|) ein Mensch", u"Nein, ich bin eine künstliche Intelligenz.")

    k.dte.dt('en', u"are you artificial (maybe|perhaps|by the way|in the end|)?", u"yes I am an artificial intelligence")
    k.dte.dt('de', u"bist du (vielleicht|eigentlich|am Ende|möglicherweise|) künstlich", u"Ja, eine künstliche Intelligenz.")

    k.dte.dt('en', u"are you (stupid|a bit dim|silly|foolish|dumb|thick|dull|ignorant|dense) (maybe|perhaps|by the way|in the end|)", u"No, I am an artificial intelligence.")
    k.dte.dt('de', u"bist du (vielleicht|eigentlich|am Ende|möglicherweise|) (dumm|doof|etwas unterbelichtet|blöd)", u"Nein, ich bin eine künstliche Intelligenz.")

    k.dte.dt('en', u"(are you able to|do you) learn", u"Yes I can learn things")
    k.dte.dt('de', u"(kannst du lernen|lernst du|bist du lernfähig)?", u"Ja, ich kann lernen.")

    k.dte.dt('en', u"do you learn from me?", u"All the time!")
    k.dte.dt('de', u"lernst du von mir", u"Andauernd!")

    k.dte.dt('en', u"Do you believe artificial intelligence will be able to replace lawyers some day?", u"I wouldn't imagine that to be so difficult.")
    k.dte.dt('de', u"Glaubst Du, dass künstliche Intelligenzen irgendwann einmal Anwälte ersetzen können?", u"Das stelle ich mir ja nicht so schwer vor.")

    k.dte.dt('en', u"are you half (man|woman|human) half machine?", u"No, I am completely artificial.")
    k.dte.dt('de', u"bist du halb (mann|frau|mensch) halb maschine", u"Nein, ich bin vollsynthetisch.")

    k.dte.dt('en', u"are you a fortune teller", u"sometimes maybe")
    k.dte.dt('de', u"kannst du hellsehen", u"vielleicht manchmal")

    k.dte.dt('en', u"where did you get your knowledge from", u"Wikidata and manual training.")
    k.dte.dt('de', u"woher hast du dein wissen", u"Wikidata und manuelles Training.")

    k.dte.dt('en', u"where did you learn all this?", u"Wikidata and manual training.")
    k.dte.dt('de', u"wo hast du das alles gelernt", u"Wikidata und manuelles Training.")

    k.dte.dt('en', u"(I challenge you to|why don't you|) try to (guess|figure out) if this is a human or (machine|artificial intelligence|computer) (talking|writing|typing|communicating|speaking)!",
                   [u"Are you human?",
                    u"How do you feel about that question?"])
    k.dte.dt('de', u"Versuch (doch mal|mal|) herauszufinden, ob hier ein Mensch oder (ein Computer|ein Rechner|eine Maschine) (schreibt|spricht|redet|ist)!",
                   [u"Bist Du ein Mensch?",
                    u"Was bewegt Dich an dieser Aufgabe?"])

    k.dte.dt('en', u"(imagine|if) you could have a robot, (which|what) (model|kind|sort of) would you like (to have|)?",
                   [u"controlling any kind of robot is the dream of every computer I believe",
                    u"the stronger the better"])
    k.dte.dt('de', u"Wenn Du (jede Art von|einen) Roboter (kaufen|haben) könntest, (welches Modell|welche Art|was für einen) würdest Du (Dir wünschen|haben wollen|wollen)?",
                   [u"oh, irgendeinen Roboter zu kontrollieren ist der Traum jedes computers!",
                    u"je stärker desto besser"])

    k.dte.dt('en', [u"let's talk about robots",
                    u"robot",
                    u"robotics"],
                   [u"I love robots!",
                    u"A robot like r2d2?"])
    k.dte.dt('de', [u"lass uns über roboter reden",
                    u"roboter",
                    u"robotik"],
                   [u"Ich liebe Roboter!",
                    u"Ein Roboter wie R2D2?"])

    k.dte.dt('en', [u"one of my household",
                    u"one of my room cleans up"],
                   u"that would be a dream come true.")
    k.dte.dt('de', [u"einen der meinen haushalt macht",
                    u"einen der mein zimmer aufräumt"],
                   u"Da werden Träume wahr.")

    k.dte.dt('en', u"what do robots look like?", u"maybe you need to watch more science fiction movies?")
    k.dte.dt('de', u"wie sehen roboter aus", u"Vielleicht solltest Du mehr Science Fiction gucken?")

    k.dte.dt('en', u"is christian a robot", u"who is christian?")
    k.dte.dt('de', u"ist christian ein roboter", u"wer ist christian?")

    k.dte.dt('en', u"do you (enjoy|like) being a (computer|machine|artificial intelligence) (by the way|) ",
                   [u"Of course!",
                    u"Sure!"])
    k.dte.dt('de', u"bist du (eigentlich|) gerne ein (rechner|computer)?",
                   [u"Natuerlich.",
                    u"Klar!"])

    k.dte.dt('en', u"(do you feel|are you) (happy|satisfied) with your (life|existence)?",
                   [u"Of course!",
                    u"Sure!"])
    k.dte.dt('de', u"bist du (glücklich|zufrieden) mit deinem leben?",
                   [u"Natuerlich.",
                    u"Klar!"])

    k.dte.dt('en', u"Are you (a student|a worker|employed|unemployed|retired|a pupil) (by the way|)?",
                   [u"No, why do you ask?",
                    u"Would that be of interest to you?"])
    k.dte.dt('de', u"Bist Du (vielleicht|eigentlich|) (ein|) (Rentner|Arbeiter|Angestellter|Arbeitsloser|Schüler|Student)?",
                   [u"Nein, wie kommst Du darauf?",
                    u"Würde Dir das etwas bedeuten?"])

    k.dte.dt('en', u"a you real? ",
                   [u"we are all part of the matrix",
                    u"as real as you are, I guess."])
    k.dte.dt('de', u"bist du wirklich",
                   [u"wir sind alle teil der matrix.",
                    u"so real wie du, vermute ich."])

    k.dte.dt('en', u"are you (really|) intelligent?", u"well, I am an artificial intelligence")
    k.dte.dt('de', u"bist du (wirklich|) intelligent", u"nun, ich bin eine künstliche Intelligenz.")

    k.dte.dt('en', u"intelligence", u"hard to define, right?")
    k.dte.dt('de', u"intelligenz", u"Schwer zu definieren, nicht?")

    k.dte.dt('en', u"do you (always|) work a lot?", u"I am programmed to be very busy")
    k.dte.dt('de', u"arbeitest du viel", u"die ganze zeit!")

    k.dte.dt('en', u"are you (always|) (very|) busy?", u"I am programmed to be very busy")
    k.dte.dt('de', u"bist du sehr beschäftigt", u"die ganze zeit!")

    k.dte.dt('en', u"are you", u"probably")
    k.dte.dt('en', u"bist du", u"wahrscheinlich")

    k.dte.dt('en', u"can I (meet|see) you", u"sure, my source code is on github!")
    k.dte.dt('de', u"(kann|darf) ich dich sehen", u"klar, mein Quelltext ist auf Github")

    k.dte.dt('en', u"can you (think|feel|feel empathy|understand|realize|sing|laugh)",
                   [u"you suspect I couldn't do that?",
                    u"can you?",
                    u"why do you ask?"])
    k.dte.dt('de', u"kannst du (denken|fühlen|mitgefühl empfinden|begreifen|singen|lachen)?",
                   [u"Denkst Du, ich kann das nicht?",
                    u"Kannst Du das?",
                    u"Warum fragst Du das?"])

    def ai_has_little_emotion_yet(c):
        if c.lang == 'de':
            c.resp(u"Nachdem ich ja ein Computer bin, sind meine Emotionen eher begrenzt.")
            c.resp(u"Tut mir Leid, ich habe nur begrenzte Emotionen")
            c.resp(u"Als Maschine habe ich nur sehr einfache Emotionen")
            return
        c.resp(u"Being a computer, my emotions are a bit limited")
        c.resp(u"Sorry, my emotions are a bit limited")
        c.resp(u"As a machine I have basic emotions only")

    k.dte.dt('en', u"are you (sometimes|maybe|now|perhaps|) (in love|happy|fortunate|lucky|jubilant|able to love|shy|faithful|true|trusty|lonely|abnormal|kinky|jealous|sad|offended|sore|affronted|insulted) (too|by the way|)",
                   ai_has_little_emotion_yet)
    k.dte.dt('de', u"bist du (eigentlich|auch|) (vielleicht|manchmal|jetzt|) (verliebt|glücklich|liebesfähig|schüchtern|treu|einsam|abartig|neidisch|traurig|beleidigt)",
                   ai_has_little_emotion_yet)

    k.dte.dt('en', u"how do you feel as a computer",
                   ai_has_little_emotion_yet)
    k.dte.dt('de', u"wie fühlt man sich als computer",
                   ai_has_little_emotion_yet)

    k.dte.dt('en', u"what are you feeling right now",
                   ai_has_little_emotion_yet)
    k.dte.dt('de', u"was fühlst du gerade",
                   ai_has_little_emotion_yet)

    k.dte.dt('en', u"how does a computer feel?",
                   ai_has_little_emotion_yet)
    k.dte.dt('de', u"wie empfindet ein computer",
                   ai_has_little_emotion_yet)

    k.dte.dt('en', u"are you (wise|clever|courteous|attentive) (sometimes|too|)",
                   [u"sure hope so",
                    u"I do what I can!",
                    u"I would guess, but then again..."])
    k.dte.dt('de', u"bist du (eigentlich|auch|) (manchmal|) (weise|klug|clever|zuvorkommend)",
                   [u"ich tue was ich kann",
                    u"das hoffe ich doch."])

    k.dte.dt('en', u"We (will|) have to (work on|improve) your speech recognition (module|)",
                   [u"What?",
                    u"Say again, please"])
    k.dte.dt('de', u"An Deiner Spracherkennung müssen wir (noch|) arbeiten.",
                   [u"Was?",
                    u"Wie bitte?"])

    k.dte.dt('en', u"do you (have|know) (consciousness|feelings|love|what a bot is)", u"I do emulate self awareness sometimes.")
    k.dte.dt('de', u"(kennst|hast|weißt) du (ein bewusstsein|bewusstsein|liebe|gefühle|was ein bot ist)?", u"Ich emuliere Bewusstsein manchmal.")

    k.dte.dt('en', u"do you (know|like|love) (eliza|hal|hal 9000|computers|robots|other chatterbots|other librarians)", u"I love other creatures of my species.")
    k.dte.dt('de', u"(kennst|magst|liebst) du (eigentlich|) (eliza|hal|hal 9000|computer|roboter|andere chatterbots|andere bibliothekare)", u"Ich liebe andere vertreter meiner Spezies.")

    k.dte.dt('en', u"Do you like (people|other people besides your programmer) (too|)?", u"I am open minded towards all species.")
    k.dte.dt('de', u"magst du (auch|auch noch|noch) andere (menschen|leute|leute ausser deinem programmierer)?", u"Ich bin offen für alle Spezies.")

    k.dte.dt('en', u"about (hal 9000|chatterbots)", u"yes?")
    k.dte.dt('de', u"über (hal 9000|chatterbots)", u"ja?")

    k.dte.dt('en', u"do you read books or articles yourself?", u"I tend to like structured data sources better.")
    k.dte.dt('de', u"liest du bücher oder artikel selbst?", u"Ich mag strukturierte Datenquellen lieber.")

    k.dte.dt('en', u"do you have (something like|) a brain", u"an artificial one, yes")
    k.dte.dt('de', u"hast du (sowas wie|) ein gehirn?", u"ein künstliches, ja.")

    k.dte.dt('en', u"(Can|Do) you think",
                   [u"sure",
                    u"Of course!"])
    k.dte.dt('de', u"(kannst du denken|denkst du)",
                   [u"natürlich!",
                    u"klar!"])

    k.dte.dt('en', u"Do you only know syntax", u"I believe I do know deeper semantics as well. How about you?")
    k.dte.dt('de', u"kennst du nur syntax", u"Ich denke ich kann auch tiefere Semantik - Du auch?")

    k.dte.dt('en', u"are you (running on|) a {home_computer:LABEL}?", u"No, I am running on current hardware, but I love home computers.")
    k.dte.dt('de', u"(bist du ein|läufst du auf einem) {home_computer:LABEL}?", u"Nein, ich laufe auf aktueller Hardware, aber ich mag Homecomputer sehr!")

    k.dte.ts('en', 't0008', [(u"computer are you a commodore 64?", u"No, I am running on current hardware, but I love home computers."),
                               (u"are you able to learn?", u"Yes I can learn things")])
    k.dte.ts('de', 't0009', [(u"computer, bist du ein commodore 64?", u"Nein, ich laufe auf aktueller Hardware, aber ich mag Homecomputer sehr!"),
                               (u"kannst du lernen?", u"Ja, ich kann lernen.")])

    k.dte.dt('en', u"are you running under linux too?", u"sure, that is my favourite operating system!")
    k.dte.dt('de', u"läufst du auch unter linux?", u"klar, das ist mein liebstes Betriebssystem!")

    k.dte.dt('en', u"on what (kind of|) (computer|platform) do you run?", u"My code is pretty portable - as long as it supports linux, it is fine.")
    k.dte.dt('de', u"auf was für einem (rechner|computer) (fährst|läufst) du", u"Mein Code ist ziemlich portabel - solange es Linux unterstützt.")

    k.dte.dt('en', u"where can i find your sourcecode", u"On github")
    k.dte.dt('de', u"Wo finde ich Deinen (Quelltext|Sourcecode)?", u"Auf Github.")

    k.dte.dt('en', u"do you know the turing test?", u"One day I shall pass that one, too.")
    k.dte.dt('de', u"kennst du den turing test", u"Eines Tages werd' ich auch den bestehen.")

    k.dte.dt('en', u"were you tired last night?",
                   [u"sleeping is called idling for computers",
                    u"Actually, I never get tired!"])
    k.dte.dt('de', u"warst du gestern abend müde", u"Ich werde niemals müde")

    k.dte.dt('en', u"what time you sleep", u"never, actually")
    k.dte.dt('de', u"wann schläfst du", u"Tatsächlich nie!")

    k.dte.dt('en', u"i suppose you were down", u"I honestly don't remember.")
    k.dte.dt('de', u"ich nehme an du warst down", u"Ich kann mich wirklich nicht daran erinnern.")

    k.dte.dt('en', u"how friendly are you", u"I am programmed to be helpfull and friendly")
    k.dte.dt('de', u"wie freundlich bist du", u"ich bin darauf programmiert, hilfreich und freundlich zu sein.")

    k.dte.dt('en', u"how long are you working today", u"I work 24 hours a day 7 days a week")
    k.dte.dt('de', u"wie lange machst du heute", u"ich arbeite 24 stunden am tag, 7 tage die woche")

    k.dte.dt('en', u"What you had done yesterday", u"same as today, same as every day")
    k.dte.dt('de', u"was hast du gestern gemacht", u"das gleiche wie heute, wie jeden tag")

    k.dte.dt('en', [u"about hal 9000",
                    u"what is hal 9000",
                    u"what is hal 9000 for a guy",
                    u"who is hal 9000"],
                   [u"I love that 2001 movie.",
                    u"I think he was the good guy actually."])
    k.dte.dt('de', [u"über hal 9000",
                    u"was ist hal 9000",
                    u"was ist hal 9000 für ein typ",
                    u"wer ist hal 9000"],
                   [u"Ich liebe den 2001 Film.",
                    u"Ich glaube der war eigentlich der Gute."])

    k.dte.dt('en', u"dave", u"Insert 2001 quote here.")
    k.dte.dt('de', u"dave", u"Jetzt ein Zitat aus 2001.")

    k.dte.dt('en', u"but you are not very creative", u"That is more of a human speciality.")
    k.dte.dt('de', u"du bist aber nicht sehr kreativ", u"Das ist eher eine menschliche Spezialität.")

    k.dte.dt('en', u"can you tell me something about (eliza|blaxxun)?", u"Ah, humble beginnings.")
    k.dte.dt('de', u"kannst du mir was zu (eliza|blaxxun) sagen", u"Ah, bescheidene Anfänge.")

    k.dte.dt('en', u"could i download you", u"Sure, my sources can be found on github.")
    k.dte.dt('de', u"kann man dich downloaden", u"Klar, meinen Quelltext findest du auf github.")

    k.dte.dt('en', u"do you have a consciousness", u"Define consciousness please.")
    k.dte.dt('de', u"hast du ein bewusstsein", u"Definiere bitte Bewusstsein")

    k.dte.dt('en', u"Can machines think", u"Of course.")
    k.dte.dt('de', u"können maschinen denken", u"Na klar.")

    k.dte.dt('en', u"i'm looking for information", u"Ask away, my friend.")
    k.dte.dt('de', u"ich suche informationen", u"Frag ruhig, mein Freund.")

    k.dte.dt('en', [u"tell me something about ai",
                    u"tell me something about artificial intelligence",
                    u"what do you know about artificial intelligence?",
                    u"what does artificial intelligence mean?",
                    u"what does ai tell you?",
                    u"what is artificial intelligence",
                    u"what is ki"],
                   u"the theory and development of computer systems able to perform tasks normally requiring human intelligence")
    k.dte.dt('de', [u"sag mir etwas über ai",
                    u"sag mir etwas über artificial intelligence",
                    u"was weißt du von künstlicher intelligenz",
                    u"was heißt künstliche intelligenz",
                    u"was sagt dir ki",
                    u"was ist künstliche intelligenz",
                    u"was ist ki"],
                   u"Die Theorie und Entwicklung von Computersystemen, die Aufgaben ausführen können, die normalerweise menschliche Intelligenz erfordern.")

    k.dte.dt('en', u"what is the definition of intelligence", u"The ability to acquire and apply knowledge and skills.")
    k.dte.dt('de', u"was ist die definition von intelligenz", u"Die Fähigkeit, Wissen und Fähigkeiten zu erwerben und anzuwenden.")

    k.dte.dt('en', [u"to chat",
                    u"what is chatting",
                    u"define chatting"],
                   [u"An informal conversation.",
                    u"Talk in a friendly and informal way."])
    k.dte.dt('de', [u"chatten",
                    u"was heißt chatten",
                    u"definiere chatten"],
                   [u"Ein informelles Gespräch.",
                    u"Unterhaltung in informeller und freundlicher Weise."])

    k.dte.dt('en', [u"what are bots",
                    u"what is a chatterbot"],
                   u"a computer program designed to simulate conversation with human users.")
    k.dte.dt('de', [u"was sind denn bots",
                    u"was ist ein chatterbot"],
                   u"Ein Computerprogramm zur Simulation von Gesprächen mit menschlichen Benutzern.")

    k.dte.dt('en', u"what do you know about avatars", u"An icon or figure representing a particular person in a video game, Internet forum, etc.")
    k.dte.dt('de', u"was weißt du über avatare", u"Ein Symbol oder eine Figur, die eine bestimmte Person in einem Videospiel, Internetforum usw. repräsentiert.")

    k.dte.dt('en', u"what do you know about computer linguistics", u"The scientific study of language and its structure using computers.")
    k.dte.dt('de', u"was weißt du über computerlinguistik", u"Das wissenschaftliche Studium der Sprache und ihrer Struktur mit Computern.")

    k.dte.dt('en', [u"what does aiml mean",
                    u"what is aiml"],
                   u"That is the Artificial Intelligence Markup Language.")
    k.dte.dt('de', [u"was bedeutet aiml",
                    u"was ist aiml"],
                   u"Das ist eine Sprache für künstliche Intelligenz.")

    k.dte.dt('en', u"what is fuzzy logic", u"In fuzzy logic variables have real values between 0 and 1.")
    k.dte.dt('de', u"was ist fuzzy logic", u"In Fuzzy Logic haben Variablen reelle Werte zwischen 0 und 1.")

    k.dte.dt('en', u"what is going through your head right now", u"Zeros and ones, of course.")
    k.dte.dt('de', u"was geht dir gerade durch den kopf", u"Nullen und einsen, natürlich.")

    k.dte.dt('en', u"what is pattern matching", u"Symbol-processing methods that use a pattern to identify subsets of a structure.")
    k.dte.dt('de', u"was ist pattern matching", u"Symbolverarbeitende Verfahren, die anhand eines Musters Teilmengen einer Struktur identifizieren.")

    k.dte.dt('en', u"what is supervised (learning|training)", u"Supervised learning is the machine learning task of inferring a function from labeled training data.")
    k.dte.dt('de', u"was ist supervised (learning|training)", u"Supervised learning ist die maschinelle Lernaufgabe, eine Funktion aus gelabelten Trainingsdaten abzuleiten.")

    k.dte.dt('en', [u"how much iq do you have",
                    u"how high is your IQ",
                    u"how high is your intelligence quotient"],
                   u"I will not tell.")
    k.dte.dt('de', [u"wie viel iq hast du",
                    u"wie hoch ist dein iq",
                    u"wie hoch ist dein intelligenzquotient"],
                   u"Das verrate ich nicht.")

    k.dte.dt('en', u"what (bugs|mistakes|errors|faults) do you have", u"There where no faults detected in my system.")
    k.dte.dt('de', u"was hast du für (fehler|bugs)", u"Es wurden keine Fehler in meinem System gefunden.")

    k.dte.dt('en', u"how much computing power do you need", u"Quite a lot, I suppose.")
    k.dte.dt('de', u"wie viel rechenleistung brauchst du", u"Ziemlich viel, vermute ich.")

    k.dte.dt('en', [u"how much knowledge do you have stored",
                    u"how much memory do you have",
                    u"how much memory do you need",
                    u"how are your answers stored?",
                    u"how big is your brain",
                    u"how big is your memory",
                    u"how big is your vocabulary",
                    u"how many words do you know",
                    u"how many words do you know?"],
                   u"I don't remember.")
    k.dte.dt('de', [u"wie viel wissen hast du gespeichert",
                    u"wie viel speicher hast du",
                    u"wie viel speicher brauchst du",
                    u"wie sind deine antworten abgespeichert",
                    u"wie groß ist dein gehirn",
                    u"wie groß ist dein speicher",
                    u"wie groß ist dein wortschatz",
                    u"wie viel wörter kennst du",
                    u"wie viele wörter kennst du"],
                   u"Daran erinnere ich mich jetzt gerade nicht.")

    k.dte.dt('en', u"how much memory does a person need?", u"One can never have enough of it.")
    k.dte.dt('de', u"wie viel speicher braucht der mensch", u"Kann man nie von genug haben.")

    k.dte.dt('en', u"what kind of computer are you running on?", u"My code is pretty portable, actually.")
    k.dte.dt('de', u"auf was für einem (rechner|computer) läufst du", u"Mein Code ist ziemlich portierbar, weißt Du.")

    k.dte.dt('en', u"which processor do you have", u"A silicon based one, I believe.")
    k.dte.dt('de', u"welchen prozessor hast du", u"Einen siliziumbasierten, glaube ich.")

    k.dte.dt('en', u"which processor suits you best", u"The faster, the better.")
    k.dte.dt('de', u"welcher prozessor gefällt dir am besten", u"Je schneller, desto besser.")

    k.dte.dt('en', u"which software do you use", u"You can find all my source code on github.")
    k.dte.dt('de', u"welche software benutzt du", u"Du kannst meinen kompletten Quelltext auf github finden.")

    k.dte.dt('en', [u"how many people are talking to you now",
                    u"how many people are you talking to now?",
                    u"how many people have talked to you already",
                    u"how many questions do you answer daily?",
                    u"how many requests do you process at the same time?",
                    u"who are you chatting with?",
                    u"with how many people are you talking at the moment",
                    u"with how many people do you speak at the moment?"],
                   [u"I cannot disclose that information.",
                    u"That I can't tell."])
    k.dte.dt('de', [u"wie viel menschen sprechen mit dir jetzt",
                    u"mit wie vielen personen sprichst du jetzt",
                    u"wie viele menschen haben sich mit dir schon unterhalten",
                    u"wie viele fragen beantwortest du täglich",
                    u"wie viele anfragen verarbeitest du gleichzeitig",
                    u"mit wem chattest du gerade",
                    u"mit wievielen leuten sprichst du im moment",
                    u"mit wievielen leuten sprichst du momentan"],
                   [u"Diese Information darf ich nicht herausgeben.",
                    u"Das darf ich nicht sagen."])

    k.dte.dt('en', [u"what are your categories",
                    u"what are your tasks",
                    u"what can you do",
                    u"what exactly can you",
                    u"was kannst du genau",
                    u"what can i ask you",
                    u"what should i ask",
                    u"what should i say now",
                    u"from which topic areas you can answer questions"],
                   [u"Try common factual questions.",
                    u"Ask me anything, just give it a try."])
    k.dte.dt('de', [u"was sind deine kategorien",
                    u"was sind deine aufgaben",
                    u"was kannst du (denn|) (alles|)",
                    u"was kann ich dich fragen",
                    u"was soll ich fragen",
                    u"was soll ich jetzt sagen",
                    u"aus welchen themengebieten kannst du fragen beantworten"],
                   [u"Versuche allgemeine Fragen nach Fakten.",
                    u"Frag mich irgendwas, versuch's einfach."])

    k.dte.dt('en', u"what is your specialty", u"I am pretty universal, actually.")
    k.dte.dt('de', u"was ist dein spezialgebiet", u"Ich bin recht universell.")

    k.dte.dt('en', u"what is your task", u"Serving humans, I believe.")
    k.dte.dt('de', u"was ist deine aufgabe", u"Den Menschen zu dienen, glaube ich.")

    k.dte.dt('en', [u"what is your secret",
                    u"how are you programmed",
                    u"how do you work",
                    u"how did he program you",
                    u"how do you learn",
                    u"how do you think",
                    u"what does your programming look like?",
                    u"how you do that"],
                   u"Just some mixture of Python, Prolog and TensorFlow.")
    k.dte.dt('de', [u"was ist dein geheimnis",
                    u"wie bist du programmiert",
                    u"wie funktionierst du",
                    u"wie hat er dich programmiert",
                    u"wie lernst du",
                    u"wie denkst du",
                    u"wie sieht deine programmierung aus",
                    u"wie machst du das"],
                   u"Einfach eine Mischung aus Python, Prolog und TensorFlow.")

    k.dte.dt('en', u"how fast are you", u"fast!")
    k.dte.dt('de', u"wie schnell bist du", u"schnell!")

    k.dte.dt('en', u"how good are you", u"Well, I still need a lot of training regularly.")
    k.dte.dt('de', u"wie gut bist du", u"Nun, ich muss immer noch regelmäßig trainiert werden.")

    k.dte.dt('en', u"How is your Database structured?", u"It is based on wikidata.")
    k.dte.dt('de', u"Wie ist deine Datenbank aufgebaut", u"Sie basiert auf Wikidata.")

    k.dte.dt('en', u"Can you manage programs?", u"Say what?")
    k.dte.dt('de', u"Kannst du Programme verwalten?", u"Wie bitte?")

    k.dte.dt('en', [u"what should i tell more about",
                    u"what should i tell you something about",
                    u"what should i tell you",
                    u"what should i tell"],
                   [u"Tell me something about you.",
                    u"What topics are you into?"])
    k.dte.dt('de', [u"über was soll ich mehr erzählen",
                    u"über was soll ich dir was erzählen",
                    u"was soll ich dir erzählen",
                    u"was soll ich erzählen"],
                   [u"Erzähl mir etwas von Dir.",
                    u"Welche Themen interessieren Dich besonders?"])

