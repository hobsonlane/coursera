central_france :- paris.
cold5 :- paris.
overcast_skies :- paris.
drizzling_rain :- central_france.
brittany :- nantes.
dry :- brittany.
mild15 :- nantes.
sunny :- nantes.
city_walk :-
 dry, clear_skies, mild15, sunny.
nantes :- fast_train.
fast_train.
paris :- false.

?- city_walk, \+drizzling_rain.
