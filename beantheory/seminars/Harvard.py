# -*- coding: utf-8 -*-
from generic import GenericSeminar
from beantheory.utils.tableparser import TableParser
from cached_property import cached_property
import re
import os
import yaml
from pytz import timezone






# TODO keep old seminars?

class HARVARD(GenericSeminar):
    url = "http://www.math.harvard.edu/cgi-bin/showtalk.pl"
    # The ical file is useless
    # cal_url = r"http://www.math.harvard.edu/seminars/seminars.ics"
    name = "Harvard number theory seminar"
    place = "Harvard"
    label = "Harvard"
    room = None

    @cached_property
    def html_table(self):
        talks_regex = r'<table width="100%" border=0 cellpadding=3 cellspacing=0>([\s\S]*?)</table></center>'
        talks = re.findall(talks_regex, self.html)
        parser = TableParser()
        for t in talks:
            parser.feed(t)
        start = [i for i, r in enumerate(parser.table) if len(r)==3]

        res = []
        for i, s in enumerate(start):
            row = []
            if i == len(start) - 1:
                e = len(parser.table)
            else:
                e = start[i + 1]
            for j in range(s, e):
                row += parser.table[j]
            res.append(row)

        return res


    @cached_property
    def html_talks(self):
        res = []
        for row in self.table:
            # ignore the seminars that the name doesn't include the words
            # number and theory
            if not ('number' in row[0].lower() and 'theory' in row[0].lower()):
                continue
            if len(row) < 4:
                self.errors.append("This row has to few columns: {}".format(row))
            # discard abstract
            _, speaker, title, timeplace = row[:4]
            time, place = re.search(r'on \w*, (.*?) in (.*)$', timeplace).groups()
            time, note = self.parse_day(time)
            if time is None:
                continue

            talk = dict(self.talk_constant)
            talk['room'] = place
            talk['time'] = time
            talk['endtime'] = time + self.duration
            talk['speaker'] = row[1].lstrip(' ')
            talk['desc'] = title.lstrip(' ')
            talk['note'] = note
            self.clean_talk(talk)
            res.append(talk)
        return res

    @cached_property
    def past_talks(self):
        past_talks = []
        utc = timezone('UTC')
        eastern = timezone('US/Eastern')
        # load talks from yaml files, so talks don't disappear
        data_path = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..','_data', 'talks'))
        for filename in ['past.yaml', 'thisweek.yaml']:
            path = os.path.join(data_path, filename)
            if os.path.exists(path):
                with open(path) as F:
                    try:
                        talks = yaml.safe_load(F)
                    except Exception:
                        talks = []

                    for elt in talks:
                        if elt.get('label') != self.label:
                            continue
                        # YAML loads it as naive datetime and ignores timezone
                        elt['time'] = utc.localize(elt['time']).astimezone(eastern)
                        elt['endtime'] = utc.localize(elt['endtime']).astimezone(eastern)
                        past_talks.append(elt)
        return past_talks

    @cached_property
    def talks(self):
        res = self.html_talks
        days = {elt['time'].date() for elt in res}
        for elt in self.past_talks:
            d = elt['time'].date()
            if d in days:
                continue
            res.append(elt)

        res.sort(key=lambda x: x['time'])
        return res




