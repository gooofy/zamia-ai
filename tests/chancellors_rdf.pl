% prolog

chancellor (PERSON) :- rdf (PERSON, dbp:office, dbr:Chancellor_of_Germany).
   
is_current_chancellor(PERSON) :- 
    rdf(PERSON, dbp:office, dbr:Chancellor_of_Germany,
        optional(PERSON, dbp:termEnd, END_TIME)),
    END_TIME is [].

chancellor_labels (PERSON, LABEL) :- rdf (PERSON, dbp:office, dbr:Chancellor_of_Germany,
                                          PERSON, rdfs:label, LABEL,
                                          filter (lang(LABEL) = 'de')).

