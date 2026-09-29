"""Application entry point. Run with:  python main.py"""

from employee_app import EmployeeService, DEFAULT_DATA_FILE
from employee_app.utils import (
    prompt,
    print_employees,
    validate_id,
    validate_name,
    validate_department,
    validate_salary,
    validate_email,
)

MENU = """
========== Employee Management ==========
1. Add employee
2. Search employee
3. Update employee
4. Delete employee
5. Display all employees
6. Exit
=========================================="""


def add_employee(service: EmployeeService) -> None:
    print("\n-- Add Employee --")
    emp_id = prompt("Employee ID     : ", validate_id)
    name = prompt("Name            : ", validate_name)
    department = prompt("Department      : ", validate_department)
    salary = prompt("Salary          : ", validate_salary)
    email = prompt("Email           : ", validate_email)
    try:
        employee = service.add_employee(emp_id, name, department, salary, email)
        print(f"Added: {employee}")
    except ValueError as error:
        print(f"Could not add employee: {error}")


def search_employee(service: EmployeeService) -> None:
    print("\n-- Search Employee --")
    query = input("Enter ID, name or department: ")
    print_employees(service.search_employees(query))


def update_employee(service: EmployeeService) -> None:
    print("\n-- Update Employee --")
    emp_id = prompt("Employee ID to update: ", validate_id)
    try:
        current = service.get_employee(emp_id)
    except KeyError as error:
        print(error.args[0])
        return

    print("Press Enter to keep the current value.")
    name = prompt(f"Name [{current.name}]: ", validate_name, current.name)
    department = prompt(f"Department [{current.department}]: ", validate_department, current.department)
    salary = prompt(f"Salary [{current.salary}]: ", validate_salary, current.salary)
    email = prompt(f"Email [{current.email}]: ", validate_email, current.email)
    try:
        updated = service.update_employee(emp_id, name, department, salary, email)
        print(f"Updated: {updated}")
    except ValueError as error:
        print(f"Could not update employee: {error}")


def delete_employee(service: EmployeeService) -> None:
    print("\n-- Delete Employee --")
    emp_id = prompt("Employee ID to delete: ", validate_id)
    try:
        employee = service.get_employee(emp_id)
    except KeyError as error:
        print(error.args[0])
        return
    confirm = input(f"Delete {employee.name}? (y/n): ").strip().lower()
    if confirm == "y":
        service.delete_employee(emp_id)
        print("Employee deleted.")
    else:
        print("Delete cancelled.")


def display_employees(service: EmployeeService) -> None:
    print(f"\n-- All Employees ({service.count()}) --")
    print_employees(service.get_all_employees())


def main() -> None:
    service = EmployeeService(DEFAULT_DATA_FILE)  # loads data/employees.json
    print(f"Loaded {service.count()} saved employee(s).")
    actions = {
        "1": add_employee,
        "2": search_employee,
        "3": update_employee,
        "4": delete_employee,
        "5": display_employees,
    }
    while True:
        print(MENU)
        choice = input("Choose an option (1-6): ").strip()  
        if choice == "6":
            print("Goodbye!")
            break
        action = actions.get(choice)
        if action:
            action(service)
        else:
            print("Invalid choice. Please enter a number from 1 to 6.")


if __name__ == "__main__":
    main()