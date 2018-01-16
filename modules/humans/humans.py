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

    # NER, macros

    for lang in ['en', 'de']:
        for res in k.prolog_query("wdpdInstanceOf(HUMAN, wdeHuman), rdfsLabel(HUMAN, %s, LABEL)." % lang):
            s_human = res[0] 
            s_label = res[1] 
            k.dte.ner(lang, 'human', s_human, s_label)
            k.dte.macro(lang, 'known_humans', {'W': s_label})

    def answer_info_human(c, ts, te):

        def act(c, entity):
            c.kernal.mem_push(c.user, 'f1ent', entity)

        # import pdb; pdb.set_trace()

        for entity, score in c.ner(c.lang, 'human', ts, te):
            if c.kernal.prolog_check('wdpdSexOrGender(%s, wdeMale),!.' % entity):
                if c.lang=='en':
                    c.resp(u"His name sounds familiar.", score=score, action=act, action_arg=entity)
                    c.resp(u"Would you like to know more about him?", score=score, action=act, action_arg=entity)
                elif c.lang=='de':
                    c.resp(u"Der Name kommt mir bekannt vor.", score=score, action=act, action_arg=entity)
                    c.resp(u"Möchtest Du mehr über ihn wissen?", score=score, action=act, action_arg=entity)
                else:
                    raise Exception ('Sorry, language %s not implemented yet.' % c.lang)
            else:
                if c.lang=='en':
                    c.resp(u"Her name sounds familiar.", score=score, action=act, action_arg=entity)
                    c.resp(u"Would you like to know more about her?", score=score, action=act, action_arg=entity)
                elif c.lang=='de':
                    c.resp(u"Der Name kommt mir bekannt vor.", score=score, action=act, action_arg=entity)
                    c.resp(u"Möchtest Du mehr über sie wissen?", score=score, action=act, action_arg=entity)
                else:
                    raise Exception ('Sorry, language %s not implemented yet.' % c.lang)

    k.dte.dt('en', [u"(do you know | do you happen to know) {known_humans:W}",
                    u"(what about | who is | who was | what is| what do you think of|by|do you know|) {known_humans:W} (then|)"], 
                   answer_info_human, ['known_humans_0_start', 'known_humans_0_end'])
    k.dte.dt('de', [u"(kennst du|kennst du eigentlich) {known_humans:W}", 
                    u"(wer ist|wer ist denn| durch| wer war | wer war eigentlich | wer war denn| wer ist eigentlich|was ist mit|was ist eigentlich mit|was weisst du über|was weisst du eigentlich über| was hältst du von|kennst du|) {known_humans:W}"],
                   answer_info_human, ['known_humans_0_start', 'known_humans_0_end'])
    k.dte.ts('de', 't0000', [(u"Kennst Du Angela Merkel?", u"Der Name kommt mir bekannt vor.", [])])
    k.dte.ts('en', 't0001', [(u"Do you know Angela Merkel?", u"Would you like to know more about her?", [])])
    k.dte.ts('de', 't0002', [(u"Wer ist Angela Merkel?", u"Möchtest Du mehr über sie wissen?", [])])
    k.dte.ts('en', 't0003', [(u"What about Angela Merkel?", u"Her name sounds familiar.", [])])
 
    k.dte.dt('en', u"how is {known_humans:W}?", u"I have no information on that.")
    k.dte.dt('de', u"wie geht es {known_humans:W}?", u"Darüber habe ich keine Informationen.")

    k.dte.dt('en', [u"is {known_humans:W} nice",
                    u"tell me more about {known_humans:W}",
                    u"what else do you know about {known_humans:W}?",
                    u"what is (her|his) (girlfriend's|boyfriend's) name"],
                   [u"Sorry, I have no further information.",
                    u"There is no further information here."])
    k.dte.dt('de', [u"ist {known_humans:W} nett",
                    u"erzähl mir mehr über {known_humans:W}",
                    u"was weißt du sonst noch über {known_humans:W}",
                    u"wie heißt (ihre|seine) freundin",
                    u"wie heißt (ihr|sein) freund"],
                   [u"Tut mir leid, mehr Informationen habe ich nicht.",
                    u"Es gibt hier nicht mehr Informationen."])

    def answer_human_born_where(c, ts, te):

        def act(c, args):
            human, bp = args
            c.kernal.mem_push(c.user, 'f1ent', human)
            c.kernal.mem_push(c.user, 'f1loc', bp)

        if ts>=0:
            hss = c.ner(c.lang, 'human', ts, te)
        else:
            # import pdb; pdb.set_trace()
            hss = c.kernal.mem_get_multi(c.user, 'f1ent')

        for human, score in hss:
            hlabel = c.kernal.prolog_query_one('rdfsLabel(%s, %s, L).' % (human, c.lang))
            bp = c.kernal.prolog_query_one("wdpdPlaceOfBirth(%s, BP)." % human)
            if hlabel and bp:
                bplabel = c.kernal.prolog_query_one('rdfsLabel(%s, %s, L).' % (bp, c.lang))
                if c.lang == 'en':
                    c.resp(u"%s was born in %s, I think." % (hlabel, bplabel), score=score, action=act, action_arg=(human, bp)) 
                    c.resp(u"I believe %s was born in %s." % (hlabel, bplabel), score=score, action=act, action_arg=(human, bp))
                elif c.lang == 'de':
                    c.resp(u"%s ist in %s geboren, denke ich." % (hlabel, bplabel), score=score, action=act, action_arg=(human, bp)) 
                    c.resp(u"Ich glaube %s ist in %s geboren." % (hlabel, bplabel), score=score, action=act, action_arg=(human, bp))
                else:
                    raise Exception ('Sorry, language %s not implemented yet.' % c.lang)

    k.dte.dt('en', [u"(where|in which town|in which city) (was|is) {known_humans:W} born?",
                    u"which (was|is) (the birthplace|place of birth) of {known_humans:W}?"],
                   answer_human_born_where, ['known_humans_0_start', 'known_humans_0_end'])
    k.dte.dt('de', [u"(wo|in welcher stadt) (wurde|ist) (eigentlich|) {known_humans:W} geboren?",
                    u"(was|welches) (war|ist) (eigentlich|) (der Geburtsort|die Geburtsstadt) von {known_humans:W}?"],
                   answer_human_born_where, ['known_humans_0_start', 'known_humans_0_end'])

    k.dte.dt('en', [u"(and|) (where|in which town|in which city) (was|is) (she|he) born (again|)?",
                    u"(and|) which is (the birthplace|place of birth) of (him|her) (again|)?"],
                   answer_human_born_where, [-1, -1])
    k.dte.dt('de', [u"(und|) (wo|in welcher stadt) (wurde|ist) (eigentlich|) (er|sie) (nochmal|) geboren?",
                    u"(und|) welches ist (eigentlich|nochmal|) (der Geburtsort|die Geburtsstadt) von (ihm|ihr)?"],
                   answer_human_born_where, [-1, -1])
 
    k.dte.ts('en', 't0004', [(u"Where was Angela Merkel born?", u"Angela Merkel was born in Barmbek-Nord, I think.", []),
                               (u"What were we talking about?", u"Didn't we talk about angela merkel?", []),
                               (u"And where was she born again?", u"I believe Angela Merkel was born in Barmbek-Nord", [])])
    k.dte.ts('de', 't0005', [(u"Wo wurde Angela Merkel geboren?", u"Angela Merkel ist in Barmbek-Nord geboren, denke ich", []),
                               (u"Welches Thema hatten wir?", u"Sprachen wir nicht über Angela Merkel?", []),
                               (u"Und wo wurde sie nochmal geboren?", u"Angela Merkel ist in Barmbek-Nord geboren, denke ich", [])])

    def answer_human_born_country(c, ts, te):

        def act(c, args):
            human, cp = args
            c.kernal.mem_push(c.user, 'f1ent', human)
            c.kernal.mem_push(c.user, 'f1loc', cp)

        if ts>=0:
            hss = c.ner(c.lang, 'human', ts, te)
        else:
            hss = c.kernal.mem_get_multi(c.user, 'f1ent')

        for human, score in hss:
            hlabel = c.kernal.prolog_query_one('rdfsLabel(%s, %s, L).' % (human, c.lang))
            # import pdb; pdb.set_trace()
            cp = c.kernal.prolog_query_one('wdpdPlaceOfBirth(%s, BP), wdpdCountry(BP, COUNTRY).'% human, idx=1)
            if hlabel and cp:
                cplabel = c.kernal.prolog_query_one('rdfsLabel(%s, %s, L).' % (cp, c.lang))
                if c.lang == 'en':
                    c.resp(u"%s was born in %s, I think." % (hlabel, cplabel), score=score, action=act, action_arg=(human, cp)) 
                    c.resp(u"I believe %s was born in %s." % (hlabel, cplabel), score=score, action=act, action_arg=(human, cp))
                elif c.lang == 'de':
                    c.resp(u"%s ist in %s geboren, denke ich." % (hlabel, cplabel), score=score, action=act, action_arg=(human, cp)) 
                    c.resp(u"Ich glaube %s ist in %s geboren." % (hlabel, cplabel), score=score, action=act, action_arg=(human, cp))
                else:
                    raise Exception ('Sorry, language %s not implemented yet.' % c.lang)

    k.dte.dt('en', [u"in which country (was|is) {known_humans:W} born?",
                    u"which (was|is) the land of birth of {known_humans:W}?"],
                   answer_human_born_country, ['known_humans_0_start', 'known_humans_0_end'])
    k.dte.dt('de', [u"in welchem land (wurde|ist) (eigentlich|) {known_humans:W} geboren?",
                    u"(was|welches) (war|ist) (eigentlich|) das Geburtsland von {known_humans:W}?"],
                   answer_human_born_country, ['known_humans_0_start', 'known_humans_0_end'])

    k.dte.dt('en', [u"(and|) in which country (was|is) (she|he) born (again|)?",
                    u"(and|) which (was|is) the country of birth of (him|her) (again|)?"],
                   answer_human_born_country, [-1, -1])
    k.dte.dt('de', [u"(und|) in welchem land (wurde|ist) (eigentlich|) (er|sie) (nochmal|) geboren?",
                    u"(und|) welches (war|ist) (eigentlich|nochmal|) das Geburtsland von (ihm|ihr)?"],
                   answer_human_born_country, [-1, -1])

    k.dte.ts('en', 't0104', [(u"In which country was Angela Merkel born?", u"Angela Merkel was born in Germany, I think.", []),
                               (u"What were we talking about?", u"Didn't we talk about angela merkel?", []),
                               (u"And in which country was she born again?", u"I believe Angela Merkel was born in Germany", [])])
    k.dte.ts('de', 't0105', [(u"In welchem Land ist Angela Merkel geboren?", u"Angela Merkel ist in Deutschland geboren, denke ich", []),
                               (u"Welches Thema hatten wir?", u"Sprachen wir nicht über Angela Merkel?", []),
                               (u"Und in welchem Land wurde sie nochmal geboren?", u"Angela Merkel ist in Deutschland geboren, denke ich", [])])

#     def answer_human_born_when_tokens(en, TS, TE):
#         and(ner(en, human, TS, TE, C:tokens, HUMAN, SCORE), set(C:mem|f1ent, HUMAN), r_score(C, SCORE), rdfsLabel(HUMAN, en, HLABEL), wdpdDateOfBirth(HUMAN, BD), set(C:mem|f1time, BD), transcribe_date(en, dativ, BD, BDLABEL), or("{HLABEL,s} was born on {BDLABEL,s}, I think.", "I believe {HLABEL,s} was born on {BDLABEL,s}."))
#     def answer_human_born_when_tokens(de, TS, TE):
#         and(ner(de, human, TS, TE, C:tokens, HUMAN, SCORE), set(C:mem|f1ent, HUMAN), r_score(C, SCORE), rdfsLabel(HUMAN, de, HLABEL), wdpdDateOfBirth(HUMAN, BD), set(C:mem|f1time, BD), transcribe_date(de, dativ, BD, BDLABEL), or("{HLABEL,s} ist am {BDLABEL,s} geboren, denke ich.", "Ich glaube {HLABEL,s} ist am {BDLABEL,s} geboren."))
#     k.dte.dt('en', u"(when|in which year) (was|is) {known_humans:W} born?",
#                    % inline(answer_human_born_when_tokens(en, tstart(known_humans), tend(known_humans))))
#     k.dte.dt('de', u"(wann|in welchem Jahr) (wurde|ist) (eigentlich|) {known_humans:W} geboren?",
#                    % inline(answer_human_born_when_tokens(de, tstart(known_humans), tend(known_humans))))
# 
#     k.dte.dt('en', u"(when is|on what day is) {known_humans:W}S birthday?",
#                    % inline(answer_human_born_when_tokens(en, tstart(known_humans), tend(known_humans))))
#     k.dte.dt('de', u"(wann hat|an welchem Tag hat) (eigentlich|) {known_humans:W} Geburtstag?",
#                    % inline(answer_human_born_when_tokens(de, tstart(known_humans), tend(known_humans))))
# 
#     k.dte.dt('en', u"how old is {known_humans:W}?",
#                    % inline(answer_human_born_when_tokens(en, tstart(known_humans), tend(known_humans))))
#     k.dte.dt('de', u"wie alt ist {known_humans:W}?",
#                    % inline(answer_human_born_when_tokens(de, tstart(known_humans), tend(known_humans))))
# 
#     def answer_human_born_when_context(en):
#         and(mem(C, f1ent, HUMAN), rdfsLabel(HUMAN, en, HLABEL), wdpdDateOfBirth(HUMAN, BD), set(C:mem|f1time, BD), transcribe_date(en, dativ, BD, BDLABEL), or("{HLABEL,s} was born on {BDLABEL,s}, I think.", "I believe {HLABEL,s} was born on {BDLABEL,s}."))
#     def answer_human_born_when_context(de):
#         and(mem(C, f1ent, HUMAN), rdfsLabel(HUMAN, de, HLABEL), wdpdDateOfBirth(HUMAN, BD), set(C:mem|f1time, BD), transcribe_date(de, dativ, BD, BDLABEL), or("{HLABEL,s} ist am {BDLABEL,s} geboren, denke ich.", "Ich glaube {HLABEL,s} ist am {BDLABEL,s} geboren."))
#     k.dte.dt('en', u"(and|) (when|in which year) (was|is) (he|she) born (again|)?",
#                    % inline(answer_human_born_when_context(en)))
#     k.dte.dt('de', u"(und|) (wann|in welchem Jahr) (wurde|ist) (eigentlich|) (sie|er) (nochmal|) geboren?",
#                    % inline(answer_human_born_when_context(de)))
# 
#     k.dte.ts('en', 't0006', [(u"When was Angela Merkel born?", u"I believe Angela Merkel was born on July 17, 1954.", []),
#                                (u"What were we talking about?", u"Didn't we talk about angela merkel?", []),
#                                (u"And when was she born?", u"I believe Angela Merkel was born on July 17, 1954.", []),
#                                (u"And where was she born again?", u"I believe Angela Merkel was born in Barmbek-Nord", [])])
#     k.dte.ts('de', 't0007', [(u"Wann wurde Angela Merkel geboren?", u"Ich glaube Angela Merkel ist am siebzehnten Juli 1954 geboren.", []),
#                                (u"Welches Thema hatten wir?", u"Sprachen wir nicht über Angela Merkel?", []),
#                                (u"Und wann wurde sie nochmal geboren?", u"Ich glaube Angela Merkel ist am siebzehnten Juli 1954 geboren.", []),
#                                (u"Und wo wurde sie nochmal geboren?", u"Angela Merkel ist in Barmbek-Nord geboren, denke ich", [])])
# 
#     def answer_human_residence_tokens(en, TS, TE):
#         and(ner(en, human, TS, TE, C:tokens, HUMAN, SCORE), set(C:mem|f1ent, HUMAN), r_score(C, SCORE), rdfsLabel(HUMAN, en, HLABEL), wdpdResidence(HUMAN, RESIDENCE), set(C:mem|f1loc, RESIDENCE), rdfsLabel(RESIDENCE, en, RLABEL), or("{HLABEL,s} lives in {RLABEL,s}, I think.", "I believe {HLABEL,s} lives in {RLABEL,s}."))
#     def answer_human_residence_tokens(de, TS, TE):
#         and(ner(de, human, TS, TE, C:tokens, HUMAN, SCORE), set(C:mem|f1ent, HUMAN), r_score(C, SCORE), rdfsLabel(HUMAN, de, HLABEL), wdpdResidence(HUMAN, RESIDENCE), set(C:mem|f1loc, RESIDENCE), rdfsLabel(RESIDENCE, de, RLABEL), or("{HLABEL,s} lebt in {RLABEL,s}, glaube ich.", "Ich denke {HLABEL,s} lebt in {RLABEL,s}."))
#     k.dte.dt('en', u"(and|) (where|in which town|in which city|in which place) (does|did) {known_humans:W} (reside|live) (again|)?",
#                    % inline(answer_human_residence_tokens(en, tstart(known_humans), tend(known_humans))))
#     k.dte.dt('de', u"(und|) (wo|in welcher Stadt|an welchem Ort) (lebte|lebt|wohnt) {known_humans:W} (eigentlich|) (nochmal|)?",
#                    % inline(answer_human_residence_tokens(de, tstart(known_humans), tend(known_humans))))
# 
#     def answer_human_residence_context(en):
#         and(mem(C, f1ent, HUMAN), rdfsLabel(HUMAN, en, HLABEL), wdpdResidence(HUMAN, RESIDENCE), set(C:mem|f1loc, RESIDENCE), rdfsLabel(RESIDENCE, en, RLABEL), or("{HLABEL,s} lives in {RLABEL,s}, I think.", "I believe {HLABEL,s} lives in {RLABEL,s}."))
#     def answer_human_residence_context(de):
#         and(mem(C, f1ent, HUMAN), rdfsLabel(HUMAN, de, HLABEL), wdpdResidence(HUMAN, RESIDENCE), set(C:mem|f1loc, RESIDENCE), rdfsLabel(RESIDENCE, de, RLABEL), or("{HLABEL,s} lebt in {RLABEL,s}, glaube ich.", "Ich denke {HLABEL,s} lebt in {RLABEL,s}."))
#     k.dte.dt('en', u"(and|) (where|in which town|in which city|in which place) (does|did) (he|she) (reside|live) (again|)?",
#                    % inline(answer_human_residence_context(en)))
#     k.dte.dt('de', u"(und|) (wo|in welcher Stadt|an welchem Ort) (lebte|lebt|wohnt) (sie|er) (eigentlich|) (nochmal|)?",
#                    % inline(answer_human_residence_context(de)))
# 
#     k.dte.ts('en', 't0008', [(u"Where does Stephen King live?", u"I believe Stephen King lives in Maine.", []),
#                                (u"And where does he live again?", u"I believe Stephen King lives in Maine.", [])])
#     k.dte.ts('de', 't0009', [(u"Wo wohnt Stephen King?", u"Ich denke Stephen King lebt in Maine.", []),
#                                (u"Und wo wohnt er nochmal?", u"Ich denke Stephen King lebt in Maine.", [])])
 

    k.dte.dt('en', [u"do you know (turing|von neumann|einstein|Marianne Rosenberg|pele|goethe|shakespeare|beethoven)?",
                    u"do you know (captain kirk|alex|elvira|homer|marvin)?"],
                   [u"that name sounds familiar"
                    u"where have I heard that name before?"])

    k.dte.dt('de', [u"kennst du (turing|von neumann|einstein|Marianne Rosenberg|pele|goethe|shakespeare|beethoven)?",
                    u"kennst du (captain kirk|alex|elvira|homer|marvin)?"],
                   [u"der name klingt bekannt", 
                    u"wo habe ich diesen namen schon einmal gehört?"])

    k.dte.dt('en', u"what is a human?", u"Humans are the only living members of the genus Homo.")
    k.dte.dt('de', u"was ist ein mensch", u"Unter Mensch versteht man den anatomisch modernen Menschen.")

    k.dte.dt('en', u"who is the richest man on earth?", u"Bill Gates?")
    k.dte.dt('de', u"wer ist der reichste mensch auf der erde", u"Bill Gates?")

    k.dte.dt('en', u"with andreas", u"excellent.")
    k.dte.dt('de', u"mit andreas", u"prima.")

    k.dte.dt('en', u"a stupid person", u"Are you sure?")
    k.dte.dt('de', u"ein dummer mensch", u"Bist Du sicher?")

