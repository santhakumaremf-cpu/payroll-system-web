"""
Core Payroll Calculation Engine
"""

from decimal import Decimal, ROUND_HALF_UP
from dataclasses import dataclass


def money(value) -> Decimal:
    return Decimal(str(value)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


@dataclass
class PayrollInput:
    daily_rate: Decimal
    present_days: Decimal
    overtime_hours: Decimal = Decimal("0")
    late_hours: Decimal = Decimal("0")
    absences: Decimal = Decimal("0")
    sss: Decimal = Decimal("0")
    pagibig: Decimal = Decimal("0")
    philhealth: Decimal = Decimal("0")
    other_deductions: Decimal = Decimal("0")
    overtime_multiplier: Decimal = Decimal("1.25")


@dataclass
class PayrollResult:
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
    hourly_rate: Decimal


def calculate_payroll(data: PayrollInput) -> PayrollResult:
    daily_rate = money(data.daily_rate)
    present_days = money(data.present_days)
    overtime_hours = money(data.overtime_hours)
    hourly_rate = money(daily_rate / Decimal("8"))
    basic_pay = money(daily_rate * present_days)
    overtime_pay = money(hourly_rate * overtime_hours * data.overtime_multiplier)
    gross_pay = money(basic_pay + overtime_pay)
    sss = money(data.sss)
    pagibig = money(data.pagibig)
    philhealth = money(data.philhealth)
    other_deductions = money(data.other_deductions)
    total_deductions = money(sss + pagibig + philhealth + other_deductions)
    net_pay = money(gross_pay - total_deductions)
    return PayrollResult(
        daily_rate=daily_rate, basic_pay=basic_pay, overtime_pay=overtime_pay,
        gross_pay=gross_pay, sss=sss, pagibig=pagibig, philhealth=philhealth,
        other_deductions=other_deductions, total_deductions=total_deductions,
        net_pay=net_pay, hourly_rate=hourly_rate,
    )
