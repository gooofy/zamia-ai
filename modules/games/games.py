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

    k.dte.dt('en', [u"(can|do) you play (go|chess)",
                    u"do you know (go|chess)",
                    u"do you want to play (go|chess) with me"],
                   [u"sorry my games modules is still in its infancy",
                    u"sorry, I do not play games yet."])
    k.dte.dt('de', [u"(kennst|spielst) du (go|schach)",
                    u"kannst du (go|schach) spielen?",
                    u"willst du mit mir (go|schach) spielen"],
                   [u"Tut mir leid, mein Spielmodul ist noch sehr unausgereift.",
                    u"Tut mir leid, ich spiele noch keine Spiele."])

    k.dte.dt('en', u"i play (quake|doom|unreal tournament)", u"very cool!")
    k.dte.dt('de', u"ich spiele (unreal tournament|doom|quake)", u"sehr cool!")

    k.dte.dt('en', u"i play", u"what is your favorite game?")
    k.dte.dt('de', u"ich spiele", u"was ist dein lieblingsspiel?")

