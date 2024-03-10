import typing
from . import base_controller
from .. import entities


class PreferencesController(base_controller.BaseController):
    def __init__(self, sql_connection):
        super().__init__(sql_connection)

    def get_available_countries(self):
        cursor = self.db.connection.cursor()
        cursor.execute(
            """
            select NOC, name from countries;
            """
        )
        results = cursor.fetchall()
        return [entities.Country(*r) for r in results]

    def get_available_years(self):
        cursor = self.db.connection.cursor()
        cursor.execute(
            """
            select distinct(year) from olympics order by year asc;
            """
        )
        results = cursor.fetchall()
        return [r for r in results]

    def get_available_sports(self):
        cursor = self.db.connection.cursor()
        cursor.execute(
            """
            select sport_id, name from sports;
            """
        )
        results = cursor.fetchall()
        return [entities.Sport(*r) for r in results]

