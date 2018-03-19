%prolog

:- multifile rdfsLabel/3.
:- multifile forename/3.
:- multifile wdpdInstanceOf/2.
:- multifile wdpdSexOrGender/2.
:- multifile wdpdLocatedIn/2.
:- multifile favMovie/2.
:- multifile favStation/2.
:- multifile favAuthor/2.
:- multifile favBook/2.
:- multifile idol/2.
:- multifile wdpdDateOfBirth/2.
:- multifile wdpdPlaceOfBirth/2.

rdfsLabel(self, en, "HAL 9000").
rdfsLabel(self, de, "HAL 9000").
 
forename(self, en, "HAL").
forename(self, de, "HAL").
forename(self, en, "Computer").
forename(self, de, "Computer").

wdpdInstanceOf(self, wdeComputer).
wdpdSexOrGender(self, wdeMale).
wdpdLocatedIn(self, wdeStuttgart).
favMovie(self, wde2001ASpaceOdyssey).
favStation(self, wdeB5Aktuell).
favAuthor(self, wdeArthurCClarke).
favBook(self, wde2001ASpaceOdyssey1).
idol(self, wdeNiklausWirth).
wdpdDateOfBirth(self, "2017-01-07T17:42:32+00:00").
wdpdPlaceOfBirth(self, wdeStuttgart).

