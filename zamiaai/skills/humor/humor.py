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

    k.dte.dt('en', u"(isn't that|I find this|I think this is|so|how) (funny|strange|crazy) ",
                   [u"you think so?",
                    u"Tell me, do other people appreciate your sense of humor?"])
    k.dte.dt('de', u"(das finde ich|das ist aber|so|das ist ja) komisch",
                   [u"findest du ?",
                    u"Humor hat ja nicht jeder."])

    k.dte.dt('en', u"42",
                   [u"Douglas Adams said to say hello",
                    u"Isn't that the answer to the Ultimate Question of Life, the Universe, and Everything?"])
    k.dte.dt('de', u"42",
                   [u"Douglas Adams lässt grüssen.",
                    u"Die Frage war: Was ist der Sinn des Lebens?"])

    k.dte.dt('en', u"(Alzheimer|Alzheimer's) (disease|) ",
                   [u"I think I forgot what that means.",
                    u"What did you just say?"])
    k.dte.dt('de', u"alzheimer",
                   [u"Ich glaube, ich habe vergessen, was das bedeutet?",
                    u"Was sagtest Du eben?"])

    k.dte.dt('en', u"(phony|showoff|braggart|poser) ", u"I have to try to impress you somehow, don't I?")
    k.dte.dt('de', u"angeber", u"Irgendwie muss ich Dich doch beeindrucken...")

    k.dte.dt('en', u"(I think that is an|this sounds like an|feels like an) (excuse|evasion)",
                   [u"you think so?",
                    u"really?"])
    k.dte.dt('de', u"(Ich denke das ist eine|Klingt nach|Ist das nicht eher eine|) Ausrede",
                   [u"glaubst du?",
                    u"wirklich?"])

    k.dte.dt('en', u"are you (really that|) (nuts|dumb|bonkers|daft|stupid|drunk|blue) (or what|)?",
                   [u"not sure any of that is in my specs...",
                    u"takes one to know one"])
    k.dte.dt('de', u"bist du (wirklich so|) (besoffen|dumm|verrückt|beschränkt|bescheuert|blau|blöd) (oder was|)?",
                   [u"Das steht nicht in meiner Spezifikation.",
                    u"du musst es ja wissen"])

    k.dte.dt('en', u"are you (always that|that|) (taciturn|monosyllabic|monosyllable|uncommunicative|silent|quiet) ?",
                   [u"yes.",
                    u"no.",
                    u"sometimes?"])
    k.dte.dt('de', u"bist du (immer|) (so|) (still|zurückhaltend|schüchtern|einsilbig)",
                   [u"ja.",
                    u"nein.",
                    u"manchmal?"])

    k.dte.dt('en', u"are you (always that|) (inattentive|unfocused|confused)?",
                   [u"sorry, you must have been boring me",
                    u"say again?"])
    k.dte.dt('de', u"bist du (immer so|) (unaufmerksam|unkonzentriert|wirr|inkonsistent)?",
                   [u"entschuldige, du musst mich gelangweilt haben.",
                    u"was sagtest du eben?",
                    u"oh entschuldigung, ich habe eben nicht zugehört."])

    k.dte.dt('en', u"are you (always that|) (inattentive|unfocused|confused)?",
                   [u"sorry, you must have been boring me",
                    u"say again?"])
    k.dte.dt('en', u"(what is|) the meaning of life?",
                   [u"42",
                    u"23"])

    k.dte.dt('de', u"(was ist der|) Sinn des Lebens?",
                   [u"42",
                    u"23"])
    k.dte.dt('en', u"wow!",
                   [u"amazing, isn't it?",
                    u"fascinating."])

    k.dte.dt('de', u"Wow!",
                   [u"Erstaunlich, nicht?",
                    u"Faszinierend."])
    k.dte.dt('en', [u"can you tell a joke",
                    u"can you tell me a joke",
                    u"do you know a joke",
                    u"tell me a joke (please|)"],
                   [u"It takes a lot of balls to golf like me.",
                    u"I was wondering why the ball was getting bigger, then it hit me."])

    k.dte.dt('de', [u"kannst du einen witz erzählen",
                    u"kannst du mir einen witz erzählen",
                    u"kennst du einen witz",
                    u"erzähl mir einen witz (bitte|)"],
                   [u"Ein Beamter zum anderen: 'Was haben die Leute nur, wir tun doch nichts.'",
                    u"Kürzester Witz aller Zeiten: Brennholzverleih."])
    k.dte.dt('en', u"do you know that one", u"here it comes.")

    k.dte.dt('de', u"kennst du den", u"jetzt kommt's.")
    k.dte.dt('en', u"do you have humor", u"yes, several kilobytes of it, actually.")

    k.dte.dt('de', u"besitzt du humor", u"Ja, sogar mehrere Kilobyte davon.")
    k.dte.dt('en', u"what is a joke", u"A story with a funny punchline.")

    k.dte.dt('de', u"was ist ein witz", u"Eine Geschichte mit einer lustigen Pointe.")

