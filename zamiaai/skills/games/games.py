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

