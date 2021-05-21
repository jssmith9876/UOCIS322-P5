"""
Replacement for RUSA ACP brevet time calculator
(see https://rusa.org/octime_acp.html)

"""

import flask
from flask import request
import arrow  # Replacement for datetime, based on moment.js
import acp_times  # Brevet time calculations
import config
import os
from pymongo import MongoClient

import logging

###
# Globals
###
app = flask.Flask(__name__)
CONFIG = config.configuration()

client = MongoClient('mongodb://' + os.environ['MONGODB_HOSTNAME'], 27017)
db = client.brevetdb

###
# Pages
###


@app.route("/")
@app.route("/index")
def index():
    app.logger.debug("Main page entry")
    return flask.render_template('calc.html')

@app.route("/display_results")
def display_results():
    return flask.render_template("display_results.html",
                                items=list(db.brevetdb.find()))

@app.errorhandler(404)
def page_not_found(error):
    app.logger.debug("Page not found")
    return flask.render_template('404.html'), 404



###############
#
# AJAX request handlers
#   These return JSON, rather than rendering pages.
#
###############
@app.route("/_calc_times")
def _calc_times():
    """
    Calculates open/close times from miles, using rules
    described at https://rusa.org/octime_alg.html.
    Expects one URL-encoded argument, the number of miles.
    """
    app.logger.debug("Got a JSON request")
    km = request.args.get('km', default=999, type=float)
    dist = request.args.get('dist', default=999, type=float)
    start_time = request.args.get('start', default=arrow.now(), type=str)
    start_time = arrow.get(start_time)
    app.logger.debug("km={}".format(km))
    app.logger.debug("request.args: {}".format(request.args))
    open_time = acp_times.open_time(km, dist, start_time).format('YYYY-MM-DDTHH:mm')
    close_time = acp_times.close_time(km, dist, start_time).format('YYYY-MM-DDTHH:mm')
    result = {"open": open_time, "close": close_time}
    return flask.jsonify(result=result)

@app.route("/_submit_values", methods=["POST"])
def submit_values():
    app.logger.debug("Got a submit request")
    entries = request.form

    db.brevetdb.drop()

    numInputs = len(entries) // 5
    fields = ['index', 'miles', 'km', 'open', 'close']
    for i in range(numInputs):
        item = {}
        for field in fields:
            item[field] = entries['entries[' + str(i) + '][' + field + ']']
        db.brevetdb.insert_one(item)

    # app.logger.debug(entries)
    result = {"delivered": True}
    return flask.jsonify(response=result)

#############

app.debug = CONFIG.DEBUG
if app.debug:
    app.logger.setLevel(logging.DEBUG)

if __name__ == "__main__":
    print("Opening for global access on port {}".format(CONFIG.PORT))
    app.run(port=CONFIG.PORT, host="0.0.0.0")
