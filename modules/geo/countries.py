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

    # NER, macros

    for lang in ['en', 'de']:
        for res in k.prolog_query("instances_of(wdeCountry, COUNTRY), rdfsLabel(COUNTRY, %s, LABEL)." % lang):
            s_country = res[0] 
            s_label   = res[1] 
            k.dte.ner(lang, 'country', s_country, s_label)
            k.dte.macro(lang, 'countries', {'LABEL': s_label})

    def country_location(c, ts, te, check_topic):

        def act(c, country):
            c.kernal.mem_push(c.user, 'f1ent', country)

        if check_topic:
            f1ent = c.kernal.mem_get_multi(c.user, 'f1ent')
            if not f1ent:
                return
            f1ent = f1ent[0][0]
            if not c.kernal.prolog_check('instances_of(%s, %s).' % ('wdeCountry', f1ent)):
                return

        if ts>=0:
            fss = c.ner(c.lang, 'country', ts, te)
        else:
            fss = c.kernal.mem_get_multi(c.user, 'f1ent')

        # import pdb; pdb.set_trace()

        for country, score in fss:
            clabel  = c.kernal.prolog_query_one('rdfsLabel(%s, %s, L).' % (country, c.lang))
            if clabel:
                if c.lang=='de':
                    c.resp(u"%s ist ein Staat auf dem Planeten Erde." % clabel, score=score, action=act, action_arg=country)
                else:
                    c.resp(u"%s is a country on planet earth." % clabel, score=score, action=act, action_arg=country)

    k.dte.dt('en', u"(what is|what about|what do you know about|where is|in what continent is|in|) {countries:LABEL} (and you|) (do you know it|do you know that|)?",
                   country_location, ['countries_0_start', 'countries_0_end', False])
    k.dte.dt('de', u"(was ist|was ist mit|was weißt Du über|wo ist|wo liegt|in|auf welchem Kontinent ist|) {countries:LABEL} (und du|weißt Du das|)?",
                   country_location, ['countries_0_start', 'countries_0_end', False])

    k.dte.ts('en', 'd0000', [(u"What is Finland?", u"Finland is a country on planet earth")])
    k.dte.ts('de', 'd0001', [(u"Wo ist Finnland?", u"Finnland ist ein Staat auf dem Planeten Erde.")])

    k.dte.dt('en', u"(and|) (in|) (a|which) country?",
                   [u"Which country comes to mind?",
                    u"Which country do you like best?"])
    k.dte.dt('en', [u"(and|) (in|) (a|which) country?", 
                    u"(and|) (where|What) (is|was) (it|that) (again|)?"],
                   country_location, [-1, -1, True])

    k.dte.dt('de', u"(und|) (in|) (einem|welchen|welcher) Staat?",
                   [u"An welchen Staat denkst Du?",
                    u"Aus welchem Staat kommst Du?"])
    k.dte.dt('de', [u"(und|) (in|) (einem|welchen|welcher) Staat?",
                    u"(und|) (was|wo) (ist|war) (das|es) (nochmal|)?",
                    u"(und|) Wo liegt (das|es) (nochmal|)?"],
                   country_location, [-1, -1, True])

    def country_population(c, ts, te, check_topic):

        def act(c, country):
            c.kernal.mem_push(c.user, 'f1ent', country)

        if check_topic:
            f1ent = c.kernal.mem_get_multi(c.user, 'f1ent')
            if not f1ent:
                return
            f1ent = f1ent[0][0]
            if not c.kernal.prolog_check('instances_of(%s, %s).' % ('wdeCountry', f1ent)):
                return

        if ts>=0:
            fss = c.ner(c.lang, 'country', ts, te)
        else:
            fss = c.kernal.mem_get_multi(c.user, 'f1ent')

        # import pdb; pdb.set_trace()

        for country, score in fss:
            clabel     = c.kernal.prolog_query_one('rdfsLabel(%s, %s, L).' % (country, c.lang))
            population = c.kernal.prolog_query_one("wdpdPopulation(%s, POPULATION)." % country)
            if clabel and population:
                if c.lang=='de':
                    c.resp(u"%s hat %d Einwohner." % (clabel, population), score=score, action=act, action_arg=country)
                else:
                    c.resp(u"The population of %s is %d." % (clabel, population), score=score, action=act, action_arg=country)

    k.dte.dt('en', u"(what is the population of |how many people live in | how many humans reside in) {countries:LABEL} (do you know it|do you know that|)?",
                   country_population, ['countries_0_start', 'countries_0_end', False])
    k.dte.dt('de', u"(wie hoch ist die bevölkerung von|wie ist die bevölkerung von|wie viele menschen leben in|wie viele leute leben in|wie viele Einwohner hat) {countries:LABEL} (weißt Du das|)?",
                   country_population, ['countries_0_start', 'countries_0_end', False])
 
    k.dte.ts('en', 'd0002', [(u"How many people live in Estonia?", u"The population of Estonia is 1315635")])
    k.dte.ts('de', 'd0003', [(u"Wie viele Menschen leben in Estland?", u"Estland hat 1315635 Einwohner.")])

    k.dte.dt('en', [u"(and|) (what is the population of |how many people live in | how many humans reside in) it (do you know it|do you know that|)?",
                    u"(and|) how many residents does it have (do you know it|do you know that|)?",
                    u"(and|) how many people live there (do you know it|do you know that|)?"],
                   country_population, [-1, -1, True])
    k.dte.dt('de', u"(und|) (wie hoch ist die bevölkerung von|wie ist die bevölkerung von|wie viele menschen leben |wie viele leute leben |wie viele Einwohner hat es) dort (weißt Du das|)?",
                   country_population, [-1, -1, True])

    def country_area(c, ts, te, check_topic):

        def act(c, country):
            c.kernal.mem_push(c.user, 'f1ent', country)

        if check_topic:
            f1ent = c.kernal.mem_get_multi(c.user, 'f1ent')
            if not f1ent:
                return
            f1ent = f1ent[0][0]
            if not c.kernal.prolog_check('instances_of(%s, %s).' % ('wdeCountry', f1ent)):
                return

        if ts>=0:
            fss = c.ner(c.lang, 'country', ts, te)
        else:
            fss = c.kernal.mem_get_multi(c.user, 'f1ent')

        # import pdb; pdb.set_trace()

        for country, score in fss:
            clabel = c.kernal.prolog_query_one('rdfsLabel(%s, %s, L).' % (country, c.lang))
            area   = c.kernal.prolog_query_one("wdpdArea(%s, AREA)." % country)
            if clabel and area:
                if c.lang=='de':
                    c.resp(u"Die Fläche von %s ist %d Quadratkilometer." % (clabel, area), score=score, action=act, action_arg=country)
                else:
                    c.resp(u"The area of %s is %d square kilometers." % (clabel, area), score=score, action=act, action_arg=country)
    k.dte.dt('en', u"(what is the area of |how big is|what is the size of) {countries:LABEL} (do you know it|do you know that|)?",
                   country_area, ['countries_0_start', 'countries_0_end', False])
    k.dte.dt('de', u"(wie groß ist|wie ist die fläche von|wie groß ist die fläche von|wie viele quadratmeter hat) {countries:LABEL} (weißt Du das|)?",
                   country_area, ['countries_0_start', 'countries_0_end', False])

    k.dte.ts('en', 'd0002', [(u"How big is Estonia?", u"The area of Estonia is 45228 square kilometers")])
    k.dte.ts('de', 'd0003', [(u"Wie groß ist Estland?", u"Die Fläche von Estland ist 45228 Quadratkilometer.")])

    k.dte.dt('en', u"(and|) (what is the area of |how big is | what is the size of) it (do you know it|do you know that|)?",
                   country_area, [-1, -1, True])
    k.dte.dt('de', u"(und|) (wie groß ist es|wie ist die fläche|wie viele quadratmeter hat es|wie groß ist die fläche) (weißt Du das|)?",
                   country_area, [-1, -1, True])

    def answer_country_capital(c, ts, te, check_topic):

        def act(c, args):
            country, capital = args
            c.kernal.mem_push(c.user, 'f1ent', country)
            c.kernal.mem_push(c.user, 'f1pat', country)
            c.kernal.mem_push(c.user, 'f1age', capital)

        if check_topic:
            f1ent = c.kernal.mem_get_multi(c.user, 'f1ent')
            if not f1ent:
                return
            f1ent = f1ent[0][0]
            if not c.kernal.prolog_check('instances_of(%s, %s).' % ('wdeCountry', f1ent)):
                return

        if ts>=0:
            fss = c.ner(c.lang, 'country', ts, te)
        else:
            fss = c.kernal.mem_get_multi(c.user, 'f1ent')

        # import pdb; pdb.set_trace()

        for country, score in fss:
            clabel   = c.kernal.prolog_query_one('rdfsLabel(%s, %s, L).' % (country, c.lang))
            capital = c.kernal.prolog_query_one("wdpdCapital(%s, CAPITAL)." % country)
            if clabel and capital:
                caplabel = c.kernal.prolog_query_one('rdfsLabel(%s, %s, L).' % (capital, c.lang))

                if c.lang=='de':
                    c.resp(u"Die Hauptstadt von %s ist %s." % (clabel, caplabel), score=score, action=act, action_arg=(country, capital))
                else:
                    c.resp(u"The capital of %s is %s." % (clabel, caplabel), score=score, action=act, action_arg=(country, capital))

    k.dte.dt('en', u"(what is the|what is the name of the|) capital of {countries:LABEL} (do you know it|do you know that|)?",
                   answer_country_capital, ['countries_0_start', 'countries_0_end', False])
    k.dte.dt('en', u"what is the name of {countries:LABEL}'s capital (do you know it|do you know that|)?",
                   answer_country_capital, ['countries_0_start', 'countries_0_end', False])

    k.dte.dt('de', u"(Was|Welches) ist (der Name der|die) Hauptstadt von {countries:LABEL} (weißt Du das|)?",
                   answer_country_capital, ['countries_0_start', 'countries_0_end', False])
    k.dte.dt('de', u"Wie heißt die Hauptstadt (von|der) {countries:LABEL} (weißt Du das|)?",
                   answer_country_capital, ['countries_0_start', 'countries_0_end', False])

    k.dte.ts('en', 'd0002', [(u"What is the Capital of Finland?", u"The capital of Finland is Helsinki")])
    k.dte.ts('de', 'd0003', [(u"Welches ist die Hauptstadt von Finnland?", u"Die Hauptstadt von Finnland ist Helsinki.")])

    k.dte.dt('en', [u"(and|) (what is the|) capital of it (do you know it|do you know that|)?",
                    u"(and|) what is its capital (do you know it|do you know that|)?"],
                   answer_country_capital, [-1, -1, True])
    k.dte.dt('de', u"(und|) (was|welches) ist die Hauptstadt (davon|) (weißt Du das|)?",
                   answer_country_capital, [-1, -1, True])

    k.dte.ts('en', 'd0004', [(u"What about Spain?", u"Spain is a country on planet Earth"),
                             (u"Which country?", u"Spain is a country on planet Earth"),
                             (u"What was our topic?", u"We have been talking about Spain, I think."),
                             (u"How many people live there?", u"The population of Spain is 46528024"),
                             (u"And where is it again?", u"spain is a country on planet earth"),
                             (u"And what is its capital?", u"The capital of Spain is Madrid."),
                             (u"And what is the size of it?", u"The area of Spain is 505990 square kilometers.")])
    k.dte.ts('de', 'd0005', [(u"Was ist mit Spanien?", u"Spanien ist ein Staat auf dem Planeten Erde"),
                             (u"Welcher Staat?", u"Spanien ist ein Staat auf dem Planeten Erde"),
                             (u"Was war unser Thema?", u"Wir hatten über Spanien gesprochen, glaube ich."),
                             (u"Wie viele Menschen leben dort?", u"Spanien hat 46528024 Einwohner."),
                             (u"Und wo ist es nochmal?", u"Spanien ist ein Staat auf dem Planeten Erde"),
                             (u"Und welches ist die Hauptstadt?", u"Die Hauptstadt von Spanien ist Madrid."),
                             (u"Und wie groß ist die Fläche?", u"Die Fläche von Spanien ist 505990 quadratkilometer.")])

    k.dte.dt('en', u"how is {countries:LABEL}", u"Not sure if countries have feelings?")
    k.dte.dt('de', u"wie ist {countries:LABEL}", u"Ich glaube Staaten haben keine Gefühle.")

    def answer_country_sure(c, ts, te, check_topic):

        def act(c, country):
            c.kernal.mem_push(c.user, 'f1ent', country)

        if check_topic:
            f1ent = c.kernal.mem_get_multi(c.user, 'f1ent')
            if not f1ent:
                return
            f1ent = f1ent[0][0]
            if not c.kernal.prolog_check('instances_of(%s, %s).' % ('wdeFilm', f1ent)):
                return

        if ts>=0:
            fss = c.ner(c.lang, 'country', ts, te)
        else:
            fss = c.kernal.mem_get_multi(c.user, 'f1ent')

        # import pdb; pdb.set_trace()

        for country, score in fss:
            clabel   = c.kernal.prolog_query_one('rdfsLabel(%s, %s, L).' % (country, c.lang))
            if c.lang=='de':
                c.resp(u"Klar, %s." % clabel, score=score, action=act, action_arg=country)
            else:
                c.resp(u"Sure, %s." % clabel, score=score, action=act, action_arg=country)
    k.dte.dt('en', u"in {countries:LABEL} (maybe|)",
                   answer_country_sure, ['countries_0_start', 'countries_0_end', False])
    k.dte.dt('de', u"in {countries:LABEL} (vielleicht|)",
                   answer_country_sure, ['countries_0_start', 'countries_0_end', False])

    k.dte.ts('en', 'd0007', [(u"in Finland maybe?", u"Sure, Finland.")])
    k.dte.ts('de', 'd0008', [(u"in Finnland?", u"Klar, Finnland.")])

    k.dte.dt('en', u"How many countries are there in europe?", u"About 50.")
    k.dte.dt('de', u"Wie viele Länder gibt es in Europa?", u"Etwa 50.")

