from collections import UserDict
from datetime import datetime, timedelta


class Field:
    def __init__(self, value):
        self.__value=None
        self.value=value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        self.__value = value


class Name(Field):
    pass

class Phone(Field):
    def __init__(self, value):
        self.__value=None
        self.value=value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        if value:
            if value.startswith("+") or value.startswith("0"):
                self.__value = value
            else:
                raise ValueError("Invalid phone number format")



class Birthday(Field):
    def __init__(self, value):
        self.__value = None
        self.value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        if value:
            try:
                datetime.strptime(value, "%Y-%m-%d")
                self.__value = value
            except ValueError:
                raise ValueError("Invalid date format")


class Record:
    def __init__(self, name: str, phone=None, birthday=None):
        self.name = Name(name)
        self.phones = []
        self.birt_list = []
        self.birthday=birthday
        if phone:
            self.add_phone(phone)
        if birthday:
            self.listb()

    def add_phone(self, phone):
        self.phones.append(Phone(phone).value)

    def listb(self):
        self.birt_list.append(Birthday(self.birthday).value)


    def remove_phone(self, phone):
        for p in self.phones:
            if p.get_value() == phone:
                self.phones.remove(p)

    def edit_phone(self, old_phone, new_phone):
        for p in self.phones:
            if p.get_value() == old_phone:
                p.set_value(new_phone)

    def days_to_birthday(self):
        today = datetime.today()
        birthday_date = datetime.strptime(self.birt_list[0], "%Y-%m-%d")
        next_birthday = birthday_date.replace(year=today.year)
        if next_birthday < today and next_birthday.day!=today.day:
            next_birthday = next_birthday.replace(year=today.year + 1)
        elif next_birthday < today and next_birthday.day==today.day:
            return f"0 days, congratulate today"
        days_left = (next_birthday - today).days
        return f"{days_left} days"


class AddressBook(UserDict,Record):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.page_size = 2  # Розмір однієї сторінки
        self.current_page = 0

    def __iter__(self):
        self.current_page = 0
        return self

    def __next__(self):
        start_idx = self.current_page * self.page_size
        end_idx = (self.current_page + 1) * self.page_size
        records = list(self.data.values())[start_idx:end_idx]
        if not records:
            raise StopIteration
        self.current_page += 1
        return records

    def add_record(self, record):
        self.data[record.name.value] = record



if __name__ == "__main__":
    address_book = AddressBook()
    record1 = Record("Dima Smith")
    record2 = Record("Jane Smith", "+876543210", "1959-08-26")
    record3 = Record("Jane", "+876543210", "1925-10-6")
    record4 = Record("Dimasik", "+876543210", "1925-08-24")
    record5 = Record("Ksusha", "+8765432510", "1925-08-07")
    record6 = Record("Vitalik", "+87654325434310", "1925-08-18")

    address_book.add_record(record1)
    address_book.add_record(record2)
    address_book.add_record(record3)
    address_book.add_record(record4)
    address_book.add_record(record5)
    address_book.add_record(record6)

    print(next(address_book))
    print(next(address_book))
    print(next(address_book))


    for records in address_book:
        for record in records:
            print(f"|->Name: {record.name.value}")
            for phone in record.phones:
                print(f"|->Phone: {phone}")
            for _ in record.birt_list:
                print(f"|->Total days to Birthday: {record.days_to_birthday()}")
            print("-----------------------------------")

