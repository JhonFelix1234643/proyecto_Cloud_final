from sqlalchemy import Column, Integer, String, Float, Enum as SQLEnum
from sqlalchemy.ext.declarative import declarative_base
from app.domain.entities.employee import Department

Base = declarative_base()

class EmployeeModel(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    department = Column(SQLEnum(Department), nullable=False)
    position = Column(String(100), nullable=False)
    salary = Column(Float, nullable=False)
    hire_date = Column(String(10), nullable=False)  # YYYY-MM-DD format