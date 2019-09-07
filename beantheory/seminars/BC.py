# -*- coding: utf-8 -*-
from ical import IcalSeminar
from beantheory.utils.tableparser import rawtext_to_paragraphlist
from cached_property import cached_property
from datetime import timedelta
import re


class BC(IcalSeminar):
    url = "https://sites.google.com/bc.edu/2019-20bcntagseminar"
    cal_url = r"https://calendar.google.com/calendar/ical/bc.edu_nqaftbfgpukja204ku04j5p5a4@group.calendar.google.com/public/basic.ics"
    name = "BC NT & AG Seminar"
    place = "BC"
    label = "BC"
    room = "Maloney 560"
    time = timedelta(hours=14)
    table_regex = r'data-code="((.|\n)*?)&lt;a href'

    def speaker_parser(self, x):
        if x.startswith('NT&AG Seminar: '):
            return x[15:]
        else:
            return x

    def desc_parser(self, text):
        if text and text.lstrip().startswith('Title: '):
                return text.split('\n', 1)[0][7:]
        return None

    @cached_property
    def html_table(self):
        table_text = re.search(self.table_regex, self.html).group(1)
        return rawtext_to_paragraphlist(table_text)

    @cached_property
    def html_talks(self):
        res = []
        for elt in self.table:
            if ':' not in elt:
                continue
            row = elt.split(':')
            # skip no seminar
            if 'no seminar' in row[1].lower():
                continue
            if 'thanksgiving break' in row[1].lower():
                continue
            # skip emtpy slots
            if re.match('^\s+$', row[1]):
                continue

            day, note = self.parse_day(row[0])
            if day is None:
                continue
            time = day + self.time
            talk = dict(self.talk_constant)
            talk['time'] = time
            talk['endtime'] = time + self.duration
            talk['speaker'] = row[1]
            talk['desc'] = None
            talk['note'] = note
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


