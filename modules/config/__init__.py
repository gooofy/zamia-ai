#!/usr/bin/env python
# -*- coding: utf-8 -*- 

#
# Copyright 2018 Guenter Bartsch
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


DEPENDS     = [ 'data' ]

PL_SOURCES  = [
               'config'
              ]

def get_data(kernal):

    #
    # name / self address utils
    #
    
    for soln in kernal.prolog_query('forename(self, L, W).'):
        kernal.dte.macro(soln[0].name, 'my_forename',  {'W': soln[1].value})
        kernal.dte.macro(soln[0].name, 'self_address', {'W': soln[1].value + ', '})
 
    kernal.dte.macro('en', 'self_address', {'W': ''})
    kernal.dte.macro('de', 'self_address', {'W': ''})

