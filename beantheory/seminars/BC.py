# -*- coding: utf-8 -*-
from ical import IcalSeminar



class BC(IcalSeminar):
    url = "https://sites.google.com/bc.edu/2019-20bcntagseminar"
    cal_url = r"https://calendar.google.com/calendar/ical/bc.edu_nqaftbfgpukja204ku04j5p5a4@group.calendar.google.com/public/basic.ics"
    name = "BC NT & AG Seminar"
    place = "BC"
    label = "BC"
    room = "Maloney 560"

    def speaker_parser(self, x):
        return x[15:] if x.startswith('NT&AG Seminar: ') else x

    def desc_parser(self, text):
        if text and text.lstrip().startswith('Title: '):
                return text.split('\n', 1)[0][7:]
        return None
