% prolog

context_set_default('production', time, today).
context_set_default('production', channel, URI) :- uriref(wde:Q795291, URI).  % b5 aktuell
context_set_default('production', place, URI) :- uriref(wde:Q1022, URI).      % stuttgart

context_set_default('production', me, URI) :- uriref(hal:hal9000,URI).

context_set_default('production', partner_name, 'Peter').
context_set_default('production', partner_gender, URI) :- uriref(wde:Male, URI).

