from flask import render_template, request, session
from app.db import controllers
from flask import jsonify
from flask import g


def get_question():
    # Simulating fetching a question from '/api/question'
    user_id = session.get('user_id', '')
    question_controller = controllers.questions.QuestionController(g.db)

    if not user_id:
        return jsonify({'error': 'User ID is required'}), 400

    q = question_controller.generate_question(user_id)
    return render_template('question.html', question=q.text, answers=q.answers, question_id=q.id, user_id=user_id)
    # return jsonify({'question': question, 'answers': answers})from flask import g


#
def submit_answer():
    selected_answer = request.form['answer']  # 'USA'
    user_id = request.form['user_id']
    question_id = request.form['question_id']

    question_controller = controllers.questions.QuestionController(g.db)
    q = question_controller.get_question(user_id, question_id)
    correct = selected_answer == q.correct_answer
    question_controller.save_answer(question_id, user_id, selected_answer, correct)

    return render_template('question.html', question=q.text, answers=q.answers, user_id=user_id,
                           correct_answer=q.correct_answer, submitted_answer=selected_answer, user_has_answered=True)
