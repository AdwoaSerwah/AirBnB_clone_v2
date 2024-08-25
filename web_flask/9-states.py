#!/usr/bin/python3
"""Flask web application to display states and cities."""

from flask import Flask, render_template
from models import storage
from models.state import State

app = Flask(__name__)


@app.teardown_appcontext
def close_storage(exception):
    """Closes the storage on teardown."""
    storage.close()


@app.route('/states', strict_slashes=False)
@app.route('/states/<id>', strict_slashes=False)
def states(id=None):
    """Display a HTML page with states or cities depending on the route."""
    states = storage.all(State)
    if id:
        state = states.get('State.' + id)
        return render_template('9-states.html', state=state)
    else:
        return render_template('9-states.html', states=states)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
