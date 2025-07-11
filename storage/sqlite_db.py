import sqlite3
from person import Person
from storage.base import BaseDatabase

class SQLiteDatabase(BaseDatabase):
    def __init__(self, db_name="people.db"):
        try:
            self.conn = sqlite3.connect(db_name)
            self.cursor = self.conn.cursor()
            self._create_table()
        except sqlite3.Error as e:
            raise Exception(f"[DB ERROR] Failed to connect to database: {e}") from e


    def _create_table(self):
        try:
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS people (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    first_name TEXT NOT NULL,
                    last_name TEXT,
                    middle_name TEXT,
                    gender TEXT NOT NULL,
                    birth_date TEXT NOT NULL,
                    death_date TEXT
                )
            ''')
            self.conn.commit()
        except sqlite3.Error as e:
            raise Exception(f"[DB ERROR] Failed to create table: {e}") from e


    def add_person(self, person: Person):
        try:
            self.cursor.execute('''
                INSERT INTO people (first_name, last_name, middle_name, gender, birth_date, death_date)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                person.first_name,
                person.last_name,
                person.middle_name,
                person.gender,
                person.birth_date.isoformat(),
                person.death_date.isoformat() if person.death_date else None
            ))
            self.conn.commit()
        except sqlite3.Error as e:
            raise Exception(f"[DB ERROR] Failed to add person: {e}") from e


    def list_all(self):
        try:
            self.cursor.execute('SELECT first_name, last_name, middle_name, gender, birth_date, death_date FROM people')
            rows = self.cursor.fetchall()
            return [
                Person(
                    first_name=row[0],
                    last_name=row[1],
                    middle_name=row[2],
                    gender=row[3],
                    birth_date=row[4],
                    death_date=row[5]
                )
                for row in rows
            ]
        except sqlite3.Error as e:
            raise Exception(f"[DB ERROR] Failed to retrieve people: {e}") from e

    def search(self, query: str):
        try:
            self.cursor.execute('''
                SELECT first_name, last_name, middle_name, gender, birth_date, death_date
                FROM people
            ''')
            rows = self.cursor.fetchall()
            query_lower = query.lower()

            results = []
            for row in rows:
                first = row[0] or ""
                last = row[1] or ""
                middle = row[2] or ""

                full_name = f"{first} {middle} {last}".lower()
                if query_lower in full_name:
                    results.append(Person(
                        first_name=first,
                        last_name=last,
                        middle_name=middle,
                        gender=row[3],
                        birth_date=row[4],
                        death_date=row[5]
                    ))

            return results

        except sqlite3.Error as e:
            raise Exception(f"[DB ERROR] Failed to search in database: {e}") from e


    def load_data(self):
        pass  # SQLite always reads from DB; no in-memory loading needed


    def save_data(self):
        pass  # SQLite automatically saves, but kept for compatibility


    def close(self):
        try:
            self.conn.close()
        except sqlite3.Error as e:
            raise Exception(f"[DB ERROR] Failed to close database: {e}") from e
