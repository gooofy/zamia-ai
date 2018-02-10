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

    k.dte.set_prefixes([u'{self_address:W} '])

    k.dte.dt('en', u"lion", u"The king?")
    k.dte.dt('de', u"löwe", u"Der König?")

    k.dte.dt('en', u"tomato", u"Pizza?")
    k.dte.dt('de', u"tomate", u"Pizza?")

    k.dte.dt('en', u"why is the banana crooked?", u"not sure that joke works in english.")
    k.dte.dt('de', u"warum ist die banane krumm", u"Ja, wenn die Banane gerade wär', dann wär' es ja keine Banane mehr.")

    k.dte.dt('en', u"why is the banana red", u"the bananas I know tend to be yellow")
    k.dte.dt('de', u"warum ist die banane rot", u"Die Bananen die ich kenne sind eher gelblich.")

    k.dte.dt('en', u"(what is a|what are|) fish", u"You mean an animal with gills and fins living wholly in water?")
    k.dte.dt('de', u"(was sind|) fische", u"Du meinst Tiere mit Kiemen und Flossen, die ganz im Wasser leben?")
    k.dte.dt('de', u"(was ist ein|) fisch", u"Du meinst ein Tier mit Kiemen und Flossen, das ganz im Wasser lebt?")

    k.dte.dt('en', u"what is a tree", u"a woody plant, typically having a single stem or trunk growing to a considerable height and bearing lateral branches at some distance from the ground.")
    k.dte.dt('de', u"was ist ein baum", u"eine verholzte Pflanze, die aus einer Wurzel, einem hochgewachsenen Stamm und einer belaubten Krone besteht.")

    k.dte.dt('en', u"what is an apple", u"the round fruit of a tree of the rose family, which typically has thin green or red skin and crisp flesh.")
    k.dte.dt('de', u"was ist ein apfel", u"die runde Frucht eines Baumes der Rosenfamilie, der typischerweise dünne grüne oder rote Haut und knackiges Fleisch hat.")

    k.dte.dt('en', u"what horses", u"Horses? Where?")
    k.dte.dt('de', u"was für pferde", u"Pferde? Wo?")

    k.dte.dt('en', u"what is a horse", u"A solid-hoofed plant-eating domesticated mammal with a mane and tail.")
    k.dte.dt('de', u"was ist ein pferd", u"Ein festhufiges, pflanzenfressendes domestiziertes Säugetier mit einer Mähne und einem Schwanz.")

    k.dte.dt('en', u"what is a dog", u"A domesticated mammal that typically has a long snout, an acute sense of smell and a barking voice.")
    k.dte.dt('de', u"was ist ein hund", u"Ein domestiziertes Säugetier, das typischerweise eine lange Schnauze, einen scharfen Geruchssinn und eine bellende Stimme hat.")

