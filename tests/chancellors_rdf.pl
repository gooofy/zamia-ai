% prolog

chancellor (PERSON) :- rdf (PERSON, dbp:office, dbr:Chancellor_of_Germany).
   
is_current_chancellor(PERSON) :- 
    rdf(PERSON, dbp:office, dbr:Chancellor_of_Germany,
        optional(PERSON, dbp:termEnd, END_TIME)),
    END_TIME is [].

