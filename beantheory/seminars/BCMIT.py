# -*- coding: utf-8 -*-
from generic import GenericSeminar
from datetime import timedelta
from cached_property import cached_property
from bs4 import BeautifulSoup
import re
import calendar

class BCMIT(GenericSeminar):
    url = "https://sites.google.com/bc.edu/benjamin-howard/bc-mit-seminar"
    name = "BC-MIT number theory seminar"
    label = "BCMIT"
    # table_regex = r'<table border="5" cellpadding="10" width="100%">((.|\n)*?)</table>'
    duration = timedelta(hours=1)

    def __init__(self):
        GenericSeminar.__init__(self)
        self.room = self.time = self.place = None

    @cached_property
    def table(self):
        soup = BeautifulSoup(self.html, 'html.parser')
        rows = []
        for elt in soup.find_all('h3'):
            if elt.text.lstrip().split()[0] in calendar.month_name:
                row = [elt.text]
                for col in elt.find_next_siblings('p', limit=2):
                    row.append(col.text)
                rows.append(row)

        return rows

    @cached_property
    def html_talks(self):
        day_place_regex = re.compile(r'(.+) \((MIT|BC),\s(.+)\)')
        hours_minutes_rest = re.compile(r'(\d+):(\d+)-(\d+):(\d+):(.+)')
        res = []
        for row in self.table:
            if len(row) != 3:
                self.errors.append('Could not parse: {} '.format(row))
                continue
            try:
                day, place, room = day_place_regex.findall(row[0])[0]
            except Exception:
                self.errors.append('Could not parse (day, place, room): {} '.format(row[0]))
                continue
            try:
                day, note = self.parse_day(day)
            except Exception:
                self.errors.append('Could not parse (day, note): {} '.format(day))


            for talk_row in row[1:]:
                talk = dict(self.talk_constant)
                try:
                    start_h, start_m, end_h, end_m, rest = hours_minutes_rest.findall(time)[0]
                except Exception:
                    self.errors.append('Could not parse (start_h, start_m, end_h, end_m): {} '.format(time))
                    continue
                try:
                    if ":" in rest:
                        speaker, title = rest.split(':', 1)
                    else:
                        speaker = rest
                        title = None
                except Exception:
                    self.errors.append('Could not parse (speaker, title): {} '.format(rest))
                    continue
                talk['time'] = day + timedelta(hours=12 + int(start_h), minutes=int(start_m))
                talk['endtime'] = day + timedelta(hours=12 + int(end_h), minutes=int(end_m))
                talk['place'] = place
                talk['room'] = room
                talk['note'] = 'BC-MIT'
                if note:
                    talk['note'] += '&mdash;' + note
                talk['speaker'] = speaker
                talk['desc'] = title
                self.clean_talk(talk)
                res.append(talk)
        return res



    @cached_property
    def talks(self):
        return self.html_talks

