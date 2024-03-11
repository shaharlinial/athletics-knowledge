from werkzeug.security import generate_password_hash

from app.db.connector import MySQLConnection
from app.db.entities import User
import random


class FakeUsersCreator:
    def __init__(self, db: MySQLConnection):
        self.db = db

    def create_fake_users(self, number_of_users: int):
        cursor = self.db.connection.cursor()
        for i in range(number_of_users):
            u = User(
                id=i,
                user_name=f"user{i}",
                first_name=f"first{i}",
                last_name=f"last{i}",
                hashed_password=generate_password_hash(f"password{i}"),
                score=random.randint(0, 100)
            )
            cursor.execute(
                f"""
                INSERT INTO users (user_name, first_name, last_name, hashed_password, points)
                VALUES ('{u.user_name}', '{u.first_name}', '{u.last_name}', '{u.hashed_password}', {u.score});
                """
            )


if __name__ == '__main__':
    host = 'localhost'
    user = 'root'
    password = 'root'
    database = 'mydatabase'
    #
    # # Create MySQL connection
    sql_connection = MySQLConnection(host, user, password, database)
    sql_connection.connect()

    fake_users_creator = FakeUsersCreator(sql_connection)
    fake_users_creator.create_fake_users(100)
    sql_connection.connection.commit()
    sql_connection.disconnect()
