% prolog

set_context_default('production', time, today).
set_context_default('production', channel, URI) :- uriref(wde:Q795291, URI).
set_context_default('production', place, URI) :- uriref(wde:Q1022, URI).

