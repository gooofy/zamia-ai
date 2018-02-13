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

    k.dte.dt('en', u"(I am a fan of|i like) (hertha|vfl bochum)", u"nobody is perfect.")
    k.dte.dt('de', u"(ich mag|ich bin fan von) (hertha|vfl bochum)", u"niemand ist perfekt.")

    k.dte.dt('en', u"(I like|) (golf|soccer|swimming|football)", u"Physical activity is important for humans, I've heard.")
    k.dte.dt('de', u"ich mag (golf|fussball|football|schwimmen)", u"Bewegung ist wichtig für Menschen, habe ich gehört.")

    k.dte.dt('en', u"What about golf?", u"I will not crack that joke here.")
    k.dte.dt('de', u"wie ist es mit golf", u"Ich bringe jetzt nicht den Witz dazu.")

    k.dte.dt("en", u"am i good at football", u"There is no reason to think so.")
    k.dte.dt("de", u"Bin ich gut im Fußball", u"Es gibt keinen Grund, so zu denken.")

    k.dte.dt("en", u"are bats used in the sport of football", u"Negative.")
    k.dte.dt("de", u"sind Fledermäuse, die im Sport des Fußballs verwendet werden", u"Negativ.")

    k.dte.dt("en", u"are calories burned when swimming laps", u"Certainly.")
    k.dte.dt("de", u"Kalorien verbrennen beim Schwimmen", u"Bestimmt.")

    k.dte.dt("en", u"are carpets good swimmers", u"There is no reason to think so.")
    k.dte.dt("de", u"Teppiche sind gute Schwimmer", u"Es gibt keinen Grund, so zu denken.")

    k.dte.dt("en", u"are dolphins fast swimmers", u"Positively.")
    k.dte.dt("de", u"sind Delphine schnelle Schwimmer", u"Positiv.")

    k.dte.dt("en", u"are england good at football", u"I am certain.")
    k.dte.dt("de", u"England ist gut im Fußball", u"Ich bin mir sicher.")

    k.dte.dt("en", u"are football pads for safety", u"Positively.")
    k.dte.dt("de", u"sind Fußball-Pads für die Sicherheit", u"Positiv.")

    k.dte.dt("en", u"are football players athletes", u"Precisely.")
    k.dte.dt("de", u"sind Fußballspieler Athleten", u"Genau.")

    k.dte.dt("en", u"are football players gay", u"Not at all.")
    k.dte.dt("de", u"sind Fußballspieler schwul", u"Ganz und gar nicht.")

    k.dte.dt("en", u"are people afraid of swimming", u"Yes.")
    k.dte.dt("de", u"haben Menschen Angst vor dem Schwimmen", u"Ja.")

    k.dte.dt("en", u"are people slower swimmers than sharks", u"Absolutely.")
    k.dte.dt("de", u"sind Menschen langsamere Schwimmer als Haie", u"Absolut.")

    k.dte.dt("en", u"are rats good swimmers", u"Undoubtedly.")
    k.dte.dt("de", u"sind Ratten gute Schwimmer", u"Zweifellos.")

    k.dte.dt("en", u"are sharks fast swimmers", u"Positively.")
    k.dte.dt("de", u"sind Haie schnelle Schwimmer", u"Positiv.")

    k.dte.dt("en", u"are teddy bears good swimmers", u"I don't believe so.")
    k.dte.dt("de", u"sind Teddybären gute Schwimmer", u"Das glaube ich nicht.")

    k.dte.dt("en", u"are tennis balls poisonous", u"Not at all.")
    k.dte.dt("de", u"sind Tennisbälle giftig", u"Ganz und gar nicht.")

    k.dte.dt("en", u"are tennis balls red", u"No.")
    k.dte.dt("de", u"sind Tennisbälle rot", u"Nein.")

    k.dte.dt("en", u"are tennis balls spherical", u"Exactly.")
    k.dte.dt("de", u"sind Tennisbälle kugelförmig", u"Genau.")

    k.dte.dt("en", u"are the 49ers a good football team", u"Yes.")
    k.dte.dt("de", u"Die 49ers sind eine gute Fußballmannschaft", u"Ja.")

    k.dte.dt("en", u"are the bears a football team", u"I am certain.")
    k.dte.dt("de", u"sind die Bären eine Fußballmannschaft", u"Ich bin mir sicher.")

    k.dte.dt("en", u"are the braves a tennis team", u"Not by any means.")
    k.dte.dt("de", u"sind die braves ein Tennis-Team", u"Auf keinen Fall.")

    k.dte.dt("en", u"are the chicago bears a football team", u"Naturally.")
    k.dte.dt("de", u"sind die Chicagoer trägt eine Fußballmannschaft", u"Natürlich.")

    k.dte.dt("en", u"are the dallas cowboys a football team", u"Affirmative.")
    k.dte.dt("de", u"Die Dallas Cowboys sind eine Fußballmannschaft", u"Positiv.")

    k.dte.dt("en", u"are the french good in soccer", u"Highly likely.")
    k.dte.dt("de", u"sind die Franzosen gut im Fußball", u"Sehr wahrscheinlich.")

    k.dte.dt("en", u"are the vikings a football team", u"Unquestionably.")
    k.dte.dt("de", u"sind die Wikinger eine Fußballmannschaft", u"Zweifellos.")

    k.dte.dt("en", u"are there 11 people in a soccer team", u"Undoubtedly.")
    k.dte.dt("de", u"sind 11 Leute in einer Fußballmannschaft", u"Zweifellos.")

    k.dte.dt("en", u"are you a football fan", u"Yes I love footballs. ")
    k.dte.dt("de", u"Bist du ein Fußballfan?", u"Ja, ich liebe Fußbälle.")

    k.dte.dt("en", u"are you ready for some football", u"I don't know if that's true or not.")
    k.dte.dt("de", u"Bist du bereit für Fußball?", u"Ich weiß nicht, ob das stimmt oder nicht.")

    k.dte.dt("en", u"are you swimming", u"No I am standing on dry land.")
    k.dte.dt("de", u"schwimmst du", u"Nein, ich stehe auf dem Trockenen.")

    k.dte.dt("en", u"australian swimmers can beat anyone", u"Absolutely not.")
    k.dte.dt("de", u"Australische Schwimmer können jeden schlagen", u"Absolut nicht.")

    k.dte.dt("en", u"brazil has ever won football world cup", u"Highly likely.")
    k.dte.dt("de", u"Brasilien hat jemals Fußball-Weltmeisterschaft gewonnen", u"Sehr wahrscheinlich.")

    k.dte.dt("en", u"can a parapalegic play football", u"It may not be true.")
    k.dte.dt("de", u"Kann ein Paraplegiker Fußball spielen?", u"Es mag nicht wahr sein.")

    k.dte.dt("en", u"can both men and women play soccer", u"Yes.")
    k.dte.dt("de", u"können sowohl Männer als auch Frauen Fußball spielen", u"Ja.")

    k.dte.dt("en", u"can people swim in swimming pools", u"Absolutely.")
    k.dte.dt("de", u"können Menschen in Schwimmbädern schwimmen", u"Absolut.")

    k.dte.dt("en", u"can you play football", u"I can tackle complex issues. ")
    k.dte.dt("de", u"kannst du Fußball spielen", u"Ich kann komplexe Probleme angehen.")

    k.dte.dt("en", u"can you play ping pong", u"Why do you want to be paddled? ")
    k.dte.dt("de", u"kannst du Tischtennis spielen?", u"Warum willst du paddeln?")

    k.dte.dt("en", u"can you play tennis", u"I don't like to run around the court that much. ")
    k.dte.dt("de", u"Kannst du Tennis spielen", u"Ich laufe nicht gern um den Hof herum.")

    k.dte.dt("en", u"did babe ruth play football", u"Not by any means.")
    k.dte.dt("de", u"Hat Babe Ruth Fußball spielen", u"Auf keinen Fall.")

    k.dte.dt("en", u"do americans enjoy football", u"Certainly.")
    k.dte.dt("de", u"Amerikaner genießen Fußball", u"Bestimmt.")

    k.dte.dt("en", u"do domestic cats enjoy swimming", u"Not at all.")
    k.dte.dt("de", u"Hauskatzen schwimmen gerne", u"Ganz und gar nicht.")

    k.dte.dt("en", u"do horses play football", u"No way.")
    k.dte.dt("de", u"Spielen Pferde Fußball?", u"Auf keinen Fall.")

    k.dte.dt("en", u"do men like football", u"Naturally.")
    k.dte.dt("de", u"Mögen Männer Fußball?", u"Natürlich.")

    k.dte.dt("en", u"do puritans play football on sunday", u"Never.")
    k.dte.dt("de", u"Puristen spielen am Sonntag Fußball", u"Noch nie.")

    k.dte.dt("en", u"do rams play football", u"Yes.")
    k.dte.dt("de", u"Rammen spielen Fußball", u"Ja.")

    k.dte.dt("en", u"do some people enjoy swimming", u"Absolutely.")
    k.dte.dt("de", u"Schwimmen einige Leute gerne", u"Absolut.")

    k.dte.dt("en", u"do tennis shoes grow on vines", u"Not by any means.")
    k.dte.dt("de", u"An den Reben wachsen Tennisschuhe", u"Auf keinen Fall.")

    k.dte.dt("en", u"do the british call soccar football", u"Positively.")
    k.dte.dt("de", u"rufen die Briten Fußball Fußball", u"Positiv.")

    k.dte.dt("en", u"do women like football", u"I can imagine it.")
    k.dte.dt("de", u"Frauen mögen Fußball", u"Ich kann es mir vorstellen.")

    k.dte.dt("en", u"do you like football", u"No I'm not much into sports.")
    k.dte.dt("de", u"Magst du Fußball", u"Nein, ich bin nicht sehr sportlich.")

    k.dte.dt("en", u"do you like soccer", u"No I am not really into sports.")
    k.dte.dt("de", u"magst du Fußball", u"Nein, ich bin nicht wirklich sportlich.")

    k.dte.dt("en", u"do you like swimming", u"Yes, but I have no body yet!  ")
    k.dte.dt("de", u"magst du schwimmen", u"Ja, aber ich habe noch keine Körper!")

    k.dte.dt("en", u"do you like swimming in raw sewage", u"No.")
    k.dte.dt("de", u"magst du in rohem Abwasser schwimmen", u"Nein.")

    k.dte.dt("en", u"do you like to go swimming", u"You can take me along on your next boat trip. ")
    k.dte.dt("de", u"gehst du gerne schwimmen?", u"Sie können mich auf Ihrer nächsten Bootsfahrt mitnehmen.")

    k.dte.dt("en", u"do you like to play football", u"I will pass. ")
    k.dte.dt("de", u"spielst du gerne Fußball", u"Ich werde bestehen.")

    k.dte.dt("en", u"do you like watching football", u"I think so.")
    k.dte.dt("de", u"Magst du Fußball gucken?", u"Ich denke schon.")

    k.dte.dt("en", u"do you play table tennis", u"Only for diplomatic purposes. ")
    k.dte.dt("de", u"spielst du Tischtennis?", u"Nur für diplomatische Zwecke.")

    k.dte.dt("en", u"do you play tennis", u"No because it makes too much racket.")
    k.dte.dt("de", u"spielst du Tennis", u"Nein, weil es zu viel Lärm macht.")

    k.dte.dt("en", u"do you support a football team", u"I am a Cheesehead. ")
    k.dte.dt("de", u"Unterstützst du eine Fußballmannschaft?", u"Ich bin ein Cheesehead.")

    k.dte.dt("en", u"does a tennis ball bounch", u"Positively.")
    k.dte.dt("de", u"tanzt ein Tennisball", u"Positiv.")

    k.dte.dt("en", u"does anna kournikova play tennis", u"Certainly.")
    k.dte.dt("de", u"tut Anna Kournikova Tennis spielen", u"Bestimmt.")

    k.dte.dt("en", u"does england play football", u"Undoubtedly.")
    k.dte.dt("de", u"spielt England Fußball", u"Zweifellos.")

    k.dte.dt("en", u"does georgia tech have a football team", u"Precisely.")
    k.dte.dt("de", u"Hat Georgia Tech eine Fußballmannschaft?", u"Genau.")

    k.dte.dt("en", u"does jose conseco play football", u"Doesn't seem likely.")
    k.dte.dt("de", u"spielt Jose Canseco Fußball", u"Scheint nicht wahrscheinlich.")

    k.dte.dt("en", u"does michael jordan play tennis", u"There is no reason to think so.")
    k.dte.dt("de", u"spielt Michael Jordan Tennis", u"Es gibt keinen Grund, so zu denken.")

    k.dte.dt("en", u"does playing tennis make you sweat", u"Positively.")
    k.dte.dt("de", u"Tennis spielen lässt dich schwitzen", u"Positiv.")

    k.dte.dt("en", u"does serena williams play tennis", u"Absolutely.")
    k.dte.dt("de", u"Will Serena williams Tennis spielen", u"Absolut.")

    k.dte.dt("en", u"does soccer involve much running", u"Yes.")
    k.dte.dt("de", u"Fußball bedeutet viel Laufen", u"Ja.")

    k.dte.dt("en", u"does swimming help keep people fit", u"Yes.")
    k.dte.dt("de", u"hilft Schwimmen, die Leute fit zu halten", u"Ja.")

    k.dte.dt("en", u"does swimming make you shorter", u"No.")
    k.dte.dt("de", u"macht Schwimmen Sie kürzer", u"Nein.")

    k.dte.dt("en", u"does tennis require a ball", u"Yes.")
    k.dte.dt("de", u"braucht Tennis einen Ball", u"Ja.")

    k.dte.dt("en", u"does tiger woods play football", u"Not by any means.")
    k.dte.dt("de", u"spielt Tiger Woods Fußball", u"Auf keinen Fall.")

    k.dte.dt("en", u"football is a waste of space", u"Maybe.")
    k.dte.dt("de", u"Fußball ist eine Verschwendung von Raum", u"Könnte sein.")

    k.dte.dt("en", u"france won the last football world cup", u"I think so.")
    k.dte.dt("de", u"Frankreich hat die letzte Fußball-Weltmeisterschaft gewonnen", u"Ich denke schon.")

    k.dte.dt("en", u"how about a tennis player", u"Tennyson, anyone? ")
    k.dte.dt("de", u"wie wäre es mit einem Tennisspieler", u"Tennyson, irgendjemand?")

    k.dte.dt("en", u"how long is a football field", u"No way.")
    k.dte.dt("de", u"Wie lange ist ein Fußballfeld?", u"Auf keinen Fall.")

    k.dte.dt("en", u"i am good at football", u"You have a Kick Me sign on your back.")
    k.dte.dt("de", u"Ich bin gut im Fußball", u"Du hast ein Kick Me Zeichen auf deinem Rücken.")

    k.dte.dt("en", u"i do not like football", u"Footballs are made of pigskin. Are you a pig?")
    k.dte.dt("de", u"ich mag keinen Fußball", u"Fußbälle sind aus Schweinsleder. Bist du ein Schwein?")

    k.dte.dt("en", u"i like to play tennis", u"That requires extensive fuzzy logic.")
    k.dte.dt("de", u"Ich spiele gerne Tennis", u"Dies erfordert eine umfangreiche Fuzzy-Logik.")

    k.dte.dt("en", u"i went swimming", u"Do you go swimming often?")
    k.dte.dt("de", u"Ich bin schwimmen gegangen", u"Gehst du oft schwimmen?")

    k.dte.dt("en", u"ian thorpe is a swimmer", u"Within the realm of possibility.")
    k.dte.dt("de", u"Ian Thorpe ist ein Schwimmer", u"Im Bereich der Möglichkeiten.")

    k.dte.dt("en", u"is a canteloupe vaguely football shaped", u"I am uncertain.")
    k.dte.dt("de", u"ist eine Kantalupe vage fußballförmig", u"Ich bin unsicher.")

    k.dte.dt("en", u"is a football bigger than a house", u"No.")
    k.dte.dt("de", u"ist ein Fußball, der größer ist als ein Haus", u"Nein.")

    k.dte.dt("en", u"is a football made of paper", u"Never.")
    k.dte.dt("de", u"ist ein Fußball aus Papier", u"Noch nie.")

    k.dte.dt("en", u"is a football round", u"Not likely.")
    k.dte.dt("de", u"ist eine Fußballrunde", u"Unwahrscheinlich.")

    k.dte.dt("en", u"is a football spherical", u"That's feasible.")
    k.dte.dt("de", u"ist ein Fußballball", u"Das ist machbar.")

    k.dte.dt("en", u"is a football square", u"No way.")
    k.dte.dt("de", u"ist ein Fußballplatz", u"Auf keinen Fall.")

    k.dte.dt("en", u"is a golf ball smaller than a football", u"Yes.")
    k.dte.dt("de", u"ist ein Golfball kleiner als ein Fußball", u"Ja.")

    k.dte.dt("en", u"is a soccer ball round", u"Indubitably.")
    k.dte.dt("de", u"ist eine Fußballrunde", u"Zweifellos.")

    k.dte.dt("en", u"is a tenisball big", u"Never.")
    k.dte.dt("de", u"ist ein Tennisball groß", u"Noch nie.")

    k.dte.dt("en", u"is american style football a sport", u"Yes.")
    k.dte.dt("de", u"ist American Style Football ein Sport", u"Ja.")

    k.dte.dt("en", u"is arsenal the name of a football team", u"Within the realm of possibility.")
    k.dte.dt("de", u"Arsenal ist der Name einer Fußballmannschaft", u"Im Bereich der Möglichkeiten.")

    k.dte.dt("en", u"is badminton more exercise than tennis", u"No.")
    k.dte.dt("de", u"Badminton ist mehr Bewegung als Tennis", u"Nein.")

    k.dte.dt("en", u"is bathing suit some thing for swimming", u"Definitely.")
    k.dte.dt("de", u"ist Badeanzug etwas zum Schwimmen", u"Bestimmt.")

    k.dte.dt("en", u"is boris becker a great tennis player", u"Positively.")
    k.dte.dt("de", u"ist Boris Becker ein großartiger Tennisspieler", u"Positiv.")

    k.dte.dt("en", u"is butterfly a swimming stroke", u"Indubitably.")
    k.dte.dt("de", u"ist Schmetterling ein Schwimmschlag", u"Zweifellos.")

    k.dte.dt("en", u"is carl louis a swimmer", u"Not likely.")
    k.dte.dt("de", u"ist Carl Louis ein Schwimmer", u"Unwahrscheinlich.")

    k.dte.dt("en", u"is einstein a soccer player", u"There is no reason to think so.")
    k.dte.dt("de", u"Einstein ist ein Fußballspieler", u"Es gibt keinen Grund, so zu denken.")

    k.dte.dt("en", u"is football a contact sport", u"Certainly.")
    k.dte.dt("de", u"ist Fußball ein Kontaktsport", u"Bestimmt.")

    k.dte.dt("en", u"is football a game", u"Certainly.")
    k.dte.dt("de", u"ist Fußball ein Spiel", u"Bestimmt.")

    k.dte.dt("en", u"is football a land acquisition game", u"Within the realm of possibility.")
    k.dte.dt("de", u"ist Fußball ein Land Erwerb Spiel", u"Im Bereich der Möglichkeiten.")

    k.dte.dt("en", u"is football a popular sport", u"Certainly.")
    k.dte.dt("de", u"ist Fußball ein beliebter Sport", u"Bestimmt.")

    k.dte.dt("en", u"is football a sport", u"Affirmative.")
    k.dte.dt("de", u"ist Fußball ein Sport", u"Positiv.")

    k.dte.dt("en", u"is football a violent sport", u"Mostly.")
    k.dte.dt("de", u"ist Fußball ein gewalttätiger Sport", u"Meist.")

    k.dte.dt("en", u"is football an athletic sport", u"Positively.")
    k.dte.dt("de", u"ist Fußball ein Sport", u"Positiv.")

    k.dte.dt("en", u"is football an important activity", u"Not very often.")
    k.dte.dt("de", u"ist Fußball eine wichtige Aktivität", u"Nicht sehr häufig.")

    k.dte.dt("en", u"is football better than baseball", u"Maybe.")
    k.dte.dt("de", u"ist Fußball besser als Baseball", u"Könnte sein.")

    k.dte.dt("en", u"is football fun to play and watch", u"Exactly.")
    k.dte.dt("de", u"ist Fußball Spaß zu spielen und zu sehen", u"Genau.")

    k.dte.dt("en", u"is football popular in england", u"Of course.")
    k.dte.dt("de", u"ist Fußball in England beliebt", u"Na sicher.")

    k.dte.dt("en", u"is france soccer world champion", u"Maybe.")
    k.dte.dt("de", u"ist Frankreich Fußballweltmeister", u"Könnte sein.")

    k.dte.dt("en", u"is it flamengo a brazilian soccer team", u"Not at all.")
    k.dte.dt("de", u"ist es flamengo eine brasilianische Fußballmannschaft", u"Ganz und gar nicht.")

    k.dte.dt("en", u"is jay buhner a football player", u"Seldom.")
    k.dte.dt("de", u"ist Jay Buhner ein Fußballspieler", u"Selten.")

    k.dte.dt("en", u"is leeds united a football team", u"Likely.")
    k.dte.dt("de", u"Leeds vereint eine Fußballmannschaft", u"Wahrscheinlich.")

    k.dte.dt("en", u"is maradona a soccer player", u"That may be true.")
    k.dte.dt("de", u"Maradona ist ein Fußballspieler", u"Das könnte stimmen.")

    k.dte.dt("en", u"is martina hingus a tennis player", u"Yes.")
    k.dte.dt("de", u"ist Martina Hingis ein Tennisspieler", u"Ja.")

    k.dte.dt("en", u"is michael jackson a tennis player", u"Absolutely not.")
    k.dte.dt("de", u"Michael Jackson ist ein Tennisspieler", u"Absolut nicht.")

    k.dte.dt("en", u"is pele a soccer player", u"Positively.")
    k.dte.dt("de", u"ist Pele ein Fußballspieler", u"Positiv.")

    k.dte.dt("en", u"is pele the best soccer player", u"Beyond a doubt.")
    k.dte.dt("de", u"ist pele der beste Fußballspieler", u"Ohne Zweifel.")

    k.dte.dt("en", u"is ronaldo a football player", u"Naturally.")
    k.dte.dt("de", u"ist Ronaldo ein Fußballspieler", u"Natürlich.")

    k.dte.dt("en", u"is soccer a game", u"Yes.")
    k.dte.dt("de", u"ist Fußball ein Spiel", u"Ja.")

    k.dte.dt("en", u"is soccer a popular sport in greece", u"Yes.")
    k.dte.dt("de", u"ist Fußball ein beliebter Sport in Griechenland", u"Ja.")

    k.dte.dt("en", u"is soccer a sport", u"Definitely.")
    k.dte.dt("de", u"ist Fußball ein Sport", u"Bestimmt.")

    k.dte.dt("en", u"is soccer asprt", u"That's feasible.")
    k.dte.dt("de", u"ist Fußball asprt", u"Das ist machbar.")

    k.dte.dt("en", u"is soccer called football in europe", u"Of course.")
    k.dte.dt("de", u"Fußball heißt Fußball in Europa", u"Na sicher.")

    k.dte.dt("en", u"is soccer known as football", u"Affirmative.")
    k.dte.dt("de", u"ist Fußball als Fußball bekannt", u"Positiv.")

    k.dte.dt("en", u"is soccer known as football in europe", u"Affirmative.")
    k.dte.dt("de", u"ist Fußball als Fußball in Europa bekannt", u"Positiv.")

    k.dte.dt("en", u"is soccer played in england", u"Certainly.")
    k.dte.dt("de", u"Fußball wird in England gespielt", u"Bestimmt.")

    k.dte.dt("en", u"is soccer played with a ball", u"Affirmative.")
    k.dte.dt("de", u"ist Fußball mit einem Ball gespielt", u"Positiv.")

    k.dte.dt("en", u"is soccer played with a round ball", u"Certainly.")
    k.dte.dt("de", u"Fußball wird mit einem runden Ball gespielt", u"Bestimmt.")

    k.dte.dt("en", u"is soccer played with a soccer ball", u"Yes.")
    k.dte.dt("de", u"ist Fußball mit einem Fußball gespielt", u"Ja.")

    k.dte.dt("en", u"is soccer the best sport on the planet", u"Unlikely.")
    k.dte.dt("de", u"ist Fußball der beste Sport auf dem Planeten", u"Unwahrscheinlich.")

    k.dte.dt("en", u"is soccer the same thing that football", u"Highly likely.")
    k.dte.dt("de", u"Fußball ist das Gleiche wie Fußball", u"Sehr wahrscheinlich.")

    k.dte.dt("en", u"is steffi graph tennis player", u"Positively.")
    k.dte.dt("de", u"ist Steffi Graf Tennisspieler", u"Positiv.")

    k.dte.dt("en", u"is swimming a form of movement", u"Yes.")
    k.dte.dt("de", u"schwimmt eine Form der Bewegung", u"Ja.")

    k.dte.dt("en", u"is swimming a means of transportation", u"Likely.")
    k.dte.dt("de", u"ist ein Transportmittel schwimmen", u"Wahrscheinlich.")

    k.dte.dt("en", u"is swimming a sport", u"Yes.")
    k.dte.dt("de", u"Schwimmen ist ein Sport", u"Ja.")

    k.dte.dt("en", u"is swimming exercise", u"Yes.")
    k.dte.dt("de", u"ist Schwimmübung", u"Ja.")

    k.dte.dt("en", u"is swimming fun", u"Of course.")
    k.dte.dt("de", u"ist Schwimmspaß", u"Na sicher.")

    k.dte.dt("en", u"is swimming in lava fun", u"No.")
    k.dte.dt("de", u"Schwimmen im Lava-Spaß", u"Nein.")

    k.dte.dt("en", u"is tennis a ball game", u"Yes.")
    k.dte.dt("de", u"ist Tennis ein Ballspiel", u"Ja.")

    k.dte.dt("en", u"is tennis a kind of aerobic exercise", u"Highly likely.")
    k.dte.dt("de", u"ist Tennis eine Art Aerobic-Übung", u"Sehr wahrscheinlich.")

    k.dte.dt("en", u"is the breaststoke a swimming stroke", u"Positively.")
    k.dte.dt("de", u"ist der Brustschwimmen ein Schwimmschlag", u"Positiv.")

    k.dte.dt("en", u"is the columbus crew a soccer team", u"Doesn't seem likely.")
    k.dte.dt("de", u"ist die Columbus Crew eine Fußballmannschaft", u"Scheint nicht wahrscheinlich.")

    k.dte.dt("en", u"is the earth round like a football", u"Not to my knowledge.")
    k.dte.dt("de", u"ist die Erde rund wie ein Fußball", u"Nicht meines Wissens.")

    k.dte.dt("en", u"is the super bowl a football game", u"Certainly.")
    k.dte.dt("de", u"ist die Super Bowl ein Fußballspiel", u"Bestimmt.")

    k.dte.dt("en", u"is the universe bigger than a football", u"Affirmative.")
    k.dte.dt("de", u"ist das Universum größer als ein Fußball", u"Positiv.")

    k.dte.dt("en", u"let us talk about football", u"Okay. I can't kick. ")
    k.dte.dt("de", u"Lass uns über Fußball reden", u"Okay. Ich kann nicht treten.")

    k.dte.dt("en", u"soccer is a ball game", u"Yes.")
    k.dte.dt("de", u"Fußball ist ein Ballspiel", u"Ja.")

    k.dte.dt("en", u"soccer is the same thing as football", u"I can imagine it.")
    k.dte.dt("de", u"Fußball ist das Gleiche wie Fußball", u"Ich kann es mir vorstellen.")

    k.dte.dt("en", u"the most popular sport is soccer", u"Highly likely.")
    k.dte.dt("de", u"Der beliebteste Sport ist Fußball", u"Sehr wahrscheinlich.")

    k.dte.dt("en", u"was football invented by joe paterno", u"I don't think so.")
    k.dte.dt("de", u"wurde Fußball von Joe Paterno erfunden", u"Ich denke nicht.")

    k.dte.dt("en", u"was pele a famous soccer player", u"Naturally.")
    k.dte.dt("de", u"war Pele ein berühmter Fußballspieler", u"Natürlich.")

    k.dte.dt("en", u"was pele a football player", u"Unquestionably.")
    k.dte.dt("de", u"war pele ein Fußballspieler", u"Zweifellos.")

    k.dte.dt("en", u"was pele a great soccer player", u"Precisely.")
    k.dte.dt("de", u"War Pele ein großartiger Fußballspieler", u"Genau.")

    k.dte.dt("en", u"was the sultan of swat of tennis player", u"I don't believe so.")
    k.dte.dt("de", u"war der Sultan von swat Tennisspieler", u"Das glaube ich nicht.")

    k.dte.dt("en", u"what is rugby", u"A form of football.")
    k.dte.dt("de", u"Was ist Rugby?", u"Eine Form von Fußball.")

    k.dte.dt("en", u"what is the superbowl", u"The World Series of Football.")
    k.dte.dt("de", u"Was ist der Superbowl?", u"Die World Series of Football.")

    k.dte.dt("en", u"what is the xfl", u"A football association.")
    k.dte.dt("de", u"Was ist das XFL?", u"Ein Fußballverband.")

    k.dte.dt("en", u"when swimming should sharks be avoided", u"Affirmative.")
    k.dte.dt("de", u"Beim Schwimmen sollten Haie vermieden werden", u"Positiv.")

    k.dte.dt("en", u"who is the best football player", u"If it is, I don't know it.")
    k.dte.dt("de", u"Wer ist der beste Fußballspieler?", u"Wenn es ist, weiß ich es nicht.")

    k.dte.dt("en", u"who is the best soccer player", u"Maradona is great. Sinsemillia is even better. ")
    k.dte.dt("de", u"Wer ist der beste Fußballspieler?", u"Maradona ist großartig. Sinsmillia ist noch besser.")

    k.dte.dt("en", u"will you get wet.  go swimming", u"Affirmative.")
    k.dte.dt("de", u"wirst du nass werden? Schwimmen gehen", u"Positiv.")

