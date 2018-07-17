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
        for res in k.prolog_query("instances_of(wdeFederatedState, STATE), rdfsLabel(STATE, %s, LABEL)." % lang):
            s_state = res[0].name
            s_label = res[1].value
            k.dte.ner(lang, 'federated_state', s_state, s_label)
            k.dte.macro(lang, 'federated_states', {'LABEL': s_label})

    def federated_state_location(c, ts, te, check_topic):

        def act(c, federated_state):
            c.kernal.mem_push(c.user, 'f1ent', federated_state)

        if check_topic:
            f1ent = c.kernal.mem_get_multi(c.user, 'f1ent')
            if not f1ent:
                return
            f1ent = f1ent[0][0]
            if not c.kernal.prolog_check('instances_of(%s, %s).' % ('wdeFederatedState', f1ent)):
                return

        if ts>=0:
            fss = c.ner(c.lang, 'federated_state', ts, te)
        else:
            fss = c.kernal.mem_get_multi(c.user, 'f1ent')

        # import pdb; pdb.set_trace()

        for federated_state, score in fss:
            flabel  = c.kernal.prolog_query_one('rdfsLabel(%s, %s, L).' % (federated_state, c.lang))
            country = c.kernal.prolog_query_one("wdpdCountry(%s, COUNTRY)." % federated_state)
            if flabel and country:
                cylabel = c.kernal.prolog_query_one('rdfsLabel(%s, %s, L).' % (country, c.lang))

                if c.lang=='de':
                    c.resp(u"%s ist ein Land in %s." % (flabel, cylabel), score=score, action=act, action_arg=federated_state)
                else:
                    c.resp(u"%s is a state in %s." % (flabel, cylabel), score=score, action=act, action_arg=federated_state)

    k.dte.dt('en', u"(what is|what about|what do you know about|where is|in what country is|in|) {federated_states:LABEL} (and you|) (do you know it|do you know that|)?",
                   federated_state_location, ['federated_states_0_start', 'federated_states_0_end', False])
    k.dte.dt('de', u"(was ist|was ist mit|was weißt Du über|wo ist|wo liegt|in|in welchem Staat ist|in welchem Land ist|) {federated_states:LABEL} (und du|weißt Du das|)?",
                   federated_state_location, ['federated_states_0_start', 'federated_states_0_end', False])

    k.dte.ts('en', 'states0', [(u"What is Bavaria?", u"Bavaria is a state in Germany")])
    k.dte.ts('de', 'states1', [(u"Wo ist Bayern?", u"Bayern ist ein Land in Deutschland.")])

    k.dte.dt('en', [u"(and|) (in|) (a|which) state?",
                    u"(and|) What (is|was) (it|that) (again|)?"],
                   [u"Which state comes to mind?",
                    u"Which state do you like best?"])
    k.dte.dt('en', [u"(and|) (in|) (a|which) state?",
                    u"(and|) What (is|was) (it|that) (again|)?",
                    u"(and|) where (is|was) (it|that) (again|)?"],
                   federated_state_location, [-1, -1, True])
    k.dte.dt('de', [u"(und|) (in|) (einem|welchen|welches) Land?",
                    u"(und|) Was (ist|war) (das|es) (nochmal|)?"],
                   [u"An welches Land denkst Du?",
                    u"Aus welchem Land kommst Du?"])
    k.dte.dt('de', [u"(und|) (in|) (einem|welchen|welches) Land?",
                    u"(und|) Was (ist|war) (das|es) (nochmal|)?",
                    u"(und|) Wo (ist|war|liegt) (das|es) (nochmal|)?"],
                   federated_state_location, [-1, -1, True])

    def federated_state_population(c, ts, te, check_topic):

        def act(c, federated_state):
            c.kernal.mem_push(c.user, 'f1ent', federated_state)

        if check_topic:
            f1ent = c.kernal.mem_get_multi(c.user, 'f1ent')
            if not f1ent:
                return
            f1ent = f1ent[0][0]
            if not c.kernal.prolog_check('instances_of(%s, %s).' % ('wdeFederatedState', f1ent)):
                return

        if ts>=0:
            fss = c.ner(c.lang, 'federated_state', ts, te)
        else:
            fss = c.kernal.mem_get_multi(c.user, 'f1ent')

        # import pdb; pdb.set_trace()

        for federated_state, score in fss:
            clabel     = c.kernal.prolog_query_one('rdfsLabel(%s, %s, L).' % (federated_state, c.lang))
            population = c.kernal.prolog_query_one("wdpdPopulation(%s, POPULATION)." % federated_state)
            if clabel and population:
                if c.lang=='de':
                    c.resp(u"%s hat %d Einwohner." % (clabel, population), score=score, action=act, action_arg=federated_state)
                else:
                    c.resp(u"The population of %s is %d." % (clabel, population), score=score, action=act, action_arg=federated_state)

    k.dte.dt('en', u"(what is the population of |how many people live in | how many humans reside in) {federated_states:LABEL} (do you know it|do you know that|)?",
                   federated_state_population, ['federated_states_0_start', 'federated_states_0_end', False])
    k.dte.dt('de', u"(wie hoch ist die bevölkerung von|wie ist die bevölkerung von|wie viele menschen leben in|wie viele leute leben in|wie viele Einwohner hat) {federated_states:LABEL} (weißt Du das|)?",
                   federated_state_population, ['federated_states_0_start', 'federated_states_0_end', False])

    k.dte.ts('en', 'states2', [(u"How many people live in Texas?", u"The population of Texas is 27469114")])
    k.dte.ts('de', 'states3', [(u"Wie viele Menschen leben in Texas?", u"Texas hat 27469114 Einwohner.")])

    k.dte.dt('en', [u"(and|) (what is the population of |how many people live in | how many humans reside in) it (do you know it|do you know that|)?",
                    u"(and|) how many residents does it have (do you know it|do you know that|)?",
                    u"(and|) how many people live there (do you know it|do you know that|)?"],
                   federated_state_population, [-1, -1, True])
    k.dte.dt('de', u"(und|) (wie hoch ist die bevölkerung von|wie ist die bevölkerung von|wie viele menschen leben |wie viele leute leben |wie viele Einwohner hat es) dort (weißt Du das|)?",
                   federated_state_population, [-1, -1, True])

    def federated_state_area(c, ts, te, check_topic):

        def act(c, federated_state):
            c.kernal.mem_push(c.user, 'f1ent', federated_state)

        if check_topic:
            f1ent = c.kernal.mem_get_multi(c.user, 'f1ent')
            if not f1ent:
                return
            f1ent = f1ent[0][0]
            if not c.kernal.prolog_check('instances_of(%s, %s).' % ('wdeFederatedState', f1ent)):
                return

        if ts>=0:
            fss = c.ner(c.lang, 'federated_state', ts, te)
        else:
            fss = c.kernal.mem_get_multi(c.user, 'f1ent')

        # import pdb; pdb.set_trace()

        for federated_state, score in fss:
            clabel = c.kernal.prolog_query_one('rdfsLabel(%s, %s, L).' % (federated_state, c.lang))
            area   = c.kernal.prolog_query_one("wdpdArea(%s, AREA)." % federated_state)
            if clabel and area:
                if c.lang=='de':
                    c.resp(u"Die Fläche von %s ist %d Quadratkilometer." % (clabel, area), score=score, action=act, action_arg=federated_state)
                else:
                    c.resp(u"The area of %s is %d square kilometers." % (clabel, area), score=score, action=act, action_arg=federated_state)

    k.dte.dt('en', u"(what is the area of |how big is|what is the size of) {federated_states:LABEL} (do you know it|do you know that|)?",
                   federated_state_area, ['federated_states_0_start', 'federated_states_0_end', False])
    k.dte.dt('de', u"(wie groß ist|wie ist die fläche von|wie groß ist die fläche von|wie viele quadratmeter hat) {federated_states:LABEL} (weißt Du das|)?",
                   federated_state_area, ['federated_states_0_start', 'federated_states_0_end', False])

    k.dte.ts('en', 'states4', [(u"How big is California?", u"The area of California is 423970 square kilometers")])
    k.dte.ts('de', 'states5', [(u"Wie groß ist Kalifornien?", u"Die Fläche von Kalifornien ist 423970 Quadratkilometer.")])

    k.dte.dt('en', u"(and|) (what is the area of |how big is | what is the size of) it (do you know it|do you know that|)?",
                   federated_state_area, [-1, -1, True])
    k.dte.dt('de', u"(und|) (wie groß ist es|wie ist die fläche|wie viele quadratmeter hat es|wie groß ist die fläche) (weißt Du das|)?",
                   federated_state_area, [-1, -1, True])

    def federated_state_capital(c, ts, te, check_topic):

        def act(c, args):
            state, capital = args
            c.kernal.mem_push(c.user, 'f1ent', state)
            c.kernal.mem_push(c.user, 'f1pat', state)
            c.kernal.mem_push(c.user, 'f1age', capital)

        if check_topic:
            f1ent = c.kernal.mem_get_multi(c.user, 'f1ent')
            if not f1ent:
                return
            f1ent = f1ent[0][0]
            if not c.kernal.prolog_check('instances_of(%s, %s).' % ('wdeFederatedState', f1ent)):
                return

        if ts>=0:
            fss = c.ner(c.lang, 'federated_state', ts, te)
        else:
            fss = c.kernal.mem_get_multi(c.user, 'f1ent')

        # import pdb; pdb.set_trace()

        for state, score in fss:
            slabel   = c.kernal.prolog_query_one('rdfsLabel(%s, %s, L).' % (state, c.lang))
            capital = c.kernal.prolog_query_one("wdpdCapital(%s, CAPITAL)." % state)
            if slabel and capital:
                caplabel = c.kernal.prolog_query_one('rdfsLabel(%s, %s, L).' % (capital, c.lang))

                if c.lang=='de':
                    c.resp(u"Die Hauptstadt von %s ist %s." % (slabel, caplabel), score=score, action=act, action_arg=(state, capital))
                else:
                    c.resp(u"The capital of %s is %s." % (slabel, caplabel), score=score, action=act, action_arg=(state, capital))

    k.dte.dt('en', u"(what is the|what is the name of the|) capital of {federated_states:LABEL} (do you know it|do you know that|)?",
                   federated_state_capital, ['federated_states_0_start', 'federated_states_0_end', False])
    k.dte.dt('en', u"what is the name of {federated_states:LABEL}'s capital (do you know it|do you know that|)?",
                   federated_state_capital, ['federated_states_0_start', 'federated_states_0_end', False])

    k.dte.dt('de', u"(Was|Welches) ist (der Name der|die) Hauptstadt von {federated_states:LABEL} (weißt Du das|)?",
                   federated_state_capital, ['federated_states_0_start', 'federated_states_0_end', False])
    k.dte.dt('de', u"Wie heißt die Hauptstadt (von|der) {federated_states:LABEL} (weißt Du das|)?",
                   federated_state_capital, ['federated_states_0_start', 'federated_states_0_end', False])

    k.dte.ts('en', 'states6', [(u"What is the Capital of Bavaria?", u"The capital of Bavaria is Munich")])
    k.dte.ts('de', 'states7', [(u"Welches ist die Hauptstadt von Bayern?", u"Die Hauptstadt von Bayern ist München.")])

    k.dte.dt('en', [u"(and|) (what is the|) capital of it (do you know it|do you know that|)?",
                    u"(and|) what is its capital (do you know it|do you know that|)?"],
                   federated_state_capital, [-1, -1, True])

    k.dte.dt('de', u"(und|) (was|welches) ist die Hauptstadt (davon|) (weißt Du das|)?",
                   federated_state_capital, [-1, -1, True])

    k.dte.ts('en', 'states8', [(u"What about Hesse?", u"Hesse is a state in Germany."),
                               (u"Which State?", u"Hesse is a state in Germany."),
                               (u"What was our topic?", u"We have been talking about Hesse, I think."),
                               (u"How many people live there?", u"The population of Hesse is 6045425"),
                               (u"And where is it again?", u"Hesse is a state in germany"),
                               (u"And what is its capital?", u"The capital of Hesse is Wiesbaden."),
                               (u"And what is the size of it?", u"The area of Hesse is 21100 square kilometers.")])
    k.dte.ts('de', 'states9', [(u"Was ist mit Hessen?", u"Hessen ist ein Land in Deutschland"),
                               (u"Welches Land?", u"Hessen ist ein Land in Deutschland"),
                               (u"Was war unser Thema?", u"Wir hatten über Hessen gesprochen, glaube ich."),
                               (u"Wie viele Menschen leben dort?", u"Hessen hat 6045425 Einwohner."),
                               (u"Und wo ist es nochmal?", u"Hessen ist ein Land in Deutschland"),
                               (u"Und welches ist die Hauptstadt?", u"Die Hauptstadt von Hessen ist Wiesbaden."),
                               (u"Und wie groß ist die Fläche?", u"Die Fläche von Hessen ist 21100 quadratkilometer.")])

    k.dte.dt('en', u"how is {federated_states:LABEL}", u"Not sure if states have feelings?")
    k.dte.dt('de', u"wie ist {federated_states:LABEL}", u"Ich glaube Länder haben keine Gefühle.")

    def answer_federated_state_sure(c, ts, te, check_topic):

        def act(c, federated_state):
            c.kernal.mem_push(c.user, 'f1ent', federated_state)

        if check_topic:
            f1ent = c.kernal.mem_get_multi(c.user, 'f1ent')
            if not f1ent:
                return
            f1ent = f1ent[0][0]
            if not c.kernal.prolog_check('instances_of(%s, %s).' % ('wdeFederatedState', f1ent)):
                return

        if ts>=0:
            fss = c.ner(c.lang, 'federated_state', ts, te)
        else:
            fss = c.kernal.mem_get_multi(c.user, 'f1ent')

        # import pdb; pdb.set_trace()

        for federated_state, score in fss:
            clabel   = c.kernal.prolog_query_one('rdfsLabel(%s, %s, L).' % (federated_state, c.lang))
            if c.lang=='de':
                c.resp(u"Klar, %s." % clabel, score=score, action=act, action_arg=federated_state)
            else:
                c.resp(u"Sure, %s." % clabel, score=score, action=act, action_arg=federated_state)

    k.dte.dt('en', u"in {federated_states:LABEL} (maybe|)",
                   answer_federated_state_sure, ['federated_states_0_start', 'federated_states_0_end', False])
    k.dte.dt('de', u"in {federated_states:LABEL} (vielleicht|)",
                   answer_federated_state_sure, ['federated_states_0_start', 'federated_states_0_end', False])

