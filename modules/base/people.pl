%prolog

is_male(PERSON) :- rdf (PERSON, wdpd:SexOrGender, wde:Male).
is_female(PERSON) :- rdf (PERSON, wdpd:SexOrGender, wde:Female). 

is_german_chancellor(PERSON) :- 
    rdf(PERSON,      wdp:PositionHeld,  OFFICE_STMT,  
        OFFICE_STMT, wdps:PositionHeld, wde:FederalChancellorOfGermany, 
        optional(OFFICE_STMT, wdpq:EndTime, END_TIME),
        filter(END_TIME is []), limit(1)).

was_german_chancellor(PERSON) :- 
    rdf(limit(1),
        PERSON,      wdp:PositionHeld,  OFFICE_STMT,  
        OFFICE_STMT, wdps:PositionHeld, wde:FederalChancellorOfGermany).

% rdf_macro ('KNOWN_PERSONS', 
%            distinct,
%            PERSON, wdpd:InstanceOf,   wde:Human,
%            PERSON, rdfs:label,        LABEL,
%            PERSON, wdpd:PositionHeld, wde:FederalChancellorOfGermany,
%            filter (lang(LABEL) = 'de')).

nlp_macro ('KNOWN_PERSONS', PERSON, LABEL) :-
    rdf (distinct,
         PERSON, wdpd:InstanceOf,   wde:Human,
         PERSON, rdfs:label,        LABEL,
         PERSON, wdpd:PositionHeld, wde:FederalChancellorOfGermany,
         filter (lang(LABEL) = 'de')).

answer (knownPerson, de, PERSON, LABEL) :-
    
    is_german_chancellor(PERSON),
    is_male(PERSON),
    say_eoa(de, 'Der ist doch gerade Bundeskanzler!').

answer (knownPerson, de, PERSON, LABEL) :-
    is_german_chancellor(PERSON),
    is_female(PERSON),
    say_eoa(de, 'Die ist doch gerade Bundeskanzlerin!').

answer (knownPerson, de, PERSON, LABEL) :-
    was_german_chancellor(PERSON), 
    not (is_german_chancellor(PERSON)),
    is_male(PERSON),
    say_eoa(de, 'Der war doch mal Bundeskanzler.').

answer (knownPerson, de, PERSON, LABEL) :-
    was_german_chancellor(PERSON), 
    not (is_german_chancellor(PERSON)),
    is_female(PERSON),
    say_eoa(de, 'Die war doch mal Bundeskanzlerin.').

nlp_gen (de, '(HAL,|Computer,|) (kennst du|wer ist) (eigentlich|) @KNOWN_PERSONS:LABEL',
             answer(knownPerson, de, '@KNOWN_PERSONS:PERSON', "@KNOWN_PERSONS:LABEL")). 

nlp_test(de,
         ivr(in('Computer, kennst du eigentlich Angela Merkel?'),
             out('die ist doch gerade bundeskanzler'))).

nlp_test(de,
         ivr(in('Computer, kennst du eigentlich Helmut Kohl?'),
             out('der war doch mal Bundeskanzler.'))).


% sparql_macro ('GERMAN_CHANCELLORS', "SELECT DISTINCT ?label ?birthPlaceLabel ?wdgender
%                                      WHERE {
%                                       ?chancellor wdt:P31 wd:Q5. # instanceof human
%                                       ?chancellor wdt:P19 ?birthPlace. # place of birth
%                                       ?chancellor rdfs:label ?label.
%                                       ?birthPlace rdfs:label ?birthPlaceLabel.
%                                       ?chancellor wdt:P21 ?wdgender.
%                                       ?chancellor wdt:P39 wd:Q4970706.
%                                       FILTER (lang(?label) = 'de')
%                                       FILTER (lang(?birthPlaceLabel) = 'de')
%                                      }
%                                     ", LABEL, BIRTHPLACELABEL, GENDER).
% 
% nlp_gen (de, '(HAL,|Computer,|) (kennst du|wer ist) (eigentlich|) @GERMAN_CHANCELLORS:LABEL',
%              '@GERMAN_CHANCELLORS:GENDER' is 'http://www.wikidata.org/entity/Q6581097', 'Ja klar, war oder ist der nicht Bundeskanzler?', or,
%              '@GERMAN_CHANCELLORS:GENDER' is 'http://www.wikidata.org/entity/Q6581072', 'Ja klar, war oder ist die nicht Bundeskanzlerin?').


% nlp_gen (de, '(HAL,|Computer,|) kennst du helmut kohl',
%              'Das ist doch der ehemalige Bundeskanzler, der Vorgaenger von Gerhard Schroeder, oder?').

% sparql_macro ('PERSON_BP', "SELECT DISTINCT ?label ?birthPlace 
%                             WHERE {
%                                 ?chancellor rdfs:label ?label.
%                                 ?chancellor dbo:birthPlace ?birthPlace.
%                                 ?chancellor rdf:type schema:Person.
%                                 ?birthPlace rdf:type dbo:Settlement.
%                                 FILTER (lang(?label) = 'de')
%                             }", L, BP).
% 
% nlp_gen (de, '(HAL,|Computer,|) (wo|in welcher stadt|in welchem ort) (wurde|ist) (eigentlich|) @PERSON_BP:L geboren?',
%              'In @PERSON_BP:BP', 'Ich glaube in @PERSON_BP:BP' ).


% <?xml version='1.0' encoding='utf8'?>',
% <ns0:template',
%  xmlns:ns0="http://alicebot.org/2001/AIML-1.0.1"',
% >',
% Momentan ist ',
% <ns0:set',
%  name="er"',
% >',
% Gerhard Schroeder',
% </ns0:set>',
%  Bundeskanzler.',
% </ns0:template>',
% ',
% nlp_gen (de, '(HAL,|Computer,|) WER IST GERHARD SCHROEDER',
%              'Momentan ist Gerhard Schroeder  Bundeskanzler.').

% <?xml version='1.0' encoding='utf8'?>',
% <ns0:template',
%  xmlns:ns0="http://alicebot.org/2001/AIML-1.0.1"',
% >',
% <ns0:set',
%  name="er"',
% >',
% Helmut Kohl',
% </ns0:set>',
%  ist der Vorgaenger von Gerhard Schroeder.',
% </ns0:template>',
% ',
% nlp_gen (de, '(HAL,|Computer,|) WER IST HELMUT KOHL',
%              'Helmut Kohl  ist der Vorgaenger von Gerhard Schroeder.').

% nlp_gen (de, '(HAL,|Computer,|) ueber aussenpolitik',
%              'Politik interessiert mich nicht sonderlich.').
% 
% nlp_gen (de, '(HAL,|Computer,|) kennst du dich mit politik aus',
%              'Ich schaue mir manchmal eine Bundestagsdebatte an, wenn ich etwas zum Lachen haben will...').

