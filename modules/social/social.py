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

    k.dte.dt('en', u"(somebody|he|she|my colleague|my boss|my mother|my father|my brother|my sister|my neighbour|my friend|my boyfriend|my girlfriend) told me about you", u"only good things, I hope")
    k.dte.dt('de', u"(jemand|er|sie|mein Kollege|mein Chef|meine Mutter|mein Vater|mein Bruder|meine Schwester|mein Nachbar|mein Freund|meine Freundin) hat mir von dir erzählt", u"nur gutes, hoffe ich?")

    k.dte.dt('en', u"(I love|I like|I want to have|I want|I hate|do you like|do you hate) (kids|children)?", u"Kids are the best!")
    k.dte.dt('de', u"(ich liebe|ich mag|ich hätte gerne|ich will|ich möchte|ich hasse|magst Du|hasst Du) kinder", u"Kinder sind toll!")

    k.dte.dt('en', u"(I think|do you think) (he|she) is looking great", u"isn't that a bit shallow?")
    k.dte.dt('de', u"(ich finde|denkst du|findest du auch) (er|sie|der|die) sieht toll aus", u"ist das nicht eine sehr oberfächliche betrachtungsweise?")

    k.dte.dt('en', u"(I am| now I am | since yesterday I am| then I am) single (again|)",
                   [u"good for you!",
                    u"enjoy your freedom!"])
    k.dte.dt('de', u"(ich bin wieder|jetzt bin ich wieder|seit gestern bin ich|das war ein tolles|gestern hörte ich ein tolles) solo",
                   [u"du fühlst dich befreit, nehme ich an?",
                    u"wie schön für dich!"])

    k.dte.dt('en', [u"(I am|I am so|I want to fall|so) in love (again|)",
                    u"i love a (man|woman)",
                    u"i'm in love",
                    u"love",
                    u"what do you know about love",
                    u"what do you mean by the word love?",
                    u"what do you understand by love",
                    u"what is in love",
                    u"what is love"],
                   u"I find love to be one of the hardest emotions to emulate")
    k.dte.dt('de', [u"ich liebe (einen mann|eine frau)",
                    u"(ich bin|ich bin ja so|ach bin ich|ich wäre so gerne mal wieder|so richtig) verliebt",
                    u"ich bin verliebt",
                    u"liebe",
                    u"was weist du über die liebe",
                    u"was verstehst du unter dem wort liebe",
                    u"was verstehst du unter liebe",
                    u"was ist verliebtheit",
                    u"was ist liebe"],
                   u"Ich finde Liebe eine der am schwierigsten zu emulierenden Emotionen.")

    k.dte.dt('en', u"everyone's to blame", u"for what?")
    k.dte.dt('de', u"alle sind schuld", u"Woran denn?")

    k.dte.dt('en', u"I am (happy|glad|so happy|so glad) to (see|hear from) you", u"same here")
    k.dte.dt('de', u"ich (freue mich|bin froh|bin so froh|bin sehr froh), dich zu (sehen|hören)", u"geht mir genau so")

    k.dte.dt('en', [u"i am lonely",
                    u"i am looking for a nice (boy|girl)",
                    u"i am looking for a (man|woman)",
                    u"how do i get a (man|woman)",
                    u"i am very lonely",
                    u"i'm looking for a (woman|man)"],
                   [u"have you tried dating websites?",
                    u"maybe you should go out more often?"])
    k.dte.dt('de', [u"ich bin einsam",
                    u"ich suche (ein nettes mädchen|einen netten jungen)",
                    u"ich suche (einen mann|eine frau)",
                    u"wie bekomme ich (einen mann|eine frau)",
                    u"ich bin sehr einsam",
                    u"ich suche (eine frau|einen mann)"],
                   [u"hast du es schon mit online dating versucht?",
                    u"vielleicht solltest Du mehr ausgehen?"])

    k.dte.dt('en', u"one who looks like sarah michelle gellar", u"sure")
    k.dte.dt('de', u"einen der aussieht wie sarah michelle gellar", u"geht klar")

    k.dte.dt('en', [u"(my|) children",
                    u"(my|) brother",
                    u"(my|) daughter",
                    u"(my|) father",
                    u"(my|) girlfriend",
                    u"(my|) mother",
                    u"(my|) mum",
                    u"(my|) sister",
                    u"married"],
                   u"ah, family business.")
    k.dte.dt('de', [u"(meine|) kinder",
                    u"(mein|) bruder",
                    u"(meine|) tochter",
                    u"(mein|) vater",
                    u"(meine|) freundin",
                    u"(meine|) mutter",
                    u"(meine|) mami",
                    u"(meine|) schwester",
                    u"verheiratet"],
                   u"ah, Familienangelegenheiten")

    k.dte.dt('en', [u"my friend",
                    u"my friends"],
                   u"what is more important, friends or family?")
    k.dte.dt('de', [u"mein freund",
                    u"meine freunde"],
                   u"Was ist wichtiger, Freunde oder Familie?")

    k.dte.dt('en', [u"what do you know about men",
                    u"what do you know about women"],
                   [u"I tend to find human issues confusing.",
                    u"Everything wikipedia told me."])
    k.dte.dt('de', [u"was weist du über männer",
                    u"was weist du über frauen"],
                   [u"Ich finde so menschliche Themen oft verwirrend.",
                    u"Alles, was mir die Wikipedia verraten hat."])

    k.dte.dt('en', u"(twin|twins)", u"really?")
    k.dte.dt('de', u"(zwilling|zwillinge)", u"wirklich?")

