import dataclasses
import math

import pandas as pd

from app.db.connector import MySQLConnection


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
    sport_id: int


@dataclasses.dataclass(frozen=True)
class Sport:
    name: str


@dataclasses.dataclass(frozen=True)
class AthleteEvent:
    athlete_id: int
    team_id: int
    event_id: int
    medal: str
    weight: int
    height: int
    age: int


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
    sports = {}
    sport_cur_id = 1
    athlete_events = set()

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

                sport = Sport(
                    name=row['Sport']
                )

                if sport not in sports:
                    sports[sport] = sport_cur_id
                    sport_cur_id += 1

                sport_id = sports[sport]

                ev = Event(
                    olympic_id=ol_id,
                    sport_id=sport_id,
                    name=row['Event']
                )
                if ev not in events:
                    events[ev] = ev_cur_id
                    ev_cur_id += 1
                event_id = events[ev]

                medal = 'NA'
                weight, height, age = None, None, None
                try:
                    if math.isnan(row['Medal']):
                        medal = 'NA'
                except Exception:
                    medal = row['Medal']
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

            sports_query = "INSERT INTO sports (sport_id, name) VALUES (%s, %s)"
            mysql_connection.insert_batch(
                batch_size=1000,
                query=sports_query,
                values=[(sport_id, sport.name) for sport, sport_id in sports.items()]
            )

            events_query = "INSERT INTO events (event_id, olympics_id, sport_id, event_name) VALUES (%s, %s, %s, %s)"
            mysql_connection.insert_batch(
                batch_size=1000,
                query=events_query,
                values=[(event_id, event.olympic_id, event.sport_id, event.name) for event, event_id in events.items()]
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
