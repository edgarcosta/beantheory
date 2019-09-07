# -*- coding: utf-8 -*-

__version__ = '0.0.1'
all = ['ical', 'talks', 'yaml_talks', 'yaml_meta', 'yaml_all']
from .app import ical, talks, yaml_talks, yaml_meta, yaml_all
assert ical
assert talks
assert yaml_talks
assert yaml_meta
assert yaml_all

