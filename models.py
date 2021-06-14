import json

from peewee import (
    BlobField, BooleanField, CharField, DateTimeField,
    DoesNotExist, ForeignKeyField, IntegerField, IntegrityError,
    Model, MySQLDatabase, TextField, OperationalError)
from playhouse.sqlite_ext import SqliteDatabase


DATABASE = SqliteDatabase('app.db')

class Employee(Model):
    name = CharField(max_length=32, unique=True)
    salary = IntegerField(default=500)
    manager = ForeignKeyField(
        model='self',
        related_name='sub',
        backref='subordinate',
        null=True
        )

    class Meta:
        database = DATABASE

def initialize():
    DATABASE.create_tables(
        [
            Employee
        ],
        safe=True)
    data_loader()

def data_loader(path='./data.json'):
    file = open(path, "r")
    employee_list = json.loads(file.read())
    if Employee.select().count() <1:
        for employee in employee_list:
            try:
                new_employee = Employee.create(name=employee['name'], salary=employee['salary'], manager=None)
                new_employee.save()
            except:
                print("Not Loaded")
    for employee in employee_list:
        db_employee = Employee.get(Employee.name==employee['name'])
        if employee['manager'] is not None:
            if db_employee.manager is None:
                    manager = Employee.get(name=employee['manager'])
                    query = Employee.update(manager=manager).where(Employee.id == db_employee.id)
                    query.execute()
                    print("{} now has {}".format(db_employee.name, db_employee.manager))
