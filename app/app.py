import uuid

from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask import jsonify

from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
import uuid

from db.controllers import QuestionController
from db.connector import MySQLConnection

from flask import current_app, g

web_app = Flask(__name__)
web_app.secret_key = 'your_secret_key'


def get_db():
    host = 'localhost'
    user = 'root'
    password = 'root'
    database = 'mydatabase'
    #
    # # Create MySQL connection
    sql_connection = MySQLConnection(host, user, password, database)
    sql_connection.connect()

    if 'db' not in g:
        g.db = sql_connection

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.disconnect()


@web_app.route('/')
def index():
    user_id = session.get('user_id', '')
    return render_template('index.html', user_id=user_id)


@web_app.route('/about')
def about():
    user_id = session.get('user_id', '')
    return render_template('about.html', user_id=user_id)


@web_app.route('/api/data')
def get_data():
    data = {'message': 'Hello from Flask!'}
    return jsonify(data)


@web_app.route('/api/leaderboard')
def get_leaderboard():
    user_id = session.get('user_id', '')
    data = {"users":[{"user_id":35, "user_name": "shaharl", "first_name": "Shahar", "last_name": "Linial", "points": 18},
                     {"user_id": 34, "user_name": "yahelj", "first_name": "Yahel", "last_name": "Jacobs", "points": 17},
                     {"user_id":33, "user_name": "shayf", "first_name": "Shay", "last_name": "Franchi", "points": 16}
                     ]}
    return render_template('leaderboard.html', users=data['users'],user_id=user_id)


@web_app.route('/api/preferences', methods=['POST'])
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


@web_app.route('/api/preferences')
def get_preferences():
    # Simulating fetching data from '/api/preferences'
    user_id = session.get('user_id', '')

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
    data = {'available_preferences': available_preferences}
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
    # If preferences exist, return them; otherwise, return None or an empty structure as web_appropriate

    return example_preferences  # For demonstration, returning example preferences


@web_app.route('/api/question', methods=['GET'])
def get_question():
    # Simulating fetching a question from '/api/question'
    user_id = session.get('user_id', '')
    question_controller = QuestionController(g.db)


    user_id = session.get('user_id')
    user_id = 2
    # TODO : Move to general place
    if not user_id:
        return jsonify({'error': 'User ID is required'}), 400

    q = question_controller.get_question()
    return render_template('question.html', question=q.text, answers=q.answers, user_id=user_id)
    # return jsonify({'question': question, 'answers': answers})


def get_correct_answer_for_question(question_id):
    pass


def generate_question_by_id(question_id):
    pass


@app.route('/api/question', methods=['POST'])

def submit_answer():
    selected_answer = request.form['answer']
    user_id = request.form['user_id']
    question_id = request.form['question_id']
    correct_answer = get_correct_answer_for_question(question_id)
    correct = check_answer(selected_answer, question_id)

    if correct:
        update_user_score_in_db(user_id, 10)
        question, answers = generate_question_by_id(question_id)
    return render_template('question.html', question=question, answers=answers, user_id=user_id, correct_answer=correct_answer, submitted_answer=selected_answer, user_has_answered=True)


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


def generate_question_based_on_preferences(sql_connection, preferences):
    q, a = sql_connection.get_question()
    print(q, a)
    # Placeholder function to generate a question based on user preferences
    # Implement your question generation logic here based on the user's preferences
    question = f"Among the countries {', '.join(preferences['countries'])}, which one secured the most gold medals in {preferences['sport_types']}?"
    answer = 'USA'  # Example answer
    answer_type = 'countries'  # Example answer type
    return q, a, answer_type


def create_user_in_db(user_id, username, password, firstname, lastname):
    pass


@web_app.route('/signup', methods=['GET', 'POST'])
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
    return render_template('signup.html',user_id=session.get('user_id',''))



def get_user_by_username_from_db(username):
    return {
        'user_id': '123',
        'username': 'aaa',
        'hashed_password': 'scrypt:32768:8:1$QJfdYoBRpF3jcXmS$c7e5d023e06357af0ef948b228f81cc85848cae15d2f6c26a5245076edd211a02ff39bbcceed559b209f5d4b56511089e9312b1b62d8968aa5815a69c8976a36',
        'firstname': 'Shahar',
        'lastname': 'Linial'
    }


@web_app.route('/login', methods=['GET', 'POST'])
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


@web_app.route('/logout')
def logout():
    # Clear the user's session
    session.clear()
    flash('You have been logged out.', 'success')
    return redirect(url_for('index'))


@web_app.before_request
def before_request():
    get_db()


@web_app.teardown_request
def teardown_request(exception=None):
    close_db()


if __name__ == '__main__':
    web_app.run(host='0.0.0.0', port=5001, debug=True)
