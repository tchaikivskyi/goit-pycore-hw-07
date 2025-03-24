from datetime import datetime, timedelta

class Birthday:
    def __init__(self, value):
        try:
            self.value = datetime.strptime(value, "%d.%m.%Y").date()
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

class Record:
    def __init__(self, name):
        self.name = name
        self.birthday = None

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def days_to_birthday(self):
        if not self.birthday:
            return None
        today = datetime.today().date()
        next_birthday = self.birthday.value.replace(year=today.year)
        if next_birthday < today:
            next_birthday = next_birthday.replace(year=today.year + 1)
        return (next_birthday - today).days

class AddressBook:
    def __init__(self):
        self.records = {}

    def add_record(self, record):
        self.records[record.name] = record

    def get_upcoming_birthdays(self):
        today = datetime.today().date()
        upcoming_birthdays = []

        for record in self.records.values():
            if record.birthday:
                next_birthday = record.birthday.value.replace(year=today.year)
                if next_birthday < today:
                    next_birthday = next_birthday.replace(year=today.year + 1)

                delta_days = (next_birthday - today).days
                if 0 <= delta_days <= 7:
                    if next_birthday.weekday() in [5, 6]:
                        next_birthday += timedelta(days=(7 - next_birthday.weekday()))

                    upcoming_birthdays.append({
                        "name": record.name,
                        "congratulation_date": next_birthday.strftime("%Y.%m.%d")
                    })

        return upcoming_birthdays

book = AddressBook()
with open("task1/contacts.txt", "r") as file:
    for line in file:
        name, birthday = line.strip().split(",")
        record = Record(name)
        record.add_birthday(birthday)
        book.add_record(record)

upcoming_birthdays = book.get_upcoming_birthdays()
for birthday in upcoming_birthdays:
    print(f"{birthday['name']} - {birthday['congratulation_date']}")
