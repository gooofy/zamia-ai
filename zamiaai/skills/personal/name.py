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

