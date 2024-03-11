import typing

from . import base_controller
from .. import entities


class UserController(base_controller.BaseController):
    def __init__(self, sql_connection):
        super().__init__(sql_connection)

    def register(
            self,
            username: str,
            hashed_password: str,
            first_name: str,
            last_name: str
    ) -> int:

        insert_user_query = f"INSERT INTO users (user_name,hashed_password, first_name, last_name, points) VALUES (%s,%s, %s, %s, %s)"
        try:
            user_id = self.db.execute_query(
                insert_user_query,
                (username, hashed_password, first_name, last_name, 0)
            )
        except Exception:
            #  Duplicate user in database, retry please
            return False

        return user_id

    def fetch_user_by_username(
            self,
            user_name: str
    ) -> entities.User:

        select_user_query = f"SELECT user_id, user_name, first_name, last_name, hashed_password FROM users where user_name = '{user_name}'"
        try:
            result = self.db.fetch_data(select_user_query)[0]
        except Exception:
            #  Duplicate user in database, retry please
            return False

        return entities.User(*result)

    def fetch_leaderboard(self, limit=10) -> typing.List[typing.Dict]:

        leaderboard_query = f"""
            select users.user_id, users.first_name, users.last_name,sum(answers.points) as total_points from answers
            inner join users on users.user_id = answers.user_id
            group by answers.user_id
            order by total_points desc
            limit {limit};
        """
        try:
            result = self.db.fetch_data(leaderboard_query)
        except Exception:
            #  Duplicate user in database, retry please
            return False

        return [{
            'id': res[0],
            'first_name': res[1],
            'last_name': res[2],
            'score': res[3]
        } for res in result]

    def fetch_user_by_id(
            self,
            user_id: int
    ) -> entities.User:

        select_user_query = f"SELECT user_id, user_name, first_name, last_name, hashed_password FROM users where user_id = '{user_id}'"
        try:
            result = self.db.fetch_data(select_user_query)[0]
        except Exception:
            #  Duplicate user in database, retry please
            return False

        return entities.User(*result)

    def count_user_correct_answers(self, user_id: int) -> int:
        count_correct_answers_query = f"SELECT count(*) FROM answers where user_id = {user_id} and is_correct = 1"
        try:
            result = self.db.fetch_data(count_correct_answers_query)
        except Exception:
            #  user not found in database, retry please
            return False

        return result[0][0]

    def count_user_total_answers(self, user_id: int) -> int:
        count_total_answers_query = f"SELECT count(*) FROM answers where user_id = {user_id}"
        try:
            result = self.db.fetch_data(count_total_answers_query)
        except Exception:
            #  user not found in database, retry please
            return False

        return result[0][0]

    def get_user_score(self, user_id: int) -> int:
        user_score_query = f"SELECT sum(points) FROM answers where user_id = {user_id}"
        try:
            result = self.db.fetch_data(user_score_query)
        except Exception:
            #  user not found in database, retry please
            return False

        return result[0][0]

