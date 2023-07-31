from os import getcwd
from os.path import join
import sqlite3

class DB:

    PATH_DB = join(getcwd(), 'data', 'contrasafer.db')
    TB_NAME = "data"

    def __init__(self) -> None:
        try:
            self._connection = sqlite3.connect(self.PATH_DB)
            self._cursor = self._connection.cursor()

            if self._not_exist_table():
                self._create_table()

            if self._not_exist_table():
                raise ValueError("Not exist table in database")

        except Exception as ex:
            raise ValueError(ex)

    # Get/Search data
    def get(self, columns: list, pk: int = None, search: str = None) -> list:
        selects = self._parse_columns(columns)
        query = f"SELECT {selects} FROM {self.TB_NAME}"

        # If the "pk" parameter isn't "None", set the query to search with ID
        if pk is not None:
            query += f" WHERE id = {pk}"

        # If the parameter "search" isn't "None", set the query to search using "LIKE" and convert it to lowercase
        if search is not None:
            query += f" WHERE LOWER(sitename) LIKE '%{search.lower()}%'"

        res = self._cursor.execute(query)

        return res.fetchall()

    # Insert data
    def insert(self, data: dict) -> None:
        columns = ""
        values = ""

        for key, item in data.items():
            columns += f"{key},"
            values += f"'{item}',"

        columns = columns.rstrip(",")
        values = values.rstrip(",")

        self._cursor.execute(f"INSERT INTO {self.TB_NAME}({columns}) VALUES({values})")
        self._connection.commit()

    # Update data
    def update(self, pk: int, data: dict) -> None:
        sets = ""

        for column, value in data.items():
            sets += f"{column} = '{value}',"

        sets = sets.rstrip(",")

        self._cursor.execute(f"UPDATE {self.TB_NAME} SET {sets} WHERE id = {pk}")
        self._connection.commit()

    # Delete data
    def delete(self, pk: int) -> None:
        self._cursor.execute(f"DELETE FROM {self.TB_NAME} WHERE id = {pk}")
        self._connection.commit()

    # Close cursor and connection
    def close_connection(self):
        self._cursor.close()
        self._connection.close()

    # Create tables
    def _create_table(self) -> None:
        self._cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS {self.TB_NAME} (
                id INTEGER PRIMARY KEY,
                sitename VARCHAR(60) NOT NULL,
                email VARCHAR(100) NOT NULL,
                username VARCHAR(60) NOT NULL,
                password VARCHAR NOT NULL,
                key VARCHAR NOT NULL
            )
        ''')

    # Check if exist table
    def _not_exist_table(self) -> bool:
        res = self._cursor.execute(f"SELECT name FROM sqlite_master WHERE name='{self.TB_NAME}'")

        return res.fetchone() is None

    # Parse columns name
    def _parse_columns(self, columns: list) -> str:
        selects = ""

        for column in columns:
            selects += f"{column},"

        return selects.rstrip(",")
