import React, { useState, useEffect } from 'react';
import axios from 'axios';
import 'bootstrap/dist/css/bootstrap.min.css';

const SmallBusinessDashboard = () => {
  const [message, setMessage] = useState('');

  useEffect(() => {
    const fetchDashboard = async () => {
      try {
        const response = await axios.get('http://127.0.0.1:8000/api/small-business/dashboard/', {
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
    <div className="container-fluid py-5" style={{ backgroundColor: '#f8f9fa', minHeight: '100vh' }}>
      <div className="row justify-content-center">
        <div className="col-md-10">
          <div className="card shadow p-4">
            <h1 className="display-4 text-primary mb-4">Small Business ERP Dashboard</h1>
            <p className="lead">{message}</p>
            <div className="row mt-5">
              <div className="col-md-4">
                <div className="card bg-light p-3">
                  <h5>Inventory</h5>
                  <p>Track stock levels and updates.</p>
                </div>
              </div>
              <div className="col-md-4">
                <div className="card bg-light p-3">
                  <h5>Accounting</h5>
                  <p>Manage finances and reports.</p>
                </div>
              </div>
              <div className="col-md-4">
                <div className="card bg-light p-3">
                  <h5>Customers</h5>
                  <p>Handle client info and orders.</p>
                </div>
              </div>
            </div>
            <button
              className="btn btn-outline-danger mt-4"
              onClick={() => {
                localStorage.removeItem('token');
                window.location.href = '/';
              }}
            >
              Logout
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SmallBusinessDashboard;
