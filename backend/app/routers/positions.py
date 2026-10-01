from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.models.database import get_db, Position
from app.core.security import get_current_user, get_current_admin
from app.schemas.schemas import PositionCreate, PositionUpdate, PositionOut
from app.models.database import User

router = APIRouter(prefix="/positions", tags=["Positions"])


@router.get("/", response_model=List[PositionOut])
def list_positions(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(Position).offset(skip).limit(limit).all()


@router.get("/{position_id}", response_model=PositionOut)
def get_position(
    position_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    pos = db.query(Position).filter(Position.id == position_id).first()
    if not pos:
        raise HTTPException(status_code=404, detail="Position not found")
    return pos


@router.post("/", response_model=PositionOut, status_code=201)
def create_position(
    data: PositionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    if db.query(Position).filter(Position.title == data.title).first():
        raise HTTPException(status_code=400, detail="Position title already exists")
    pos = Position(**data.model_dump())
    db.add(pos)
    db.commit()
    db.refresh(pos)
    return pos


@router.put("/{position_id}", response_model=PositionOut)
def update_position(
    position_id: int,
    data: PositionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    pos = db.query(Position).filter(Position.id == position_id).first()
    if not pos:
        raise HTTPException(status_code=404, detail="Position not found")
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(pos, field, value)
    db.commit()
    db.refresh(pos)
    return pos


@router.delete("/{position_id}", status_code=204)
def delete_position(
    position_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    pos = db.query(Position).filter(Position.id == position_id).first()
    if not pos:
        raise HTTPException(status_code=404, detail="Position not found")
    db.delete(pos)
    db.commit()
    return None
