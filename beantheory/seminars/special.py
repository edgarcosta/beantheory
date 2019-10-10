# -*- coding: utf-8 -*-
import requests
from cached_property import cached_property
from generic import GenericSeminar
import yaml
import os
from pytz import timezone

class SPECIAL(GenericSeminar):
    """
    class used for special seminars, like yearly events
    """
    def __init__(self):
        pass

    @cached_property
    def talks(self):
        utc = timezone('UTC')
        eastern = timezone('US/Eastern')
        filename = os.path.join(os.path.dirname(os.path.abspath(__file__)),'special.yaml')
        res = []
        with open(filename) as F:
            for elt in yaml.safe_load(F):
                if elt.get('speaker'):
                    elt['label'] = "special"
                    # YAML loads it as naive datetime and ignores timezone
                    elt['time'] = utc.localize(elt['time']).astimezone(eastern)
                    elt['endtime'] = utc.localize(elt['endtime']).astimezone(eastern)
                    self.clean_talk(elt)
                    res.append(elt)
        return res

