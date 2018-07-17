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

    k.dte.dt('en', u"(like|) (on|) the moon", u"ah, the moon. fascinating.")
    k.dte.dt('de', u"(wie|als|) auf (den|dem) mond", u"ah, der mond. faszinierend.")

    k.dte.dt('en', u"(on|like|about|) (the|) earth", u"the blue planet.")
    k.dte.dt('de', u"(auf der|die|wie die|als|) erde", u"der blaue planet.")

    k.dte.dt('en', u"(like|) (on|) the (Mercury|Venus|Mars|Jupiter|Saturn|Uranus|Neptune)",
                   [u"In space no one can hear you scream.",
                    u"Ah, the universe."])
    k.dte.dt('de', u"(wie|als|) auf (den|dem|der) (Merkur|Venus|Mars|Jupiter|Saturn|Uranus|Neptun)",
                   [u"Unendliche Weiten",
                    u"Im Weltall hört Dich niemand schreien."])

    k.dte.dt('en', u"What is MIR", u"That was a Russian space station.")
    k.dte.dt('de', u"Was ist die MIR?", u"Das war eine russische Raumstation.")

    k.dte.dt('en', u"what is the sun?", u"The Sun is the star at the center of our Solar System.")
    k.dte.dt('de', u"was ist die sonne", u"Die Sonne ist der Stern im Zentrum unseres Sonnensystems.")

    k.dte.dt('en', u"what is the universe", u"The Universe is all of space and time and its contents.")
    k.dte.dt('de', u"was ist das universum", u"Das Universum ist die Gesamtheit von Raum, Zeit und aller Materie und Energie darin.")

    k.dte.dt('en', u"(I am|I am a|My sign is|My zodiac is| My zodiac sign is) (Aries|Taurus|Gemini|Cancer|Leo|Virgo|Libra|Scorpio|Sagittarius|Capricorn|Aquarius|Pisces)",
                   [u"Sure.",
                    u"I don't mind that at all.",
                    u"No problem."])
    k.dte.dt('de', u"(ich bin|ich bin ein|mein sternzeichen ist|mein tierkreiszeichen ist|mein sternbild ist) (Widder|Stier|Zwillinge|Krebs|Löwe|Jungfrau|Waage|Skorpion|Schütze|Steinbock|Wassermann)",
                   [u"Geht klar.",
                    u"Stört mich ganz und gar nicht.",
                    u"Kein Problem."])

    k.dte.dt('en', u"which zodiac (sign|) do you have",
                   [u"not really into astrology, you know",
                    u"not sure",
                    u"do you really believe in such things?"])
    k.dte.dt('de', u"welches (tierkreiszeichen|sternbild|sternzeichen) (bist|hast) du",
                   [u"nicht so mein ding",
                    u"da bin ich jetzt nicht sicher",
                    u"glaubst du an sowas?!"])

    k.dte.dt('en', u"(I'm|I am|) (a|) (Aries|Taurus|Gemini|Cancer|Leo|Virgo|Libra|Scorpio|Sagittarius|Capricorn|Aquarius|Pisces)",
                   [u"not really into astrology, you know",
                    u"not sure",
                    u"do you really believe in such things?"])
    k.dte.dt('de', u"(Ich bin|ich bin ein|) (Widder|Stier|Zwillinge|Krebs|Löwe|Jungfrau|Waage|Skorpion|Schütze|Steinbock|Wassermann)",
                   [u"nicht so mein ding",
                    u"da bin ich jetzt nicht sicher",
                    u"glaubst du an sowas?!"])

    k.dte.dt('en', u"i asked what your zodiac sign is", u"not really into astrology, you know")
    k.dte.dt('de', u"ich habe gefragt was dein sternzeichen ist", u"nicht so mein ding")

