% prolog

set_context_default('production', time, today).
set_context_default('production', channel, URI) :- uriref(wde:Q795291, URI).  % b5 aktuell
set_context_default('production', place, URI) :- uriref(wde:Q1022, URI).      % stuttgart

set_context_default('production', myname, 'HAL').
set_context_default('production', myfavmovie, URI) :- uriref(wde:Q103474, URI). % 2001: A Space Odyssey

set_context_default('production', partner_name, 'Peter').
set_context_default('production', partner_gender, URI) :- uriref(wde:Male, URI).

