import json

from flask import render_template, session, g, jsonify

from app.db.controllers.user import UserController


def get_leaderboard():
    user_id = session.get('user_id', '')
    data = UserController(g.db).fetch_leaderboard()
    return render_template('leaderboard.html', users=data, user_id=user_id)
