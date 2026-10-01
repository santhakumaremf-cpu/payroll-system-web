from datetime import date, time, datetime
from decimal import Decimal
from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: str
    username: str


class LoginRequest(BaseModel):
    username: str
    password: str


class PositionBase(BaseModel):
    title: str
    contractual_rate: Decimal
    regular_rate: Decimal
    description: Optional[str] = None
    is_active: bool = True


class PositionCreate(PositionBase):
    pass


class PositionUpdate(BaseModel):
    title: Optional[str] = None
    contractual_rate: Optional[Decimal] = None
    regular_rate: Optional[Decimal] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None


class PositionOut(PositionBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class EmployeeBase(BaseModel):
    employee_no: str
    last_name: str
    first_name: str
    middle_name: Optional[str] = None
    gender: Optional[str] = None
    birth_date: Optional[date] = None
    birth_place: Optional[str] = None
    address: Optional[str] = None
    contact_no: Optional[str] = None
    position_id: int
    date_hired: Optional[date] = None
    employment_status: str = "Regular"
    current_status: str = "Active"
    sss_no: Optional[str] = None
    pagibig_no: Optional[str] = None
    philhealth_no: Optional[str] = None


class EmployeeCreate(EmployeeBase):
    pass


class EmployeeUpdate(BaseModel):
    last_name: Optional[str] = None
    first_name: Optional[str] = None
    middle_name: Optional[str] = None
    gender: Optional[str] = None
    birth_date: Optional[date] = None
    birth_place: Optional[str] = None
    address: Optional[str] = None
    contact_no: Optional[str] = None
    position_id: Optional[int] = None
    date_hired: Optional[date] = None
    employment_status: Optional[str] = None
    current_status: Optional[str] = None
    sss_no: Optional[str] = None
    pagibig_no: Optional[str] = None
    philhealth_no: Optional[str] = None


class EmployeeOut(EmployeeBase):
    id: int
    position: Optional[PositionOut] = None
    model_config = ConfigDict(from_attributes=True)


class DTRBase(BaseModel):
    employee_id: int
    work_date: date
    time_in: Optional[time] = None
    time_out: Optional[time] = None
    working_hours: Decimal = Decimal("0")
    overtime_hours: Decimal = Decimal("0")
    late_hours: Decimal = Decimal("0")
    status: str = "Present"
    notes: Optional[str] = None


class DTRCreate(DTRBase):
    pass


class DTROut(DTRBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class PayrollProcessRequest(BaseModel):
    employee_id: int
    period_id: int
    present_days: Decimal
    overtime_hours: Decimal = Decimal("0")
    late_hours: Decimal = Decimal("0")
    absences: Decimal = Decimal("0")
    sss: Optional[Decimal] = None
    pagibig: Optional[Decimal] = None
    philhealth: Optional[Decimal] = None
    other_deductions: Decimal = Decimal("0")
    notes: Optional[str] = None


class PayslipOut(BaseModel):
    id: int
    employee_id: int
    period_id: int
    present_days: Decimal
    overtime_hours: Decimal
    late_hours: Decimal
    absences: Decimal
    daily_rate: Decimal
    basic_pay: Decimal
    overtime_pay: Decimal
    gross_pay: Decimal
    sss: Decimal
    pagibig: Decimal
    philhealth: Decimal
    other_deductions: Decimal
    total_deductions: Decimal
    net_pay: Decimal
    date_processed: datetime
    notes: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)


class PayrollPeriodOut(BaseModel):
    id: int
    start_date: date
    end_date: date
    working_days: int
    status: str
    model_config = ConfigDict(from_attributes=True)


class DeductionSettingOut(BaseModel):
    id: int
    name: str
    amount: Decimal
    is_percentage: bool
    is_active: bool
    model_config = ConfigDict(from_attributes=True)
