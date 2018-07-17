#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# Copyright 2016, 2017, 2018 Guenter Bartsch
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

# MACRO_LIMIT=8

def get_data(k):

    # k.dte.set_prefixes([u''])
    k.dte.set_prefixes([u''])

    #
    # numbers NER
    #

    cnt = 0
    for res in k.prolog_query("wdpdInstanceOf(NUMBER, wdeNaturalNumber), rdfsLabel(NUMBER, en, LABEL), rdfsLabel(NUMBER, de, DE_LABEL)."):

        s_number    = res[0].name
        s_label_en  = res[1].value
        s_label_de  = res[2].value
        # import pdb; pdb.set_trace()
        k.dte.ner('en', 'natnum', s_number, s_label_en)
        k.dte.ner('de', 'natnum', s_number, s_label_de)
        # if cnt<MACRO_LIMIT:
        k.dte.macro('en', 'natnum', {'W': s_label_en})
        k.dte.macro('de', 'natnum', {'W': s_label_de})
        k.dte.macro('en', 'natnum2', {'W': s_label_en})
        k.dte.macro('de', 'natnum2', {'W': s_label_de})
        cnt += 1

    def compute_squared(c, n1_start, n1_end):
        def action_set_ent_math(c):
            c.kernal.mem_push(c.user, 'f1ent', 'wdeMathematics')
        for n1e, score in c.ner(c.lang, 'natnum', n1_start, n1_end):
            for row in c.kernal.prolog_query('wdpdNumericValue(%s, N1).' % unicode(n1e)):
                n1 = row[0]
                res = n1 * n1
                c.resp(u"%d" % res, score=score+100.0, action=action_set_ent_math)

    k.dte.dt('en', [u"what (gives|is|makes) {natnum:W} (squared|square)", 
                    u"calculate {natnum:W} (squared|square) (please|)"], compute_squared, ['natnum_0_start', 'natnum_0_end'])
    k.dte.dt('de', [u"was (gibt|ist|ergibt) {natnum:W} (zum|ins) quadrat",
                    u"(berechne|rechne) (bitte|) {natnum:W} (zum|ins) quadrat"], compute_squared, ['natnum_0_start', 'natnum_0_end'])

    k.dte.ts('en', 'square00', [(u"what is 12 squared?", u"144.", [])])
    k.dte.ts('de', 'square01', [(u"was ergibt 12 ins quadrat?", u"144.", [])])

    def compute_addition(c, n1_start, n1_end, n2_start, n2_end):
        def action_set_ent_math(c):
            c.kernal.mem_push(c.user, 'f1ent', 'wdeMathematics')
        for n1e, s1 in c.ner(c.lang, 'natnum', n1_start, n1_end):
            for row in c.kernal.prolog_query('wdpdNumericValue(%s, N1).' % unicode(n1e)):
                n1 = row[0]
            for n2e, s2 in c.ner(c.lang, 'natnum', n2_start, n2_end):
                for row in c.kernal.prolog_query('wdpdNumericValue(%s, N2).' % unicode(n2e)):
                    n2 = row[0]
                    res = n1 + n2
                    score = s1+s2
                    c.resp(u"%d" % res, score=score+100.0, action=action_set_ent_math)

    k.dte.dt('en', [u"what (gives|is|makes) {natnum:W} (plus|and|added) {natnum2:W}", 
                    u"calculate {natnum:W} (plus|and|added) {natnum2:W} (please|)", 
                    u"add {natnum:W} (and|) {natnum2:W} (please|)"], 
                   compute_addition, ['natnum_0_start', 'natnum_0_end', 'natnum2_0_start', 'natnum2_0_end'])
    k.dte.dt('de', [u"was (gibt|ist|ergibt) {natnum:W} (und|plus) {natnum2:W}", 
                    u"(berechne|rechne) (bitte|) {natnum:W} (und|plus) {natnum2:W}", 
                    u"addiere (bitte|) {natnum:W} (mit|und) {natnum2:W}"], 
                   compute_addition, ['natnum_0_start', 'natnum_0_end', 'natnum2_0_start', 'natnum2_0_end'])

    k.dte.ts('en', 'plus00', [(u"what is 12 plus 11?", u"23.", [])])
    k.dte.ts('de', 'plus01', [(u"was ergibt 12 plus 11?", u"23.", [])])

    def compute_subtraction(c, n1_start, n1_end, n2_start, n2_end):
        def action_set_ent_math(c):
            c.kernal.mem_push(c.user, 'f1ent', 'wdeMathematics')
        for n1e, s1 in c.ner(c.lang, 'natnum', n1_start, n1_end):
            for row in c.kernal.prolog_query('wdpdNumericValue(%s, N1).' % unicode(n1e)):
                n1 = row[0]
            for n2e, s2 in c.ner(c.lang, 'natnum', n2_start, n2_end):
                for row in c.kernal.prolog_query('wdpdNumericValue(%s, N2).' % unicode(n2e)):
                    n2 = row[0]
                    res = n1 - n2
                    score = s1+s2
                    c.resp(u"%d" % res, score=score+100.0, action=action_set_ent_math)

    k.dte.dt('en', [u"what (gives|is|makes) {natnum:W} (minus|subtracted) {natnum2:W}", 
                    u"calculate {natnum:W} (minus|subtracted) {natnum2:W} (please|)",
                    u"subtract {natnum2:W} from {natnum:W} (please|)"], 
                   compute_subtraction, ['natnum_0_start', 'natnum_0_end', 'natnum2_0_start', 'natnum2_0_end'])
    k.dte.dt('de', [u"was (gibt|ist|ergibt) {natnum:W} (weniger|minus) {natnum2:W}", 
                    u"(berechne|rechne) (bitte|) {natnum:W} (weniger|minus) {natnum2:W}",
                    u"subtrahiere (bitte|) {natnum2:W} von {natnum:W}" ],
                   compute_subtraction, ['natnum_0_start', 'natnum_0_end', 'natnum2_0_start', 'natnum2_0_end'])
    k.dte.ts('en', 'minus00', [(u"what is 20 minus 11?", u"9.", [])])
    k.dte.ts('de', 'minus01', [(u"was ergibt 20 minus 11?", u"9.", [])])
    k.dte.ts('en', 'minus02', [(u"subtract 5 from 11", u"6.", [])])
    k.dte.ts('de', 'minus03', [(u"subtrahiere 5 von 11", u"6.", [])])

    def compute_multiplication(c, n1_start, n1_end, n2_start, n2_end):
        def action_set_ent_math(c):
            c.kernal.mem_push(c.user, 'f1ent', 'wdeMathematics')
        for n1e, s1 in c.ner(c.lang, 'natnum', n1_start, n1_end):
            for row in c.kernal.prolog_query('wdpdNumericValue(%s, N1).' % unicode(n1e)):
                n1 = row[0]
            for n2e, s2 in c.ner(c.lang, 'natnum', n2_start, n2_end):
                for row in c.kernal.prolog_query('wdpdNumericValue(%s, N2).' % unicode(n2e)):
                    n2 = row[0]
                    res = n1 * n2
                    score = s1+s2
                    c.resp(u"%d" % res, score=score+100.0, action=action_set_ent_math)

    k.dte.dt('en', [u"what (gives|is|makes) {natnum:W} (times|multiplied with|multiplied by) {natnum2:W}", 
                    u"calculate {natnum:W} (times|multiplied with) {natnum2:W} (please|)", 
                    u"multiply {natnum:W} by {natnum2:W} (please|)"], 
                   compute_multiplication, ['natnum_0_start', 'natnum_0_end', 'natnum2_0_start', 'natnum2_0_end'])
    k.dte.dt('de', [u"was (gibt|ist|ergibt) {natnum:W} (mal|multipliziert mit) {natnum2:W}", 
                    u"(berechne|rechne) (bitte|) {natnum:W} (mal|multipliziert mit) {natnum2:W}", 
                    u"multipliziere (bitte|) {natnum:W} mit {natnum2:W}"],
                   compute_multiplication, ['natnum_0_start', 'natnum_0_end', 'natnum2_0_start', 'natnum2_0_end'])
    k.dte.ts('en', 'multiply00', [(u"what is 3 times 3?", u"9.", [])])
    k.dte.ts('de', 'multiply01', [(u"was ergibt 3 mal 3?", u"9.", [])])

    def compute_division(c, n1_start, n1_end, n2_start, n2_end):
        def action_set_ent_math(c):
            c.kernal.mem_push(c.user, 'f1ent', 'wdeMathematics')
        for n1e, s1 in c.ner(c.lang, 'natnum', n1_start, n1_end):
            for row in c.kernal.prolog_query('wdpdNumericValue(%s, N1).' % unicode(n1e)):
                n1 = row[0]
            for n2e, s2 in c.ner(c.lang, 'natnum', n2_start, n2_end):
                for row in c.kernal.prolog_query('wdpdNumericValue(%s, N2).' % unicode(n2e)):
                    n2 = row[0]
                    res = n1 / n2
                    score = s1+s2
                    c.resp(u"%d" % res, score=score+100.0, action=action_set_ent_math)

    k.dte.dt('en', [u"what (gives|is|makes) {natnum:W} divided by {natnum2:W}", 
                    u"calculate {natnum:W} didivded by {natnum2:W} (please|)", 
                    u"divide {natnum:W} by {natnum2:W} (please|)"], 
                   compute_division, ['natnum_0_start', 'natnum_0_end', 'natnum2_0_start', 'natnum2_0_end'])
    k.dte.dt('de', [u"was (gibt|ist|ergibt) {natnum:W} (durch|geteilt durch) {natnum2:W}", 
                    u"(berechne|rechne) (bitte|) {natnum:W} (durch|geteilt durch) {natnum2:W}", 
                    u"teile (bitte|) {natnum:W} durch {natnum2:W}"],
                   compute_division, ['natnum_0_start', 'natnum_0_end', 'natnum2_0_start', 'natnum2_0_end'])
    k.dte.ts('en', 'division00', [(u"what is 8 divided by 2?", u"4.", [])])
    k.dte.ts('de', 'division01', [(u"was ergibt 8 durch 2?", u"4.", [])])

    k.dte.dt('en', [u"are you able to calculate",
                    u"can you (do|) (mathematics|math)",
                    u"do you know (math|mathematics)?"],
                   [u"Sure, I am a computer after all.",
                    u"Of course - being a computer, you know."])
    k.dte.dt('de', [u"kannst du rechnen",
                    u"kannst du (mathe|mathematik)",
                    u"kennst du dich mit (mathe|mathematik) aus"],
                   [u"Klar, ich bin doch immerhin ein Rechner.",
                    u"Natürlich - so als Rechner, weißt Du?"])

    # FIXME: set(C:context|topic, wdeMathematics)
    k.dte.dt('en', u"about prime numbers", u"what about them?")
    k.dte.dt('de', u"über primzahlen", u"Was ist damit?")
    k.dte.dt('en', u"(compute|calculate) (it|) (please|)", u"What would you like me to calculate?")
    k.dte.dt('de', u"rechne es (bitte|) aus", u"Was hättest Du gerne ausgerechnet?")
    k.dte.dt('en', u"can you philosophise better than calculate", u"Maybe?")
    k.dte.dt('de', u"kannst du besser philosophieren als rechnen", u"Vielleicht?")
    k.dte.dt('en', u"you can not count", u"One two three four five")
    k.dte.dt('de', u"du kannst nicht rechnen", u"Eins zwei drei vier fünf")
    k.dte.dt('en', u"what is a talor series", u"An infinite sum giving the value of a function in the neighborhood of a point in terms of the derivatives of the function.")
    k.dte.dt('de', u"was ist eine taylorreihe", u"Taylorreihen werden benutzt, um den Wert einer Funktion an einer Stelle näherungsweise zu berechnen.")
    k.dte.dt('en', u"what is a sphere", u"A perfectly round ball shaped object.")
    k.dte.dt('de', u"was ist eine kugel", u"Ein perfekt rundes Objekt das die Form eines Balls hat.")

