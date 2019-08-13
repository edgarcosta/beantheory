# -*- coding: utf-8 -*-
from html.parser import HTMLParser
from htmlentitydefs import name2codepoint

class TableParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.table = []
        self.table_row = None
        self.data = None
    def handle_starttag(self, tag, attrs):
        if tag == 'tr':
            if self.table_row is not None:
                if self.data is not None:
                    self.table_row.append("".join(self.data))
                self.table.append(self.table_row)

            self.table_row = []
        if tag == 'td':
            if self.data is not None and self.table_row is not None:
                self.table_row.append("".join(self.data))
            self.data = []
        if tag == 'br':
            if self.data is not None:
                self.data.append(" ")



    def handle_endtag(self, tag):
        if tag in ['tr', 'td']:
            if self.data is not None and self.table_row is not None:
                self.table_row.append("".join(self.data))
            self.data = None
        if tag == 'tr':
            if self.table_row is not None:
                self.table.append(self.table_row)
            self.table_row = None

    def handle_data(self, data):
        if self.data is not None:
            self.data.append(data)

    def handle_entityref(self, name):
        c = unichr(name2codepoint[name])
        if self.data is not None:
            self.data.append(c)

    def handle_charref(self, name):
        if name.startswith('x'):
            c = unichr(int(name[1:], 16))
        else:
            c = unichr(int(name))
        if self.data is not None:
            self.data.append(c)

    def close(self):
        if self.table_row is not None:
            self.table.append(self.table_row)
        HTMLParser.close(self)
