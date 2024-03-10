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

    def fetch_leaderboard(self, limit=10) -> typing.List[entities.User]:

        select_user_query = f"SELECT user_id, user_name, first_name, last_name, hashed_password, points FROM users ORDER BY points DESC LIMIT {limit}"
        try:
            result = self.db.fetch_data(select_user_query)
        except Exception:
            #  Duplicate user in database, retry please
            return False

        return [entities.User(*res) for res in result]
