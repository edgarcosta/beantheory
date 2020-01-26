# -*- coding: utf-8 -*-
import os
import yaml
from datetime import date, datetime
from seminars import BU, MIT, BC, BCMIT, TUFTS, STAGE, HARVARD, SPECIAL
from utils import root_path
from icalendar import Calendar, Event

global_seminars = [
    # HARVARD(),
    #BCMIT(),
    BU(),
    MIT(),
    TUFTS(),
    BC(),
    STAGE()
]


def talks():
    talks = []
    seminars = []
    for s in global_seminars:
        talks += s.talks
        seminars.append(
            {
                "name": s.name,
                "url": s.url,
                "errors": "\n ".join(s.errors),
                "label": s.label,
            }
        )
    talks += SPECIAL().talks
    talks.sort(key=lambda x: x["time"])

    seminars.sort(key=lambda x: x["name"])

    today = date.today()
    year, weeknumber, weekday = today.isocalendar()
    if weekday == 7:  # sunday
        weeknumber += 1
    past = [
        elt
        for elt in talks
        if tuple(elt["time"].isocalendar()[:2]) < (year, weeknumber)
    ]
    # reverse ordering on the past seminars
    past.reverse()
    upcoming = [
        elt
        for elt in talks
        if tuple(elt["time"].isocalendar()[:2]) > (year, weeknumber + 1)
    ]
    thisweek = [
        elt
        for elt in talks
        if tuple(elt["time"].isocalendar()[:2]) == (year, weeknumber)
    ]
    nextweek = [
        elt
        for elt in talks
        if tuple(elt["time"].isocalendar()[:2]) == (year, weeknumber + 1)
    ]
    return past, thisweek, nextweek, upcoming, seminars


def ical(filename=None):
    if filename is None:
        filename = os.path.join(root_path(), "assets/beantheory.ics")
    cal = Calendar()
    cal.add("VERSION", "2.0")
    cal.add("PRODID", "beantheory")
    cal.add("CALSCALE", "GREGORIAN")
    cal.add("X-WR-CALNAME", "Bean Theory")
    for talk in SPECIAL().talks + sum((s.talks for s in global_seminars), []):
        event = Event()
        event.add("summary", talk["speaker"])
        event.add("dtstart", talk["time"])
        event.add("dtend", talk["endtime"])
        if talk["desc"]:
            event.add("description", talk["desc"])
        event.add("location", "{} usually {}".format(talk["place"], talk["room"]))
        event.add("url", talk["url"])
        cal.add_component(event)

    f = open(filename, "wb")
    f.write(cal.to_ical())
    f.close()


def yaml_talks(folder=None):
    if folder is None:
        folder = os.path.join(root_path(), "_data/talks")

    for filename, data in zip(
        ["past", "thisweek", "nextweek", "upcoming", "seminars"], talks()
    ):
        with open(os.path.join(folder, filename + ".yaml"), "w") as F:
            F.write(yaml.safe_dump(data))


def git_infos():
    try:
        from subprocess import Popen, PIPE

        # cwd should be the root of git repo
        cwd = root_path()
        git_rev_cmd = """git rev-parse HEAD"""
        git_date_cmd = """git show --format="%ci" -s HEAD"""
        rev = Popen([git_rev_cmd], shell=True, stdout=PIPE, cwd=cwd).communicate()[0]
        date = Popen([git_date_cmd], shell=True, stdout=PIPE, cwd=cwd).communicate()[0]
        cmd_output = rev.rstrip("\n"), date.rstrip("\n")
    except Exception:
        cmd_output = "-", "-", "-"
    return cmd_output


def yaml_meta(folder=None):
    if folder is None:
        folder = os.path.join(root_path(), "_data/")
    git_rev, git_date = git_infos()
    data = {"git_rev": git_rev, "git_date": git_date, "now": datetime.now()}
    with open(os.path.join(folder, "meta.yaml"), "w") as F:
        F.write(yaml.safe_dump(data))


def yaml_all(folder=None):
    yaml_talks(folder)
    yaml_meta(folder)
