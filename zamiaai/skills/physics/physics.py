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

