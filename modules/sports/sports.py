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

    k.dte.dt('en', u"(I am a fan of|i like) (hertha|vfl bochum)", u"nobody is perfect.")
    k.dte.dt('de', u"(ich mag|ich bin fan von) (hertha|vfl bochum)", u"niemand ist perfekt.")

    k.dte.dt('en', u"(I like|) (golf|soccer|swimming|football)", u"Physical activity is important for humans, I've heard.")
    k.dte.dt('de', u"ich mag (golf|fussball|football|schwimmen)", u"Bewegung ist wichtig für Menschen, habe ich gehört.")

    k.dte.dt('en', u"What about golf?", u"I will not crack that joke here.")
    k.dte.dt('de', u"wie ist es mit golf", u"Ich bringe jetzt nicht den Witz dazu.")

