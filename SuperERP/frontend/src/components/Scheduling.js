import React, { useState, useEffect, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import Navbar from './Navbar';
import 'bootstrap/dist/css/bootstrap.min.css';

const Scheduling = () => {
  const [timetable, setTimetable] = useState([]);
  const [fees, setFees] = useState([]);
  const [totals, setTotals] = useState({ total_due: 0, total_paid: 0 });
  const [timetableForm, setTimetableForm] = useState({ staff_id: '', student_id: '', subject: '', day_of_week: '', start_time: '', end_time: '' });
  const [feeForm, setFeeForm] = useState({ student_id: '', amount: '', due_date: '' });
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const fetchTimetable = useCallback(async () => {
    try {
      const response = await axios.get('http://127.0.0.1:8000/api/education/timetable/', {
        headers: { Authorization: `Bearer ${localStorage.getItem('token')}` },
      });
      setTimetable(response.data);
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to load timetable');
      if (err.response?.status === 403) {
        localStorage.removeItem('token');
        navigate('/');
      }
    }
  }, [navigate]);

  const fetchFees = useCallback(async () => {
    try {
      const response = await axios.get('http://127.0.0.1:8000/api/education/fees/', {
        headers: { Authorization: `Bearer ${localStorage.getItem('token')}` },
      });
      setFees(response.data.fees);
      setTotals({ total_due: response.data.total_due, total_paid: response.data.total_paid });
      const blob = new Blob([new Uint8Array.from(Buffer.from(response.data.report_pdf, 'hex'))], { type: 'application/pdf' });
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = 'fee_report.pdf';
      link.click();
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to load fees');
    }
  }, []);

  useEffect(() => {
    fetchTimetable();
    fetchFees();
  }, [fetchTimetable, fetchFees]);

  const handleTimetableChange = (e) => {
    setTimetableForm({ ...timetableForm, [e.target.name]: e.target.value });
  };

  const handleFeeChange = (e) => {
    setFeeForm({ ...feeForm, [e.target.name]: e.target.value });
  };

  const handleAddTimetable = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('http://127.0.0.1:8000/api/education/timetable/', timetableForm, {
        headers: { Authorization: `Bearer ${localStorage.getItem('token')}` },
      });
      setTimetable([...timetable, { id: response.data.id, ...timetableForm }]);
      setTimetableForm({ staff_id: '', student_id: '', subject: '', day_of_week: '', start_time: '', end_time: '' });
      setError('');
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to add timetable entry');
    }
  };

  const handleAddFee = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('http://127.0.0.1:8000/api/education/fees/', feeForm, {
        headers: { Authorization: `Bearer ${localStorage.getItem('token')}` },
      });
      setFees([...fees, { id: response.data.id, ...feeForm, amount: parseFloat(feeForm.amount), paid: false }]);
      setTotals({ ...totals, total_due: totals.total_due + parseFloat(feeForm.amount) });
      setFeeForm({ student_id: '', amount: '', due_date: '' });
      fetchFees(); // Refresh PDF
      setError('');
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to add fee');
    }
  };

  const handleMarkPaid = async (feeId) => {
    try {
      await axios.put(`http://127.0.0.1:8000/api/education/fees/${feeId}/`, { paid: true }, {
        headers: { Authorization: `Bearer ${localStorage.getItem('token')}` },
      });
      const updatedFees = fees.map(f => f.id === feeId ? { ...f, paid: true, paid_date: new Date().toISOString().split('T')[0] } : f);
      const fee = fees.find(f => f.id === feeId);
      setFees(updatedFees);
      setTotals({
        total_due: totals.total_due - fee.amount,
        total_paid: totals.total_paid + fee.amount,
      });
      fetchFees(); // Refresh PDF
      setError('');
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to update fee');
    }
  };

  return (
    <>
      <Navbar />
      <div className="container-fluid py-5" style={{ backgroundColor: '#f8f9fa', minHeight: '100vh' }}>
        <div className="row justify-content-center">
          <div className="col-md-10">
            <div className="card shadow p-4">
              <h1 className="display-4 text-primary mb-4">Scheduling & Fees</h1>
              {error && <p className="text-danger">{error}</p>}
              <h3 className="mt-4">Timetable</h3>
              <form onSubmit={handleAddTimetable} className="mb-4">
                <div className="row">
                  <div className="col-md-2"><input type="text" className="form-control" name="staff_id" placeholder="Staff ID" value={timetableForm.staff_id} onChange={handleTimetableChange} required /></div>
                  <div className="col-md-2"><input type="text" className="form-control" name="student_id" placeholder="Student ID" value={timetableForm.student_id} onChange={handleTimetableChange} required /></div>
                  <div className="col-md-2"><input type="text" className="form-control" name="subject" placeholder="Subject" value={timetableForm.subject} onChange={handleTimetableChange} required /></div>
                  <div className="col-md-2"><input type="text" className="form-control" name="day_of_week" placeholder="Day" value={timetableForm.day_of_week} onChange={handleTimetableChange} required /></div>
                  <div className="col-md-1"><input type="time" className="form-control" name="start_time" value={timetableForm.start_time} onChange={handleTimetableChange} required /></div>
                  <div className="col-md-1"><input type="time" className="form-control" name="end_time" value={timetableForm.end_time} onChange={handleTimetableChange} required /></div>
                  <div className="col-md-2"><button type="submit" className="btn btn-primary w-100">Add Entry</button></div>
                </div>
              </form>
              <table className="table table-striped mb-5">
                <thead><tr><th>Staff</th><th>Student</th><th>Subject</th><th>Day</th><th>Start</th><th>End</th></tr></thead>
                <tbody>{timetable.map(t => (
                  <tr key={t.id}><td>{t.staff_name}</td><td>{t.student_name}</td><td>{t.subject}</td><td>{t.day_of_week}</td><td>{t.start_time}</td><td>{t.end_time}</td></tr>
                ))}</tbody>
              </table>
              <h3>Fee Tracking</h3>
              <div className="card mb-4">
                <div className="card-body">
                  <p>Total Due: ${totals.total_due.toFixed(2)}</p>
                  <p>Total Paid: ${totals.total_paid.toFixed(2)}</p>
                  <button className="btn btn-secondary" onClick={fetchFees}>Download Fee Report PDF</button>
                </div>
              </div>
              <form onSubmit={handleAddFee} className="mb-4">
                <div className="row">
                  <div className="col-md-3"><input type="text" className="form-control" name="student_id" placeholder="Student ID" value={feeForm.student_id} onChange={handleFeeChange} required /></div>
                  <div className="col-md-3"><input type="number" className="form-control" name="amount" placeholder="Amount" value={feeForm.amount} onChange={handleFeeChange} step="0.01" required /></div>
                  <div className="col-md-3"><input type="date" className="form-control" name="due_date" value={feeForm.due_date} onChange={handleFeeChange} required /></div>
                  <div className="col-md-3"><button type="submit" className="btn btn-primary w-100">Add Fee</button></div>
                </div>
              </form>
              <table className="table table-striped">
                <thead><tr><th>Student</th><th>Amount</th><th>Due Date</th><th>Paid</th><th>Paid Date</th><th>Action</th></tr></thead>
                <tbody>{fees.map(f => (
                  <tr key={f.id}><td>{f.student_name}</td><td>${f.amount.toFixed(2)}</td><td>{f.due_date}</td><td>{f.paid ? 'Yes' : 'No'}</td><td>{f.paid_date || 'N/A'}</td>
                    <td>{!f.paid && (
                      <button className="btn btn-success btn-sm" onClick={() => handleMarkPaid(f.id)}>Mark Paid</button>
                    )}</td>
                  </tr>
                ))}</tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </>
  );
};

export default Scheduling;
