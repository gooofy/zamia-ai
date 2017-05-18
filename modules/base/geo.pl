%prolog

%
% very basic geo location predicates
%

geo_location_category (CAT) :- CAT is uriref(wde:City).
geo_location_category (CAT) :- CAT is uriref(wde:Municipality).
geo_location_category (CAT) :- CAT is uriref(wde:GeographicRegion).
geo_location_category (CAT) :- CAT is uriref(wde:MunicipalityOfGermany).
geo_location_category (CAT) :- CAT is uriref(wde:HumanSettlement).
geo_location_category (CAT) :- CAT is uriref(wde:BigCity).
geo_location_category (CAT) :- CAT is uriref(wde:GeographicLocation).
geo_location_category (CAT) :- CAT is uriref(wde:Location).
geo_location_category (CAT) :- CAT is uriref(wde:BigCity).

%
% named entity recognition (NER)
%

ner_learn_geo_locations(LANG) :-
    atom_chars(LANG, LSTR),

    geo_location_category(CAT),

    % log(info, format_str('learning geo location category %s', CAT)),

    rdf_lists (distinct,
               GEO_LOCATIONS, wdpd:InstanceOf,   CAT,
               GEO_LOCATIONS, rdfs:label,        GEO_LOCATION_LABELS,
               filter (lang(GEO_LOCATION_LABELS) = LSTR)),

    ner_learn(LANG, geo_location, GEO_LOCATIONS, GEO_LOCATION_LABELS).

init('base') :-
    ner_learn_geo_locations(en),
    ner_learn_geo_locations(de).

