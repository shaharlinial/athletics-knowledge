import typing
from . import base_controller
from .. import entities


class PreferencesController(base_controller.BaseController):
    def __init__(self, sql_connection):
        super().__init__(sql_connection)

    def get_available_countries(self):
        pass

    def get_available_years(self):
        pass

    def get_available_sports(self):
        pass


    def get_available_preferences(
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
