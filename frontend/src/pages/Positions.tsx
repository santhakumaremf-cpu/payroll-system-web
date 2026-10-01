import React, { useEffect, useState } from 'react';
import { getPositions, createPosition, updatePosition, deletePosition } from '../api/client';
import type { Position } from '../types';
import { useAuth } from '../context/AuthContext';
import { Plus, Pencil, Trash2 } from 'lucide-react';

export default function Positions() {
  const { isAdmin } = useAuth();
  const [positions, setPositions] = useState<Position[]>([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [editing, setEditing] = useState<Position | null>(null);
  const [form, setForm] = useState({ title: '', contractual_rate: '', regular_rate: '', description: '' });

  const load = () => {
    setLoading(true);
    getPositions().then((res) => setPositions(res.data)).finally(() => setLoading(false));
  };

  useEffect(() => { load(); }, []);

  const openCreate = () => {
    setEditing(null);
    setForm({ title: '', contractual_rate: '', regular_rate: '', description: '' });
    setShowForm(true);
  };

  const openEdit = (p: Position) => {
    setEditing(p);
    setForm({ title: p.title, contractual_rate: p.contractual_rate, regular_rate: p.regular_rate, description: p.description || '' });
    setShowForm(true);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const payload = {
        title: form.title,
        contractual_rate: Number(form.contractual_rate),
        regular_rate: Number(form.regular_rate),
        description: form.description || null,
        is_active: true,
      };
      if (editing) await updatePosition(editing.id, payload);
      else await createPosition(payload);
      setShowForm(false);
      load();
    } catch (err: any) {
      alert(err.response?.data?.detail || 'Error');
    }
  };

  const handleDelete = async (id: number) => {
    if (!confirm('Delete this position?')) return;
    try { await deletePosition(id); load(); }
    catch (err: any) { alert(err.response?.data?.detail || 'Error'); }
  };

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-2xl font-bold text-slate-800">Positions</h1>
        {isAdmin && (
          <button onClick={openCreate} className="flex items-center gap-1.5 px-3 py-2 bg-blue-600 text-white text-sm font-medium rounded-lg hover:bg-blue-500">
            <Plus className="w-4 h-4" /> Add
          </button>
        )}
      </div>

      <div className="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden">
        <table className="w-full text-sm">
          <thead className="bg-slate-50 text-slate-600 text-left">
            <tr>
              <th className="px-4 py-3 font-medium">Title</th>
              <th className="px-4 py-3 font-medium">Contractual Rate</th>
              <th className="px-4 py-3 font-medium">Regular Rate</th>
              {isAdmin && <th className="px-4 py-3 font-medium">Actions</th>}
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100">
            {loading ? (
              <tr><td colSpan={4} className="px-4 py-8 text-center text-slate-400">Loading...</td></tr>
            ) : positions.map((p) => (
              <tr key={p.id} className="hover:bg-slate-50">
                <td className="px-4 py-3 font-medium">{p.title}</td>
                <td className="px-4 py-3">P{Number(p.contractual_rate).toLocaleString()}</td>
                <td className="px-4 py-3">P{Number(p.regular_rate).toLocaleString()}</td>
                {isAdmin && (
                  <td className="px-4 py-3">
                    <div className="flex gap-1">
                      <button onClick={() => openEdit(p)} className="p-1.5 rounded hover:bg-slate-100 text-slate-500"><Pencil className="w-4 h-4" /></button>
                      <button onClick={() => handleDelete(p.id)} className="p-1.5 rounded hover:bg-red-50 text-red-500"><Trash2 className="w-4 h-4" /></button>
                    </div>
                  </td>
                )}
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {showForm && (
        <div className="fixed inset-0 bg-black/40 z-40 flex items-center justify-center p-4">
          <div className="bg-white rounded-xl shadow-xl w-full max-w-md">
            <div className="px-6 py-4 border-b"><h3 className="text-lg font-semibold">{editing ? 'Edit' : 'Add'} Position</h3></div>
            <form onSubmit={handleSubmit} className="p-6 space-y-4">
              <div>
                <label className="block text-sm font-medium mb-1">Title</label>
                <input required value={form.title} onChange={(e) => setForm({ ...form, title: e.target.value })}
                  className="w-full px-3 py-2 border rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500" />
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium mb-1">Contractual Rate</label>
                  <input type="number" required value={form.contractual_rate} onChange={(e) => setForm({ ...form, contractual_rate: e.target.value })}
                    className="w-full px-3 py-2 border rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500" />
                </div>
                <div>
                  <label className="block text-sm font-medium mb-1">Regular Rate</label>
                  <input type="number" required value={form.regular_rate} onChange={(e) => setForm({ ...form, regular_rate: e.target.value })}
                    className="w-full px-3 py-2 border rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500" />
                </div>
              </div>
              <div className="flex justify-end gap-2">
                <button type="button" onClick={() => setShowForm(false)} className="px-4 py-2 text-sm border rounded-lg hover:bg-slate-50">Cancel</button>
                <button type="submit" className="px-4 py-2 text-sm bg-blue-600 text-white rounded-lg hover:bg-blue-500">Save</button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
