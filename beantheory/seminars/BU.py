# -*- coding: utf-8 -*-
from generic import GenericSeminar
from cached_property import cached_property
import dateutil.parser


class BU(GenericSeminar):
    url = "http://math.bu.edu/research/algebra/seminar.html"
    name = "BU"
    place = "BU"
    room_regex = '(?<= in room )(.+)(?= unless)'
    time_regex = '(?<=talks at )([0-9]+):([0-9]+)(?= in)'
    table_regex = '(?<=<table BORDER=3 CELLSPACING=0 CELLPADDING=8 >)((.|\n)*)(?=</table>)'

    @cached_property
    def talks(self):
        res = []
        # skip header
        for row in self.table[1:]:
            # skip ill formed rows
            if len(row) != 3:
                continue
            # skip TBA speakers
            if 'TBA' in row[1]:
                continue
            if 'no seminar' in (row[1]+row[2]).lower():
                continue
            try:
                day = dateutil.parser.parse(row[0])
            except ValueError:
                continue
            time = day + self.time
            talk = dict(self.talk_constant)
            talk['time'] = time
            talk['speaker'] = row[1]
            talk['desc'] = row[2]
            if 'TBA' in talk['desc']:
                talk['desc'] = None
            res.append(talk)

        return res
