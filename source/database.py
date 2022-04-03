from __future__ import annotations

from typing import Union

from mysql import connector


class Database:
    """
    Class handling all database related stuff.
    """

    connection: connector.MySQLConnection

    def __init__(self) -> None:

        self.create_database()
        self.initialise_connection()

    def create_database(self) -> None:
        """
        Creating the database in the MySQL server.
        """
        try:
            temp_conn: connector.CMySQLConnection = connector.connect(
                host="localhost", user="root"
            )
        except connector.errors.DatabaseError:
            raise BaseException(
                "Unable to connect to the MySQL server, check out the README for more information."
            )
        with temp_conn.cursor() as cursor:
            cursor.execute(
                """
                CREATE DATABASE IF NOT EXISTS school_project
                """
            )
        temp_conn.close()

    def initialise_connection(self) -> None:
        """
        Adding tables and creating a permanent connection to the database within the class.
        """
        conn: connector.CMySQLConnection = connector.connect(
            host="localhost", user="root", database="school_project"
        )
        with conn.cursor() as cursor:
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS quiz_data
                ( quiz TEXT, option1 TEXT, option2 TEXT, option3 TEXT, option4 TEXT, correct INT(1) )
                """
            )
        conn.commit()
        self.connection = conn

    def add_question(
        self,
        question: str,
        option1: str,
        option2: str,
        option3: str,
        option4: str,
        correct: int,
    ) -> None:
        """
        Method for adding new questions in the table.
        """
        with self.connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO quiz_data
                ( quiz, option1, option2, option3, option4, correct )
                VALUES ( %s, %s, %s, %s, %s, %s )
                """,
                (question, option1, option2, option3, option4, correct),
            )
        self.connection.commit()

    def get_questions(self, amount: int = 10) -> list[tuple(Union[str, int])]:
        """
        Getting `amount` number of questions from the table.
        """
        with self.connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT * FROM quiz_data
                """
            )
            data = cursor.fetchall()
        return data[:amount]

    @property
    def number_of_questions(self) -> int:
        """
        Check how many questions exist inside the table.
        """
        with self.connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT * FROM quiz_data
                """
            )
            data = cursor.fetchall()
        return len(data)


def setup() -> Database:
    return Database()
