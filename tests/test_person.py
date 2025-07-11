import unittest
from datetime import date
from person import Person

class TestPerson(unittest.TestCase):

    def test_parse_date_formats(self):
        dates = [
            ("12.10.1980", date(1980, 10, 12)),
            ("11 10 2000", date(2000, 10, 11)),
            ("01/02/1995", date(1995, 2, 1)),
            ("3-9-2007", date(2007, 9, 3)),
            ("1990-03-03", date(1990, 3, 3)),
        ]
        for string, expected in dates:
            with self.subTest(date_string=string):
                self.assertEqual(Person.parse_date(string), expected)

    def test_invalid_date_format(self):
        with self.assertRaises(ValueError):
            Person.parse_date("invalid-date")

    def test_age_when_alive(self):
        p = Person("Іван", "male", "2000-01-01")
        today = date.today()
        expected_age = today.year - 2000
        if (today.month, today.day) < (1, 1):
            expected_age -= 1
        self.assertEqual(p.age, expected_age)

    def test_age_when_dead(self):
        p = Person("Марія", "female", "1990-01-01", death_date="2020-01-01")
        self.assertEqual(p.age, 30)

    def test_format_age_ending(self):
        cases = {
            "1 рік": ("2024-07-10", None),
            "2 роки": ("2023-07-10", None),
            "5 років": ("2020-07-10", None),
            "12 років": ("2013-07-11", None),
            "23 роки": ("2001-07-12", None),
        }
        today = date(2025, 7, 11)
        for expected, (birth, death) in cases.items():
            p = Person("Тест", "male", birth, death)
            p.age = p.calculate_age(today)
            self.assertEqual(p.format_age(), expected)


    def test_to_and_from_dict(self):
        data = {
            "first_name": "Олена",
            "last_name": "Петренко",
            "middle_name": "Іванівна",
            "gender": "female",
            "birth_date": "1995-01-01",
            "death_date": "2020-01-01"
        }
        p = Person.from_dict(data)
        self.assertEqual(p.first_name, "Олена")
        self.assertEqual(p.to_dict(), data)

if __name__ == '__main__':
    unittest.main()
