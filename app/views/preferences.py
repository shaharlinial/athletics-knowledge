from flask import render_template, request, redirect, url_for, session, g
from flask import jsonify

from app.db.controllers.preferences import PreferencesController


def set_preferences():
    # Extract form data
    countries = request.form.getlist('countries')  # country_NOC
    start_year = request.form['start_time_range']  # start_year
    end_year = request.form['end_time_range']  # end_year
    sport_type = request.form.getlist('sport_type')  # sport_id
    user_id = session.get('user_id', '')
    preference_controller = PreferencesController(g.db)
    preference_controller.update_preferences(
        user_id=user_id,
        countries=countries,
        start_year=int(start_year),
        end_year=int(end_year),
        sports=sport_type
    )

    # Redirect or show a success message
    return redirect(url_for('get_preferences'))


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
    user_preferences = {
        'countries':  preference_controller.get_user_countries_preferences(user_id),
        'time_ranges': preference_controller.get_user_years_preferences(user_id),
        'sport_types': preference_controller.get_user_sports_preferences(user_id)
    }

    data = {
        'available_preferences': available_preferences,
        'user_preferences': user_preferences
    }


    return render_template('preferences.html', data=data, user_id=user_id)
