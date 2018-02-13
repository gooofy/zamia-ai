#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# Copyright 2018 Guenter Bartsch
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

    k.dte.dt('en', u"(at|in) the (Ocean|Atlantic|Pacific|North Sea|Baltic Sea|Gulf)", u"Holidays?")
    k.dte.dt('de', u"(an|in) (dem|der|) (Ozean|Atlantik|Pazifik|Nordsee|Ostsee|Golf)", u"Urlaub?")

    k.dte.dt('en', u"which is the highest mountain in the world", u"Many say Mount Everest.")
    k.dte.dt('de', u"welches ist der höchste berg der welt", u"Viele sagen der Mount Everest.")

    k.dte.dt('en', u"(at|in) my house", u"Really?")
    k.dte.dt('de', u"(an|in) meinem haus", u"Wirklich?")

    k.dte.dt('en', u"(at|in) everything", u"Everything?")
    k.dte.dt('de', u"(an|in) (alles|allem)", u"Ganz sicher?")

    k.dte.dt('en', u"where can i find one", u"Search and you will find one eventually.")
    k.dte.dt('de', u"wo kann ich (eines|einen|eine) finden", u"Suchet, so werdet ihr finden!")

    k.dte.dt('en', u"where exactly", u"Right there maybe?")
    k.dte.dt('de', u"wo genau", u"Genau da vielleicht?")

    k.dte.dt('en', u"where is the car", u"That is the question!")
    k.dte.dt('de', u"wo ist das auto", u"Das ist hier die Frage!")

    k.dte.dt('en', u"where, then", u"There, then.")
    k.dte.dt('de', u"wo denn", u"Dort vielleicht?")

    k.dte.dt('en', u"Do you know the four heavenly directions?", u"North, south, west and ... how many did you ask for?")
    k.dte.dt('de', u"kennst du die vier himmelsrichtungen", u"Norden, Süden, Westen und ... wie viele wolltest Du wissen?")

    k.dte.dt('en', u"how many continents are there", u"By most standards, there are a maximum of seven continents.")
    k.dte.dt('de', u"wie viele kontinente gibt es", u"Nach den meisten Standards gibt es maximal sieben Kontinente.")

