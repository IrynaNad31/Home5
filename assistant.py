import pickle 
from collections import UserDict
from datetime import datetime, timedelta

class Field:
    def __init__(self, value):
        self._value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        self.validate(new_value)
        self._value = new_value

    def validate(self, value):
        pass

    def __str__(self):
        return str(self._value)

class Phone(Field):
    def validate(self, value):
        if not value or not value.isdigit():
            raise ValueError("Invalid phone number")

class Birthday(Field):
    def validate(self, value):
        try:
            datetime.strptime(value, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Invalid birthday format. Please use YYYY-MM-DD")

class Name(Field):
    pass

class Record:
    def __init__(self, name_value, birthday_value=None):
        self.name = Name(name_value)
        self.birthday = Birthday(birthday_value) if birthday_value else None
        self.phones = []

    def add_phone(self, phone_value):
        phone = Phone(phone_value)
        self.phones.append(phone)

    def remove_phone(self, phone_value):
        self.phones = [phone for phone in self.phones if str(phone) != phone_value]

    def edit_phone(self, old_phone_value, new_phone_value):
        for phone in self.phones:
            if str(phone) == old_phone_value:
                phone.value = new_phone_value

    def days_to_birthday(self):
        if not self.birthday:
            return None
        today = datetime.today().date()
        next_birthday = datetime(today.year, self.birthday.value.month, self.birthday.value.day).date()
        if today > next_birthday:
            next_birthday = datetime(today.year + 1, self.birthday.value.month, self.birthday.value.day).date()
        return (next_birthday - today).days

    def __str__(self):
        phones_str = ", ".join(map(str, self.phones))
        birthday_str = f", Birthday: {self.birthday}" if self.birthday else ""
        return f"Name: {self.name}{birthday_str}, Phones: {phones_str}"

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[str(record.name)] = record

    def search_by_name(self, name):
        results = []
        for record in self.data.values():
            if str(record.name) == name:
                results.append(record)
        return results

    def search_by_phone(self, phone):
        results = []
        for record in self.data.values():
            for record_phone in record.phones:
                if str(record_phone) == phone:
                    results.append(record)
                    break 
        return results
    def save_to_file(self, filename):
        with open(filename, 'wb') as file:
            pickle.dump(self.data, file)

    def load_from_file(self, filename):
        try:
            with open(filename, 'rb') as file:
                self.data = pickle.load(file)
        except FileNotFoundError:
            pass

    def __iter__(self):
        return AddressBookIterator(self)

class AddressBookIterator:
    def __init__(self, address_book):
        self.address_book = address_book
        self.keys = list(self.address_book.data.keys())
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index < len(self.keys):
            key = self.keys[self.index]
            self.index += 1
            return self.address_book.data[key]
        raise StopIteration

if __name__ == "__main__":
    address_book = AddressBook()
    address_book.load_from_file('address_book_data.pkl')

    record1 = Record("John Doe", "1990-05-15")
    record1.add_phone("123-456-7890")
    record1.add_phone("987-654-3210")
    address_book.add_record(record1)

    record2 = Record("Jane Smith", "1985-10-20")
    record2.add_phone("555-123-4567")
    address_book.add_record(record2)

    search_results = address_book.search_by_name("John Doe")
    for result in search_results:
        print(result)

    search_results = address_book.search_by_phone("987-654-3210")
    for result in search_results:
        print(result)

    for record in address_book:
        days = record.days_to_birthday()
        if days is not None:
            print(f"{record.name}'s birthday is in {days} days")



     address_book.save_to_file('address_book_data.pkl')



