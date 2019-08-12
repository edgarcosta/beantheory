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
def fmtdatetime(value, format='%m-%d %H:%M'):
    if isinstance(value, datetime.datetime):
        return value.strftime(format)
    else:
        return "-"



##############################
#       Top-level pages      #
##############################

@app.route("/")
def index():
    from seminars import BU, MIT
    talks = sorted(BU().talks() + MIT().talks(), key=lambda x: x['time'])
    print talks
    return render_template('index.html',
        upcoming=talks)
