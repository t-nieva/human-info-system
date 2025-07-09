from datetime import datetime, date
class Person:


    def __init__(self, first_name, gender, birth_date, last_name="", middle_name="", death_date=None):
        self.first_name = first_name
        self.last_name = last_name
        self.middle_name = middle_name
        self.gender = gender
        # Date normalization
        self.birth_date = self.parse_date(birth_date)
        self.death_date = self.parse_date(death_date) if death_date else None
        self.age = self.calculate_age()


    def __str__(self):
        full_name = f"{self.last_name} {self.first_name} {self.middle_name}".strip().title()
        if self.gender == "male":
            info = f"{full_name}, { self.format_age() }, чоловік.\nНародився {self.birth_date} "
            if self.death_date:
                info += f"Помер: {self.death_date}."
            return info
        elif self.gender == "female":
            info = f"{full_name}, { self.format_age() }, жінка.\nНародилася {self.birth_date} "
            if self.death_date:
                info += f"Померла: {self.death_date}."
            return info
        return None

    @staticmethod
    def parse_date(user_input: str)->date:
        # Додати метод для нормалізації дати (parse_date())
        """Parses a user input date string and returns it in date format."""
        formats = ["%Y-%m-%d", "%d.%m.%Y", "%d %m %Y", "%d/%m/%Y", "%d-%m-%Y"]
        for fmt in formats:
            try:
                return datetime.strptime(user_input.strip(), fmt).date()
            except ValueError:
                continue
        raise ValueError(f"Invalid date format: {user_input}")

    @staticmethod
    def from_dict(data: dict) -> 'Person':
        return Person(
            first_name=data["first_name"],
            gender=data["gender"],
            birth_date=data["birth_date"],
            last_name=data.get("last_name", ""),
            middle_name=data.get("middle_name", ""),
            death_date=data.get("death_date")
        )


    def to_dict(self)->dict:
        return {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "middle_name": self.middle_name,
            "gender": self.gender,
            "birth_date": self.birth_date.isoformat(),
            "death_date": self.death_date.isoformat() if self.death_date else None
        }


    def calculate_age(self)-> int:
        """Calculates age in full years (at death or today)."""
        end_date = self.death_date or date.today()
        age = end_date.year - self.birth_date.year
        # Якщо день народження ще не настав у цьому році — відняти 1
        if (end_date.month, end_date.day) < (self.birth_date.month, self.birth_date.day):
            age -= 1
        return age

    def format_age(self) -> str:
        """Returns age with correct Ukrainian word form: рік / роки / років."""
        age = self.age
        if 11 <= age % 100 <= 14:
            suffix = "років"
        else:
            last_digit = age % 10
            if last_digit == 1:
                suffix = "рік"
            elif last_digit in (2, 3, 4):
                suffix = "роки"
            else:
                suffix = "років"
        return f"{age} {suffix}"

