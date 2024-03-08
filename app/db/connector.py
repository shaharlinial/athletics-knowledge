import mysql.connector
from mysql.connector import Error
import pandas as pd


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

    def execute_query(self, query):
        try:
            cursor = self.connection.cursor()
            cursor.execute(query)
            self.connection.commit()
            print("Query executed successfully")
        except Error as e:
            print(f"Error executing query: {e}")

    def executemany(self, query, values):
        try:
            cursor = self.connection.cursor()
            cursor.executemany(query, values)
            self.connection.commit()
            print("Query executed successfully")
        except Error as e:
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



# Define database connection parameters
host = 'localhost'
user = 'root'
password = 'root'
database = 'mydatabase'

# Create MySQL connection
mysql_connection = MySQLConnection(host, user, password, database)
mysql_connection.connect()

# database CSV file
csv_path = 'C:/Users/jacob/PycharmProjects/athletics-knowledge/data/athlete_events.csv'

# Import data
data_importer = DataImporter(csv_path)


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

if data_importer.table is not None:
    try:
        # Insert data into the athletes table in bulk
        athlete_values = [(row['ID'], row['Name'], row['Sex']) for index, row in data_importer.table.iterrows()]
        # remove duplicates
        athlete_values = list(set(athlete_values))
        athlete_query = "INSERT INTO athletes (athlete_id, name, sex) VALUES (%s, %s, %s)"
        mysql_connection.executemany(athlete_query, athlete_values)

        # Insert data into the teams table in bulk
        team_values = [(row['ID'], row['Team'], row['NOC']) for index, row in data_importer.table.iterrows()]
        team_query = "INSERT INTO teams (team_id, team_name, NOC) VALUES (%s, %s, %s)"
        mysql_connection.executemany(team_query, team_values)

        # Insert data into the olympics table in bulk
        olympics_values = [(row['ID'], row['Games'], row['Year'], row['Season'], row['City']) for index, row in data_importer.table.iterrows()]
        olympics_query = "INSERT INTO olympics (olympics_id, games, year, season, city) VALUES (%s, %s, %s, %s, %s)"
        mysql_connection.executemany(olympics_query, olympics_values)

        # Insert data into the events table in bulk
        events_values = [(row['ID'], row['ID'], row['Sport'], row['Event']) for index, row in data_importer.table.iterrows()]
        events_query = "INSERT INTO events (event_id, olympics_id, sport, event_name) VALUES (%s, %s, %s, %s)"
        mysql_connection.executemany(events_query, events_values)

        # Insert data into the athlete_events table in bulk
        athlete_events_values = [(row['ID'], row['ID'], row['ID'], row['Medal'], row['Weight'], row['Height'], row['Age']) for index, row in data_importer.table.iterrows()]
        athlete_events_query = "INSERT INTO athlete_events (athlete_id, team_id, event_id, medal, weight, height, age) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        mysql_connection.executemany(athlete_events_query, athlete_events_values)

        print("Data imported to MySQL successfully.")
    except Exception as e:
        print(f"Error importing data to MySQL: {e}")

else:
    print("No data loaded.")
