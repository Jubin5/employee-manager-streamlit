"""employee_app package: a small Employee Management application.

Modules:
    models            - Employee data model
    utils             - validation and helper functions
    employee_service  - business logic (CRUD operations + JSON storage)
"""

from .models import Employee
from .employee_service import EmployeeService, DEFAULT_DATA_FILE

__all__ = ["Employee", "EmployeeService", "DEFAULT_DATA_FILE"]
__version__ = "1.0.0"