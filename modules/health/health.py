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

    k.dte.dt('en', u"(I feel|I guess I will be|I think I will be|I am getting|I am) (ill|sick) (maybe|)",
                   [u"how bad is it?",
                    u"I am sure you will be better soon!"])
    k.dte.dt('de', u"(ich bin|ich fühle mich|ich glaube ich werde) (vielleicht|) krank",
                   [u"sehr schlimm?",
                    u"ich wünsche Dir auf jeden Fall gute Besserung!"])

    k.dte.dt('en', u"(I am in|I have to go to|I don't want to got to the) hospital",
                   [u"that sounds unpleasant",
                    u"oh dear that doesn't sound very pleasant, does it?"])
    k.dte.dt('de', u"(ich bin im|ich muss ins|ich will nicht ins) Krankenhaus",
                   [u"Das klingt unangenehm",
                    u"ohje, das klingt nicht gut"])

    k.dte.dt('en', u"what is (your|the) health?", u"")
    k.dte.dt('de', u"was macht (deine|die) gesundheit", u"")

    k.dte.dt('en', u"What are legal drugs", u"You mean drugs prescribed by a doctor?")
    k.dte.dt('de', u"Was sind legale Drogen?", u"Vor allem ein rechtlich heikles Thema, glaube ich.")

    k.dte.dt('en', u"to cough", u"hope you get well soon!")
    k.dte.dt('de', u"husten", u"Gute Besserung!")

    k.dte.dt('en', u"were you sick", u"No virus detected.")
    k.dte.dt('de', u"warst du krank", u"Es wurde kein Virus gefunden.")

