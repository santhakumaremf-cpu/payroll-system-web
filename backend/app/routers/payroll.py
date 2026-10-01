from typing import List
from decimal import Decimal
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.models.database import (
    get_db, Employee, Position, Payslip, PayrollPeriod,
    DeductionSetting, User
)
from app.core.security import get_current_user, get_current_admin
from app.schemas.schemas import (
    PayrollProcessRequest, PayslipOut, PayrollPeriodOut, DeductionSettingOut
)
from app.services.payroll_calculator import PayrollInput, calculate_payroll

router = APIRouter(prefix="/payroll", tags=["Payroll"])


@router.get("/periods", response_model=List[PayrollPeriodOut])
def list_periods(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(PayrollPeriod).order_by(PayrollPeriod.start_date.desc()).all()


@router.get("/deductions", response_model=List[DeductionSettingOut])
def list_deductions(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(DeductionSetting).filter(DeductionSetting.is_active == True).all()


@router.get("/payslips", response_model=List[PayslipOut])
def list_payslips(
    employee_id: int = None,
    period_id: int = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    q = db.query(Payslip)
    if employee_id:
        q = q.filter(Payslip.employee_id == employee_id)
    if period_id:
        q = q.filter(Payslip.period_id == period_id)
    return q.order_by(Payslip.date_processed.desc()).offset(skip).limit(limit).all()


@router.get("/payslips/{payslip_id}", response_model=PayslipOut)
def get_payslip(
    payslip_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    ps = db.query(Payslip).filter(Payslip.id == payslip_id).first()
    if not ps:
        raise HTTPException(status_code=404, detail="Payslip not found")
    return ps


@router.post("/process", response_model=PayslipOut, status_code=201)
def process_payroll(
    data: PayrollProcessRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    emp = db.query(Employee).filter(Employee.id == data.employee_id).first()
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    if emp.current_status != "Active":
        raise HTTPException(status_code=400, detail="Employee is not active")

    period = db.query(PayrollPeriod).filter(PayrollPeriod.id == data.period_id).first()
    if not period:
        raise HTTPException(status_code=404, detail="Payroll period not found")

    pos = db.query(Position).filter(Position.id == emp.position_id).first()
    if not pos:
        raise HTTPException(status_code=400, detail="Position not found")

    daily_rate = pos.regular_rate if emp.employment_status == "Regular" else pos.contractual_rate

    sss, pagibig, philhealth = data.sss, data.pagibig, data.philhealth
    if sss is None or pagibig is None or philhealth is None:
        settings = {d.name: d.amount for d in db.query(DeductionSetting).filter(DeductionSetting.is_active == True).all()}
        sss = sss if sss is not None else settings.get("SSS", Decimal("0"))
        pagibig = pagibig if pagibig is not None else settings.get("Pag-IBIG", Decimal("0"))
        philhealth = philhealth if philhealth is not None else settings.get("PhilHealth", Decimal("0"))

    result = calculate_payroll(PayrollInput(
        daily_rate=daily_rate,
        present_days=data.present_days,
        overtime_hours=data.overtime_hours,
        late_hours=data.late_hours,
        absences=data.absences,
        sss=sss,
        pagibig=pagibig,
        philhealth=philhealth,
        other_deductions=data.other_deductions,
    ))

    existing = db.query(Payslip).filter(
        Payslip.employee_id == data.employee_id, Payslip.period_id == data.period_id
    ).first()

    if existing:
        existing.present_days = data.present_days
        existing.overtime_hours = data.overtime_hours
        existing.late_hours = data.late_hours
        existing.absences = data.absences
        existing.daily_rate = result.daily_rate
        existing.basic_pay = result.basic_pay
        existing.overtime_pay = result.overtime_pay
        existing.gross_pay = result.gross_pay
        existing.sss = result.sss
        existing.pagibig = result.pagibig
        existing.philhealth = result.philhealth
        existing.other_deductions = result.other_deductions
        existing.total_deductions = result.total_deductions
        existing.net_pay = result.net_pay
        existing.processed_by = current_user.id
        existing.notes = data.notes
        db.commit()
        db.refresh(existing)
        return existing

    payslip = Payslip(
        employee_id=data.employee_id,
        period_id=data.period_id,
        present_days=data.present_days,
        overtime_hours=data.overtime_hours,
        late_hours=data.late_hours,
        absences=data.absences,
        daily_rate=result.daily_rate,
        basic_pay=result.basic_pay,
        overtime_pay=result.overtime_pay,
        gross_pay=result.gross_pay,
        sss=result.sss,
        pagibig=result.pagibig,
        philhealth=result.philhealth,
        other_deductions=result.other_deductions,
        total_deductions=result.total_deductions,
        net_pay=result.net_pay,
        processed_by=current_user.id,
        notes=data.notes,
    )
    db.add(payslip)
    db.commit()
    db.refresh(payslip)
    return payslip


@router.get("/payslips/{payslip_id}/pdf")
def download_payslip_pdf(
    payslip_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    from fastapi.responses import Response
    from app.services.payslip_pdf import generate_payslip_pdf

    ps = db.query(Payslip).filter(Payslip.id == payslip_id).first()
    if not ps:
        raise HTTPException(status_code=404, detail="Payslip not found")

    emp = db.query(Employee).filter(Employee.id == ps.employee_id).first()
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")

    pos = db.query(Position).filter(Position.id == emp.position_id).first()
    period = db.query(PayrollPeriod).filter(PayrollPeriod.id == ps.period_id).first()

    employee_dict = {
        "employee_no": emp.employee_no,
        "last_name": emp.last_name,
        "first_name": emp.first_name,
        "middle_name": emp.middle_name or "",
        "employment_status": emp.employment_status,
        "position_title": pos.title if pos else "-",
    }
    payslip_dict = {
        "basic_pay": ps.basic_pay, "overtime_pay": ps.overtime_pay,
        "gross_pay": ps.gross_pay, "sss": ps.sss, "pagibig": ps.pagibig,
        "philhealth": ps.philhealth, "other_deductions": ps.other_deductions,
        "total_deductions": ps.total_deductions, "net_pay": ps.net_pay,
        "present_days": ps.present_days, "overtime_hours": ps.overtime_hours,
        "late_hours": ps.late_hours, "absences": ps.absences,
        "daily_rate": ps.daily_rate,
        "date_processed": str(ps.date_processed) if ps.date_processed else "",
    }
    period_dict = None
    if period:
        period_dict = {"start_date": str(period.start_date), "end_date": str(period.end_date)}

    pdf_bytes = generate_payslip_pdf(
        employee=employee_dict, payslip=payslip_dict,
        period=period_dict, company_name="Payroll System",
    )
    filename = f"payslip_{emp.employee_no}_{payslip_id}.pdf"
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )
