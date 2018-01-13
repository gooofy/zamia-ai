#!/usr/bin/env python
# -*- coding: utf-8 -*-

def get_data(k):

    k.dte.set_prefixes([])

    def answer_greeting_att(c):

        def action_attention_on(c):
            c.mem_set(c.realm, 'attention', 'on')

        if c.lang == 'en':
            c.resp(u"Hello!",     action=action_attention_on)
            c.resp(u"Hi!",        action=action_attention_on)
            c.resp(u"Greetings!", action=action_attention_on)
            c.resp(u"Hey!",       action=action_attention_on)
        elif c.lang == 'de':
            c.resp(u"Hallo!",     action=action_attention_on)
            c.resp(u"Hi!",        action=action_attention_on)
            c.resp(u"Grüß Dich!", action=action_attention_on)
            c.resp(u"Hey!",       action=action_attention_on)
        else:
            raise Exception ('sorry, language %s not implemented yet.' % lang)

    k.dte.dt('en', u"ok, {my_forename:W}", answer_greeting_att)
    k.dte.dt('de', u"ok, {my_forename:W}", answer_greeting_att)

    def check_att_on(c):
        assert c.mem_get(c.realm, 'attention') == 'on'

    k.dte.ts('en', 't0010', [(u"ok, computer", u"hello!", check_att_on)])
    k.dte.ts('de', 't0011', [(u"OK, HAL!", u"Hallo!", check_att_on)])

    def answer_greeting(c):
        if c.lang == 'en':
            c.resp("Hello!")
            c.resp("Hi!")
            c.resp("Greetings!")
            c.resp("Hey!")
        elif c.lang == 'de':
            c.resp("Hallo!")
            c.resp("Hi!")
            c.resp("Grüß Dich!")
            c.resp("Hey!")
        else:
            raise Exception ('sorry, language %s not implemented yet.' % lang)

    k.dte.dt('en', u"(greetings| good morning | hello | hallo | hi | good day | morning | good evening | good night | Cooee| Cooey | hi there) {self_address:W}",
                   answer_greeting)
    k.dte.dt('en', u"{self_address:W} (greetings| good morning | hello | hallo | hi | good day | morning | good evening | good night | Cooee| Cooey | hi there)",
                   answer_greeting)

    k.dte.dt('de', u"(grüß dich|guten morgen | hallo | hi | guten tag | tag | morgen | guten abend | gute nacht | huhu) {self_address:W}",
                   answer_greeting)
    k.dte.dt('de', u"{self_address:W} (grüß dich|guten morgen | hallo | hi | guten tag | tag | morgen | guten abend | gute nacht | huhu)",
                   answer_greeting)

    k.dte.dt('en', [u"day",
                    u"g'day",
                    u"here i am",
                    u"hey you",
                    u"hey",
                    u"tach"],
                   answer_greeting)
    k.dte.dt('de', [u"tag",
                    u"tach auch",
                    u"da bin ich wieder",
                    u"hey du",
                    u"hey",
                    u"tach"],
                   answer_greeting)


    def answer_bye(c):
        def action_attention_off(c):
            c.mem_set(c.realm, 'attention', 'off')
        if c.lang == 'en':
            c.resp(u"Bye",           action=action_attention_off)
            c.resp(u"So long",       action=action_attention_off)
            c.resp(u"See you later", action=action_attention_off)
            c.resp(u"Bye for now",   action=action_attention_off)
        elif c.lang == 'de':
            c.resp(u"Ade",           action=action_attention_off)
            c.resp(u"Tschüss",       action=action_attention_off)
            c.resp(u"Bis bald",      action=action_attention_off)
            c.resp(u"Ciao",          action=action_attention_off)
        else:
            raise Exception ('sorry, language %s not implemented yet.' % lang)

    k.dte.dt('en', u"(goodbye | bye | ciao | so long | bye for now | see ya | see you later | till next time) {self_address:W}",
                   answer_bye)
    k.dte.dt('en', u"{self_address:W} (goodbye | bye | ciao | so long | bye for now | see ya | see you later | till next time)",
                   answer_bye)

    k.dte.dt('de', u"(auf wiedersehen | tschüss | ciao | ade | bye | cu | bis bald | bis zum nächsten mal) {self_address:W}",
                   answer_bye)
    k.dte.dt('de', u"{self_address:W} (auf wiedersehen | tschüss | ciao | ade | bye | cu | bis bald | bis zum nächsten mal)",
                   answer_bye)

    k.dte.dt('en', [u"cu later",
                    u"i am going to sleep now",
                    u"i go to bed",
                    u"i have to go now",
                    u"i have to go",
                    u"i will leave you now",
                    u"i'll stop now",
                    u"i'll turn you off now",
                    u"i'm going",
                    u"i'm leaving again now",
                    u"i'm leaving now",
                    u"sleep well",
                    u"take care",
                    u"that's enough",
                    u"until next time",
                    u"we are done"],
                   answer_bye)
    k.dte.dt('de', [u"cu later",
                    u"ich gehe jetzt schlafen",
                    u"ich gehe ins bett",
                    u"ich muss jetzt gehen",
                    u"ich muss gehen",
                    u"ich werde dich jetzt verlassen",
                    u"ich höre jetzt auf",
                    u"ich mach dich jetzt aus",
                    u"ich geh jetzt",
                    u"ich gehe jetzt wieder",
                    u"ich gehe jetzt",
                    u"schlaf gut",
                    u"machs gut",
                    u"das reicht",
                    u"bis zum nächsten mal",
                    u"sind wir fertig"],
                   answer_bye)

    k.dte.ts('en', 't0000', [(u"hi", u"hello!", [])])
    k.dte.ts('de', 't0001', [(u"hi", u"Hallo!", [])])

    k.dte.ts('en', 't0002', [(u"computer hello", u"Hi!", [])])
    k.dte.ts('de', 't0003', [(u"computer hallo", u"Hi!", [])])

    def check_att_off(c):
        assert c.mem_get(c.realm, 'attention') == 'off'

    k.dte.ts('en', 't0004', [(u"bye computer",     u"bye",      check_att_off)]) 
    k.dte.ts('de', 't0005', [(u"Tschüss computer", u"Tschüss!", check_att_off)])

    k.dte.ts('en', 't0006', [(u"bye",  u"so long",  check_att_off)])
    k.dte.ts('de', 't0007', [(u"Ciao", u"Bis bald", check_att_off)])

    k.dte.dt('en', u"(ah|) there you are!", u"Hi there!")
    k.dte.dt('de', u"(ah|) da bist du (ja|)", u"Hallo hallo")

    k.dte.dt('en', [u"but i have no time",
                    u"i'm a bit tired",
                    u"i'm out of time",
                    u"i'm tired",
                    u"leave me alone"],
                   [u"Shall we call it a day?",
                    u"Ok, another time maybe?"])
    k.dte.dt('de', [u"ich habe aber keine zeit",
                    u"ich bin ein bischen müde",
                    u"ich habe keine zeit mehr",
                    u"ich bin müde",
                    u"lass mich in ruhe"],
                   [u"Wollen wir für heute Schluss machen?",
                    u"OK, vielleicht ein andermal?"])

