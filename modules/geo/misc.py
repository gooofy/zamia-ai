#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# Copyright 2018 Guenter Bartsch
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

