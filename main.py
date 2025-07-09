from person import Person
from database import Database

db = Database()
# first_name = input("first_name: ")
# last_name = input("last_name: ")
# middle_name = input("middle_name")
# gender = input("gender")
# birth_date = input("birth_date")

db.load_from_file("people.json")
people = db.list_all()
print(len(people))

