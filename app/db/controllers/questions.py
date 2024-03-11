from . import base_controller
from .. import entities


class QuestionController(base_controller.BaseController):

    def __init__(self, sql_connection):
        super().__init__(sql_connection)

    def generate_question(self, user_id, country_preferences, sports_preferences,
                          years_preferences) -> entities.question.Question:
        countries = "all countries"
        if len(country_preferences) > 0:
            countries = ",".join([c.name for c in country_preferences])

        sports = "all sports"
        if len(sports_preferences) > 0:
            sports = ",".join([s.name for s in sports_preferences])

        years = f"between {years_preferences['start']} and {years_preferences['end']}"

        try:
            cursor = self.db.connection.cursor()
            cursor.execute(
                """
                select 
                template_id,
                replace(template_query, '<user_id>', %s), 
                REPLACE(
                    REPLACE(
                        REPLACE(template_text, '[countries]', %s),
                        '[sports]', %s),
                    '[years]', %s)
                INTO @question_id, @sql_txt, @sql_question from question_templates
                where template_id = (select count(*) from answers where user_id = %s) + 1;
                """ , (user_id, countries, sports, years , user_id)
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
            return entities.question.Question(
                text=question_text,
                id=question_id,
                answers=answers,
                correct_answer=answers[0]
            )
        except Exception:
            raise

    def get_question(self, user_id, question_id, country_preferences, sports_preferences,
                     years_preferences) -> entities.question.Question:

        countries = "all countries"
        if len(country_preferences) > 0:
            countries = ",".join([c.name for c in country_preferences])

        sports = "all sports"
        if len(sports_preferences) > 0:
            sports = ",".join([s.name for s in sports_preferences])

        years = f"between {years_preferences['start']} and {years_preferences['end']}"

        try:
            cursor = self.db.connection.cursor()
            cursor.execute(
                """
                select 
                template_id,
                replace(template_query, '<user_id>', %s), 
                REPLACE(
                    REPLACE(
                        REPLACE(template_text, '[countries]', %s),
                        '[sports]', %s),
                    '[years]', %s)
                INTO @question_id, @sql_txt, @sql_question from question_templates
                where template_id = (select count(*) from answers where user_id = %s) + 1;
                """ , (user_id, countries, sports, years , user_id)
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
