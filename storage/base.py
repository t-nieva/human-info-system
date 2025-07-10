from abc import ABC, abstractmethod
from person import Person

class BaseDatabase(ABC):

    @abstractmethod
    def add_person(self, person: Person):
        """Add a new person to the database"""
        pass

    @abstractmethod
    def list_all(self):
        """Return all stored people as a list of Person objects"""
        pass

    @abstractmethod
    def search(self, query: str):
        """Search people by full or partial name"""
        pass

    @abstractmethod
    def load_data(self):
        """Load data from storage"""
        pass

    @abstractmethod
    def save_data(self):
        """Save current data to storage"""
        pass
