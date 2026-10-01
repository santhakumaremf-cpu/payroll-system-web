import React, { useEffect, useState } from 'react';
import { getEmployees, getPeriods, getDeductions, processPayroll } from '../api/client';
import type { Employee, PayrollPeriod } from '../types';
import { useAuth } from '../context/AuthContext';
import { Calculator } from 'lucide-react';

export default function Payroll() {
  const { isAdmin } = useAuth();
  const [employees, setEmployees] = useState<Employee[]>([]);
  const [periods, setPeriods] = useState<PayrollPeriod[]>([]);
  const [deductions, setDeductions] = useState<any[]>([]);
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [form, setForm] = useState({
    employee_id: 0, period_id: 0, present_days: '15',
    overtime_hours: '0', late_hours: '0', absences: '0', other_deductions: '0',
  });

  useEffect(() => {
    Promise.all([getEmployees({ status: 'Active' }), getPeriods(), getDeductions()])
      .then(([emp, per, ded]) => {
        setEmployees(emp.data);
        setPeriods(per.data);
        setDeductions(ded.data);
        if (emp.data.length) setForm((f) => ({ ...f, employee_id: emp.data[0].id }));
        if (per.data.length) setForm((f) => ({ ...f, period_id: per.data[0].id }));
      });
  }, []);

  const handleProcess = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!isAdmin) { alert('Admin only'); return; }
    setLoading(true);
    setResult(null);
    try {
      const res = await processPayroll({
        employee_id: form.employee_id,
        period_id: form.period_id,
        present_days: Number(form.present_days),
        overtime_hours: Number(form.overtime_hours),
        late_hours: Number(form.late_hours),
        absences: Number(form.absences),
        other_deductions: Number(form.other_deductions),
      });
      setResult(res.data);
    } catch (err: any) {
      alert(err.response?.data?.detail || 'Process failed');
    } finally {
      setLoading(false);
    }
  };

  const selectedEmp = employees.find((e) => e.id === form.employee_id);

  return (
    <div>
      <h1 className="text-2xl font-bold text-slate-800 mb-6">Process Payroll</h1>
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6">
          <form onSubmit={handleProcess} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">Employee</label>
              <select value={form.employee_id} onChange={(e) => setForm({ ...form, employee_id: Number(e.target.value) })}
                className="w-full px-3 py-2 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500">
                {employees.map((e) => (
                  <option key={e.id} value={e.id}>{e.employee_no} — {e.last_name}, {e.first_name}</option>
                ))}
              </select>
              {selectedEmp && (
                <p className="mt-1 text-xs text-slate-500">
                  {selectedEmp.position?.title} · {selectedEmp.employment_status} · Rate: P
                  {selectedEmp.employment_status === 'Regular'
                    ? selectedEmp.position?.regular_rate
                    : selectedEmp.position?.contractual_rate}/day
                </p>
              )}
            </div>
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">Payroll Period</label>
              <select value={form.period_id} onChange={(e) => setForm({ ...form, period_id: Number(e.target.value) })}
                className="w-full px-3 py-2 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500">
                {periods.map((p) => (
                  <option key={p.id} value={p.id}>{p.start_date} → {p.end_date} ({p.working_days} days)</option>
                ))}
              </select>
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-1">Present Days</label>
                <input type="number" step="0.5" value={form.present_days} onChange={(e) => setForm({ ...form, present_days: e.target.value })}
                  className="w-full px-3 py-2 border border-slate-300 rounded-lg text-sm" />
              </div>
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-1">OT Hours</label>
                <input type="number" step="0.5" value={form.overtime_hours} onChange={(e) => setForm({ ...form, overtime_hours: e.target.value })}
                  className="w-full px-3 py-2 border border-slate-300 rounded-lg text-sm" />
              </div>
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-1">Late Hours</label>
                <input type="number" step="0.5" value={form.late_hours} onChange={(e) => setForm({ ...form, late_hours: e.target.value })}
                  className="w-full px-3 py-2 border border-slate-300 rounded-lg text-sm" />
              </div>
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-1">Other Deductions</label>
                <input type="number" step="0.01" value={form.other_deductions} onChange={(e) => setForm({ ...form, other_deductions: e.target.value })}
                  className="w-full px-3 py-2 border border-slate-300 rounded-lg text-sm" />
              </div>
            </div>
            <div className="bg-slate-50 rounded-lg p-3 text-xs text-slate-600">
              <p className="font-medium mb-1">Default Deductions:</p>
              {deductions.map((d) => (
                <span key={d.id} className="inline-block mr-3">{d.name}: P{d.amount}</span>
              ))}
            </div>
            <button type="submit" disabled={loading || !isAdmin}
              className="w-full flex items-center justify-center gap-2 py-2.5 bg-blue-600 hover:bg-blue-500 disabled:bg-slate-400 text-white font-medium rounded-lg">
              <Calculator className="w-4 h-4" />
              {loading ? 'Processing...' : 'Process Payroll'}
            </button>
          </form>
        </div>

        <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6">
          <h2 className="text-lg font-semibold text-slate-800 mb-4">Payslip Result</h2>
          {!result ? (
            <p className="text-slate-400 text-sm">Process a payroll to see the result here.</p>
          ) : (
            <div className="space-y-3 text-sm">
              <div className="flex justify-between py-2 border-b border-slate-100"><span className="text-slate-500">Daily Rate</span><span className="font-medium">P{Number(result.daily_rate).toLocaleString()}</span></div>
              <div className="flex justify-between py-2 border-b border-slate-100"><span className="text-slate-500">Basic Pay</span><span className="font-medium">P{Number(result.basic_pay).toLocaleString()}</span></div>
              <div className="flex justify-between py-2 border-b border-slate-100"><span className="text-slate-500">Overtime Pay</span><span className="font-medium">P{Number(result.overtime_pay).toLocaleString()}</span></div>
              <div className="flex justify-between py-2 border-b border-slate-100"><span className="text-slate-500">Gross Pay</span><span className="font-semibold text-blue-600">P{Number(result.gross_pay).toLocaleString()}</span></div>
              <div className="flex justify-between py-2 border-b border-slate-100"><span className="text-slate-500">SSS</span><span>P{Number(result.sss).toLocaleString()}</span></div>
              <div className="flex justify-between py-2 border-b border-slate-100"><span className="text-slate-500">Pag-IBIG</span><span>P{Number(result.pagibig).toLocaleString()}</span></div>
              <div className="flex justify-between py-2 border-b border-slate-100"><span className="text-slate-500">PhilHealth</span><span>P{Number(result.philhealth).toLocaleString()}</span></div>
              <div className="flex justify-between py-2 border-b border-slate-100"><span className="text-slate-500">Total Deductions</span><span className="text-red-600">P{Number(result.total_deductions).toLocaleString()}</span></div>
              <div className="flex justify-between py-3 bg-emerald-50 rounded-lg px-3 mt-2">
                <span className="font-semibold text-emerald-800">Net Pay</span>
                <span className="font-bold text-lg text-emerald-700">P{Number(result.net_pay).toLocaleString()}</span>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
