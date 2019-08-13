# -*- coding: utf-8 -*-
import os
import yaml
from datetime import date, datetime
from seminars import BU, MIT
from seminars.STAGE import STAGES19
from seminars.MIT import MITS19
from utils import root_path

def talks():
    talks = []
    seminars = []
    for s in [BU(), MIT(),  STAGES19(), MITS19()]:
        talks += s.talks
        seminars.append({"name": s.name, "url": s.url})
    talks.sort(key=lambda x: x['time'])

    today = date.today()
    _, weeknumber, weekday = today.isocalendar()
    if weekday == 7:  # sunday
        weeknumber += 1
    past = [elt for elt in talks
            if elt['time'].isocalendar()[1] < weeknumber]
    # reverse ordering on the past seminars
    past.reverse()
    upcoming = [elt for elt in talks
                if elt['time'].isocalendar()[1] > weeknumber]
    thisweek = [elt for elt in talks
                if elt['time'].isocalendar()[1] == weeknumber]
    return past, thisweek, upcoming, seminars


def yaml_talks(folder=None):
    if folder is None:
        folder = os.path.join(root_path(), '_data/talks')

    for filename, data in zip(['past', 'thisweek', 'upcoming', 'seminars'], talks()):
        with open(os.path.join(folder, filename + ".yaml"), 'w') as F:
            F.write(yaml.safe_dump(data))


def git_infos():
    try:
        from subprocess import Popen, PIPE
        # cwd should be the root of git repo
        cwd = root_path()
        git_rev_cmd = '''git rev-parse HEAD'''
        git_date_cmd = '''git show --format="%ci" -s HEAD'''
        rev = Popen([git_rev_cmd], shell=True, stdout=PIPE, cwd=cwd).communicate()[0]
        date = Popen([git_date_cmd], shell=True, stdout=PIPE, cwd=cwd).communicate()[0]
        cmd_output = rev.rstrip('\n'), date.rstrip('\n')
    except Exception:
        cmd_output = '-', '-', '-'
    return cmd_output

def yaml_meta(folder=None):
    if folder is None:
        folder = os.path.join(root_path(), '_data/')
    git_rev, git_date = git_infos()
    data = {'git_rev': git_rev,
        'git_date': git_date,
        'now': datetime.now()}
    with open(os.path.join(folder, 'meta.yaml'), 'w') as F:
        F.write(yaml.safe_dump(data))


def yaml_all(folder=None):
    yaml_talks(folder)
    yaml_meta(folder)







