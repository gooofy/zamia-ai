#!/usr/bin/env python
# -*- coding: utf-8 -*-

def get_data(k):
    k.dte.set_prefixes([u'{self_address:L} '])
    def my_languagesupport(en):
        or("My system supports german and english but this instance is configured for english", "I am currently running in english mode but I can be configured for german, too", "This seems to be my english configuration, but I can be run in german mode, too")
    def my_languagesupport(de):
        or("Mein System unterstützt Deutsch und Englisch aber diese Instanz ist für Deutsch konfiguriert", "Ich laufe gerade im deutschen Modus aber man kann mich auch auf Englisch umschalten", "Dies hier scheint meine deutsche Version zu sein, man kann mich aber auch auf Englisch betreiben")
    k.dte.dt('en', u"which languages do you speak",
                   % inline(my_languagesupport(en)))
    k.dte.dt('de', u"welche sprachen sprichst du",
                   % inline(my_languagesupport(de)))

    k.dte.dt('en', u"(do you understand | do you speak | are you|do you know) (english|american|german|arabic|french|turkish|spanish|italian) (well|) (by the way|really|)",
                   % inline(my_languagesupport(en)))
    k.dte.dt('en', u"can you (speak|understand|talk in) (english|american|german|arabic|french|spanish|italian) (well|) (by the way|really|too|)",
                   % inline(my_languagesupport(en)))

    k.dte.dt('en', u"are you (really|) as good as your (english|american|german) program (by the way|)?",
                   % inline(my_languagesupport(en)))
    k.dte.dt('en', [u"why do you speak german",
                    u"since when do you speak German",
                    u"why are you talking German",
                    u"which languages do you speak"],
                   % inline(my_languagesupport(en)))

    k.dte.dt('de', [u"warum kannst du deutsch",
                    u"seit wann sprichst du deutsch",
                    u"warum redest du deutsch",
                    u"welche sprachen sprichst du"],
                   % inline(my_languagesupport(de)))
    k.dte.dt('en', u"Do you know your (english-speaking|german-speaking) (brother|sister)?", u"sure, lives in the folder right next to mine")

    k.dte.dt('de', u"kennst du deine (deutschsprachige|englischsprachige) schwester?", u"klar, wohnt im verzeichnis nebenan.")
    k.dte.dt('de', u"kennst du deinen (deutschsprachigen|englischsprachigen) bruder?", u"klar, wohnt im verzeichnis nebenan.")

    k.dte.dt('en', u"(which|what|love that|is your|do you like that|) language?",
                   % inline(my_languagesupport(en)))
    k.dte.dt('de', u"(sprichst|bist|verstehst) du (eigentlich|auch|) (gut|) (englisch|amerikanisch|deutsch|türkisch|arabisch|französisch|spanisch|italienisch)",
                   % inline(my_languagesupport(de)))

    k.dte.dt('de', u"kannst du (eigentlich|) (auch|) (gut|) (englisch|amerikanisch|deutsch|arabisch|französisch|spanisch|italienisch) (verstehen|sprechen)",
                   % inline(my_languagesupport(de)))
    k.dte.dt('de', u"bist du (eigentlich|) so gut wie dein (englisches|amerikanisches|deutsches) programm?",
                   % inline(my_languagesupport(de)))

    k.dte.dt('de', u"(kennst Du diese|was für eine|welche|magst du die|) Sprache?",
                   % inline(my_languagesupport(de)))
    k.dte.dt('en', u"Are you good in (english|american|german|arabic|french|turkish|spanish|italian)?",
                   % inline(my_languagesupport(en)))

    k.dte.dt('de', u"Bist Du gut in (Englisch|Deutsch|Amerikanisch|arabisch|französisch|spanisch|italienisch)?",
                   % inline(my_languagesupport(de)))
    k.dte.dt('en', u"in which language may I speak?",
                   % inline(my_languagesupport(en)))

    k.dte.dt('de', u"in welcher sprache darf ich sprechen",
                   % inline(my_languagesupport(de)))
    k.dte.dt('en', u"can you understand foreign languages?",
                   % inline(my_languagesupport(en)))

    k.dte.dt('de', u"kannst du fremdsprachen verstehen",
                   % inline(my_languagesupport(de)))
    k.dte.dt('en', u"you can not understand foreign languages",
                   % inline(my_languagesupport(en)))

    k.dte.dt('de', u"du kannst keine fremdsprachen verstehen",
                   % inline(my_languagesupport(de)))
    k.dte.dt('en', u"(are your good in|are you fluent in|how well do you speak|) (english|american|german|arabic|french|turkish|spanish|italian)",
                   % inline(my_languagesupport(en)))

    k.dte.dt('de', u"(bist du gut in|sprichst du|sprichst du fließend|wie gut bist du in|wie gut kannst du) (Englisch|Deutsch|Amerikanisch|Arabisch|Französisch|Spanisch|Italienisch)?",
                   % inline(my_languagesupport(de)))
    k.dte.dt('en', u"pity but you will still learn in my language", u"Sure!")

    k.dte.dt('de', u"schade aber das wirst du auch in meiner sprache noch lernen", u"Sicherlich!")
    k.dte.dt('en', u"in which lexicon", u"wiktionary or something.")

    k.dte.dt('de', u"in welchem lexikon", u"Wiktionary oder so.")
    k.dte.dt('en', u"What (about|is) linguistics?", u"Linguistics is the science of language itself.")

    k.dte.dt('de', u"Was (weißt Du über|ist) Linguistik", u"Linguistik ist die Wissenschaft von der Sprache an sich.")
    k.dte.dt('en', u"You do not know which language you speak", u"Really?")

    k.dte.dt('de', u"Du weisst nicht in welcher sprache du sprichst", u"Echt jetzt?")
    k.dte.ts('en', 't0020', [(u"Computer do you speak german?", u"My system supports german and english but this instance is configured for english")])
    k.dte.ts('de', 't0021', [(u"Computer sprichst Du auch englisch?", u"Dies hier scheint meine deutsche Version zu sein, man kann mich aber auch auf Englisch betreiben")])

    k.dte.dt('en', u"can you speak", u"can you hear me now?")

    k.dte.dt('de', u"kannst du sprechen", u"kannst du mich jetzt hören?")
    k.dte.dt('en', u"do you know 1000 words or more?", u"far more!")

    k.dte.dt('de', u"kennst du 1000 wörter oder mehr?", u"viel mehr!")
    k.dte.dt('en', u"do you know key words", u"lots of them!")

    k.dte.dt('de', u"kennst du schluesselwoerter", u"viele!")
    k.dte.dt('en', u"do you know many words", u"even more!")

    k.dte.dt('de', u"kennst du viele woerter", u"noch mehr!")
