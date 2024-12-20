import os
from datetime import datetime

class PhoneBook:
    book_file = "phonebook.txt"

    def __init__(self):
        self.entries = self.load_phonebook()

    def load_phonebook(self):
        if not os.path.exists(self.book_file):
            print("Phone book does not exist")
            return None
        phonebook = []
        with open(self.book_file, "r") as file:
            for line in file:
                parts = line.strip().split(";")
                if len(parts) == 4:
                    phonebook.append({
                        "name": parts[0],
                        "surname": parts[1],
                        "phone": parts[2],
                        "birth_date": parts[3] if parts[3] else None
                    })
        return phonebook

    def save_phonebook(self):
        with open(self.book_file, "w") as file:
            for person in self.entries:
                file.write(f"{person['name']};{person['surname']};{person['phone']};{person['birth_date'] or ''}\n")

    @staticmethod
    def validate_name(name):
        return name.isalnum() or " " in name

    @staticmethod
    def validate_phone(phone):
        if len(phone) == 11 and phone.isdigit():
            return phone
        if phone.startswith("+7") and len(phone) == 12:
            return "8" + phone[2:]
        return None

    @staticmethod
    def validate_date(date):
        try:
            datetime.strptime(date, "%d.%m.%Y")
            return True
        except ValueError:
            return False

    def find_person(self, name, surname):
        for person in self.entries:
            if person["name"] == name and person["surname"] == surname:
                return person
        return None

    def add_person(self):
        name = input("Enter name: ").capitalize()
        surname = input("Enter surname: ").capitalize()


        if self.find_person(name, surname):
            print("Contact already exists")                                             
            rewrite = input("Do you want to rewrite contact?\n[print 'y' - if yes or any other button to skip]: ")
            if rewrite == 'y':
                self.edit(self.find_person(name, surname))
            return

        phone = input("Enter phone number: ")
        validated_phone = self.validate_phone(phone)
        if not validated_phone:
            print("Invalid phone number")
            return

        birth_date = input("Enter birth date (DD.MM.YYYY) [to skip this step press 'Enter']: ")
        if birth_date and not self.validate_date(birth_date):
            print("Invalid birth date")
            return

        self.entries.append({
            "name": name,
            "surname": surname,
            "phone": validated_phone,
            "birth_date": birth_date if birth_date else None
        })
        print("Contact added")

    def delete_person(self):
        name = input("Enter name: ").capitalize()
        surname = input("Enter surname: ").capitalize()
        person = self.find_person(name, surname)

        if person:
            self.entries.remove(person)
            print("Contact deleted")
        else:
            print("Contact not found")
            
    def search_entries(self):
        queries = input("Enter search queries (separate by space): ").lower().split()
        queries = [query.strip() for query in queries]

        results = [person for person in self.entries if all(query in str(person).lower() for query in queries)]

        if results:
            for person in results:
                self.print_person(person)
        else:
            print("No results")

    def update_person(self):
        name = input("Enter name: ").capitalize()
        surname = input("Enter surname: ").capitalize()
        person = self.find_person(name, surname)

        if not person:
            print("Contact does not exist")
            return
        self.edit(person)
    
    def edit(self, person):
        print("Current contact data:", self.print_person(person))

        field = input("Which field to update? (name, surname, phone, birth_date): ")
        if field not in person:
            print("Invalid field")
            return

        new_value = input(f"Enter new value for {field}: ")
        if field in ("name", "surname"):
            new_value = new_value.capitalize()
        elif field == "phone":
            new_value = self.validate_phone(new_value)
            if not new_value:
                print("Invalid phone number")
                return
        elif field == "birth_date":
            if not self.validate_date(new_value):
                print("Invalid birth date")
                return

        person[field] = new_value
        print("Contact updated")

    def calculate_age(self):
        name = input("Enter name: ").capitalize()
        surname = input("Enter surname: ").capitalize()
        person = self.find_person(name, surname)

        if not person:
            print("Contact does not exist")
            return

        if not person["birth_date"]:
            print("Birth date not available for this person")
            return

        birth_date = datetime.strptime(person["birth_date"], "%d.%m.%Y")
        today = datetime.now()
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        print(f"Age: {age} years")

    def print_book(self):
        if not self.entries:
            print("Phonebook is empty")
            return
        print("Your phone contacts:")
        for person in self.entries:
            self.print_person(person)
    
    def print_person(self, person):
        print(f"{person["phone"]} - {person["name"]} {person["surname"]}", end=' ')
        if person["birth_date"]:
            print(f"({person["birth_date"]})")
        else:
            print()

class Interface:
    def __init__(self):
        self.phonebook = PhoneBook()
        
        self.operations = {
            "1": self.phonebook.print_book,
            "2": self.phonebook.search_entries,
            "3": self.phonebook.add_person,
            "4": self.phonebook.update_person,
            "5": self.phonebook.delete_person,
            "6": self.phonebook.calculate_age,
            "7": self.phonebook.save_phonebook,
            "8": self.quit
        }

    def run(self):        
        while True:
            print("\nPlease choose the number of the desired operation:")
            for key, value in self.operations.items():
                print(f"'{key}' - {value.__name__.replace('_', ' ').capitalize()}")
            command = input("Enter command: ")

            operation = self.operations.get(command)
            if operation:
                operation()
            else:
                print("Unknown command")

    def quit(self):
        self.phonebook.save_phonebook()
        print("Exiting")
        exit()


app = Interface()
if app.phonebook.entries != None:
    app.run()
