from flask import render_template, request, session
from app.db import controllers
from flask import jsonify

from flask import Blueprint
from flask import g


def get_question():
    # Simulating fetching a question from '/api/question'
    user_id = session.get('user_id', '')
    question_controller = controllers.questions.QuestionController(g.db)

    user_id = session.get('user_id')
    user_id = 2
    # TODO : Move to general place
    if not user_id:
        return jsonify({'error': 'User ID is required'}), 400

    q = question_controller.get_question()
    return render_template('question.html', question=q.text, answers=q.answers, user_id=user_id)
    # return jsonify({'question': question, 'answers': answers})from flask import g


#
def submit_answer():
    selected_answer = request.form['answer']  # 'USA'
    user_id = request.form['user_id']
    question_id = request.form['question_id']
    # correct_answer = get_correct_answer_for_question(question_id)
    # correct = check_answer(selected_answer, question_id)


    #
    # if correct:
    #     update_user_score_in_db(user_id, 10)
    #     question, answers = generate_question_by_id(question_id)
    return render_template('question.html', question=question, answers=answers, user_id=user_id,
                           correct_answer=correct_answer, submitted_answer=selected_answer, user_has_answered=True)