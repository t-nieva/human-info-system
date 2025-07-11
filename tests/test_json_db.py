import unittest
import os
from storage.json_db import JsonDatabase
from person import Person

class TestJsonDatabase(unittest.TestCase):
    def setUp(self):
        """Create a test file and an instance of the database before each test."""
        self.test_file = "test_people.json"
        self.db = JsonDatabase(filename=self.test_file)


    def tearDown(self):
        """Delete the test file after each test to avoid leaving unnecessary files."""
        if os.path.exists(self.test_file):
            os.remove(self.test_file)


    def test_add_and_list_person(self):
        """Check that adding a person and listing all people works correctly."""
        person = Person("Іван", "male", "2000-01-01", last_name="Іваненко")
        self.db.add_person(person)
        people = self.db.list_all()
        self.assertEqual(len(people), 1)
        self.assertEqual(people[0].first_name, "Іван")


    def test_save_and_load_data(self):
        """Verify that saving and loading data from a JSON file works correctly."""
        person = Person("Марія", "female", "1995-03-15", last_name="Петренко")
        self.db.add_person(person)
        self.db.save_data()

        # Create a new database instance that reads from the same file
        new_db = JsonDatabase(filename=self.test_file)
        new_db.load_data()
        people = new_db.list_all()
        self.assertEqual(len(people), 1)
        self.assertEqual(people[0].first_name, "Марія")
        self.assertEqual(people[0].last_name, "Петренко")


    def test_search(self):
        """Test searching by first name, last name, and middle name (including partial matches)."""
        p1 = Person("Євген", "male", "1980-10-12", last_name="Крут", middle_name="Михайлович", death_date="2001-10-11")
        p2 = Person("Євгенія", "female", "1980-10-12", death_date="2001-10-12")
        p3 = Person("Дмитро", "male", "2000-03-10", middle_name="Євгенович")

        self.db.add_person(p1)
        self.db.add_person(p2)
        self.db.add_person(p3)

        # Perform search
        results = self.db.search("євген")

        # Check that all 3 are matched
        self.assertEqual(len(results), 3)

        names = [p.first_name for p in results]
        self.assertIn("Євген", names)
        self.assertIn("Євгенія", names)
        self.assertIn("Дмитро", names)

if __name__ == "__main__":
    unittest.main()
