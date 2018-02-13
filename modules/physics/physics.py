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

    k.dte.dt('en', u"Do you know anything about dosimetry?", u"What a question!")
    k.dte.dt('de', u"weißt du etwas über dosimetrie?", u"Was für eine Frage!")

    k.dte.dt('en', u"Do you know the relativity theory?", u"You mean the one that has speed limits even for photons?")
    k.dte.dt('de', u"kennst du die relativitätstheorie?", u"Du meinst die mit der Geschwindigkeitsbegrenzung für Photonen?")

    k.dte.dt('en', u"who was albert einstein?", u"You mean the famous theoretical physicist?")
    k.dte.dt('de', u"wer war albert einstein", u"Du meinst den theoretischen Physiker?")

    k.dte.dt('en', u"what does darkness mean?", u"In order for the light to shine so brightly, the darkness must be present.")
    k.dte.dt('de', u"was bedeutet dunkelheit", u"Damit das Licht so hell scheint, muss die Dunkelheit vorhanden sein.")

    k.dte.dt('en', u"why is the sky blue", u"Because of the way the atmosphere interacts with sunlight.")
    k.dte.dt('de', u"warum ist der himmel blau", u"Wegen der Art, wie die Atmosphäre mit Sonnenlicht interagiert.")

    k.dte.dt('en', u"how does (current|electricity) taste", u"I've heard it's quite a strong sensation.")
    k.dte.dt('de', u"wie schmeckt (elektrizität|strom)", u"Ich habe gehört dass es sich um eine intensive Erfahrung handeln soll.")

