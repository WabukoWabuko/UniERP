import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import Navbar from './Navbar';
import 'bootstrap/dist/css/bootstrap.min.css';

const DashboardHub = () => {
  const [erps, setErps] = useState([]);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    const fetchDashboard = async () => {
      try {
        const response = await axios.get('http://127.0.0.1:8000/api/dashboard/', {
          headers: { Authorization: `Bearer ${localStorage.getItem('token')}` },
        });
        setErps(response.data.available_erps);
      } catch (err) {
        setError('Failed to load dashboard. Please log in again.');
        localStorage.removeItem('token');
        navigate('/');
      }
    };
    fetchDashboard();
  }, [navigate]);

  return (
    <>
      <Navbar />
      <div className="container-fluid py-5" style={{ backgroundColor: '#f8f9fa', minHeight: '100vh' }}>
        <div className="row justify-content-center">
          <div className="col-md-10">
            <div className="card shadow p-4">
              <h1 className="display-4 text-primary mb-4">SuperERP Dashboard</h1>
              <p className="lead">Welcome! Pick your ERP below:</p>
              {error && <p className="text-danger">{error}</p>}
              <div className="row mt-5">
                {erps.map((erp) => (
                  <div className="col-md-4 mb-3" key={erp.id}>
                    <div className="card bg-light p-3 text-center">
                      <h5>{erp.name}</h5>
                      <button
                        className="btn btn-primary mt-2"
                        onClick={() => navigate(erp.url)}
                      >
                        Go to Dashboard
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>
    </>
  );
};

export default DashboardHub;
