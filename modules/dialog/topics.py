#!/usr/bin/env python
# -*- coding: utf-8 -*-

# some building blocks that might be useful in other modules:

def question_what_was_our_topic_en():
    return [u"What (were we talking|did we talk) about (again|) ?", 
            u"(Which|What) was our topic (again|)?", 
            u"Give me a hint", 
            u"Which topic did we have (again|)?", 
            u"I (think|believe) I lost my train of thought (just now|again|).", 
            u"(lets get|) back to our topic.", 
            u"what are we talking about right now", 
            u"what have we just talked about?", 
            u"what did we just chat about?", 
            u"what are we talking about at the moment", 
            u"what did we talk about earlier", 
            u"what have we talked about?", 
            u"what is our topic", 
            u"so back to the topic"]

def question_what_was_our_topic_de():
    return [u"(Wovon|Worüber|Was) (hatten|haben) wir (eben|) gesprochen?", 
            u"(Wie|Was) war (doch gleich|gleich|) unser Thema?", 
            u"(Hilfst Du|Hilf) mir (bitte|) auf die Sprünge?", 
            u"Welches Thema hatten wir (doch gleich|)?", 
            u"Ich (glaub|glaube|) ich habe (jetzt|) den Faden verloren?", 
            u"Jetzt habe ich (glaube ich|) den Faden verloren.", 
            u"Also zurück zum Thema!", "worüber reden wir gerade", 
            u"worüber haben wir gerade geredet", 
            u"worüber haben wir gerade gesprochen", 
            u"worüber reden wir im moment", 
            u"worüber haben wir vorhin gesprochen", 
            u"worüber haben wir gesprochen", 
            u"was ist unser thema"]

def get_data(k):
    k.dte.set_prefixes([u'{self_address:W} '])


    def answer_what_was_our_topic_en(c):

        # did we talk about some entity?

        xsb_make_vars(2)
        rcode = xsb_query_string("mem(%s, f1ent, E), rdfsLabel(E, en, L)." % c.user)

        if not rcode:

            while not rcode:

                s1 = xsb_var_string(1)
                s2 = xsb_var_string(2)

                # import pdb; pdb.set_trace()

                c.resp(u"We have been talking about %s, I think." % s2, score=100.0)
                c.resp(u"Our topic was %s, I believe." % s2, score=100.0)
                c.resp(u"Didn't we talk about %s?" % s2, score=100.0)

                rcode = xsb_next()
        else:

            # dodge question

            c.resp(u"We have had many topics.")
            c.resp(u"We were talking about you for the most part, I believe.")
            c.resp(u"What would you like to talk about?")

    def answer_what_was_our_topic_de(c):

        # did we talk about some entity?

        xsb_make_vars(2)
        rcode = xsb_query_string("mem(%s, f1ent, E), rdfsLabel(E, de, L)." % c.user)

        if not rcode:

            while not rcode:

                s1 = xsb_var_string(1)
                s2 = xsb_var_string(2)

                # import pdb; pdb.set_trace()

                c.resp(u"Wir hatten über %s gesprochen, glaube ich." % s2, score=100.0)
                c.resp(u"Ich denke unser Thema war %s." % s2, score=100.0)
                c.resp(u"Sprachen wir nicht über %s ?" % s2, score=100.0)

                rcode = xsb_next()
        else:

            # dodge question

            c.resp(u"Wir hatten schon viele Themen.")
            c.resp(u"Ich glaube wir haben vor allem über Dich gesprochen.")
            c.resp(u"Worüber würdest Du denn gerne sprechen?")

    k.dte.dt('en', question_what_was_our_topic_en(), answer_what_was_our_topic_en)
    k.dte.dt('de', question_what_was_our_topic_de(), answer_what_was_our_topic_de)

    k.dte.ts('en', 'topics0000', [(u"what did we talk about", u"We have had many topics.", [])])
    k.dte.ts('de', 'topics0001', [(u"worüber haben wir gesprochen?", u"Wir hatten schon viele Themen.", [])])

    def prep_topic(c):
        xsb_command_string('retractall(mem(%s, f1ent, _)).' % c.user)
        xsb_command_string('assertz(mem(%s, f1ent, wdeStuttgart)).' % c.user)

    k.dte.ts('en', 'topics0002', [(u"what did we talk about", u"our topic was stuttgart i believe", [])], prep=prep_topic)
    k.dte.ts('de', 'topics0003', [(u"worüber haben wir gesprochen?", u"Sprachen wir nicht über Stuttgart?", [])], prep=prep_topic)

    k.dte.dt('en', u"can you give me information on this topic", u"Ask away!")
    k.dte.dt('de', u"kannst du mir informationen zu diesem thema geben", u"Frag ruhig!")

    k.dte.dt('en', [u"about which topic",
                    u"I conclude the previous topic",
                    u"let us talk about something else",
                    u"let's change the subject",
                    u"let's talk about something else",
                    u"other topic"],
                   [u"So what would you like to talk about next?",
                    u"So what is our next topic?"])
    k.dte.dt('de', [u"über welches thema",
                    u"ich schließe das vorherige thema ab",
                    u"lass uns über etwas anderes reden",
                    u"lass uns das thema wechseln",
                    u"lass uns über was anderes reden",
                    u"anderes thema"],
                   [u"Worüber würdest du gerne als nächstes sprechen?",
                    u"Was ist also unser nächstes Thema?"])

    k.dte.dt('en', u"can you give me an answer", u"I tend to answer all questions, sometimes even successfully!")
    k.dte.dt('de', u"kannst du mir eine antwort geben", u"Ich neige dazu, alle Fragen zu beantworten - manchmal sogar erfolgreich!")

