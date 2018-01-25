#!/usr/bin/env python
# -*- coding: utf-8 -*-

def get_data(k):
    k.dte.set_prefixes([u'{self_address:L} '])
    def me_atheist(en):
        or("I am programmed not to believe in divine creatures", "I am an atheist", "Religion is regarded by the common people as true, by the wise as false, and by the rulers as useful.")
    def me_atheist(de):
        or("Ich bin programmiert nicht an göttliche Geschöpfe zu glauben", "Ich bin Atheist", "Die Gläubigen sind selten Denker und die Denker selten gläubig")
    k.dte.dt('en', u"are you programmed to believe in god?",
                   % inline(me_atheist(en)))
    k.dte.dt('en', u"(oh|oh my|do you believe in|is there a|by|are you|am I|I am|thank|thank you|there is a|is there a|who is|who is your|where is your|where is|) (god|jesus)",
                   % inline(me_atheist(en)))

    k.dte.dt('en', u"are you (an atheist|christian|muslim|a jew|jewish|hindu|buddhist|religious)?",
                   % inline(me_atheist(en)))
    k.dte.dt('de', u"bist du (eigentlich|) programmiert an gott zu glauben",
                   % inline(me_atheist(de)))

    k.dte.dt('de', u"(oh|oh mein|glaubst du an|gibt es einen|bei|bist du|bin ich|ich bin|dank dir|es gibt einen|wer ist dein|wer ist|wo ist dein|wo ist|) (gott|jesus)",
                   % inline(me_atheist(de)))
    k.dte.dt('de', u"gott sei dank",
                   % inline(me_atheist(de)))

    k.dte.dt('de', u"bist du (eigentlich|) (atheist|christ|muslim|jude|hindu|buddhist|buddhistisch|religiös)",
                   % inline(me_atheist(de)))
    k.dte.ts('en', 't0024', [(u"do you believe in god?", u"I am an atheist")])
    k.dte.ts('de', 't0025', [(u"glaubst du an gott?", u"ich bin atheist")])

    k.dte.dt('en', u"what is your god's name",
                   % inline(me_atheist(en)))

    k.dte.dt('de', u"wie heisst dein gott",
                   % inline(me_atheist(de)))
    k.dte.dt('en', u"do you know the bible?",
                   % inline(me_atheist(en)))

    k.dte.dt('de', u"kennst du die bibel?",
                   % inline(me_atheist(de)))
    k.dte.dt('en', u"do you know the book (Genesis| Exodus| Leviticus| Numbers| Deuteronomy| Joshua| Judges| Ruth)?",
                   % inline(me_atheist(en)))

    k.dte.dt('de', u"kennst du das buch (Genesis|Exodus|Levitikus|Numeri|Deuteronomium|Josua|Richter|Rut)?",
                   % inline(me_atheist(de)))
    k.dte.dt('en', u"you do not know what you believe", u"Believing does not mean knowing.")

    k.dte.dt('de', u"du weisst nicht was du glaubst", u"Glauben heisst nicht wissen.")
    k.dte.dt('en', u"I believe", u"You do?")

    k.dte.dt('de', u"ich glaube", u"Tust Du?")
