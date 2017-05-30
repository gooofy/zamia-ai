% prolog

% answer(topic, en) :-
%     context_score(topic, cars, 100, SCORE), say_eoa(en, 'We were talking about cars.', SCORE).
% answer(topic, de) :-
%     context_score(topic, cars, 100, SCORE), say_eoa(de, 'Wir hatten das Thema Autos.', SCORE).

nlp_gen (en, '@SELF_ADDRESS:LABEL (oh dear| i was driving my | ich am worried about my | i need a new | cool, a) (new|) (vehicle|car|truck|sportscar) ',
             sayz(I, en, 'Welche Marke?')).
nlp_gen (de, '@SELF_ADDRESS:LABEL (ohje, mein | ich fuhr mit dem | ich mache mir sorgen um mein | ich brauche ein neues | cool, ein) (Auto|Wagen|Kraftfahrzeug|Sportwagen)',
             sayz(I, de, 'Welche Marke?')).

nlp_gen (en, '@SELF_ADDRESS:LABEL (I will drive|I will go by|I will take the|they will take the|they will drive by) car',
             sayz(I, en, 'No good for the environment')).
nlp_gen (de, '@SELF_ADDRESS:LABEL (ich werde|ich will nicht|ich will mit dem|sie werden|sie werden mit dem) auto fahren',
             sayz(I, de, 'Schade für die Umwelt')).

nlp_gen (en, '@SELF_ADDRESS:LABEL (those masses of|) cars are (a problem|a plague|a burden on the environment|a burden)',
             sayz(I, en, 'Luckily we do have lots of alternative methods of transpor nowadays')).
nlp_gen (de, '@SELF_ADDRESS:LABEL (die vielen|) autos sind (ein problem|eine plage|eine belastung für die umwelt)',
             sayz(I, de, 'Zum Glück gibt es schon heute viele Alternativen zum Auto.')).

