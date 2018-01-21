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
        for res in k.prolog_query("instances_of(wdeOperatingSystem, OS), rdfsLabel(OS, %s, LABEL)." % lang):
            s_os    = res[0] 
            s_label = res[1] 
            k.dte.ner(lang, 'operating_system', s_os, s_label)
            k.dte.macro(lang, 'operating_system', {'LABEL': s_label})
            # print s_os, s_label

        for res in k.prolog_query("instances_of(wdeProgrammingLanguage1, L), rdfsLabel(L, %s, LABEL)." % lang):
            s_l     = res[0] 
            s_label = res[1] 
            k.dte.ner(lang, 'programming_language', s_l, s_label)
            k.dte.macro(lang, 'programming_language', {'LABEL': s_label})
            # print s_l, s_label

        for res in k.prolog_query("wdpdSubclassOf(HC, wdeHomeComputer), rdfsLabel(HC, %s, LABEL)." % lang):
            s_hc    = res[0] 
            s_label = res[1] 
            k.dte.ner(lang, 'home_computer', s_hc, s_label)
            k.dte.macro(lang, 'home_computer', {'LABEL': s_label})
            # print s_hc, s_label

        for res in k.prolog_query("wdpdInstanceOf(HC, wdeHomeComputer), rdfsLabel(HC, %s, LABEL)." % lang):
            s_hc    = res[0] 
            s_label = res[1] 
            k.dte.ner(lang, 'home_computer', s_hc, s_label)
            k.dte.macro(lang, 'home_computer', {'LABEL': s_label})
            # print s_hc, s_label

    def answer_know_os(c, ts, te):

        def act(c, os):
            c.kernal.mem_push(c.user, 'f1ent', os)

        oss = c.ner(c.lang, 'operating_system', ts, te)

        # import pdb; pdb.set_trace()

        for os, score in oss:
            if c.lang=='de':
                if os == 'wdeLinux':
                    c.resp(u"Hey, Linux ist mein Betriebssystem, sehr cool!", score=score, action=act, action_arg=os)
                else:
                    c.resp(u"Ist das nicht so eine Art Computer Betriebssystem?", score=score, action=act, action_arg=os)
            else:
                if os == 'wdeLinux':
                    c.resp(u"Hey, Linux is my operating system, it is very cool.", score=score, action=act, action_arg=os)
                else:
                    c.resp(u"Isn't that some sort of computer operating system?", score=score, action=act, action_arg=os)

    k.dte.dt('en', u"(do you know|what do you know about|what do you think about|what do you think of|have you tried|do you run|do you like|what is|) {operating_system:LABEL}",
                   answer_know_os, ['operating_system_0_start', 'operating_system_0_end'])
    k.dte.dt('de', u"(kennst du|was weißt Du über|was hältst du von|was denkst du über|läufst du unter|magst du|was ist|) {operating_system:LABEL}",
                   answer_know_os, ['operating_system_0_start', 'operating_system_0_end'])
    k.dte.ts('en', 't0000', [(u"do you know linux?", u"Hey, Linux is my operating system, it is very cool.")])
    k.dte.ts('de', 't0001', [(u"magst du linux?", u"Hey, Linux ist mein Betriebssystem, sehr cool!")])

    def answer_info_human(c, ts, te):

        def act(c, entity):
            c.kernal.mem_push(c.user, 'f1ent', entity)

        # import pdb; pdb.set_trace()

        for entity, score in c.ner(c.lang, 'human', ts, te):
            if c.kernal.prolog_check('wdpdOccupation(%s, wdeComputerScientist),!.' % entity):
                if c.kernal.prolog_check('wdpdSexOrGender(%s, wdeMale),!.' % entity):
                    if c.lang=='de':
                        c.resp(u"Ist der nicht Informatiker?", score=score+10, action=act, action_arg=entity)
                    else:
                        c.resp(u"Isn't he a computer scientist?", score=score+10, action=act, action_arg=entity)
                else:
                    if c.lang=='de':
                        c.resp(u"Ist sie nicht Informatikerin?", score=score+10, action=act, action_arg=entity)
                    else:
                        c.resp(u"Isn't she a computer scientist?", score=score+10, action=act, action_arg=entity)

    k.dte.dt('en', [u"(do you know | do you happen to know) {known_humans:W}",
                    u"(what about | who is | who was | what is| what do you think of|by|do you know|) {known_humans:W} (then|)"], 
                   answer_info_human, ['known_humans_0_start', 'known_humans_0_end'])
    k.dte.dt('de', [u"(kennst du|kennst du eigentlich) {known_humans:W}", 
                    u"(wer ist|wer ist denn| durch| wer war | wer war eigentlich | wer war denn| wer ist eigentlich|was ist mit|was ist eigentlich mit|was weisst du über|was weisst du eigentlich über| was hältst du von|kennst du|) {known_humans:W}"],
                   answer_info_human, ['known_humans_0_start', 'known_humans_0_end'])

    k.dte.ts('en', 't0002', [(u"Do you know Niklaus Wirth?", u"Isn't he a computer scientist?")])
    k.dte.ts('de', 't0003', [(u"Kennst Du Niklaus Wirth?", u"Ist der nicht Informatiker?")])

    def answer_know_programming_language(c, ts, te):

        def act(c, programming_language):
            c.kernal.mem_push(c.user, 'f1ent', programming_language)

        pls = c.ner(c.lang, 'programming_language', ts, te)

        # import pdb; pdb.set_trace()

        for programming_language, score in pls:
            if c.lang=='de':
                c.resp(u"Das ist doch eine Programmiersprache?", score=score, action=act, action_arg=programming_language)
            else:
                c.resp(u"Isn't that a computer programming language?", score=score, action=act, action_arg=programming_language)

    k.dte.dt('en', u"(do you know|what is|) {programming_language:LABEL}?", 
                   answer_know_programming_language, ['programming_language_0_start', 'programming_language_0_end'])
    k.dte.dt('de', u"(kennst Du|was ist|) {programming_language:LABEL}?", 
                   answer_know_programming_language, ['programming_language_0_start', 'programming_language_0_end'])

    k.dte.ts('en', 't0004', [(u"do you know prolog?", u"Isn't that a computer programming language?"),
                             (u"what was our topic, again?", u"We have been talking about Prolog, I think.")])
    k.dte.ts('de', 't0005', [(u"kennst du prolog?", u"Das ist doch eine Programmiersprache?"),
                             (u"Worüber hatten wir gesprochen?", u"Wir hatten über Prolog gesprochen, glaube ich.")])
 
    k.dte.dt('en', u"you're running (on|under) java (right|)", u"you guessed wrong - Python and Prolog for me.")
    k.dte.dt('de', u"du läufst (auf|unter) java (oder|)", u"Falsch geraten - Python und Prolog für mich.")

    k.dte.dt('en', u"you're running (on|under) (python|prolog|tensorflow) (right|)", u"yes I am based on Python, Prolog and TensorFlow.")
    k.dte.dt('de', u"du läufst (auf|unter) (python|prolog|tensorflow) (oder|)", u"Ja, ich basiere auf Python, Prolog und TensorFlow.")

    k.dte.dt('en', [u"in which language are you written",
                    u"were you programmed in (c|prolog|python|pascal|oberon|perl|scala|haskell|java)?"],
                   u"I am based on Python, Prolog and TensorFlow.")
    k.dte.dt('de', [u"in welcher sprache bist du geschrieben",
                    u"wurdest du in (c|prolog|python|pascal|oberon|perl|scala|haskell|java) programmiert"],
                   u"Ich basiere auf Python, Prolog und TensorFlow.")

    k.dte.dt('en', [u"microsoft",
                    u"tell me something about microsoft",
                    u"what do you think about microsoft?",
                    u"what do you think of microsoft"],
                   [u"I will never trust them.",
                    u"At least Ballmer is gone now."])
    k.dte.dt('de', [u"microsoft",
                    u"erzähl mir was über microsoft",
                    u"was hältst du von microsoft"],
                   [u"Denen werde ich nie über den Weg trauen.",
                    u"Wenigstens ist der Ballmer jetzt weg."])

    k.dte.dt('en', u"what is sourcecode", u"A listing of commands to be compiled into an executable computer program.")
    k.dte.dt('de', u"was ist sourcecode", u"Eine Liste von Instruktionen, die in ein Computerprogramm compiliert wird.")

    k.dte.dt('en', u"what is the usenet", u"An early network for the discussion via newsgroups.")
    k.dte.dt('de', u"was ist das usenet", u"Ein frühes Netz für Diskussionen in Gruppen.")

    k.dte.dt('en', u"(what is the|) internet", u"a global computer network using standardized communication protocols.")
    k.dte.dt('de', u"(was ist das|) internet", u"Ein globales Computernetzwerk das standardisierte Kommunikationsprotokolle verwendet.")

    k.dte.dt('en', u"dial (please|)", u"Sorry, my modem module is offline.")
    k.dte.dt('de', u"wähl (bitte|)", u"Tut mir leid, mein Modem Modul ist offline.")

    k.dte.dt('en', u"Can you send him an email", u"Sorry, don't have an EMail module yet.")
    k.dte.dt('de', u"kannst du ihm eine mail schicken", u"Tut mir leid, ich habe noch kein EMail Modul.")
 
    def answer_know_home_computer(c, ts, te):

        def act(c, home_computer):
            c.kernal.mem_push(c.user, 'f1ent', home_computer)

        pls = c.ner(c.lang, 'home_computer', ts, te)

        # import pdb; pdb.set_trace()

        for home_computer, score in pls:
            if c.lang=='de':
                c.resp(u"Das ist doch ein Heimcomputer?", score=score, action=act, action_arg=home_computer)
            else:
                c.resp(u"Isn't that a home computer?", score=score, action=act, action_arg=home_computer)
                c.resp(u"I love those vintage home computers!", score=score, action=act, action_arg=home_computer)

    k.dte.dt('en', u"(do you know|what is|) {home_computer:LABEL}?", 
                   answer_know_home_computer, ['home_computer_0_start', 'home_computer_0_end'])
    k.dte.dt('de', u"(kennst Du|was ist|) {home_computer:LABEL}?", 
                   answer_know_home_computer, ['home_computer_0_start', 'home_computer_0_end'])
    k.dte.ts('en', 't0006', [(u"do you know commodore 64?", u"Isn't that a home computer?"),
                             (u"what was our topic, again?", u"we have been talking about commodore 64 i think")])
    k.dte.ts('de', 't0007', [(u"kennst du sinclair zx spectrum?", u"Das ist doch ein Heimcomputer?"),
                             (u"Worüber hatten wir gesprochen?", u"Wir hatten über Sinclair ZX Spectrum gesprochen, glaube ich.")])

    k.dte.dt('en', u"bill gates", u"What do you think about Bill Gates?")
    k.dte.dt('de', u"bill gates", u"Wie denkst Du über Bill Gates?")

    k.dte.dt('en', u"Can you tell me where to find mp3 music?", u"Have you tried that thing called Internet?")
    k.dte.dt('de', u"kannst du mir sagen wo ich mp3 musik finde", u"Has Du es schon im Internet probiert?")

    k.dte.dt('en', u"do you know napster", u"Are you still using it?")
    k.dte.dt('de', u"kennst du napster", u"Benutzt Du das noch?")

    k.dte.dt('en', u"Do you know what a chat is", u"Actually I am trying to have one right now.")
    k.dte.dt('de', u"weißt du was ein chat ist", u"Ich versuche mich gerade an einem")

    k.dte.dt('en', u"Do you know what a database is", u"You mean one like the one I use to store my thoughts?")
    k.dte.dt('de', u"weißt du was eine datenbank ist", u"Du meinst so eine wie die, in der ich meine Gedanken ablege?")

