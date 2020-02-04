# -*- coding: utf-8 -*-
from __future__ import absolute_import
from .generic import GenericSeminar
from cached_property import cached_property
import os
import yaml
from pytz import timezone
from datetime import timedelta
from bs4 import BeautifulSoup







class HARVARD(GenericSeminar):
    url = "https://www.math.harvard.edu/event/?cat=number-theory"
    # The ical file is useless
    # cal_url = r"http://www.math.harvard.edu/seminars/seminars.ics"
    name = "Harvard number theory seminar"
    place = "Harvard"
    label = "Harvard"
    time = timedelta(hours=3)
    room = "Science Center 507"

    @cached_property
    def html_table(self):
        soup = BeautifulSoup(self.html, 'html.parser')
        res = []
        for div in soup.find_all('div',{'class':'event_item'}):
            startdate = div.find('span',{'class':'date-info'}).text
            abstract = div.find_all('p')[1].text
            speaker = div.find('div',{'class':'event-archive-speaker'}).text
            if speaker.startswith('Speaker:'):
                speaker = speaker[8:].lstrip()
            speaker = speaker.rstrip()
            if '-' in speaker:
                speaker, uni = speaker.split('-')
                uni = '(' + uni.lstrip() + ')'
                speaker = speaker.rstrip()
                speaker = speaker + " " + uni
            title = div.find('h3').text
            res.append((startdate, speaker, title, abstract))
        return res


    @cached_property
    def html_talks(self):
        res = []
        for row in self.table:
            # discard abstract
            time, speaker, title, _ = row
            time, note = self.parse_day(time)
            if time is None:
                continue
            if note is not None:
                # something went wrong with the parsing, and we only got the date
                time += self.time
                note = None

            talk = dict(self.talk_constant)
            talk['time'] = time
            talk['endtime'] = time + self.duration
            talk['speaker'] = speaker
            talk['desc'] = title
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




