# -*- coding: utf-8 -*-
from __future__ import absolute_import
from .generic import GenericSeminar
from cached_property import cached_property
import yaml
import os
from pytz import timezone, utc

class SPECIAL(GenericSeminar):
    """
    class used for special seminars, like yearly events
    """
    def __init__(self):
        pass

    @cached_property
    def talks(self):
        eastern = timezone('US/Eastern')
        filename = os.path.join(os.path.dirname(os.path.abspath(__file__)),'special.yaml')
        res = []
        with open(filename, 'r') as F:
            for elt in yaml.safe_load(F):
                if elt.get('speaker'):
                    elt['label'] = "special"
                    # YAML loads it as naive datetime and ignores timezone
                    elt['time'] = elt['time'].replace(tzinfo=utc).astimezone(eastern)
                    elt['endtime'] = elt['endtime'].replace(tzinfo=utc).astimezone(eastern)
                    self.clean_talk(elt)
                    res.append(elt)
        return res

