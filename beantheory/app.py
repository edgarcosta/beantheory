# -*- coding: utf-8 -*-
import os
import yaml
from datetime import date, datetime
from seminars import BU, MIT, BC, TUFTS, STAGE
from utils import root_path

def talks():
    talks = []
    seminars = []
    for s in [BU(), MIT(), TUFTS(), BC(), STAGE()]:
        talks += s.talks
        seminars.append({"name": s.name,
                         "url": s.url,
                         "errors": "\n ".join(s.errors),
                         "label": s.label})
    talks.sort(key=lambda x: x['time'])

    seminars.sort(key=lambda x: x['name'])

    today = date.today()
    year, weeknumber, weekday = today.isocalendar()
    if weekday == 7:  # sunday
        weeknumber += 1
    past = [elt for elt in talks
            if tuple(elt['time'].isocalendar()[:2]) < (year, weeknumber)]
    # reverse ordering on the past seminars
    past.reverse()
    upcoming = [elt for elt in talks
                if tuple(elt['time'].isocalendar()[:2]) > (year, weeknumber + 1)]
    thisweek = [elt for elt in talks
                if tuple(elt['time'].isocalendar()[:2]) == (year, weeknumber)]
    nextweek = [elt for elt in talks
                if tuple(elt['time'].isocalendar()[:2]) == (year, weeknumber + 1)]
    return past, thisweek, nextweek, upcoming, seminars


def yaml_talks(folder=None):
    if folder is None:
        folder = os.path.join(root_path(), '_data/talks')

    for filename, data in zip(['past', 'thisweek', 'nextweek', 'upcoming', 'seminars'], talks()):
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







