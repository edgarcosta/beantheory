# -*- coding: utf-8 -*-
import requests
from datetime import timedelta, datetime
from cached_property import cached_property
import icalendar
from pytz import timezone
from generic import GenericSeminar


eastern = timezone('US/Eastern')
threshold_time = timedelta(weeks=14)

class IcalSeminar(GenericSeminar):
    def __init__(self):
        GenericSeminar.__init__(self)
        r = requests.get(self.cal_url)
        self.gcal = icalendar.Calendar.from_ical(r.text)
        self.errors = []

    def speaker_parser(self, x):
        return x

    def desc_parser(self, x):
        return x



    @cached_property
    def ical_table(self):
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
    def ical_talks(self):
        res = []
        for time, speaker, desc, location in self.ical_table:
            talk = dict(self.talk_constant)
            talk['time'] = time
            speaker = self.speaker_parser(speaker)
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

    @cached_property
    def talks(self):
        return self.ical_talks








