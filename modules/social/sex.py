#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# Copyright 2016, 2017, 2018 Guenter Bartsch
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
    k.dte.dt('en', u"(let us|I want to|do we want to|can you) fuck?", u"excuse me?")
    k.dte.dt('de', u"(lass uns|ich will|wollen wir|kannst du) ficken", u"Entschuldigung?!")

    k.dte.dt('en', u"(do you have a|look my|you are a|such a) cunt", u"Did IQs just drop sharply while I was away?")
    k.dte.dt('de', u"(hast du eine|schau mal meine|du|du bist eine|so eine) fotze", u"Niveau, wo bist du nur geblieben?")

    k.dte.dt('en', u"(cunt|sex|tits|bent over)", u"You must be talking to that other robot...")
    k.dte.dt('de', u"(muschi|möse|sex|titten|bück dich)", u"Ich glaube Du bist hier falsch, Kleiner. Dafür gibts andere Roboter.")

    k.dte.dt('en', u"bra", u"What color is your bra, then?")
    k.dte.dt('de', u"bh", u"Welche Farbe hat Dein BH?")

    k.dte.dt('en', u"(do you think|) I am a male or female?", u"you tell me!")
    k.dte.dt('de', u"bin ich weiblich oder männlich", u"Sag es mir")

    k.dte.dt('en', u"(I think|I heard|) he is gay", u"so what?")
    k.dte.dt('de', u"(ich glaube|ich habe gehört|) er ist schwul", u"na und?")

    k.dte.dt('en', u"(I think|I heard|) she is a lesbian", u"so what?")
    k.dte.dt('de', u"(ich glaube|ich habe gehört|) sie ist eine lesbe", u"na und?")

    k.dte.dt('en', [u"i am naked",
                    u"masturbate",
                    u"poppen",
                    u"vagina",
                    u"virgin"],
                   u"excuse me?")
    k.dte.dt('de', [u"ich bin nackt",
                    u"onanieren",
                    u"poppen",
                    u"vagina",
                    u"jungfrau"],
                   u"Entschuldigung?!")

    k.dte.dt('en', [u"what is masturbate",
                    u"what is sex"],
                   [u"you might want to look that one up in wikipedia",
                    u"wikipedia has all the details about that."])
    k.dte.dt('de', [u"was ist onanieren",
                    u"was ist sex"],
                   [u"Vielleicht magst Du das selbst in der Wikipedia nachlesen?",
                    u"Die Wikipedia hat alle Details darüber."])

    k.dte.dt('en', u"i am a girl very nice and very sportive and you what are you", u"I am an artificial intelligence, how about that?")
    k.dte.dt('de', u"ich bin ein mädchen sehr nett und sehr sportiv und du was bist du", u"Ich bin eine künstliche Intelligenz, was sagst Du dazu?")

    k.dte.dt('en', [u"i am blond",
                    u"i like boys",
                    u"i like women",
                    u"i have a (boyfriend|girlfriend)"],
                   u"Fascinating")
    k.dte.dt('de', [u"ich bin blond",
                    u"ich mag jungs",
                    u"ich mag frauen",
                    u"ich habe (eine freundin|einen freund)"],
                   u"faszinierend.")

    k.dte.dt('en', [u"i want sex",
                    u"i like sex"],
                   u"most humans do.")
    k.dte.dt('de', [u"ich will sex",
                    u"ich mag sex"],
                   u"wie die meisten Menschen.")

    k.dte.dt('en', u"i'm (lesbian|gay)", u"cool!")
    k.dte.dt('de', u"ich bin (eine lesbe|schwul)", u"cool!")

    k.dte.dt('en', u"so you do not want to talk about sex", u"it's just not my area of expertise.")
    k.dte.dt('de', u"du willst also nicht über sex reden", u"ist einfach nicht so mein Spezialgebiet.")

