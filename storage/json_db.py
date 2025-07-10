import json
from person import Person
from storage.base import BaseDatabase

class JsonDatabase(BaseDatabase):
    def __init__(self, filename="people.json"):
        self.filename = filename
        self.people = []  # List of Person objects


    def add_person(self, person: Person):
        self.people.append(person)


    def list_all(self):
        return self.people


    def search(self, query: str):
        results = []
        query = query.lower()
        for person in self.people:
            full_name = f"{person.first_name} {person.last_name} {person.middle_name}".lower()
            if query in full_name:
                results.append(person)
        return results


    def load_data(self):
        try:
            with open(self.filename, "r", encoding="utf-8") as file:
                data = json.load(file)
                self.people = [Person.from_dict(d) for d in data]
        except FileNotFoundError:
            self.people = []


    def save_data(self):
        with open(self.filename, "w", encoding="utf-8") as file:
            json.dump([p.to_dict() for p in self.people], file, ensure_ascii=False, indent=2)
