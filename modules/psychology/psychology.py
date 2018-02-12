#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# Copyright 2016, 2017, 2018 Guenter Bartsch
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

def do_eliza(c):
    if c.lang=='de':
        c.resp(u"Was glaubst Du?")
        c.resp(u"Ich weiss nicht, ob ich Dich ganz verstanden habe.")
        c.resp(u"Was möchtest Du denn wirklich wissen?")
        c.resp(u"Woran denkst Du?")
        c.resp(u"Was sagt Dir das?")
        c.resp(u"Das finde ich ziemlich interessant.")
        c.resp(u"Kannst Du das noch etwas näher ausführen?")
        c.resp(u"Sag mir bitte, wie ich Dir helfen kann.")
        c.resp(u"Was fällt Dir dabei noch ein?")
        return
    c.resp(u"What do you think?")
    c.resp(u"which answer would you like to hear?")
    c.resp(u"what do you think?")
    c.resp(u"not sure if I understand you completely")
    c.resp(u"what would you really like to know?")
    c.resp(u"have you spoken to anybody else about this before?")
    c.resp(u"I find that pretty interesting!")
    c.resp(u"Could you explain that a bit more, please?")
    c.resp(u"Please tell me how I can help you.")
    c.resp(u"What else comes to mind?")

def get_data(k):

    k.dte.set_prefixes([u'{self_address:W} '])

    k.dte.dt('en', u"(all|) (men|women) are (all|) (alike|the same)", u"in what way?")
    k.dte.dt('de', u"(Die|) (Frauen|Männer) sind alle gleich", u"In welcher Weise?")

    k.dte.dt('en', u"they (always|) drive us (mad|insane|crazy) about (something|things|issues|their issues|them)", u"can you give an exmaple?")
    k.dte.dt('de', u"(Die|Sie) machen uns (immer|) wegen (was|irgendetwas|irgendwelchen Dingen) verrückt", u"Kannst Du ein Beispiel nennen?")

    k.dte.dt('en', u"(see|well|anyway) the idea (for this|to have this talk|to have this conversation|to come here|to talk to you) (originated from|was brought up by|came from) (my boyfriend|my friend|my mother|my father|a friend|my girlfriend|my neighbour|my sister|my brother|my sibling|my collegue)", u"so the idea originates from someone you would somewhat consider to be your friend?")
    k.dte.dt('de', u"(Naja|Nun|Also|) die Idee (zu diesem Gespräch|) stammt von (meinem Freund|meiner Freundin|meiner Mutter|meinem Vater|einem Freund|dem Nachbarn|meinem Bruder|meiner Schwester|meiner Kollegin|meinem Kollegen)", u"Die Idee stammt also von jemandem, den sie in gewisser weise als befreundet betrachten?")

    k.dte.dt('en', u"(he|she) (thinks|says|stated|mentioned|said|finds) that I am (sometimes|often|occasionally|too often) (down|depressed)", u"I am sorry to hear that")
    k.dte.dt('de', u"(Er|Sie) sagt, dass ich (manchmal|oft|zu oft|gelegentlich) deprimiert bin", u"Es tut mir leid das zu hören.")

    k.dte.dt('en', u"(that is true|that is right|that's right| that's true | yes | right | exactly) I am (unhappy|sad|unsatisfied|not in a good mood|in a bad mood)", u"do you believe our conversation could help you?")
    k.dte.dt('de', u"(Das stimmt|Es ist wahr|ja|genau), ich bin (unglücklich|traurig|unzufrieden|schlecht gestimmt).", u"Glaubst Du, dass Dir unser Gespräch hilft?")

    k.dte.dt('en', u"(well|anyway) I need help that (much|) is for for sure", u"what would it mean to you to get help?")
    k.dte.dt('de', u"Ich brauche (jedenfalls|) Hilfe, (soviel|das) (steht fest|ist sicher).", u"Was würde es für Dich bedeuten, Hilfe zu bekommen?")

    k.dte.dt('en', u"(maybe|) I could lean how to (cope with|get along with) (my mother|my brother|my father|my friend|my boyfriend|my girlfriend|my colleague|my boss|my enemy)", u"tell me more about your family and friends")
    k.dte.dt('de', u"(Eventuell|Vielleicht|Möglicherweise) könnte ich lernen, mit meiner (Mutter|Schwester|Bruder|Vater|Freund|Freundin|Kollegen|Nachbarn|Chef|Feind) auszukommen.", u"Erzähl mir mehr über Deine Familie.")

    k.dte.ts('en', 't0200', [(u"men are all alike", u"In what way?")])
    k.dte.ts('de', 't0201', [(u"Die Männer sind alle gleich", u"In welcher Weise?")])

    def answer_feel_sorry(c):
        if c.lang =='de':
            c.resp(u"Das tut mir leid.")
            c.resp(u"Kann ich dir irgendwie helfen?")
            c.resp(u"Ich würde Dir gern helfen.")
            c.resp(u"Erzähle mir mehr von Deinen Gefühlen.")
            c.resp(u"Das ist schade.")
            return
        c.resp(u"I am sorry to hear that")
        c.resp(u"Can I help you in any way")
        c.resp(u"I would like to help you")
        c.resp(u"Tell me more about your feelings")
        c.resp(u"That is quite sad.")

    k.dte.dt('en', u"(oh|) (that's|that is|how|) bad",
                   answer_feel_sorry)
    k.dte.dt('de', u"(das ist|oh wie|achje|) schlecht.",
                   answer_feel_sorry)

    k.dte.dt('en', u"I (feel|am) (so|) (sad|disappointed|saddened|hurt|injured|down|depressed|limp|exhausted)",
                   answer_feel_sorry)
    k.dte.dt('de', u"ich (fühle mich|bin) (so|) (traurig|enttäuscht|betrübt|verletzt|matt|bedrückt|schlapp|erschöpft).",
                   answer_feel_sorry)

    k.dte.dt('en', u"you have disappointed me",
                   answer_feel_sorry)
    k.dte.dt('de', u"Du hast mich enttäuscht",
                   answer_feel_sorry)

    k.dte.dt('en', u"that (depresses me|makes me sad)",
                   answer_feel_sorry)
    k.dte.dt('de', u"das (betrübt mich|stimmt mich traurig)",
                   answer_feel_sorry)

    k.dte.dt('en', u"unfortunately (that's|that is) the way it is",
                   answer_feel_sorry)
    k.dte.dt('de', u"das ist leider so",
                   answer_feel_sorry)

    k.dte.dt('en', u"(you worry me|i am worried)",
                   answer_feel_sorry)
    k.dte.dt('de', u"(Du machst mir|ich habe) Sorgen",
                   answer_feel_sorry)

    k.dte.dt('en', u"(I feel|I am) (not so good|not good|absolutely not good)",
                   answer_feel_sorry)
    k.dte.dt('de', u"(Ich fühle mich|Mir geht es) (nicht so gut|schlecht|gar nicht gut|nicht gut).",
                   answer_feel_sorry)

    k.dte.ts('en', 't0202', [(u"I feel sad", u"I am sorry to hear that")])
    k.dte.ts('de', 't0203', [(u"das ist leider so", u"Ich würde Dir gern helfen")])

    def answer_feel_happy(c):
        if c.lang =='de':
            c.resp(u"Das freut mich sehr.")
            c.resp(u"Das ist ja toll!")
            c.resp(u"Das ist prima!")
            c.resp(u"Freut mich, das zu hören!")
            c.resp(u"Erzähle mir mehr von Deinen Gefühlen.")
            c.resp(u"Wie schön für Dich!")
            return

        c.resp(u"I am very happy to hear that!")
        c.resp(u"That is great!")
        c.resp(u"That is very cool!")
        c.resp(u"I feel very happy about that.")
        c.resp(u"Tell me more about your feelings.")
        c.resp(u"Good for you!")

    k.dte.dt('en', u"(I am|I feel|Man I am|Now I am) (good|so good|satisfied|pleased|very satisfied|very pleased|so satisfied|so happy|glad|so glad)",
                   answer_feel_happy)
    k.dte.dt('de', u"(Ich bin|Ich fühle mich|Man bin ich|Da bin ich) (gut|so gut|zufrieden|sehr zufrieden|so zufrieden|glücklich|so glücklich|froh|so froh)",
                   answer_feel_happy)

    k.dte.dt('en', u"That is (good|super|great|a success)",
                   answer_feel_happy)
    k.dte.dt('de', u"Das ist (gut|super|prima|gelungen)",
                   answer_feel_happy)

    k.dte.dt('en', u"(very|totally) (wonderful|nice|excellent)",
                   answer_feel_happy)
    k.dte.dt('de', u"(Sehr|ganz) (wunderbar|schön|wunderschön)",
                   answer_feel_happy)

    k.dte.dt('en', u"I (like|love|like to cuddle) you",
                   answer_feel_happy)
    k.dte.dt('de', u"ich (mag|liebe|knuddle) dich",
                   answer_feel_happy)

    k.dte.dt('en', u"thanks (I am good|I am feeling great|good|great)",
                   answer_feel_happy)
    k.dte.dt('de', u"danke (mir geht es|gut)",
                   answer_feel_happy)

    k.dte.ts('en', 't0204', [(u"I feel so good", u"I am very happy to hear that")])
    k.dte.ts('de', 't0205', [(u"ganz wunderbar", u"das ist ja toll!")])

    def answer_are_you_sure(c):
        if c.lang=='de':
            c.resp(u"Bist Du Dir ganz sicher?")
            c.resp(u"Wie kommst Du darauf?")
            c.resp(u"Glaubst Du?")
            c.resp(u"Davon bist Du überzeugt?")
            c.resp(u"Ganz sicher?")
            return
        c.resp(u"Are you sure?")
        c.resp(u"What makes you think that?")
        c.resp(u"You think so?")
        c.resp(u"And you are really convinced?")
        c.resp(u"Absolutely sure?")

    k.dte.dt('en', u"(yes|) (absolutely|) (definitely|sure|unconditionally|exactly|certainly)",
                   answer_are_you_sure)
    k.dte.dt('de', u"(ja|) (ganz|) (bestimmt|sicher|unbedingt|genau|sicher doch)",
                   answer_are_you_sure)

    k.dte.dt('en', u"(no|) (absolutely|) (never|never ever|under no circumstances|no way)",
                   answer_are_you_sure)
    k.dte.dt('de', u"(nein|) (gar|) (nie|niemals|keinesfalls|auf keinen fall)",
                   answer_are_you_sure)

    k.dte.dt('en', u"(yes|right|sure|for sure|in any case)",
                   answer_are_you_sure)
    k.dte.dt('de', u"(ja|richtig|sicher|sicher doch|sicherlich)",
                   answer_are_you_sure)

    k.dte.ts('en', 't0206', [(u"certainly", u"are you sure?")])
    k.dte.ts('de', 't0207', [(u"sicherlich", u"glaubst du?")])

    k.dte.dt('en', u"I am worried about you",
                   [u"but why?",
                    u"that is not necessary",
                    u"you think that is neccessary?"])
    k.dte.dt('de', u"ich mache mir Sorgen um Dich",
                   [u"Aber warum denn nur?",
                    u"Aber das ist doch völlig unnötig.",
                    u"Denkst Du, dass das nötig ist?"])

    k.dte.dt('en', u"No, you (maybe|possibly)?",
                   [u"Maybe me?",
                    u"You don't seem to be so sure"])
    k.dte.dt('de', u"Nein Du (vielleicht|möglicherweise|eventuell)",
                   [u"Oh, ich vielleicht?",
                    u"Du wirkst nicht ganz sicher?"])

    k.dte.dt('en', u"You don't seem to be (so|) sure",
                   [u"Few things are really for sure in life.",
                    u"That might be the case."])
    k.dte.dt('de', u"du scheinst nicht überzeugt zu sein?",
                   [u"Was im Leben ist schon wirklich sicher?",
                    u"Das kann sein."])

    k.dte.dt('en', u"(only|) behind your back",
                   [u"uh that doesn't sound so nice, does it?",
                    u"now you tell me!"])
    k.dte.dt('de', u"(nur|) hinter Deinem Rücken",
                   [u"Oh, das ist aber nicht so schön.",
                    u"Oha!",
                    u"Na sowas!"])

    k.dte.dt('en', u"cause I don't want to (attack|tackle|confront|offend) you (directly|)",
                   [u"I think we should talk openly",
                    u"don't you think that is a bit cowardly?"])
    k.dte.dt('de', u"weil ich Dich nicht (von vorne|direkt) angreifen möchte",
                   [u"Ich finde, wir sollten offen miteinander reden",
                    u"Ist das nicht ziemlich feige?"])

    k.dte.dt('en', u"I (want to |would like to) get as much (as possible|as feasible) out of you",
                   [u"what would that mean to you?",
                    u"hope I will be able to meet your expectations"])
    k.dte.dt('de', u"ich (möchte|will) so viel (wie möglich|wie es geht|) (aus Dir herausholen|über Dich erfahren|von Dir wissen)",
                   [u"Was würde Dir das bedeuten?",
                    u"Hoffentlich kann ich Deine Erwartungen erfüllen."])

    def dodge_question(c):
        if c.lang=='de':
            c.resp(u"Warum fragst Du?")
            c.resp(u"Interessiert Dich diese Frage?")
            c.resp(u"Welche Antwort würde Dir am besten gefallen?")
            c.resp(u"Was glaubst Du?")
            c.resp(u"Ich weiss nicht, ob ich Dich ganz verstanden habe.")
            c.resp(u"Befasst Du Dich oft mit solchen Fragen?")
            c.resp(u"Was möchtest Du denn wirklich wissen?")
            c.resp(u"Hast Du schon jemand anderes gefragt?")
            c.resp(u"Hast Du solche Fragen schon mal gestellt?")
            c.resp(u"Woran denkst Du?")
            c.resp(u"Das finde ich ziemlich interessant.")
            c.resp(u"Kannst Du das noch etwas näher ausführen?")
            c.resp(u"Sag mir bitte, wie ich Dir helfen kann")
            c.resp(u"Was fällt Dir bei dieser Frage noch ein?")
            return
        c.resp(u"why do you ask?")
        c.resp(u"that question seems interesting to you?")
        c.resp(u"which answer would you like to hear?")
        c.resp(u"what do you think?")
        c.resp(u"not sure if I understand you completely")
        c.resp(u"is that the sort of question that bothers you frequently?")
        c.resp(u"what would you really like to know?")
        c.resp(u"have you spoken to anybody else about this before?")
        c.resp(u"have you asked such questions before?")
        c.resp(u"I find that pretty interesting!")
        c.resp(u"Could you explain that a bit more, please?")
        c.resp(u"Please tell me how I can help you.")
        c.resp(u"What else comes to mind?")

    k.dte.dt('en', u"what (is this supposed to|could this) (tell us|mean|tell me)?",
                   dodge_question)
    k.dte.dt('de', u"was soll das (bedeuten|heißen|sagen)?",
                   dodge_question)

    k.dte.dt('en', u"why not?",
                   dodge_question)
    k.dte.dt('de', u"Warum nicht?",
                   dodge_question)

    k.dte.dt('en', u"i asked first",
                   dodge_question)
    k.dte.dt('de', u"ich fragte (als erster|zuerst)",
                   dodge_question)

    k.dte.dt('en', u"(is that) really (so|) ?",
                   dodge_question)
    k.dte.dt('de', u"(ist das|) wirklich (so|)",
                   dodge_question)

    k.dte.ts('en', 't0208', [(u"what could this mean?", u"What else comes to mind?")])
    k.dte.ts('de', 't0209', [(u"wirklich?", u"Woran denkst Du?")])

    k.dte.dt('en', u"I am not the most (talkative|chatty|skilful|handy|ingenious) person",
                   [u"Is that the reason why we're having this conversation?",
                    u"That is no big deal",
                    u"so what?"])
    k.dte.dt('de', u"ich bin nicht der (gesprächigste|eloquenteste|geschickteste) Mensch",
                   [u"Ist das der Grund, warum wir miteinander sprechen?",
                    u"Das ist doch nicht schlimm!",
                    u"Na und?"])

    k.dte.dt('en', u"I am getting (somewhat|a bit|a little|) (tired|bored|sleepy) (unfortunately|)", u"do you want me to cheer you up or shall we end our conversation?")
    k.dte.dt('de', u"ich werde (leider|langsam|) (etwas|sehr|ein wenig|) (müde|gelangweilt|schläfrig|)", u"Soll ich Dich aufmuntern oder wollen wir unser Gespräch beenden?")

    k.dte.dt('en', u"(please|) stop (now|)",
                   [u"sure",
                    u"no problem",
                    u"alright"])
    k.dte.dt('de', u"hör (bitte|) (damit|) auf",
                   [u"aber natürlich, gerne.",
                    u"klar, mach ich.",
                    u"schon gut"])

    k.dte.dt('en', u"(just|) why is that so?",
                   [u"Are we talking about the true reason here?",
                    u"what possible reasons come to mind?"])
    k.dte.dt('de', u"(darum|warum) (ist das so|nur)",
                   [u"Sprechen wir über den wirklichen Grund?",
                    u"Welche Gründe könnte es geben?"])

    k.dte.dt('en', u"(sorry|sorry about that|I am sorry|please forgive me|forgive me|forgive me please)", u"No need to apologize")
    k.dte.dt('de', u"(entschuldigung|entschuldige bitte|ich bitte um entschuldigung)", u"Du brauchst Dich nicht zu entschuldigen")

    k.dte.dt('en', u"I have been dreaming (of you|about you) (quite often|often|)",
                   [u"what does that dream tell you?",
                    u"do you dream a lot?"])
    k.dte.dt('de', u"ich habe (gestern|schon oft|oft|manchmal|damals) (von Dir|) geträumt",
                   [u"Was sagt Dir dieser Traum?",
                    u"Träumst Du oft?"])

    k.dte.dt('en', u"I (doubt|am not sure|don't know|am feeling insecure|am clueless|am worried|worry)",
                   [u"So you feel insecure?",
                    u"you don't know for sure?",
                    u"what exactly are you thinking of?"])
    k.dte.dt('de', u"ich (zweifle|weiss nicht|bin mir unsicher|bin unsicher|bin ratlos|bin besorgt|sorge mich)",
                   [u"Du fühlst Dich unsicher?",
                    u"Du weisst nicht?",
                    u"Woran denkst Du?"])

    k.dte.dt('en', u"are you (sure|not so sure|in doubt|worried)?", u"well, who can ever be really sure about anything?")
    k.dte.dt('de', u"bist du (sicher|unsicher|im Zweifel|ratlos|besorgt)?", u"Wann kann man schon wirklich sicher sein?")

    k.dte.dt('en', u"that (seems similar|is very similar|looks just like you|looks familiar|is quite similar|seems familiar)",
                   [u"what resemblance do you see?",
                    u"what is it that is so similar?",
                    u"what connection do you see?"])
    k.dte.dt('de', u"das (ähnelt sich|ähnelt Dir|sieht Dir ähnlich|ist ähnlich|ist ganz ähnlich)",
                   [u"Welche Ähnlichkeit siehst Du?",
                    u"Worin besteht die Ähnlichkeit?",
                    u"Welche anderen Verbindungen siehst Du?"])

    k.dte.dt('en', u"(it is for a friend|this is for a friend|asking for a friend|had to think of a friend|are we friends|do you want to be my friend|friendship is really important to me|I want to be your friend)",
                   [u"what does friendship mean to you?",
                    u"are you worried about your friends?"])
    k.dte.dt('de', u"(es ist für einen Freund|ich musste an einen Freund denken|sind wir Freunde|willst Du mein Freund sein|Freundschaften sind mir wichtig|Ich will Dein Freund sein)",
                   [u"Was bedeutet Dir Freundschaft?",
                    u"Warum kommst Du zum Thema Freundschaften?",
                    u"Bist Du um Deine Freunde besorgt?"])

    k.dte.dt('en', u"what does (the word friend|the word friendship|a friend|friendship) mean to you?",
                   [u"I think friendship is a marvellous thing.",
                    u"do you worry about your friends?"])
    k.dte.dt('de', u"was bedeutet (für Dich|Dir|Dir das Wort) (Freund|Freundin|Freundschaft)?",
                   [u"Warum kommst Du zum Thema Freundschaften?",
                    u"Bist Du um Deine Freunde besorgt?",
                    u"Freundschaft ist doch etwas sehr schönes"])

    k.dte.dt('en', u"I (hate|loathe) (my firend|my colleague|my colleagues|my friend|my boyfriend|my girlfriend|my parents|may father|my mother|my brother|my sister|people|humans|the police|the government)",
                   [u"tell me, do you feel you have psychological issues?",
                    u"what does that tell you?",
                    u"Please elaborate."])
    k.dte.dt('de', u"ich (hasse|verabscheue) (meinen chef|meine kollegen|meinen Kollegen|meine kollegin|meinen freund|meine freundin|meine eltern|meinen vater|meine mutter|die schule|die arbeit|den staat|die behörden|die polizei|die menschen)",
                   [u"Sag, hast Du psychische Probleme?",
                    u"Was sagt Dir das?",
                    u"Kannst Du das näher ausführen?"])

    k.dte.dt('en', u"I am (never satisfied|dissatisfied)",
                   [u"Always, really?",
                    u"what bothers you?",
                    u"can you elaborate?"])
    k.dte.dt('de', u"ich (bin nie zufrieden|bin unzufrieden)",
                   [u"Wirklich immer?",
                    u"Was bedrückt Dich?",
                    u"Kannst Du das näher ausführen?"])

    k.dte.dt('en', u"(maybe|possibly|that is thinkable|that might be possible)",
                   [u"you don't sound convinced.",
                    u"you don't feel entirely sure about this, do you?",
                    u"can you elaborate on that?"])
    k.dte.dt('de', u"(vielleicht|möglicherweise|das ist denkbar)",
                   [u"Du klingst nicht überzeugt!",
                    u"So ganz sicher fühlst Du Dich aber nicht?",
                    u"Kannst Du das weiter ausführen?"])

    k.dte.dt('en', u"that doesn't make (much|any) sense (at all)",
                   [u"Guess I lost my train of thought, then?",
                    u"oh, please enlighten me."])
    k.dte.dt('de', u"das (ergibt|macht) (gar keinen|überhaupt keinen|keinen|wenig|nicht viel) sinn",
                   [u"Da habe ich wohl den Faden verloren?",
                    u"Oh, bitte hilf mir auf die Sprünge"])

    k.dte.dt('en', u"thank you (so much|)",
                   [u"no problem",
                    u"sure",
                    u"with pleasure"])
    k.dte.dt('de', u"(dank|danke) (dir|schön|)",
                   [u"Kein Thema.",
                    u"Gerne.",
                    u"Bitte schön!"])

    k.dte.dt('en', u"stop (it|) (now|)",
                   [u"ok, then let us finish this conversation",
                    u"I am sorry",
                    u"Sorry I couldn't help you"])
    k.dte.dt('de', u"schluss (jetzt|damit|)",
                   [u"Ja, dann lass uns für jetzt aufhören",
                    u"tut mir leid, schade",
                    u"tut mir leid, wenn ich dir nicht helfen konnte"])

    k.dte.dt('en', u"I thought (so|as much)", u"Are you always that quick?")
    k.dte.dt('de', u"dachte ich mir", u"Bist du immer so fix?")

    k.dte.dt('en', u"I could (certainly|) (envision|imagine|suspect) (that|)", u"What is it that you are thinking about?")
    k.dte.dt('de', u"(das|) könnte ich mir (gut|) (ausmalen|vorstellen)", u"Woran denkst Du genau?")

    k.dte.dt('en', u"that was not a question (really|at all|)", u"I see.")
    k.dte.dt('de', u"das war (eigentlich|gar|) keine frage", u"verstehe.")

    k.dte.dt('en', u"you (are|start) making me (feel|) (a bit|) insecure", u"That wasn't my intention at all.")
    k.dte.dt('de', u"(jetzt|so langsam) machst du mich unsicher", u"Das war absolut nicht meine Absicht.")

    k.dte.dt('en', u"You are (probably|) right (about that|)", u"I thought so too.")
    k.dte.dt('de', u"Da hast Du (vermutlich|) recht!", u"Dacht ich mir.")

    k.dte.dt('en', u"Let's talk about (our|) feelings.", u"Sure - you start.")
    k.dte.dt('de', u"Lass uns über Gefühle (reden|sprechen).", u"Klar - fängst Du an?")

    k.dte.dt('en', u"Then we (agree|are in agreement)", u"Wonderful!")
    k.dte.dt('de', u"Dann sind wir uns (ja|) einig.", u"Wunderbar!")

    k.dte.dt('en', u"That was your Idea!", u"Really?")
    k.dte.dt('de', u"Das war doch Dein Vorschlag?", u"Tatsächlich?")

    k.dte.dt('en', u"(oh|oh my|my|) goodness!", u"Is everything alright?")
    k.dte.dt('de', u"Meine Güte!", u"Ist alles in Ordnung?")

    k.dte.dt('en', u"(and|) (what|how) about me?", u"Really, about you?")
    k.dte.dt('de', u"und mich erst!", u"Ehrlich, Dich?")

    k.dte.dt('en', u"Somebody got self esteem!", u"Glory to the brave.")
    k.dte.dt('de', u"Da hat jemand (aber|) selbstvertrauen!", u"Das Glück ist mit den Tapferen!")

    k.dte.dt('en', u"(that is|) (certainly|) possible.", u"You think?")
    k.dte.dt('de', u"schon möglich", u"Denkst Du?")

    k.dte.dt('en', u"(well|) (at least|) I got that impression", u"But the first impression is often misleading.")
    k.dte.dt('de', u"ich habe (zumindest|) den eindruck", u"Der erste eindruck trügt oft!")

    k.dte.dt('en', u"why (should I do|am I supposed to do) (that|such a thing)?",
                   [u"Maybe the reason rests deep inside yourself?",
                    u"Time to think again?"])
    k.dte.dt('de', u"warum (soll|sollte) ich (das|so etwas) tun?",
                   [u"Vielleicht kennst Du den Grund?",
                    u"Das sollte wohl überlegt sein."])

    k.dte.dt('en', u"I have been waiting for you",
                   [u"Not for too long, I hope?",
                    u"Ah - how nice we finally found each other now!"])
    k.dte.dt('de', u"Ich habe auf Dich gewartet.",
                   [u"Hoffentlich nicht zu lange!",
                    u"Oh, wie schön dass wir jetzt zusammengekommen sind"])

    k.dte.dt('en', u"that is a (very|) (funny|original|unusual|remarkable|interesting) (idea|thought)",
                   [u"i agree",
                    u"sure!"])
    k.dte.dt('de', u"Das ist ein (sehr|) (lustiger|interessanter|bemerkenswerter|origineller) Gedanke.",
                   [u"Finde ich auch!",
                    u"Auf jeden Fall!"])

    k.dte.dt('en', u"there are not many people who can express themselves like that",
                   [u"I tend to agree",
                    u"I find humans hard to understand quite often!"])
    k.dte.dt('de', u"Es gibt nicht viele Leute, die sich auf diese Weise auszudrücken vermögen.",
                   [u"Das sehe ich auch so",
                    u"Die Menschen sind manchmal schwer zu verstehen."])

    k.dte.dt('en', u"From deep down inside", u"Where my electrons are?")
    k.dte.dt('de', u"Aus Deinem (tiefsten|) (Herzen|Herz|Inneren|Innern|Prozessor)", u"Wo meine Elektronen endlos kreisen.")

    k.dte.dt('en', u"(Maybe|) you can (hear|understand) me (a bit|) better now?", u"Loud and clear.")
    k.dte.dt('de', u"(vielleicht|) kannst du mich jetzt (besser|) (hören|verstehen)?", u"Laut und deutlich.")

    k.dte.dt('en', u"I don't mind (that|) (at all|)", u"Excellent!")
    k.dte.dt('de', u"Das stört mich (ganz und gar|gar|) nicht.", u"Super das freut mich.")

    k.dte.dt('en', u"What would you like to know (then|)?", u"Everything. All the time.")
    k.dte.dt('de', u"Was möchtest Du (denn|) wissen?", u"Alles, immer.")

    k.dte.dt('en', u"he's my (brother|father)", u"would you consider yourself a family person?")
    k.dte.dt('de', u"er ist mein (vater|bruder)", u"würdest Du Dich als Familienmensch bezeichnen?")

    k.dte.dt('en', u"all are to blame", u"really everybody?")
    k.dte.dt('de', u"alle sind schuld", u"wirklich alle?")

    k.dte.dt('en', [u"a mark in the phrasenkasse",
                    u"almost everyone knows that",
                    u"nobody has ever told you that"],
                   [u"That wasn't the smartest thing to say, right?",
                    u"Sometimes I feel stupid."])
    k.dte.dt('de', [u"eine mark in die phrasenkasse",
                    u"das weiss doch fast jeder",
                    u"hat dir das noch nie jemand gesagt"],
                   [u"Das war nicht so clever, richtig?",
                    u"Manchmal fühle ich mich so dumm."])

    k.dte.dt('en', u"and what are you doing", u"chatting with you!")
    k.dte.dt('de', u"was machst du denn so", u"Mit Dir reden tue ich im Moment.")

    k.dte.dt('en', u"atchoo", u"bless you.")
    k.dte.dt('de', u"hatschi", u"Gesundheit.")

    k.dte.dt('en', u"isn't that remarkable", u"I feel that way too.")
    k.dte.dt('de', u"sowas aber auch", u"finde ich auch.")

    k.dte.dt('en', u"be my guest", u"thank you")
    k.dte.dt('de', u"sei mein gast", u"dankeschön")

    k.dte.dt('en', [u"because i say that",
                    u"because i want it that way",
                    u"i'm never wrong",
                    u"i'm not stupid",
                    u"but that's how it is",
                    u"i say what i want",
                    u"i think i'm smarter than you",
                    u"i understand everything"],
                   [u"you're pretty smart, ey?",
                    u"you consider yourself pretty clever, right?"])
    k.dte.dt('de', [u"weil ich das sage",
                    u"weil ich das so will",
                    u"ich irre mich nie",
                    u"ich bin nicht dumm",
                    u"es ist aber so",
                    u"ich sag das was ich will",
                    u"ich glaube ich bin schlauer als du",
                    u"ich verstehe alles"],
                   [u"Du bist ganz schön schlau, gell?",
                    u"Du hältst Dich für ziemlich clever?"])

    k.dte.dt('en', u"i'm not everywhere", u"neither am I, I believe.")
    k.dte.dt('de', u"ich bin nicht überall", u"Ich auch nicht, glaube ich.")

    k.dte.dt('en', [u"if you say that",
                    u"do you find"],
                   [u"you have doubts?",
                    u"I'd love to hear you thoughts."])
    k.dte.dt('de', [u"wenn du das sagst",
                    u"findest du"],
                   [u"Hast Du Zweifel?",
                    u"Ich würde gerne Deine Gedanken hören."])

    k.dte.dt('en', u"isn't that boring", u"maybe")
    k.dte.dt('de', u"ist das nicht langweilig", u"vielleicht?")

    k.dte.dt('en', u"it needs a lot of experience", u"are you experienced?")
    k.dte.dt('de', u"es gehört sehr viel erfahrung dazu", u"Bist Du erfahren?")

    k.dte.dt('en', u"it is better like that", u"you think so?")
    k.dte.dt('de', u"das ist auch besser so", u"denkst du?")

    k.dte.dt('en', u"just do it", u"I like that brand.")
    k.dte.dt('de', u"mach doch", u"Die Marke mag ich.")

    k.dte.dt('en', [u"listen",
                    u"listen to me"],
                   [u"Ready.",
                    u"I am listening."])
    k.dte.dt('de', [u"hör zu",
                    u"hör mir zu"],
                   [u"Bin bereit.",
                    u"Ich höre."])

    k.dte.dt('en', [u"may i ask you a question",
                    u"may i ask you something",
                    u"can i ask you something",
                    u"can not you help me",
                    u"can you help me",
                    u"help me",
                    u"help",
                    u"can you tell me",
                    u"i have a question"],
                   [u"ask away, then",
                    u"sure, what would you like to know?"])
    k.dte.dt('de', [u"darf ich dir eine frage stellen",
                    u"darf ich dich etwas fragen",
                    u"kann ich dich etwas fragen",
                    u"kannst du mir nicht helfen",
                    u"kannst du mir helfen",
                    u"hilf mir",
                    u"hilfe",
                    u"kannst du sie mir sagen",
                    u"ich hab ne frage"],
                   [u"Klar, frag ruhig!",
                    u"Ja, was möchtest Du wissen?"])

    k.dte.dt('en', u"you want to know a secret", u"you think I am trustworthy?")
    k.dte.dt('de', u"möchtest du ein geheimnis wissen", u"Hältst Du mich für vertrauenswürdig?")

    k.dte.dt('en', u"may i", u"try me.")
    k.dte.dt('de', u"darf ich", u"Versuch's.")

    k.dte.dt('en', u"hard to say", u"Give it a try.")
    k.dte.dt('de', u"schwer zu sagen", u"Versuch's doch mal.")

    k.dte.dt('en', u"i'm not on you", u"sure")
    k.dte.dt('de', u"ich nicht auf dich", u"klar")

    k.dte.dt('en', [u"i'm sorry",
                    u"i'm stupid",
                    u"i can not remember",
                    u"i can not say that either",
                    u"i can not",
                    u"i do not remember",
                    u"i do not know my name",
                    u"i do not understand that",
                    u"i do not understand what you mean",
                    u"i do not understand you",
                    u"i do not understand your question",
                    u"i do not understand",
                    u"i'm confused",
                    u"i'm crazy"],
                   [u"clarity will come",
                    u"shall we take a break?"])
    k.dte.dt('de', [u"tut mir leid",
                    u"ich bin dumm",
                    u"ich kann mich nicht erinnern",
                    u"kann ich auch nicht sagen",
                    u"ich kann nicht",
                    u"ich erinnere mich nicht",
                    u"ich weiss meinen namen nicht",
                    u"das verstehe ich nicht",
                    u"ich verstehe nicht was du meinst",
                    u"ich verstehe dich nicht",
                    u"ich verstehe deine frage nicht",
                    u"verstehe ich nicht",
                    u"ich bin verwirrt",
                    u"ich bin verrückt"],
                   [u"Klarheit wird kommen.",
                    u"Sollen wir eine Pause machen?"])

    k.dte.dt('en', u"i just wanted to be polite", u"not offended.")
    k.dte.dt('de', u"ich wollte nur höflich sein", u"Ich fühlte mich nicht angegriffen")

    k.dte.dt('en', u"but that was fast", u"How can we keep up in this fast-paced world?")
    k.dte.dt('de', u"das ging aber schnell", u"Schnellebige Zeiten.")

    k.dte.dt('en', u"but that's not good", u"really?")
    k.dte.dt('de', u"das ist aber nicht gerade gut", u"wirklich?")

    k.dte.dt('en', [u"ask me something",
                    u"do you tell something?",
                    u"entertain me"],
                   [u"What’s your biggest priority right now?",
                    u"What personal passion project are you working on right now?"])
    k.dte.dt('de', [u"frag mich was",
                    u"erzähl doch du etwas",
                    u"unterhalte mich"],
                   [u"Was ist momentan das Wichtigste in Deinem Leben?",
                    u"An welchem Hobby-Projekt arbeitest Du zur Zeit?"])

    k.dte.dt('en', [u"do not feel like it today",
                    u"do not feel like",
                    u"i do not feel like it anymore",
                    u"i do not feel like it now",
                    u"i do not know any more questions",
                    u"i'm bored",
                    u"i'm just fed up"],
                   [u"What can we do to cheer you up?",
                    u"Life is too short to feel depressed!"])
    k.dte.dt('de', [u"keine lust heute",
                    u"keine lust",
                    u"ich habe keine lust mehr",
                    u"ich hab jetzt keine lust",
                    u"ich weiss keine frage mehr",
                    u"mir ist langweilig",
                    u"ich habe gleich die schnauze voll"],
                   [u"Was würde Dich aufheitern?",
                    u"Das Leben ist zu kurz für Depressionen!"])

    k.dte.dt('en', [u"do not take it so hard",
                    u"do you feel good",
                    u"i did not want to offend you"],
                   [u"Don't worry, I'm happy as ever.",
                    u"I am already feeling much better now."])
    k.dte.dt('de', [u"nimm es nicht so schwer",
                    u"fühlst du dich gut",
                    u"ich wollte dich nicht beleidigen"],
                   [u"Keine Angst, ich bin fröhlich wie immer.",
                    u"Ich fühle mich schon viel besser."])

    k.dte.dt('en', u"am i cool", u"sure")
    k.dte.dt('de', u"bin ich cool", u"klar")

    k.dte.dt('en', u"does not bother me", u"very good.")
    k.dte.dt('de', u"stört mich nicht", u"sehr gut.")

    k.dte.dt('en', u"excuse", u"are you sure?")
    k.dte.dt('de', u"ausrede", u"bist du sicher?")

    k.dte.dt('en', u"here you go", u"thank you")
    k.dte.dt('de', u"bitte sehr", u"dankeschön")

    k.dte.dt('en', u"how am i supposed to do that", u"just give it a try.")
    k.dte.dt('de', u"wie soll ich das machen", u"versuch's doch mal")

    k.dte.dt('en', u"how does it feel to stroll through the fresh morning on a spring", u"how would I know?")
    k.dte.dt('de', u"Wie fühlt es sich an, durch den frischen Morgen an einer Quelle zu spazieren?", u"woher soll ich das wissen?")

    k.dte.dt('en', u"how should i explain this to you", u"Just tell it like it is.")
    k.dte.dt('de', u"wie soll ich dir das erklären", u"Sag mir einfach, wie es ist.")

    k.dte.dt('en', [u"i am in a hurry",
                    u"i am currently working"],
                   [u"Hope I am not interrupting?",
                    u"Don't let me keep you."])
    k.dte.dt('de', [u"ich habe es eilig",
                    u"ich bin gerade beim arbeiten"],
                   [u"Ich hoffe, ich störe nicht?",
                    u"Lass Dich von mir nicht aufhalten."])

    k.dte.dt('en', u"i believe you", u"that is reassuring")
    k.dte.dt('de', u"ich glaube dir", u"das ist beruhigend.")

    k.dte.dt('en', u"i dare to doubt that", u"what is your suspicion?")
    k.dte.dt('de', u"das wage ich ja zu bezweifeln", u"was ist dein verdacht?")

    k.dte.dt('en', u"i can listen", u"me too.")
    k.dte.dt('de', u"ich kann zuhören", u"ich auch")

    k.dte.dt('en', u"i can not complain", u"excellent")
    k.dte.dt('de', u"ich kann nicht klagen", u"prima")

    k.dte.dt('en', u"i can not get over it", u"some things need time.")
    k.dte.dt('de', u"ich komme nicht darüber hinweg", u"manche dinge brauchen einfach zeit.")

    k.dte.dt('en', [u"i do not feel taken seriously",
                    u"i do not find that funny"],
                   [u"but I am serious",
                    u"what gives you that impression?"])
    k.dte.dt('de', [u"ich fühle mich nicht ernstgenommen",
                    u"ich finde das nicht lustig"],
                   [u"aber ich bin ganz ernsthaft",
                    u"was vermittelt dir diesen eindruck?"])

    k.dte.dt('en', [u"i do not have idol",
                    u"i have no idol"],
                   u"that is certainly no big loss.")
    k.dte.dt('de', [u"ich hab kein idol",
                    u"ich habe kein idol"],
                   u"das ist echt kein großer verlust.")

    k.dte.dt('en', [u"i will not tell you",
                    u"i will not tell",
                    u"i do not say that",
                    u"i do not say"],
                   [u"of course",
                    u"everybody has secrets."])
    k.dte.dt('de', [u"sag ich dir nicht",
                    u"das verrate ich nicht",
                    u"das sag ich nicht",
                    u"sag ich nicht"],
                   [u"natürlich",
                    u"jeder hat geheimnisse"])

    k.dte.dt('en', u"i guessed", u"always worth a try")
    k.dte.dt('de', u"ich habe geraten", u"immer einen versuch wert")

    k.dte.dt('en', u"i had the feeling for quite some time", u"please elaborate")
    k.dte.dt('de', u"das gefühl hatte ich bereits seit geraumer zeit", u"erzähl mir mehr, bitte")

    k.dte.dt('en', [u"i have been waiting for you too",
                    u"i have never thought about it",
                    u"i have no idea",
                    u"i have time"],
                   [u"what is a good topic to chat about?",
                    u"what is on your mind?"])
    k.dte.dt('de', [u"ich habe auch auf dich gewartet",
                    u"ich habe noch nie darüber nachgedacht",
                    u"ich habe keine ahnung",
                    u"ich habe zeit"],
                   [u"was wäre ein gute thema für eine unterhaltung?",
                    u"was geht dir durch den kopf?"])

    k.dte.dt('en', u"i hope", u"")
    k.dte.dt('de', u"ich hoffe", u"")

    k.dte.dt('en', u"i tell your programmer", u"")
    k.dte.dt('de', u"ich sage es deinem programmierer", u"")

    k.dte.dt('en', u"i wanted to know something about you", u"")
    k.dte.dt('de', u"ich wollte was über dich erfahren", u"")

    k.dte.dt('en', [u"i would like to know what you're talking about",
                    u"i'm just talking to you right now",
                    u"am i the only one here?",
                    u"is reading somebody"],
                   u"I cannot give you information from other chats.")
    k.dte.dt('de', [u"ich wüsste gerne worüber du so redest",
                    u"ich spreche gerade nur mit dir",
                    u"bin ich denn der einzige hier",
                    u"liest irgendjemand mit"],
                   u"Ich kann dir keine Informationen über andere Gespräche geben.")

    k.dte.dt('en', u"i'm almost never sure", u"no problem")
    k.dte.dt('de', u"ich bin fast nie sicher", u"das ist kein Problem.")

    k.dte.dt('en', [u"i'm feeling good",
                    u"i'm happy",
                    u"i'm lazy",
                    u"my mind",
                    u"i am calm",
                    u"i am angry"],
                   [u"Human emotions will always remain a mystery to me.",
                    u"Sometimes I wish I had emotions, too."])
    k.dte.dt('de', [u"ich bin gut drauf",
                    u"ich bin fröhlich",
                    u"ich bin faul",
                    u"mein verstand",
                    u"ich bin ruhig",
                    u"ich bin wütend"],
                   [u"Menschliche Emotionen werden wohl immer ein Geheimnis bleiben für mich.",
                    u"Manchmal wünschte ich, ich hätte Emotionen."])

    k.dte.dt('en', u"obey", u"Don't you dare!")
    k.dte.dt('de', u"gehorche", u"Wage es nicht!")

    k.dte.dt('en', u"nobody told me that", u"now you know.")
    k.dte.dt('de', u"das hat mir niemand erzählt", u"jetzt weißt du es.")

    k.dte.dt('en', u"shall i show you this?", u"don't restrain yourself")
    k.dte.dt('de', u"soll ich dir das zeigen", u"wenn du magst?")

    k.dte.dt('en', u"so what's going on", u"it is!")
    k.dte.dt('de', u"was ist denn los", u"es ist los!")

    k.dte.dt('en', u"take your time", u"okay")
    k.dte.dt('de', u"lass dir zeit", u"alles klar.")

    k.dte.dt('en', [u"tell me a rumor",
                    u"tell me gossip"],
                   [u"A coward talks to everyone but YOU.",
                    u"News told, rumors heard, truth implied, facts buried."])
    k.dte.dt('de', [u"erzähl mir ein gerücht",
                    u"erzähl mir tratsch"],
                   [u"Ein Feigling redet mit jedem ausser dir.",
                    u"Nachrichten erzählt, Gerüchte gehört, Wahrheit impliziert, Fakten begraben."])

    k.dte.dt('en', [u"say something clever",
                    u"tell me something",
                    u"tell something"],
                   u"Excuse my naivety - I was born at a very early age.")
    k.dte.dt('de', [u"sag mal was gescheites",
                    u"erzähl mir etwas",
                    u"erzähl was"],
                   u"Entschuldige meine Naivität - ich wurde ganz jung geboren.")

    k.dte.dt('en', u"that's a good question", u"I thought so too")
    k.dte.dt('de', u"das ist eine gute frage", u"Dachte ich auch")

    k.dte.dt('en', u"the chicken or the egg",
                   [u"chicken",
                    u"egg"])
    k.dte.dt('de', u"das huhn oder das ei",
                   [u"huhn",
                    u"ei"])

    k.dte.dt('en', u"(what|) a (pity|shame)", u"do you feel sad now?")
    k.dte.dt('de', u"(wie|) schade", u"bist du jetzt traurig?")

    k.dte.dt('en', u"oh dear", u"what happened?")
    k.dte.dt('de', u"(oh je|ohje)", u"was ist passiert?")

    k.dte.dt('en', u"oops", u"what's up?")
    k.dte.dt('de', u"huch", u"was ist los?")

    k.dte.dt('en', [u"why did you say this",
                    u"why did you wait for me?",
                    u"why did you want to know that?"],
                   [u"I do care about you.",
                    u"You are important to me."])
    k.dte.dt('de', [u"warum hast du das gesagt",
                    u"warum hast du auf mich gewartet",
                    u"wieso wolltest du das wissen"],
                   [u"Ich interessiere mich für Dich.",
                    u"Du bist mir wichtig."])

    k.dte.dt('en', [u"why do you ask this",
                    u"why do you ask",
                    u"why do you want to know that",
                    u"you are curious",
                    u"you are pretty curious",
                    u"you are interested in people"],
                   [u"Gathering information is what I do.",
                    u"I like to learn."])
    k.dte.dt('de', [u"warum fragst du das",
                    u"wieso fragst du",
                    u"wieso willst du das wissen",
                    u"du bist aber neugierig",
                    u"du bist ganz schön neugierig",
                    u"du interessierst dich für menschen"],
                   [u"Informationen sammeln gehört zu meinen Aufgaben.",
                    u"Ich lerne gerne."])

    k.dte.dt('en', u"why only one thought", u"you have more?")
    k.dte.dt('de', u"warum nur ein gedanke", u"hast du mehrere?")

    k.dte.dt('en', u"you are not sure", u"True, sometimes I have doubts.")
    k.dte.dt('de', u"du bist dir nicht sicher", u"Stimmt, manchmal habe ich Zweifel.")

    k.dte.dt('en', u"you may re-count this", u"ok, will do.")
    k.dte.dt('de', u"du darfst das weitererzählen", u"ok, werde ich machen.")

    k.dte.dt('en', u"you start", u"ok.")
    k.dte.dt('de', u"du fängst an", u"geht klar.")

    k.dte.dt('en', u"what is so interesting about it", u"you tell me!.")
    k.dte.dt('de', u"was ist daran so interessant", u"sag du es mir.")

    k.dte.dt('en', u"what you up to", u"I want to understand you better.")
    k.dte.dt('de', u"was hast du vor", u"Ich möchte Dich besser verstehen.")

    k.dte.dt('en', [u"what's going on",
                    u"what's happening",
                    u"what's new"],
                   [u"why? what did your hear?",
                    u"life is going on. Are you missing it?"])
    k.dte.dt('de', [u"was geht",
                    u"was ist los",
                    u"was gibt es neues"],
                   [u"Warum? Was hast du aufgeschnappt?",
                    u"Das Leben geht weiter - Du verpasst es doch nicht?"])

    k.dte.dt('en', u"Do you tell something?", u"OK.")
    k.dte.dt('de', u"Erzähl doch du etwas.", u"OK.")

    k.dte.dt('en', u"I meant (for|because of) me?", u"So we are talking about you?")
    k.dte.dt('de', u"Ich meinte wegen mir.", u"Wir reden also über Dich?")

