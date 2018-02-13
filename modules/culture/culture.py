#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# Copyright 2016, 2017 Guenter Bartsch
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

