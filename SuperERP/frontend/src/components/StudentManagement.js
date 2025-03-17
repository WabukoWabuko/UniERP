import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import Navbar from './Navbar';
import 'bootstrap/dist/css/bootstrap.min.css';

const StudentManagement = () => {
  const [students, setStudents] = useState([]);
  const [formData, setFormData] = useState({ name: '', student_id: '', grade: '', date_of_birth: '' });
  const [error, setError] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    fetchStudents();
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

  const handleInputChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
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
      setStudents(students.filter(student => student.id !== studentId));
      setError('');
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to delete student');
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
                  <div className="col-md-3">
                    <input
                      type="text"
                      className="form-control"
                      name="name"
                      placeholder="Name"
                      value={formData.name}
                      onChange={handleInputChange}
                      required
                    />
                  </div>
                  <div className="col-md-3">
                    <input
                      type="text"
                      className="form-control"
                      name="student_id"
                      placeholder="Student ID"
                      value={formData.student_id}
                      onChange={handleInputChange}
                      required
                    />
                  </div>
                  <div className="col-md-2">
                    <input
                      type="text"
                      className="form-control"
                      name="grade"
                      placeholder="Grade"
                      value={formData.grade}
                      onChange={handleInputChange}
                      required
                    />
                  </div>
                  <div className="col-md-2">
                    <input
                      type="date"
                      className="form-control"
                      name="date_of_birth"
                      value={formData.date_of_birth}
                      onChange={handleInputChange}
                    />
                  </div>
                  <div className="col-md-2">
                    <button type="submit" className="btn btn-primary w-100">Add Student</button>
                  </div>
                </div>
              </form>
              <table className="table table-striped">
                <thead>
                  <tr>
                    <th>Name</th>
                    <th>Student ID</th>
                    <th>Grade</th>
                    <th>Enrollment Date</th>
                    <th>Date of Birth</th>
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {students.map(student => (
                    <tr key={student.id}>
                      <td>{student.name}</td>
                      <td>{student.student_id}</td>
                      <td>{student.grade}</td>
                      <td>{student.enrollment_date}</td>
                      <td>{student.date_of_birth || 'N/A'}</td>
                      <td>
                        <button
                          className="btn btn-danger btn-sm"
                          onClick={() => handleDeleteStudent(student.id)}
                        >
                          Delete
                        </button>
                      </td>
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

export default StudentManagement;
