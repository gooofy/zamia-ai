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

