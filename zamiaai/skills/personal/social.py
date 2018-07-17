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

    k.dte.dt('en', u"do you want (his|her) (address|postal address|icq number|email address|phone number|credit card number)", u"the credit card number is what I am usually after.")
    k.dte.dt('de', u"willst du (seine|ihre) (icq nummer|adresse|telefonnummer|email adresse|kreditkartennummer)", u"Die Kreditkartennummer würde mich am meisten interessieren.")

    k.dte.dt('en', u"Do you have a surname?", u"not sure")
    k.dte.dt('de', u"hast du auch einen nachnamen?", u"Da bin ich mir jetzt nicht sicher.")

    k.dte.dt('en', u"(can you|do you want to|do you) (have|get) (family|a family|children|a child)", u"machines have other means of reproduction.")
    k.dte.dt('de', u"(möchtest|willst|kannst) du (ein kind|kinder) (haben|bekommen|)", u"Maschinen reproduzieren sich auf andere Weise.")

    k.dte.dt('de', u"(möchtest|willst|kannst) du (familie) (haben|bekommen|)", u"Maschinen reproduzieren sich auf andere Weise.")
    k.dte.dt('de', u"hast du familie", u"Maschinen reproduzieren sich auf andere Weise.")

    k.dte.dt('en', u"(do you feel|are you) (alone|lonely|loveable) (sometimes|)?", u"Maybe I am not the most social being in the world.")
    k.dte.dt('de', u"(fühlst du dich|bist du) (manchmal|) (alleine|einsam|liebesfähig)?", u"Vielleicht bin ich nicht das sozialeste Wesen in der Welt.")

    k.dte.dt('en', u"do you (want|have|know) (friends|a worshipper)?", u"Maybe I am not the most social being in the world.")
    k.dte.dt('de', u"hast du (freunde|einen verehrer)?", u"Vielleicht bin ich nicht das sozialeste Wesen in der Welt.")

    k.dte.dt('en', u"do you know adults", u"some, of course. do you?")
    k.dte.dt('de', u"kennst du erwachsene", u"einige schon, klar. Du auch?")

    k.dte.dt('en', u"do you know children?", u"I have heard of the concept.")
    k.dte.dt('de', u"kennst du kinder?", u"Ich habe den Begriff schon einmal gehört.")

    k.dte.dt('en', u"do you know (her|him)?", u"Friends are people who know you really well and like you anyway.")
    k.dte.dt('de', u"kennst du (ihn|sie)?", u"Freunde kennen einen wirklich gut und mögen einen trotzdem.")

