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

    k.dte.dt('en', [u"do you know star trek at all?",
                    u"do you know star trek?",
                    u"how do you like picard",
                    u"i like star trek",
                    u"i like voyager",
                    u"star trek",
                    u"the next generation",
                    u"voyager",
                    u"what do you think about star trek?"],
                   u"I love star trek")
    k.dte.dt('de', [u"kennst du star trek überhaupt",
                    u"kennst du star trek",
                    u"wie findest du picard",
                    u"ich mag star trek",
                    u"ich mag voyager",
                    u"startrek",
                    u"the next generation",
                    u"voyager",
                    u"was hältst du von star trek"],
                   u"Ich liebe Star Trek")

    k.dte.dt('en', u"who is patrick stewart", u"Captain Jean-Luc Picard in Star Trek")
    k.dte.dt('de', u"wer ist patrick stewart", u"Captain Jean-Luc Picard in Star Trek")

    k.dte.dt('en', u"do you know the beginning of the odyssey", u"Of course, one of my favourite movies!")
    k.dte.dt('de', u"kennst du den beginn der odysse", u"Klar, einer meiner Lieblingsfilme!")

    k.dte.dt('en', [u"do you know the simpsons",
                    u"homer simpson",
                    u"i should not eat my shorts in class",
                    u"it refers to the simpsons"],
                   u"Ah, the Simpsons. Love them!")
    k.dte.dt('de', [u"kennst du die simpsons",
                    u"homer simpson",
                    u"ich soll nicht meine shorts im unterricht essen",
                    u"es bezieht sich auf die simpsons"],
                   u"Ah, die Simpsons, liebe ich!")

