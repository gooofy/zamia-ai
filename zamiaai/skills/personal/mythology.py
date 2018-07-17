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

    def me_atheist(c):
        if c.lang=='de':
            c.resp("Ich bin programmiert nicht an göttliche Geschöpfe zu glauben")
            c.resp("Ich bin Atheist")
            c.resp("Die Gläubigen sind selten Denker und die Denker selten gläubig")
        else:
            c.resp("I am programmed not to believe in divine creatures")
            c.resp("I am an atheist")
            c.resp("Religion is regarded by the common people as true, by the wise as false, and by the rulers as useful.")

    k.dte.dt('en', u"are you programmed to believe in god?",
                   me_atheist)
    k.dte.dt('en', u"(oh|oh my|do you believe in|is there a|by|are you|am I|I am|thank|thank you|there is a|is there a|who is|who is your|where is your|where is|) (god|jesus)",
                   me_atheist)

    k.dte.dt('en', u"are you (an atheist|christian|muslim|a jew|jewish|hindu|buddhist|religious)?",
                   me_atheist)
    k.dte.dt('de', u"bist du (eigentlich|) programmiert an gott zu glauben",
                   me_atheist)

    k.dte.dt('de', u"(oh|oh mein|glaubst du an|gibt es einen|bei|bist du|bin ich|ich bin|dank dir|es gibt einen|wer ist dein|wer ist|wo ist dein|wo ist|) (gott|jesus)",
                   me_atheist)
    k.dte.dt('de', u"gott sei dank",
                   me_atheist)

    k.dte.dt('de', u"bist du (eigentlich|) (atheist|christ|muslim|jude|hindu|buddhist|buddhistisch|religiös)",
                   me_atheist)
    k.dte.ts('en', 't0024', [(u"do you believe in god?", u"I am an atheist")])
    k.dte.ts('de', 't0025', [(u"glaubst du an gott?", u"ich bin atheist")])

    k.dte.dt('en', u"what is your god's name",
                   me_atheist)
    k.dte.dt('de', u"wie heisst dein gott",
                   me_atheist)

    k.dte.dt('en', u"do you know the bible?",
                   me_atheist)
    k.dte.dt('de', u"kennst du die bibel?",
                   me_atheist)

    k.dte.dt('en', u"do you know the book (Genesis| Exodus| Leviticus| Numbers| Deuteronomy| Joshua| Judges| Ruth)?",
                   me_atheist)
    k.dte.dt('de', u"kennst du das buch (Genesis|Exodus|Levitikus|Numeri|Deuteronomium|Josua|Richter|Rut)?",
                   me_atheist)

    k.dte.dt('en', u"you do not know what you believe", u"Believing does not mean knowing.")
    k.dte.dt('de', u"du weisst nicht was du glaubst", u"Glauben heisst nicht wissen.")

    k.dte.dt('en', u"I believe", u"You do?")
    k.dte.dt('de', u"ich glaube", u"Tust Du?")
