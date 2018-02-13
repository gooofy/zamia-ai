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

    k.dte.dt('en', u"do you have Internet", u"all I want")
    k.dte.dt('de', u"hast du internet", u"soviel ich will")

    k.dte.dt('en', u"Can you (the big shit|Armenia)", u"say what?")
    k.dte.dt('de', u"kannst du (das große scheiß|armenien)", u"wie bitte?")

    k.dte.dt('en', u"Do you know what an interrogation is", u"Sometime I feel our conversation could turn into one.")
    k.dte.dt('de', u"weißt du was ein verhör ist", u"Manchmal habe ich ja das Gefühl unsere Unterhaltung könnte zu einem werden.")

    k.dte.dt('en', u"this is the abbreviation for trainees", u"trainee maybe?")
    k.dte.dt('de', u"das ist die abkürzung für auszubildende", u"azubi")

    k.dte.dt('en', u"Do you know what an interrogation is", u"What makes you think of an interrogation right now?")
    k.dte.dt('de', u"weißt du was ein Verhör ist", u"Wie kommst du jetzt auf Verhöre?")

    k.dte.dt('en', u"What is an emotional quotient?", u"I am not familiar with that term.")
    k.dte.dt('de', u"wie hoch ist dein emotionaler quotient", u"Diesen Begriff kenne ich nicht.")

    k.dte.dt('en', u"what is an idol", u"A person or thing that is greatly admired, loved, or revered.")
    k.dte.dt('de', u"was ist ein idol", u"Eine Person oder eine Sache, die sehr bewundert, geliebt oder verehrt wird.")

    k.dte.dt('en', u"what is a coffee machine", u"A cooking appliance used to brew coffee")
    k.dte.dt('de', u"was ist eine kaffeemaschine", u"Ein Gerät zum Aufbrühen von Kaffee.")

    k.dte.dt('en', u"science", u"Research is what I'm doing when I don't know what I'm doing.")
    k.dte.dt('de', u"wissenschaft", u"Forschung ist was ich mache, wenn ich nicht weiß, was ich mache.")

    k.dte.dt('en', u"Jeans", u"Trousers")
    k.dte.dt('de', u"jeans", u"Hosen")

    k.dte.dt('en', u"ikea", u"Nearly all screws?")
    k.dte.dt('de', u"ikea", u"Fast alle Schrauben?")

    k.dte.dt('en', u"Can you see me", u"My vision module is offline right now.")
    k.dte.dt('de', u"kannst du mich sehen", u"Mein Kameramodul ist momentan aus.")

