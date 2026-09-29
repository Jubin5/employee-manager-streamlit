"""Validation and helper functions. (Member 1)

Every validator returns the cleaned value or raises ValueError with a
readable message, so both the service layer and the UI can reuse them.
"""

import re

EMAIL_PATTERN = re.compile(r"^[\w.+-]+@[\w-]+(\.[\w-]+)+$")


def validate_id(value) -> int:
    try:
        emp_id = int(value)
    except (TypeError, ValueError):
        raise ValueError("Employee ID must be a whole number.")
    if emp_id <= 0:
        raise ValueError("Employee ID must be greater than zero.")
    return emp_id


def validate_name(value) -> str:
    name = str(value).strip()
    if len(name) < 2:
        raise ValueError("Name must have at least 2 characters.")
    if not all(ch.isalpha() or ch in " .'-" for ch in name):
        raise ValueError("Name may contain only letters, spaces, '.', '-' and apostrophes.")
    return name.title()


def validate_department(value) -> str:
    department = str(value).strip()
    if not department:
        raise ValueError("Department cannot be empty.")
    return department.title()


def validate_salary(value) -> float:
    try:
        salary = float(value)
    except (TypeError, ValueError):
        raise ValueError("Salary must be a number.")
    if salary <= 0:
        raise ValueError("Salary must be greater than zero.")
    return round(salary, 2)


def validate_email(value) -> str:
    email = str(value).strip().lower()
    if not EMAIL_PATTERN.match(email):
        raise ValueError("Email format is invalid (example: name@company.com).")
    return email


def prompt(message: str, validator, current=None):
    """Ask until the input passes `validator`.

    If `current` is given, pressing Enter keeps the current value
    (used by the update flow).
    """
    while True:
        raw = input(message).strip()
        if raw == "" and current is not None:
            return current
        try:
            return validator(raw)
        except ValueError as error:
            print(f"  Invalid input: {error}")


def print_employees(employees) -> None:
    """Print a list of employees as an aligned table."""
    if not employees:
        print("  No employees found.")
        return
    header = f"{'ID':<6}{'Name':<22}{'Department':<16}{'Salary':>12}  Email"
    print(header)
    print("-" * (len(header) + 12))
    for e in employees:
        print(f"{e.emp_id:<6}{e.name:<22}{e.department:<16}{e.salary:>12,.2f}  {e.email}")
