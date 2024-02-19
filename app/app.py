from flask import Flask, render_template, jsonify, redirect, url_for, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/api/data')
def get_data():
    data = {'message': 'Hello from Flask!'}
    return jsonify(data)


@app.route('/api/leaderboard')
def get_leaderboard():
    data = {"users":[{"user_id":35, "user_name": "shaharl", "first_name": "Shahar", "last_name": "Linial", "points": 18},
                     {"user_id": 34, "user_name": "yahelj", "first_name": "Yahel", "last_name": "Jacobs", "points": 17},
                     {"user_id":33, "user_name": "shayf", "first_name": "Shay", "last_name": "Franchi", "points": 16}
                     ]}
    return render_template('leaderboard.html', users=data['users'])

@app.route('/api/preferences', methods=['POST'])
def set_preferences():
    # Extract form data
    user_id = request.form['user_id']
    country = request.form['country']
    start_time = request.form['start_time']
    end_time = request.form['end_time']
    sport_type = request.form['sport_type']

    # Update preferences in the database
    update_preferences(user_id, country, start_time, end_time, sport_type)

    # Redirect or show a success message
    return redirect(url_for('some_other_function'))

def update_preferences(user_id, country, start_time, end_time, sport_type):
    # Placeholder function to update preferences in the database
    # Implement database update logic here
    pass

@app.route('/api/preferences')
def get_preferences():
    # Simulating fetching data from '/api/preferences'
    user_id = request.args.get('user_id', None)
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
    return render_template('preferences.html', data=data)
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
    user_id = request.args.get('user_id', None)
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
    return render_template('question.html', question=question, answers=answers)
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
    return render_template('answer_feedback.html', correct=correct)


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


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)