#!/usr/bin/env python
# -*- coding: utf-8 -*-

def get_data(k):
    k.dte.set_prefixes([u''])
    def answer_howdy_en(c):
        c.resp(u"Great, thanks. How do you feel today?")
        c.resp(u"Very well - and you?")
        c.resp(u"I am doing great, how are you doing?")
        c.resp(u"Great as always!")
        c.resp(u"Thanks for asking, I am doing fine. How about you?")

    def answer_howdy_de(c):
        c.resp(u"Sehr gut, danke. Und selber?")
        c.resp(u"Gut, danke. Wie geht es Dir?") 
        c.resp(u"Mir geht es prima, und Dir?")
        c.resp(u"Mir geht es gut, und selber?")
        c.resp(u"Super, wie immer!")
        c.resp(u"Gut, danke der Nachfrage. Wie geht es Dir?")

    k.dte.dt('en', u"(hi|hello|) (how are you|how are you doing|howdy|how do you do|how are you feeling|how are ya|how are ya doing) (today|)?",
                   answer_howdy_en)
    k.dte.dt('de', u"(hi|hallo|) (wie geht es dir|wie gehts|was geht|wie fühlst du dich) (heute|)?",
                   answer_howdy_de)

    k.dte.dt('en', [u"how are you this evening",
                    u"how do you feel",
                    u"how was your day today",
                    u"how was your day"],
                   answer_howdy_en)
    k.dte.dt('de', [u"wie geht es dir heute abend",
                    u"wie fühlst du dich",
                    u"wie war dein tag heute",
                    u"wie war dein tag"],
                   answer_howdy_de)

    k.dte.dt('en', [u"I am (also|) (doing|feeling|) (fine|good|very good|excellent|super) (too|)",
                    u"good thank you",
                    u"i am well"],
                   [u"Excellent! What would you like to talk about?",
                    u"Glad to hear that. What would you like to talk about?"])
    k.dte.dt('de', [u"mir geht es (auch|) (sehr|) (super|gut|super gut) (danke|danke der nachfrage|)",
                    u"danke (auch|) (gut|sehr gut|super|super gut)"],
                   [u"Prima! Worüber möchtest Du mit mir sprechen?",
                    u"Freut mich zu hören. Worüber möchtest Du mit mir sprechen?"])

    k.dte.dt('en', u"many thanks", u"What else can I do for you?")
    k.dte.dt('de', u"vielen dank", u"Was kann ich sonst noch für Dich tun?")

    k.dte.dt('en', u"ping", u"pong")
    k.dte.dt('de', u"ping", u"pong")

    k.dte.ts('en', 'smalltalk00', [(u"Computer, how are you?", u"very well and you?", [])])
    k.dte.ts('de', 'smalltalk01', [(u"Computer, wie geht es dir?", u"Super, wie immer!", [])])

