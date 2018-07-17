#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# Copyright 2018 Guenter Bartsch
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

    def weather_location(LOC):
        owmCityId(LOC, CITYID)

    # NER, macros

    for lang in ['en', 'de']:
        for res in k.prolog_query("owmCityId(LOC, CITYID), rdfsLabel(LOC, %s, LABEL)." % lang):
            s_loc   = res[0].name
            s_label = res[2].value
            k.dte.ner(lang, 'weather_location', s_loc, s_label)
            k.dte.macro(lang, 'weather_location', {'LABEL': s_label})

    def answer_weather(c, mode, lts, lte, timespan, check_topic):

        def act(c, args):
            ts, loc = args
            c.kernal.mem_push(c.user, 'f1ent', 'wdeWeatherForecast')
            c.kernal.mem_push(c.user, 'f1time', ts)
            c.kernal.mem_push(c.user, 'f1loc',  loc)

        import weather

        if check_topic:
            topic = c.kernal.mem_get_multi(c.user, 'f1ent')
            if not topic:
                return
            topic = topic[0][0]
            if topic != 'wdeWeatherForecast':
                return

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
                prec = wd['precipitation']

                if mode == 'prec_cloud':

                    if prec < 1.0:
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
                                c.resp(u"%s scheint in %s oft die Sonne, aber es gibt auch %d Millimeter Niederschlag." % (tlabel, llabel, prec), score=score, action=act, action_arg=(ts, loc))
                            c.resp(u"%s the sun will shine quite often in %s but there might be some precipitation of %d millimeters." % (tlabel, llabel, prec), score=score, action=act, action_arg=(ts, loc))
                        else:
                            if c.lang == 'de':
                                c.resp(u"%s ist es in %s überwiegend bewölkt, und es gibt %d Millimeter Niederschlag." % (tlabel, llabel, prec), score=score, action=act, action_arg=(ts, loc))
                            c.resp(u"%s it will be mostly cloudy in %s with %d millimeters of precipitation." % (tlabel, llabel, prec), score=score, action=act, action_arg=(ts, loc))

                elif mode == 'full':

                    icon = wd['icon'][:2]
                    tmin = wd['temp_min']
                    tmax = wd['temp_max']

                    if c.lang == 'de':
                        if icon == u'01':
                            c.resp(u"%s wird der Himmel klar sein in %s und es wird zwischen %d und %d Grad warm." % (tlabel, llabel, tmin, tmax), score=score, action=act, action_arg=(ts, loc))
                        elif icon == u'02':
                            c.resp(u"%s wird es wenige Wolken geben in %s und es wird zwischen %d und %d Grad warm." % (tlabel, llabel, tmin, tmax), score=score, action=act, action_arg=(ts, loc))
                        elif icon == u'03':
                            c.resp(u"%s wird es lockere Wolken geben in %s und es wird zwischen %d und %d Grad warm." % (tlabel, llabel, tmin, tmax), score=score, action=act, action_arg=(ts, loc))
                        elif icon == u'04':
                            c.resp(u"%s zeigt sich ab und an die Sonne in %s und es wird zwischen %d und %d Grad warm." % (tlabel, llabel, tmin, tmax), score=score, action=act, action_arg=(ts, loc))
                        elif icon == u'09':
                            c.resp(u"%s wird es %d Millimeter Schauer geben in %s und es wird zwischen %d und %d Grad warm." % (tlabel, prec, llabel, tmin, tmax), score=score, action=act, action_arg=(ts, loc))
                        elif icon == u'10':
                            if prec >= 1.0:
                                c.resp(u"%s regnet es %d Millimeter in %s und es wird zwischen %d und %d Grad warm." % (tlabel, prec, llabel, tmin, tmax), score=score, action=act, action_arg=(ts, loc))
                            else:
                                c.resp(u"%s kann es etwas Niederschlag geben in %s und es wird zwischen %d und %d Grad warm." % (tlabel, llabel, tmin, tmax), score=score, action=act, action_arg=(ts, loc))
                        elif icon == u'11':
                            c.resp(u"%s wird es Gewitter geben mit %d Millimeter Niederschlag in %s und es wird zwischen %d und %d Grad warm." % (tlabel, prec, llabel, tmin, tmax), score=score, action=act, action_arg=(ts, loc))
                        elif icon == u'13':
                            if prec >= 1.0:
                                c.resp(u"%s schneit es %d Millimeter in %s und es wird zwischen %d und %d Grad kalt." % (tlabel, prec, llabel, tmin, tmax), score=score, action=act, action_arg=(ts, loc))
                            else:
                                c.resp(u"%s schneit es ein wenig in %s und es wird zwischen %d und %d Grad kalt." % (tlabel, llabel, tmin, tmax), score=score, action=act, action_arg=(ts, loc))
                        elif icon == u'50':
                            c.resp(u"%s wird es neblich in %s und es wird zwischen %d und %d Grad geben." % (tlabel, llabel, tmin, tmax), score=score, action=act, action_arg=(ts, loc))

                    else:

                        if icon == u'01':
                            c.resp(u"%s will be clear skies in %s with temperatures between %d and %d degrees." % (tlabel, llabel, tmin, tmax), score=score, action=act, action_arg=(ts, loc))
                        elif icon == u'02':
                            c.resp(u"%s will be mostly clear skies in %s with temperatures between %d and %d degrees." % (tlabel, llabel, tmin, tmax), score=score, action=act, action_arg=(ts, loc))
                        elif icon == u'03':
                            c.resp(u"%s there will be some clouds in %s with temperatures between %d and %d degrees." % (tlabel, llabel, tmin, tmax), score=score, action=act, action_arg=(ts, loc))
                        elif icon == u'04':
                            c.resp(u"%s the sun will show up occasionally in %s with temperatures between %d and %d degrees." % (tlabel, llabel, tmin, tmax), score=score, action=act, action_arg=(ts, loc))
                        elif icon == u'09':
                            c.resp(u"%s there will be rain showers of %d millimeters in %s with temperatures between %d and %d degrees." % (tlabel, prec, llabel, tmin, tmax), score=score, action=act, action_arg=(ts, loc))
                        elif icon == u'10':
                            if prec >= 1.0:
                                c.resp(u"%s it will rain %d millimeters in %s with temperatures between %d and %d degrees." % (tlabel, prec, llabel, tmin, tmax), score=score, action=act, action_arg=(ts, loc))
                            else:
                                c.resp(u"%s there might be a little rain in %s with temperatures between %d and %d degrees." % (tlabel, llabel, tmin, tmax), score=score, action=act, action_arg=(ts, loc))
                        elif icon == u'11':
                            c.resp(u"%s we will have thunderstorms and %d millimeters of rain in %s with temperatures between %d and %d degrees." % (tlabel, prec, llabel, tmin, tmax), score=score, action=act, action_arg=(ts, loc))
                        elif icon == u'13':
                            c.resp(u"%s it will snow %d millimeters in %s with temperatures between %d and %d degrees." % (tlabel, prec, llabel, tmin, tmax), score=score, action=act, action_arg=(ts, loc))
                        elif icon == u'50':
                            c.resp(u"%s it will be foggy in %s with temperatures between %d and %d degrees" % (tlabel, llabel, tmin, tmax), score=score, action=act, action_arg=(ts, loc))

                else:
                    raise Exception ('Mode %s not implemented yet.' % mode)

    k.dte.dt('en', [u"how likely is it that it will rain ?", 
                    u"(will the sun shine | will there be sunshine ) ?", 
                    u"(will it | does it) rain ?", 
                    u"(will rain come | is rain coming) ?", 
                    u"(what is the likelihood of|how likely is) rain ?"], 
                   answer_weather, ['prec_cloud', -1, -1, None, False])

    def prep_time_a(c):
        import dateutil.parser
        c.current_dt = dateutil.parser.parse('2017-06-12T07:30:00+01:00')

    k.dte.ts('en', 't0000', [(u"will it rain?", u"today it will be mostly sunny in stuttgart with little precipitation")], prep=prep_time_a)
    k.dte.ts('en', 't0003', [(u"how likely is rain?", u"today it will be mostly sunny in stuttgart with little precipitation")], prep=prep_time_a)
 
    k.dte.ts('en', 't0005', [(u"how likely is it that it will rain ?", u"today it will be mostly sunny in stuttgart with little precipitation")], prep=prep_time_a)
    k.dte.ts('en', 't0009', [(u"will there be sunshine?", u"today it will be mostly sunny in stuttgart with little precipitation")], prep=prep_time_a)

    k.dte.ts('en', 't0011', [(u"Will it rain?", u"today it will be mostly sunny in stuttgart with little precipitation")], prep=prep_time_a)
    k.dte.ts('en', 't0013', [(u"is rain coming?", u"today it will be mostly sunny in stuttgart with little precipitation")], prep=prep_time_a)

    k.dte.dt('en', [u"what (will the weather|is the weather gonna|is the weather going to) be like ?", 
                    u"how (cold|warm) (is it going to|will it) (be|become) ?", 
                    u"(what will the weather be|what is the weather gonna be|what is the weather going to be) (like|) ?", 
                    u"what (is the weather outlook | does the weather forecast look like | is the weather forecast | does the weather forecast say) ?", 
                    u"(and|) how is the weather (there|then|)?", 
                    u"(and|) what is the weather like (there|then|)?",
                    u"(how|what|) about the weather",
                    u"do you known what the weather (will be like|is going to be)?"],
                   answer_weather, ['full', -1, -1, None, False])

    k.dte.ts('en', 't0007', [(u"what will the weather be like?", u"today will be mostly clear skies in stuttgart with temperatures between minus eight and four degrees")], prep=prep_time_a)
    k.dte.ts('en', 't0015', [(u"how warm will it be ?", u"today will be mostly clear skies in stuttgart with temperatures between minus eight and four degrees")], prep=prep_time_a)

    k.dte.ts('en', 't0017', [(u"what will the weather be like?", u"today will be mostly clear skies in stuttgart with temperatures between minus eight and four degrees")], prep=prep_time_a)
    k.dte.ts('en', 't0021', [(u"what does the weather forecast say?", u"today will be mostly clear skies in Stuttgart with temperatures between -8 and 4 degrees.")], prep=prep_time_a)
 
    k.dte.dt('de', [u"wird es (regnen|Regen geben) ?", 
                    u"(was ist die Wahrscheinlichkeit für|wie groß ist die Wahrscheinlichkeit für|wie wahrscheinlich ist) Regen ?", 
                    u"wie wahrscheinlich ist es, dass es regnen wird?", 
                    u"scheint die Sonne?", 
                    u"regnet es ?", 
                    u"kommt noch Regen ?"],
                   answer_weather, ['prec_cloud', -1, -1, None, False])

    k.dte.ts('de', 't0002', [(u"wird es regnen?", u"heute scheint in stuttgart überwiegend die sonne und es wird kaum niederschlag geben")], prep=prep_time_a)
    k.dte.ts('de', 't0004', [(u"wie groß ist die Wahrscheinlichkeit für Regen?", u"heute scheint in stuttgart überwiegend die sonne und es wird kaum niederschlag geben")], prep=prep_time_a)

    k.dte.ts('de', 't0006', [(u"wie wahrscheinlich ist es, dass es regnen wird?", u"heute scheint in stuttgart überwiegend die sonne und es wird kaum niederschlag geben")], prep=prep_time_a)
    k.dte.ts('de', 't0010', [(u"scheint die Sonne?", u"heute scheint in stuttgart überwiegend die sonne und es wird kaum niederschlag geben")], prep=prep_time_a)

    k.dte.ts('de', 't0012', [(u"Regnet es?", u"heute scheint in stuttgart überwiegend die sonne und es wird kaum niederschlag geben")], prep=prep_time_a)
    k.dte.ts('de', 't0014', [(u"kommt noch Regen?", u"heute scheint in stuttgart überwiegend die sonne und es wird kaum niederschlag geben")], prep=prep_time_a)

    k.dte.dt('de', [u"wie (ist|ist denn|wird) das Wetter (werden|)?", 
                    u"wie (kalt|warm) wird es (werden|) ?", 
                    u"(wie sind die Wetteraussichten | was sagt die Wettervorhersage | was sagt der Wetterbericht ) ?", 
                    u"(und|) wie (ist das Wetter|sieht das Wetter aus|wie wird das wetter) (dort|dann|)?",
                    u"(was ist mit dem|über das) wetter?",
                    u"Weißt Du, wie das Wetter (werden|) wird?"],
                   answer_weather, ['full', -1, -1, None, False])

    k.dte.ts('de', 't0008', [(u"wie wird das Wetter werden?", u"heute wird es wenige wolken geben in stuttgart und es wird zwischen minus acht und vier grad warm")], prep=prep_time_a)
    k.dte.ts('de', 't0016', [(u"wie warm wird es?", u"heute wird es wenige wolken geben in stuttgart und es wird zwischen minus acht und vier grad warm")], prep=prep_time_a)

    k.dte.ts('de', 't0018', [(u"wie wird das Wetter?", u"heute wird es wenige wolken geben in stuttgart und es wird zwischen minus acht und vier grad warm")], prep=prep_time_a)
    k.dte.ts('de', 't0022', [(u"was sagt der Wetterbericht?", u"heute wird es wenige wolken geben in stuttgart und es wird zwischen minus acht und vier grad warm")], prep=prep_time_a)

    k.dte.dt('en', [u"(what is the likelihood of | how likely is) rain {timespec:LABEL} ?", 
                    u"How likely is it that it will rain {timespec:LABEL}?", 
                    u"(will the sun shine|will there be sunshine) {timespec:LABEL} ?", 
                    u"(will it|does it) rain {timespec:LABEL}?", 
                    u"(will rain come|is rain coming) {timespec:LABEL}?"],
                   answer_weather, ['prec_cloud', -1, -1, 'timespec_0_time', False])

    k.dte.ts('en', 't0100', [(u"will it rain tomorrow?", u"tomorrow it will be mostly sunny in stuttgart with little precipitation")], prep=prep_time_a)
    k.dte.ts('en', 't0102', [(u"how likely is rain the day after tomorrow?", u"day after tomorrow it will be mostly sunny in Stuttgart with little precipitation.")], prep=prep_time_a)

    k.dte.ts('en', 't0104', [(u"how likely is it that it will rain today?", u"today it will be mostly sunny in stuttgart with little precipitation")], prep=prep_time_a)
    k.dte.ts('en', 't0108', [(u"will there be sunshine the day after tomorrow?", u"day after tomorrow it will be mostly sunny in Stuttgart with little precipitation.")], prep=prep_time_a)

    k.dte.ts('en', 't0110', [(u"Will it rain today?", u"today it will be mostly sunny in stuttgart with little precipitation")], prep=prep_time_a)
    k.dte.ts('en', 't0112', [(u"is rain coming tomorrow?", u"tomorrow it will be mostly sunny in stuttgart with little precipitation")], prep=prep_time_a)
 
    k.dte.dt('en', [u"what (will the weather|is the weather gonna|is the weather going to) be like {timespec:LABEL} ?", 
                    u"how (cold|warm) (is it going to|will it) (be|become) {timespec:LABEL}?", 
                    u"what (is the weather outlook|does the weather forecast look like|is the weather forecast|does the weather forecast say) for {timespec:LABEL} ?", 
                    u"(and|) how is the weather {timespec:LABEL} ?",
                    u"(and|) what is the weather like (there|then|) {timespec:LABEL} ?",
                    u"(how|what|) about the weather {timespec:LABEL} ",
                    u"do you known what the weather (will be like|is going to be) {timespec:LABEL} ?"],
                   answer_weather, ['full', -1, -1, 'timespec_0_time', False])

    k.dte.ts('en', 't0106', [(u"what will the weather be like tomorrow?", u"tomorrow will be mostly clear skies in stuttgart with temperatures between minus eight and four degrees")], prep=prep_time_a)
    k.dte.ts('en', 't0114', [(u"how warm will it be the day after tomorrow?", u"day after tomorrow will be mostly clear skies in stuttgart with temperatures between minus eight and four degrees")], prep=prep_time_a)

    k.dte.ts('en', 't0116', [(u"what will the weather be like today?", u"today will be mostly clear skies in stuttgart with temperatures between minus eight and four degrees")], prep=prep_time_a)
    k.dte.ts('en', 't0118', [(u"what is the weather gonna be like tomorrow?", u"tomorrow will be mostly clear skies in stuttgart with temperatures between minus eight and four degrees")], prep=prep_time_a)

    k.dte.ts('en', 't0120', [(u"what does the weather forecast say for today?", u"today will be mostly clear skies in stuttgart with temperatures between minus eight and four degrees")], prep=prep_time_a)

    k.dte.dt('de', [u"wird es {timespec:LABEL} (regnen|Regen geben)?", 
                    u"(was ist die Wahrscheinlichkeit für|wie groß ist die Wahrscheinlichkeit für|wie wahrscheinlich ist) Regen {timespec:LABEL} ?", 
                    u"Wie wahrscheinlich ist es, dass es {timespec:LABEL} regnen wird?", 
                    u"scheint {timespec:LABEL} die Sonne?", 
                    u"regnet es {timespec:LABEL}?", 
                    u"kommt {timespec:LABEL} noch Regen ?"],
                   answer_weather, ['prec_cloud', -1, -1, 'timespec_0_time', False])

    k.dte.dt('de', [u"wie wird {timespec:LABEL} das Wetter?", 
                    u"wie (kalt|warm) wird es {timespec:LABEL} (werden|)?", 
                    u"wie (ist|wird|ist denn) das Wetter {timespec:LABEL}?", 
                    u"(wie sind die Wetteraussichten|was sagt die Wettervorhersage|was sagt der Wetterbericht) für {timespec:LABEL} ?"],
                   answer_weather, ['full', -1, -1, 'timespec_0_time', False])

    k.dte.ts('de', 't0101', [(u"wird es morgen regnen?", u"morgen scheint in stuttgart überwiegend die sonne und es wird kaum niederschlag geben")], prep=prep_time_a)

    k.dte.ts('de', 't0103', [(u"wie groß ist die Wahrscheinlichkeit für Regen übermorgen?", u"übermorgen scheint in stuttgart überwiegend die sonne und es wird kaum niederschlag geben")], prep=prep_time_a)
    k.dte.ts('de', 't0105', [(u"wie wahrscheinlich ist es, dass es heute regnen wird?", u"heute scheint in stuttgart überwiegend die sonne und es wird kaum niederschlag geben")], prep=prep_time_a)

    k.dte.ts('de', 't0107', [(u"wie wird morgen das Wetter?", u"morgen wird es wenige wolken geben in stuttgart und es wird zwischen minus acht und vier grad warm")], prep=prep_time_a)
    k.dte.ts('de', 't0109', [(u"scheint übermorgen die Sonne?", u"übermorgen scheint in stuttgart überwiegend die sonne und es wird kaum niederschlag geben")], prep=prep_time_a)

    k.dte.ts('de', 't0111', [(u"Regnet es heute?", u"heute scheint in stuttgart überwiegend die sonne und es wird kaum niederschlag geben")], prep=prep_time_a)
    k.dte.ts('de', 't0113', [(u"kommt morgen noch Regen?", u"morgen scheint in stuttgart überwiegend die sonne und es wird kaum niederschlag geben")], prep=prep_time_a)

    k.dte.ts('de', 't0115', [(u"wie warm wird es übermorgen?", u"übermorgen wird es wenige wolken geben in stuttgart und es wird zwischen minus acht und vier grad warm")], prep=prep_time_a)
    k.dte.ts('de', 't0117', [(u"wie wird das Wetter heute?", u"heute wird es wenige wolken geben in stuttgart und es wird zwischen minus acht und vier grad warm")], prep=prep_time_a)

    k.dte.ts('de', 't0119', [(u"wie wird das Wetter morgen?", u"morgen wird es wenige wolken geben in stuttgart und es wird zwischen minus acht und vier grad warm")], prep=prep_time_a)
    k.dte.ts('de', 't0121', [(u"was sagt der Wetterbericht für heute?", u"heute wird es wenige wolken geben in stuttgart und es wird zwischen minus acht und vier grad warm")], prep=prep_time_a)

    k.dte.dt('en', [u"(what is the likelihood of | how likely is) rain in {weather_location:LABEL} ?", 
                    u"how likely is it that it will rain in {weather_location:LABEL} ?", 
                    u"(will the sun shine | will there be sunshine )  in {weather_location:LABEL} ?", 
                    u"(will it | does it) rain in {weather_location:LABEL} ?", 
                    u"(will rain come|is rain coming) in {weather_location:LABEL} ?", 
                    u"how (cold|warm) (is it going to|will it) (be|become) in {weather_location:LABEL}?"],
                   answer_weather, ['prec_cloud', 'weather_location_0_start', 'weather_location_0_end', None, False])

    k.dte.ts('en', 't0200', [(u"will it rain in Freudental?", u"today it will be mostly sunny in freudental with little precipitation")], prep=prep_time_a)
    k.dte.ts('en', 't0202', [(u"how likely is rain in Stuttgart?", u"today it will be mostly sunny in stuttgart with little precipitation")], prep=prep_time_a)

    k.dte.ts('en', 't0204', [(u"how likely is it that it will rain in Freudental?", u"today it will be mostly sunny in Freudental with little precipitation.")], prep=prep_time_a)
    k.dte.ts('en', 't0208', [(u"will there be sunshine in stuttgart?", u"today it will be mostly sunny in stuttgart with little precipitation")], prep=prep_time_a)

    k.dte.ts('en', 't0210', [(u"Will it rain in Freudental?", u"today it will be mostly sunny in Freudental with little precipitation.")], prep=prep_time_a)
    k.dte.ts('en', 't0212', [(u"is rain coming in Tallinn?", u"today it will be mostly sunny in tallinn with little precipitation")], prep=prep_time_a)

    k.dte.ts('en', 't0214', [(u"how warm will it be in Stuttgart?", u"today it will be mostly sunny in stuttgart with little precipitation")], prep=prep_time_a)
    
    k.dte.dt('en', [u"what ( will the weather | is the weather gonna | is the weather going to ) be (like|) in {weather_location:LABEL} ?", 
                    u"how (cold|warm) (is it going to|will it) (be|become) in {weather_location:LABEL} ?", 
                    u"what (is the weather outlook|does the weather forecast look like|is the weather forecast|does the weather forecast say) for {weather_location:LABEL} ?", 
                    u"How is the weather in {weather_location:LABEL} ?",
                    u"(How|What) about the weather in {weather_location:LABEL} ?"],
                   answer_weather, ['full', 'weather_location_0_start', 'weather_location_0_end', None, False])

    k.dte.ts('en', 't0206', [(u"what will the weather be like in Tallinn?", u"today will be mostly clear skies in tallinn with temperatures between minus eight and four degrees")], prep=prep_time_a)

    k.dte.ts('en', 't0216', [(u"what will the weather be like in Tallinn?", u"today will be mostly clear skies in tallinn with temperatures between minus eight and four degrees")], prep=prep_time_a)
    k.dte.ts('en', 't0218', [(u"what is the weather gonna be like in stuttgart?", u"today will be mostly clear skies in stuttgart with temperatures between minus eight and four degrees")], prep=prep_time_a)

    k.dte.ts('en', 't0220', [(u"what does the weather forecast say for stuttgart?", u"today will be mostly clear skies in stuttgart with temperatures between minus eight and four degrees")], prep=prep_time_a)

    k.dte.dt('de', [u"wird es in {weather_location:LABEL} (regnen | Regen geben) ?", 
                    u"( was ist die Wahrscheinlichkeit für | wie groß ist die Wahrscheinlichkeit für | wie wahrscheinlich ist ) Regen in {weather_location:LABEL} ?", 
                    u"wie wahrscheinlich ist es, dass es in {weather_location:LABEL} regnen wird?", 
                    u"scheint in {weather_location:LABEL} die Sonne?", 
                    u"regnet es in {weather_location:LABEL} ?", 
                    u"kommt noch Regen in {weather_location:LABEL} ?", 
                    u"wie (kalt|warm) wird es in {weather_location:LABEL} (werden|)?",
                    u"was ist mit dem Wetter in {weather_location:LABEL}?",
                    u"Weißt Du, wie das Wetter (werden|) wird in {weather_location:LABEL}?"],
                   answer_weather, ['prec_cloud', 'weather_location_0_start', 'weather_location_0_end', None, False])

    k.dte.ts('de', 't0201', [(u"wird es in Freudental regnen?", u"heute scheint in freudental überwiegend die sonne und es wird kaum niederschlag geben")], prep=prep_time_a)

    k.dte.ts('de', 't0203', [(u"wie groß ist die Wahrscheinlichkeit für Regen in Stuttgart?", u"heute scheint in stuttgart überwiegend die sonne und es wird kaum niederschlag geben")], prep=prep_time_a)
    k.dte.ts('de', 't0205', [(u"wie wahrscheinlich ist es, dass es in Freudental regnen wird?", u"heute scheint in freudental überwiegend die sonne und es wird kaum niederschlag geben")], prep=prep_time_a)

    k.dte.ts('de', 't0209', [(u"scheint in Stuttgart die Sonne?", u"heute scheint in stuttgart überwiegend die sonne und es wird kaum niederschlag geben")], prep=prep_time_a)
    k.dte.ts('de', 't0211', [(u"Regnet es in Freudental?", u"heute scheint in freudental überwiegend die sonne und es wird kaum niederschlag geben")], prep=prep_time_a)

    k.dte.ts('de', 't0213', [(u"kommt noch Regen in Tallinn?", u"heute scheint in tallinn überwiegend die sonne und es wird kaum niederschlag geben")], prep=prep_time_a)
    k.dte.ts('de', 't0215', [(u"wie warm wird es in Stuttgart?", u"heute scheint in stuttgart überwiegend die sonne und es wird kaum niederschlag geben")], prep=prep_time_a)

    k.dte.dt('de', [u"wie (ist|ist denn|wird) in {weather_location:LABEL} das Wetter?", 
                    u"wie (ist|ist denn|wird) das Wetter in {weather_location:LABEL}?", 
                    u"(wie sind die Wetteraussichten|was sagt die Wettervorhersage|was sagt der Wetterbericht) für {weather_location:LABEL}?"],
                   answer_weather, ['full', 'weather_location_0_start', 'weather_location_0_end', None, False])

    k.dte.ts('de', 't0207', [(u"wie wird in Tallinn das Wetter?", u"heute wird es wenige wolken geben in tallinn und es wird zwischen minus acht und vier grad warm")], prep=prep_time_a)
    k.dte.ts('de', 't0217', [(u"wie wird das Wetter in Tallinn?", u"heute wird es wenige wolken geben in tallinn und es wird zwischen minus acht und vier grad warm")], prep=prep_time_a)

    k.dte.ts('de', 't0219', [(u"wie wird das Wetter in Stuttgart?", u"heute wird es wenige wolken geben in stuttgart und es wird zwischen minus acht und vier grad warm")], prep=prep_time_a)
    k.dte.ts('de', 't0221', [(u"was sagt der Wetterbericht für Stuttgart?", u"heute wird es wenige wolken geben in stuttgart und es wird zwischen minus acht und vier grad warm")], prep=prep_time_a)

    k.dte.dt('en', [u"will it rain in {weather_location:LABEL} {timespec:LABEL} ?", 
                    u"(what is the likelihood of | how likely is | rain in ) {weather_location:LABEL} {timespec:LABEL} ?", 
                    u"how likely is it that it will rain {timespec:LABEL} in {weather_location:LABEL} ?", 
                    u"(will the sun shine | will there be sunshine ) {timespec:LABEL}  in {weather_location:LABEL} ?", 
                    u"(will it | does it) rain in {weather_location:LABEL} {timespec:LABEL} ?", 
                    u"(will rain come|is rain coming) in {weather_location:LABEL} {timespec:LABEL} ?"],
                   answer_weather, ['prec_cloud', 'weather_location_0_start', 'weather_location_0_end', 'timespec_0_time', False])

    k.dte.dt('en', [u"what ( will the weather | is the weather gonna | is the weather going to ) be like {timespec:LABEL} in {weather_location:LABEL} ?", 
                    u"how (cold|warm) (is it going to|will it) (be|become) in {weather_location:LABEL} {timespec:LABEL}?", 
                    u"(what will the weather be|what is the weather gonna be|what is the weather going to be) (like|) in {weather_location:LABEL} {timespec:LABEL} ?", 
                    u"what (is the weather outlook|does the weather forecast look like|is the weather forecast|does the weather forecast say) for {weather_location:LABEL} {timespec:LABEL} ?", 
                    u"How is the weather in {weather_location:LABEL} {timespec:LABEL}?",
                    u"(What|how) about the weather in {weather_location:LABEL} {timespec:LABEL} ?"],
                   answer_weather, ['full', 'weather_location_0_start', 'weather_location_0_end', 'timespec_0_time', False])

    k.dte.dt('de', [u"kommt {timespec:LABEL} noch Regen in {weather_location:LABEL} ?", 
                    u"regnet es {timespec:LABEL} in {weather_location:LABEL} ?", 
                    u"scheint in {weather_location:LABEL} {timespec:LABEL} die Sonne?", 
                    u"wie wahrscheinlich ist es, dass es {timespec:LABEL} in {weather_location:LABEL} regnen wird?", 
                    u"wird es {timespec:LABEL} in {weather_location:LABEL} (regnen | Regen geben) ?", 
                    u"( was ist die Wahrscheinlichkeit für | wie groß ist die Wahrscheinlichkeit für | wie wahrscheinlich ist ) Regen {timespec:LABEL} in {weather_location:LABEL} ?"],
                   answer_weather, ['prec_cloud', 'weather_location_0_start', 'weather_location_0_end', 'timespec_0_time', False])

    k.dte.dt('de', [u"wie (kalt|warm) wird es {timespec:LABEL} in {weather_location:LABEL} werden?", 
                    u"wie (ist|ist denn|wird) {timespec:LABEL} in {weather_location:LABEL} das Wetter?", 
                    u"wie (ist|ist denn|wird) {timespec:LABEL} das Wetter in {weather_location:LABEL}?", 
                    u"wie wird das Wetter {timespec:LABEL} in {weather_location:LABEL}?", 
                    u"(wie sind die Wetteraussichten|was sagt die Wettervorhersage|was sagt der Wetterbericht) für {timespec:LABEL} (in|für) {weather_location:LABEL}?",
                    u"(Was ist mit dem|über das) Wetter für {timespec:LABEL} (in|für) {weather_location:LABEL}?",
                    u"Weißt Du, wie das Wetter für {timespec:LABEL} (in|für) {weather_location:LABEL} (werden|) wird?"],
                   answer_weather, ['full', 'weather_location_0_start', 'weather_location_0_end', 'timespec_0_time', False])

    k.dte.ts('en', 't0300', [(u"what does the weather forecast say for stuttgart tomorrow?", u"tomorrow will be mostly clear skies in stuttgart with temperatures between minus eight and four degrees")], prep=prep_time_a)
    k.dte.ts('de', 't0301', [(u"was sagt der Wetterbericht für heute für Tallinn?", u"heute wird es wenige wolken geben in tallinn und es wird zwischen minus acht und vier grad warm")], prep=prep_time_a)

    k.dte.dt('en', u"(and|) {timespec:LABEL}", answer_weather, ['full', -1, -1, 'timespec_0_time', True])
    k.dte.dt('de', u"(und|) {timespec:LABEL}", answer_weather, ['full', -1, -1, 'timespec_0_time', True])

    k.dte.dt('en', u"(and|) in {weather_location:LABEL} ?", answer_weather, ['full', 'weather_location_0_start', 'weather_location_0_end', None, True])
    k.dte.dt('de', u"(und|) in {weather_location:LABEL} ?", answer_weather, ['full', 'weather_location_0_start', 'weather_location_0_end', None, True])

    k.dte.dt('en', [u"that is (definitely|) (pretty|too) (cold|warm|hot)", 
                    u"that is too (cold|warm|hot) for (me|my taste)"],
                   [u"Proper clothing will fix that.", 
                    u"The weather service will hear about that.", 
                    u"Maybe you should move to a milder climate?"])
    k.dte.dt('de', [u"das ist (ja|) (ganz schön|zu|) (warm|kalt|heiß)", 
                    u"das ist mir zu (warm|kalt|heiß)"],
                   [u"Alles eine Frage der richtigen Kleidung!", 
                    u"Ich sende eine Beschwerde an das Wetteramt.", 
                    u"Vielleicht solltest Du über einen Umzug nachdenken?"])

    k.dte.dt('en', u"the weather is bad", u"So let's stay inside and chat some more!")
    k.dte.dt('de', u"das wetter ist schlecht", u"Dann lass uns drinnen bleiben und noch ein wenig reden!")

