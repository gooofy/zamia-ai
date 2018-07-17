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

