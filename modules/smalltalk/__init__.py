#!/usr/bin/env python
# -*- coding: utf-8 -*- 

#
# Copyright 2016, 2017 Guenter Bartsch
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
# 
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

from greetings  import nlp_smalltalk_greetings_train  , nlp_smalltalk_greetings_test
# from psychology import nlp_smalltalk_psychology_train , nlp_smalltalk_psychology_test
# from cars       import nlp_smalltalk_cars_train       , nlp_smalltalk_cars_test
# from sex        import nlp_smalltalk_sex_train        , nlp_smalltalk_sex_test
# from music      import nlp_smalltalk_music_train      , nlp_smalltalk_music_test
# from health     import nlp_smalltalk_health_train     , nlp_smalltalk_health_test
# from humor      import nlp_smalltalk_humor_train      , nlp_smalltalk_humor_test
# from languages  import nlp_smalltalk_languages_train  , nlp_smalltalk_languages_test
# from religion   import nlp_smalltalk_religion_train   , nlp_smalltalk_religion_test
# from social     import nlp_smalltalk_social_train     , nlp_smalltalk_social_test
# from astro      import nlp_smalltalk_astro_train      , nlp_smalltalk_astro_test
# from geo        import nlp_smalltalk_geo_train        , nlp_smalltalk_geo_test

DEPENDS    = [ 'base' ]

KB_SOURCES = [
             ]

def nlp_train (kernal):

    res = []

    res = nlp_smalltalk_greetings_train(kernal, res)
    # nlp_smalltalk_psychology_train(kernal, res)
    # nlp_smalltalk_cars_train(kernal, res)
    # nlp_smalltalk_sex_train(kernal, res)
    # nlp_smalltalk_music_train(kernal, res)
    # nlp_smalltalk_health_train(kernal, res)
    # nlp_smalltalk_humor_train(kernal, res)
    # nlp_smalltalk_languages_train(kernal, res)
    # nlp_smalltalk_religion_train(kernal, res)
    # nlp_smalltalk_social_train(kernal, res)
    # nlp_smalltalk_astro_train(kernal, res)
    # nlp_smalltalk_geo_train(kernal, res)

    return res

def nlp_test (kernal):

    res = []

    nlp_smalltalk_greetings_test(kernal, res)
    # nlp_smalltalk_psychology_test(kernal, res)
    # nlp_smalltalk_cars_test(kernal, res)
    # nlp_smalltalk_sex_test(kernal, res)
    # nlp_smalltalk_music_test(kernal, res)
    # nlp_smalltalk_health_test(kernal, res)
    # nlp_smalltalk_humor_test(kernal, res)
    # nlp_smalltalk_languages_test(kernal, res)
    # nlp_smalltalk_religion_test(kernal, res)
    # nlp_smalltalk_social_test(kernal, res)
    # nlp_smalltalk_astro_test(kernal, res)
    # nlp_smalltalk_geo_test(kernal, res)

    return res
