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
#

def get_data(k):

    k.dte.set_prefixes([u''])

    # NER, macros

    for lang in ['en', 'de']:
        for res in k.prolog_query("aiMediaSlot(STATION, SLOT), rdfsLabel(STATION, %s, LABEL)." % lang):
            s_station = res[0] 
            s_label   = res[2] 
            k.dte.ner(lang, 'media_station', s_station, s_label)
            k.dte.macro(lang, 'media_stations', {'LABEL': s_label})

    def change_media_station(c, ts, te):

        def act(c, station):
            c.kernal.mem_set(c.realm, 'action', 'media_on')
            c.kernal.mem_push(c.user, 'f1ent', station)
            c.kernal.mem_push(c.user, 'station', station)

        if ts>=0:
            mss = c.ner(c.lang, 'media_station', ts, te)
        else:
            mss = c.kernal.mem_get_multi(c.user, 'station')
            if not mss:
                s = c.kernal.prolog_query_one("favStation(self, X).")
                mss = [(s, 1.0)]

        for station, score in mss:
            c.resp(u"", score=score, action=act, action_arg=station)

    k.dte.dt('en', u"(please|) (switch|turn|tune) (to|on|into) {media_stations:LABEL}",
                   change_media_station, ['media_stations_0_start', 'media_stations_0_end'])
    k.dte.dt('de', u"(schalte|mach|stell) (bitte|) (mal|) {media_stations:LABEL} (an|ein)",
                   change_media_station, ['media_stations_0_start', 'media_stations_0_end'])

    k.dte.dt('en', u"(please|) (switch|turn|tune) (to|on|into) (the radio|the music|media|the media player)",
                   change_media_station, [-1, -1])
    k.dte.dt('de', u"(schalte|mach|stell) (bitte|) (mal|) (das radio|musik|die musik|ein bischen musik|die unterhaltung|den media player) (an|ein)",
                   change_media_station, [-1, -1])

    def media_station_off(c):
        def act(c):
            c.kernal.mem_set(c.realm, 'action', 'media_off')
        c.resp(u"", score=1.0, action=act)

    k.dte.dt('en', u"(please|) (switch|turn|tune) off (the radio|the music|media|the media player)",
                   media_station_off)
    k.dte.dt('de', u"(schalte|mach|stell) (bitte|) (mal|) (das radio|musik|die musik|ein bischen musik|die unterhaltung|den media player) (aus|still)",
                   media_station_off)

    def check_media (c, args):
        action, station = args
        assert c.kernal.mem_get(c.realm, 'action') == action
        if station:
            # import pdb; pdb.set_trace()
            s1, score = c.kernal.mem_get_multi(c.user, 'station')[0] 
            assert s1 == station
        
    k.dte.ts('en', 't0002', [(u"please switch on the radio", u"", check_media, ['media_on', 'wdeB5Aktuell'])])
    k.dte.ts('de', 't0003', [(u"schalte bitte das Radio ein", u"", check_media, ['media_on', 'wdeB5Aktuell'])])

    k.dte.ts('en', 't0004', [(u"please tune into new rock", u"",  check_media, ['media_on', 'aiNewRock'])])
    k.dte.ts('de', 't0005', [(u"schalte bitte new rock ein", u"", check_media, ['media_on', 'aiNewRock'])])

    k.dte.ts('en', 't0006', [(u"turn off the radio", u"", check_media, ['media_off', None])])
    k.dte.ts('de', 't0007', [(u"mach das radio aus", u"", check_media, ['media_off', None])])

    k.dte.ts('en', 't0008', [(u"please switch on new rock", u"", check_media, ['media_on', 'aiNewRock']),
                             (u"switch off the radio", u"", check_media, ['media_off', None]),
                             (u"please turn on the radio", u"", check_media, ['media_on', 'aiNewRock'])])
    k.dte.ts('de', 't0009', [(u"schalte bitte new rock ein", u"", check_media, ['media_on', 'aiNewRock']),
                             (u"mach das radio aus", u"", check_media, ['media_off', None]),
                             (u"schalte bitte das radio ein", u"", check_media, ['media_on', 'aiNewRock'])])

    k.dte.dt('en', [u"My radio is on",
                    u"I am listening to the radio"],
                   [u"Which station?",
                    u"I will try to filter out the baground noise."])
    k.dte.dt('de', [u"ich habe radio an",
                    u"ich höre radio"],
                   [u"Welches Programm?",
                    u"Ich werde versuchen, die Hintergrundgeräusche auszufiltern."])

