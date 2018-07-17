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

