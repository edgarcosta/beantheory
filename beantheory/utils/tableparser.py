# -*- coding: utf-8 -*-
from html.parser import HTMLParser
import sys
if sys.version_info[0] < 3:
    from htmlentitydefs import name2codepoint
else:
    from html.entities import name2codepoint

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


class DataParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.data = []
    def output(self):
        return ''.join(self.data)

    def handle_data(self, data):
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

class ParagraphParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.table = []
        self.data = []
    def handle_starttag(self, tag, attrs):
        if tag == 'p':
            if self.data:
                self.table.append("".join(self.data))
            self.data = []

        if tag == 'br':
            self.data.append(" ")



    def handle_endtag(self, tag):
        if tag == 'p':
            if self.data:
                self.table.append("".join(self.data))
            self.data = []

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

def rawtext_to_paragraphlist(text):
    # first unescape html
    parser = DataParser()
    parser.feed(text)
    # convert paragraphs to lines
    pparser = ParagraphParser()
    pparser.feed(parser.output())
    return pparser.table

