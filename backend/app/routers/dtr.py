from typing import List
from datetime import date
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.models.database import get_db, DTR, User
from app.core.security import get_current_user, get_current_admin
from app.schemas.schemas import DTRCreate, DTROut

router = APIRouter(prefix="/dtr", tags=["DTR"])


@router.get("/", response_model=List[DTROut])
def list_dtr(
    employee_id: int = Query(None),
    start_date: date = Query(None),
    end_date: date = Query(None),
    skip: int = 0,
    limit: int = 200,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    q = db.query(DTR)
    if employee_id:
        q = q.filter(DTR.employee_id == employee_id)
    if start_date:
        q = q.filter(DTR.work_date >= start_date)
    if end_date:
        q = q.filter(DTR.work_date <= end_date)
    return q.order_by(DTR.work_date.desc()).offset(skip).limit(limit).all()


@router.post("/", response_model=DTROut, status_code=201)
def create_dtr(
    data: DTRCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    existing = (
        db.query(DTR)
        .filter(DTR.employee_id == data.employee_id, DTR.work_date == data.work_date)
        .first()
    )
    if existing:
        raise HTTPException(status_code=400, detail="DTR already exists for this date")
    record = DTR(**data.model_dump())
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


@router.put("/{dtr_id}", response_model=DTROut)
def update_dtr(
    dtr_id: int,
    data: DTRCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    record = db.query(DTR).filter(DTR.id == dtr_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="DTR not found")
    for field, value in data.model_dump().items():
        setattr(record, field, value)
    db.commit()
    db.refresh(record)
    return record


@router.delete("/{dtr_id}", status_code=204)
def delete_dtr(
    dtr_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    record = db.query(DTR).filter(DTR.id == dtr_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="DTR not found")
    db.delete(record)
    db.commit()
    return None
