from pydantic import BaseModel
from typing import Optional
from enum import Enum

class Department(str, Enum):
    IT = "IT"
    HR = "HR"
    FINANCE = "Finance"
    MARKETING = "Marketing"
    SALES = "Sales"
    OPERATIONS = "Operations"

class Employee(BaseModel):
    id: Optional[int] = None
    name: str
    email: str
    department: Department
    position: str
    salary: float
    hire_date: str

    class Config:
        from_attributes = True