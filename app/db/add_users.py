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
                hashed_password=generate_password_hash(f"password{i}")
            )
            cursor.execute(
                f"""
                INSERT INTO users (user_name, first_name, last_name, hashed_password)
                VALUES ('{u.user_name}', '{u.first_name}', '{u.last_name}', '{u.hashed_password}');
                """
            )
            user_id = cursor.lastrowid
            for j in range(1, 10):
                cursor.execute(
                    f"""
                    INSERT INTO answers (user_id, question_id, answer_text, is_correct, points) 
                    VALUES ({user_id}, {j}, 'USA', {random.choice([True, False])}, {random.randint(0, 10)});
                    """
                )


if __name__ == '__main__':
    # # Create MySQL connection
    sql_connection = MySQLConnection()
    sql_connection.connect()

    fake_users_creator = FakeUsersCreator(sql_connection)
    fake_users_creator.create_fake_users(100)
    sql_connection.connection.commit()
    sql_connection.disconnect()