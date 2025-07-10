import sqlite3
from person import Person
from storage.base import BaseDatabase

class SQLiteDatabase(BaseDatabase):
    def __init__(self, db_name="people.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.people = []
        self._create_table()


    def _create_table(self):
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


    def add_person(self, person: Person):
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
        self.people.append(person)


    def list_all(self):
        return self.people


    def search(self, query: str):
        query = query.lower()
        return [p for p in self.people if query in f"{p.first_name} {p.last_name} {p.middle_name}".lower()]


    def load_data(self):
        self.people.clear()
        self.cursor.execute('SELECT first_name, last_name, middle_name, gender, birth_date, death_date FROM people')
        rows = self.cursor.fetchall()
        for row in rows:
            person = Person(
                first_name=row[0],
                last_name=row[1],
                middle_name=row[2],
                gender=row[3],
                birth_date=row[4],
                death_date=row[5]
            )
            self.people.append(person)


    def save_data(self):
        pass  # SQLite automatically saves, but kept for compatibility
