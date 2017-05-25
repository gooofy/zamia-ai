%prolog

%
% if we do not have a msg frame, use a previous one
%
l3proc (I, F, fnRequest) :-

    uriref (aiu:self, SELF),
    frame (F, add, SELF),
    not (frame (F, msg, MSGF)),

    context_search_l2(I, I, 100, 25, uframe, fnRequest, L1FRAME, msg, MSGFT, MSGF),

    assertz(frame(F, msg, MSGF)),

    l3proc (I, F, fnRequest, MSGF, MSGFT).

%
% map request with known msg frame to 2-layer l3proc search
%

l3proc (I, F, fnRequest) :-

    uriref (aiu:self, SELF),
    frame (F, add, SELF),

    % look for message frame + type, run l3proc on it

    frame(F, msg, MSGF),
    frame(MSGF, type, MSGFT),

    l3proc (I, F, fnRequest, MSGF, MSGFT).

