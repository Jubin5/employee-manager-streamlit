"""Employee data model. (Member 1)"""

from dataclasses import dataclass


@dataclass
class Employee:
    """Represents a single employee record."""

    emp_id: int
    name: str
    department: str
    salary: float
    email: str

    def __str__(self) -> str:
        return (
            f"[{self.emp_id}] {self.name} | {self.department} | "
            f"{self.salary:,.2f} | {self.email}"
        )

