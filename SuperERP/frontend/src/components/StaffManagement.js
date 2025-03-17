import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import Navbar from './Navbar';
import 'bootstrap/dist/css/bootstrap.min.css';

const StaffManagement = () => {
  const [staff, setStaff] = useState([]);
  const [payroll, setPayroll] = useState([]);
  const [formData, setFormData] = useState({ name: '', staff_id: '', role: '', salary: '', tax_rate: '' });
  const [error, setError] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    fetchStaff();
    fetchPayroll();
  }, []);

  const fetchStaff = async () => {
    try {
      const response = await axios.get('http://127.0.0.1:8000/api/education/staff/', {
        headers: { Authorization: `Bearer ${localStorage.getItem('token')}` },
      });
      setStaff(response.data);
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to load staff');
      if (err.response?.status === 403) {
        localStorage.removeItem('token');
        navigate('/');
      }
    }
  };

  const fetchPayroll = async () => {
    try {
      const response = await axios.get('http://127.0.0.1:8000/api/education/payroll/', {
        headers: { Authorization: `Bearer ${localStorage.getItem('token')}` },
      });
      setPayroll(response.data.payroll);
      const blob = new Blob([new Uint8Array.from(Buffer.from(response.data.report_pdf, 'hex'))], { type: 'application/pdf' });
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = 'payroll_report.pdf';
      link.click();
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to load payroll');
    }
  };

  const handleInputChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleAddStaff = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('http://127.0.0.1:8000/api/education/staff/', formData, {
        headers: { Authorization: `Bearer ${localStorage.getItem('token')}` },
      });
      setStaff([...staff, { id: response.data.id, ...formData, salary: parseFloat(formData.salary || 0), tax_rate: parseFloat(formData.tax_rate || 10) }]);
      setFormData({ name: '', staff_id: '', role: '', salary: '', tax_rate: '' });
      fetchPayroll(); // Refresh payroll
      setError('');
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to add staff');
    }
  };

  const handleDeleteStaff = async (staffId) => {
    try {
      await axios.delete(`http://127.0.0.1:8000/api/education/staff/${staffId}/`, {
        headers: { Authorization: `Bearer ${localStorage.getItem('token')}` },
      });
      setStaff(staff.filter(s => s.id !== staffId));
      fetchPayroll(); // Refresh payroll
      setError('');
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to delete staff');
    }
  };

  return (
    <>
      <Navbar />
      <div className="container-fluid py-5" style={{ backgroundColor: '#f8f9fa', minHeight: '100vh' }}>
        <div className="row justify-content-center">
          <div className="col-md-10">
            <div className="card shadow p-4">
              <h1 className="display-4 text-primary mb-4">Staff Management</h1>
              {error && <p className="text-danger">{error}</p>}
              <div className="card mb-4">
                <div className="card-body">
                  <h5>Payroll Overview</h5>
                  <table className="table">
                    <thead><tr><th>Name</th><th>Gross</th><th>Tax</th><th>Net</th><th>Leave</th></tr></thead>
                    <tbody>{payroll.map(p => (
                      <tr key={p.staff_id}><td>{p.name}</td><td>${p.gross_salary.toFixed(2)}</td><td>{p.tax_rate}%</td><td>${p.net_salary.toFixed(2)}</td><td>{p.leave_balance}</td></tr>
                    ))}</tbody>
                  </table>
                  <button className="btn btn-secondary" onClick={fetchPayroll}>Download Payroll PDF</button>
                </div>
              </div>
              <form onSubmit={handleAddStaff} className="mb-4">
                <div className="row">
                  <div className="col-md-2"><input type="text" className="form-control" name="name" placeholder="Name" value={formData.name} onChange={handleInputChange} required /></div>
                  <div className="col-md-2"><input type="text" className="form-control" name="staff_id" placeholder="Staff ID" value={formData.staff_id} onChange={handleInputChange} required /></div>
                  <div className="col-md-2"><input type="text" className="form-control" name="role" placeholder="Role" value={formData.role} onChange={handleInputChange} required /></div>
                  <div className="col-md-2"><input type="number" className="form-control" name="salary" placeholder="Salary" value={formData.salary} onChange={handleInputChange} step="0.01" /></div>
                  <div className="col-md-2"><input type="number" className="form-control" name="tax_rate" placeholder="Tax Rate" value={formData.tax_rate} onChange={handleInputChange} step="0.01" /></div>
                  <div className="col-md-2"><button type="submit" className="btn btn-primary w-100">Add Staff</button></div>
                </div>
              </form>
              <table className="table table-striped">
                <thead>
                  <tr><th>Name</th><th>Staff ID</th><th>Role</th><th>Hire Date</th><th>Salary</th><th>Actions</th></tr>
                </thead>
                <tbody>
                  {staff.map(s => (
                    <tr key={s.id}><td>{s.name}</td><td>{s.staff_id}</td><td>{s.role}</td><td>{s.hire_date}</td><td>${s.salary.toFixed(2)}</td>
                      <td><button className="btn btn-danger btn-sm" onClick={() => handleDeleteStaff(s.id)}>Delete</button></td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </>
  );
};

export default StaffManagement;
