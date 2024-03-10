import uuid

from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask import jsonify

from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
import uuid

app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.route('/')
def index():
    user_id = session.get('user_id', '')
    return render_template('index.html', user_id=user_id)


@app.route('/about')
def about():
    user_id = session.get('user_id')
    return render_template('about.html',user_id=user_id)

@app.route('/contact')
def contact():
    user_id = session.get('user_id')
    return render_template('contact.html',user_id=user_id)

@app.route('/api/data')
def get_data():
    data = {'message': 'Hello from Flask!'}
    return jsonify(data)


@app.route('/api/leaderboard')
def get_leaderboard():
    user_id = session.get('user_id')
    data = {"users":[{"user_id":35, "user_name": "shaharl", "first_name": "Shahar", "last_name": "Linial", "points": 18},
                     {"user_id": 34, "user_name": "yahelj", "first_name": "Yahel", "last_name": "Jacobs", "points": 17},
                     {"user_id":33, "user_name": "shayf", "first_name": "Shay", "last_name": "Franchi", "points": 16}
                     ]}
    return render_template('leaderboard.html', users=data['users'],user_id=user_id)

@app.route('/api/preferences', methods=['POST'])
def set_preferences():
    # Extract form data
    user_id = request.form['user_id']
    country = request.form['country']
    start_time = request.form['start_time']
    end_time = request.form['end_time']
    sport_type = request.form['sport_type']

    # Update preferences in the database
    update_preferences_in_db(user_id, country, start_time, end_time, sport_type)

    # Redirect or show a success message
    return redirect(url_for('some_other_function'))

def update_preferences_in_db(user_id, country, start_time, end_time, sport_type):
    # Placeholder function to update preferences in the database
    # Implement database update logic here
    pass

@app.route('/api/preferences')
def get_preferences():
    # Simulating fetching data from '/api/preferences'
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'User ID is required'}), 400

    available_preferences = {
        'countries': ['USA', 'Canada', 'UK', 'Australia'],
        'time_ranges': [
            {'start': '1990', 'end': '2000'},
            {'start': '2000', 'end': '2010'},
            {'start': '2010', 'end': '2016'}
        ],
        'sport_types': ['Football', 'Basketball', 'Tennis', 'Soccer']
    }
    user_preferences = get_user_preferences(user_id)
    # In a real scenario, replace the above with a request to the database or another service to fetch the actual preferences.
    data={'available_preferences':available_preferences}
    if user_preferences:
        data['user_preferences'] = user_preferences
    return render_template('preferences.html', data=data, user_id=user_id)
    # return jsonify(data)

def get_user_preferences(user_id):
    # Placeholder function to simulate fetching user preferences from a database
    # Replace with actual database fetching logic
    # This example returns a set of preferences for demonstration
    example_preferences = {
        'user_id': user_id,
        'countries': ['USA', 'Canada'],
        'time_ranges': [{'start': '1990', 'end': '2016'}],
        'sport_types': ['Football', 'Basketball']
    }

    # In a real scenario, you would query your database to check if preferences exist for the given user_id
    # If preferences exist, return them; otherwise, return None or an empty structure as appropriate

    return example_preferences  # For demonstration, returning example preferences

@app.route('/api/question', methods=['GET'])
def get_question():
    # Simulating fetching a question from '/api/question'
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'User ID is required'}), 400

    # Fetch user preferences from the database
    user_preferences = get_user_preferences(user_id)
    # Generate a question based on preferences
    question, answer, answer_type = generate_question_based_on_preferences(user_preferences)

    # Fetch multiple-choice answers from the database based on answer type
    answers = get_multiple_choice_answers(answer, answer_type)
    # data={'question':question, 'answers':answers}
    # Return the question and answers
    return render_template('question.html', question=question, answers=answers, user_id=user_id)
    # return jsonify({'question': question, 'answers': answers})

@app.route('/api/question', methods=['POST'])

def update_user_score(user_id, question_id, user_answer):
    selected_answer = request.form['answer']
    user_id = request.form['user_id']  # Make sure to include this in your form as a hidden field
    question_id= request.form['question_id']
    correct = check_answer(selected_answer,question_id)  # Placeholder for your answer checking logic

    if correct:
        # Update points in the database
        update_user_score_in_db(user_id, 10)  # Placeholder for your database update logic
    #
    return render_template('answer_feedback.html', correct=correct, user_id=user_id)


def check_answer(selected_answer, question_id):
    # Placeholder function to check the selected answer against the correct answer in the database
    # Implement your answer checking logic here
    # This example always returns True for demonstration
    return True
def update_user_score_in_db(user_id, points):
    # Placeholder function to update the user's score in the database
    # Implement your database update logic here
    pass

def get_multiple_choice_answers(answer, answer_type):
    # Placeholder function to fetch multiple-choice answers from the database
    # Implement your database query logic here based on the answer type
    # Example return value:
    return ['Answer 1', 'Answer 2', 'Answer 3', 'Answer 4']

def generate_question_based_on_preferences(preferences):
    # Placeholder function to generate a question based on user preferences
    # Implement your question generation logic here based on the user's preferences
    question = f"Among the countries {', '.join(preferences['countries'])}, which one secured the most gold medals in {preferences['sport_types']}?"
    answer = 'USA'  # Example answer
    answer_type = 'countries'  # Example answer type
    return question, answer, answer_type


def create_user_in_db(user_id, username, password, firstname, lastname):
    pass


@app.route('/signup', methods=['GET', 'POST'])
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
    return render_template('signup.html',user_id=session.get('user_id'))


def get_user_by_username_from_db(username):
    return {
        'user_id': '123',
        'username': 'aaa',
        'hashed_password': 'scrypt:32768:8:1$QJfdYoBRpF3jcXmS$c7e5d023e06357af0ef948b228f81cc85848cae15d2f6c26a5245076edd211a02ff39bbcceed559b209f5d4b56511089e9312b1b62d8968aa5815a69c8976a36',
        'firstname': 'Shahar',
        'lastname': 'Linial'
    }


@app.route('/login', methods=['GET', 'POST'])
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

@app.route('/logout')
def logout():
    # Clear the user's session
    session.clear()
    flash('You have been logged out.', 'success')
    return redirect(url_for('index'))



if __name__ == '__main__':
    app.run(debug=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)