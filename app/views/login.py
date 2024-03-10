from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, render_template, request, redirect, url_for, flash, session
import uuid
from app.db.controllers.user import UserController
from flask import g


def signup():
    if request.method == 'POST':
        username = request.form['username']
        firstname, lastname = request.form['firstname'], request.form['lastname']
        # Hash the password provided by the user during signup
        hashed_password = generate_password_hash(request.form['password'])

        # create_user_in_db(user_id, username, hashed_password, )
        user_id = UserController(g.db).register(
            username=username,
            first_name=firstname,
            hashed_password=hashed_password,
            last_name=lastname
        )

        session['user_id'] = user_id

        flash('User created successfully. Please login.', 'success')
        return redirect(url_for('index'))
    return render_template('signup.html', user_id=session.get('user_id', ''))


def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = UserController(g.db).fetch_user_by_username(
            user_name=username
        )
        if not user:
            print('User Not Found!')
            flash('Login failed. Please check your credentials.', 'danger')
            return redirect(url_for('login'))

        # Check if the password provided matches the hashed password
        if check_password_hash(user.hashed_password, password):
            session['user_id'] = user.id
            flash('You were successfully logged in', 'success')
            return redirect(url_for('index'))
        else:
            print('Invalid Passowrd!')
            flash('Login failed. Please check your credentials.', 'danger')
    return render_template('login.html')


def logout():
    # Clear the user's session
    session.clear()
    flash('You have been logged out.', 'success')
    return redirect(url_for('index'))
