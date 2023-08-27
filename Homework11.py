from ast import pattern
from collections import UserDict
from datetime import datetime, timedelta
import re

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
            pattern_for_phone=r'^\+?\d{11,16}$|^\d{10,12}$|^\+?\d{0,4}\(\d{3}\)\d{7,9}$|^\+?\d{0,4}\(\d{3}\)\d{1,3}-\d{1,3}-\d{1,3}$|^\(\d{3}\)\d{1,3}-\d{1,3}-\d{1,3}|^\d{3}-\d{1,3}-\d{1,3}-\d{1,3}$'
            if re.match(pattern_for_phone, value):
                self.__value=value
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
                raise ValueError("Invalid date format, format should be like 2000-01-31")


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


class AddressBook(UserDict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.page_size = 1 # Розмір однієї сторінки
        self.current_page = 0

    def __call__(self,n):
        if n:
            self.page_size = n  # Розмір однієї сторінки
        return self.__iter__()

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
        yield records

    def add_record(self, record):
        self.data[record.name.value] = record

    def iterator(self, n=None):
        try:
            generator = address_book(n)
            for records_list in generator:
                for records in records_list:
                    print(f"--------------PAGE {self.current_page}---------------")
                    for record in records:
                        print(f"|->Name: {record.name.value}")
                        for phone in record.phones:
                            print(f"|->Phone: {phone}")
                        for _ in record.birt_list:
                            print(f"|->Total days to Birthday: {record.days_to_birthday()}")
                        print("***********************************")
        except RuntimeError:
            return ">>>>>>>>>>>>>>>END<<<<<<<<<<<<<<<<<"



if __name__ == "__main__":
    address_book = AddressBook()
    record1 = Record("Dima Smith")
    record2 = Record("Jane Smith", "+38(098)5433521", "1959-08-26")
    record3 = Record("Jane", "2222876543210", "1925-10-6")
    record4 = Record("Dimasik", "2222876543210", "1925-08-24")
    record5 = Record("Ksusha", "22228765432510", "1925-08-07")
    record6 = Record("Vitalik", "22228754324310", "1925-08-18")

    address_book.add_record(record1)
    address_book.add_record(record2)
    address_book.add_record(record3)
    address_book.add_record(record4)
    address_book.add_record(record5)
    address_book.add_record(record6)

print(address_book.iterator(2))

