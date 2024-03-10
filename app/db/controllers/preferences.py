import typing

import mysql

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
        return [r[0] for r in results]

    def get_available_sports(self):
        cursor = self.db.connection.cursor()
        cursor.execute(
            """
            select sport_id, name from sports;
            """
        )
        results = cursor.fetchall()
        return [entities.Sport(*r) for r in results]

    def get_user_countries_preferences(self, user_id):
        cursor = self.db.connection.cursor()
        cursor.execute(
            f"""
            select countries.NOC, countries.name from country_preferences 
            inner join countries on countries.NOC = country_preferences.preference_value
            where country_preferences.user_id = {user_id};
            """
        )
        results = cursor.fetchall()
        return [entities.Country(*r) for r in results]

    def get_user_sports_preferences(self, user_id):
        cursor = self.db.connection.cursor()
        cursor.execute(
            f"""
                select sports.sport_id, sports.name from sports_preferences 
                inner join sports on sports.sport_id = sports_preferences.preference_value
                where sports_preferences.user_id = {user_id};
                """
        )
        results = cursor.fetchall()
        return [entities.Sport(*r) for r in results]

    def get_user_years_preferences(self, user_id):
        years = {'start': None, 'end':None}
        cursor = self.db.connection.cursor()
        cursor.execute(
                f"""
                select preference_value from year_preferences 
                where year_preferences.user_id = {user_id} and year_preferences.preference_param = 'start_year';
                """
        )
        results = cursor.fetchone()
        if results is not None:
            years['start'] = results[0]

        cursor.execute(
                f"""
                select preference_value from year_preferences 
                where year_preferences.user_id = {user_id} and year_preferences.preference_param = 'end_year';
                """
        )
        results = cursor.fetchone()
        if results is not None:
            years['end'] = results[0]
        return years

    def update_preferences(
            self,
            user_id: int,
            countries: typing.List[str],
            start_year: int,
            end_year: int,
            sports: typing.List[int]
    ):
        cursor = self.db.connection.cursor()
        try:
            # Start the transaction
            cursor.execute("START TRANSACTION")

            cursor.execute(f"DELETE FROM year_preferences WHERE user_id = {user_id}")

            # Your SQL statements go here
            if countries is not None and len(countries) > 0:
                cursor.execute(f"DELETE FROM country_preferences WHERE user_id = {user_id}")
                cursor.executemany("INSERT INTO country_preferences (user_id, preference_value) VALUES (%s, %s)",
                                   [(user_id, country) for country in countries])

            if sports is not None and len(sports) > 0:
                cursor.execute(f"DELETE FROM sports_preferences WHERE user_id = {user_id}")
                cursor.executemany("INSERT INTO sports_preferences (user_id, preference_value) VALUES (%s, %s)",
                                   [(user_id, sport) for sport in sports])

            if start_year is not None:
                cursor.execute(
                    "INSERT INTO year_preferences (user_id, preference_param ,preference_value) VALUES (%s, %s, %s)",
                    (user_id, 'start_year', start_year))

            if end_year is not None:
                cursor.execute(
                    "INSERT INTO year_preferences (user_id, preference_param ,preference_value) VALUES (%s, %s, %s)",
                    (user_id, 'end_year', end_year))

            # Commit the transaction if everything is successful
            cursor.execute("COMMIT")
            success = True
        except Exception as err:
            # An error occurred, rollback the transaction
            print(f"Error: {err}")
            cursor.execute("ROLLBACK")
            success = False

        return success
