#!/usr/bin/env python
# -*- coding: utf-8 -*- 

#
# Copyright 2016, 2017, 2018 Guenter Bartsch
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

DEPENDS     = [ 'config', 'data', 'base', 'dialog', 'tech' ]

import culture
import humor
import lang
import mythology
import name
import opinion
import personal
import food
import private
import rec
import social
import user

def get_data(k):
    culture.get_data(k)
    humor.get_data(k)
    lang.get_data(k)
    mythology.get_data(k)
    name.get_data(k)
    opinion.get_data(k)
    personal.get_data(k)
    food.get_data(k)
    private.get_data(k)
    rec.get_data(k)
    social.get_data(k)
    user.get_data(k)

