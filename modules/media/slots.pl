%prolog

:- multifile rdfsLabel/3.

rdfsLabel(aiDance, de, 'Dance').
rdfsLabel(aiDance, en, 'Dance').
rdfsLabel(aiMusic, de, 'Musik').
rdfsLabel(aiMusic, en, 'Music').
rdfsLabel(aiNewRock, de, 'New Rock').
rdfsLabel(aiNewRock, en, 'New Rock').
rdfsLabel(aiNews, de, 'Aktuelles').
rdfsLabel(aiNews, en, 'News').
rdfsLabel(aiNewstalk, de, 'Newstalk').
rdfsLabel(aiNewstalk, en, 'Newstalk').
rdfsLabel(aiPop, de, 'Pop').
rdfsLabel(aiPop, en, 'Pop').
rdfsLabel(aiRock, de, 'Rock').
rdfsLabel(aiRock, en, 'Rock').
rdfsLabel(aiTechNews, de, 'Tech News').
rdfsLabel(aiTechNews, en, 'Tech News').
rdfsLabel(aiWorkout, de, 'Workout').
rdfsLabel(aiWorkout, en, 'Workout').
rdfsLabel(wde1046RTL, de, 'RTL').

aiMediaSlot(aiDance, 6).
aiMediaSlot(aiMusic, 3).
aiMediaSlot(aiNewRock, 3).
aiMediaSlot(aiNews, 9).
aiMediaSlot(aiNewstalk, 13).
aiMediaSlot(aiPop, 5).
aiMediaSlot(aiRock, 4).
aiMediaSlot(aiTechNews, 1).
aiMediaSlot(aiWorkout, 15).
aiMediaSlot(wde1046RTL, 8).
aiMediaSlot(wdeB5Aktuell, 9).
aiMediaSlot(wdeDeutschlandfunk, 9).
aiMediaSlot(wdePowerHitRadio, 7).
aiMediaSlot(wdeSWR3, 5).
aiMediaSlot(wdeSWRAktuell, 9).

aiMediaTitle(aiDance, []).
aiMediaTitle(aiMusic, []).
aiMediaTitle(aiNewRock, []).
aiMediaTitle(aiNews, []).
aiMediaTitle(aiNewstalk, []).
aiMediaTitle(aiPop, []).
aiMediaTitle(aiRock, []).
aiMediaTitle(aiTechNews, []).
aiMediaTitle(aiWorkout, []).
aiMediaTitle(wde1046RTL, []).
aiMediaTitle(wdeB5Aktuell, 1).
aiMediaTitle(wdeDeutschlandfunk, 2).
aiMediaTitle(wdePowerHitRadio, []).
aiMediaTitle(wdeSWR3, 6).
aiMediaTitle(wdeSWRAktuell, 9).
