
"""Business logic and CRUD operations. (Member 2)
 
Employees are kept in memory in a dict and, when a storage file is given,
saved to a JSON file after every change so data survives restarts.
"""
 
import json
import os
from dataclasses import asdict
from pathlib import Path
from typing import Dict, List, Optional, Union
 
from .models import Employee
from .utils import (
    validate_id,
    validate_name,
    validate_department,
    validate_salary,
    validate_email,
)
 
# <project root>/data/employees.json  (independent of the current working directory)
DEFAULT_DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "employees.json"
 
 
class EmployeeService:
    """Manages employees, keyed by employee ID.
 
    Pass `storage_file` to enable JSON persistence; leave it as None for a
    purely in-memory service.
    """
 
    def __init__(self, storage_file: Optional[Union[str, Path]] = None) -> None:
        self._employees: Dict[int, Employee] = {}
        self._storage_file: Optional[Path] = Path(storage_file) if storage_file else None
        if self._storage_file is not None:
            self._load()
 
    # ---- Persistence ----
    def _load(self) -> None:
        """Load employees from the JSON file (if it exists)."""
        if not self._storage_file.exists():
            return
        try:
            with open(self._storage_file, "r", encoding="utf-8") as file:
                records = json.load(file)
            self._employees = {
                int(item["emp_id"]): Employee(
                    emp_id=int(item["emp_id"]),
                    name=item["name"],
                    department=item["department"],
                    salary=float(item["salary"]),
                    email=item["email"],
                )
                for item in records
            }
        except (json.JSONDecodeError, KeyError, TypeError, ValueError):
            # Unreadable file: keep a backup copy and start with an empty list.
            backup = self._storage_file.with_suffix(".corrupt.json")
            os.replace(self._storage_file, backup)
            self._employees = {}
 
    def _save(self) -> None:
        """Write all employees to the JSON file (safe write via temp file)."""
        if self._storage_file is None:
            return
        self._storage_file.parent.mkdir(parents=True, exist_ok=True)
        temp_file = self._storage_file.with_suffix(".tmp")
        with open(temp_file, "w", encoding="utf-8") as file:
            json.dump([asdict(e) for e in self.get_all_employees()], file, indent=2)
        os.replace(temp_file, self._storage_file)
 
    # ---- Create ----
    def add_employee(self, emp_id, name, department, salary, email) -> Employee:
        emp_id = validate_id(emp_id)
        if emp_id in self._employees:
            raise ValueError(f"Employee ID {emp_id} already exists.")
        email = validate_email(email)
        if any(e.email == email for e in self._employees.values()):
            raise ValueError(f"Email {email} is already in use.")
 
        employee = Employee(
            emp_id=emp_id,
            name=validate_name(name),
            department=validate_department(department),
            salary=validate_salary(salary),
            email=email,
        )
        self._employees[emp_id] = employee
        self._save()
        return employee
 
    # ---- Read ----
    def get_employee(self, emp_id) -> Employee:
        emp_id = validate_id(emp_id)
        if emp_id not in self._employees:
            raise KeyError(f"No employee found with ID {emp_id}.")
        return self._employees[emp_id]
 
    def search_employees(self, query: str) -> List[Employee]:
        """Case-insensitive match on ID, name or department."""
        query = str(query).strip().lower()
        if not query:
            return []
        return [
            e for e in self.get_all_employees()
            if query == str(e.emp_id)
            or query in e.name.lower()
            or query in e.department.lower()
        ]
 
    def get_all_employees(self) -> List[Employee]:
        return sorted(self._employees.values(), key=lambda e: e.emp_id)
 
    # ---- Update ----
    def update_employee(self, emp_id, name=None, department=None,
                        salary=None, email=None) -> Employee:
        """Update only the fields that are provided (not None).
 
        All new values are validated first, so a bad value never leaves
        the record half-updated.
        """
        employee = self.get_employee(emp_id)
 
        new_name = validate_name(name) if name is not None else employee.name
        new_department = (validate_department(department)
                          if department is not None else employee.department)
        new_salary = validate_salary(salary) if salary is not None else employee.salary
        new_email = validate_email(email) if email is not None else employee.email
        if any(e.email == new_email and e.emp_id != employee.emp_id
               for e in self._employees.values()):
            raise ValueError(f"Email {new_email} is already in use.")
 
        employee.name = new_name
        employee.department = new_department
        employee.salary = new_salary
        employee.email = new_email
        self._save()
        return employee
 
    # ---- Delete ----
    def delete_employee(self, emp_id) -> Employee:
        employee = self.get_employee(emp_id)
        del self._employees[employee.emp_id]
        self._save()
        return employee
 
    def clear_all(self) -> None:
        """Remove every employee (and update the storage file)."""
        self._employees.clear()
        self._save()
 
    def count(self) -> int:
        return len(self._employees)
 
