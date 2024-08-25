#!/usr/bin/python3
""" This module sorts and prints cities and states"""
from models import storage
from models.state import State
# from os import environ
from flask import Flask, render_template

app = Flask(__name__)


@app.teardown_appcontext
def close_db(error):
    """ Remove the current SQLAlchemy Session """
    storage.close()


@app.route('/states', strict_slashes=False)
@app.route('/states/<id>', strict_slashes=False)
def states_state(id=""):
    states = storage.all(State).values()
    states = sorted(states, key=lambda k: k.name)
    skk_found = 0
    skk_state = ""
    cities = []

    for i in states:
        if id == i.id:
            skk_state = i
            skk_found = 1
            break

    if skk_found:
        states = sorted(skk_state.cities, key=lambda x: x.name)
        skk_state = skk_state.name

    if id and not skk_found:
        skk_found = 2

    return render_template('9-states.html',
                           state=skk_state,
                           lists=states,
                           found=skk_found)


if __name__ == "__main__":
    """ Main Function """
    app.run(host='0.0.0.0', port=5000)
