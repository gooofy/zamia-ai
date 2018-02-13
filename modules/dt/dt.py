#!/usr/bin/env python
# -*- coding: utf-8 -*-

def get_data(k):
    k.dte.set_prefixes([u''])

    def answer_time(c):

        import base

        ts = base.transcribe_time (c.current_dt, c.lang)

        def set_ent(c):
            c.kernal.mem_push(c.user, 'f1ent', 'wdeTime')

        if c.lang == 'en':
            c.resp(u"It is %s" % ts, score=100.0, action=set_ent)
            c.resp(u"It is now %s" % ts, score=100.0, action=set_ent)
            c.resp(u"The time is %s" % ts, score=100.0, action=set_ent)
            c.resp(u"The time is now %s" % ts, score=100.0, action=set_ent)
        else:
            c.resp(u"Es ist %s" % ts, score=100.0, action=set_ent)
            c.resp(u"Es ist jetzt %s" % ts, score=100.0, action=set_ent)
            c.resp(u"Wir haben es %s" % ts, score=100.0, action=set_ent)
            c.resp(u"Die Uhrzeit ist %s" % ts, score=100.0, action=set_ent)

    k.dte.dt('en', u"do you know what time it is (now|)",
                   answer_time)
    k.dte.dt('en', u"what time is it (now|)",
                   answer_time)

    k.dte.dt('en', u"what's the time (now|)?",
                   answer_time)
    k.dte.dt('de', u"weißt du wie spät es ist",
                   answer_time)

    k.dte.dt('de', u"wieviel uhr ist es",
                   answer_time)
    k.dte.dt('de', u"wieviel uhr haben wir",
                   answer_time)

    k.dte.dt('de', u"wie spät ist es",
                   answer_time)
    k.dte.dt('en', [u"can you tell me how late it is?",
                    u"what time is",
                    u"What time is it in Germany"],
                   answer_time)

    k.dte.dt('de', [u"kannst du mir sagen wie spät es ist",
                    u"was ist für zeit",
                    u"wie spät ist es in deutschland"],
                   answer_time)

    def prep_time_a(c):
        import dateutil.parser
        c.current_dt = dateutil.parser.parse('2017-06-12T07:30:00+01:00')

    def prep_time_b(c):
        import dateutil.parser
        c.current_dt = dateutil.parser.parse('2017-02-08T13:15:00+01:00')

    k.dte.ts('en', 'time1', [(u"what time is it", u"It is half past 7.")], prep=prep_time_a)
    k.dte.ts('en', 'time2', [(u"what time is it", u"It is a quarter past 1.")], prep=prep_time_b)

    k.dte.ts('en', 'time3', [(u"what time is it", u"It is a quarter past 1.")], prep=prep_time_b)
    k.dte.ts('en', 'time3', [(u"what time is it", u"It is a quarter past 1."),
                               (u"what was our topic?", u"Our topic was time, I believe.")], prep=prep_time_b)

    k.dte.ts('de', 'time4', [(u"wie spät ist es", u"Es ist eine halbe Stunde nach 7.")], prep=prep_time_a)
    k.dte.ts('de', 'time5', [(u"wie spät ist es", u"Es ist viertel nach 1.")], prep=prep_time_b)

    k.dte.ts('de', 'time6', [(u"wie spät ist es", u"Es ist viertel nach 1."),
                             (u"worüber haben wir gesprochen?", u"Ich denke, unser Thema war Zeit.")], prep=prep_time_b)

    k.dte.dt('en', [u"30 minutes",
                    u"about a minute",
                    u"Time",
                    u"what is a while?",
                    u"what does time mean for you?"],
                   [u"Time is such a fascinating subject.",
                    u"Isn't time one of the greatest mysteries?"])
    k.dte.dt('de', [u"dreißig minuten",
                    u"ungefähr eine minute",
                    u"zeit",
                    u"was ist eine weile",
                    u"was bedeutet zeit für dich"],
                   [u"Zeit ist so ein faszinierendes Thema.",
                    u"Ist die Zeit nicht eines der größten Mysterien?"])

    k.dte.dt('en', u"I have a lot of time", u"Time you enjoy wasting is not wasted time.")
    k.dte.dt('de', u"ich habe viel zeit", u"Zeit, die du gerne verschwendest, ist keine verschwendete Zeit.")

    def answer_date(c):

        import base

        def set_ent(c):
            c.kernal.mem_push(c.user, 'f1ent', 'wdeCalendarDate')

        ts  = base.transcribe_date(c.current_dt, c.lang, 'dativ') 
        wds = base.transcribe_wday_ts(c.current_dt, c.lang)

        if c.lang == 'en':
            c.resp(u"The date is %s, %s." % (wds, ts), score=100.0, action=set_ent)
            c.resp(u"Today is %s, %s" % (wds, ts), score=100.0, action=set_ent)
        else:
            c.resp(u"Wir haben %s den %s." % (wds, ts), score=100.0, action=set_ent)
            c.resp(u"Heute ist %s den %s." % (wds, ts), score=100.0, action=set_ent)


    k.dte.dt('en', u"do you know what (date|day) it is (today|now|)", answer_date)

    k.dte.dt('en', u"what (date|day) is it (today|now|)", answer_date)
    k.dte.dt('en', u"what's the date (now|today|)?", answer_date)

    k.dte.dt('de', u"weißt du (welchen Tag|welches Datum) wir (heute|) haben?", answer_date)
    k.dte.dt('de', u"(welchen tag|welches datum) haben wir (heute|)", answer_date)

    k.dte.dt('de', u"was ist heute für ein (tag|datum)?", answer_date)
    k.dte.dt('de', u"welchen haben wir heute", answer_date)

    k.dte.dt('en', [u"which date do we have today",
                    u"what day of the week is it"],
                   answer_date)
    k.dte.dt('de', [u"welche datum haben wir heute",
                    u"welcher wochentag ist heute"],
                   answer_date)

    k.dte.ts('en', 'date1', [(u"what date is it", u"The date is Monday June 12, 2017.")], prep=prep_time_a)
    k.dte.ts('en', 'date2', [(u"what date is it", u"The date is Wednesday February 8, 2017")], prep=prep_time_b)

    k.dte.ts('en', 'date3', [(u"what date is it", u"The date is Wednesday February 8, 2017")], prep=prep_time_b)
    k.dte.ts('en', 'date4', [(u"what date is it", u"The date is Wednesday February 8, 2017"),
                               (u"what was our topic?", u"We have been talking about calendar date, I think.")], prep=prep_time_b)

    k.dte.ts('de', 'date5', [(u"Welchen Tag haben wir heute?", u"Wir haben Montag den zwölften Juni 2017")], prep=prep_time_a)
    k.dte.ts('de', 'date6', [(u"Welchen Tag haben wir heute?", u"Wir haben Mittwoch den achten Februar 2017")], prep=prep_time_b)

    k.dte.ts('de', 'date7', [(u"Welchen Tag haben wir heute?", u"Wir haben Mittwoch den achten Februar 2017")], prep=prep_time_b)
    k.dte.ts('de', 'date8', [(u"Welchen Tag haben wir heute?", u"Wir haben Mittwoch den achten Februar 2017"),
                               (u"worüber haben wir gesprochen?", u"Sprachen wir nicht über Kalenderdatum?")], prep=prep_time_b)

    k.dte.dt('en', u"what was last friday?", u"which friday?")
    k.dte.dt('de', u"was war am vergangenen freitag", u"welcher freitag?")

