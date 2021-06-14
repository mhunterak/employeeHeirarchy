import copy

from flask import Flask

import models
from peewee import fn

app=Flask(__name__,static_url_path='/static')

indent = " | "
print_buffer = ""


def print_subordinates(employee, indent=" | "):
    global print_buffer
    indent += " | "
    subs = models.Employee.select().where(models.Employee.manager == employee.id)        
    for subordinate in subs:
        print_buffer += "<br>"+ indent + subordinate.name
        print_subordinates(subordinate, indent)

@app.route('/')
def hello_world():
    global print_buffer
    employees = models.Employee.select()
    for employee in employees:
        if employee.manager is None:
            print_buffer += "<br>"+ indent + employee.name
            print_subordinates(employee, indent)


    print_buffer += "<br> TOTAL SALARY " +str( models.Employee.select(fn.SUM(models.Employee.salary)).scalar())
    copy_print_buffer = copy.copy(print_buffer)
    print_buffer = ""
    return copy_print_buffer

@app.route('/alpha')
def alphabet():
    global print_buffer

    employees = models.Employee.select().order_by(models.Employee.name)
    for employee in employees:
        print_buffer+="<br>"+ indent + employee.name

    copy_print_buffer = copy.copy(print_buffer)
    print_buffer = ""
    return copy_print_buffer

if __name__=='__main__':
    models.initialize()
    app.run(debug=True, host='0.0.0.0', port=8000)
