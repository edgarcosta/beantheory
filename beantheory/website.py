import beantheory.app # So that we can set it running below
from beantheory.app import app

import seminars
assert seminars


def main():
    from beantheory.utils.config import Configuration
    flask_options = Configuration().get_flask();

    if "profiler" in flask_options and flask_options["profiler"]:
        print "Profiling!"
        from werkzeug.contrib.profiler import ProfilerMiddleware
        app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions = [30], sort_by=('cumulative','time','calls'))
        del flask_options["profiler"]

    beantheory.app.set_running()
    app.run(**flask_options)
