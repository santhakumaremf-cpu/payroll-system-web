import React, { useEffect, useState } from 'react';
import { getEmployees, getPositions, getPayslips, getPeriods } from '../api/client';
import { Users, Briefcase, FileText, Calendar } from 'lucide-react';

export default function Dashboard() {
  const [stats, setStats] = useState({
    employees: 0, positions: 0, payslips: 0, periods: 0,
  });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([getEmployees(), getPositions(), getPayslips(), getPeriods()])
      .then(([emp, pos, pay, per]) => {
        setStats({
          employees: emp.data.length,
          positions: pos.data.length,
          payslips: pay.data.length,
          periods: per.data.length,
        });
      })
      .finally(() => setLoading(false));
  }, []);

  const cards = [
    { label: 'Employees', value: stats.employees, icon: Users, color: 'bg-blue-500' },
    { label: 'Positions', value: stats.positions, icon: Briefcase, color: 'bg-emerald-500' },
    { label: 'Payslips', value: stats.payslips, icon: FileText, color: 'bg-violet-500' },
    { label: 'Periods', value: stats.periods, icon: Calendar, color: 'bg-amber-500' },
  ];

  return (
    <div>
      <h1 className="text-2xl font-bold text-slate-800 mb-6">Dashboard</h1>
      {loading ? (
        <div className="text-slate-500">Loading...</div>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          {cards.map((c) => (
            <div key={c.label} className="bg-white rounded-xl shadow-sm border border-slate-200 p-5 flex items-center gap-4">
              <div className={`${c.color} p-3 rounded-lg text-white`}>
                <c.icon className="w-6 h-6" />
              </div>
              <div>
                <p className="text-sm text-slate-500">{c.label}</p>
                <p className="text-2xl font-bold text-slate-800">{c.value}</p>
              </div>
            </div>
          ))}
        </div>
      )}
      <div className="mt-8 bg-white rounded-xl shadow-sm border border-slate-200 p-6">
        <h2 className="text-lg font-semibold text-slate-800 mb-2">Welcome</h2>
        <p className="text-slate-600 text-sm leading-relaxed">
          Modern web version of the original VB6 Payroll System (2013).
          Use the sidebar to manage employees, positions, process payroll, and view payslips.
        </p>
      </div>
    </div>
  );
}
