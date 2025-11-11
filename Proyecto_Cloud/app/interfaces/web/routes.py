from fastapi import APIRouter, Request, Depends, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.database.database import get_db
from app.infrastructure.repositories.employee_repository import EmployeeRepository
from app.application.use_cases.employee_use_cases import EmployeeUseCases
from app.application.dto.employee_dto import CreateEmployeeDTO, UpdateEmployeeDTO
from app.domain.entities.employee import Department

router = APIRouter()

def get_employee_use_cases(db: AsyncSession = Depends(get_db)):
    employee_repository = EmployeeRepository(db)
    return EmployeeUseCases(employee_repository)

@router.get("/", response_class=HTMLResponse)
async def list_employees(request: Request, use_cases: EmployeeUseCases = Depends(get_employee_use_cases)):
    employees = await use_cases.get_all_employees()
    
    # Calculate statistics
    total_employees = len(employees)
    total_salary = sum(emp.salary for emp in employees)
    avg_salary = total_salary / total_employees if total_employees > 0 else 0
    
    return request.app.state.templates.TemplateResponse(
        "list.html", 
        {
            "request": request, 
            "employees": employees,
            "total_employees": total_employees,
            "total_salary": total_salary,
            "avg_salary": avg_salary,
            "Department": Department
        }
    )

@router.get("/create", response_class=HTMLResponse)
async def create_employee_form(request: Request):
    return request.app.state.templates.TemplateResponse(
        "create.html", 
        {
            "request": request,
            "departments": [dept.value for dept in Department]
        }
    )

@router.post("/create")
async def create_employee(
    request: Request,
    name: str = Form(...),
    email: str = Form(...),
    department: str = Form(...),
    position: str = Form(...),
    salary: float = Form(...),
    hire_date: str = Form(...),
    use_cases: EmployeeUseCases = Depends(get_employee_use_cases)
):
    employee_dto = CreateEmployeeDTO(
        name=name,
        email=email,
        department=Department(department),
        position=position,
        salary=salary,
        hire_date=hire_date
    )
    await use_cases.create_employee(employee_dto)
    return RedirectResponse(url="/", status_code=303)

@router.get("/edit/{employee_id}", response_class=HTMLResponse)
async def edit_employee_form(
    request: Request, 
    employee_id: int, 
    use_cases: EmployeeUseCases = Depends(get_employee_use_cases)
):
    employee = await use_cases.get_employee_by_id(employee_id)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    return request.app.state.templates.TemplateResponse(
        "edit.html", 
        {
            "request": request, 
            "employee": employee,
            "departments": [dept.value for dept in Department]
        }
    )

@router.post("/edit/{employee_id}")
async def update_employee(
    request: Request,
    employee_id: int,
    name: str = Form(...),
    email: str = Form(...),
    department: str = Form(...),
    position: str = Form(...),
    salary: float = Form(...),
    hire_date: str = Form(...),
    use_cases: EmployeeUseCases = Depends(get_employee_use_cases)
):
    employee_dto = UpdateEmployeeDTO(
        name=name,
        email=email,
        department=Department(department),
        position=position,
        salary=salary,
        hire_date=hire_date
    )
    await use_cases.update_employee(employee_id, employee_dto)
    return RedirectResponse(url="/", status_code=303)

@router.get("/delete/{employee_id}", response_class=HTMLResponse)
async def delete_employee_form(
    request: Request, 
    employee_id: int, 
    use_cases: EmployeeUseCases = Depends(get_employee_use_cases)
):
    employee = await use_cases.get_employee_by_id(employee_id)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    return request.app.state.templates.TemplateResponse(
        "delete.html", 
        {
            "request": request, 
            "employee": employee
        }
    )

@router.post("/delete/{employee_id}")
async def delete_employee(
    request: Request,
    employee_id: int,
    use_cases: EmployeeUseCases = Depends(get_employee_use_cases)
):
    await use_cases.delete_employee(employee_id)
    return RedirectResponse(url="/", status_code=303)