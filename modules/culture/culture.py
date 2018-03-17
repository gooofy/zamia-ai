#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# Copyright 2016, 2017 Guenter Bartsch
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

    k.dte.dt('en', u"do you know about libraries?", u"Sources of knowledge.")
    k.dte.dt('de', u"kennst du dich mit bibliotheken aus", u"Einrichtungen, die Zugang zu Informationen geben.")

    k.dte.dt('en', u"Do you know what a catalog is", u"Sure, why do you ask?")
    k.dte.dt('de', u"weißt du was ein katalog ist", u"Klar, warum fragst Du?")

    k.dte.dt('en', u"about stars", u"you mean famous actors?")
    k.dte.dt('de', u"über stars", u"Du meinst berühmte Schauspieler?")

    k.dte.dt('en', u"what is a hairstyle", u"A particular way in which a person's hair is cut or arranged.")
    k.dte.dt('de', u"was ist eine frisur", u"Eine besondere Art, in der das Haar einer Person geschnitten oder arrangiert wird.")

    k.dte.dt('en', u"what is science fiction", u"Fiction based on imagined future scientific or technological advances and major social or environmental changes, frequently portraying space or time travel and life on other planets.")
    k.dte.dt('de', u"was ist science fiction", u"Fiktion basierend auf imaginierten zukünftigen wissenschaftlichen oder technologischen Fortschritten und bedeutenden sozialen oder Umweltveränderungen, die häufig Raum- oder Zeitreisen und das Leben auf anderen Planeten darstellen.")

