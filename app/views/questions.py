from flask import render_template, request, session
from app.db import controllers
from flask import jsonify
from flask import g

from app.db.controllers.user import UserController


def get_question():
    # Simulating fetching a question from '/api/question'
    user_id = session.get('user_id', '')
    question_controller = controllers.questions.QuestionController(g.db)
    preferences_controller = controllers.preferences.PreferencesController(g.db)

    if not user_id:
        return jsonify({'error': 'User ID is required'}), 400

    q = question_controller.generate_question(
        user_id,
        country_preferences=preferences_controller.get_user_countries_preferences(user_id),
        sports_preferences=preferences_controller.get_user_sports_preferences(user_id),
        years_preferences=preferences_controller.get_user_years_preferences(user_id)
    )
    return render_template('question.html', question=q.text, answers=q.answers, question_id=q.id, user_id=user_id)
    # return jsonify({'question': question, 'answers': answers})from flask import g


#
def submit_answer():
    selected_answer = request.form['answer']  # 'USA'
    user_id = request.form['user_id']
    question_id = request.form['question_id']
    preferences_controller = controllers.preferences.PreferencesController(g.db)

    question_controller = controllers.questions.QuestionController(g.db)
    q = question_controller.get_question(
        user_id, question_id,
        country_preferences=preferences_controller.get_user_countries_preferences(user_id),
        sports_preferences=preferences_controller.get_user_sports_preferences(user_id),
        years_preferences=preferences_controller.get_user_years_preferences(user_id)
    )

    correct = selected_answer == q.correct_answer
    question_controller.save_answer(question_id, user_id, selected_answer, correct)

    return render_template('question.html', question=q.text, answers=q.answers, user_id=user_id,
                           correct_answer=q.correct_answer, submitted_answer=selected_answer, user_has_answered=True)


# def end_game():
#     user_score = 100  # User's final score
#     correct_answers_count = 5  # How many answers were correct
#     total_questions = 10  # Total questions answered
#
#     return render_template('end_game.html', user_name="John Doe", user_score=user_score,
#                            correct_answers_count=correct_answers_count, total_questions=total_questions)


def end_game():
    user_id = session.get('user_id', '')
    user_controller = UserController(g.db)
    user = user_controller.fetch_user_by_id(
        user_id=user_id
    )

    user_score = user_controller.get_user_score(user_id)  # User's final score
    correct_answers_count =user_controller.count_user_correct_answers(user_id)    # How many answers were correct
    total_questions = user_controller.count_user_total_answers(user_id)  # Total questions answered


    return render_template('end_game.html', user_id=user_id, user_name=user.user_name, user_score=user_score,
                           correct_answers_count=correct_answers_count, total_questions=total_questions)

