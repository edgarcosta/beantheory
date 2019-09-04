# -*- coding: utf-8 -*-
import requests
from datetime import timedelta, datetime
import re
from cached_property import cached_property
import dateutil
import icalendar
from pytz import timezone


eastern = timezone('US/Eastern')
threshold_time = timedelta(weeks=14)

class IcalSeminar(object):
    def __init__(self):
        r = requests.get(self.cal_url)
        self.gcal = icalendar.Calendar.from_ical(r.text)
        self.errors = []

    def speaker_parser(self, x):
        return x

    def desc_parser(self, x):
        return x

    @cached_property
    def talk_constant(self):
        return {'url': self.url,
                'seminar': self.name,
                'place': self.place,
                'room': self.room,
                'label': self.label}

    @cached_property
    def table(self):
        now = eastern.localize(datetime.now())
        res = []
        for component in self.gcal.walk():
            if component.name == "VEVENT":
                time = component.get('dtstart').dt.astimezone(eastern)
                if now - time > threshold_time:
                    continue
                res.append([
                    component.get('dtstart').dt.astimezone(eastern),
                    component.get('summary').encode('utf-8'),
                    component.get("description").encode('utf-8'),
                    component.get("location").encode('utf-8')])

        return res

    @cached_property
    def talks(self):
        res = []
        for time, speaker, desc, location in self.table:
            talk = dict(self.talk_constant)
            talk['time'] = time
            self.speaker_parser(speaker)
            if not speaker or 'TBA' in speaker or 'TBD' in speaker:
                continue
            talk['speaker'] = speaker
            desc = self.desc_parser(desc)
            if desc:
                talk['desc'] = desc
            else:
                talk['desc'] = None
            if location:
                talk['room'] = location

            res.append(talk)
        return res








