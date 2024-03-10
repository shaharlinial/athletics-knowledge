from .base_controller import BaseController
from ..entities.question import Question


class QuestionController(BaseController):

    def __init__(self, sql_connection):
        super().__init__(sql_connection)

    def get_question(self) -> Question:
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                """
                select template_query, template_text INTO @sql_txt, @sql_question from question_templates;
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
                select @sql_question;
                """
            )
            question = cursor.fetchone()[0]

            # TODO: Shuffle Answers
            return Question(
                text=question,
                answers=answers,
                correct_answer=answers[0]
            )
        except Exception:
            raise
