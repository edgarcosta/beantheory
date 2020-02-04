# -*- coding: utf-8 -*-
from __future__ import absolute_import
from .ical import IcalSeminar
from cached_property import cached_property
import re
from datetime import timedelta

class STAGE(IcalSeminar):
    url = "http://math.mit.edu/nt/stage.html"
    cal_url = 'http://calendar.mit.edu/search/events.ics?search="STAGE+Seminar"'
    name = "STAGE"
    place = "MIT-STAGE"
    label = "STAGE"
    room_regex = r'(?<=in MIT room )(?:.+)(\d\-\d{3})(?:.+)(?=, unless indicated otherwise below)'
    table_regex = r'(?<=<TABLE BORDER=5 CELLPADDING=10 width=100% >)((.|\n)*)(?=</TABLE>)'
    duration = timedelta(hours=2)

    @cached_property
    def time(self):
        time_blob = re.search(r'(?<=Meetings are held on)(.*)(?=in MIT room)', self.html)
        h = re.search('(?<=, )([0-9]+)(?=[[a|p]m|-)', time_blob.group(0)).group(0)
        h = int(h)
        if h < 8:
            h += 12
        return timedelta(hours=h)

    @cached_property
    def html_talks(self):
        res = []
        # skip header
        for row in self.table:
            # there are some empty rows in the table
            if len(row) == 0:
                continue
            # skip ill formed rows
            if len(row) != 1:
                self.errors.append('Skipping ill formed row = {}'.format(row))
                continue

            # fetch the first two words
            s = row[0].lstrip(' ').split(' ', 2)
            if len(s) != 3:
                continue
            row = [s[0] + " " + s[1], s[2]]
            if ":" == row[0][-1]:
                row[0] = row[0][:-1]
            if ":" == row[1][0]:
                row[1] = row[1][1:]



            # skip no meeting
            if 'no meeting' in row[1].lower():
                continue

            # skip no seminar
            if 'no seminar' in row[1].lower():
                continue

            # skip emtpy slots
            if re.match('^\s+$', row[1]):
                continue

            day, note = self.parse_day(row[0])
            if day is None:
                continue
            time = day + self.time

            if '.' in row[1]:
                speaker, desc = row[1].split('.', 1)
            else:
                speaker, desc = row[1], None

            if desc:
                if re.match('^\s+$', desc):
                    desc = None

            talk = dict(self.talk_constant)
            talk['time'] = time
            talk['endtime'] = time + self.duration
            talk['speaker'] = speaker
            talk['desc'] = desc
            talk['note'] = note
            self.clean_talk(talk)
            res.append(talk)
        return res

    @cached_property
    def ical_talks(self):
        res = []
        for time, endtime, summary, desc, location in self.ical_table:
            if summary != 'STAGE Seminar':
                continue
            talk = dict(self.talk_constant)
            talk['time'] = time
            talk['endtime'] = endtime
            # the speaker is the first line
            speaker, desc = desc.split('\n',1)
            desc = desc.lstrip('\n')
            talk['speaker'] = speaker
            # this gets the title between utf-8 quotes
            for pattern in [u'\xe2\x80\x9c((.|\n)*?)\xe2\x80\x9d', u'"((.|\n)*?)"', u'((.)*?)\n']:
                title = re.search(pattern, desc)
                if title is not None:
                    title = title.group(1)
                    break

            talk['desc'] = title
            if location:
                talk['room'] = location

            res.append(talk)
        return res

    @cached_property
    def talks(self):
        res = self.ical_talks
        days = {elt['time'].date() for elt in res}
        for elt in self.html_talks:
            d = elt['time'].date()
            if d in days:
                continue
            res.append(elt)

        res.sort(key=lambda x: x['time'])
        return res

class STAGES19(STAGE):
    name = "STAGE S19"
    url = "http://math.mit.edu/nt/old/stage_s19.html"

class STAGEF18(STAGE):
    url = "http://math.mit.edu/nt/old/stage_f18.html"
    name = "STAGE F18"
