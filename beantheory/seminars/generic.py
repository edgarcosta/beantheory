# -*- coding: utf-8 -*-
import requests
from datetime import timedelta
import re
from sage.all import cached_method
from beantheory.utils import TableParser

class GenericSeminar(object):
    def __init__(self):
        r = requests.get(self.url)
        self.html = r.text.replace('\n','').replace('&nbsp;','')

    @cached_method
    def room(self):
        return re.search(self.room_regex, self.html).group(0)

    @cached_method
    def time(self):
        h, m = re.search(self.time_regex, self.html).groups()
        h = int(h)
        m = int(m)
        if h < 8:
            h += 12
        return timedelta(hours=h, minutes=m)

    @cached_method
    def table(self):
        table_text = re.search(self.table_regex, self.html).group(0)

        parser = TableParser()
        parser.feed(table_text)
        table = parser.table[:]
        parser.close
        return table
