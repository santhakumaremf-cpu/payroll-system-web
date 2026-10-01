"""Seed initial data from the original VB6 system"""
import sys
sys.path.append("../backend")

from decimal import Decimal
from datetime import date
from passlib.context import CryptContext
from app.models.database import (
    SessionLocal, init_db,
    Position, Employee, User, DeductionSetting, PayrollPeriod
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def seed():
    init_db()
    db = SessionLocal()
    try:
        positions_data = [
            ("Manager", 380, 420), ("Accountant", 100, 200), ("Employee", 100, 200),
            ("Maintenance", 100, 200), ("Driver", 90, 100), ("Programmer", 100, 200),
            ("Designer", 100, 200), ("Administrator", 150, 250),
        ]
        pos_map = {}
        for title, con, reg in positions_data:
            p = db.query(Position).filter(Position.title == title).first()
            if not p:
                p = Position(title=title, contractual_rate=Decimal(str(con)), regular_rate=Decimal(str(reg)), is_active=True)
                db.add(p)
                db.flush()
            pos_map[title] = p.id

        for name, amount in [("SSS", 300), ("Pag-IBIG", 150), ("PhilHealth", 100)]:
            if not db.query(DeductionSetting).filter(DeductionSetting.name == name).first():
                db.add(DeductionSetting(name=name, amount=Decimal(str(amount)), is_percentage=False))

        employees_data = [
            {"employee_no": "NEPC-161053", "last_name": "Carino", "first_name": "Jhon Kenneth",
             "middle_name": "Napallacan", "gender": "Male", "birth_date": date(1994, 11, 21),
             "birth_place": "Quezon City", "address": "Las Pinas City", "contact_no": "09163369826",
             "position": "Programmer", "date_hired": date(2013, 4, 26),
             "employment_status": "Regular", "current_status": "Active",
             "sss_no": "300", "pagibig_no": "150", "philhealth_no": "100"},
            {"employee_no": "NEPC-1001", "last_name": "Admin", "first_name": "System",
             "middle_name": "", "gender": "Male", "birth_date": date(1990, 1, 1),
             "birth_place": "Quezon City", "address": "Las Pinas City", "contact_no": "0987654321",
             "position": "Administrator", "date_hired": date(2013, 2, 12),
             "employment_status": "Regular", "current_status": "Active",
             "sss_no": "350", "pagibig_no": "150", "philhealth_no": "100"},
        ]
        emp_map = {}
        for e in employees_data:
            existing = db.query(Employee).filter(Employee.employee_no == e["employee_no"]).first()
            if not existing:
                emp = Employee(
                    employee_no=e["employee_no"], last_name=e["last_name"], first_name=e["first_name"],
                    middle_name=e["middle_name"] or None, gender=e["gender"], birth_date=e["birth_date"],
                    birth_place=e["birth_place"], address=e["address"], contact_no=e["contact_no"],
                    position_id=pos_map[e["position"]], date_hired=e["date_hired"],
                    employment_status=e["employment_status"], current_status=e["current_status"],
                    sss_no=e["sss_no"], pagibig_no=e["pagibig_no"], philhealth_no=e["philhealth_no"],
                )
                db.add(emp)
                db.flush()
                emp_map[e["employee_no"]] = emp.id
            else:
                emp_map[e["employee_no"]] = existing.id

        for username, password, role, emp_no in [("admin", "admin123", "admin", "NEPC-1001"), ("khen", "khen123", "user", "NEPC-161053")]:
            if not db.query(User).filter(User.username == username).first():
                db.add(User(
                    username=username, password_hash=pwd_context.hash(password),
                    role=role, employee_id=emp_map.get(emp_no), is_active=True
                ))

        if not db.query(PayrollPeriod).first():
            db.add(PayrollPeriod(start_date=date(2026, 9, 1), end_date=date(2026, 9, 15), working_days=15, status="Open"))

        db.commit()
        print("Seed successful!")
        print("Admin: admin / admin123")
        print("User:  khen / khen123")
    except Exception as e:
        db.rollback()
        print("Error:", e)
        raise
    finally:
        db.close()

if __name__ == "__main__":
    seed()
