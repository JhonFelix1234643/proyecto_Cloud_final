from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.domain.entities.employee import Employee, Department
from app.infrastructure.database.models import EmployeeModel

class EmployeeRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self) -> List[Employee]:
        result = await self.session.execute(select(EmployeeModel))
        employees = result.scalars().all()
        return [Employee(
            id=emp.id,
            name=emp.name,
            email=emp.email,
            department=emp.department,
            position=emp.position,
            salary=emp.salary,
            hire_date=emp.hire_date
        ) for emp in employees]

    async def get_by_id(self, employee_id: int) -> Optional[Employee]:
        result = await self.session.execute(
            select(EmployeeModel).where(EmployeeModel.id == employee_id)
        )
        employee = result.scalar_one_or_none()
        if employee:
            return Employee(
                id=employee.id,
                name=employee.name,
                email=employee.email,
                department=employee.department,
                position=employee.position,
                salary=employee.salary,
                hire_date=employee.hire_date
            )
        return None

    async def create(self, employee: Employee) -> Employee:
        db_employee = EmployeeModel(
            name=employee.name,
            email=employee.email,
            department=employee.department,
            position=employee.position,
            salary=employee.salary,
            hire_date=employee.hire_date
        )
        self.session.add(db_employee)
        await self.session.commit()
        await self.session.refresh(db_employee)
        return Employee(
            id=db_employee.id,
            name=db_employee.name,
            email=db_employee.email,
            department=db_employee.department,
            position=db_employee.position,
            salary=db_employee.salary,
            hire_date=db_employee.hire_date
        )

    async def update(self, employee_id: int, employee_data: dict) -> Optional[Employee]:
        result = await self.session.execute(
            select(EmployeeModel).where(EmployeeModel.id == employee_id)
        )
        db_employee = result.scalar_one_or_none()
        if db_employee:
            for key, value in employee_data.items():
                setattr(db_employee, key, value)
            await self.session.commit()
            await self.session.refresh(db_employee)
            return Employee(
                id=db_employee.id,
                name=db_employee.name,
                email=db_employee.email,
                department=db_employee.department,
                position=db_employee.position,
                salary=db_employee.salary,
                hire_date=db_employee.hire_date
            )
        return None

    async def delete(self, employee_id: int) -> bool:
        result = await self.session.execute(
            select(EmployeeModel).where(EmployeeModel.id == employee_id)
        )
        db_employee = result.scalar_one_or_none()
        if db_employee:
            await self.session.delete(db_employee)
            await self.session.commit()
            return True
        return False