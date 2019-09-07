# -*- coding: utf-8 -*-
import requests
from datetime import timedelta
import re
from cached_property import cached_property
from beantheory.utils import TableParser
from pytz import timezone


eastern = timezone('US/Eastern')

class GenericSeminar(object):
    duration = timedelta(hours=1)
    def __init__(self):
        r = requests.get(self.url)
        self.html = r.text.replace('\n',' ').replace('&nbsp;',' ')
        self.errors = []

    @cached_property
    def room(self):
        return re.search(self.room_regex, self.html).group(1)

    @cached_property
    def time(self):
        h, m = re.search(self.time_regex, self.html).groups()
        h = int(h)
        m = int(m)
        if h < 8:
            h += 12
        return timedelta(hours=h, minutes=m)

    @cached_property
    def html_table(self):
        table_text = re.search(self.table_regex, self.html).group(1)

        parser = TableParser()
        parser.feed(table_text)
        table = parser.table[:]
        parser.close
        return table

    @cached_property
    def table(self):
        return self.html_table

    @cached_property
    def talk_constant(self):
        return {'url': self.url,
                'seminar': self.name,
                'place': self.place,
                'room': self.room,
                'label': self.label}


    def parse_day(self, text):
        from dateutil import parser
        try:
            day = parser.parse(text)
            other = None
        except ValueError:
            try:
                # try to only parse the first two words
                text = text.lstrip(" ")
                words = text.split(" ", 2)
                twowords = " ".join(words[:2])
                day = parser.parse(twowords)
                other = words[2]
            except ValueError:
                self.errors.append('Could not parse: {} to a date'.format(repr(text)))
                day = None
                other = text

        if day:
            day = eastern.localize(day)

        return day, other
