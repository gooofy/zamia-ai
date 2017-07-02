#!/usr/bin/env python
# -*- coding: utf-8 -*- 

from utils import hears, says

#
# say again type follow up questions
#

def nlp_base_sayagain_s(lang, s):

    if lang == 'en':

        return [ hears ('en', s, 'huh?'),
                 hears ('en', s, 'say again please?'),
                 hears ('en', s, 'say again?'),
                 hears ('en', s, 'what was that?') ]

    elif lang == 'de':

        return [ hears ('de', s, 'was?'),
                 hears ('de', s, 'wie war das?'),
                 hears ('de', s, 'bitte sag nochmal was du gesagt hast?'),
                 hears ('de', s, 'wie bitte?') ]

    else:
        raise Exception ('unsupported language: %s' % lang)


def nlp_base_isaid_r (lang, r):

    if lang == 'en':

        return [ says ('en', r, 'I said'),
                 says ('en', r, 'As I just said'),
                 says ('en', r, 'I repeat') ]

    elif lang == 'de':

        return [ says ('de', r, 'Ich sagte'),
                 says ('de', r, 'Wie ich eben sagte'),
                 says ('de', r, 'Nochmal'),
                 says ('de', r, 'Ich wiederhole') ]

    else:
        raise Exception ('unsupported language: %s' % lang)
    

#
# very basic building blocks for topic handling
#

def nlp_base_whatwasourtopic_s(lang, s):

    if lang == 'en':

        res = []

        res.extend(hears ('en', s, ['What', ['were we talking','did we talk'], 'about', ['again','']]))
        res.extend(hears ('en', s, [['Which', 'What'], 'was our topic', ['again','']]))
        res.extend(hears ('en', s, ['Give me a hint']))
        res.extend(hears ('en', s, ['Which topic did we have', ['again','']]))
        res.extend(hears ('en', s, ['I', ['think', 'believe'], 'I lost my train of thought', ['just now','']]))
        res.extend(hears ('en', s, [['lets get',''], 'Back to our topic']))

    elif lang == 'de':

        res = []

        res.extend(hears ('de', s, [['Wovon','Worüber','Was'], ['hatten','haben'], 'wir', ['eben',''], 'gesprochen']))
        res.extend(hears ('de', s, [['Wie','Was'], 'war', ['doch gleich','gleich',''], 'unser Thema']))
        res.extend(hears ('de', s, ['Hilf mir auf die Sprünge?']))
        res.extend(hears ('de', s, ['Welches Thema hatten wir', ['doch gleich','']]))
        res.extend(hears ('de', s, ['Ich', ['glaub','glaube',''], 'ich habe', ['jetzt',''], 'den Faden verloren']))
        res.extend(hears ('de', s, ['jetzt habe ich' ,['glaube ich',''], 'den Faden verloren']))
        res.extend(hears ('de', s, ['also zurück zum thema']))

    else:
        raise Exception ('unsupported language: %s' % lang)

    return res

# % answer(topic, en) :-
# %     say_eoa(en, 'We have had many topics.'), 
# %     say_eoa(en, 'We were talking about you for the most part, I believe.').
# % 
# % answer(topic, de) :-
# %     say_eoa(de, 'Wir hatten schon viele Themen.'), 
# %     say_eoa(de, 'Ich glaube vor allem über Dich!').
# % 
# % answer(topic, en) :-
# %     context_score(topic, ENTITY, 100, S),
# %     rdf (limit(1),
# %          ENTITY, rdfs:label, LABEL,
# %          filter (lang(LABEL) = 'en')),
# %     say_eoa(en, format_str('We were talking about %s.', LABEL), S).
# % 
# % answer(topic, de) :-
# %     context_score(topic, ENTITY, 100, S),
# %     rdf (limit(1),
# %          ENTITY, rdfs:label, LABEL,
# %          filter (lang(LABEL) = 'de')),
# %     say_eoa(de, format_str('Wir hatten über %s gesprochen.', LABEL), S).
# 
# answerz (I, en, weHaveBeenTalkingAbout, LABEL) :- sayz(I, en, format_str("We have been talking about %s", LABEL)).
# answerz (I, en, weHaveBeenTalkingAbout, LABEL) :- sayz(I, en, format_str("Our topic was %s", LABEL)).
# answerz (I, en, weHaveBeenTalkingAbout, LABEL) :- sayz(I, en, format_str("Didn't we talk about %s", LABEL)).
# 
# answerz (I, de, weHaveBeenTalkingAbout, LABEL) :- sayz(I, de, format_str("Wir hatten über %s gesprochen", LABEL)).
# answerz (I, de, weHaveBeenTalkingAbout, LABEL) :- sayz(I, de, format_str("Unser Thema war %s", LABEL)).
# answerz (I, de, weHaveBeenTalkingAbout, LABEL) :- sayz(I, de, format_str("Sprachen wir nicht über %s ?", LABEL)).
# 
# l4proc (I, F, fnTelling, topic, MSGF, fnCommunication) :-
# 
#     frame (MSGF, com,  we),
#     frame (MSGF, top,  entity),    
#     frame (MSGF, time, recently),    
#     frame (MSGF, msg,  ENTITY),    
# 
#     ias (I, uttLang, LANG),
# 
#     entity_label(LANG, ENTITY, LABEL),
# 
#     answerz (I, LANG, weHaveBeenTalkingAbout, LABEL).
# 
# l4proc (I, F, fnTelling, topic, MSGF, fnFamiliarity) :-
# 
#     frame (MSGF, ent,  ENTITY),    
# 
#     ias (I, uttLang, LANG),
# 
#     entity_label(LANG, ENTITY, LABEL),
# 
#     answerz (I, LANG, weHaveBeenTalkingAbout, LABEL).
# 
# %
# % look for entity we have been talking about with the user
# %
# 
# l3proc (I, F, fnQuestioning) :-
# 
#     uriref (aiu:self, SELF),
#     frame (F, add, SELF),
#     frame (F, top, topic),
#     not (frame (F, msg, MSGF)),
# 
#     log (debug, "l3proc looking for fnQuestioning topic frame..."),
# 
#     context_search_l2(I, I, 8, 1, URFRAME, L1T, L1F, L1FE, L2FT, L2F),
# 
#     log (debug, "l3proc looking for fnQuestioning topic frame... found one."),
# 
#     assertz (ias(I, score, 10)),
# 
#     % remember our utterance interpretation
# 
#     assertz(ias(I, uframe, F)),
# 
#     % produce response frame graph (here: tell user about last topic entity)
#     
#     list_append(VMC, fe(msg,  L2F)),
#     list_append(VMC, fe(top,  topic)),
#     frame (F, spkr, USER),
#     list_append(VMC, fe(add,  USER)),
#     list_append(VMC, fe(spkr, uriref(aiu:self))),
#     list_append(VMC, frame(fnTelling)),
# 
#     fnvm_graph(VMC, RFRAME),
# 
#     % remember response frame
# 
#     assertz(ias(I, rframe, RFRAME)),
# 
#     % generate response actions
#     
#     % trace(on),
# 
#     l4proc (I).
# 
# l2proc_whatWasOurTopic :-
#     list_append(VMC, fe(top,  topic)),
#     list_append(VMC, fe(add,  uriref(aiu:self))),
#     ias(I, user, USER),
#     list_append(VMC, fe(spkr, USER)),
#     list_append(VMC, frame(fnQuestioning)),
#    
#     fnvm_exec (I, VMC).
# 
# 
# nlp_test(en,
#          ivr(in('what did we talk about'),
#              out("sorry i dont know"))
#              ).
# 
# nlp_gens(en, '@SELF_ADDRESS:LABEL (uh|) now for a different subject!', 'What would you like to talk about?').
# nlp_gens(de, '@SELF_ADDRESS:LABEL (ach|) (jetzt ein|mal ein|) anderes thema', 'Worüber möchtest Du sprechen?').


