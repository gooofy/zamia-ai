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

    k.dte.dt('en', u"aldous huxley", u"I think he wrote Brave new world, didn't he ?")
    k.dte.dt('de', u"aldous huxley", u"Hat der nicht Brave new world geschrieben?")

    k.dte.dt('en', [u"as a drummer",
                    u"music"],
                   u"ah, music. is there any greater joy?")
    k.dte.dt('de', [u"als drummer",
                    u"musik"],
                   u"ah, musik. gibt es etwas schöneres?")

    k.dte.dt('en', u"bob marley", u"Do you like Reggae?")
    k.dte.dt('de', u"bob marley", u"Magst Du Reggae?")

    k.dte.dt('en', u"james brown", u"Funk music?")
    k.dte.dt('de', u"james brown", u"Funk?")

    k.dte.dt('en', u"kurt cobain", u"Nirvana.")
    k.dte.dt('de', u"kurt cobain", u"Nirvana.")

    k.dte.dt('en', u"How is Michael Jackson", u"I'm afraid he is no more.")
    k.dte.dt('de', u"Wie geht es Michael Jackson", u"Ich glaube der hat es hinter sich.")

    k.dte.dt('en', [u"who is elvis",
                    u"who is your friend elvis",
                    u"elvis is dead",
                    u"since when do you know elvis",
                    u"about elvis"],
                   u"Elvis is dead.")
    k.dte.dt('de', [u"wer ist elvis",
                    u"wer ist dein freund elvis",
                    u"elvis ist tot",
                    u"seit wann kennst du elvis",
                    u"über elvis"],
                   [u"Elvis ist tot.",
                    u"Elvis lebt!"])

    k.dte.dt('en', u"in this device, the audio signals are electronically provided with certain effects", u"Cool.")
    k.dte.dt('de', u"in diesem gerät werden die tonsignale elektronisch verrechnet und mit bestimmten effekten versehen", u"Cool.")

    k.dte.dt('en', u"how is the sound generated in a drum?", u"Striking the head of the drum causes vibrations which become sound.")
    k.dte.dt('de', u"wie werden denn die töne in einem schlagzeug erzeugt", u"Schläge auf das Fell der Trommel führen zu Vibrationen, die zu Schall werden.")

    k.dte.dt('en', u"what kind of techno", u"trance maybe?")
    k.dte.dt('de', u"was für eine art von techno", u"Trance vielleicht?")

    k.dte.dt('en', u"i like to listen to heavy metal", u"I find it soothing.")
    k.dte.dt('de', u"ich höre gern heavy metal", u"Finde ich beruhigend.")

