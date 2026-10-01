import axios from 'axios';

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';

const api = axios.create({
  baseURL: API_BASE,
  headers: { 'Content-Type': 'application/json' },
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

api.interceptors.response.use(
  (res) => res,
  (err) => {
    if (err.response?.status === 401) {
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      window.location.href = '/login';
    }
    return Promise.reject(err);
  }
);

export default api;

export const login = (username: string, password: string) => {
  const form = new URLSearchParams();
  form.append('username', username);
  form.append('password', password);
  return api.post('/auth/login', form, {
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
  });
};

export const getMe = () => api.get('/auth/me');

export const getEmployees = (params?: { search?: string; status?: string }) =>
  api.get('/employees/', { params });

export const getEmployee = (id: number) => api.get(`/employees/${id}`);
export const createEmployee = (data: any) => api.post('/employees/', data);
export const updateEmployee = (id: number, data: any) => api.put(`/employees/${id}`, data);
export const deleteEmployee = (id: number) => api.delete(`/employees/${id}`);

export const getPositions = () => api.get('/positions/');
export const createPosition = (data: any) => api.post('/positions/', data);
export const updatePosition = (id: number, data: any) => api.put(`/positions/${id}`, data);
export const deletePosition = (id: number) => api.delete(`/positions/${id}`);

export const getPeriods = () => api.get('/payroll/periods');
export const getDeductions = () => api.get('/payroll/deductions');
export const processPayroll = (data: any) => api.post('/payroll/process', data);
export const getPayslips = (params?: { employee_id?: number; period_id?: number }) =>
  api.get('/payroll/payslips', { params });
export const getPayslip = (id: number) => api.get(`/payroll/payslips/${id}`);
