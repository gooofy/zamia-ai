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

def get_data(k):

    k.dte.set_prefixes([u'{self_address:W} '])

    k.dte.dt('en', u"(isn't that a wonderful|wonderful|a very nice|terrible) language",
                   [u"do you speak any foreign languages?",
                    u"du you like foreign languages?"])
    k.dte.dt('de', u"(ist das nicht eine wunderbare|wunderbare|eine sehr schöne|furchtbare) sprache",
                   [u"Sprichst Du irgendwelche Fremdsprachen?",
                    u"Magst Du Fremdsprachen?"])

    k.dte.ts('en', 't0100', [(u"terrible language", u"do you speak any foreign languages?")])
    k.dte.ts('de', 't0101', [(u"wunderbare sprache", u"Magst Du Fremdsprachen?")])

