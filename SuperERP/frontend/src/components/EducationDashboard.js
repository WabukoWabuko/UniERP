import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import Navbar from './Navbar';
import 'bootstrap/dist/css/bootstrap.min.css';
import { Bar } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend } from 'chart.js';

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

const EducationDashboard = () => {
  const [data, setData] = useState({});
  const navigate = useNavigate();

  useEffect(() => {
    const fetchDashboard = async () => {
      try {
        const response = await axios.get('http://127.0.0.1:8000/api/education/dashboard/', {
          headers: { Authorization: `Bearer ${localStorage.getItem('token')}` },
        });
        setData(response.data);
      } catch (err) {
        localStorage.removeItem('token');
        navigate('/');
      }
    };
    fetchDashboard();
  }, [navigate]);

  const chartData = {
    labels: ['Students', 'Staff', 'Fees Due', 'Attendance Today'],
    datasets: [{
      label: 'Overview',
      data: [data.total_students || 0, data.total_staff || 0, data.total_fees_due || 0, data.attendance_today || 0],
      backgroundColor: ['#007bff', '#28a745', '#dc3545', '#ffc107'],
    }],
  };

  return (
    <>
      <Navbar />
      <div className="container-fluid py-5" style={{ backgroundColor: '#f8f9fa', minHeight: '100vh' }}>
        <div className="row justify-content-center">
          <div className="col-md-10">
            <div className="card shadow p-4">
              <h1 className="display-4 text-primary mb-4">Education ERP Dashboard</h1>
              <div className="row mb-4">
                <div className="col-md-6">
                  <Bar data={chartData} options={{ responsive: true, scales: { y: { beginAtZero: true } } }} />
                </div>
                <div className="col-md-6">
                  <p>Total Students: {data.total_students}</p>
                  <p>Total Staff: {data.total_staff}</p>
                  <p>Total Fees Due: ${data.total_fees_due?.toFixed(2)}</p>
                  <p>Attendance Today: {data.attendance_today}</p>
                </div>
              </div>
              <div className="row mt-5">
                <div className="col-md-4">
                  <div className="card bg-light p-3">
                    <h5>Students</h5>
                    <button className="btn btn-primary mt-2" onClick={() => navigate('/dashboard/education/students')}>
                      Manage Students
                    </button>
                  </div>
                </div>
                <div className="col-md-4">
                  <div className="card bg-light p-3">
                    <h5>Staff</h5>
                    <button className="btn btn-primary mt-2" onClick={() => navigate('/dashboard/education/staff')}>
                      Manage Staff
                    </button>
                  </div>
                </div>
                <div className="col-md-4">
                  <div className="card bg-light p-3">
                    <h5>Scheduling</h5>
                    <button className="btn btn-primary mt-2" onClick={() => navigate('/dashboard/education/scheduling')}>
                      Manage Scheduling
                    </button>
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
