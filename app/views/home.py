from flask import render_template, session


def index():
    user_id = session.get('user_id', '')
    return render_template('index.html', user_id=user_id)


def about():
    user_id = session.get('user_id', '')
    return render_template('about.html', user_id=user_id)
