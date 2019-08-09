# -*- coding: utf-8 -*-
from generic import GenericSeminar
import dateutil
from sage.all import cached_method

class MIT(GenericSeminar):
    url = "http://math.mit.edu/nt/nts.html"
    name = "MIT NT"
    room_regex = '(?<=in MIT room )(.+)(?=\.)'
    time_regex = '(?<=, )([0-9]+):([0-9]+)(?=\-[0-9]+:[0-9]+[a|p]m)'
    table_regex = '(?<=<TABLE BORDER=5 CELLPADDING=10 width=100% >)((.|\n)*)(?=</TABLE>)'

    @cached_method
    def talks(self):
        res = []
        # skip header
        for row in self.table():
            # skip ill formed rows
            if len(row) != 1:
                continue

            # fetch the first two words
            s = row[0].split(' ', 2)
            if len(s) != 3:
                continue
            row = [s[0] + " " + s[1], s[2]]
            if ":" == row[0][-1]:
                row[0] = row[0][:-1]


            # skip no seminar
            if 'no seminar' in row[1].lower():
                continue
            # skip emtpy slots
            if '' == row[1].replace(' ', ''):
                continue
            # skip BC/MIT
            if 'BC-MIT' in row[1]:
                continue
            try:
                day = dateutil.parser.parse(row[0])
            except ValueError:
                continue
            time = day + self.time()

            {'time':time, 'speaker': row[1], 'desc': None, 'seminar': self.name}
        return res

class MITS17(MIT):
    url = "http://math.mit.edu/nt/old/nts_s17.html"
class MITS19(MIT):
    url = "http://math.mit.edu/nt/old/nts_s19.html"
