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

