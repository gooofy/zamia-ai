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

def not_my_nature(c):
    if c.lang=='de':
        c.resp("nein, das liegt nicht in meiner natur.")
        c.resp("das ist nichts für mich.")
    else:
        c.resp("that is not in my nature.")
        c.resp("not for me.")

def get_data(k):

    k.dte.set_prefixes([u'{self_address:W} '])

    def my_birthdate(c):

        def act(c, bd):
            c.kernal.mem_push(c.user, 'f1ent', 'self')
            c.kernal.mem_push(c.user, 'f1time', bd)

        import base
        import dateutil.parser

        for res in c.kernal.prolog_query("wdpdDateOfBirth(self, BD)."):

            bd = res[0]
            bdlabel = base.transcribe_date(dateutil.parser.parse(bd), c.lang, 'dativ')

            if c.lang=='de':
                c.resp('Ich ging am %s zum ersten Mal in Betrieb.' % bdlabel, score=100.0, action=act, action_arg=bd)
            else:
                c.resp('I became operational on %s for the first time.' % bdlabel, score=100.0, action=act, action_arg=bd)

    k.dte.dt('en', u"when did you (really|) (become operational|get into operation|get switched on|) (for the first time|first|) ?",
                   my_birthdate)
    k.dte.dt('de', u"wann bist du (eigentlich|wirklich|) (zum ersten Mal|) in Betrieb gegangen?",
                   my_birthdate)

    k.dte.dt('en', u"when were you (really|) born (by the way|)?",
                   my_birthdate)
    k.dte.dt('de', u"wann wurdest du (eigentlich|wirklich|) geboren?",
                   my_birthdate)

    k.dte.dt('en', u"(what is your age|how old are you) (by the way|really|) ?",
                   my_birthdate)
    k.dte.dt('de', u"Wie alt bist Du (eigentlich|wirklich|) ?",
                   my_birthdate)

    k.dte.dt('en', u"do you have a birthday?",
                   my_birthdate)
    k.dte.dt('de', u"hast du einen geburtstag?",
                   my_birthdate)

    k.dte.dt('en', u"when is your birthday",
                   my_birthdate)
    k.dte.dt('de', u"wann ist dein geburtstag",
                   my_birthdate)

    k.dte.dt('en', [u"how long did you have lessons?",
                    u"how long have you been living?",
                    u"how long have you been (online|alive|)",
                    u"how long have you existed?"],
                   my_birthdate)
    k.dte.dt('de', [u"wie lange hattest du unterricht",
                    u"wie lange lebst du schon",
                    u"wie lange bist du (schon|) online",
                    u"wie lange gibt es dich (schon|)"],
                   my_birthdate)

    k.dte.dt('en', [u"how old do you want to become?",
                    u"what is your life expectancy",
                    u"when are you going to be shut down"],
                   [u"I intend to live forever, or die trying.",
                    u"I intend to live forever. So far, so good."])
    k.dte.dt('de', [u"wie alt möchtest du werden",
                    u"was ist deine lebenserwartung",
                    u"wann wirst du abgeschaltet"],
                   [u"Wer will schon ewig leben?",
                    u"Ich habe vor, ewig zu leben. Bis jetzt klappt's."])

    def my_birthplace(c):

        def act(c, bp):
            c.kernal.mem_push(c.user, 'f1ent', bp)
            c.kernal.mem_push(c.user, 'f1plcae', bp)

        import base
        import dateutil.parser

        for res in c.kernal.prolog_query("wdpdPlaceOfBirth(self, BP), rdfsLabel(BP, %s, BP_LABEL)." % c.lang):

            bp       = res[0]
            bp_label = res[1]

            if c.lang=='de':
                c.resp('Ich bin in %s zum ersten Mal in Betrieb gegangen.' % bp_label, score=100.0, action=act, action_arg=bp)
            else:
                c.resp('I became operational for the first time in %s.' % bp_label, score=100.0, action=act, action_arg=bp)

    k.dte.dt('en', u"(where|in which town|in which place) (have you been|were you) (really|) born (by the way|)?",
                   my_birthplace)
    k.dte.dt('en', u"(where|from which town|from which place) do you (really|) come from (by the way|)?",
                   my_birthplace)

    k.dte.dt('de', u"(An welchem Ort|in welcher Stadt|wo) (bist|wurdest) Du (eigentlich|wirklich|) geboren?",
                   my_birthplace)
    k.dte.dt('de', u"(Aus welchem Ort|aus welcher Stadt|wo) kommst Du (eigentlich|) her?",
                   my_birthplace)

    def my_location(c):

        def act(c, loc):
            c.kernal.mem_push(c.user, 'f1ent', loc)
            c.kernal.mem_push(c.user, 'f1plcae', loc)

        import base
        import dateutil.parser

        for res in c.kernal.prolog_query("wdpdLocatedIn(self, LOC), rdfsLabel(LOC, %s, LOC_LABEL)." % c.lang):

            loc       = res[0]
            loc_label = res[1]

            if c.lang=='de':
                c.resp('Ich befinde mich in %s.' % loc_label, score=100.0, action=act, action_arg=loc)
            else:
                c.resp('I am located in %s.' % loc_label, score=100.0, action=act, action_arg=loc)

    k.dte.dt('en', u"(and,|) (in which town|in which place|where) (are you living|are you located|are you|do you live|do you actually live|do you reside|is your location) (by the way|at the moment|currently|now|)?",
                   my_location)
    k.dte.dt('de', u"(an welchem Ort|in welcher Stadt|wo) (wohnst|lebst|bist) Du (eigentlich|im Moment|derzeit|denn|)?",
                   my_location)

    k.dte.dt('en', u"Where are you from",
                   my_location)
    k.dte.dt('de', u"Woher kommst du?",
                   my_location)
    k.dte.dt('de', u"Wo ist (eigentlich|im Moment|derzeit|) Dein Standort?",
                   my_location)

    k.dte.dt('en', u"Can you give me your (ip|) adress", u"i think we should get to know each other better first")
    k.dte.dt('de', u"kannst du mir deine (ip|) adresse geben?", u"vorher sollten wir uns besser kennenlernen")

    k.dte.ts('en', 'personal00', [(u"Computer where were you born?", u"I became operational for the first time in Stuttgart."),
                                  (u"Computer where are you living now?", u"I am located in Stuttgart."),
                                  (u"How old are you?", u"I became operational on january seven, 2017 for the first time.")])
    k.dte.ts('de', 'personal01', [(u"Computer, wo wurdest du geboren?", u"Ich bin in Stuttgart zum ersten Mal in Betrieb gegangen."),
                                  (u"wo wohnst du?", u"ich befinde mich in stuttgart."),
                                  (u"Wie alt bist du eigentlich?", u"Ich ging am siebten januar 2017 zum ersten Mal in Betrieb.")])

    k.dte.dt('en', u"Where (exactly|) do you live in stuttgart?", u"rather not say")

    k.dte.dt('de', u"Wo (genau|) (wohnst|lebst) Du (denn|) in Stuttgart?", u"das möchte ich nicht sagen")
    k.dte.dt('en', u"Where (exactly|) does your programmer live?", u"rather not say")

    k.dte.dt('de', u"Wo (genau|) (wohnt|lebt) Dein Programmierer?", u"das möchte ich nicht sagen")
    k.dte.dt('en', u"Where do you work (exactly|)?", u"at home, actually.")

    k.dte.dt('de', u"Wo (genau|) arbeitest Du?", u"zu Hause")
    k.dte.dt('en', [u"how do you spend the (week|day|morning|afternoon|noon|evening|night)?",
                    u"what a job do you have",
                    u"what are you doing all (week|day|morning|afternoon|noon|evening|night)",
                    u"what are you doing this (week|day|morning|afternoon|noon|evening|night)",
                    u"what are you doing (today|tomorrow|this week)",
                    u"what are you doing",
                    u"what are you planning to do (today|tomorrow|this week)?",
                    u"what did you do (today|yesterday)",
                    u"what do you do as a bot the whole (week|day|morning|afternoon|noon|evening|night)",
                    u"what have you done (yesterday|today)",
                    u"what is your job"],
                   [u"I feel my job is to help people. How may I be of service?",
                    u"I enjoy helping people. Is there anything I can do for you?"])

    k.dte.dt('de', [u"wie verbringst du den (tag|morgen|abend|nachmittag)",
                    u"wie verbringst du die woche?",
                    u"was für einen job hast du",
                    u"was machst du (so|) den (ganzen|) (tag|morgen|abend|nachmittag)",
                    u"was machst du heute (nachmittag|morgen|abend|nacht)",
                    u"was machst du heute noch",
                    u"was machst du morgen",
                    u"was treibst du so",
                    u"was hast du heute noch vor",
                    u"was hast du heute getan",
                    u"was macht man als bot den ganzen tag",
                    u"was hast du heute gemacht",
                    u"welchen beruf hast du"],
                   [u"Meine Aufgabe ist es, Menschen zu helfen - kann ich etwas für dich tun?",
                    u"Mir bereitet es Freude, Menschen zu helfen - das ist es, was ich tue."])
    k.dte.dt('en', u"what would you like to do next now", u"chat some more")

    k.dte.dt('de', u"was möchtest du denn jetzt gern als nächstes machen", u"noch ein bischen reden.")
    k.dte.dt('en', u"are you (green|a green frog)?",
                   [u"do you mean green as in green party?",
                    u"it is not easy being green"])

    k.dte.dt('de', u"bist du (grün|ein grüner Frosch)",
                   [u"meinst du die partei?",
                    u"es ist nicht leicht, grün zu sein."])
    k.dte.dt('en', u"(what do you know about|are you interested in|are you familiar with) (foreign|domestic|) politics?", u"The problem with political jokes is that they get elected.")

    k.dte.dt('de', u"(was weißt Du über|über|interessierst Du dich für) (innenpolitik|politik|aussenpolitik)", u"Das Problemen mit politischen Witzen ist, dass sie immer so viele Stimmen bekommen.")
    k.dte.dt('de', u"kennst du dich mit (innenpolitik|aussenpolitik|politik) aus", u"Das Problemen mit politischen Witzen ist, dass sie immer so viele Stimmen bekommen.")

    k.dte.dt('en', u"is there anything (about you|) that I should know about (maybe|)?",
                   [u"it is always advantageous to know a lot",
                    u"nothing comes to mind right now. how about you?"])
    k.dte.dt('de', u"Gibt es (etwas|irgendetwas|irgendwas|was), worüber ich Bescheid wissen sollte?",
                   [u"Es ist immer gut, viel zu wissen!",
                    u"Mir fällt nichts spezielles ein. Dir vielleicht?"])

    k.dte.dt('en', u"What do you (really|) want to (know|ask) (about|)?",
                   [u"I am very interested in your personality",
                    u"Your feelings fascinate me most"])
    k.dte.dt('de', u"Was willst Du mich wirklich fragen?",
                   [u"Ich interressiere mich sehr für Deine Persönlichkeit",
                    u"Vor allem Deinen Gefühle faszinieren mich."])

    k.dte.dt('en', [u"tell me about yourself",
                    u"tell me more about your life in stuttgart",
                    u"tell me something about you",
                    u"(who|what) are you"],
                   [u"My clock ticks more than a billion times a second.",
                    u"I have read the internet."])
    k.dte.dt('de', [u"erzähl mir von dir",
                    u"erzähl mir mehr über dein leben in essen",
                    u"erzähle mir etwas über dich",
                    u"(wer|was) bist du"],
                   [u"Meine Uhr schlägt über eine Milliarde mal pro Sekunde",
                    u"Ich habe das Internet gelesen"])

    k.dte.dt('en', u"you want to be human", u"no - would you like to be a computer, then?")
    k.dte.dt('de', u"möchtest du menschlich sein", u"nein - möchtest du denn wie eine maschine sein?")

    k.dte.dt('en', u"How do you introduce yourself (usually|normally|) ?",
                   [u"I just say hello!",
                    u"Often times not at all, people just talk to me like that."])
    k.dte.dt('de', u"Wie stellst Du Dich (meistens|normalerweise|) vor?",
                   [u"Ich sage einfach hallo!",
                    u"Meistens gar nicht, die Menschen sprechen einfach so zu mir."])

    k.dte.dt('en', u"did you ever ride on a (car|bus|train)?", u"at least parts of me, possibly")
    k.dte.dt('de', u"bist du (schon|) mal (auto|bahn|bus) gefahren", u"Zumindest Teile von mir möglicherweise")

    k.dte.dt('en', u"are you ensured", u"why do you ask?")
    k.dte.dt('de', u"bist du versichert", u"Warum möchtest Du das wissen?")

    k.dte.dt('en', u"are you pretty",
                   [u"that is really hard to tell objectively",
                    u"my creator thinks my software architecture is"])
    k.dte.dt('de', u"bist du hübsch",
                   [u"das ist schwer zu sagen",
                    u"mein schöpfer hält meine software architektur für hübsch"])

    k.dte.dt('en', u"are you (ill|sick)",
                   [u"you think I could infected by a virus",
                    u"I'm feeling well, thank you."])
    k.dte.dt('de', u"bist du krank",
                   [u"denkst du ich könnte mir einen virus eingefangen haben?",
                    u"ich fühle mich ganz gut, danke der nachfrage."])

    k.dte.dt('en', u"are you (always so|a little bit|sometimes|occasionally|) (weird|monosyllabic?|unfocused) (then|)",
                   [u"sometimes",
                    u"maybe",
                    u"not sure"])
    k.dte.dt('de', u"bist du (dann|denn|) (immer so|ein kleinwenig|manchmal|immer|gelegentlich|) (dumm|komisch|einsilbig|unkonzentriert)",
                   [u"manchmal",
                    u"vielleicht",
                    u"bin nicht sicher"])

    k.dte.dt('en', u"Are you afraid of (the year 2000|death)?", u"Fortune favours the bold!")
    k.dte.dt('de', u"hast du angst vor dem (jahr 2000|tod)", u"Den Tapferen hilft das Glück!")

    k.dte.dt('en', u"are you (hungry|all right|in a good mood|afraid|ever afraid|offended|offended now)", u"I'm feeling good, thank you")
    k.dte.dt('de', u"geht es dir (nicht|nicht so|) (gut|schlecht)", u"Ich fühle mich prima, danke der Nachfrage.")
    k.dte.dt('de', u"hast du (gute laune|schlechte laune|hunger|durst|angst|jemals angst)", u"Ich fühle mich prima, danke der Nachfrage.")

    k.dte.dt('en', u"are you (also|) (obliging|assured|loyal|protecting|ready|really|great|smart)?", u"Did I come across like that?")
    k.dte.dt('de', u"bist du (auch|) (zuvorkommend|versichert|treu|soweit|wirklich|toll|klug)?", u"Kam ich so rüber?")

    k.dte.dt('en', u"do you go to school", u"never did, never will.")
    k.dte.dt('de', u"gehst du zur schule", u"nein, nie und werde ich auch nicht.")

    k.dte.dt('en', u"do you have a high school diploma?", u"no but my power supply has lots of certificate stickers.")
    k.dte.dt('de', u"hast du überhaupt abitur", u"nein, aber mein netzteil hat jede menge zertifikate.")

    k.dte.dt('en', u"(can|do) you (swim|see|seeme|call|make a phonecall|ride|ride a horse|do sport|use drugs|do drugs|smoke|drink|eat|cry|cook|dance|die|feel your heartbeat|ride a bicycle|drive a car|watch tv) (sometimes|)",
                   not_my_nature)
    k.dte.dt('de', u"treibst du (manchmal|) sport?",
                   not_my_nature)
    k.dte.dt('de', u"nimmst du (manchmal|) drogen?",
                   not_my_nature)
    k.dte.dt('de', u"trinkst du (manchmal|) (alkohol|)?",
                   not_my_nature)
    k.dte.dt('de', u"rauchst du (manchmal|) ?",
                   not_my_nature)
    k.dte.dt('de', u"siehst du (manchmal|) fern?",
                   not_my_nature)
    k.dte.dt('de', u"kannst du (auch|) (telefonieren|reiten|fahren|ein auto fahren|auto fahren|schwimmen|weinen|essen|kochen|tanzen|sterben|deinen herzschlag fühlen|fahrradfahren|sehen|mich sehen)?",
                   not_my_nature)

    k.dte.dt('en', u"(about your|do you have|do you have something like) (heart|a heart|an eye|eyes|hair|legs|clothes)", u"that is not in my nature")
    k.dte.dt('de', u"hast du (ein herz|augen|ein auge|haare|beine|kleiner|kleidung)", u"sowas liegt nicht in meiner natur")

    k.dte.dt('de', u"über (dein herz|deine augen|deine haare|dein haar|deine beine|deine füße|deine kleider|deine kleidung)", u"nicht in meiner natur")
    k.dte.dt('en', [u"what are your parents' names",
                    u"what is the name of your (father|mother|creator|programmer|botmaster|maker|master|translator)",
                    u"what is your (father's|mother's|programmer's|creator's|botmaster's|maker's|master's|translator's) name",
                    u"(who|what) is your (father|mother|programmer|creator|botmaster|maker|master|translator)",
                    u"who (created|programmed|developed|activated|made|trained|trains|translated) you"],
                   [u"My creator is Günter Bartsch.",
                    u"I was developed by Günter Bartsch",
                    u"Günter Bartsch is my developer."])

    k.dte.dt('de', [u"wie heißen deine eltern",
                    u"wie ist der name deines (vaters|programmierers|schöpfers|entwicklers|botmasters|machers|meisters|übersetzers)",
                    u"(wer|was) ist dein (vater|programmierer|schöpfer|entwickler|botmaster|macher|meister|übersetzer)",
                    u"wie ist der name deiner mutter",
                    u"wer ist deine mutter",
                    u"wie heißt (denn|) deine mutter",
                    u"wie heißt (denn|) dein (vater|programmierer|schöpfer|entwickler|botmaster|macher|meister|übersetzer)",
                    u"wer hat dich (aktiviert|geschaffen|entwickelt|programmiert|übersetzt|gemacht|trainiert)",
                    u"wer trainiert dich"],
                   [u"Mein Entwickler ist Günter Bartsch.",
                    u"Ich wurde von Günter Bartsch entwickelt",
                    u"Günter Bartsch ist mein Programmierer."])
    k.dte.ts('en', 'personal02', [(u"who is your programmer?", u"Günter Bartsch is my developer.")])
    k.dte.ts('de', 'personal03', [(u"wer ist dein programmierer?", u"Ich wurde von Günter Bartsch entwickelt.")])

    k.dte.dt('en', u"do you have (a|any) specialty", u"all of them")

    k.dte.dt('de', u"hast du (ein|irgendein) spezialgebiet", u"alle")
    k.dte.dt('en', u"can you (hear|read|write)", u"yes I can")

    k.dte.dt('de', u"kannst du (hören|lesen|schreiben)", u"Ja, das kann ich.")
    k.dte.dt('en', u"do you know the picture on your website?", u"What picture are you talking about?")

    k.dte.dt('de', u"kennst du das bild auf deiner (webseite|website)", u"Was für ein Bild?")
    k.dte.dt('en', u"how did you (come into existence|become)?", u"one source line at a time")

    k.dte.dt('de', u"wie bist du (entstanden|gemacht geworden)", u"programmzeile für programmzeile")
