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

def get_data(k):

    k.dte.set_prefixes([u''])

    k.dte.dt('en', u"Constitution.", u"Very important.")
    k.dte.dt('de', u"(Die Verfassung|Das Grundgesetz).", u"Sehr wichtig.")

    k.dte.dt('en', u"Do you know a lawyer?", u"You think I need one?")
    k.dte.dt('de', u"Kennst du einen Anwalt?", u"Denkst Du, ich brauche einen?")

