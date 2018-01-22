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

    k.dte.set_prefixes([u'{self_address:W} '])

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

