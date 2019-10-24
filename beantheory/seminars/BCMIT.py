# -*- coding: utf-8 -*-
from generic import GenericSeminar
from datetime import timedelta
from cached_property import cached_property

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
        def parse_room(i, words):
            roomw = []
            for j, w in enumerate(words[i:]):
                roomw.append(w.rstrip(')'))
                if w.endswith(')'):
                    return i + j + 1, " ".join(roomw)
            return None, None
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
                i, room = parse_room(4, words)
            elif words[3].startswith('(BC'):
                place = 'BC'
                if words[3] == '(BC)':
                    room = 'Maloney 560'
                    i = 4
                else:
                    i, room = parse_room(4, words)
            else:
                self.errors.append('Could not parse: {}, 3rd word does not match the possible cases'.format(row[0]))
                continue
            if i is None:
                self.errors.append('Could not parse room: {}'.format(row[0]))
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
            talk1['speaker'] = " ".join(words[i+1:j])
            talk2['speaker'] = " ".join(words[j+1:])
            for t in [talk1, talk2]:
                if ":" in t['speaker']:
                    t['speaker'], t['desc'] = t['speaker'].split(':',1)
                if t['note']:
                    t['note'] = 'BC-MIT &mdash; ' + t['note']
                else:
                    t['note'] = 'BC-MIT'
            self.clean_talk(talk1)
            self.clean_talk(talk2)
            res += [talk1, talk2]
        return res






    @cached_property
    def talks(self):
        return self.html_talks

