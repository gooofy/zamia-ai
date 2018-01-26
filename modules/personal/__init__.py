#!/usr/bin/env python
# -*- coding: utf-8 -*- 

#
# Copyright 2016, 2017, 2018 Guenter Bartsch
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

DEPENDS     = [ 'config', 'data', 'base', 'dialog', 'tech' ]

import culture
import humor
import lang
import mythology
# import name
import opinion
import personal
import food
# import private
# import rec
# import social
# import user

def get_data(k):
    culture.get_data(k)
    humor.get_data(k)
    lang.get_data(k)
    mythology.get_data(k)
#     name.get_data(k)
    opinion.get_data(k)
    personal.get_data(k)
    food.get_data(k)
#     private.get_data(k)
#     rec.get_data(k)
#     social.get_data(k)
#     user.get_data(k)

