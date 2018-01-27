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

    # NER, macros

    for lang in ['en', 'de']:
        for res in k.prolog_query("aiHomeLocation(HOME_LOCATION), rdfsLabel(HOME_LOCATION, %s, LABEL), aiPrepLoc(HOME_LOCATION, %s, PL)." % (lang, lang)):
            s_loc   = res[0] 
            s_label = res[1]
            s_pl    = res[2]
            k.dte.ner(lang, 'home_location', s_loc, s_label)
            k.dte.macro(lang, 'home_locations', {'LABEL': s_label, 'PL': s_pl})

    k.dte.macro('en', 'light_actions', {'LABEL':  'on', 'ACTION': 'light_on'})
    k.dte.macro('en', 'light_actions', {'LABEL': 'off', 'ACTION': 'light_off'})
    k.dte.macro('de', 'light_actions', {'LABEL':  'an', 'ACTION': 'light_on'})
    k.dte.macro('de', 'light_actions', {'LABEL': 'ein', 'ACTION': 'light_on'})
    k.dte.macro('de', 'light_actions', {'LABEL': 'aus', 'ACTION': 'light_off'})

    def turn_lights(c, ts, te, laction):

        def act(c, args):
            laction, loc = args
            c.kernal.mem_set(c.realm, 'action', laction)
            c.kernal.mem_push(c.user, 'f1loc', loc)

        if ts>=0:
            hss = c.ner(c.lang, 'home_location', ts, te)
        else:
            hss = c.kernal.mem_get_multi(c.user, 'f1loc')

        for loc, score in hss:
            c.resp(u"", score=score, action=act, action_arg=(laction, loc) )

    k.dte.dt('en', u"(please|) (switch|turn|dim) {light_actions:LABEL} the lights {home_locations:PL} {home_locations:LABEL}",
                   turn_lights, ['home_locations_0_start', 'home_locations_0_end', 'light_actions_0_action'])
    k.dte.dt('de', u"(bitte|) (schalte|mach) (bitte|) (mal|) das Licht {home_locations:PL} {home_locations:LABEL} {light_actions:LABEL}",
                   turn_lights, ['home_locations_0_start', 'home_locations_0_end', 'light_actions_0_action'])

    def check_light (c, args):
        action, loc = args
        assert c.kernal.mem_get(c.realm, 'action') == action
        l1, score = c.kernal.mem_get_multi(c.user, 'f1loc')[0] 
        assert l1 == loc
        
    k.dte.ts('en', 't0000', [(u"computer, please switch on the lights in the living room", u"", check_light, ['light_on', 'aiHLLivingRoom'])])
    k.dte.ts('de', 't0001', [(u"Computer, bitte schalte das Licht in der Werkstatt ein", u"", check_light, ['light_on', 'aiHLWorkshop'])])

    k.dte.ts('en', 't0004', [(u"computer, please switch off the lights in the dining room", u"", check_light, ['light_off', 'aiHLDiningRoom'])])
    k.dte.ts('de', 't0005', [(u"Computer, schalte mal das Licht im Schlafzimmer aus", u"", check_light, ['light_off', 'aiHLBedroom'])])

    k.dte.dt('en', u"(please|) lights {light_actions:LABEL} {home_locations:PL} {home_locations:LABEL}",
                   turn_lights, ['home_locations_0_start', 'home_locations_0_end', 'light_actions_0_action'])
    k.dte.dt('de', u"(bitte|) Licht {light_actions:LABEL} {home_locations:PL} {home_locations:LABEL}",
                   turn_lights, ['home_locations_0_start', 'home_locations_0_end', 'light_actions_0_action'])

    k.dte.ts('en', 't0002', [(u"computer, lights on in the kitchen", u"", check_light, ['light_on', 'aiHLKitchen'])])
    k.dte.ts('de', 't0003', [(u"Licht an im Keller", u"", check_light, ['light_on', 'aiHLBasement'])])

    k.dte.dt('en', u"(please|) lights {light_actions:LABEL} (please|)",
                   turn_lights, [-1, -1, 'light_actions_0_action'])
    k.dte.dt('de', u"(bitte|) Licht {light_actions:LABEL} (bitte|)",
                   turn_lights, [-1, -1, 'light_actions_0_action'])

    k.dte.dt('en', u"(please|) (switch|turn|dim) {light_actions:LABEL} the lights",
                   turn_lights, [-1, -1, 'light_actions_0_action'])
    k.dte.dt('de', u"(bitte|) (schalte|mach) (bitte|) (mal|) das Licht {light_actions:LABEL}",
                   turn_lights, [-1, -1, 'light_actions_0_action'])

    k.dte.ts('en', 't0006', [(u"computer lights on in the living room", u"", check_light, ['light_on', 'aiHLLivingRoom']),
                             (u"switch on the lights in the attic", u"", check_light, ['light_on', 'aiHLAttic']),
                             (u"please turn off the lights", u"", check_light, ['light_off', 'aiHLAttic'])])
    k.dte.ts('de', 't0007', [(u"computer licht an im Wohnzimmer", u"", check_light, ['light_on', 'aiHLLivingRoom']),
                             (u"schalte das licht auf dem dachboden ein", u"", check_light, ['light_on', 'aiHLAttic']),
                             (u"bitte schalte das licht aus", u"", check_light, ['light_off', 'aiHLAttic'])])

