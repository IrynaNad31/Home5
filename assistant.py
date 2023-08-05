from collections import UserDict

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    pass

class Phone(Field):
    pass

class Record:
    def __init__(self, name_value):
        self.name = Name(name_value)
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

    def __str__(self):
        phones_str = ", ".join(map(str, self.phones))
        return f"Name: {self.name}, Phones: {phones_str}"

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
                    break  # Only add the record once if any phone matches
        return results

if __name__ == "__main__":
    # Example usage
    address_book = AddressBook()

    record1 = Record("John Doe")
    record1.add_phone("123-456-7890")
    record1.add_phone("987-654-3210")
    address_book.add_record(record1)

    record2 = Record("Jane Smith")
    record2.add_phone("555-123-4567")
    address_book.add_record(record2)

    # Search for records
    search_results = address_book.search_by_name("John Doe")
    for result in search_results:
        print(result)

    search_results = address_book.search_by_phone("987-654-3210")
    for result in search_results:
        print(result)
