import React from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';

const EducationDashboard = () => {
  const token = localStorage.getItem('token');

  return (
    <div className="container-fluid py-5" style={{ backgroundColor: '#f8f9fa', minHeight: '100vh' }}>
      <div className="row justify-content-center">
        <div className="col-md-10">
          <div className="card shadow p-4">
            <h1 className="display-4 text-primary mb-4">Education ERP Dashboard</h1>
            <p className="lead">Welcome to your Education ERP! Manage your school like a pro.</p>
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
            <button
              className="btn btn-outline-danger mt-4"
              onClick={() => localStorage.removeItem('token') && window.location.reload()}
            >
              Logout
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default EducationDashboard;
