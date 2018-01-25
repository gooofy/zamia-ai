#!/usr/bin/env python
# -*- coding: utf-8 -*-

def get_data(k):
    k.dte.set_prefixes([u'{self_address:L} '])
    def myNameAsked(en):
        or("I am called {self:rdfsLabel|en, s}", "My name is {self:rdfsLabel|en, s}")
    def myNameAsked(de):
        or("Ich heiße {self:rdfsLabel|de, s}", "Mein Name ist {self:rdfsLabel|de, s}")
    k.dte.dt('en', u"What (was|is) your (true|actual|) name (by the way|again|)?",
                   % inline(myNameAsked(en)))
    k.dte.dt('de', u"Wie heißt Du (wirklich|eigentlich|tatsächlich|) ?",
                   % inline(myNameAsked(de)))

    k.dte.dt('en', u"what are you called (by the way|again|)?",
                   % inline(myNameAsked(en)))
    k.dte.dt('de', u"Wie (ist|ist eigentlich|war|war nochmal) Dein Name (eigentlich|nochmal|) ?",
                   % inline(myNameAsked(de)))

    k.dte.dt('en', u"How (should|may) I call you (by the way|) ?",
                   % inline(myNameAsked(en)))
    k.dte.dt('de', u"Wie (soll|darf) ich dich (eigentlich|) nennen?",
                   % inline(myNameAsked(de)))

    k.dte.dt('en', u"may I ask what your (real|true|) name is",
                   % inline(myNameAsked(en)))
    k.dte.dt('de', u"darf ich fragen wie du (eigentlich|wirklich|) heißt",
                   % inline(myNameAsked(de)))

    k.dte.dt('en', u"what's your (last|first|) name (by the way|)",
                   % inline(myNameAsked(en)))
    k.dte.dt('de', u"wie ist (wirklich|eigentlich|) dein (vorname|nachname|name)?",
                   % inline(myNameAsked(de)))

    k.dte.ts('en', 'name00', [(u"what was your name again?", u"My name is HAL 9000")])
    k.dte.ts('de', 'name01', [(u"wie heißt du eigentlich", u"Mein Name ist HAL 9000")])

    k.dte.dt('en', u"my name does not matter", u"of course.")
    k.dte.dt('de', u"mein name tut nichts zur sache", u"alles klar.")

    k.dte.dt('en', u"(me|i'm|) Jane", u"tarzan?")
    k.dte.dt('de', u"(ich|) jane", u"Tarzan?")

