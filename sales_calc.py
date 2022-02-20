# Sales Calc
# Lewis Shaw
#
#
# TODO:
# [x] - Load employees from file.
# [x] - Input number of properties sold by an employee.
# [x] - Calculate commission for employees.
# [x] - Calculate total commission pay.
# [x] - Calculate total number of properties sold.
# [x] - Apply a 15% bouns to employee with most sold properties.

import os
import csv

EMPLOYEE_FILE = "employees.csv"
isProgramRunning = True
hasProgramLoaded = False
lastMenuOptionSelected = 0
employees = []
currentEmployee = None

class Employee:
    id: int
    name: str
    propertiesSold: int = 0

    def __init__(self, id: str, name: str):
        self.id = id
        self.name = name

    def get_id(self) -> str:
        return self.id

    def get_name(self) -> str:
        return self.name

    def get_properties_sold(self) -> int:
        return self.propertiesSold

    def add_properties(self):
        self.propertiesSold += 1

    def get_commission(self) -> float:
        ranked = sort_employee_by_sales()
        commission = calculate_commission(self.get_properties_sold())

        if self.get_id() == ranked[0].get_id():
            commission = calculate_bonus(commission)

        return commission

def load_employees():
    global employees

    with open(EMPLOYEE_FILE, "r") as employeesFile:
        reader = csv.reader(employeesFile)

        for row in reader:
            id = row[0]
            name = row[1]
            employee = Employee(id, name)

            employees.append(employee)

        employeesFile.close()

currentEmployee: Employee

def main_menu():
    print_header("Main Menu")
    print("Current employee is", currentEmployee.get_name())
    new_line()

    print("1: Properties Sold")
    print("2: Calculate commission")
    print("3: Calculate total sales")
    print("4: Rank employees")
    print("5: Change employee")
    print("6: Exit")

    option = input("Select an option: ")

    if option == "1":
        show_menu(2)
    elif option == "2":
        show_menu(4)
    elif option == "4":
        show_menu(3)
    elif option == "5":
        show_menu(1)
    elif option == "3":
        show_menu(5)
    elif option == "6":
        exit_program()

def show_menu(menu: int):
    global lastMenuOptionSelected

    new_line()
    
    if menu == 0:
        main_menu()
        lastMenuOptionSelected = 0
    elif menu == 1:
        employee_menu()
        lastMenuOptionSelected = 1
    elif menu == 2:
        properties_sold_menu()
        lastMenuOptionSelected = 2
    elif menu == 3:
        rank_employees_menu()
        lastMenuOptionSelected = 3
    elif menu == 4:
        calculate_commission_menu()
        lastMenuOptionSelected = 4
    elif menu == 5:
        calculate_total_sales_menu()
        lastMenuOptionSelected = 5

def get_employee_by_id(target: str) -> Employee:
    length = len(employees)
    founded = False
    currentPos = 0
    employee = None
    
    while founded == False:
        for i in range(length):
            if employees[i].get_id() == target:
                currentPos = i
                founded = True
                employee = employees[i]

    return employee

def sort_employee_by_sales():
    length = len(employees)
    swapped = True
    currentPass = 0
    sortedList = []

    for employee in employees:
        sortedList.append(employee)

    while length > 0 and swapped == True:
        swapped = False
        length = length - 1

        for i in range(length):
            if sortedList[i].get_properties_sold() < sortedList[i+1].get_properties_sold():
                temp = sortedList[i]
                sortedList[i] = sortedList[i+1]
                sortedList[i+1] = temp
                swapped = True
                currentPass = currentPass + 1

    return sortedList

def properties_sold_menu():
    print_header("Properties Sold")

    print(currentEmployee.get_name(), "has sold", currentEmployee.get_properties_sold(), "properties")

    answer = input("Would you like to add properties? ")

    if answer == "yes" or answer == "Yes":
        ammount = int(input("How many properties sold? "))

        for x in range(ammount):
            currentEmployee.add_properties()
    else:
        show_menu(0)

def employee_menu():
    global currentEmployee
    
    print_header("Enter employee details")

    for employee in employees:
        print(employee.get_id(), ":", employee.get_name())

    employeeID = input("Enter employee ID: ")
    employee = get_employee_by_id(employeeID)
    
    if employee != None:
        currentEmployee = employee
        print("Current employee has been set to", currentEmployee.get_name())
        show_menu(0)
    else:
        handle_error("Can not find an employee with ID", employeeID)

def calculate_total_sales_menu():
    print_header("Total Sales")

    print(calculate_total_sales())
    

def rank_employees_menu():
    print_header("Employee Rank")

    for employee in sort_employee_by_sales():
        print(employee.get_name(), "with", employee.get_properties_sold(), "properties sold")

def calculate_commission_menu():
    print_header("Commission")

    for employee in sort_employee_by_sales():
        print(employee.get_name() + "'s commission is £" + str(employee.get_commission()))
        
    new_line()
    print("Total commission pay", "£" + str(calculate_total_commission_pay()))

def calculate_total_commission_pay() -> float:
    total = 0
    
    for employee in employees:
        total += employee.get_commission()

    return round(total, 2)

def calculate_total_sales() -> int:
    total = 0

    for employee in employees:
        total += employee.get_properties_sold()

    return total

def calculate_commission(properties: int) -> float:
    return round(500 * properties, 2)

def calculate_bonus(commission: float) -> float:
    bonus = commission / 100 * 15
    commission = commission + bonus

    return round(commission, 2)

def handle_error(error: str):
    clear_screen()
    
    new_line()
    print("Error:", error)
    show_menu(lastMenuOptionSelected)

def clear_screen():
    if os.name == "nt":
        _ = os.system("cls")
    else:
        _ = os.system("clear")

def new_line():
    print()

def print_header(title: str):
    print(title)
    print("=" * 25)
    new_line()

def exit_program():
    global isProgramRunning
    isProgramRunning = False
    exit()

def load_program():
    global hasProgramLoaded
    
    print("Loading...")
    load_employees()

    print(len(employees), "employee(s) loaded.")

    hasProgramLoaded = True

def program():
    if hasProgramLoaded == False:
        load_program()

    if currentEmployee == None:
        show_menu(1)
    else:
        show_menu(0)

while isProgramRunning:
    program()
