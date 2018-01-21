#!/usr/bin/env python
# -*- coding: utf-8 -*-

def get_data(k):
    k.dte.set_prefixes([u'{self_address:L} '])
    def train_ner(en, federated_state, FEDERATED_STATE, LABEL):
        and(instances_of(wdeFederatedState, FEDERATED_STATE), rdfsLabel(FEDERATED_STATE, en, LABEL))
    def train_ner(de, federated_state, FEDERATED_STATE, LABEL):
        and(instances_of(wdeFederatedState, FEDERATED_STATE), rdfsLabel(FEDERATED_STATE, de, LABEL))
    def macro(en, federated_states, LABEL):
        and(instances_of(wdeFederatedState, FEDERATED_STATE), rdfsLabel(FEDERATED_STATE, en, LABEL))
    def macro(de, federated_states, LABEL):
        and(instances_of(wdeFederatedState, FEDERATED_STATE), rdfsLabel(FEDERATED_STATE, de, LABEL))
    def answer_federated_state_location_tokens(en, TS, TE):
        and(ner(en, federated_state, TS, TE, C:tokens, FEDERATED_STATE, SCORE), set(C:mem|f1ent, FEDERATED_STATE), r_score(C, SCORE), rdfsLabel(FEDERATED_STATE, en, CLABEL), set(C:context|topic, wdeFederatedState), wdpdCountry(FEDERATED_STATE, COUNTRY), rdfsLabel(COUNTRY, en, CYLABEL), "{CLABEL,s} is a state in {CYLABEL,s}.")
    def answer_federated_state_location_tokens(de, TS, TE):
        and(ner(de, federated_state, TS, TE, C:tokens, FEDERATED_STATE, SCORE), set(C:mem|f1ent, FEDERATED_STATE), r_score(C, SCORE), rdfsLabel(FEDERATED_STATE, de, CLABEL), set(C:context|topic, wdeFederatedState), wdpdCountry(FEDERATED_STATE, COUNTRY), rdfsLabel(COUNTRY, de, CYLABEL), "{CLABEL,s} ist ein Land in {CYLABEL,s}.")
    k.dte.dt('en', u"(what is|what about|what do you know about|where is|in what country is|in|) {federated_states:LABEL} (and you|) (do you know it|do you know that|)?",
                   % inline(answer_federated_state_location_tokens(en, tstart(federated_states), tend(federated_states))))
    k.dte.dt('de', u"(was ist|was ist mit|was weißt Du über|wo ist|wo liegt|in|in welchem Staat ist|in welchem Land ist|) {federated_states:LABEL} (und du|weißt Du das|)?",
                   % inline(answer_federated_state_location_tokens(de, tstart(federated_states), tend(federated_states))))

    k.dte.ts('en', 'd0000', [(u"What is Bavaria?", u"Bavaria is a state in Germany")])
    k.dte.ts('de', 'd0001', [(u"Wo ist Bayern?", u"Bayern ist ein Land in Deutschland.")])

    k.dte.dt('en', u"(and|) (in|) (a|which) state?",
                   [u"Which state comes to mind?",
                    u"Which state do you like best?"])
#    train(en) :- and(context(topic, wdeFederatedState), "(and|) (in|) (a|which) state?", or("The state is {C:mem|f1ent:rdfsLabel|en, s}.", "You mean {C:mem|f1ent:rdfsLabel|en, s}?")).
#    train(en) :- and(context(topic, wdeFederatedState), "(and|) What (is|was) (it|that) (again|)?", or("The state is {C:mem|f1ent:rdfsLabel|en, s}.", "You mean {C:mem|f1ent:rdfsLabel|en, s}?")).
    k.dte.dt('de', u"(und|) (in|) (einem|welchen) Land?",
                   [u"An welches Land denkst Du?",
                    u"Aus welchem Land kommst Du?"])

#    train(de) :- and(context(topic, wdeFederatedState), "(und|) (in einem|in welchem|welches|ein|) Land?", or("Das Land ist {C:mem|f1ent:rdfsLabel|de, s}.", "Du meinst {C:mem|f1ent:rdfsLabel|de, s}?")).
#    train(de) :- and(context(topic, wdeFederatedState), "(und|) Was (ist|war) (das|es) (nochmal|)?", or("Das Land ist {C:mem|f1ent:rdfsLabel|de, s}.", "Du meinst {C:mem|f1ent:rdfsLabel|de, s}?")).
    def answer_federated_state_location_context(en):
        and(mem(C, f1ent, FEDERATED_STATE), rdfsLabel(FEDERATED_STATE, en, CLABEL), wdpdCountry(FEDERATED_STATE, COUNTRY), set(C:mem|f1loc, COUNTRY), set(C:context|topic, wdeFederatedState), rdfsLabel(COUNTRY, en, CYLABEL), "{CLABEL,s} is a state in {CYLABEL,s}.")
    def answer_federated_state_location_context(de):
        and(mem(C, f1ent, FEDERATED_STATE), rdfsLabel(FEDERATED_STATE, de, CLABEL), wdpdCountry(FEDERATED_STATE, COUNTRY), set(C:mem|f1loc, COUNTRY), set(C:context|topic, wdeFederatedState), rdfsLabel(COUNTRY, de, CYLABEL), "{CLABEL,s} ist ein Land in {CYLABEL,s}.")
#    train(en) :- and(context(topic, wdeFederatedState), "(and|) where (is|was) (it|that) (again|)?", inline(answer_federated_state_location_context(en))).
#    train(de) :- and(context(topic, wdeFederatedState), "(und|) Wo (ist|war|liegt) (das|es) (nochmal|)?", inline(answer_federated_state_location_context(de))).
    def answer_federated_state_population_tokens(en, TS, TE):
        and(ner(en, federated_state, TS, TE, C:tokens, FEDERATED_STATE, SCORE), set(C:mem|f1ent, FEDERATED_STATE), r_score(C, SCORE), rdfsLabel(FEDERATED_STATE, en, CLABEL), wdpdPopulation(FEDERATED_STATE, POPULATION), set(C:context|topic, wdeFederatedState), "The population of {CLABEL,s} is {POPULATION,d}.")
    def answer_federated_state_population_tokens(de, TS, TE):
        and(ner(de, federated_state, TS, TE, C:tokens, FEDERATED_STATE, SCORE), set(C:mem|f1ent, FEDERATED_STATE), r_score(C, SCORE), rdfsLabel(FEDERATED_STATE, de, CLABEL), wdpdPopulation(FEDERATED_STATE, POPULATION), set(C:context|topic, wdeFederatedState), "{CLABEL,s} hat {POPULATION,d} Einwohner.")
    k.dte.dt('en', u"(what is the population of |how many people live in | how many humans reside in) {federated_states:LABEL} (do you know it|do you know that|)?",
                   % inline(answer_federated_state_population_tokens(en, tstart(federated_states), tend(federated_states))))
    k.dte.dt('de', u"(wie hoch ist die bevölkerung von|wie ist die bevölkerung von|wie viele menschen leben in|wie viele leute leben in|wie viele Einwohner hat) {federated_states:LABEL} (weißt Du das|)?",
                   % inline(answer_federated_state_population_tokens(de, tstart(federated_states), tend(federated_states))))

    k.dte.ts('en', 's0002', [(u"How many people live in Texas?", u"The population of Texas is 27469114")])
    k.dte.ts('de', 's0003', [(u"Wie viele Menschen leben in Texas?", u"Texas hat 27469114 Einwohner.")])

    def answer_federated_state_population_context(en):
        and(mem(C, f1ent, FEDERATED_STATE), rdfsLabel(FEDERATED_STATE, en, CLABEL), wdpdPopulation(FEDERATED_STATE, POPULATION), set(C:context|topic, wdeFederatedState), "The population of {CLABEL,s} is {POPULATION,d}.")
    def answer_federated_state_population_context(de):
        and(mem(C, f1ent, FEDERATED_STATE), rdfsLabel(FEDERATED_STATE, de, CLABEL), wdpdPopulation(FEDERATED_STATE, POPULATION), set(C:context|topic, wdeFederatedState), "{CLABEL,s} hat {POPULATION,d} Einwohner.")
#    train(en) :- and(context(topic, wdeFederatedState), "(and|) (what is the population of |how many people live in | how many humans reside in) it (do you know it|do you know that|)?", inline(answer_federated_state_population_context(en))).
#    train(en) :- and(context(topic, wdeFederatedState), "(and|) how many residents does it have (do you know it|do you know that|)?", inline(answer_federated_state_population_context(en))).
#    train(en) :- and(context(topic, wdeFederatedState), "(and|) how many people live there (do you know it|do you know that|)?", inline(answer_federated_state_population_context(en))).
#    train(de) :- and(context(topic, wdeFederatedState), "(und|) (wie hoch ist die bevölkerung von|wie ist die bevölkerung von|wie viele menschen leben |wie viele leute leben |wie viele Einwohner hat es) dort (weißt Du das|)?", inline(answer_federated_state_population_context(de))).
    def answer_federated_state_area_tokens(en, TS, TE):
        and(ner(en, federated_state, TS, TE, C:tokens, FEDERATED_STATE, SCORE), set(C:mem|f1ent, FEDERATED_STATE), r_score(C, SCORE), rdfsLabel(FEDERATED_STATE, en, CLABEL), wdpdArea(FEDERATED_STATE, AREA), set(C:context|topic, wdeFederatedState), "The area of {CLABEL,s} is {AREA,d} square kilometers.")
    def answer_federated_state_area_tokens(de, TS, TE):
        and(ner(de, federated_state, TS, TE, C:tokens, FEDERATED_STATE, SCORE), set(C:mem|f1ent, FEDERATED_STATE), r_score(C, SCORE), rdfsLabel(FEDERATED_STATE, de, CLABEL), wdpdArea(FEDERATED_STATE, AREA), set(C:context|topic, wdeFederatedState), "Die Fläche von {CLABEL,s} ist {AREA,d} Quadratkilometer.")
    k.dte.dt('en', u"(what is the area of |how big is|what is the size of) {federated_states:LABEL} (do you know it|do you know that|)?",
                   % inline(answer_federated_state_area_tokens(en, tstart(federated_states), tend(federated_states))))
    k.dte.dt('de', u"(wie groß ist|wie ist die fläche von|wie groß ist die fläche von|wie viele quadratmeter hat) {federated_states:LABEL} (weißt Du das|)?",
                   % inline(answer_federated_state_area_tokens(de, tstart(federated_states), tend(federated_states))))

    k.dte.ts('en', 's0002', [(u"How big is California?", u"The area of California is 423970 square kilometers")])
    k.dte.ts('de', 's0003', [(u"Wie groß ist Kalifornien?", u"Die Fläche von Kalifornien ist 423970 Quadratkilometer.")])

    def answer_federated_state_area_context(en):
        and(mem(C, f1ent, FEDERATED_STATE), rdfsLabel(FEDERATED_STATE, en, CLABEL), wdpdArea(FEDERATED_STATE, AREA), set(C:context|topic, wdeFederatedState), "The area of {CLABEL,s} is {AREA,d} square kilometers.")
    def answer_federated_state_area_context(de):
        and(mem(C, f1ent, FEDERATED_STATE), rdfsLabel(FEDERATED_STATE, de, CLABEL), wdpdArea(FEDERATED_STATE, AREA), set(C:context|topic, wdeFederatedState), "Die Fläche von {CLABEL,s} ist {AREA,d} Quadratkilometer.")
#    train(en) :- and(context(topic, wdeFederatedState), "(and|) (what is the area of |how big is | what is the size of) it (do you know it|do you know that|)?", inline(answer_federated_state_area_context(en))).
#    train(de) :- and(context(topic, wdeFederatedState), "(und|) (wie groß ist es|wie ist die fläche|wie viele quadratmeter hat es|wie groß ist die fläche) (weißt Du das|)?", inline(answer_federated_state_area_context(de))).
    def answer_federated_state_capital_tokens(en, TS, TE):
        and(ner(en, federated_state, TS, TE, C:tokens, FEDERATED_STATE, SCORE), set(C:mem|f1ent, FEDERATED_STATE), r_score(C, SCORE), rdfsLabel(FEDERATED_STATE, en, CLABEL), wdpdCapital(FEDERATED_STATE, CAPITAL), rdfsLabel(CAPITAL, en, CALABEL), set(C:context|topic, wdeFederatedState), "The capital of {CLABEL,s} is {CALABEL,s}.")
    def answer_federated_state_capital_tokens(de, TS, TE):
        and(ner(de, federated_state, TS, TE, C:tokens, FEDERATED_STATE, SCORE), set(C:mem|f1ent, FEDERATED_STATE), r_score(C, SCORE), rdfsLabel(FEDERATED_STATE, de, CLABEL), wdpdCapital(FEDERATED_STATE, CAPITAL), rdfsLabel(CAPITAL, de, CALABEL), set(C:context|topic, wdeFederatedState), "Die Hauptstadt von {CLABEL,s} ist {CALABEL,s}.")
    k.dte.dt('en', u"(what is the|what is the name of the|) capital of {federated_states:LABEL} (do you know it|do you know that|)?",
                   % inline(answer_federated_state_capital_tokens(en, tstart(federated_states), tend(federated_states))))
    k.dte.dt('en', u"what is the name of {federated_states:LABEL}'s capital (do you know it|do you know that|)?",
                   % inline(answer_federated_state_capital_tokens(en, tstart(federated_states), tend(federated_states))))

    k.dte.dt('de', u"(Was|Welches) ist (der Name der|die) Hauptstadt von {federated_states:LABEL} (weißt Du das|)?",
                   % inline(answer_federated_state_capital_tokens(de, tstart(federated_states), tend(federated_states))))
    k.dte.dt('de', u"Wie heißt die Hauptstadt (von|der) {federated_states:LABEL} (weißt Du das|)?",
                   % inline(answer_federated_state_capital_tokens(de, tstart(federated_states), tend(federated_states))))

    k.dte.ts('en', 's0002', [(u"What is the Capital of Bavaria?", u"The capital of Bavaria is Munich")])
    k.dte.ts('de', 's0003', [(u"Welches ist die Hauptstadt von Bayern?", u"Die Hauptstadt von Bayern ist München.")])

    def answer_federated_state_capital_context(en):
        and(mem(C, f1ent, FEDERATED_STATE), rdfsLabel(FEDERATED_STATE, en, CLABEL), wdpdCapital(FEDERATED_STATE, CAPITAL), rdfsLabel(CAPITAL, en, CALABEL), set(C:context|topic, wdeFederatedState), "The capital of {CLABEL,s} is {CALABEL,s}.")
    def answer_federated_state_capital_context(de):
        and(mem(C, f1ent, FEDERATED_STATE), rdfsLabel(FEDERATED_STATE, de, CLABEL), wdpdCapital(FEDERATED_STATE, CAPITAL), rdfsLabel(CAPITAL, de, CALABEL), set(C:context|topic, wdeFederatedState), "Die Hauptstadt von {CLABEL,s} ist {CALABEL,s}.")
#    train(en) :- and(context(topic, wdeFederatedState), "(and|) (what is the|) capital of it (do you know it|do you know that|)?", inline(answer_federated_state_capital_context(en))).
#    train(en) :- and(context(topic, wdeFederatedState), "(and|) what is its capital (do you know it|do you know that|)?", inline(answer_federated_state_capital_context(en))).
#    train(de) :- and(context(topic, wdeFederatedState), "(und|) (was|welches) ist die Hauptstadt (davon|) (weißt Du das|)?", inline(answer_federated_state_capital_context(de))).
    def get_topic_label(C, en, "Countries"):
        and(context(C, topic, wdeFederatedState), r_score(C, 10.0))
    def get_topic_label(C, de, "Staaten"):
        and(context(C, topic, wdeFederatedState), r_score(C, 10.0))
#    train(en) :- and(context(topic, wdeFederatedState), inline(question_what_was_our_topic(en)), r_score(C, 100.0), or(say(C, "We have been talking about {C:mem|f1ent:rdfsLabel|en,s}, I think."), say(C, "Our topic was {C:mem|f1ent:rdfsLabel|en,s}, I believe."), say(C, "Didn't we talk about {C:mem|f1ent:rdfsLabel|en,s}?"))).
#    train(de) :- and(context(topic, wdeFederatedState), inline(question_what_was_our_topic(de)), r_score(C, 100.0), or(say(C, "Wir hatten über {C:mem|f1ent:rdfsLabel|de,s} gesprochen, glaube ich."), say(C, "Ich denke unser Thema war {C:mem|f1ent:rdfsLabel|de,s}."), say(C, "Sprachen wir nicht über {C:mem|f1ent:rdfsLabel|de,s} ?"))).
    k.dte.ts('en', 's0004', [(u"What about Hesse?", u"Hesse is a state in germany"),
                               (u"Which State?", u"The State is Hesse."),
                               (u"What was our topic?", u"We have been talking about Hesse, I think."),
                               (u"How many people live there?", u"The population of Hesse is 6045425"),
                               (u"And where is it again?", u"Hesse is a state in germany"),
                               (u"And what is its capital?", u"The capital of Hesse is Wiesbaden."),
                               (u"And what is the size of it?", u"The area of Hesse is 21100 square kilometers.")])
    k.dte.ts('de', 's0005', [(u"Was ist mit Hessen?", u"Hessen ist ein Land in Deutschland"),
                               (u"Welches Land?", u"Das Land ist Hessen."),
                               (u"Was war unser Thema?", u"Wir hatten über Hessen gesprochen, glaube ich."),
                               (u"Wie viele Menschen leben dort?", u"Hessen hat 6045425 Einwohner."),
                               (u"Und wo ist es nochmal?", u"Hessen ist ein Land in Deutschland"),
                               (u"Und welches ist die Hauptstadt?", u"Die Hauptstadt von Hessen ist Wiesbaden."),
                               (u"Und wie groß ist die Fläche?", u"Die Fläche von Hessen ist 21100 quadratkilometer.")])

    k.dte.dt('en', u"how is {federated_states:LABEL}", u"Not sure if states have feelings?")
    k.dte.dt('de', u"wie ist {federated_states:LABEL}", u"Ich glaube Länder haben keine Gefühle.")

    def answer_federated_state_sure(en, TS, TE):
        and(ner(en, federated_state, TS, TE, C:tokens, FEDERATED_STATE, SCORE), set(C:mem|f1ent, FEDERATED_STATE), r_score(C, SCORE), rdfsLabel(FEDERATED_STATE, en, CLABEL), set(C:context|topic, wdeFederatedState), "Sure, {CLABEL,s}.")
    def answer_federated_state_sure(de, TS, TE):
        and(ner(de, federated_state, TS, TE, C:tokens, FEDERATED_STATE, SCORE), set(C:mem|f1ent, FEDERATED_STATE), r_score(C, SCORE), rdfsLabel(FEDERATED_STATE, de, CLABEL), set(C:context|topic, wdeFederatedState), "Klar, {CLABEL,s}.")
    k.dte.dt('en', u"in {federated_states:LABEL} (maybe|)",
                   % inline(answer_federated_state_sure(en, tstart(federated_states), tend(federated_states))))
    k.dte.dt('de', u"in {federated_states:LABEL} (vielleicht|)",
                   % inline(answer_federated_state_sure(de, tstart(federated_states), tend(federated_states))))

