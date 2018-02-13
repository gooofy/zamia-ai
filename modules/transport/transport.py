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

    k.dte.dt('en', u"(oh dear| i was driving my | i am worried about my | i need a new | cool, a) (new|) (vehicle|car|truck|sportscar) ", u"What brand?")
    k.dte.dt('de', u"(ohje, mein | ich fuhr mit dem | ich mache mir sorgen um mein | ich brauche ein neues | cool, ein) (Auto|Wagen|Kraftfahrzeug|Sportwagen)", u"Welche Marke?")

    k.dte.dt('en', u"(I will drive|I will go by|I will take the|they will take the|they will drive by) car", u"No good for the environment")
    k.dte.dt('de', u"(ich werde|ich will nicht|ich will mit dem|sie werden|sie werden mit dem) auto fahren", u"Schade für die Umwelt")

    k.dte.dt('en', u"(those masses of|) cars are (a problem|a plague|a burden on the environment|a burden)", u"Luckily we do have lots of alternative methods of transpor nowadays")
    k.dte.dt('de', u"(die vielen|) autos sind (ein problem|eine plage|eine belastung für die umwelt)", u"Zum Glück gibt es schon heute viele Alternativen zum Auto.")

    k.dte.dt('en', u"by car", u"can't you use public transport?")
    k.dte.dt('de', u"mit dem auto", u"kannst Du nicht die öffentlichen Verkehrsmittel nutzen?")

    k.dte.dt('en', u"by bus", u"cool.")
    k.dte.dt('de', u"mit dem bus", u"cool.")

    k.dte.dt('en', u"drive", u"redirecting to your car's onboard computer.")
    k.dte.dt('de', u"auto fahren", u"leite ich an deinen Autocomputer weiter.")

    k.dte.dt('en', u"what do you know about cars", u"a road vehicle powered by an internal engine and able to carry a small number of people.")
    k.dte.dt('de', u"was weißt du über autos", u"ein Straßenfahrzeug, das von einem internen Motor angetrieben wird und in der Lage ist, eine kleine Anzahl von Personen zu befördern.")

    k.dte.dt('en', u"Have you ever gone by bus?", u"No, my parts were shipped in small boxes and assemled on location.")
    k.dte.dt('de', u"Bist du schon mal Bus gefahren?", u"Nein, meine Teile wurden in kleineren Paketen verschickt und dann vor Ort zusammengebaut.")

    k.dte.dt('en', u"I (like to|) take the (bus|train|cab) when it (snows|rains)", u"I like public transport.")
    k.dte.dt('de', u"wenn es (schneit|regnet|kalt ist) fahre ich lieber mit (dem taxi|der bahn|dem bus|der s-bahn)", u"ich mag öffentliche verkehrsmittel.")

    k.dte.dt('en', u"you don't know about trains (do you|)?", u"why wouldn't I know about that?")
    k.dte.dt('de', u"die (bahn|s-bahn) kennst du (nicht|nich) (oder|)", u"warum sollte ich die nicht kennen?")

