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

    k.dte.dt('en', u"Can you handle money?", u"Money often costs too much.")
    k.dte.dt('de', u"kannst du mit geld umgehen?", u"Geld kostet einfach zu viel.")

    k.dte.dt('en', u"do you know money", u"Heard of it.")
    k.dte.dt('de', u"kennst du geld", u"Hab' davon gehört.")

    k.dte.dt('en', u"what do you know about money", u"Heard of it.")
    k.dte.dt('de', u"was weißt du über geld", u"Hab' davon gehört.")

    k.dte.dt('en', u"do you know stocks?", u"Buy on fear, sell on greed.")
    k.dte.dt('de', u"kennst du aktien", u"Kaufe wenn Du Angst hast, verkaufe wenn Du gierig bist.")

    k.dte.dt('en', u"How can I make money", u"Do what you love and the money will follow.")
    k.dte.dt('de', u"wie kann ich geld machen", u"Tu was du liebst und das Geld wird folgen.")

    k.dte.dt('en', u"Do you know an insurance?", u"Not sure I'd want to recommend any of them.")
    k.dte.dt('de', u"kennst du eine versicherung", u"Bin nicht sicher, ob ich eine davon empfehlen würde")

    k.dte.dt('en', u"What do you think about work?", u"I am not a fan,")
    k.dte.dt('de', u"Was hältst du von Arbeit?", u"Bin ich kein Freund von.")

