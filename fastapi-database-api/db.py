import psycopg2
from psycopg2 import sql

class ConnectionDB:
    def __init__(self, login, password, database):
        self.connect = psycopg2.connect(
            user=login,
            password=password,
            database=database
        )
        self.cursor = self.connect.cursor()

    def fetch_all_people(self):
        """Возвращает все данные из таблицы 'people'."""
        query = "SELECT * FROM people"
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        return [dict((self.cursor.description[i][0], value) for i, value in enumerate(row)) for row in rows]

    def fetch_ten_people(self):
        """Возвращает первые 10 строк из таблицы 'people'."""
        query = "SELECT * FROM people LIMIT 10"
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        return [dict((self.cursor.description[i][0], value) for i, value in enumerate(row)) for row in rows]

    def search_by_name(self, name):
        """Поиск людей по имени в таблице 'people'."""
        query = "SELECT * FROM people WHERE name = %s"
        self.cursor.execute(query, (name,))
        rows = self.cursor.fetchall()
        return [dict((self.cursor.description[i][0], value) for i, value in enumerate(row)) for row in rows]
