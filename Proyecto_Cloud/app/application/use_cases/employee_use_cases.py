from typing import List, Optional
from app.domain.entities.employee import Employee
from app.application.dto.employee_dto import CreateEmployeeDTO, UpdateEmployeeDTO, EmployeeResponseDTO  # Cambiado
from app.infrastructure.repositories.employee_repository import EmployeeRepository

class EmployeeUseCases:
    def __init__(self, employee_repository: EmployeeRepository):
        self.employee_repository = employee_repository

    async def get_all_employees(self) -> List[EmployeeResponseDTO]:
        employees = await self.employee_repository.get_all()
        return [EmployeeResponseDTO(**employee.__dict__) for employee in employees]

    async def get_employee_by_id(self, employee_id: int) -> Optional[EmployeeResponseDTO]:
        employee = await self.employee_repository.get_by_id(employee_id)
        if employee:
            return EmployeeResponseDTO(**employee.__dict__)
        return None

    async def create_employee(self, employee_dto: CreateEmployeeDTO) -> EmployeeResponseDTO:
        employee = Employee(
            name=employee_dto.name,
            email=employee_dto.email,
            department=employee_dto.department,
            position=employee_dto.position,
            salary=employee_dto.salary,
            hire_date=employee_dto.hire_date
        )
        created_employee = await self.employee_repository.create(employee)
        return EmployeeResponseDTO(**created_employee.__dict__)

    async def update_employee(self, employee_id: int, employee_dto: UpdateEmployeeDTO) -> Optional[EmployeeResponseDTO]:
        employee = await self.employee_repository.get_by_id(employee_id)
        if not employee:
            return None
        
        update_data = employee_dto.dict(exclude_unset=True)
        updated_employee = await self.employee_repository.update(employee_id, update_data)
        return EmployeeResponseDTO(**updated_employee.__dict__)

    async def delete_employee(self, employee_id: int) -> bool:
        return await self.employee_repository.delete(employee_id)