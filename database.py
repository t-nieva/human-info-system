from person import Person
import json

class Database:

    def __init__(self):
        self.people = []  # Список об'єктів Person


    def add_person(self, person: Person):
        self.people.append(person)


    def list_all(self):
        return self.people

    @staticmethod
    def search(query: str):
        pass # Метод search(query: str) — нечіткий пошук у ПІБ


    def save_to_file(self, filename: str):
        with open(filename, "w", encoding="utf-8") as file:
            json.dump([person.to_dict() for person in self.people], file, ensure_ascii=False, indent=2)

    def load_from_file(self, filename: str):
        try:
            with open(filename, "r", encoding="utf-8") as file:
                data = json.load(file)
                self.people = [Person.from_dict(item) for item in data]
        except FileNotFoundError:
            self.people = []
