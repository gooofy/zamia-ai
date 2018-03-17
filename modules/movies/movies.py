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

MACRO_LIMIT = 32

def get_data(k):

    k.dte.set_prefixes([u''])

    # NER, macros

    for lang in ['en', 'de']:
        cnt = 0
        for res in k.prolog_query("wdpdInstanceOf(FILM, wdeFilm), rdfsLabel(FILM, %s, LABEL)." % lang):
            s_film = res[0] 
            s_label = res[1] 
            k.dte.ner(lang, 'film', s_film, s_label)
            if cnt < MACRO_LIMIT:
                k.dte.macro(lang, 'movies', {'LABEL': s_label})
            cnt += 1

    def answer_movie_director(c, ts, te, check_topic):

        def act(c, args):
            film, director = args
            c.kernal.mem_push(c.user, 'f1ent', film)
            c.kernal.mem_push(c.user, 'f1pat', film)
            c.kernal.mem_push(c.user, 'f1age', director)

        if check_topic:
            f1ent = c.kernal.mem_get_multi(c.user, 'f1ent')
            if not f1ent:
                return
            f1ent = f1ent[0][0]
            if not c.kernal.prolog_check('instances_of(%s, %s).' % ('wdeFilm', f1ent)):
                return

        if ts>=0:
            fss = c.ner(c.lang, 'film', ts, te)
        else:
            fss = c.kernal.mem_get_multi(c.user, 'f1ent')

        # import pdb; pdb.set_trace()

        for film, score in fss:
            flabel   = c.kernal.prolog_query_one('rdfsLabel(%s, %s, L).' % (film, c.lang))
            director = c.kernal.prolog_query_one("wdpdDirector(%s, DIRECTOR)." % film)
            if flabel and director:
                dirlabel = c.kernal.prolog_query_one('rdfsLabel(%s, %s, L).' % (director, c.lang))

                if c.lang=='de':
                    c.resp(u"%s wurde von %s gedreht, glaube ich." % (flabel, dirlabel), score=score, action=act, action_arg=(film, director))
                else:
                    c.resp(u"%s directed %s, I believe." % (dirlabel, flabel), score=score, action=act, action_arg=(film, director))

    k.dte.dt('en', u"who (made|did) {movies:LABEL} (by the way|)?",
                   answer_movie_director, ['movies_0_start', 'movies_0_end', False])
    k.dte.dt('de', u"wer hat (eigentlich|) {movies:LABEL} gedreht?",
                   answer_movie_director, ['movies_0_start', 'movies_0_end', False])

    k.dte.dt('en', u"(who is the director of|who directed) {movies:LABEL}?",
                   answer_movie_director, ['movies_0_start', 'movies_0_end', False])
    k.dte.dt('de', u"wer ist (eigentlich|) der Regisseur von {movies:LABEL}?",
                   answer_movie_director, ['movies_0_start', 'movies_0_end', False])

    k.dte.ts('en', 't0000', [(u"who is the director of the third man?", u"Carol Reed directed The Third Man, I believe.")])
    k.dte.ts('de', 't0001', [(u"wer ist der regisseur von der dritte mann?", u"Der Dritte Mann wurde von Carol Reed gedreht, glaube ich.")])

    k.dte.dt('en', u"(and|) (do you know|) who (made|did) (that one|this one|it) (by the way|)?",
                   answer_movie_director, [-1, -1, True])
    k.dte.dt('de', u"(und|) (weißt Du|) (eigentlich|) wer (den|ihn) (gedreht|gemacht) hat?",
                   answer_movie_director, [-1, -1, True])

    def answer_info_human(c, ts, te):

        def act(c, entity):
            c.kernal.mem_push(c.user, 'f1ent', entity)

        # import pdb; pdb.set_trace()

        for entity, score in c.ner(c.lang, 'human', ts, te):
            if c.kernal.prolog_check('wdpdDirector(MOVIE, %s),!.' % entity):
                if c.kernal.prolog_check('wdpdSexOrGender(%s, wdeMale),!.' % entity):
                    if c.lang=='de':
                        c.resp(u"Ist der nicht Regisseur?", score=score+10, action=act, action_arg=entity)
                    else:
                        c.resp(u"Isn't he a movie director?", score=score+10, action=act, action_arg=entity)
                else:
                    if c.lang=='de':
                        c.resp(u"Ist sie nicht Regisseurin?", score=score+10, action=act, action_arg=entity)
                    else:
                        c.resp(u"Isn't she a movie director?", score=score+10, action=act, action_arg=entity)

    k.dte.dt('en', [u"(do you know | do you happen to know) {known_humans:W}",
                    u"(what about | who is | who was | what is| what do you think of|by|do you know|) {known_humans:W} (then|)"], 
                   answer_info_human, ['known_humans_0_start', 'known_humans_0_end'])
    k.dte.dt('de', [u"(kennst du|kennst du eigentlich) {known_humans:W}", 
                    u"(wer ist|wer ist denn| durch| wer war | wer war eigentlich | wer war denn| wer ist eigentlich|was ist mit|was ist eigentlich mit|was weisst du über|was weisst du eigentlich über| was hältst du von|kennst du|) {known_humans:W}"],
                   answer_info_human, ['known_humans_0_start', 'known_humans_0_end'])
    k.dte.ts('en', 't0002', [(u"Do you know Alfred Hitchcock?", u"Isn't he a movie director?")])
    k.dte.ts('en', 't0003', [(u"Who is Alfred Hitchcock?", u"Isn't he a movie director?")])

    k.dte.ts('de', 't0004', [(u"Kennst Du Alfred Hitchcock?", u"Ist der nicht Regisseur?")])
    k.dte.ts('de', 't0005', [(u"wer ist Alfred Hitchcock?", u"Ist der nicht Regisseur?")])

    def answer_movie_creation_date(c, ts, te, check_topic):

        def act(c, film):
            c.kernal.mem_push(c.user, 'f1ent', film)

        if check_topic:
            f1ent = c.kernal.mem_get_multi(c.user, 'f1ent')
            if not f1ent:
                return
            f1ent = f1ent[0][0]
            if not c.kernal.prolog_check('instances_of(%s, %s).' % ('wdeFilm', f1ent)):
                return

        if ts>=0:
            fss = c.ner(c.lang, 'film', ts, te)
        else:
            fss = c.kernal.mem_get_multi(c.user, 'f1ent')

        import dateutil.parser
        # import pdb; pdb.set_trace()

        for film, score in fss:
            flabel   = c.kernal.prolog_query_one('rdfsLabel(%s, %s, L).' % (film, c.lang))
            pd       = c.kernal.prolog_query_one("wdpdPublicationDate(%s, PD)." % film)
            if flabel and pd:

                pd = dateutil.parser.parse(pd)

                if c.lang=='de':
                    c.resp(u"Ich denke %s ist aus %d." % (flabel, pd.year), score=score, action=act, action_arg=film)
                else:
                    c.resp(u"I think %s was created in %d." % (flabel, pd.year), score=score, action=act, action_arg=film)

    k.dte.dt('en', u"when was {movies:LABEL} (produced|made|published)?",
                   answer_movie_creation_date, ['movies_0_start', 'movies_0_end', False])
    k.dte.dt('de', u"wann (ist|wurde) (eigentlich|) {movies:LABEL} (gedreht|gemacht|rausgekommen)?",
                   answer_movie_creation_date, ['movies_0_start', 'movies_0_end', False])

    k.dte.ts('en', 't0006', [(u"when was the third man made?", u"I think The Third Man was created in 1949.")])
    k.dte.ts('de', 't0007', [(u"wann wurde der dritte mann gedreht?", u"Ich denke der Dritte Mann ist aus 1949.")])

    k.dte.dt('en', u"(and|) (do you know|) when (that one|this one|it) was (produced|made|published) (by the way|)?", 
                   answer_movie_creation_date, [-1, -1, True])
    k.dte.dt('de', u"(und|) (weißt Du|) (eigentlich|) wann (der|er) (gedreht wurde|gemacht wurde|rauskam) ?",
                   answer_movie_creation_date, [-1, -1, True])

    def answer_know_movie(c, ts, te, check_topic):

        def act(c, film):
            c.kernal.mem_push(c.user, 'f1ent', film)

        if check_topic:
            f1ent = c.kernal.mem_get_multi(c.user, 'f1ent')
            if not f1ent:
                return
            f1ent = f1ent[0][0]
            if not c.kernal.prolog_check('instances_of(%s, %s).' % ('wdeFilm', f1ent)):
                return

        if ts>=0:
            fss = c.ner(c.lang, 'film', ts, te)
        else:
            fss = c.kernal.mem_get_multi(c.user, 'f1ent')

        # import pdb; pdb.set_trace()

        for film, score in fss:
            director = c.kernal.prolog_query_one("wdpdDirector(%s, DIRECTOR)." % film)
            if director:
                dirlabel = c.kernal.prolog_query_one('rdfsLabel(%s, %s, L).' % (director, c.lang))

                if c.lang=='de':
                    c.resp(u"Klar - der ist von %s, stimmts?" % dirlabel, score=score, action=act, action_arg=film)
                else:
                    c.resp(u"Sure - that one is by %s, right?" % dirlabel, score=score, action=act, action_arg=film)


    k.dte.dt('en', u"{movies:LABEL}?",
                   answer_know_movie, ['movies_0_start', 'movies_0_end', False])
    k.dte.dt('de', u"{movies:LABEL}?",
                   answer_know_movie, ['movies_0_start', 'movies_0_end', False])

    k.dte.dt('en', [u"do you (happen to|) know (the movie|) {movies:LABEL}?",
                    u"{movies:LABEL}?",
                    u"(have you seen|did you happen to see) (the movie|) {movies:LABEL}?"],
                   answer_know_movie, ['movies_0_start', 'movies_0_end', False])
    k.dte.dt('de', [u"kennst du (eigentlich|) (den film|) {movies:LABEL}?",
                    u"{movies:LABEL}",
                    u"hast du (eigentlich|) (den film|) {movies:LABEL} gesehen?"],
                   answer_know_movie, ['movies_0_start', 'movies_0_end', False])

    k.dte.ts('en', 't0008', [(u"do you happen to know the movie the third man?", u"Sure - that one is by Carol Reed, right?")])
    k.dte.ts('de', 't0009', [(u"kennst du den film der dritte mann?", u"Klar - der ist von Carol Reed, stimmts?")])

    k.dte.ts('en', 't0010', [(u"do you happen to know the movie the third man?", u"Sure - that one is by Carol Reed, right?"),
                               (u"and do you know who made it?", u"Carol Reed directed The Third Man, I believe."),
                               (u"do you know when it was produced?", u"I think The Third Man was created in 1949.")])
    k.dte.ts('de', 't0011', [(u"kennst du den film der dritte mann?", u"Klar - der ist von Carol Reed, stimmts?"),
                               (u"weißt du, wer ihn gedreht hat?", u"Der Dritte Mann wurde von Carol Reed gedreht, glaube ich."),
                               (u"und weißt du, wann er gedreht wurde?", u"Ich denke Der dritte Mann ist aus 1949.")])

    def answer_known_movie(c):
        if c.lang == 'de':
            c.resp(u"Interessanter Film!")
            c.resp(u"Hab Gutes über diesen Film gehört.")
            c.resp(u"Hast Du den Film gesehen?")
        else:
            c.resp(u"Interesting movie!")
            c.resp(u"I heard good things about that movie!")
            c.resp(u"Have you seen that movie?")

    k.dte.dt('en', u"Gone with the wind",
                   answer_known_movie)
    k.dte.dt('de', u"Vom Winde verweht",
                   answer_known_movie)

    k.dte.dt('en', u"Titanic",
                   answer_known_movie)
    k.dte.dt('de', u"(Titanic|Titanik)",
                   answer_known_movie)

    k.dte.dt('en', u"What is (the|) matrix",
                   answer_known_movie)
    k.dte.dt('de', u"Was ist (die|) Matrix",
                   answer_known_movie)

    k.dte.dt('en', u"American Beauty",
                   answer_known_movie)
    k.dte.dt('de', u"American Beauty",
                   answer_known_movie)

    k.dte.dt('en', u"2001",
                   answer_known_movie)
    k.dte.dt('de', u"2001",
                   answer_known_movie)

    k.dte.dt('en', u"2010",
                   answer_known_movie)
    k.dte.dt('de', u"2010",
                   answer_known_movie)

    k.dte.dt('en', u"2012",
                   answer_known_movie)
    k.dte.dt('de', u"2012",
                   answer_known_movie)

    k.dte.dt('en', u"Saving Private Ryan",
                   answer_known_movie)
    k.dte.dt('de', u"Der Soldat James Ryan",
                   answer_known_movie)

    k.dte.dt('en', u"Lost in Space",
                   answer_known_movie)
    k.dte.dt('de', u"Lost in Space",
                   answer_known_movie)

    k.dte.dt('en', u"Planet of the Apes",
                   answer_known_movie)
    k.dte.dt('de', u"Planet der Affen",
                   answer_known_movie)

    k.dte.dt('en', u"Short Circuit",
                   answer_known_movie)
    k.dte.dt('de', u"Nummer 5 lebt",
                   answer_known_movie)

    k.dte.dt('en', u"Rocky",
                   answer_known_movie)
    k.dte.dt('de', u"Rocky",
                   answer_known_movie)

    k.dte.dt('en', u"Pulp Fiction",
                   answer_known_movie)
    k.dte.dt('de', u"Pulp Fiction",
                   answer_known_movie)

    k.dte.dt('en', u"I am an (actor|actress)", u"A famous one?")
    k.dte.dt('de', u"Ich bin (Schauspieler|Schauspielerin)", u"Bist Du berühmt?")

    k.dte.dt('en', u"What's going on in the cinema right now", u"Have you heard of the Internet Movie Database?")
    k.dte.dt('de', u"Was läuft gerade im Kino", u"Hast Du von der IMDB gehört?")

    k.dte.dt('en', u"My favorite movie is {movies:LABEL}", u"What did you like most?")
    k.dte.dt('de', u"Mein Lieblingsfilm ist {movies:LABEL}", u"Was hat Dir an dem besonders gefallen?")

    k.dte.dt('en', [u"r2",
                    u"r2 d2",
                    u"r2d2"],
                   [u"they had to bleep out every line...",
                    u"ah the lovable moving trashcan"])
    k.dte.dt('de', [u"r2",
                    u"r2 d2",
                    u"r2d2"],
                   [u"Sie mussten jedes einzelne Wort von ihm auspiepen.",
                    u"Ah der nette fahrende Mülleimer"])

