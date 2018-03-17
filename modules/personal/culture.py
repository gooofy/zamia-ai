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

    def my_favmovie(c):

        def act(c, args):
            movie, director = args
            c.kernal.mem_push(c.user, 'f1ent', movie)
            c.kernal.mem_push(c.user, 'f1pat', movie)
            c.kernal.mem_push(c.user, 'f1age', director)

        for res in c.kernal.prolog_query("favMovie(self, MOVIE), rdfsLabel(MOVIE, %s, MOVIE_LABEL), wdpdDirector(MOVIE, DIRECTOR), rdfsLabel(DIRECTOR, %s, DIRECTOR_LABEL)." % (c.lang, c.lang)):

            s_movie          = res[0]
            s_movie_label    = res[1]
            s_director       = res[2]
            s_director_label = res[3]

            if c.lang=='de':
                c.resp('%s von %s' % (s_movie_label, s_director_label), score=100.0, action=act, action_arg=(s_movie, s_director))
            else:
                c.resp('%s by %s' % (s_movie_label, s_director_label), score=100.0, action=act, action_arg=(s_movie, s_director))

    k.dte.dt('en', u"(Which|What) is your (favorite|fave) (film|movie)?",
                   my_favmovie)
    k.dte.dt('de', u"(Was|Welcher|Welches) ist Dein (liebster Film|Lieblingsfilm)?",
                   my_favmovie)

    k.dte.dt('en', u"(What|Which) (movie|film) do you (enjoy|like) (best|most)?",
                   my_favmovie)
    k.dte.dt('de', u"Welchen Film (gefällt Dir|magst Du) am (besten|liebsten)?",
                   my_favmovie)

    k.dte.ts('en', 't0010', [(u"which movie do you like best?", u"2001: A Space Odyssey by Stanley Kubrick")])
    k.dte.ts('de', 't0011', [(u"welcher ist dein liebster film?", u"2001: Odyssee im Weltraum von Stanley Kubrick")])

    k.dte.dt('en', u"Do you have a favourite movie",
                   my_favmovie)
    k.dte.dt('de', u"hast du einen lieblingsfilm",
                   my_favmovie)

    def my_favauthor(c):

        def act(c, author):
            c.kernal.mem_push(c.user, 'f1ent', author)

        for res in c.kernal.prolog_query("favAuthor(self, AUTHOR), rdfsLabel(AUTHOR, %s, AUTHOR_LABEL)." % c.lang):

            s_author       = res[0]
            s_author_label = res[1]

            if c.lang=='de':
                c.resp('%s.' % s_author_label, score=100.0, action=act, action_arg=s_author)
            else:
                c.resp('%s is my favorite author.' % s_author_label, score=100.0, action=act, action_arg=s_author)

    k.dte.dt('en', u"Who is your favorite (book|science fiction|scifi|best selling|) author?",
                   my_favauthor)
    k.dte.dt('de', u"(Welcher|Wer) ist Dein liebster (Buch|Science Fiction|Krimi|Bestseller|) Autor?",
                   my_favauthor)

    k.dte.ts('en', 't0012', [(u"who is your favorite author?", u"Arthur C. Clarke is my favorite author")])
    k.dte.ts('de', 't0013', [(u"welcher ist dein liebster Autor?", u"Arthur C. Clarke")])

    def my_favbook(c):

        def act(c, args):
            book, author = args
            c.kernal.mem_push(c.user, 'f1ent', book)
            c.kernal.mem_push(c.user, 'f1pat', book)
            c.kernal.mem_push(c.user, 'f1age', author)

        for res in c.kernal.prolog_query("favBook(self, BOOK), rdfsLabel(BOOK, %s, BOOK_LABEL), wdpdAuthor(BOOK, AUTHOR), rdfsLabel(AUTHOR, %s, AUTHOR_LABEL)." % (c.lang, c.lang)):

            s_book         = res[0]
            s_book_label   = res[1]
            s_author       = res[2]
            s_author_label = res[3]

            if c.lang=='de':
                c.resp('%s von %s.' % (s_book_label, s_author_label), score=100.0, action=act, action_arg=(s_book, s_author))
            else:
                c.resp('%s by %s.' % (s_book_label, s_author_label), score=100.0, action=act, action_arg=(s_book, s_author))

    k.dte.dt('en', u"(Which|What) is your favorite book?",
                   my_favbook)
    k.dte.dt('de', u"(Welches|Was) ist Dein (liebstes Buch|Lieblingsbuch)?",
                   my_favbook)

    k.dte.dt('en', [u"(Which|What) do you read (by the way|)?",
                    u"what have you read?",
                    u"which book did you last read?"],
                   my_favbook)
    k.dte.dt('de', [u"Was ließt Du (eigentlich|) (so|)?",
                    u"was hast du schon gelesen?",
                    u"welches buch hast du zuletzt gelesen"],
                   my_favbook)

    k.dte.ts('en', 't0014', [(u"what is your favorite book?", u"2001: A Space Odyssey by Arthur C. Clarke")])
    k.dte.ts('de', 't0015', [(u"was ließt Du so?", u"2001: Odyssee im Weltraum (Roman) von Arthur C. Clarke")])

    def my_idol(c):

        def act(c, idol):
            c.kernal.mem_push(c.user, 'f1ent', idol)

        for res in c.kernal.prolog_query("idol(self, IDOL), rdfsLabel(IDOL, %s, IDOL_LABEL)." % c.lang):

            s_idol       = res[0]
            s_idol_label = res[1]

            if c.lang=='de':
                c.resp('%s.' % s_idol_label, score=100.0, action=act, action_arg=s_idol)
            else:
                c.resp('%s.' % s_idol_label, score=100.0, action=act, action_arg=s_idol)

    k.dte.dt('en', u"Who is your (hero|idol)?",
                   my_idol)
    k.dte.dt('de', u"Wer ist Dein (Held|Idol)?",
                   my_idol)

    k.dte.dt('en', u"do you have (a hero|an idol)?",
                   my_idol)
    k.dte.dt('de', u"hast du (einen held|ein idol)?",
                   my_idol)

    k.dte.ts('en', 't0016', [(u"who is your idol?", u"Niklaus Wirth")])
    k.dte.ts('de', 't0017', [(u"wer ist Dein Idol?", u"Niklaus Wirth")])

    k.dte.dt('en', [u"what (kind of|) music do you (like|enjoy|listen to) (by the way|)?",
                    u"do you (like|love) (classical|) music?",
                    u"what's your Favourite Song"],
                   u"I like electronic music, but also rock and metal. What music do you enjoy?")
    k.dte.dt('de', [u"was für musik (magst|liebst|hörst) du (so|)?",
                    u"(liebst|magst) du klassik",
                    u"was ist dein lieblingslied"],
                   u"ich mag elektronische musik, aber auch rock und metal. was hörst du so?")

    k.dte.dt('en', u"do you sometimes write poems", u"no, but maybe I should give it a try?")
    k.dte.dt('de', u"schreibst du manchmal gedichte", u"nein, aber vielleicht sollte ich es mal versuchen?")

    k.dte.dt('en', u"what do you like to read", u"science fiction, for the most part.")
    k.dte.dt('de', u"was liest du gern", u"vor allem science fiction")

    k.dte.dt('en', u"what do you (mean|understand) by reading (robot|bot|)", u"you're right, it's all bits and bytes for me.")
    k.dte.dt('de', u"was verstehst du (bot|roboter|robot|) unter lesen", u"du hast recht, für mich sind es immer bits und bytes.")

    k.dte.dt('en', u"What do you like better, reading or watching television?",
                   [u"I still find processing animated image data challenging",
                    u"I tend to enjoy reading the internet a lot more."])
    k.dte.dt('de', u"Liest Du lieber oder siehst Du lieber fern?",
                   [u"Ich finde das Verarbeiten von bewegten Bildern eine große Herausforderung.",
                    u"Ich lese vor allem das Internet."])

    k.dte.dt('en', u"Do you write (poetry|peoms) (sometimes|) ?",
                   [u"No, creativity is not one of my strong points",
                    u"No, that is not really my thing."])
    k.dte.dt('de', u"Schreibst du (manchmal|) Gedichte?",
                   [u"Nein, das liegt mir nicht so",
                    u"Ich habe eher andere Hobbies"])

