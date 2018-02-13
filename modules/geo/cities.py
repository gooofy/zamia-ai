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

MACRO_LIMIT = 12

def get_data(k):

    k.dte.set_prefixes([u''])

    # NER, macros

    for lang in ['en', 'de']:
        cnt = 0
        for res in k.prolog_query("instances_of(wdeCity, CITY), rdfsLabel(CITY, %s, LABEL)." % lang):
            s_city  = res[0] 
            s_label = res[1] 
            k.dte.ner(lang, 'city', s_city, s_label)
            if cnt < MACRO_LIMIT:
                k.dte.macro(lang, 'cities', {'LABEL': s_label})
            cnt += 1

    def city_location(c, ts, te, check_topic):

        def act(c, city):
            c.kernal.mem_push(c.user, 'f1ent', city)

        if check_topic:
            f1ent = c.kernal.mem_get_multi(c.user, 'f1ent')
            if not f1ent:
                return
            f1ent = f1ent[0][0]
            if not c.kernal.prolog_check('instances_of(%s, %s).' % ('wdeCity', f1ent)):
                return

        if ts>=0:
            fss = c.ner(c.lang, 'city', ts, te)
        else:
            fss = c.kernal.mem_get_multi(c.user, 'f1ent')

        # import pdb; pdb.set_trace()

        for city, score in fss:
            clabel  = c.kernal.prolog_query_one('rdfsLabel(%s, %s, L).' % (city, c.lang))
            country = c.kernal.prolog_query_one("wdpdCountry(%s, COUNTRY)." % city)
            if clabel and country:
                cylabel = c.kernal.prolog_query_one('rdfsLabel(%s, %s, L).' % (country, c.lang))

                if c.lang=='de':
                    c.resp(u"%s ist eine Stadt in %s." % (clabel, cylabel), score=score, action=act, action_arg=city)
                else:
                    c.resp(u"%s is a city in %s." % (clabel, cylabel), score=score, action=act, action_arg=city)

    k.dte.dt('en', u"(what is|what about|what do you know about|where is|in what country is|in|do you know|do you know the city|over|) {cities:LABEL} (and you|) (again|then|do you know it|do you know that|)?",
                   city_location, ['cities_0_start', 'cities_0_end', False])
    k.dte.dt('de', u"(was ist|was ist mit|was weißt Du über|wo ist|wo liegt|in|in welchem land ist|kennst du|kennst du die stadt|über|) {cities:LABEL} (nochmal|denn|und du|kennst Du das|)?",
                   city_location, ['cities_0_start', 'cities_0_end', False])

    k.dte.ts('en', 'c0000', [(u"What is Tallinn?", u"Tallinn is a city in Estonia")])
    k.dte.ts('de', 'c0001', [(u"Wo ist Tallinn?", u"Tallinn ist eine Stadt in Estland.")])

    k.dte.dt('en', u"(and|) (in|) (a|which) (town|city)?",
                   [u"Which city comes to mind?",
                    u"The city of your dreams, perhaps?"])
    k.dte.dt('en', [u"(and|) (in|) (a|which) (town|city)?",
                    u"(and|) (What|where) (is|was) (it|that) (again|)?"],
                   city_location, [-1, -1, True])
    k.dte.dt('de', u"(und|) (in|) (einer|welcher) Stadt?",
                   [u"An welche Stadt denkst Du?",
                    u"Die Stadt Deiner Träume, möglicherweise?"])
    k.dte.dt('de', [u"(und|) (in einer|in welcher|welche|eine|) Stadt?",
                    u"(und|) (Wo|Was) (ist|war) (das|es) (nochmal|)?"],
                   city_location, [-1, -1, True])

    def city_population(c, ts, te, check_topic):

        def act(c, city):
            c.kernal.mem_push(c.user, 'f1ent', city)

        if check_topic:
            f1ent = c.kernal.mem_get_multi(c.user, 'f1ent')
            if not f1ent:
                return
            f1ent = f1ent[0][0]
            if not c.kernal.prolog_check('instances_of(%s, %s).' % ('wdeCity', f1ent)):
                return

        if ts>=0:
            fss = c.ner(c.lang, 'city', ts, te)
        else:
            fss = c.kernal.mem_get_multi(c.user, 'f1ent')

        # import pdb; pdb.set_trace()

        for city, score in fss:
            clabel     = c.kernal.prolog_query_one('rdfsLabel(%s, %s, L).' % (city, c.lang))
            population = c.kernal.prolog_query_one("wdpdPopulation(%s, POPULATION)." % city)
            if clabel and population:
                if c.lang=='de':
                    c.resp(u"%s hat %d Einwohner." % (clabel, population), score=score, action=act, action_arg=city)
                else:
                    c.resp(u"The population of %s is %d." % (clabel, population), score=score, action=act, action_arg=city)

    k.dte.dt('en', u"(what is the population of |how many people live in | how many humans reside in) {cities:LABEL} (do you know it|do you know that|)?",
                   city_population, ['cities_0_start', 'cities_0_end', False])
    k.dte.dt('de', u"(wie hoch ist die bevölkerung von|wie ist die bevölkerung von|wie viele menschen leben in|wie viele leute leben in|wie viele Einwohner hat) {cities:LABEL} (weißt Du das|)?",
                   city_population, ['cities_0_start', 'cities_0_end', False])

    k.dte.ts('en', 'c0002', [(u"How many people live in Tallinn?", u"The population of Tallinn is 446055")])
    k.dte.ts('de', 'c0003', [(u"Wie viele Menschen leben in Tallinn?", u"Tallinn hat 446055 Einwohner.")])

    k.dte.dt('en', [u"(and|) (what is the population of |how many people live in | how many humans reside in) it (do you know it|do you know that|)?",
                    u"(and|) how many residents does it have (do you know it|do you know that|)?",
                    u"(and|) how many people live there (do you know it|do you know that|)?"],
                   city_population, [-1, -1, True])
    k.dte.dt('de', u"(und|) (wie hoch ist die Bevölkerung von|wie ist die Bevölkerung von|wie viele Menschen leben |wie viele Leute leben |wie viele Einwohner hat es) dort (weißt Du das|)?",
                   city_population, [-1, -1, True])

    def city_area(c, ts, te, check_topic):

        def act(c, city):
            c.kernal.mem_push(c.user, 'f1ent', city)

        if check_topic:
            f1ent = c.kernal.mem_get_multi(c.user, 'f1ent')
            if not f1ent:
                return
            f1ent = f1ent[0][0]
            if not c.kernal.prolog_check('instances_of(%s, %s).' % ('wdeCity', f1ent)):
                return

        if ts>=0:
            fss = c.ner(c.lang, 'city', ts, te)
        else:
            fss = c.kernal.mem_get_multi(c.user, 'f1ent')

        # import pdb; pdb.set_trace()

        for city, score in fss:
            clabel = c.kernal.prolog_query_one('rdfsLabel(%s, %s, L).' % (city, c.lang))
            area   = c.kernal.prolog_query_one("wdpdArea(%s, AREA)." % city)
            if clabel and area:
                if c.lang=='de':
                    c.resp(u"Die Fläche von %s ist %d Quadratkilometer." % (clabel, area), score=score, action=act, action_arg=city)
                else:
                    c.resp(u"The area of %s is %d square kilometers." % (clabel, area), score=score, action=act, action_arg=city)

    k.dte.dt('en', u"(what is the area of |how big is|what is the size of) {cities:LABEL} (do you know it|do you know that|)?",
                   city_area, ['cities_0_start', 'cities_0_end', False])
    k.dte.dt('de', u"(wie groß ist|wie ist die fläche von|wie groß ist die fläche von|wie viele quadratmeter hat) {cities:LABEL} (weißt Du das|)?",
                   city_area, ['cities_0_start', 'cities_0_end', False])

    k.dte.ts('en', 'd0002', [(u"How big is London?", u"The area of London is 1572 square kilometers")])
    k.dte.ts('de', 'd0003', [(u"Wie groß ist London?", u"Die Fläche von London ist 1572 Quadratkilometer.")])

    k.dte.dt('en', u"(and|) (what is the area of |how big is | what is the size of) it (do you know it|do you know that|)?",
                   city_area, [-1, -1, True])
    k.dte.dt('de', u"(und|) (wie groß ist es|wie ist die fläche|wie viele quadratmeter hat es|wie groß ist die fläche) (weißt Du das|)?",
                   city_area, [-1, -1, True])

    k.dte.ts('en', 'c0004', [(u"What about Berlin?", u"Berlin is a city in Germany."),
                               (u"Which city?", u"Berlin is a city in Germany."),
                               (u"What was our topic?", u"We have been talking about Berlin, I think."),
                               (u"How many people live there?", u"The population of Berlin is 3469849"),
                               (u"And where is it again?", u"Berlin is a city in Germany"),
                               (u"And what is the size of it?", u"The area of Berlin is 891 square kilometers.")])
    k.dte.ts('de', 'c0005', [(u"Was ist mit Berlin?", u"Berlin ist eine Stadt in Deutschland"),
                               (u"Welche Stadt?", u"Berlin ist eine Stadt in Deutschland."),
                               (u"Was war unser Thema?", u"Wir hatten über Berlin gesprochen, glaube ich."),
                               (u"Wie viele Menschen leben dort?", u"Berlin hat 3469849 Einwohner."),
                               (u"Und wo ist es nochmal?", u"Berlin ist eine Stadt in Deutschland"),
                               (u"Und wie groß ist die Fläche?", u"Die Fläche von Berlin ist 891 Quadratkilometer.")])

    k.dte.dt('en', u"(what are the coordinates of|coordinates of) {cities:LABEL} (please|) ?", u"sorry, I do not have geo coordinates in my database yet.")
    k.dte.dt('de', u"(wie sind die koordinaten von|was sind die koordinaten von|koordinaten von) {cities:LABEL} (bitte|)?", u"tut mir leid, ich habe keine geo koordinaten in meiner datenbank")

    k.dte.dt('en', u"the expo takes place in Hanover", u"Have you been there?")
    k.dte.dt('de', u"in hannover findet die expo statt", u"Warst Du da schon mal?")

