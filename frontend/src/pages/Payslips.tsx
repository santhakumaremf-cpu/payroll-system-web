import React, { useEffect, useState } from 'react';
import { getPayslips, getEmployees } from '../api/client';
import type { Payslip, Employee } from '../types';
import { Download } from 'lucide-react';

export default function Payslips() {
  const [payslips, setPayslips] = useState<Payslip[]>([]);
  const [employees, setEmployees] = useState<Employee[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([getPayslips(), getEmployees()])
      .then(([pay, emp]) => {
        setPayslips(pay.data);
        setEmployees(emp.data);
      })
      .finally(() => setLoading(false));
  }, []);

  const getEmpName = (id: number) => {
    const e = employees.find((x) => x.id === id);
    return e ? `${e.last_name}, ${e.first_name}` : `#${id}`;
  };

  const getEmpNo = (id: number) => {
    const e = employees.find((x) => x.id === id);
    return e?.employee_no || '';
  };

  const downloadPdf = async (payslipId: number, empNo: string) => {
    try {
      const token = localStorage.getItem('token');
      const base = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';
      const res = await fetch(
        `${base}/payroll/payslips/${payslipId}/pdf`,
        { headers: { Authorization: `Bearer ${token}` } }
      );
      if (!res.ok) throw new Error('Download failed');
      const blob = await res.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `payslip_${empNo || payslipId}.pdf`;
      document.body.appendChild(a);
      a.click();
      a.remove();
      window.URL.revokeObjectURL(url);
    } catch {
      alert('Failed to download PDF. Make sure backend is running.');
    }
  };

  return (
    <div>
      <h1 className="text-2xl font-bold text-slate-800 mb-6">Payslips</h1>
      <div className="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead className="bg-slate-50 text-slate-600 text-left">
              <tr>
                <th className="px-4 py-3 font-medium">Employee</th>
                <th className="px-4 py-3 font-medium">Present</th>
                <th className="px-4 py-3 font-medium">OT Hrs</th>
                <th className="px-4 py-3 font-medium">Basic</th>
                <th className="px-4 py-3 font-medium">Gross</th>
                <th className="px-4 py-3 font-medium">Deductions</th>
                <th className="px-4 py-3 font-medium">Net Pay</th>
                <th className="px-4 py-3 font-medium">Processed</th>
                <th className="px-4 py-3 font-medium">PDF</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {loading ? (
                <tr><td colSpan={9} className="px-4 py-8 text-center text-slate-400">Loading...</td></tr>
              ) : payslips.length === 0 ? (
                <tr><td colSpan={9} className="px-4 py-8 text-center text-slate-400">No payslips yet. Process a payroll first.</td></tr>
              ) : (
                payslips.map((p) => (
                  <tr key={p.id} className="hover:bg-slate-50">
                    <td className="px-4 py-3 font-medium">{getEmpName(p.employee_id)}</td>
                    <td className="px-4 py-3">{p.present_days}</td>
                    <td className="px-4 py-3">{p.overtime_hours}</td>
                    <td className="px-4 py-3">₱{Number(p.basic_pay).toLocaleString()}</td>
                    <td className="px-4 py-3">₱{Number(p.gross_pay).toLocaleString()}</td>
                    <td className="px-4 py-3 text-red-600">₱{Number(p.total_deductions).toLocaleString()}</td>
                    <td className="px-4 py-3 font-semibold text-emerald-700">₱{Number(p.net_pay).toLocaleString()}</td>
                    <td className="px-4 py-3 text-xs text-slate-500">{new Date(p.date_processed).toLocaleDateString()}</td>
                    <td className="px-4 py-3">
                      <button
                        onClick={() => downloadPdf(p.id, getEmpNo(p.employee_id))}
                        className="inline-flex items-center gap-1 px-2.5 py-1.5 text-xs font-medium bg-blue-50 text-blue-700 rounded-lg hover:bg-blue-100"
                      >
                        <Download className="w-3.5 h-3.5" /> PDF
                      </button>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
