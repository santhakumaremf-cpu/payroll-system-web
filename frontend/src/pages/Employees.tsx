import React, { useEffect, useState } from 'react';
import { getEmployees, getPositions, createEmployee, updateEmployee, deleteEmployee } from '../api/client';
import type { Employee, Position } from '../types';
import { useAuth } from '../context/AuthContext';
import { Plus, Search, Pencil, Trash2 } from 'lucide-react';

export default function Employees() {
  const { isAdmin } = useAuth();
  const [employees, setEmployees] = useState<Employee[]>([]);
  const [positions, setPositions] = useState<Position[]>([]);
  const [search, setSearch] = useState('');
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [editing, setEditing] = useState<Employee | null>(null);
  const [form, setForm] = useState({
    employee_no: '', last_name: '', first_name: '', middle_name: '',
    gender: 'Male', position_id: 0, employment_status: 'Regular',
    current_status: 'Active', contact_no: '', address: '',
  });

  const load = () => {
    setLoading(true);
    Promise.all([getEmployees({ search: search || undefined }), getPositions()])
      .then(([emp, pos]) => {
        setEmployees(emp.data);
        setPositions(pos.data);
        if (pos.data.length && !form.position_id) setForm((f) => ({ ...f, position_id: pos.data[0].id }));
      })
      .finally(() => setLoading(false));
  };

  useEffect(() => { load(); }, [search]);

  const openCreate = () => {
    setEditing(null);
    setForm({
      employee_no: '', last_name: '', first_name: '', middle_name: '',
      gender: 'Male', position_id: positions[0]?.id || 0,
      employment_status: 'Regular', current_status: 'Active', contact_no: '', address: '',
    });
    setShowForm(true);
  };

  const openEdit = (e: Employee) => {
    setEditing(e);
    setForm({
      employee_no: e.employee_no, last_name: e.last_name, first_name: e.first_name,
      middle_name: e.middle_name || '', gender: e.gender || 'Male', position_id: e.position_id,
      employment_status: e.employment_status, current_status: e.current_status,
      contact_no: e.contact_no || '', address: e.address || '',
    });
    setShowForm(true);
  };

  const handleSubmit = async (ev: React.FormEvent) => {
    ev.preventDefault();
    try {
      if (editing) await updateEmployee(editing.id, form);
      else await createEmployee(form);
      setShowForm(false);
      load();
    } catch (err: any) {
      alert(err.response?.data?.detail || 'Error saving');
    }
  };

  const handleDelete = async (id: number) => {
    if (!confirm('Delete this employee?')) return;
    try { await deleteEmployee(id); load(); }
    catch (err: any) { alert(err.response?.data?.detail || 'Error'); }
  };

  return (
    <div>
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-6">
        <h1 className="text-2xl font-bold text-slate-800">Employees</h1>
        <div className="flex gap-2">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
            <input type="text" placeholder="Search..." value={search} onChange={(e) => setSearch(e.target.value)}
              className="pl-9 pr-3 py-2 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500" />
          </div>
          {isAdmin && (
            <button onClick={openCreate} className="flex items-center gap-1.5 px-3 py-2 bg-blue-600 text-white text-sm font-medium rounded-lg hover:bg-blue-500">
              <Plus className="w-4 h-4" /> Add
            </button>
          )}
        </div>
      </div>

      <div className="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead className="bg-slate-50 text-slate-600 text-left">
              <tr>
                <th className="px-4 py-3 font-medium">Emp No</th>
                <th className="px-4 py-3 font-medium">Name</th>
                <th className="px-4 py-3 font-medium">Position</th>
                <th className="px-4 py-3 font-medium">Status</th>
                <th className="px-4 py-3 font-medium">Employment</th>
                {isAdmin && <th className="px-4 py-3 font-medium">Actions</th>}
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {loading ? (
                <tr><td colSpan={6} className="px-4 py-8 text-center text-slate-400">Loading...</td></tr>
              ) : employees.length === 0 ? (
                <tr><td colSpan={6} className="px-4 py-8 text-center text-slate-400">No employees</td></tr>
              ) : employees.map((e) => (
                <tr key={e.id} className="hover:bg-slate-50">
                  <td className="px-4 py-3 font-mono text-xs">{e.employee_no}</td>
                  <td className="px-4 py-3 font-medium">{e.last_name}, {e.first_name}</td>
                  <td className="px-4 py-3">{e.position?.title || '-'}</td>
                  <td className="px-4 py-3">
                    <span className={`inline-flex px-2 py-0.5 rounded-full text-xs font-medium ${
                      e.current_status === 'Active' ? 'bg-green-100 text-green-700' : 'bg-slate-100 text-slate-600'
                    }`}>{e.current_status}</span>
                  </td>
                  <td className="px-4 py-3">{e.employment_status}</td>
                  {isAdmin && (
                    <td className="px-4 py-3">
                      <div className="flex gap-1">
                        <button onClick={() => openEdit(e)} className="p-1.5 rounded hover:bg-slate-100 text-slate-500"><Pencil className="w-4 h-4" /></button>
                        <button onClick={() => handleDelete(e.id)} className="p-1.5 rounded hover:bg-red-50 text-red-500"><Trash2 className="w-4 h-4" /></button>
                      </div>
                    </td>
                  )}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {showForm && (
        <div className="fixed inset-0 bg-black/40 z-40 flex items-center justify-center p-4">
          <div className="bg-white rounded-xl shadow-xl w-full max-w-lg max-h-[90vh] overflow-y-auto">
            <div className="px-6 py-4 border-b"><h3 className="text-lg font-semibold">{editing ? 'Edit' : 'Add'} Employee</h3></div>
            <form onSubmit={handleSubmit} className="p-6 space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium mb-1">Employee No</label>
                  <input required disabled={!!editing} value={form.employee_no} onChange={(e) => setForm({ ...form, employee_no: e.target.value })}
                    className="w-full px-3 py-2 border rounded-lg text-sm disabled:bg-slate-50" />
                </div>
                <div>
                  <label className="block text-sm font-medium mb-1">Position</label>
                  <select value={form.position_id} onChange={(e) => setForm({ ...form, position_id: Number(e.target.value) })}
                    className="w-full px-3 py-2 border rounded-lg text-sm">
                    {positions.map((p) => <option key={p.id} value={p.id}>{p.title}</option>)}
                  </select>
                </div>
              </div>
              <div className="grid grid-cols-3 gap-3">
                <div>
                  <label className="block text-sm font-medium mb-1">Last Name</label>
                  <input required value={form.last_name} onChange={(e) => setForm({ ...form, last_name: e.target.value })} className="w-full px-3 py-2 border rounded-lg text-sm" />
                </div>
                <div>
                  <label className="block text-sm font-medium mb-1">First Name</label>
                  <input required value={form.first_name} onChange={(e) => setForm({ ...form, first_name: e.target.value })} className="w-full px-3 py-2 border rounded-lg text-sm" />
                </div>
                <div>
                  <label className="block text-sm font-medium mb-1">Middle</label>
                  <input value={form.middle_name} onChange={(e) => setForm({ ...form, middle_name: e.target.value })} className="w-full px-3 py-2 border rounded-lg text-sm" />
                </div>
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium mb-1">Employment</label>
                  <select value={form.employment_status} onChange={(e) => setForm({ ...form, employment_status: e.target.value })} className="w-full px-3 py-2 border rounded-lg text-sm">
                    <option>Regular</option><option>Contractual</option>
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium mb-1">Status</label>
                  <select value={form.current_status} onChange={(e) => setForm({ ...form, current_status: e.target.value })} className="w-full px-3 py-2 border rounded-lg text-sm">
                    <option>Active</option><option>Inactive</option>
                  </select>
                </div>
              </div>
              <div className="flex justify-end gap-2 pt-2">
                <button type="button" onClick={() => setShowForm(false)} className="px-4 py-2 text-sm border rounded-lg">Cancel</button>
                <button type="submit" className="px-4 py-2 text-sm bg-blue-600 text-white rounded-lg">Save</button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
