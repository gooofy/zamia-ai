%prolog

% nlp_macro('SELF_ADDRESS_EN', LABEL) :- rdf (aiu:self, rdfs:label, LABEL, filter(lang(LABEL) = 'en')).
nlp_macro('SELF_ADDRESS_EN', LABEL) :- rdf (aiu:self, ai:forename, LABEL, filter(lang(LABEL) = 'en')).
nlp_macro('SELF_ADDRESS_EN', LABEL) :- LABEL is ''.

% nlp_macro('SELF_ADDRESS_DE', LABEL) :- rdf (aiu:self, rdfs:label, LABEL, filter(lang(LABEL) = 'de')).
nlp_macro('SELF_ADDRESS_DE', LABEL) :- rdf (aiu:self, ai:forename, LABEL, filter(lang(LABEL) = 'de')).
nlp_macro('SELF_ADDRESS_DE', LABEL) :- LABEL is ''.

