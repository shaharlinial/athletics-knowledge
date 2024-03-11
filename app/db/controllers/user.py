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

        select_user_query = f"SELECT user_id, user_name, first_name, last_name, hashed_password, points FROM users where user_name = '{user_name}'"
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
            order by total_points desc;
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
