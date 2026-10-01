export interface User {
  id: number;
  username: string;
  role: string;
  employee_id?: number;
}

export interface Position {
  id: number;
  title: string;
  contractual_rate: string;
  regular_rate: string;
  description?: string;
  is_active: boolean;
}

export interface Employee {
  id: number;
  employee_no: string;
  last_name: string;
  first_name: string;
  middle_name?: string;
  gender?: string;
  birth_date?: string;
  birth_place?: string;
  address?: string;
  contact_no?: string;
  position_id: number;
  date_hired?: string;
  employment_status: string;
  current_status: string;
  sss_no?: string;
  pagibig_no?: string;
  philhealth_no?: string;
  position?: Position;
}

export interface Payslip {
  id: number;
  employee_id: number;
  period_id: number;
  present_days: string;
  overtime_hours: string;
  late_hours: string;
  absences: string;
  daily_rate: string;
  basic_pay: string;
  overtime_pay: string;
  gross_pay: string;
  sss: string;
  pagibig: string;
  philhealth: string;
  other_deductions: string;
  total_deductions: string;
  net_pay: string;
  date_processed: string;
  notes?: string;
}

export interface PayrollPeriod {
  id: number;
  start_date: string;
  end_date: string;
  working_days: number;
  status: string;
}

export interface LoginResponse {
  access_token: string;
  token_type: string;
  role: string;
  username: string;
}
