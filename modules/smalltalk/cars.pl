% prolog

% answer(topic, en) :-
%     context_score(topic, cars, 100, SCORE), say_eoa(en, 'We were talking about cars.', SCORE).
% answer(topic, de) :-
%     context_score(topic, cars, 100, SCORE), say_eoa(de, 'Wir hatten das Thema Autos.', SCORE).

nlp_gens("smalltalk", en, [["oh dear"," i was driving my "," ich am worried about my "," i need a new "," cool, a"],["new",""],["vehicle","car","truck","sportscar"]], "Welche Marke?").
nlp_gens("smalltalk", de, [["ohje, mein "," ich fuhr mit dem "," ich mache mir sorgen um mein "," ich brauche ein neues "," cool, ein"],["Auto","Wagen","Kraftfahrzeug","Sportwagen"]], "Welche Marke?").
nlp_gens("smalltalk", en, [["I will drive","I will go by","I will take the","they will take the","they will drive by"],"car"], "No good for the environment").
nlp_gens("smalltalk", de, [["ich werde","ich will nicht","ich will mit dem","sie werden","sie werden mit dem"],"auto fahren"], "Schade für die Umwelt").
nlp_gens("smalltalk", en, [["those masses of",""],"cars are",["a problem","a plague","a burden on the environment","a burden"]], "Luckily we do have lots of alternative methods of transpor nowadays").
nlp_gens("smalltalk", de, [["die vielen",""],"autos sind",["ein problem","eine plage","eine belastung für die umwelt"]], "Zum Glück gibt es schon heute viele Alternativen zum Auto.").


