% prolog

init('config').

%
% FIXME: remove old code below.
%
%    % FIXME: this should probably be the AI's "favourite" station which it tunes in
%    % by default as long as it does not know what the user's favourite station is
%    uriref(wde:Q795291, URI_CHANNEL), context_set(channel, URI_CHANNEL),  % b5 aktuell
%
%    uriref(wde:Q1022, URI_PLACE), context_set(place, URI_PLACE),          % stuttgart

% context_set_default('production', time, today).
% context_set_default('production', channel, URI) :- uriref(wde:Q795291, URI).  % b5 aktuell
% context_set_default('production', place, URI) :- uriref(wde:Q1022, URI).      % stuttgart
% 
% context_set_default('production', me, URI) :- uriref(hal:hal9000,URI).
% 
% context_set_default('production', partner_name, 'Peter').
% context_set_default('production', partner_gender, URI) :- uriref(wde:Male, URI).

