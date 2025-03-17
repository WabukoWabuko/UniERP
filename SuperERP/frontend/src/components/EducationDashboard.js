import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Navbar from './Navbar';
import 'bootstrap/dist/css/bootstrap.min.css';

const EducationDashboard = () => {
  const [message, setMessage] = useState('');

  useEffect(() => {
    const fetchDashboard = async () => {
      try {
        const response = await axios.get('http://127.0.0.1:8000/api/education/dashboard/', {
          headers: { Authorization: `Bearer ${localStorage.getItem('token')}` },
        });
        setMessage(response.data.message);
      } catch (err) {
        setMessage(err.response?.data?.error || 'Error loading dashboard');
      }
    };
    fetchDashboard();
  }, []);

  return (
    <>
      <Navbar />
      <div className="container-fluid py-5" style={{ backgroundColor: '#f8f9fa', minHeight: '100vh' }}>
        <div className="row justify-content-center">
          <div className="col-md-10">
            <div className="card shadow p-4">
              <h1 className="display-4 text-primary mb-4">Education ERP Dashboard</h1>
              <p className="lead">{message}</p>
              <div className="row mt-5">
                <div className="col-md-4">
                  <div className="card bg-light p-3">
                    <h5>Students</h5>
                    <p>Track student records, grades, and attendance.</p>
                  </div>
                </div>
                <div className="col-md-4">
                  <div className="card bg-light p-3">
                    <h5>Staff</h5>
                    <p>Manage teachers, payroll, and schedules.</p>
                  </div>
                </div>
                <div className="col-md-4">
                  <div className="card bg-light p-3">
                    <h5>Scheduling</h5>
                    <p>Create timetables and track fees.</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </>
  );
};

export default EducationDashboard;
