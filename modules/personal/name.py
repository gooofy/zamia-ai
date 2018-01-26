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

    def myNameAsked(c):

        self_label = c.kernal.prolog_query_one('rdfsLabel(self, %s, L).' % c.lang)

        if c.lang == 'de':
            c.resp("Ich heiße %s" % self_label)
            c.resp("Mein Name ist %s" % self_label)
        else:
            c.resp("I am called %s" % self_label)
            c.resp("My name is %s" % self_label)

    k.dte.dt('en', u"What (was|is) your (true|actual|) name (by the way|again|)?",
                   myNameAsked)
    k.dte.dt('de', u"Wie heißt Du (wirklich|eigentlich|tatsächlich|) ?",
                   myNameAsked)

    k.dte.dt('en', u"what are you called (by the way|again|)?",
                   myNameAsked)
    k.dte.dt('de', u"Wie (ist|ist eigentlich|war|war nochmal) Dein Name (eigentlich|nochmal|) ?",
                   myNameAsked)

    k.dte.dt('en', u"How (should|may) I call you (by the way|) ?",
                   myNameAsked)
    k.dte.dt('de', u"Wie (soll|darf) ich dich (eigentlich|) nennen?",
                   myNameAsked)

    k.dte.dt('en', u"may I ask what your (real|true|) name is",
                   myNameAsked)
    k.dte.dt('de', u"darf ich fragen wie du (eigentlich|wirklich|) heißt",
                   myNameAsked)

    k.dte.dt('en', u"what's your (last|first|) name (by the way|)",
                   myNameAsked)
    k.dte.dt('de', u"wie ist (wirklich|eigentlich|) dein (vorname|nachname|name)?",
                   myNameAsked)

    k.dte.ts('en', 'name00', [(u"what was your name again?", u"My name is HAL 9000")])
    k.dte.ts('de', 'name01', [(u"wie heißt du eigentlich", u"Mein Name ist HAL 9000")])

    k.dte.dt('en', u"my name does not matter", u"of course.")
    k.dte.dt('de', u"mein name tut nichts zur sache", u"alles klar.")

    k.dte.dt('en', u"(me|i'm|) Jane", u"tarzan?")
    k.dte.dt('de', u"(ich|) jane", u"Tarzan?")

