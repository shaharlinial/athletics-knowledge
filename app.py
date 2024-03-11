from flask import Flask
from app.db.connector import MySQLConnection
from flask import g
from app import views


web_app = Flask(__name__, template_folder='app/templates', static_folder='app/static')
web_app.secret_key = 'your_secret_key'
web_app.add_url_rule('/', view_func=views.home.index)
web_app.add_url_rule('/about', view_func=views.home.about)
web_app.add_url_rule('/api/leaderboard', view_func=views.leaderboard.get_leaderboard)
web_app.add_url_rule('/api/preferences', methods=['POST'], view_func=views.preferences.set_preferences)
web_app.add_url_rule('/api/preferences', methods=['GET'], view_func=views.preferences.get_preferences)
web_app.add_url_rule('/api/question', methods=['GET'], view_func=views.questions.get_question)
web_app.add_url_rule('/end_game', view_func=views.questions.end_game)
web_app.add_url_rule('/api/submit_answer', methods=['POST'], view_func=views.questions.submit_answer)
web_app.add_url_rule('/signup', methods=['GET', 'POST'], view_func=views.login.signup)
web_app.add_url_rule('/login',  methods=['GET', 'POST'], view_func=views.login.login)
web_app.add_url_rule('/logout', view_func=views.login.logout)

def update_preferences_in_db(user_id, country, start_time, end_time, sport_type):
    # Placeholder function to update preferences in the database
    # Implement database update logic here
    pass


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



def get_correct_answer_for_question(question_id):
    pass


def generate_question_by_id(question_id):
    pass

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


@web_app.before_request
def before_request():
    get_db()
    # Handle user id


@web_app.teardown_request
def teardown_request(exception=None):
    close_db()


if __name__ == '__main__':
    web_app.run(host='0.0.0.0', port=5001, debug=True)
