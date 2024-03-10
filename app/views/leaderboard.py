from flask import render_template, session


def get_leaderboard():
    user_id = session.get('user_id', '')
    data = {
        "users": [{"user_id": 35, "user_name": "shaharl", "first_name": "Shahar", "last_name": "Linial", "points": 18},
                  {"user_id": 34, "user_name": "yahelj", "first_name": "Yahel", "last_name": "Jacobs", "points": 17},
                  {"user_id": 33, "user_name": "shayf", "first_name": "Shay", "last_name": "Franchi", "points": 16}
                  ]}
    return render_template('leaderboard.html', users=data['users'], user_id=user_id)
