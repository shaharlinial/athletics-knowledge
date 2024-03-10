import mysql.connector
from mysql.connector import Error


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
            raise

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
