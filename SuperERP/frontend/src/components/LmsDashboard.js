import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import Navbar from './Navbar';
import 'bootstrap/dist/css/bootstrap.min.css';

const LmsDashboard = () => {
  const [data, setData] = useState({ courses: [], assignments: [], grades: [] });
  const [error, setError] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    const fetchData = async () => {
      try {
        const token = localStorage.getItem('token');
        if (!token) throw new Error('No token found');
        const response = await axios.get('http://127.0.0.1:8000/api/dashboard/education/lms/', {
          headers: { Authorization: `Bearer ${token}` },
        });
        setData(response.data);
        setError('');
      } catch (err) {
        setError(err.response?.data?.error || 'Failed to load LMS');
        if (err.response?.status === 403) {
          localStorage.removeItem('token');
          navigate('/');
        }
      }
    };
    fetchData();
  }, [navigate]);

  return (
    <>
      <Navbar />
      <div className="container-fluid py-5" style={{ backgroundColor: '#f8f9fa', minHeight: '100vh' }}>
        <div className="row justify-content-center">
          <div className="col-md-10">
            <div className="card shadow p-4">
              <h1 className="display-4 text-primary mb-4">LMS Dashboard</h1>
              {error && <p className="text-danger">{error}</p>}
              <h3>Courses</h3>
              <ul>{data.courses.map(c => <li key={c.id}>{c.name} ({c.code})</li>)}</ul>
              <h3>Assignments</h3>
              <ul>{data.assignments.map(a => <li key={a.id}>{a.title} - Due: {new Date(a.due_date).toLocaleString()}</li>)}</ul>
              <h3>Grades</h3>
              <ul>{data.grades.map(g => <li key={g.assignment}>{g.assignment}: {g.score}</li>)}</ul>
            </div>
          </div>
        </div>
      </div>
    </>
  );
};

export default LmsDashboard;
