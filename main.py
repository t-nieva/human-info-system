from person import Person
from storage.json_db import JsonDatabase
from storage.sqlite_db import SQLiteDatabase

def select_storage():
    print("Оберіть тип сховища:")
    print("1. JSON файл")
    print("2. SQLite база даних")
    choice_db = input("Ваш вибір (1/2): ").strip()
    if choice_db == "2":
        return SQLiteDatabase()
    else:
        return JsonDatabase()

db = select_storage()
db.load_data()

# **************** Console interface ****************
def print_menu():
    print("\nОберіть дію:")
    print("1. Додати людину")
    print("2. Пошук")
    print("3. Переглянути всі записи")
    print("4. Зберегти у файл")
    print("5. Завантажити з файлу")
    print("6. Вихід")

while True:
    print_menu()
    choice = input("Ваш вибір: ")

    if choice == "1":
        try:
            first_name = input("Ім'я (обов'язково): ").strip()
            if not first_name:
                raise ValueError("Ім'я обов'язкове")

            last_name = input("Прізвище (може бути порожнє): ").strip()
            middle_name = input("По-батькові (може бути порожнє): ").strip()
            gender = input("Стать (male/female): ").strip().lower()
            if gender not in ["male", "female"]:
                raise ValueError("Стать має бути 'male' або 'female'")

            birth_date = input("Дата народження (різні формати): ")
            death_date = input("Дата смерті (якщо є, інакше Enter): ").strip() or None

            person = Person(first_name, gender, birth_date, last_name, middle_name, death_date)
            db.add_person(person)
            print("Людину додано успішно!")

        except Exception as e:
            print(f"Помилка: {e}")

    elif choice == "2":
        query = input("Введіть текст для пошуку: ").strip()
        results = db.search(query)
        if results:
            for person in results:
                print("\n" + str(person))
        else:
            print("Нічого не знайдено.")

    elif choice == "3":
        people = db.list_all()
        if people:
            for person in people:
                print("\n" + str(person))
        else:
            print("База порожня.")

    elif choice == "4":
        db.save_data()
        print("Дані збережено у файл.")

    elif choice == "5":
        db.load_data()
        print("Дані завантажено з файлу.")

    elif choice == "6":
        print("До побачення!")
        break

    else:
        print("Невірний вибір. Спробуйте ще раз.")

