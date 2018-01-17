#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# Copyright 2018 Guenter Bartsch
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

    def weather_location(LOC):
        owmCityId(LOC, CITYID)

    # NER, macros

    for lang in ['en', 'de']:
        for res in k.prolog_query("owmCityId(LOC, CITYID), rdfsLabel(LOC, %s, LABEL)." % lang):
            s_loc   = res[0] 
            s_label = res[2] 
            k.dte.ner(lang, 'weather_location', s_loc, s_label)
            k.dte.macro(lang, 'weather_location', {'LABEL': s_label})

            print s_loc, s_label


# 
# 
#     def answer_weather_r(C, en, full, LPLACE, LTIMESPAN, "01", PREC, TEMP_MIN, TEMP_MAX, CLOUDS):
#         say(C, "{LTIMESPAN,s} will be clear skies in {LPLACE,s} with temperatures between {TEMP_MIN,d} and {TEMP_MAX,d} degrees.")
#     def answer_weather_r(C, en, full, LPLACE, LTIMESPAN, "02", PREC, TEMP_MIN, TEMP_MAX, CLOUDS):
#         say(C, "{LTIMESPAN,s} will be mostly clear skies in {LPLACE,s} with temperatures between {TEMP_MIN,d} and {TEMP_MAX,d} degrees.")
#     def answer_weather_r(C, en, full, LPLACE, LTIMESPAN, "03", PREC, TEMP_MIN, TEMP_MAX, CLOUDS):
#         say(C, "{LTIMESPAN,s} there will be some clouds in {LPLACE,s} with temperatures between {TEMP_MIN,d} and {TEMP_MAX,d} degrees.")
#     def answer_weather_r(C, en, full, LPLACE, LTIMESPAN, "04", PREC, TEMP_MIN, TEMP_MAX, CLOUDS):
#         say(C, "{LTIMESPAN,s} the sun will show up occasionally in {LPLACE,s} with temperatures between {TEMP_MIN,d} and {TEMP_MAX,d} degrees.")
#     def answer_weather_r(C, en, full, LPLACE, LTIMESPAN, "09", PREC, TEMP_MIN, TEMP_MAX, CLOUDS):
#         say(C, "{LTIMESPAN,s} there will be rain showers of {PREC,d} millimeters in {LPLACE,s} with temperatures between {TEMP_MIN,d} and {TEMP_MAX,d} degrees.")
#     def answer_weather_r(C, en, full, LPLACE, LTIMESPAN, "10", PREC, TEMP_MIN, TEMP_MAX, CLOUDS):
#         and(>=(PREC, 1.0), say(C, "{LTIMESPAN,s} it will rain {PREC,d} millimeters in {LPLACE,s} with temperatures between {TEMP_MIN,d} and {TEMP_MAX,d} degrees."))
#     def answer_weather_r(C, en, full, LPLACE, LTIMESPAN, "10", PREC, TEMP_MIN, TEMP_MAX, CLOUDS):
#         and(<(PREC, 1.0), say(C, "{LTIMESPAN,s} there might be a little rain in {LPLACE,s} with temperatures between {TEMP_MIN,d} and {TEMP_MAX,d} degrees."))
#     def answer_weather_r(C, en, full, LPLACE, LTIMESPAN, "11", PREC, TEMP_MIN, TEMP_MAX, CLOUDS):
#         say(C, "{LTIMESPAN,s} we will have thunderstorms and {PREC,d} millimeters of rain in {LPLACE,s} with temperatures between {TEMP_MIN,d} and {TEMP_MAX,d} degrees.")
#     def answer_weather_r(C, en, full, LPLACE, LTIMESPAN, "13", PREC, TEMP_MIN, TEMP_MAX, CLOUDS):
#         say(C, "{LTIMESPAN,s} it will snow {PREC,d} millimeters in {LPLACE,s} with temperatures between {TEMP_MIN,d} and {TEMP_MAX,d} degrees.")
#     def answer_weather_r(C, en, full, LPLACE, LTIMESPAN, "50", PREC, TEMP_MIN, TEMP_MAX, CLOUDS):
#         say(C, "{LTIMESPAN,s} it will be foggy in {LPLACE,s} with temperatures between {TEMP_MIN,d} and {TEMP_MAX,d} degrees")
#     def answer_weather_r(C, de, full, LPLACE, LTIMESPAN, "01", PREC, TEMP_MIN, TEMP_MAX, CLOUDS):
#         say(C, "{LTIMESPAN,s} wird der Himmel klar sein in {LPLACE,s} und es wird zwischen {TEMP_MIN,d} und {TEMP_MAX,d} Grad warm.")
#     def answer_weather_r(C, de, full, LPLACE, LTIMESPAN, "02", PREC, TEMP_MIN, TEMP_MAX, CLOUDS):
#         say(C, "{LTIMESPAN,s} wird es wenige Wolken geben in {LPLACE,s} und es wird zwischen {TEMP_MIN,d} und {TEMP_MAX,d} Grad warm.")
#     def answer_weather_r(C, de, full, LPLACE, LTIMESPAN, "03", PREC, TEMP_MIN, TEMP_MAX, CLOUDS):
#         say(C, "{LTIMESPAN,s} wird es lockere Wolken geben in {LPLACE,s} und es wird zwischen {TEMP_MIN,d} und {TEMP_MAX,d} Grad warm.")
#     def answer_weather_r(C, de, full, LPLACE, LTIMESPAN, "04", PREC, TEMP_MIN, TEMP_MAX, CLOUDS):
#         say(C, "{LTIMESPAN,s} zeigt sich ab und an die Sonne in {LPLACE,s} und es wird zwischen {TEMP_MIN,d} und {TEMP_MAX,d} Grad warm.")
#     def answer_weather_r(C, de, full, LPLACE, LTIMESPAN, "09", PREC, TEMP_MIN, TEMP_MAX, CLOUDS):
#         say(C, "{LTIMESPAN,s} wird es {PREC,d} Millimeter Schauer geben in {LPLACE,s} und es wird zwischen {TEMP_MIN,d} und {TEMP_MAX,d} Grad warm.")
#     def answer_weather_r(C, de, full, LPLACE, LTIMESPAN, "10", PREC, TEMP_MIN, TEMP_MAX, CLOUDS):
#         and(>=(PREC, 1.0), say(C, "{LTIMESPAN,s} regnet es {PREC,d} Millimeter in {LPLACE,s} und es wird zwischen {TEMP_MIN,d} und {TEMP_MAX,d} Grad warm."))
#     def answer_weather_r(C, de, full, LPLACE, LTIMESPAN, "10", PREC, TEMP_MIN, TEMP_MAX, CLOUDS):
#         and(<(PREC, 1.0), say(C, "{LTIMESPAN,s} kann es etwas Niederschlag geben in {LPLACE,s} und es wird zwischen {TEMP_MIN,d} und {TEMP_MAX,d} Grad warm."))
#     def answer_weather_r(C, de, full, LPLACE, LTIMESPAN, "11", PREC, TEMP_MIN, TEMP_MAX, CLOUDS):
#         say(C, "{LTIMESPAN,s} wird es Gewitter geben mit {PREC,d} Millimeter Niederschlag in {LPLACE,s} und es wird zwischen {TEMP_MIN,d} und {TEMP_MAX,d} Grad warm.")
#     def answer_weather_r(C, de, full, LPLACE, LTIMESPAN, "13", PREC, TEMP_MIN, TEMP_MAX, CLOUDS):
#         say(C, "{LTIMESPAN,s} schneit es {PREC,d} Millimeter in {LPLACE,s} und es wird zwischen {TEMP_MIN,d} und {TEMP_MAX,d} Grad kalt.")
#     def answer_weather_r(C, de, full, LPLACE, LTIMESPAN, "50", PREC, TEMP_MIN, TEMP_MAX, CLOUDS):
#         say(C, "{LTIMESPAN,s} wird es neblich in {LPLACE,s} und es wird zwischen {TEMP_MIN,d} und {TEMP_MAX,d} Grad geben.")

#     def weather_events(PLACE, TSTART, TEND, CODE, PREC, TEMP_MIN, TEMP_MAX, CLOUDS):
#         and(aiLocation(WEV, PLACE), aiDtStart(WEV, TSTART), aiDtEnd(WEV, TEND), aiIcon(WEV, CODE), aiPrecipitation(WEV, PREC), aiTempMin(WEV, TEMP_MIN), aiTempMax(WEV, TEMP_MAX), aiClouds(WEV, CLOUDS))
#     def answer_weather_r(C, LANG, REPORT):
#         and(time_span(C:time, C:mem|f1timespan, TSTART, TEND), weather_data(C:mem|f1loc, TSTART, TEND, CODE, PREC, TEMP_MIN, TEMP_MAX, CLOUDS), rdfsLabel(C:mem|f1loc, LANG, LPLACE), time_label(C:time, LANG, C:mem|f1timespan, LTIMESPAN), r_score(C, 100.0), answer_weather_r(C, LANG, REPORT, LPLACE, LTIMESPAN, CODE, PREC, TEMP_MIN, TEMP_MAX, CLOUDS))
#     def answer_weather_context(en, REPORT):
#         and(or(and(var(C:mem|f1loc), set(C:mem|f1loc, self:wdpdLocatedIn)), and(not(var(C:mem|f1loc)), true)), or(and(var(C:mem|f1timespan), set(C:mem|f1timespan, weatherNearFuture)), and(not(var(C:mem|f1timespan)), true)), set(C:context|topic, wdeWeatherForecast), answer_weather_r(C, en, REPORT))
#     def answer_weather_context(de, REPORT):
#         and(or(and(var(C:mem|f1loc), set(C:mem|f1loc, self:wdpdLocatedIn)), and(not(var(C:mem|f1loc)), true)), or(and(var(C:mem|f1timespan), set(C:mem|f1timespan, weatherNearFuture)), and(not(var(C:mem|f1timespan)), true)), set(C:context|topic, wdeWeatherForecast), answer_weather_r(C, de, REPORT))

    def answer_weather_prec_cloud(c, lts, lte, timespan):

        def act(c, args):
            ts, loc = args
            c.kernal.mem_push(c.user, 'f1ent', 'wdeWeatherForecast')
            c.kernal.mem_push(c.user, 'f1time', ts)
            c.kernal.mem_push(c.user, 'f1loc',  loc)

        import weather

        # import pdb; pdb.set_trace()
        if lts>=0:
            lss = c.ner(c.lang, 'weather_location', lts, lte)
        else:
            lss = c.kernal.mem_get_multi(c.user, 'f1loc')

        if not lss:
            my_location = c.kernal.prolog_query_one('wdpdLocatedIn(self, X).')
            lss = [(my_location, 1.0)]

        if timespan:
            tss = [(timespan, 1.0)]
        else:
            tss = c.kernal.mem_get_multi(c.user, 'f1time')

        if not tss:
            tss = [('weatherNearFuture', 1.0)]

        for loc, lscore in lss:

            llabel = c.kernal.prolog_query_one('rdfsLabel(%s,%s,L).' % (loc, c.lang))
            if not llabel:
                continue

            for ts, tscore in tss:

                tlabel = weather.get_time_label(c, c.current_dt, ts)

                score = lscore + tscore
                wd = weather.fetch_weather_data (c, c.current_dt, loc, ts)

                if wd['precipitation'] < 1.0:
                    if wd['clouds'] < 50.0:
                        if c.lang == 'de':
                            c.resp(u"%s scheint in %s überwiegend die Sonne und es wird kaum Niederschlag geben." % (tlabel, llabel), score=score, action=act, action_arg=(ts, loc))
                        c.resp(u"%s it will be mostly sunny in %s with little precipitation." % (tlabel, llabel), score=score, action=act, action_arg=(ts, loc))
                    else:
                        if c.lang == 'de':
                            c.resp(u"%s ist es in %s überwiegend bewölkt, aber es gibt wenig Niederschlag." % (tlabel, llabel), score=score, action=act, action_arg=(ts, loc))
                        c.resp(u"%s it will be mostly cloudy in %s with little precipitation." % (tlabel, llabel), score=score, action=act, action_arg=(ts, loc))
                else:
                    if wd['clouds'] < 50.0:
                        if c.lang == 'de':
                            c.resp(u"%s scheint in %s oft die Sonne, aber es gibt auch %d Millimeter Niederschlag." % (tlabel, llabel, res['precipitation']), score=score, action=act, action_arg=(ts, loc))
                        c.resp(u"%s the sun will shine quite often in %s but there might be some precipitation of %d millimeters." % (tlabel, llabel, res['precipitation']), score=score, action=act, action_arg=(ts, loc))
                    else:
                        if c.lang == 'de':
                            c.resp(u"%s ist es in %s überwiegend bewölkt, und es gibt %d Millimeter Niederschlag." % (tlabel, llabel, res['precipitation']), score=score, action=act, action_arg=(ts, loc))
                        c.resp(u"%s it will be mostly cloudy in %s with %d millimeters of precipitation." % (tlabel, llabel, res['precipitation']), score=score, action=act, action_arg=(ts, loc))

    k.dte.dt('en', [u"how likely is it that it will rain ?", 
                    u"(will the sun shine | will there be sunshine ) ?", 
                    u"(will it | does it) rain ?", 
                    u"(will rain come | is rain coming) ?", 
                    u"(what is the likelihood of|how likely is) rain ?"], 
                   answer_weather_prec_cloud, [-1, -1, None])

    def prep_time_a(c):
        import dateutil.parser
        # c.current_dt = dateutil.parser.parse('2016-12-06T11:00:00+01:00')

    k.dte.ts('en', 't0000', [(u"Computer, will it rain?", u"today it will be mostly sunny in stuttgart with little precipitation", [])], prep=prep_time_a)
#     k.dte.ts('en', 't0003', [(u"how likely is rain?", u"today it will be mostly sunny in stuttgart with little precipitation", [])], prep=[Predicate(set(C:time, "2016-12-06T11:00:00+01:00"))])
# 
#     k.dte.ts('en', 't0005', [(u"Computer, how likely is it that it will rain ?", u"today it will be mostly sunny in stuttgart with little precipitation", [])], prep=[Predicate(set(C:time, "2016-12-06T11:00:00+01:00"))])
#     k.dte.ts('en', 't0009', [(u"computer, will there be sunshine?", u"today it will be mostly sunny in stuttgart with little precipitation", [])], prep=[Predicate(set(C:time, "2016-12-06T11:00:00+01:00"))])
# 
#     k.dte.ts('en', 't0011', [(u"Will it rain?", u"today it will be mostly sunny in stuttgart with little precipitation", [])], prep=[Predicate(set(C:time, "2016-12-06T11:00:00+01:00"))])
#     k.dte.ts('en', 't0013', [(u"Computer, is rain coming?", u"today it will be mostly sunny in stuttgart with little precipitation", [])], prep=[Predicate(set(C:time, "2016-12-06T11:00:00+01:00"))])
# 
# #    train(en) :- and(or(true, context(topic, wdeWeatherForecast)), or("what (will the weather|is the weather gonna|is the weather going to) be like ?", "how (cold|warm) (is it going to|will it) (be|become) ?", "(what will the weather be|what is the weather gonna be|what is the weather going to be) (like|) ?", "what (is the weather outlook | does the weather forecast look like | is the weather forecast | does the weather forecast say) ?", "(and|) how is the weather (there|then|)?", "(and|) what is the weather like (there|then|)?"), inline(answer_weather_context(en, full))).
#     k.dte.ts('en', 't0007', [(u"Computer, what will the weather be like?", u"today will be mostly clear skies in stuttgart with temperatures between minus eight and four degrees", [])], prep=[Predicate(set(C:time, "2016-12-06T11:00:00+01:00"))])
#     k.dte.ts('en', 't0015', [(u"Computer, how warm will it be ?", u"today will be mostly clear skies in stuttgart with temperatures between minus eight and four degrees", [])], prep=[Predicate(set(C:time, "2016-12-06T11:00:00+01:00"))])
# 
#     k.dte.ts('en', 't0017', [(u"computer, what will the weather be like?", u"today will be mostly clear skies in stuttgart with temperatures between minus eight and four degrees", [])], prep=[Predicate(set(C:time, "2016-12-06T11:00:00+01:00"))])
#     k.dte.ts('en', 't0021', [(u"Computer, what does the weather forecast say?", u"today will be mostly clear skies in Stuttgart with temperatures between -8 and 4 degrees.", [])], prep=[Predicate(set(C:time, "2016-12-06T11:00:00+01:00"))])
# 
# #    train(de) :- and(or(true, context(topic, wdeWeatherForecast)), or("wird es (regnen|Regen geben) ?", "(was ist die Wahrscheinlichkeit für|wie groß ist die Wahrscheinlichkeit für|wie wahrscheinlich ist) Regen ?", "wie wahrscheinlich ist es, dass es regnen wird?", "scheint die Sonne?", "regnet es ?", "kommt noch Regen ?"), inline(answer_weather_context(de, prec_cloud))).
#     k.dte.ts('de', 't0002', [(u"Computer, wird es regnen?", u"heute scheint in stuttgart überwiegend die sonne und es wird kaum niederschlag geben", [])], prep=[Predicate(set(C:time, "2016-12-06T11:00:00+01:00"))])
#     k.dte.ts('de', 't0004', [(u"wie groß ist die Wahrscheinlichkeit für Regen?", u"heute scheint in stuttgart überwiegend die sonne und es wird kaum niederschlag geben", [])], prep=[Predicate(set(C:time, "2016-12-06T11:00:00+01:00"))])
# 
#     k.dte.ts('de', 't0006', [(u"Computer, wie wahrscheinlich ist es, dass es regnen wird?", u"heute scheint in stuttgart überwiegend die sonne und es wird kaum niederschlag geben", [])], prep=[Predicate(set(C:time, "2016-12-06T11:00:00+01:00"))])
#     k.dte.ts('de', 't0010', [(u"computer, scheint die Sonne?", u"heute scheint in stuttgart überwiegend die sonne und es wird kaum niederschlag geben", [])], prep=[Predicate(set(C:time, "2016-12-06T11:00:00+01:00"))])
# 
#     k.dte.ts('de', 't0012', [(u"Regnet es?", u"heute scheint in stuttgart überwiegend die sonne und es wird kaum niederschlag geben", [])], prep=[Predicate(set(C:time, "2016-12-06T11:00:00+01:00"))])
#     k.dte.ts('de', 't0014', [(u"Computer, kommt noch Regen?", u"heute scheint in stuttgart überwiegend die sonne und es wird kaum niederschlag geben", [])], prep=[Predicate(set(C:time, "2016-12-06T11:00:00+01:00"))])
# 
# #    train(de) :- and(or(true, context(topic, wdeWeatherForecast)), or("wie (ist|ist denn|wird) das Wetter (werden|)?", "wie (kalt|warm) wird es (werden|) ?", "(wie sind die Wetteraussichten | was sagt die Wettervorhersage | was sagt der Wetterbericht ) ?", "(und|) wie (ist das Wetter|sieht das Wetter aus|wie wird das wetter) (dort|dann|)?"), inline(answer_weather_context(de, full))).
#     k.dte.ts('de', 't0008', [(u"Computer, wie wird das Wetter werden?", u"heute wird es wenige wolken geben in stuttgart und es wird zwischen minus acht und vier grad warm", [])], prep=[Predicate(set(C:time, "2016-12-06T11:00:00+01:00"))])
#     k.dte.ts('de', 't0016', [(u"Computer, wie warm wird es?", u"heute wird es wenige wolken geben in stuttgart und es wird zwischen minus acht und vier grad warm", [])], prep=[Predicate(set(C:time, "2016-12-06T11:00:00+01:00"))])
# 
#     k.dte.ts('de', 't0018', [(u"computer, wie wird das Wetter?", u"heute wird es wenige wolken geben in stuttgart und es wird zwischen minus acht und vier grad warm", [])], prep=[Predicate(set(C:time, "2016-12-06T11:00:00+01:00"))])
#     k.dte.ts('de', 't0022', [(u"Computer, was sagt der Wetterbericht?", u"heute wird es wenige wolken geben in stuttgart und es wird zwischen minus acht und vier grad warm", [])], prep=[Predicate(set(C:time, "2016-12-06T11:00:00+01:00"))])
# 
#     def answer_weather_expl_time(en, REPORT, TIME):
#         and(or(and(var(C:mem|f1loc), set(C:mem|f1loc, self:wdpdLocatedIn)), and(not(var(C:mem|f1loc)), true)), set(C:mem|f1timespan, TIME), set(C:context|topic, wdeWeatherForecast), answer_weather_r(C, en, REPORT))
#     def answer_weather_expl_time(de, REPORT, TIME):
#         and(or(and(var(C:mem|f1loc), set(C:mem|f1loc, self:wdpdLocatedIn)), and(not(var(C:mem|f1loc)), true)), set(C:mem|f1timespan, TIME), set(C:context|topic, wdeWeatherForecast), answer_weather_r(C, de, REPORT))
# #    train(en) :- and(or(true, context(topic, wdeWeatherForecast)), or("(what is the likelihood of | how likely is) rain {timespec:LABEL} ?", "How likely is it that it will rain {timespec:LABEL}?", "(will the sun shine|will there be sunshine) {timespec:LABEL} ?", "(will it|does it) rain {timespec:LABEL}?", "(will rain come|is rain coming) {timespec:LABEL}?"), inline(answer_weather_expl_time(en, prec_cloud, mvar(timespec, time)))).
#     k.dte.ts('en', 't0100', [(u"Computer, will it rain tomorrow?", u"tomorrow it will be mostly sunny in stuttgart with little precipitation", [])], prep=[Predicate(set(C:time, "2016-12-06T11:00:00+01:00"))])
#     k.dte.ts('en', 't0102', [(u"how likely is rain the day after tomorrow?", u"day after tomorrow it will be mostly sunny in Stuttgart with little precipitation.", [])], prep=[Predicate(set(C:time, "2016-12-06T11:00:00+01:00"))])
# 
#     k.dte.ts('en', 't0104', [(u"Computer, how likely is it that it will rain today?", u"today it will be mostly sunny in stuttgart with little precipitation", [])], prep=[Predicate(set(C:time, "2016-12-06T11:00:00+01:00"))])
#     k.dte.ts('en', 't0108', [(u"computer, will there be sunshine the day after tomorrow?", u"day after tomorrow it will be mostly sunny in Stuttgart with little precipitation.", [])], prep=[Predicate(set(C:time, "2016-12-06T11:00:00+01:00"))])
# 
#     k.dte.ts('en', 't0110', [(u"Will it rain today?", u"today it will be mostly sunny in stuttgart with little precipitation", [])], prep=[Predicate(set(C:time, "2016-12-06T11:00:00+01:00"))])
#     k.dte.ts('en', 't0112', [(u"Computer, is rain coming tomorrow?", u"tomorrow it will be mostly sunny in stuttgart with little precipitation", [])], prep=[Predicate(set(C:time, "2016-12-06T11:00:00+01:00"))])
# 
# #    train(en) :- and(or(true, context(topic, wdeWeatherForecast)), or("what (will the weather|is the weather gonna|is the weather going to) be like {timespec:LABEL} ?", "how (cold|warm) (is it going to|will it) (be|become) {timespec:LABEL}?", "what (is the weather outlook|does the weather forecast look like|is the weather forecast|does the weather forecast say) for {timespec:LABEL} ?", "How is the weather {timespec:LABEL} ?"), inline(answer_weather_expl_time(en, full, mvar(timespec, time)))).
#     k.dte.ts('en', 't0106', [(u"Computer, what will the weather be like tomorrow?", u"tomorrow will be mostly clear skies in stuttgart with temperatures between minus nine and one degrees", [])], prep=[Predicate(set(C:time, "2016-12-06T11:00:00+01:00"))])
#     k.dte.ts('en', 't0114', [(u"Computer, how warm will it be the day after tomorrow?", u"day after tomorrow the sun will show up occasionally in Stuttgart with temperatures between -10 and 1 degrees.", [])], prep=[Predicate(set(C:time, "2016-12-06T11:00:00+01:00"))])
# 
#     k.dte.ts('en', 't0116', [(u"computer, what will the weather be like today?", u"today will be mostly clear skies in stuttgart with temperatures between minus eight and four degrees", [])], prep=[Predicate(set(C:time, "2016-12-06T11:00:00+01:00"))])
#     k.dte.ts('en', 't0118', [(u"what is the weather gonna be like tomorrow?", u"tomorrow will be mostly clear skies in stuttgart with temperatures between minus nine and one degrees", [])], prep=[Predicate(set(C:time, "2016-12-06T11:00:00+01:00"))])
# 
#     k.dte.ts('en', 't0120', [(u"Computer, what does the weather forecast say for today?", u"today will be mostly clear skies in stuttgart with temperatures between minus eight and four degrees", [])], prep=[Predicate(set(C:time, "2016-12-06T11:00:00+01:00"))])
# #    train(de) :- and(or(true, context(topic, wdeWeatherForecast)), or("wird es {timespec:LABEL} (regnen|Regen geben)?", "(was ist die Wahrscheinlichkeit für|wie groß ist die Wahrscheinlichkeit für|wie wahrscheinlich ist) Regen {timespec:LABEL} ?", "Wie wahrscheinlich ist es, dass es {timespec:LABEL} regnen wird?", "scheint {timespec:LABEL} die Sonne?", "regnet es {timespec:LABEL}?", "kommt {timespec:LABEL} noch Regen ?"), inline(answer_weather_expl_time(de, prec_cloud, mvar(timespec, time)))).
# #    train(de) :- and(or(true, context(topic, wdeWeatherForecast)), or("wie wird {timespec:LABEL} das Wetter?", "wie (kalt|warm) wird es {timespec:LABEL} (werden|)?", "wie (ist|wird|ist denn) das Wetter {timespec:LABEL}?", "(wie sind die Wetteraussichten|was sagt die Wettervorhersage|was sagt der Wetterbericht) für {timespec:LABEL} ?"), inline(answer_weather_expl_time(de, full, mvar(timespec, time)))).
#     k.dte.ts('de', 't0101', [(u"Computer, wird es morgen regnen?", u"morgen scheint in stuttgart überwiegend die sonne und es wird kaum niederschlag geben", [])], prep=[Predicate(set(C:time, "2016-12-06T11:00:00+01:00"))])
# 
#     k.dte.ts('de', 't0103', [(u"wie groß ist die Wahrscheinlichkeit für Regen übermorgen?", u"übermorgen scheint in stuttgart überwiegend die sonne und es wird kaum niederschlag geben", [])], prep=[Predicate(set(C:time, "2016-12-06T11:00:00+01:00"))])
#     k.dte.ts('de', 't0105', [(u"Computer, wie wahrscheinlich ist es, dass es heute regnen wird?", u"heute scheint in stuttgart überwiegend die sonne und es wird kaum niederschlag geben", [])], prep=[Predicate(set(C:time, "2016-12-06T11:00:00+01:00"))])
# 
#     k.dte.ts('de', 't0107', [(u"Computer, wie wird morgen das Wetter?", u"morgen wird es wenige wolken geben in stuttgart und es wird zwischen minus neun und eins grad warm", [])], prep=[Predicate(set(C:time, "2016-12-06T11:00:00+01:00"))])
#     k.dte.ts('de', 't0109', [(u"computer, scheint übermorgen die Sonne?", u"übermorgen scheint in stuttgart überwiegend die sonne und es wird kaum niederschlag geben", [])], prep=[Predicate(set(C:time, "2016-12-06T11:00:00+01:00"))])
# 
#     k.dte.ts('de', 't0111', [(u"Regnet es heute?", u"heute scheint in stuttgart überwiegend die sonne und es wird kaum niederschlag geben", [])], prep=[Predicate(set(C:time, "2016-12-06T11:00:00+01:00"))])
#     k.dte.ts('de', 't0113', [(u"Computer, kommt morgen noch Regen?", u"morgen scheint in stuttgart überwiegend die sonne und es wird kaum niederschlag geben", [])], prep=[Predicate(set(C:time, "2016-12-06T11:00:00+01:00"))])
# 
#     k.dte.ts('de', 't0115', [(u"Computer, wie warm wird es übermorgen?", u"übermorgen zeigt sich ab und an die sonne in stuttgart und es wird zwischen minus 10 und eins grad warm", [])], prep=[Predicate(set(C:time, "2016-12-06T11:00:00+01:00"))])
#     k.dte.ts('de', 't0117', [(u"computer, wie wird das Wetter heute?", u"heute wird es wenige wolken geben in stuttgart und es wird zwischen minus acht und vier grad warm", [])], prep=[Predicate(set(C:time, "2016-12-06T11:00:00+01:00"))])
# 
#     k.dte.ts('de', 't0119', [(u"wie wird das Wetter morgen?", u"morgen wird es wenige wolken geben in stuttgart und es wird zwischen minus neun und eins grad warm", [])], prep=[Predicate(set(C:time, "2016-12-06T11:00:00+01:00"))])
#     k.dte.ts('de', 't0121', [(u"Computer, was sagt der Wetterbericht für heute?", u"heute wird es wenige wolken geben in stuttgart und es wird zwischen minus acht und vier grad warm", [])], prep=[Predicate(set(C:time, "2016-12-06T11:00:00+01:00"))])
# 
#     def answer_weather_expl_place(en, REPORT, TS, TE):
#         and(ner(en, weather_location, TS, TE, C:tokens, LOCATION, SCORE), r_score(C, SCORE), set(C:mem|f1loc, LOCATION), or(and(var(C:mem|f1timespan), set(C:mem|f1timespan, weatherNearFuture)), and(not(var(C:mem|f1timespan)), true)), set(C:context|topic, wdeWeatherForecast), answer_weather_r(C, en, REPORT))
#     def answer_weather_expl_place(de, REPORT, TS, TE):
#         and(ner(de, weather_location, TS, TE, C:tokens, LOCATION, SCORE), r_score(C, SCORE), set(C:mem|f1loc, LOCATION), or(and(var(C:mem|f1timespan), set(C:mem|f1timespan, weatherNearFuture)), and(not(var(C:mem|f1timespan)), true)), set(C:context|topic, wdeWeatherForecast), answer_weather_r(C, de, REPORT))
# #    train(en) :- and(or(true, context(topic, wdeWeatherForecast)), or("(what is the likelihood of | how likely is) rain in {weather_location:LABEL} ?", "how likely is it that it will rain in {weather_location:LABEL} ?", "(will the sun shine | will there be sunshine )  in {weather_location:LABEL} ?", "(will it | does it) rain in {weather_location:LABEL} ?", "(will rain come|is rain coming) in {weather_location:LABEL} ?", "how (cold|warm) (is it going to|will it) (be|become) in {weather_location:LABEL}?"), inline(answer_weather_expl_place(en, prec_cloud, tstart(weather_location), tend(weather_location)))).
#     k.dte.ts('en', 't0200', [(u"Computer, will it rain in Freudental?", u"today it will be mostly sunny in freudental with little precipitation", [])], prep=[Predicate(set(C:time, "2016-12-06T11:00:00+01:00"))])
#     k.dte.ts('en', 't0202', [(u"how likely is rain in Stuttgart?", u"today it will be mostly sunny in stuttgart with little precipitation", [])], prep=[Predicate(set(C:time, "2016-12-06T11:00:00+01:00"))])
# 
#     k.dte.ts('en', 't0204', [(u"Computer, how likely is it that it will rain in Freudental?", u"today it will be mostly sunny in Freudental with little precipitation.", [])], prep=[Predicate(set(C:time, "2016-12-06T11:00:00+01:00"))])
#     k.dte.ts('en', 't0208', [(u"computer, will there be sunshine in stuttgart?", u"today it will be mostly sunny in stuttgart with little precipitation", [])], prep=[Predicate(set(C:time, "2016-12-06T11:00:00+01:00"))])
# 
#     k.dte.ts('en', 't0210', [(u"Will it rain in Freudental?", u"today it will be mostly sunny in Freudental with little precipitation.", [])], prep=[Predicate(set(C:time, "2016-12-06T11:00:00+01:00"))])
#     k.dte.ts('en', 't0212', [(u"Computer, is rain coming in Tallinn?", u"today it will be mostly sunny in tallinn with little precipitation", [])], prep=[Predicate(set(C:time, "2016-12-06T11:00:00+01:00"))])
# 
#     k.dte.ts('en', 't0214', [(u"Computer, how warm will it be in Stuttgart?", u"today it will be mostly sunny in stuttgart with little precipitation", [])], prep=[Predicate(set(C:time, "2016-12-06T11:00:00+01:00"))])
# #    train(en) :- and(or(true, context(topic, wdeWeatherForecast)), or("what ( will the weather | is the weather gonna | is the weather going to ) be (like|) in {weather_location:LABEL} ?", "how (cold|warm) (is it going to|will it) (be|become) in {weather_location:LABEL} ?", "what (is the weather outlook|does the weather forecast look like|is the weather forecast|does the weather forecast say) for {weather_location:LABEL} ?", "How is the weather in {weather_location:LABEL} ?"), inline(answer_weather_expl_place(en, full, tstart(weather_location), tend(weather_location)))).
#     k.dte.ts('en', 't0206', [(u"Computer, what will the weather be like in Tallinn?", u"today there will be some clouds in tallinn with temperatures between minus eight and minus three degrees", [])], prep=[Predicate(set(C:time, "2016-12-06T11:00:00+01:00"))])
# 
#     k.dte.ts('en', 't0216', [(u"computer, what will the weather be like in Tallinn?", u"today there will be some clouds in tallinn with temperatures between minus eight and minus three degrees", [])], prep=[Predicate(set(C:time, "2016-12-06T11:00:00+01:00"))])
#     k.dte.ts('en', 't0218', [(u"what is the weather gonna be like in stuttgart?", u"today will be mostly clear skies in stuttgart with temperatures between minus eight and four degrees", [])], prep=[Predicate(set(C:time, "2016-12-06T11:00:00+01:00"))])
# 
#     k.dte.ts('en', 't0220', [(u"Computer, what does the weather forecast say for stuttgart?", u"today will be mostly clear skies in stuttgart with temperatures between minus eight and four degrees", [])], prep=[Predicate(set(C:time, "2016-12-06T11:00:00+01:00"))])
# #    train(de) :- and(or(true, context(topic, wdeWeatherForecast)), or("wird es in {weather_location:LABEL} (regnen | Regen geben) ?", "( was ist die Wahrscheinlichkeit für | wie groß ist die Wahrscheinlichkeit für | wie wahrscheinlich ist )  Regen in {weather_location:LABEL} ?", "wie wahrscheinlich ist es, dass es in {weather_location:LABEL} regnen wird?", "scheint in {weather_location:LABEL} die Sonne?", "regnet es in {weather_location:LABEL} ?", "kommt noch Regen in {weather_location:LABEL} ?", "wie (kalt|warm) wird es in {weather_location:LABEL} (werden|)?"), inline(answer_weather_expl_place(de, prec_cloud, tstart(weather_location), tend(weather_location)))).
#     k.dte.ts('de', 't0201', [(u"Computer, wird es in Freudental regnen?", u"heute scheint in freudental überwiegend die sonne und es wird kaum niederschlag geben", [])], prep=[Predicate(set(C:time, "2016-12-06T11:00:00+01:00"))])
# 
#     k.dte.ts('de', 't0203', [(u"wie groß ist die Wahrscheinlichkeit für Regen in Stuttgart?", u"heute scheint in stuttgart überwiegend die sonne und es wird kaum niederschlag geben", [])], prep=[Predicate(set(C:time, "2016-12-06T11:00:00+01:00"))])
#     k.dte.ts('de', 't0205', [(u"Computer, wie wahrscheinlich ist es, dass es in Freudental regnen wird?", u"heute scheint in freudental überwiegend die sonne und es wird kaum niederschlag geben", [])], prep=[Predicate(set(C:time, "2016-12-06T11:00:00+01:00"))])
# 
#     k.dte.ts('de', 't0209', [(u"computer, scheint in Stuttgart die Sonne?", u"heute scheint in stuttgart überwiegend die sonne und es wird kaum niederschlag geben", [])], prep=[Predicate(set(C:time, "2016-12-06T11:00:00+01:00"))])
#     k.dte.ts('de', 't0211', [(u"Regnet es in Freudental?", u"heute scheint in freudental überwiegend die sonne und es wird kaum niederschlag geben", [])], prep=[Predicate(set(C:time, "2016-12-06T11:00:00+01:00"))])
# 
#     k.dte.ts('de', 't0213', [(u"Computer, kommt noch Regen in Tallinn?", u"heute scheint in tallinn überwiegend die sonne und es wird kaum niederschlag geben", [])], prep=[Predicate(set(C:time, "2016-12-06T11:00:00+01:00"))])
#     k.dte.ts('de', 't0215', [(u"Computer, wie warm wird es in Stuttgart?", u"heute scheint in stuttgart überwiegend die sonne und es wird kaum niederschlag geben", [])], prep=[Predicate(set(C:time, "2016-12-06T11:00:00+01:00"))])
# 
# #    train(de) :- and(or(true, context(topic, wdeWeatherForecast)), or("wie (ist|ist denn|wird) in {weather_location:LABEL} das Wetter?", "wie (ist|ist denn|wird) das Wetter in {weather_location:LABEL}?", "(wie sind die Wetteraussichten|was sagt die Wettervorhersage|was sagt der Wetterbericht) für {weather_location:LABEL}?"), inline(answer_weather_expl_place(de, full, tstart(weather_location), tend(weather_location)))).
#     k.dte.ts('de', 't0207', [(u"Computer, wie wird in Tallinn das Wetter?", u"heute wird es lockere wolken geben in tallinn und es wird zwischen minus acht und minus drei grad warm", [])], prep=[Predicate(set(C:time, "2016-12-06T11:00:00+01:00"))])
#     k.dte.ts('de', 't0217', [(u"computer, wie wird das Wetter in Tallinn?", u"heute wird es lockere wolken geben in tallinn und es wird zwischen minus acht und minus drei grad warm", [])], prep=[Predicate(set(C:time, "2016-12-06T11:00:00+01:00"))])
# 
#     k.dte.ts('de', 't0219', [(u"wie wird das Wetter in Stuttgart?", u"heute wird es wenige wolken geben in stuttgart und es wird zwischen minus acht und vier grad warm", [])], prep=[Predicate(set(C:time, "2016-12-06T11:00:00+01:00"))])
#     k.dte.ts('de', 't0221', [(u"Computer, was sagt der Wetterbericht für Stuttgart?", u"heute wird es wenige wolken geben in stuttgart und es wird zwischen minus acht und vier grad warm", [])], prep=[Predicate(set(C:time, "2016-12-06T11:00:00+01:00"))])
# 
#     def answer_weather_expl_place_time(en, REPORT, TS, TE, TIME):
#         and(ner(en, weather_location, TS, TE, C:tokens, LOCATION, SCORE), r_score(C, SCORE), set(C:mem|f1loc, LOCATION), set(C:mem|f1timespan, TIME), set(C:context|topic, wdeWeatherForecast), answer_weather_r(C, en, REPORT))
#     def answer_weather_expl_place_time(de, REPORT, TS, TE, TIME):
#         and(ner(de, weather_location, TS, TE, C:tokens, LOCATION, SCORE), r_score(C, SCORE), set(C:mem|f1loc, LOCATION), set(C:mem|f1timespan, TIME), set(C:context|topic, wdeWeatherForecast), answer_weather_r(C, de, REPORT))
# #    train(en) :- and(or(true, context(topic, wdeWeatherForecast)), or("will it rain in {weather_location:LABEL} {timespec:LABEL} ?", "(what is the likelihood of | how likely is | rain in ) {weather_location:LABEL} {timespec:LABEL} ?", "how likely is it that it will rain {timespec:LABEL} in {weather_location:LABEL} ?", "(will the sun shine | will there be sunshine ) {timespec:LABEL}  in {weather_location:LABEL} ?", "(will it | does it) rain in {weather_location:LABEL} {timespec:LABEL} ?", "(will rain come|is rain coming) in {weather_location:LABEL} {timespec:LABEL} ?"), inline(answer_weather_expl_place_time(en, prec_cloud, tstart(weather_location), tend(weather_location), mvar(timespec, time)))).
# #    train(en) :- and(or(true, context(topic, wdeWeatherForecast)), or("what ( will the weather | is the weather gonna | is the weather going to ) be like {timespec:LABEL} in {weather_location:LABEL} ?", "how (cold|warm) (is it going to|will it) (be|become) in {weather_location:LABEL} {timespec:LABEL}?", "(what will the weather be|what is the weather gonna be|what is the weather going to be) (like|) in {weather_location:LABEL} {timespec:LABEL} ?", "(what will the weather be|what is the weather gonna be|what is the weather going to be) (like|) in {weather_location:LABEL} {timespec:LABEL} ?", "what (is the weather outlook|does the weather forecast look like|is the weather forecast|does the weather forecast say) for {weather_location:LABEL} {timespec:LABEL} ?", "How is the weather in {weather_location:LABEL} {timespec:LABEL}?"), inline(answer_weather_expl_place_time(en, full, tstart(weather_location), tend(weather_location), mvar(timespec, time)))).
# #    train(de) :- and(or(true, context(topic, wdeWeatherForecast)), or("wie (kalt|warm) wird es {timespec:LABEL} in {weather_location:LABEL} werden?", "kommt {timespec:LABEL} noch Regen in {weather_location:LABEL} ?", "regnet es {timespec:LABEL} in {weather_location:LABEL} ?", "scheint in {weather_location:LABEL} {timespec:LABEL} die Sonne?", "wie wahrscheinlich ist es, dass es {timespec:LABEL} in {weather_location:LABEL} regnen wird?", "wird es {timespec:LABEL} in {weather_location:LABEL} (regnen | Regen geben) ?", "( was ist die Wahrscheinlichkeit für | wie groß ist die Wahrscheinlichkeit für | wie wahrscheinlich ist )  Regen {timespec:LABEL} in {weather_location:LABEL} ?"), inline(answer_weather_expl_place_time(de, prec_cloud, tstart(weather_location), tend(weather_location), mvar(timespec, time)))).
# #    train(de) :- and(or(true, context(topic, wdeWeatherForecast)), or("wie (ist|ist denn|wird) {timespec:LABEL} in {weather_location:LABEL} das Wetter?", "wie (ist|ist denn|wird) {timespec:LABEL} das Wetter in {weather_location:LABEL}?", "wie wird das Wetter {timespec:LABEL} in {weather_location:LABEL}?", "(wie sind die Wetteraussichten|was sagt die Wettervorhersage|was sagt der Wetterbericht) für {timespec:LABEL} für {weather_location:LABEL}?"), inline(answer_weather_expl_place_time(de, full, tstart(weather_location), tend(weather_location), mvar(timespec, time)))).
#     k.dte.ts('en', 't0300', [(u"Computer, what does the weather forecast say for stuttgart tomorrow?", u"tomorrow will be mostly clear skies in stuttgart with temperatures between minus nine and one degrees", [])], prep=[Predicate(set(C:time, "2016-12-06T11:00:00+01:00"))])
#     k.dte.ts('de', 't0301', [(u"Computer, was sagt der Wetterbericht für heute für Tallinn?", u"heute wird es lockere wolken geben in tallinn und es wird zwischen minus acht und minus drei grad warm", [])], prep=[Predicate(set(C:time, "2016-12-06T11:00:00+01:00"))])
# 
# #    train(en) :- and(context(topic, wdeWeatherForecast), "(and|) {timespec:LABEL}", inline(answer_weather_expl_time(en, full, mvar(timespec, time)))).
# #    train(de) :- and(context(topic, wdeWeatherForecast), "(und|) {timespec:LABEL}", inline(answer_weather_expl_time(de, full, mvar(timespec, time)))).
# #    train(en) :- and(context(topic, wdeWeatherForecast), "(and|) in {weather_location:LABEL} ?", inline(answer_weather_expl_place(en, full, tstart(weather_location), tend(weather_location)))).
# #    train(de) :- and(context(topic, wdeWeatherForecast), "(und|) in {weather_location:LABEL} ?", inline(answer_weather_expl_place(de, full, tstart(weather_location), tend(weather_location)))).
#     def get_topic_label(C, en, "the weather report"):
#         and(context(C, topic, wdeWeatherForecast), r_score(C, 10.0))
#     def get_topic_label(C, de, "der Wetterbericht"):
#         and(context(C, topic, wdeWeatherForecast), r_score(C, 10.0))
# #    train(en) :- and(context(topic, wdeWeatherForecast), inline(question_what_was_our_topic(en)), r_score(C, 100.0), or(say(C, "We have been talking about the weather report, I think."), say(C, "Our topic was the weather, I believe."), say(C, "Didn't we talk about the weather report?"))).
# #    train(de) :- and(context(topic, wdeWeatherForecast), inline(question_what_was_our_topic(de)), r_score(C, 100.0), or(say(C, "Wir hatten über das Wetter gesprochen, glaube ich."), say(C, "Ich denke unser Thema war der Wetterbericht."), say(C, "Sprachen wir nicht über den Wetterbericht ?"))).
# #    train(en) :- and(context(topic, wdeWeatherForecast), or("that is (definitely|) (pretty|too) (cold|warm|hot)", "that is too (cold|warm|hot) for (me|my taste)"), or("Proper clothing will fix that.", "The weather service will hear about that.", "Maybe you should move to a milder climate?")).
# #    train(de) :- and(context(topic, wdeWeatherForecast), or("das ist (ja|) (ganz schön|zu|) (warm|kalt|heiß)", "das ist mir zu (warm|kalt|heiß)"), or("Alles eine Frage der richtigen Kleidung!", "Ich sende eine Beschwerde an das Wetteramt.", "Vielleicht solltest Du über einen Umzug nachdenken?")).
#     k.dte.dt('en', u"about the weather", u"Always a good topic.")
#     k.dte.dt('de', u"über das wetter", u"Immer ein gutes Thema.")
# 
#     k.dte.dt('en', u"the weather is bad", u"So let's stay inside and chat some more!")
#     k.dte.dt('de', u"das wetter ist schlecht", u"Dann lass uns drinnen bleiben und noch ein wenig reden!")

