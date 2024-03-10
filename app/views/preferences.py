from flask import render_template, request, redirect, url_for, session, g
from flask import jsonify

from app.db.controllers.preferences import PreferencesController


def set_preferences():
    # Extract form data
    user_id = request.form['user_id']
    country = request.form['country']
    start_time = request.form['start_time']
    end_time = request.form['end_time']
    sport_type = request.form['sport_type']

    # Update preferences in the database
    # TODO: Move to controllers
    update_preferences_in_db(user_id, country, start_time, end_time, sport_type)

    # Redirect or show a success message
    return redirect(url_for('some_other_function'))


def get_preferences():
    # Simulating fetching data from '/api/preferences'
    user_id = session.get('user_id', '')
    preference_controller = PreferencesController(g.db)
    if not user_id:
        return jsonify({'error': 'User ID is required'}), 400

    available_preferences = {
        'countries': preference_controller.get_available_countries(),
        'time_ranges': preference_controller.get_available_years(),
        'sport_types': preference_controller.get_available_sports()
    }
    print(available_preferences)
    user_preferences = {}
    # In a real scenario, replace the above with a request to the database or another service to fetch the actual preferences.

    data = {'available_preferences': available_preferences}
    data['user_preferences'] = user_preferences

    return render_template('preferences.html', data=data, user_id=user_id)
    # return jsonify(data)
