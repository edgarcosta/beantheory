# -*- coding: utf-8 -*-
from generic import GenericSeminar
import dateutil
from sage.all import cached_method
import re
from datetime import timedelta

class STAGE(GenericSeminar):
    url = "http://math.mit.edu/nt/stage.html"
    name = "STAGE"
    room_regex = '(?<=in MIT room )(.+)(?=\,)'
    table_regex = '(?<=<TABLE BORDER=5 CELLPADDING=10 width=100% >)((.|\n)*)(?=</TABLE>)'

    @cached_method
    def time(self):
        time_blob = re.search('(?<=Meetings are held on)(.*)(?=in MIT room)', self.html)
        h = re.search('(?<=, )([0-9]+)(?=[[a|p]m|-)', time_blob.group(0)).group(0)
        h = int(h)
        if h < 8:
            h += 12
        return timedelta(hours=h)

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


            # skip no meeting
            if 'no meeting' in row[1].lower():
                continue

            # skip emtpy slots
            if re.match('^\s+$', row[1]):
                continue
            try:
                day = dateutil.parser.parse(row[0])
            except ValueError:
                continue
            time = day + self.time()

            if '.' in row[1]:
                author, desc = row[1].split('.', 1)
            else:
                author, desc = None, row[1]

            res.append({'time':time, 'speaker': author, 'desc': desc, 'seminar': self.name})
        return res

class STAGES19(STAGE):
    url = "http://math.mit.edu/nt/old/stage_s19.html"

class STAGEF18(STAGE):
    url = "http://math.mit.edu/nt/old/stage_f18.html"
