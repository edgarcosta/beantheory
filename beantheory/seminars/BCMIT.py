# -*- coding: utf-8 -*-
from generic import GenericSeminar
from datetime import timedelta
from cached_property import cached_property
import re

class BCMIT(GenericSeminar):
    url = "https://www2.bc.edu/benjamin-howard/BC-MIT.html"
    name = "BC-MIT number theory seminar"
    label = "BCMIT"
    table_regex = r'<table border="5" cellpadding="10" width="100%">((.|\n)*?)</table>'
    duration = timedelta(hours=1)


    def __init__(self):
        GenericSeminar.__init__(self)
        self.room = self.time = self.place = None

    @cached_property
    def html_talks(self):
        res = []
        for row in self.table:
            if len(row) != 1:
                self.errors.append('Could not parse: {} '.format(row))
                continue

            words = row[0].split()
            day, note = self.parse_day(" ".join(words[:3]))
            i = 3
            if words[3].startswith('(MIT'):
                place = 'MIT'
                room = words[4].rstrip(')')
                i = 5
            elif words[3] == '(BC)':
                place = 'BC'
                room = 'Maloney 560'
                i = 4
            else:
                self.errors.append('Could not parse: {}, 3rd word does not match the possible cases'.format(row[0]))
                continue

            if words[i] != '3:00-4:00:':
                self.errors.append('Could not parse: {}, 3:00-4:00 not where expected'.format(row[0]))
                continue

            talk1 = dict(self.talk_constant)
            talk2 = dict(self.talk_constant)
            for k, t in enumerate([talk1, talk2]):
                if k == 0:
                    t['time'] = day + timedelta(hours=15)
                else:
                    t['time'] = day + timedelta(hours=16, minutes=30)
                t['endtime'] = t['time'] + self.duration
                t['place'] = place 
                t['room'] = room
                t['note'] = note
                t['desc'] = None

            try:
                j = words.index('4:30-5:30:')
            except ValueError:
                self.errors.append('Could not parse: {}, as could not find 4:30-5:30:'.format(row[0]))
                continue
            talk1['speaker'] = " ".join(words[i+1:j]) + ' [BC-MIT]'
            talk2['speaker'] = " ".join(words[j+1:]) + ' [BC-MIT]'
            self.clean_talk(talk1)
            self.clean_talk(talk2)
            res += [talk1, talk2]
        return res






    @cached_property
    def talks(self):
        return self.html_talks

