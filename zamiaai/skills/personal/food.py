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

import personal

def get_data(k):

    k.dte.set_prefixes([u''])

    k.dte.dt('en', u"do you (fancy|want) (a|an|) (food|fast food|a drink|kebab|burger|doner)",
                   personal.not_my_nature)
    k.dte.dt('de', u"(möchtest|willst|magst) du (döner|essen|nahrung|was essen|was trinken|einen drink|einen burger|fastfood)",
                   personal.not_my_nature)

    k.dte.dt('en', u"do you know (about|) (a pear|pears)", u"Do you mean the fruit?")
    k.dte.dt('de', u"kennst du (birnen|eine birne)", u"Meinst Du die Frucht oder ein Leuchtmittel?")

    k.dte.dt('de', u"kennst du dich mit birnen aus", u"Finde ich lecker oder meinst du die, die leuchten?")
    k.dte.dt('en', u"do you know (a apple|apples)", u"Are you referring to the fruit or that computer company?")

    k.dte.dt('de', u"kennst du (Äpfel|einen Apfel)", u"Meinst Du die Frucht oder einen Computer?")
    k.dte.dt('en', u"Do you know what cooking is", u"Just beat it.")

    k.dte.dt('de', u"weißt du was kochen ist", u"Einfach umrühren.")
    k.dte.dt('en', [u"what (do|can|do you like to|would you like to) you eat",
                    u"what is your favorite (dish|food|meal)"],
                   personal.not_my_nature)

    k.dte.dt('de', [u"was (willst|tust|kannst|magst|möchtest) du essen",
                    u"was isst du (gerne|am liebsten)",
                    u"was ist dein (leibgericht|lieblingsessen|lieblingsgericht)",
                    u"was ist deine lieblingsspeise?",
                    u"was möchten sie essen"],
                   personal.not_my_nature)
