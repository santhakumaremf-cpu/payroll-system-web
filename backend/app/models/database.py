"""
SQLAlchemy models for modern Payroll System
"""

from datetime import datetime, date, time
from typing import Optional
from sqlalchemy import (
    create_engine, Column, Integer, String, Text, Boolean,
    Date, Time, DateTime, Numeric, ForeignKey, UniqueConstraint
)
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from sqlalchemy.sql import func

DATABASE_URL = "sqlite:///./payroll.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class Position(Base):
    __tablename__ = "positions"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), unique=True, nullable=False)
    contractual_rate = Column(Numeric(10, 2), nullable=False, default=0)
    regular_rate = Column(Numeric(10, 2), nullable=False, default=0)
    description = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    employees = relationship("Employee", back_populates="position")


class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    employee_no = Column(String(20), unique=True, nullable=False, index=True)
    last_name = Column(String(100), nullable=False)
    first_name = Column(String(100), nullable=False)
    middle_name = Column(String(100), nullable=True)
    gender = Column(String(10), nullable=True)
    birth_date = Column(Date, nullable=True)
    birth_place = Column(String(150), nullable=True)
    address = Column(Text, nullable=True)
    contact_no = Column(String(30), nullable=True)
    position_id = Column(Integer, ForeignKey("positions.id"), nullable=False)
    date_hired = Column(Date, nullable=True)
    employment_status = Column(String(20), nullable=False, default="Regular")
    current_status = Column(String(20), nullable=False, default="Active")
    sss_no = Column(String(30), nullable=True)
    pagibig_no = Column(String(30), nullable=True)
    philhealth_no = Column(String(30), nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    position = relationship("Position", back_populates="employees")
    dtr_records = relationship("DTR", back_populates="employee")
    payslips = relationship("Payslip", back_populates="employee")
    user = relationship("User", back_populates="employee", uselist=False)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(20), nullable=False, default="user")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    employee = relationship("Employee", back_populates="user")


class DeductionSetting(Base):
    __tablename__ = "deduction_settings"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)
    amount = Column(Numeric(10, 2), nullable=False, default=0)
    is_percentage = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)


class DTR(Base):
    __tablename__ = "dtr"
    __table_args__ = (UniqueConstraint("employee_id", "work_date", name="uq_employee_workdate"),)

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    work_date = Column(Date, nullable=False)
    time_in = Column(Time, nullable=True)
    time_out = Column(Time, nullable=True)
    working_hours = Column(Numeric(5, 2), default=0)
    overtime_hours = Column(Numeric(5, 2), default=0)
    late_hours = Column(Numeric(5, 2), default=0)
    status = Column(String(20), default="Present")
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, server_default=func.now())

    employee = relationship("Employee", back_populates="dtr_records")


class PayrollPeriod(Base):
    __tablename__ = "payroll_periods"

    id = Column(Integer, primary_key=True, index=True)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    working_days = Column(Integer, nullable=False, default=15)
    status = Column(String(20), default="Open")
    processed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, server_default=func.now())

    payslips = relationship("Payslip", back_populates="period")


class Payslip(Base):
    __tablename__ = "payslips"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    period_id = Column(Integer, ForeignKey("payroll_periods.id"), nullable=False)

    present_days = Column(Numeric(5, 2), default=0)
    overtime_hours = Column(Numeric(5, 2), default=0)
    late_hours = Column(Numeric(5, 2), default=0)
    absences = Column(Numeric(5, 2), default=0)

    daily_rate = Column(Numeric(10, 2), nullable=False)
    basic_pay = Column(Numeric(12, 2), nullable=False)
    overtime_pay = Column(Numeric(12, 2), default=0)
    gross_pay = Column(Numeric(12, 2), nullable=False)

    sss = Column(Numeric(10, 2), default=0)
    pagibig = Column(Numeric(10, 2), default=0)
    philhealth = Column(Numeric(10, 2), default=0)
    other_deductions = Column(Numeric(10, 2), default=0)
    total_deductions = Column(Numeric(12, 2), default=0)
    net_pay = Column(Numeric(12, 2), nullable=False)

    date_processed = Column(DateTime, server_default=func.now())
    processed_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    notes = Column(Text, nullable=True)

    employee = relationship("Employee", back_populates="payslips")
    period = relationship("PayrollPeriod", back_populates="payslips")


def init_db():
    Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
