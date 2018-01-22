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

    k.dte.dt('en', u"who is electra", u"The daughter of King Agamemnon and Queen Clytemnestra.")
    k.dte.dt('de', u"wer ist electra", u"Die Tochter des Königs Agamemnon und der Klytaimnestra.")

    k.dte.dt('en', u"what do you know about eva", u"I am not old enough to have known her.")
    k.dte.dt('de', u"was weißt du über eva", u"Ich bin nicht alt genug um sie gekannt zu haben.")

    k.dte.dt('en', u"what do you know about god", u"and promptly vanishes in a puff of logic.")
    k.dte.dt('de', u"was weißt du über gott", u"und löst sich prompt in einen Schwaden aus Logik auf.")

    k.dte.dt('en', u"did you read the bible?", u"never got round to it.")
    k.dte.dt('de', u"hast du die bibel gelesen", u"bin ich nie dazu gekommen.")

