%prolog

test_setup('base').

% nlp_macro('SELF_ADDRESS_EN', LABEL) :- rdf (aiu:self, rdfs:label, LABEL, filter(lang(LABEL) = 'en')).
nlp_macro('SELF_ADDRESS_EN', LABEL) :- rdf (aiu:self, ai:forename, LABEL, filter(lang(LABEL) = 'en')).
nlp_macro('SELF_ADDRESS_EN', LABEL) :- LABEL is ''.

% NE: not empty
nlp_macro('SELF_ADDRESS_EN_NE', LABEL) :- rdf (aiu:self, ai:forename, LABEL, filter(lang(LABEL) = 'en')).

% nlp_macro('SELF_ADDRESS_DE', LABEL) :- rdf (aiu:self, rdfs:label, LABEL, filter(lang(LABEL) = 'de')).
nlp_macro('SELF_ADDRESS_DE', LABEL) :- rdf (aiu:self, ai:forename, LABEL, filter(lang(LABEL) = 'de')).
nlp_macro('SELF_ADDRESS_DE', LABEL) :- LABEL is ''.

% NE: not empty
nlp_macro('SELF_ADDRESS_DE_NE', LABEL) :- rdf (aiu:self, ai:forename, LABEL, filter(lang(LABEL) = 'de')).

