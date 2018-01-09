#!/usr/bin/env python
# -*- coding: utf-8 -*-

from xsbprolog import xsb_make_vars, xsb_query_string, xsb_var_string, xsb_next

def get_data(k):

    k.dte.set_prefixes([u'{self_address:W} '])

    #
    # numbers NER
    #

    xsb_make_vars(3)
    rcode = xsb_query_string("wdpdInstanceOf(NUMBER, wdeNaturalNumber), rdfsLabel(NUMBER, en, LABEL), rdfsLabel(NUMBER, de, DE_LABEL).")

    if not rcode:

        while not rcode:

            s_number    = xsb_var_string(1)
            s_label_en  = xsb_var_string(2)
            s_label_de  = xsb_var_string(3)
            # import pdb; pdb.set_trace()
            k.dte.ner('en', 'natnum', s_number, s_label_en)
            k.dte.ner('de', 'natnum', s_number, s_label_de)
            k.dte.macro('en', 'natnum', {'W': s_label_en})
            k.dte.macro('de', 'natnum', {'W': s_label_de})
            k.dte.macro('en', 'natnum2', {'W': s_label_en})
            k.dte.macro('de', 'natnum2', {'W': s_label_de})

            rcode = xsb_next()

    def compute_squared_en(c):
        for n1e, score in c.ner('en', 'natnum', tstart(natnum), tend(natnum)):
            for row in xsb_hl_query('wdpdNumericValue', [n1e, 'N1']):
                n1 = row['N1']
                res = n1 * n1
                # FIXME: set(C:context|topic, wdeMathematics)
                c.resp(u"%d" % res, score=score+100.0)

    k.dte.dt('en', [u"what (gives|is|makes) {natnum:W} (squared|square)", 
                    u"calculate {natnum:W} (squared|square) (please|)"], compute_squared_en)
# train(en) :- and(or("what (gives|is|makes) {natnum:W} (squared|square)", "calculate {natnum:W} (squared|square) (please|)"), ner(en, natnum, tstart(natnum), tend(natnum), C:tokens, N1E, SCORE), wdpdNumericValue(N1E, N1), r_score(C, SCORE), set(RES, *(N1, N1)), r_score(C, 100.0), set(C:context|topic, wdeMathematics), "{RES,d}").
# train(de) :- and(or("was (gibt|ist|ergibt) {natnum:W} (zum|ins) quadrat", "(berechne|rechne) (bitte|) {natnum:W} (zum|ins) quadrat"), ner(de, natnum, tstart(natnum), tend(natnum), C:tokens, N1E, SCORE), wdpdNumericValue(N1E, N1), r_score(C, SCORE), set(RES, *(N1, N1)), r_score(C, 100.0), set(C:context|topic, wdeMathematics), "{RES,d}").
    k.dte.ts('en', 'square00', [(u"what is 12 squared?", u"144.", [])])
    k.dte.ts('de', 'square01', [(u"was ergibt 12 ins quadrat?", u"144.", [])])

#    train(en) :- and(or("what (gives|is|makes) {natnum:W} (plus|and|added) {natnum2:W}", "calculate {natnum:W} (plus|and|added) {natnum2:W} (please|)", "add {natnum:W} (and|) {natnum2:W} (please|)"), ner(en, natnum, tstart(natnum), tend(natnum), C:tokens, N1E, SCORE1), wdpdNumericValue(N1E, N1), r_score(C, SCORE1), ner(en, natnum, tstart(natnum2), tend(natnum2), C:tokens, N2E, SCORE2), wdpdNumericValue(N2E, N2), r_score(C, SCORE2), set(RES, +(N1, N2)), r_score(C, 100.0), set(C:context|topic, wdeMathematics), "{RES,d}").
#    train(de) :- and(or("was (gibt|ist|ergibt) {natnum:W} (und|plus) {natnum2:W}", "(berechne|rechne) (bitte|) {natnum:W} (und|plus) {natnum2:W}", "addiere (bitte|) {natnum:W} (mit|und) {natnum2:W}"), ner(de, natnum, tstart(natnum), tend(natnum), C:tokens, N1E, SCORE1), wdpdNumericValue(N1E, N1), r_score(C, SCORE1), ner(de, natnum, tstart(natnum2), tend(natnum2), C:tokens, N2E, SCORE2), wdpdNumericValue(N2E, N2), r_score(C, SCORE2), set(RES, +(N1, N2)), r_score(C, 100.0), set(C:context|topic, wdeMathematics), "{RES,d}").
    k.dte.ts('en', 'plus00', [(u"what is 12 plus 11?", u"23.", [])])
    k.dte.ts('de', 'plus01', [(u"was ergibt 12 plus 11?", u"23.", [])])

#    train(en) :- and(or("what (gives|is|makes) {natnum:W} (minus|subtracted) {natnum2:W}", "calculate {natnum:W} (minus|subtracted) {natnum2:W} (please|)"), ner(en, natnum, tstart(natnum), tend(natnum), C:tokens, N1E, SCORE1), wdpdNumericValue(N1E, N1), r_score(C, SCORE1), ner(en, natnum, tstart(natnum2), tend(natnum2), C:tokens, N2E, SCORE2), wdpdNumericValue(N2E, N2), r_score(C, SCORE2), set(RES, -(N1, N2)), r_score(C, 100.0), set(C:context|topic, wdeMathematics), "{RES,d}").
#    train(de) :- and(or("was (gibt|ist|ergibt) {natnum:W} (weniger|minus) {natnum2:W}", "(berechne|rechne) (bitte|) {natnum:W} (weniger|minus) {natnum2:W}"), ner(de, natnum, tstart(natnum), tend(natnum), C:tokens, N1E, SCORE1), wdpdNumericValue(N1E, N1), r_score(C, SCORE1), ner(de, natnum, tstart(natnum2), tend(natnum2), C:tokens, N2E, SCORE2), wdpdNumericValue(N2E, N2), r_score(C, SCORE2), set(RES, -(N1, N2)), r_score(C, 100.0), set(C:context|topic, wdeMathematics), "{RES,d}").
    k.dte.ts('en', 'minus00', [(u"what is 20 minus 11?", u"9.", [])])
    k.dte.ts('de', 'minus01', [(u"was ergibt 20 minus 11?", u"9.", [])])

#    train(en) :- and("subtract {natnum:W} from {natnum2:W} (please|)", ner(en, natnum, tstart(natnum), tend(natnum), C:tokens, N1E, SCORE1), wdpdNumericValue(N1E, N1), r_score(C, SCORE1), ner(en, natnum, tstart(natnum2), tend(natnum2), C:tokens, N2E, SCORE2), wdpdNumericValue(N2E, N2), r_score(C, SCORE2), set(RES, -(N2, N1)), r_score(C, 100.0), set(C:context|topic, wdeMathematics), "{RES,d}").
#    train(de) :- and("subtrahiere (bitte|) {natnum:W} von {natnum2:W}", ner(de, natnum, tstart(natnum), tend(natnum), C:tokens, N1E, SCORE1), wdpdNumericValue(N1E, N1), r_score(C, SCORE1), ner(de, natnum, tstart(natnum2), tend(natnum2), C:tokens, N2E, SCORE2), wdpdNumericValue(N2E, N2), r_score(C, SCORE2), set(RES, -(N2, N1)), r_score(C, 100.0), set(C:context|topic, wdeMathematics), "{RES,d}").
    k.dte.ts('en', 'minus02', [(u"subtract 5 from 11", u"6.", [])])
    k.dte.ts('de', 'minus03', [(u"subtrahiere 5 von 11", u"6.", [])])

#    train(en) :- and(or("what (gives|is|makes) {natnum:W} (times|multiplied with|multiplied by) {natnum2:W}", "calculate {natnum:W} (times|multiplied with) {natnum2:W} (please|)", "multiply {natnum:W} by {natnum2:W} (please|)"), ner(en, natnum, tstart(natnum), tend(natnum), C:tokens, N1E, SCORE1), wdpdNumericValue(N1E, N1), r_score(C, SCORE1), ner(en, natnum, tstart(natnum2), tend(natnum2), C:tokens, N2E, SCORE2), wdpdNumericValue(N2E, N2), r_score(C, SCORE2), set(RES, *(N1, N2)), r_score(C, 100.0), set(C:context|topic, wdeMathematics), "{RES,d}").
#    train(de) :- and(or("was (gibt|ist|ergibt) {natnum:W} (mal|multipliziert mit) {natnum2:W}", "(berechne|rechne) (bitte|) {natnum:W} (mal|multipliziert mit) {natnum2:W}", "multipliziere (bitte|) {natnum:W} mit {natnum2:W}"), ner(de, natnum, tstart(natnum), tend(natnum), C:tokens, N1E, SCORE1), wdpdNumericValue(N1E, N1), r_score(C, SCORE1), ner(de, natnum, tstart(natnum2), tend(natnum2), C:tokens, N2E, SCORE2), wdpdNumericValue(N2E, N2), r_score(C, SCORE2), set(RES, *(N1, N2)), r_score(C, 100.0), set(C:context|topic, wdeMathematics), "{RES,d}").
    k.dte.ts('en', 'multiply00', [(u"what is 3 times 3?", u"9.", [])])
    k.dte.ts('de', 'multiply01', [(u"was ergibt 3 mal 3?", u"9.", [])])

#    train(en) :- and(or("what (gives|is|makes) {natnum:W} divided by {natnum2:W}", "calculate {natnum:W} didivded by {natnum2:W} (please|)", "divide {natnum:W} by {natnum2:W} (please|)"), ner(en, natnum, tstart(natnum), tend(natnum), C:tokens, N1E, SCORE1), wdpdNumericValue(N1E, N1), r_score(C, SCORE1), ner(en, natnum, tstart(natnum2), tend(natnum2), C:tokens, N2E, SCORE2), wdpdNumericValue(N2E, N2), r_score(C, SCORE2), set(RES, /(N1, N2)), r_score(C, 100.0), set(C:context|topic, wdeMathematics), "{RES,d}").
#    train(de) :- and(or("was (gibt|ist|ergibt) {natnum:W} (durch|geteilt durch) {natnum2:W}", "(berechne|rechne) (bitte|) {natnum:W} (durch|geteilt durch) {natnum2:W}", "teile (bitte|) {natnum:W} durch {natnum2:W}"), ner(de, natnum, tstart(natnum), tend(natnum), C:tokens, N1E, SCORE1), wdpdNumericValue(N1E, N1), r_score(C, SCORE1), ner(de, natnum, tstart(natnum2), tend(natnum2), C:tokens, N2E, SCORE2), wdpdNumericValue(N2E, N2), r_score(C, SCORE2), set(RES, /(N1, N2)), r_score(C, 100.0), set(C:context|topic, wdeMathematics), "{RES,d}").
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

#    train(en) :- and("about prime numbers", "what about them?", set(C:context|topic, wdeMathematics)).
#    train(de) :- and("über primzahlen", "Was ist damit?", set(C:context|topic, wdeMathematics)).
#    train(en) :- and("(compute|calculate) (it|) (please|)", "What would you like me to calculate?", set(C:context|topic, wdeMathematics)).
#    train(de) :- and("rechne es (bitte|) aus", "Was hättest Du gerne ausgerechnet?", set(C:context|topic, wdeMathematics)).
#    train(en) :- and("can you philosophise better than calculate", "Maybe?", set(C:context|topic, wdeMathematics)).
#    train(de) :- and("kannst du besser philosophieren als rechnen", "Vielleicht?", set(C:context|topic, wdeMathematics)).
#    train(en) :- and("you can not count", "One two three four five", set(C:context|topic, wdeMathematics)).
#    train(de) :- and("du kannst nicht rechnen", "Eins zwei drei vier fünf", set(C:context|topic, wdeMathematics)).
#    train(en) :- and("what is a talor series", "An infinite sum giving the value of a function in the neighborhood of a point in terms of the derivatives of the function.", set(C:context|topic, wdeMathematics)).
#    train(de) :- and("was ist eine taylorreihe", "Taylorreihen werden benutzt, um den Wert einer Funktion an einer Stelle näherungsweise zu berechnen.", set(C:context|topic, wdeMathematics)).
    k.dte.dt('en', u"what is a sphere", u"A perfectly round ball shaped object.")
    k.dte.dt('de', u"was ist eine kugel", u"Ein perfekt rundes Objekt das die Form eines Balls hat.")

