# -*- coding: utf-8 -*-
from flask import Flask, render_template
import datetime
app = Flask(__name__)

app.is_running = False
def set_running():
    app.is_running = True
def is_running():
    return app.is_running


# If the debug toolbar is installed then use it
if app.debug:
    try:
        from flask_debugtoolbar import DebugToolbarExtension
        app.config['SECRET_KEY'] = '''shh, it's a secret'''
        toolbar = DebugToolbarExtension(app)
    except ImportError:
        pass


# tell jinja to remove linebreaks
app.jinja_env.trim_blocks = True

# enable break and continue in jinja loops
app.jinja_env.add_extension('jinja2.ext.loopcontrols')
app.jinja_env.add_extension('jinja2.ext.do')


##############################
#      Jinja formatters      #
##############################

# you can pass in a datetime.datetime python object and via
# {{ <datetimeobject> | fmtdatetime }} you can format it inside a jinja template
# if you want to do more than just the default, use it for example this way:
# {{ <datetimeobject>|fmtdatetime('%H:%M:%S') }}
@app.template_filter("fmtdatetime")
def fmtdatetime(value, format='%b %d %H:%M'):
    if isinstance(value, datetime.datetime):
        return value.strftime(format)
    else:
        return "-"



##############################
#       Top-level pages      #
##############################

def talks():
    from datetime import date
    from seminars import BU, MIT
    talks = sorted(BU().talks + MIT().talks, key=lambda x: x['time'])
    today = date.today()
    _, weeknumber, weekday = today.isocalendar()
    if weekday == 7: # sunday
        weeknumber += 1
    past = [elt for elt in talks
            if elt['time'].isocalendar()[1] < weeknumber]
    upcoming = [elt for elt in talks
                if elt['time'].isocalendar()[1] > weeknumber]
    thisweek = [elt for elt in talks
                if elt['time'].isocalendar()[1] == weeknumber]
    return past, thisweek, upcoming


@app.route("/")
def index():
    past, thisweek, upcoming = talks()
    return render_template('index.html',
        past=past,
        thisweek=thisweek,
        upcoming=upcoming)
