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

def get_data(k):

    k.dte.set_prefixes([u''])

    # NER, macros

    for lang in ['en', 'de']:
        for res in k.prolog_query("wdpdPositionHeld(PERSON, wdePresidentOfTheUnitedStatesOfAmerica), rdfsLabel(PERSON, %s, LABEL)." % lang):
            s_person = res[0] 
            s_label  = res[1] 
            k.dte.macro(lang, 'known_politicians', {'LABEL': s_label})
        for res in k.prolog_query("wdpdPositionHeld(PERSON, wdePresidentOfGermany), rdfsLabel(PERSON, %s, LABEL)." % lang):
            s_person = res[0] 
            s_label  = res[1] 
            k.dte.macro(lang, 'known_politicians', {'LABEL': s_label})
        for res in k.prolog_query("wdpdPositionHeld(PERSON, wdeFederalChancellorOfGermany), rdfsLabel(PERSON, %s, LABEL)." % lang):
            s_person = res[0] 
            s_label  = res[1] 
            k.dte.macro(lang, 'known_politicians', {'LABEL': s_label})

    k.dte.dt('en', u"do you know politics?", u"a little")
    k.dte.dt('de', u"kennst du dich mit politik aus", u"ein wenig")

    def answer_info_human(c, ts, te):

        def act(c, entity):
            c.kernal.mem_push(c.user, 'f1ent', entity)

        # import pdb; pdb.set_trace()

        for entity, score in c.ner(c.lang, 'human', ts, te):

            # president of the united states

            if c.kernal.prolog_check('wdpPositionHeld(%s, OFFICE_STMT), wdpsPositionHeld(OFFICE_STMT, wdePresidentOfTheUnitedStatesOfAmerica), not(wdpqEndTime(OFFICE_STMT, _)).' % entity):
                if c.kernal.prolog_check('wdpdSexOrGender(%s, wdeMale),!.' % entity):
                    if c.lang=='de':
                        c.resp(u"Ist der nicht der US Präsident?", score=score+10, action=act, action_arg=entity)
                    else:
                        c.resp(u"Isn't he the current US President?", score=score+10, action=act, action_arg=entity)
                else:
                    if c.lang=='de':
                        c.resp(u"Ist sie nicht die US Präsidentin?", score=score+10, action=act, action_arg=entity)
                    else:
                        c.resp(u"Isn't she the current US President?", score=score+10, action=act, action_arg=entity)

            elif c.kernal.prolog_check('wdpPositionHeld(%s, OFFICE_STMT), wdpsPositionHeld(OFFICE_STMT, wdePresidentOfTheUnitedStatesOfAmerica).' % entity):
                if c.kernal.prolog_check('wdpdSexOrGender(%s, wdeMale),!.' % entity):
                    if c.lang=='de':
                        c.resp(u"War der nicht mal US Präsident?", score=score+10, action=act, action_arg=entity)
                    else:
                        c.resp(u"Isn't he a former US President?", score=score+10, action=act, action_arg=entity)
                else:
                    if c.lang=='de':
                        c.resp(u"War sie nicht mal US Präsidentin?", score=score+10, action=act, action_arg=entity)
                    else:
                        c.resp(u"Isn't she a former US President?", score=score+10, action=act, action_arg=entity)

            # german chancellor

            if c.kernal.prolog_check('wdpPositionHeld(%s, OFFICE_STMT), wdpsPositionHeld(OFFICE_STMT, wdeFederalChancellorOfGermany), not(wdpqEndTime(OFFICE_STMT, _)).' % entity):
                if c.kernal.prolog_check('wdpdSexOrGender(%s, wdeMale),!.' % entity):
                    if c.lang=='de':
                        c.resp(u"Ist der nicht der Bundeskanzler?", score=score+10, action=act, action_arg=entity)
                    else:
                        c.resp(u"Isn't he the current German chancellor?", score=score+10, action=act, action_arg=entity)
                else:
                    if c.lang=='de':
                        c.resp(u"Ist sie nicht die Bundeskanzlerin?", score=score+10, action=act, action_arg=entity)
                    else:
                        c.resp(u"Isn't she the current German chancellor?", score=score+10, action=act, action_arg=entity)

            elif c.kernal.prolog_check('wdpPositionHeld(%s, OFFICE_STMT), wdpsPositionHeld(OFFICE_STMT, wdeFederalChancellorOfGermany).' % entity):
                if c.kernal.prolog_check('wdpdSexOrGender(%s, wdeMale),!.' % entity):
                    if c.lang=='de':
                        c.resp(u"War der nicht mal Bundeskanzler?", score=score+10, action=act, action_arg=entity)
                    else:
                        c.resp(u"Isn't he a former German chancellor?", score=score+10, action=act, action_arg=entity)
                else:
                    if c.lang=='de':
                        c.resp(u"War sie nicht mal Bundeskanzlerin?", score=score+10, action=act, action_arg=entity)
                    else:
                        c.resp(u"Isn't she a former German chancellor?", score=score+10, action=act, action_arg=entity)

            # german president

            if c.kernal.prolog_check('wdpPositionHeld(%s, OFFICE_STMT), wdpsPositionHeld(OFFICE_STMT, wdePresidentOfGermany), not(wdpqEndTime(OFFICE_STMT, _)).' % entity):
                if c.kernal.prolog_check('wdpdSexOrGender(%s, wdeMale),!.' % entity):
                    if c.lang=='de':
                        c.resp(u"Ist der nicht der Bundespräsident?", score=score+10, action=act, action_arg=entity)
                    else:
                        c.resp(u"Isn't he the current German president?", score=score+10, action=act, action_arg=entity)
                else:
                    if c.lang=='de':
                        c.resp(u"Ist sie nicht die Bundespräsidentin?", score=score+10, action=act, action_arg=entity)
                    else:
                        c.resp(u"Isn't she the current German president?", score=score+10, action=act, action_arg=entity)

            elif c.kernal.prolog_check('wdpPositionHeld(%s, OFFICE_STMT), wdpsPositionHeld(OFFICE_STMT, wdePresidentOfGermany).' % entity):
                if c.kernal.prolog_check('wdpdSexOrGender(%s, wdeMale),!.' % entity):
                    if c.lang=='de':
                        c.resp(u"War der nicht mal Bundespräsident?", score=score+10, action=act, action_arg=entity)
                    else:
                        c.resp(u"Isn't he a former German president?", score=score+10, action=act, action_arg=entity)
                else:
                    if c.lang=='de':
                        c.resp(u"War sie nicht mal Bundespräsidentin?", score=score+10, action=act, action_arg=entity)
                    else:
                        c.resp(u"Isn't she a former German president?", score=score+10, action=act, action_arg=entity)

    k.dte.dt('en', [u"(do you know | do you happen to know) {known_humans:W}",
                    u"(what about | who is | who was | what is| what do you think of|by|do you know|) {known_humans:W} (then|)"], 
                   answer_info_human, ['known_humans_0_start', 'known_humans_0_end'])
    k.dte.dt('de', [u"(kennst du|kennst du eigentlich) {known_humans:W}", 
                    u"(wer ist|wer ist denn| durch| wer war | wer war eigentlich | wer war denn| wer ist eigentlich|was ist mit|was ist eigentlich mit|was weisst du über|was weisst du eigentlich über| was hältst du von|kennst du|) {known_humans:W}"],
                   answer_info_human, ['known_humans_0_start', 'known_humans_0_end'])

    k.dte.ts('en', 't0000', [(u"Computer, do you know Donald Trump?", u"Isn't he the current US President")])
    k.dte.ts('de', 't0001', [(u"Computer, kennst du eigentlich Donald Trump?", u"Ist der nicht der US Präsident?")])

    k.dte.ts('en', 't0002', [(u"Computer, who is Ronald Reagan?", u"Isn't he a former US President?")])
    k.dte.ts('de', 't0003', [(u"Computer, wer ist Ronald Reagan?", u"War der nicht mal US Präsident?")])

    def answer_current_position_holder(c, position):

        import dateutil.parser

        def act(c, entity):
            c.kernal.mem_push(c.user, 'f1ent', entity)

        entity   = None
        start_dt = None

        for res in c.kernal.prolog_query('wdpPositionHeld(ENTITY, OFFICE_STMT), wdpsPositionHeld(OFFICE_STMT, %s), not(wdpqEndTime(OFFICE_STMT, _)), rdfsLabel(%s, %s, POSITION_LABEL), rdfsLabel(ENTITY, %s, ENTITY_LABEL), wdpqStartTime(OFFICE_STMT, STV), wboTimeValue(STV, START_TIME).' % (position, position, c.lang, c.lang)):
            q_entity       = res[0] 
            q_pos_label    = res[3] 
            q_entity_label = res[4] 
            q_start_time   = res[6]

            # logging.info ('answer_current_position_holder: %s' % repr(res))

            q_start_dt = dateutil.parser.parse(q_start_time)
            
            if not start_dt or q_start_dt > start_dt:
                entity       = q_entity
                pos_label    = q_pos_label
                entity_label = q_entity_label
                start_dt     = q_start_dt

        if not entity:
            if c.lang == 'de':
                c.resp(u"Da bin ich mir nicht sicher.")
            else:
                c.resp(u"Not sure.")
            return

        if c.lang == 'de':
            c.resp(u"%s ist %s." % (pos_label, entity_label), score=100.0, action=act, action_arg=entity)
        else:
            c.resp(u"%s is %s." % (pos_label, entity_label), score=100.0, action=act, action_arg=entity)

    k.dte.dt('en', u"(Who is|What is the name of) the (US|) president?",
                   answer_current_position_holder, ['wdePresidentOfTheUnitedStatesOfAmerica'])
    k.dte.dt('de', u"(wer ist|wie heißt) (der amerikanische Präsident|der US Präsident|die amerikanische Präsidentin|die US Präsidentin)",
                   answer_current_position_holder, ['wdePresidentOfTheUnitedStatesOfAmerica'])

    k.dte.ts('en', 'uspres00', [(u"Who is the president?", u"President of the United States of America is Donald Trump.")])
    k.dte.ts('de', 'uspres01', [(u"Wer ist der US Präsident?", u"Präsident der Vereinigten Staaten ist Donald Trump.")])

    k.dte.dt('en', u"(about|) foreign policy", u"Delicate topic.")
    k.dte.dt('de', u"(über|) aussenpolitik", u"Heikles Thema.")

    k.dte.dt('en', u"who is saddam", u"He is no longer, I think.")
    k.dte.dt('de', u"wer ist saddam", u"Der ist nicht mehr, glaube ich.")

    k.dte.dt('en', [u"what do you know about bill clinton?",
                    u"what do you think about bill clinton?"],
                   [u"He served as the 42nd President of the United States.",
                    u"It depends upon what your definition of is is."])
    k.dte.dt('de', [u"was denkst du über bill clinton",
                    u"was hältst du von bill clinton"],
                   [u"Er war der zweiundvierzigste Präsident der USA.",
                    u"Das ist der mit der Definition..."])

    k.dte.ts('en', 't0004', [(u"Computer, do you know Angela Merkel?", u"Isn't she the current German Chancellor?")])
    k.dte.ts('de', 't0005', [(u"Computer, kennst du eigentlich Angela Merkel?", u"Ist sie nicht die Bundeskanzlerin?")])

    k.dte.ts('en', 't0006', [(u"Computer, who is Helmut Kohl?", u"Isn't he a former German Chancellor?")])
    k.dte.ts('de', 't0007', [(u"Computer, wer ist Helmut Kohl?", u"War der nicht mal Bundeskanzler?")])

    k.dte.dt('en', u"(Who is|What is the name of) the (german|) Chancellor?",
                   answer_current_position_holder, ['wdeFederalChancellorOfGermany'])
    k.dte.dt('de', u"(wer ist|wie heißt) (der bundeskanzler|die bundeskanzlerin)",
                   answer_current_position_holder, ['wdeFederalChancellorOfGermany'])

    k.dte.ts('en', 'chancellor00', [(u"Who is the Chancellor?", u"Federal chancellor of Germany is Angela Merkel.")])
    k.dte.ts('de', 'chancellor01', [(u"Wer ist die Bundeskanzlerin", u"Bundeskanzler ist Angela Merkel.")])

    k.dte.ts('en', 't0008', [(u"Computer, do you know Frank-Walter Steinmeier?", u"Isn't he the current German President?")])
    k.dte.ts('de', 't0009', [(u"Computer, kennst du eigentlich Frank-Walter Steinmeier?", u"Ist der nicht der Bundespräsident?")])

    k.dte.ts('en', 't0010', [(u"Computer, who is Joachim Gauck?", u"Isn't he a former German President?")])
    k.dte.ts('de', 't0011', [(u"Computer, wer ist Joachim Gauck?", u"War der nicht mal Bundespräsident?")])

    k.dte.dt('en', u"(Who is|What is the name of) the German president?",
                   answer_current_position_holder, ['wdePresidentOfGermany'])
    k.dte.dt('de', u"(wer ist|wie heißt) (der deutsche Präsident|der Präsident|Präsident|Bundespräsident|die deutsche Präsidentin|die Präsidentin|Präsidentin|Bundespräsidentin)",
                   answer_current_position_holder, ['wdePresidentOfGermany'])

    k.dte.ts('en', 'depres00', [(u"Who is the German president?", u"President of Germany is Frank Walter Steinmeier.")])
    k.dte.ts('de', 'depres01', [(u"Wer ist Präsident?", u"Bundespräsident ist Frank Walter Steinmeier.")])

    def answer_position_predsucc(c, pred_succ, ts, te, check_topic):

        def act(c, film):
            c.kernal.mem_push(c.user, 'f1ent', film)

        if check_topic:
            f1ent = c.kernal.mem_get_multi(c.user, 'f1ent')
            if not f1ent:
                return
            f1ent = f1ent[0][0]
            if not c.kernal.prolog_check('instances_of(%s, %s).' % ('wdeHuman', f1ent)):
                return

        if ts>=0:
            fss = c.ner(c.lang, 'human', ts, te)
        else:
            fss = c.kernal.mem_get_multi(c.user, 'f1ent')

        for position in ['wdePresidentOfTheUnitedStatesOfAmerica','wdePresidentOfGermany','wdeFederalChancellorOfGermany']:
            for human, score in fss:
                query = 'wdpPositionHeld(%s, OFFICE_STMT), wdpsPositionHeld(OFFICE_STMT, %s), %s(OFFICE_STMT, PREDECESSOR), %s \= PREDECESSOR, rdfsLabel(%s, %s, POSLABEL), rdfsLabel(%s, %s, HLABEL), rdfsLabel(PREDECESSOR, %s, PLABEL).' \
                         % (             human,                                    position, pred_succ,                  human,                    position, c.lang,               human, c.lang,                           c.lang)

                # logging.info(query)

                # import pdb; pdb.set_trace()

                for res in c.kernal.prolog_query(query):
                    s_p        = res[1] 
                    s_poslabel = res[2] 
                    s_hlabel   = res[3] 
                    s_plabel   = res[4] 

                    if pred_succ == 'wdpqReplaces':
                        if c.lang=='de':
                            c.resp(u"Der Vorgänger von %s als %s war %s." % (s_hlabel, s_poslabel, s_plabel), score=score, action=act, action_arg=s_p)
                        else:
                            c.resp(u"The predecessor of %s as %s was %s." % (s_hlabel, s_poslabel, s_plabel), score=score, action=act, action_arg=s_p)
                    else:
                        if c.lang=='de':
                            c.resp(u"Der Nachfolger von %s als %s war %s." % (s_hlabel, s_poslabel, s_plabel), score=score, action=act, action_arg=s_p)
                        else:
                            c.resp(u"The successor of %s as %s was %s." % (s_hlabel, s_poslabel, s_plabel), score=score, action=act, action_arg=s_p)

    k.dte.dt('en', u"who (is|was|happened to be) the predecessor of {known_politicians:LABEL} (by the way|) ?",
                   answer_position_predsucc, ['wdpqReplaces', 'known_politicians_0_start', 'known_politicians_0_end', False])
    k.dte.dt('de', u"wer (ist|war) (eigentlich|) (die vorgängerin|der vorgänger) von {known_politicians:LABEL} ?",
                   answer_position_predsucc, ['wdpqReplaces', 'known_politicians_0_start', 'known_politicians_0_end', False])

    k.dte.ts('en', 'predsucc12', [(u"who happened to be the predecessor of Ronald Reagan?", u"the predecessor of ronald reagan as president of the united states of america was jimmy carter")])
    k.dte.ts('de', 'predsucc13', [(u"wer war eigentlich der vorgänger von Ronald Reagan?", u"der vorgänger von ronald reagan als präsident der vereinigten staaten war jimmy carter")])

    k.dte.ts('en', 'predsucc14', [(u"who happened to be the predecessor of Helmut Kohl?", u"the predecessor of helmut kohl as federal chancellor of germany was helmut schmidt")])
    k.dte.ts('de', 'predsucc15', [(u"wer war eigentlich der vorgänger von Helmut Kohl?", u"der vorgänger von helmut kohl als bundeskanzler war helmut schmidt.")])

    k.dte.ts('en', 'predsucc16', [(u"who happened to be the predecessor of Richard von Weizsäcker?", u"the predecessor of richard nixon as president of the united states of america was lyndon b johnson")])
    k.dte.ts('de', 'predsucc17', [(u"wer war eigentlich der vorgänger von Richard von Weizsäcker?", u"der vorgänger von richard nixon als präsident der vereinigten staaten war lyndon b johnson")])

    k.dte.dt('en', u"who (is|was|happened to be) the successor of {known_politicians:LABEL} (by the way|) ?",
                   answer_position_predsucc, ['wdpqReplacedBy', 'known_politicians_0_start', 'known_politicians_0_end', False])
    k.dte.dt('de', u"wer (ist|war) (eigentlich|) (die nachfolgerin|der nachfolger) von {known_politicians:LABEL} ?",
                   answer_position_predsucc, ['wdpqReplacedBy', 'known_politicians_0_start', 'known_politicians_0_end', False])

    k.dte.ts('en', 'predsucc18', [(u"who happened to be the successor of Ronald Reagan?", u"the successor of ronald reagan as president of the united states of america was george h w bush")])
    k.dte.ts('de', 'predsucc19', [(u"wer war eigentlich der nachfolger von Ronald Reagan?", u"der nachfolger von ronald reagan als präsident der vereinigten staaten war george h w bush")])

    k.dte.ts('en', 'predsucc20', [(u"who happened to be the successor of Helmut Kohl?", u"the successor of helmut kohl as federal chancellor of germany was gerhard schröder")])
    k.dte.ts('de', 'predsucc21', [(u"wer war eigentlich der nachfolger von Helmut Kohl?", u"der nachfolger von helmut kohl als bundeskanzler war gerhard schröder")])

    k.dte.ts('en', 'predsucc22', [(u"who happened to be the successor of Richard von Weizsäcker?", u"the successor of richard nixon as president of the united states of america was gerald ford")])
    k.dte.ts('de', 'predsucc23', [(u"wer war eigentlich der nachfolger von Richard von Weizsäcker?", u"der nachfolger von richard nixon als präsident der vereinigten staaten war gerald ford")])

