import dataclasses

import mysql.connector
from mysql.connector import Error
import pandas as pd

import math


class MySQLConnection:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            if self.connection.is_connected():
                print("Connected to MySQL database")
        except Error as e:
            print(f"Error connecting to MySQL database: {e}")

    def reconnect(self):
        self.disconnect()
        self.connect()

    def disconnect(self):
        if self.connection.is_connected():
            self.connection.close()
            print("Disconnected from MySQL database")

    def execute_query(self, query, values):
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, values)
            self.connection.commit()
            print("Query executed successfully")
            return cursor.lastrowid
        except Error as e:
            print(f"Error executing query: {e}")

    def insert_batch(self, batch_size: int, query: str, values):
        for i in range(0, len(values), batch_size):
            batch = values[i:i + batch_size]
            self.executemany(query, batch)

    def executemany(self, query, values):
        try:
            cursor = self.connection.cursor()
            cursor.executemany(query, values)
            self.connection.commit()
            print("Query executed successfully")
        except Error as e:
            print(query)
            print(values)
            print(f"Error executing query: {e}")

    def fetch_data(self, query):
        try:
            cursor = self.connection.cursor()
            cursor.execute(query)
            records = cursor.fetchall()
            return records
        except Error as e:
            print(f"Error fetching data: {e}")


# class DataImporter:
#     def __init__(self, mysql_connection):
#         self.mysql_connection = mysql_connection
#         self.table = None
#
#
#     def import_data(self, csv_url):
#         try:
#             # Read CSV file into a DataFrame
#             df = pd.read_csv(csv_url)
#
#             # Insert data into tables
#             for table_name in df.columns:
#                 df_table = df[[table_name]].drop_duplicates().dropna()
#                 df_table.to_sql(name=table_name, con=self.mysql_connection.connection, if_exists='append', index=False)
#
#             self.table = df
#             print("Data imported successfully.")
#         except Exception as e:
#             print(f"Error importing data: {e}")
#
#         import pandas as pd

class DataImporter:
    def __init__(self, path):
        self.path = path
        self.table = None
        self._load_data()

    def _load_data(self):
        try:
            self.table = pd.read_csv(self.path)
        except Exception as e:
            print(f"Error loading data from {self.path}: {e}")

    def show_table(self):
        if self.table is not None:
            print(self.table)
        else:
            print("No data loaded.")

    def get_column(self, column_name):
        if self.table is not None:
            if column_name in self.table.columns:
                return self.table[column_name]
            else:
                print(f"Column '{column_name}' not found.")
        else:
            print("No data loaded.")


# CREATE TABLE athletes (
#     athlete_id INT PRIMARY KEY,
#     name VARCHAR(255) NOT NULL,
#     sex ENUM('M', 'F', 'O')
# );
#
# CREATE TABLE teams (
#     team_id INT PRIMARY KEY,
#     team_name VARCHAR(255) NOT NULL,
#     NOC CHAR(3) NOT NULL
# );
#
# CREATE TABLE olympics (
#     olympics_id INT PRIMARY KEY,
#     games VARCHAR(255) NOT NULL,
#     year YEAR,
#     season ENUM('SUMMER', 'WINTER'),
#     city VARCHAR(255) NOT NULL
# );
#
# CREATE TABLE events (
#     event_id INT PRIMARY KEY,
#     olympics_id INT,
#     sport VARCHAR(255) NOT NULL,
#     event_name VARCHAR(255) NOT NULL,
#     FOREIGN KEY (olympics_id) REFERENCES olympics(olympics_id)
# );
#
# CREATE TABLE athlete_events (
#     athlete_id INT,
#     team_id INT,
#     event_id INT,
#     medal ENUM('GOLD', 'SILVER', 'BRONZE', 'NA'),
#     weight INT,
#     height INT,
#     age INT,
#     PRIMARY KEY (athlete_id, event_id),
#     FOREIGN KEY (athlete_id) REFERENCES athletes(athlete_id),
#     FOREIGN KEY (team_id) REFERENCES teams(team_id),
#     FOREIGN KEY (event_id) REFERENCES events(event_id)
# );
#


if __name__ == '__main__':
    # Define database connection parameters
    host = 'localhost'
    user = 'root'
    password = 'root'
    database = 'mydatabase'
    #
    # # Create MySQL connection
    mysql_connection = MySQLConnection(host, user, password, database)
    mysql_connection.connect()

    # # database CSV file
    from app import consts
    import os

    #
    csv_path = os.path.join(consts.DATA_DIR, 'athlete_events.csv')
    #
    #

    # Import data
    data_importer = DataImporter(csv_path)
    batch_size = 1000
    athletes = {}
    ath_cur_id = 1
    teams = {}
    team_cur_id = 1
    olympics = {}
    ol_cur_id = 1
    events = {}
    ev_cur_id = 1
    athlete_events = set()


    @dataclasses.dataclass(frozen=True)
    class Athlete:
        id: int
        name: str
        sex: str


    @dataclasses.dataclass(frozen=True)
    class Team:
        name: str
        noc: str


    @dataclasses.dataclass(frozen=True)
    class Olympic:
        game: str
        year: str
        season: str
        city: str


    @dataclasses.dataclass(frozen=True)
    class Event:
        olympic_id: int
        name: str
        sport: str


    @dataclasses.dataclass(frozen=True)
    class AthleteEvent:
        athlete_id: int
        team_id: int
        event_id: int
        medal: str
        weight: int
        height: int
        age: int


    if data_importer.table is not None:
        try:
            # Run in two steps: one - insert athletes, teams, events, olympics
            # Second Run: insert athlete events from re run.

            rows = data_importer.table.iterrows()
            for index, row in rows:

                ath = Athlete(
                    id=row['ID'],
                    name=row['Name'],
                    sex=row['Sex']
                )

                if ath not in athletes:
                    athletes[ath] = ath.id

                ath_id = athletes[ath]

                tea = Team(
                    name=row['Team'],
                    noc=row['NOC']
                )

                if tea not in teams:
                    teams[tea] = team_cur_id
                    team_cur_id += 1

                team_id = teams[tea]

                ol = Olympic(
                    game=row['Games'],
                    year=row['Year'],
                    season=row['Season'],
                    city=row['City']
                )
                if ol not in olympics:
                    olympics[ol] = ol_cur_id
                    ol_cur_id += 1

                ol_id = olympics[ol]

                ev = Event(
                    olympic_id=ol_id,
                    sport=row['Sport'],
                    name=row['Event']
                )
                if ev not in events:
                    events[ev] = ev_cur_id
                    ev_cur_id += 1
                event_id = events[ev]

                medal = 'NA'
                weight, height, age = None, None, None
                try:
                    if not math.isnan(row['Medal']):
                        medal = row['Medal']
                except Exception:
                    pass
                try:
                    if not math.isnan(row['Weight']):
                        weight = row['Weight']
                except Exception:
                    pass
                try:
                    if not math.isnan(row['Height']):
                        height = row['Height']
                except Exception:
                    pass
                try:
                    if not math.isnan(row['Age']):
                        age = row['Age']
                except Exception:
                    pass
                athev = athlete_events.add(
                    AthleteEvent(
                        athlete_id=ath_id,
                        team_id=team_id,
                        event_id=event_id,
                        medal=medal,
                        weight=weight,
                        height=height,
                        age=age
                    )
                )

            athlete_query = "INSERT INTO athletes (athlete_id, name, sex) VALUES (%s, %s, %s)"
            mysql_connection.insert_batch(
                batch_size=1000,
                query=athlete_query,
                values=[(athlete.id, athlete.name, athlete.sex) for athlete in athletes.keys()]
            )

            teams_query = "INSERT INTO teams (team_id, NOC, team_name) VALUES (%s, %s, %s)"
            mysql_connection.insert_batch(
                batch_size=1000,
                query=teams_query,
                values=[(team_id, team.noc, team.name) for team, team_id in teams.items()]
            )

            olympics_query = "INSERT INTO olympics (olympics_id, games, year, season, city) VALUES (%s, %s, %s, %s, %s)"
            mysql_connection.insert_batch(
                batch_size=1000,
                query=olympics_query,
                values=[(ol_id, olympic.game, olympic.year, olympic.season, olympic.city) for olympic, ol_id in
                        olympics.items()]
            )

            events_query = "INSERT INTO events (event_id, olympics_id, sport, event_name) VALUES (%s, %s, %s, %s)"
            mysql_connection.insert_batch(
                batch_size=1000,
                query=events_query,
                values=[(event_id, event.olympic_id, event.sport, event.name) for event, event_id in events.items()]
            )

            athlete_events_query = "INSERT INTO athlete_events (athlete_id, team_id, event_id, medal, weight, height, age) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            mysql_connection.insert_batch(
                batch_size=1000,
                query=athlete_events_query,
                values=[(athlete_event.athlete_id, athlete_event.team_id, athlete_event.event_id, athlete_event.medal,
                         athlete_event.weight, athlete_event.height, athlete_event.age) for athlete_event in
                        athlete_events]
            )

        except Exception as e:
            raise e

    else:
        print("No data loaded.")
