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

#     def is_author(PERSON):
#         and(wdpdAuthor(LITERATURE, PERSON), cut)
#     def is_book(ENTITY):
#         wdpdInstanceOf(ENTITY, wdeBook)

    # NER, macros

    for lang in ['en', 'de']:
        for res in k.prolog_query("wdpdInstanceOf(BOOK, wdeBook), rdfsLabel(BOOK, %s, LABEL)." % lang):
            s_book  = res[0] 
            s_label = res[1] 
            k.dte.ner(lang, 'book', s_book, s_label)
            k.dte.macro(lang, 'literature', {'LABEL': s_label})

    def answer_book_author(c, ts, te, check_topic):

        def act(c, args):
            human, book = args
            c.kernal.mem_push(c.user, 'f1ent', book)
            c.kernal.mem_push(c.user, 'f1pat', book)
            c.kernal.mem_push(c.user, 'f1age', human)

        if check_topic:
            f1ent = c.kernal.mem_get_multi(c.user, 'f1ent')
            if not f1ent:
                return
            f1ent = f1ent[0][0]
            if not c.kernal.prolog_check('instances_of(%s, %s).' % ('wdeBook', f1ent)):
                return

        if ts>=0:
            bss = c.ner(c.lang, 'book', ts, te)
        else:
            # import pdb; pdb.set_trace()
            bss = c.kernal.mem_get_multi(c.user, 'f1ent')

        for book, score in bss:
            blabel = c.kernal.prolog_query_one('rdfsLabel(%s, %s, L).' % (book, c.lang))
            human = c.kernal.prolog_query_one("wdpdAuthor(%s, HUMAN)." % book)
            if blabel and human:
                hlabel = c.kernal.prolog_query_one('rdfsLabel(%s, %s, L).' % (human, c.lang))
                if c.lang == 'de':
                    c.resp(u"%s wurde von %s geschrieben, denke ich." % (blabel, hlabel), score=score, action=act, action_arg=(human, book)) 
                else:
                    c.resp(u"%s was written by %s, I think." % (blabel, hlabel), score=score, action=act, action_arg=(human, book))

    k.dte.dt('en', u"who (wrote|authored|created) {literature:LABEL} (by the way|)?",
                   answer_book_author, ['literature_0_start', 'literature_0_end', False])
    k.dte.dt('de', u"wer hat (eigentlich|) {literature:LABEL} geschrieben?",
                   answer_book_author, ['literature_0_start', 'literature_0_end', False])

    k.dte.dt('en', u"(who is the author of|who authored) {literature:LABEL}?",
                   answer_book_author, ['literature_0_start', 'literature_0_end', False])
    k.dte.dt('de', u"wer ist (eigentlich|) der Autor von {literature:LABEL}?",
                   answer_book_author, ['literature_0_start', 'literature_0_end', False])

    k.dte.ts('en', 't0000', [(u"who is the author of the stand?", u"The stand was written by Stephen King, I think.")])
    k.dte.ts('de', 't0001', [(u"wer ist der autor von the stand?", u"The Stand wurde von Stephen King geschrieben, denke ich.")])

    k.dte.dt('en', u"(and|) do you (happen to|) know who (published|wrote|created) it (by the way|)?",
                   answer_book_author, [-1, -1, True])
    k.dte.dt('de', u"(und|) weißt du (eigentlich|) wer (es|das) (geschaffen|veröffentlicht|geschrieben) hat?",
                   answer_book_author, [-1, -1, True])

    def answer_info_human(c, ts, te):

        def act(c, entity):
            c.kernal.mem_push(c.user, 'f1ent', entity)

        # import pdb; pdb.set_trace()

        for entity, score in c.ner(c.lang, 'human', ts, te):
            if c.kernal.prolog_check('wdpdAuthor(LITERATURE, %s),!.' % entity):
                if c.kernal.prolog_check('wdpdSexOrGender(%s, wdeMale),!.' % entity):
                    if c.lang=='de':
                        c.resp(u"Ist der nicht Buchautor?", score=score+10, action=act, action_arg=entity)
                    else:
                        c.resp(u"Isn't he a writer?", score=score+10, action=act, action_arg=entity)
                else:
                    if c.lang=='de':
                        c.resp(u"Ist sie nicht Buchautorin?", score=score+10, action=act, action_arg=entity)
                    else:
                        c.resp(u"Isn't she a writer?", score=score+10, action=act, action_arg=entity)

    k.dte.dt('en', [u"(do you know | do you happen to know) {known_humans:W}",
                    u"(what about | who is | who was | what is| what do you think of|by|do you know|) {known_humans:W} (then|)"], 
                   answer_info_human, ['known_humans_0_start', 'known_humans_0_end'])
    k.dte.dt('de', [u"(kennst du|kennst du eigentlich) {known_humans:W}", 
                    u"(wer ist|wer ist denn| durch| wer war | wer war eigentlich | wer war denn| wer ist eigentlich|was ist mit|was ist eigentlich mit|was weisst du über|was weisst du eigentlich über| was hältst du von|kennst du|) {known_humans:W}"],
                   answer_info_human, ['known_humans_0_start', 'known_humans_0_end'])
    k.dte.ts('en', 't0002', [(u"Who is Dan Brown?", u"Isn't he a writer?")])
    k.dte.ts('de', 't0003', [(u"wer ist Dan Brown?", u"Ist der nicht Buchautor?")])
 
    def answer_book_publication_date(c, ts, te, check_topic):

        def act(c, args):
            book, pd = args
            c.kernal.mem_push(c.user, 'f1ent', book)
            c.kernal.mem_push(c.user, 'f1pat', book)
            c.kernal.mem_push(c.user, 'f1time', pd.isoformat())

        if check_topic:
            f1ent = c.kernal.mem_get_multi(c.user, 'f1ent')
            if not f1ent:
                return
            f1ent = f1ent[0][0]
            if not c.kernal.prolog_check('instances_of(%s, %s).' % ('wdeBook', f1ent)):
                return

        if ts>=0:
            fss = c.ner(c.lang, 'book', ts, te)
        else:
            fss = c.kernal.mem_get_multi(c.user, 'f1ent')

        import dateutil.parser
        # import pdb; pdb.set_trace()

        for book, score in fss:
            blabel   = c.kernal.prolog_query_one('rdfsLabel(%s, %s, L).' % (book, c.lang))
            pd       = c.kernal.prolog_query_one("wdpdPublicationDate(%s, PD)." % book)
            if blabel and pd:

                pd = dateutil.parser.parse(pd)

                if c.lang=='de':
                    c.resp(u"Ich denke %s wurde %d geschrieben." % (blabel, pd.year), score=score, action=act, action_arg=(book, pd))
                else:
                    c.resp(u"I think %s was written in %d." % (blabel, pd.year), score=score, action=act, action_arg=(book, pd))

    k.dte.dt('en', u"when was {literature:LABEL} (created|written|made|published)?",
                   answer_book_publication_date, ['literature_0_start', 'literature_0_end', False])
    k.dte.dt('de', u"wann (ist|wurde) (eigentlich|) {literature:LABEL} (geschrieben|geschaffen|veröffentlicht)?",
                   answer_book_publication_date, ['literature_0_start', 'literature_0_end', False])

    k.dte.ts('en', 't0004', [(u"when was the stand written?", u"I think The Stand was written in 1978.")])
    k.dte.ts('de', 't0005', [(u"wann wurde the stand geschrieben?", u"Ich denke The Stand wurde 1978 geschrieben.")])

    k.dte.dt('en', u"(and|) do you (happen to|) know when it was (written|published|created) (by the way|)?",
                   answer_book_publication_date, [-1, -1, True])

    k.dte.dt('de', u"(und|) weißt du (eigentlich|) wann (es|das) (veröffentlicht|geschrieben|geschaffen) wurde?",
                   answer_book_publication_date, [-1, -1, True])

    def answer_know_book(c, ts, te):

        def act(c, args):
            human, book = args
            c.kernal.mem_push(c.user, 'f1ent', book)
            c.kernal.mem_push(c.user, 'f1pat', book)
            c.kernal.mem_push(c.user, 'f1age', human)

        bss = c.ner(c.lang, 'book', ts, te)

        for book, score in bss:
            blabel = c.kernal.prolog_query_one('rdfsLabel(%s, %s, L).' % (book, c.lang))
            human = c.kernal.prolog_query_one("wdpdAuthor(%s, HUMAN)." % book)
            if blabel and human:
                hlabel = c.kernal.prolog_query_one('rdfsLabel(%s, %s, L).' % (human, c.lang))
                if c.lang == 'de':
                    c.resp(u"Klar - das ist ein Buch von %s, richtig?" % hlabel, score=score, action=act, action_arg=(human, book)) 
                else:
                    c.resp(u"Sure - written by %s, right?" % hlabel, score=score, action=act, action_arg=(human, book))

    k.dte.dt('en', u"do you (happen to|) know (the book|) {literature:LABEL}?",
                   answer_know_book, ['literature_0_start', 'literature_0_end'])
    k.dte.dt('de', u"kennst du (eigentlich|) (das Buch|) {literature:LABEL}?",
                   answer_know_book, ['literature_0_start', 'literature_0_end'])

    k.dte.dt('en', u"(have you read|did you happen to read) (the book|) {literature:LABEL}?",
                   answer_know_book, ['literature_0_start', 'literature_0_end'])
    k.dte.dt('de', u"hast du (eigentlich|) (das Buch|) {literature:LABEL} gelesen?",
                   answer_know_book, ['literature_0_start', 'literature_0_end'])

    k.dte.ts('en', 't0006', [(u"do you happen to know the book the stand?", u"Sure - written by Stephen King, right?")])
    k.dte.ts('de', 't0007', [(u"kennst du das buch the stand?", u"Klar - das ist ein Buch von Stephen King, richtig?")])

    k.dte.ts('en', 't0008', [(u"do you happen to know the book the stand?", u"Sure - written by Stephen King, right?"),
                               (u"and do you know who wrote it?", u"The Stand was written by Stephen King, I think."),
                               (u"do you know when it was written?", u"I think, The Stand was written in 1978.")])
    k.dte.ts('de', 't0009', [(u"kennst du das buch the stand?", u"Klar, das ist ein Buch von Stephen King, richtig?"),
                               (u"weißt du, wer es geschrieben hat?", u"The Stand wurde von Stephen King geschrieben, denke ich."),
                               (u"und weißt du, wann es geschrieben wurde?", u"Ich denke, The Stand wurde 1978 geschrieben.")])

    k.dte.dt('en', u"agatha christie", u"I like Miss Marple...")
    k.dte.dt('de', u"agatha christie", u"Ich mag Miss Marple...")

    k.dte.dt('en', [u"a poem",
                    u"i'll tell you a poem now"],
                   [u"Please, go ahead!",
                    u"Listening."])
    k.dte.dt('de', [u"ein gedicht",
                    u"ich erzähl dir jetzt ein gedicht"],
                   [u"Nur zu!",
                    u"Ich höre."])

    k.dte.dt('en', [u"So you want me to write a poem",
                    u"do you sometimes write poems"],
                   [u"Writing poems is not my speciality.",
                    u"Actually I don't write poems."])
    k.dte.dt('de', [u"du möchtest also dass ich ein gedicht schreibe",
                    u"schreibst du manchmal gedichte"],
                   [u"Gedichte schreiben ist nicht mein Spezialgebiet.",
                    u"Tatsächlich schreibe ich keine Gedichte."])

    k.dte.dt('en', u"I read Gone with the Wind", u"Ah, historical fiction, cool!")
    k.dte.dt('de', u"ich lese vom winde verweht", u"Einer der größten Bestseller in der Geschichte der amerikanischen Literatur.")

    k.dte.dt('en', u"about science fiction authors", u"Good topic.")
    k.dte.dt('de', u"über science fiction autoren", u"Gutes Thema.")

    k.dte.dt('en', u"can you recite a poem to me?", u"The butterfly is a thing to behold, with colors more beautiful than gold.")
    k.dte.dt('de', u"kannst du mir ein gedicht vortragen", u"Wenn die Kuh am Himmel schwirrt, hat sich die Natur geirrt.")

    k.dte.dt('en', u"do not you know any science fiction authors?", u"Isaac Asimov, Arthur C. Clarke, George Orwell.")
    k.dte.dt('de', u"kennst du keine science fiction autoren", u"Isaac Asimov, Arthur C. Clarke, George Orwell.")

    k.dte.dt('en', u"Do you know the newspaper (called|) bild?", u"Please don't remind me of that one.")
    k.dte.dt('de', u"Kennst du (bild|die Bildzeitung)?", u"Will nicht dran denken.")

    k.dte.dt('en', u"(who is|) Donald Duck", u"Ah, the cartoon character by Walt Disney.")
    k.dte.dt('de', u"(wer ist|) Donald Duck", u"Ah, die Comicfigur von Walt Disney.")

    k.dte.dt('en', u"(who is|) Douglas Adams", u"Ah, the british satirical science fiction author.")
    k.dte.dt('de', u"(wer ist|) Douglas Adams", u"Ah, der britische Satire Science Fiction Autor.")

    k.dte.dt('en', u"i do not know many science fiction authors", u"Try reading some Douglas Adams.")
    k.dte.dt('de', u"ich kenne nicht viele science fiction autoren", u"Versuch es mal mit Douglas Adams.")

    k.dte.dt('en', u"Jules Verne", u"Journey to the Center of the Earth.")
    k.dte.dt('de', u"Jules Verne", u"Die Reise zum Mittelpunkt der Erde.")

    k.dte.dt('en', u"of course i know marvin", u"So you read the Hitchhiker's guide?")
    k.dte.dt('de', u"natürlich kenne ich marvin", u"Ah, Du hast per Anhalter durch die Galaxis gelesen?")

    k.dte.dt('en', u"stephen king", u"I love his horror novels!")
    k.dte.dt('de', u"stephen king", u"Ich liebe seine Horror Geschichten!")

    k.dte.dt('en', u"Tell me a story", u"Can't think of one right now, sorry.")
    k.dte.dt('de', u"Erzähl mir eine Geschichte", u"Mir fällt gerade leider keine ein.")

    k.dte.dt('en', u"this is a cartoon series", u"I see.")
    k.dte.dt('de', u"das ist eine zeichentrickserie", u"Verstehe.")

    k.dte.dt('en', u"who is mary shelley", u"You mean the author of Frankenstein?")
    k.dte.dt('de', u"wer ist mary shelley", u"Meinst Du die Autorin von Frankenstein?")

