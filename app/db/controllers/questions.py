from . import base_controller
from .. import entities


class QuestionController(base_controller.BaseController):

    def __init__(self, sql_connection):
        super().__init__(sql_connection)

    def generate_question(self, user_id) -> entities.question.Question:
        try:
            cursor = self.db.connection.cursor()
            cursor.execute(
                f"""
                select template_id, replace(template_query, '<user_id>', {user_id}), template_text INTO @question_id, @sql_txt, @sql_question from question_templates
                where template_id = (select count(*) from answers where user_id = {user_id}) + 1;
                """
            )
            cursor.execute(
                """
                PREPARE sql_query FROM @sql_txt
                """
            )
            cursor.execute(
                """
                EXECUTE sql_query;
                """
            )
            results = cursor.fetchall()
            answers = [r[0] for r in results]
            cursor.execute(
                """
                select @question_id, @sql_question;
                """
            )
            question_id, question_text = cursor.fetchone()

            # TODO: Shuffle Answers
            # TODO: from NOC to country
            return entities.question.Question(
                text=question_text,
                id=question_id,
                answers=answers,
                correct_answer=answers[0]
            )
        except Exception:
            raise

    def get_question(self, user_id, question_id) -> entities.question.Question:
        try:
            cursor = self.db.connection.cursor()
            cursor.execute(
                f"""
                select template_id, replace(template_query, '<user_id>', {user_id}), template_text INTO @question_id, @sql_txt, @sql_question from question_templates
                where template_id = {question_id};
                """
            )
            cursor.execute(
                """
                PREPARE sql_query FROM @sql_txt
                """
            )
            cursor.execute(
                """
                EXECUTE sql_query;
                """
            )
            results = cursor.fetchall()
            answers = [r[0] for r in results]
            cursor.execute(
                """
                select @question_id, @sql_question;
                """
            )
            question_id, question_text = cursor.fetchone()

            return entities.question.Question(
                text=question_text,
                id=question_id,
                answers=answers,
                correct_answer=answers[0]
            )
        except Exception:
            raise

    def save_answer(self, question_id, user_id, selected_answer, correct) -> bool:
        cursor = self.db.connection.cursor()
        try:
            # Start the transaction
            cursor.execute("START TRANSACTION")
            cursor.execute(f"""
                SELECT COALESCE((SELECT points FROM answers
                WHERE user_id = {user_id}
                ORDER BY answer_id DESC 
                LIMIT 1), 0) AS points
            """)
            result = cursor.fetchone()
            points = result[0]  # Assuming the result is a single value

            insert_answer_query = "INSERT INTO answers (user_id, question_id, answer_text, is_correct, points) VALUES (%s, %s, %s, %s, %s)"
            if correct:
                points += 10
            else:
                points = 0

            insert_data = (user_id, question_id, selected_answer, correct, points)
            cursor.execute(insert_answer_query, insert_data)
            # Commit the transaction if everything is successful
            cursor.execute("COMMIT")
            success = True
        except Exception as err:
            # An error occurred, rollback the transaction
            print(f"Error: {err}")
            cursor.execute("ROLLBACK")
            success = False

        return success
