from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, render_template, request, redirect, url_for, flash, session
import uuid

def signup():
    if request.method == 'POST':
        username = request.form['username']
        # Hash the password provided by the user during signup
        hashed_password = generate_password_hash(request.form['password'])
        print(hashed_password)

        # Generate a unique userId
        user_id = str(uuid.uuid4())

        session['username'] = username
        session['user_id'] = user_id

        create_user_in_db(user_id, username, hashed_password, request.form['firstname'], request.form['lastname'])

        flash('User created successfully. Please login.', 'success')
        return redirect(url_for('index'))
    return render_template('signup.html', user_id=session.get('user_id', ''))


def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = get_user_by_username_from_db(username)
        if not user:
            flash('Login failed. Please check your credentials.', 'danger')
            return redirect(url_for('login'))

        # Check if the password provided matches the hashed password
        if check_password_hash(user['hashed_password'], password):
            session['user_id'] = user['user_id']
            flash('You were successfully logged in', 'success')
            return redirect(url_for('index'))
        else:
            flash('Login failed. Please check your credentials.', 'danger')
    return render_template('login.html')


def logout():
    # Clear the user's session
    session.clear()
    flash('You have been logged out.', 'success')
    return redirect(url_for('index'))
