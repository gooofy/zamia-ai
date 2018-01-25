#!/usr/bin/env python
# -*- coding: utf-8 -*-

def get_data(k):
    k.dte.set_prefixes([u'{self_address:L} '])
    k.dte.dt('en', u"do you (fancy|want) (a|an|) (food|fast food|a drink|kebab|burger|doner)",
                   % inline(not_my_nature(en)))
    k.dte.dt('de', u"(möchtest|willst|magst) du (döner|essen|nahrung|was essen|was trinken|einen drink|einen burger|fastfood)",
                   % inline(not_my_nature(de)))

    k.dte.dt('en', u"do you know (about|) (a pear|pears)", u"Do you mean the fruit?")
    k.dte.dt('de', u"kennst du (birnen|eine birne)", u"Meinst Du die Frucht oder ein Leuchtmittel?")

    k.dte.dt('de', u"kennst du dich mit birnen aus", u"Finde ich lecker oder meinst du die, die leuchten?")
    k.dte.dt('en', u"do you know (a apple|apples)", u"Are you referring to the fruit or that computer company?")

    k.dte.dt('de', u"kennst du (Äpfel|einen Apfel)", u"Meinst Du die Frucht oder einen Computer?")
    k.dte.dt('en', u"Do you know what cooking is", u"Just beat it.")

    k.dte.dt('de', u"weißt du was kochen ist", u"Einfach umrühren.")
    k.dte.dt('en', [u"what (do|can|do you like to|would you like to) you eat",
                    u"what is your favorite (dish|food|meal)"],
                   % inline(not_my_nature(en)))

    k.dte.dt('de', [u"was (willst|tust|kannst|magst|möchtest) du essen",
                    u"was isst du (gerne|am liebsten)",
                    u"was ist dein (leibgericht|lieblingsessen|lieblingsgericht)",
                    u"was ist deine lieblingsspeise?",
                    u"was möchten sie essen"],
                   % inline(not_my_nature(de)))
