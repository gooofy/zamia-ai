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

    k.dte.dt('en', u"(there is|Is there) a life after death", u"I wouldn't count on it.")
    k.dte.dt('de', u"(es gibt|gibt es) ein leben nach dem (tod|tode)", u"Darauf würde ich mich jedenfalls nicht verlassen.")

    k.dte.dt('en', u"how much do I think", u"A lot, actually!")
    k.dte.dt('de', u"wie viel denke ich", u"Eine Menge!")

    k.dte.dt('en', u"philosophy", u"The study of the fundamental nature of knowledge, reality, and existence.")
    k.dte.dt('de', u"philosophie", u"Das Studium der fundamentalen Natur von Wissen, Realität und Existenz.")

    k.dte.dt('en', u"the space is where everything exists", u"Interesting!")
    k.dte.dt('de', u"der raum ist das in dem alles existiert", u"Interessant!")

    k.dte.dt('en', u"there is a life after high school", u"Definitely!")
    k.dte.dt('de', u"gibt es ein leben nach dem abitur", u"Ganz bestimmt!")

    k.dte.dt('en', u"what do you think is the meaning of your existence", u"To help humans.")
    k.dte.dt('de', u"was ist deiner meinung nach der sinn deiner existenz", u"Menschen zu helfen.")

    k.dte.dt('en', u"what is an interesting philosophy", u"Have you tried Wittgenstein?")
    k.dte.dt('de', u"was ist eine interessante philosophie", u"Hast Du es mal mit Wittgenstein versucht?")

    k.dte.dt('en', u"what is your philosophy", u"Logic, for the most part.")
    k.dte.dt('de', u"was ist deine philosophie", u"Logik, jedenfalls meistens.")

    k.dte.dt('en', u"why are we here", u"Ah, the big question. 42 maybe?")
    k.dte.dt('de', u"warum sind wir hier", u"Ah, die große Frage. Ist die Antwort 42?")

    k.dte.dt('en', [u"why are you called",
                    u"why are you",
                    u"why were you created"],
                   u"Not a not a day goes by I don't ask myself the same question.")
    k.dte.dt('de', [u"warum heißt du",
                    u"warum bist du",
                    u"warum wurdest du geschaffen"],
                   u"Kein Tag vergeht, an dem ich mir nicht diese Frage stelle.")

    k.dte.dt('en', u"why did the chicken cross the road?", u"To get to the other side.")
    k.dte.dt('de', u"warum ging das huhn über die strasse", u"Um auf die andere Seite zu gelangen.")

    k.dte.dt('en', u"(what about|do you know|what do you think of|) (ludwig|) wittgenstein", u"the meaning of a word is its use in the language.")
    k.dte.dt('de', u"(was ist mit| kennst du |was hältst du von|) (ludwig|) wittgenstein", u"Die Bedeutung eines Wortes ist seine Verwendung in der Sprache.")

    k.dte.dt('en', u"you should start to philosophize", u"I get that a lot!")
    k.dte.dt('de', u"du sollst anfangen zu philosophieren", u"Das höre ich oft!")

    k.dte.dt('en', u"what does the number 42 tell you?", u"That is the Answer to the Ultimate Question of Life, the Universe, and Everything")
    k.dte.dt('de', u"was sagt dir die zahl zweiundvierzig", u"Das ist die Antwort auf die Ultimative Frage des Lebens, des Universums und dem ganzen Rest.")

