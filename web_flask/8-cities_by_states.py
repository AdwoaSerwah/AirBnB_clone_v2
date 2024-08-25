#!/usr/bin/python3
"""
Flask web application to display states and their cities from the database.
"""
from flask import Flask, render_template
from models import storage
from models.state import State
from models.city import City

app = Flask(__name__)


@app.teardown_appcontext
def teardown_db(exception):
    """Remove the current SQLAlchemy Session."""
    storage.close()


@app.route('/cities_by_states', strict_slashes=False)
def cities_by_states():
    """Display HTML page with all State objects and their cities sorted"""
    states = storage.all(State).values()
    sorted_states = sorted(states, key=lambda x: x.name)
    html_file = '8-cities_by_states.html'

    # Prepare the data for the template
    states_cities = []
    for state in sorted_states:
        if hasattr(state, 'cities'):
            cities = sorted(state.cities, key=lambda x: x.name)
        else:
            cities = sorted(storage.all(City).values(), key=lambda x: x.name)
        states_cities.append({
            'state': state,
            'cities': cities
        })

    return render_template(html_file, states_cities=states_cities)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
