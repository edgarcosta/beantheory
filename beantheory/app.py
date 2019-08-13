import os
import yaml
from datetime import date
from seminars import BU, MIT
from utils import root_path

def talks():
    talks = sorted(BU().talks + MIT().talks, key=lambda x: x['time'])
    today = date.today()
    _, weeknumber, weekday = today.isocalendar()
    if weekday == 7:  # sunday
        weeknumber += 1
    past = [elt for elt in talks
            if elt['time'].isocalendar()[1] < weeknumber]
    upcoming = [elt for elt in talks
                if elt['time'].isocalendar()[1] > weeknumber]
    thisweek = [elt for elt in talks
                if elt['time'].isocalendar()[1] == weeknumber]
    return past, thisweek, upcoming


def yaml_talks(folder=None):
    if folder is None:
        folder = os.path.join(root_path(), '_data/talks')

    for filename, data in zip(['past', 'thisweek', 'upcoming'], talks()):
        with open(os.path.join(folder, filename + ".yaml")) as F:
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
        cmd_output = rev, date
    except Exception:
        cmd_output = '-', '-', '-'
    return cmd_output

def yaml_meta(folder=None):
    if folder is None:
        folder = os.path.join(root_path(), '_data/')
    git_rev, git_date = git_infos()
    data = {'git_rev': git_rev,
        'git_data': git_data,
        'now:' datetime.datetime.now()}
    with open(os.path.join(folder, 'meta.yaml') as F:
        F.write(yaml.safe_dump(data))


def yaml_all(folder=None):
    yaml_talks(folder)
    yaml_meta(folder)







