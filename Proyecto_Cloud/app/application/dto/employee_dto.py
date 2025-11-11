from pydantic import BaseModel
from typing import Optional
from app.domain.entities.employee import Department

class CreateEmployeeDTO(BaseModel):
    name: str
    email: str
    department: Department
    position: str
    salary: float
    hire_date: str

class UpdateEmployeeDTO(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    department: Optional[Department] = None
    position: Optional[str] = None
    salary: Optional[float] = None
    hire_date: Optional[str] = None

class EmployeeResponseDTO(BaseModel):
    id: int
    name: str
    email: str
    department: Department
    position: str
    salary: float
    hire_date: str

    class Config:
        from_attributes = True