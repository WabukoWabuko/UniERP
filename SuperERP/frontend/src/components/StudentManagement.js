import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import Navbar from './Navbar';
import 'bootstrap/dist/css/bootstrap.min.css';

const StudentManagement = () => {
  const [students, setStudents] = useState([]);
  const [attendance, setAttendance] = useState([]);
  const [grades, setGrades] = useState([]);
  const [formData, setFormData] = useState({ name: '', student_id: '', grade: '', date_of_birth: '' });
  const [gradeForm, setGradeForm] = useState({ student_id: '', subject: '', grade_value: '' });
  const [error, setError] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    fetchStudents();
    fetchAttendance();
    fetchGrades();
  }, []);

  const fetchStudents = async () => {
    try {
      const response = await axios.get('http://127.0.0.1:8000/api/education/students/', {
        headers: { Authorization: `Bearer ${localStorage.getItem('token')}` },
      });
      setStudents(response.data);
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to load students');
      if (err.response?.status === 403) {
        localStorage.removeItem('token');
        navigate('/');
      }
    }
  };

  const fetchAttendance = async () => {
    try {
      const response = await axios.get('http://127.0.0.1:8000/api/education/attendance/', {
        headers: { Authorization: `Bearer ${localStorage.getItem('token')}` },
      });
      setAttendance(response.data);
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to load attendance');
    }
  };

  const fetchGrades = async () => {
    try {
      const response = await axios.get('http://127.0.0.1:8000/api/education/grades/', {
        headers: { Authorization: `Bearer ${localStorage.getItem('token')}` },
      });
      setGrades(response.data);
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to load grades');
    }
  };

  const handleInputChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleGradeChange = (e) => {
    setGradeForm({ ...gradeForm, [e.target.name]: e.target.value });
  };

  const handleAddStudent = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('http://127.0.0.1:8000/api/education/students/', formData, {
        headers: { Authorization: `Bearer ${localStorage.getItem('token')}` },
      });
      setStudents([...students, { id: response.data.id, ...formData }]);
      setFormData({ name: '', student_id: '', grade: '', date_of_birth: '' });
      setError('');
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to add student');
    }
  };

  const handleDeleteStudent = async (studentId) => {
    try {
      await axios.delete(`http://127.0.0.1:8000/api/education/students/${studentId}/`, {
        headers: { Authorization: `Bearer ${localStorage.getItem('token')}` },
      });
      setStudents(students.filter(s => s.id !== studentId));
      setError('');
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to delete student');
    }
  };

  const handleAttendance = async (studentId, present) => {
    try {
      await axios.post('http://127.0.0.1:8000/api/education/attendance/', { student_id: studentId, present }, {
        headers: { Authorization: `Bearer ${localStorage.getItem('token')}` },
      });
      setAttendance(attendance.map(a => a.student_id === studentId ? { ...a, present } : a));
      setError('');
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to update attendance');
    }
  };

  const handleAddGrade = async (e) => {
    e.preventDefault();
    try {
      await axios.post('http://127.0.0.1:8000/api/education/grades/', gradeForm, {
        headers: { Authorization: `Bearer ${localStorage.getItem('token')}` },
      });
      setGrades([...grades, { ...gradeForm, grade: parseFloat(gradeForm.grade_value) }]);
      setGradeForm({ student_id: '', subject: '', grade_value: '' });
      setError('');
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to add grade');
    }
  };

  return (
    <>
      <Navbar />
      <div className="container-fluid py-5" style={{ backgroundColor: '#f8f9fa', minHeight: '100vh' }}>
        <div className="row justify-content-center">
          <div className="col-md-10">
            <div className="card shadow p-4">
              <h1 className="display-4 text-primary mb-4">Student Management</h1>
              {error && <p className="text-danger">{error}</p>}
              <form onSubmit={handleAddStudent} className="mb-4">
                <div className="row">
                  <div className="col-md-3"><input type="text" className="form-control" name="name" placeholder="Name" value={formData.name} onChange={handleInputChange} required /></div>
                  <div className="col-md-3"><input type="text" className="form-control" name="student_id" placeholder="Student ID" value={formData.student_id} onChange={handleInputChange} required /></div>
                  <div className="col-md-2"><input type="text" className="form-control" name="grade" placeholder="Grade" value={formData.grade} onChange={handleInputChange} required /></div>
                  <div className="col-md-2"><input type="date" className="form-control" name="date_of_birth" value={formData.date_of_birth} onChange={handleInputChange} /></div>
                  <div className="col-md-2"><button type="submit" className="btn btn-primary w-100">Add Student</button></div>
                </div>
              </form>
              <h3>Students</h3>
              <table className="table table-striped mb-4">
                <thead>
                  <tr><th>Name</th><th>Student ID</th><th>Grade</th><th>Attendance Today</th><th>Actions</th></tr>
                </thead>
                <tbody>
                  {students.map(s => {
                    const att = attendance.find(a => a.student_id === s.id);
                    return (
                      <tr key={s.id}>
                        <td>{s.name}</td><td>{s.student_id}</td><td>{s.grade}</td>
                        <td>
                          <button className={`btn btn-sm ${att?.present ? 'btn-success' : 'btn-danger'}`} onClick={() => handleAttendance(s.id, !att?.present)}>
                            {att?.present ? 'Present' : 'Absent'}
                          </button>
                        </td>
                        <td><button className="btn btn-danger btn-sm" onClick={() => handleDeleteStudent(s.id)}>Delete</button></td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
              <h3>Add Grade</h3>
              <form onSubmit={handleAddGrade} className="mb-4">
                <div className="row">
                  <div className="col-md-3"><input type="text" className="form-control" name="student_id" placeholder="Student ID" value={gradeForm.student_id} onChange={handleGradeChange} required /></div>
                  <div className="col-md-3"><input type="text" className="form-control" name="subject" placeholder="Subject" value={gradeForm.subject} onChange={handleGradeChange} required /></div>
                  <div className="col-md-2"><input type="number" className="form-control" name="grade_value" placeholder="Grade" value={gradeForm.grade_value} onChange={handleGradeChange} required step="0.01" /></div>
                  <div className="col-md-2"><button type="submit" className="btn btn-primary w-100">Add Grade</button></div>
                </div>
              </form>
              <h3>Grades</h3>
              <table className="table table-striped">
                <thead>
                  <tr><th>Student ID</th><th>Subject</th><th>Grade</th><th>Date</th></tr>
                </thead>
                <tbody>
                  {grades.map(g => (
                    <tr key={`${g.student_id}-${g.subject}-${g.date}`}><td>{g.student_id}</td><td>{g.subject}</td><td>{g.grade.toFixed(2)}</td><td>{g.date}</td></tr>
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

export default StudentManagement;
