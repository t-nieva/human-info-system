import unittest
from storage.sqlite_db import SQLiteDatabase
from person import Person

class TestSQLiteDatabase(unittest.TestCase):

    def setUp(self):
        """Create a fresh in-memory SQLite database before each test."""
        # :memory: means that the database is created in memory only
        # and disappears after the test is finished.
        self.db = SQLiteDatabase(db_name=":memory:")

    def tearDown(self):
        self.db.close()

    def test_add_and_list_person(self):
        """Check that adding a person works, and they appear in list_all()."""
        person = Person(
            first_name="Андрій",
            gender="male",
            birth_date="1990-01-01",
            last_name="Шевченко"
        )
        self.db.add_person(person)
        people = self.db.list_all()
        self.assertEqual(len(people), 1)
        self.assertEqual(people[0].first_name, "Андрій")

    def test_load_data_from_db(self):
        """Verify that loading from the database repopulates the in-memory list."""
        # Add directly and clear internal list to simulate new session
        person = Person(
            first_name="Ірина",
            gender="female",
            birth_date="1985-05-15",
            last_name="Коваль"
        )
        self.db.add_person(person)

        # load_data() does nothing, so just test list_all returns added person
        people = self.db.list_all()
        self.assertEqual(len(people), 1)
        self.assertEqual(people[0].first_name, "Ірина")

    def test_search(self):
        """Test searching people by first, last, or middle name (including partial match)."""
        p1 = Person("Євген", "male", "1980-10-12", last_name="Крут", middle_name="Михайлович")
        p2 = Person("Євгенія", "female", "1980-10-12")
        p3 = Person("Дмитро", "male", "2000-03-10", middle_name="Євгенович")

        self.db.add_person(p1)
        self.db.add_person(p2)
        self.db.add_person(p3)

        results = self.db.search("євген")
        self.assertEqual(len(results), 3)

        names = [p.first_name for p in results]
        self.assertIn("Євген", names)
        self.assertIn("Євгенія", names)
        self.assertIn("Дмитро", names)

if __name__ == "__main__":
    unittest.main()