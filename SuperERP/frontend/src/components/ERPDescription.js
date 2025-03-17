import React, { useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import axios from 'axios';
import 'bootstrap/dist/css/bootstrap.min.css';
import './ERPDescription.css';

const erpDetails = {
  education: { name: 'Education ERP', desc: 'Manage students, staff, and schedules with ease. Perfect for schools and educational institutions.', tagline: 'Empower Education' },
  'small-business': { name: 'Small Business ERP', desc: 'Track inventory, finances, and customers for small business success.', tagline: 'Grow Smarter' },
  freelancer: { name: 'Freelancer ERP', desc: 'Organize tasks, log time, and invoice clients seamlessly.', tagline: 'Work Your Way' },
  retail: { name: 'Retail/E-commerce ERP', desc: 'Run your store or e-commerce platform with powerful tools.', tagline: 'Sell with Ease' },
  nonprofit: { name: 'Nonprofit ERP', desc: 'Coordinate donors, volunteers, and campaigns for your mission.', tagline: 'Drive Impact' },
  manufacturing: { name: 'Manufacturing ERP', desc: 'Streamline production, supply chain, and quality control.', tagline: 'Build Better' },
  healthcare: { name: 'Healthcare ERP', desc: 'Enhance patient care with efficient management tools.', tagline: 'Care Connected' },
  hr: { name: 'HR ERP', desc: 'Simplify employee management, payroll, and recruitment.', tagline: 'People First' },
  financial: { name: 'Financial ERP', desc: 'Master budgets, accounting, and audits with precision.', tagline: 'Money Matters' },
  crm: { name: 'CRM ERP', desc: 'Build stronger customer relationships with lead and support tracking.', tagline: 'Customer Love' },
};

const ERPDescription = () => {
  const { erpId } = useParams();
  const navigate = useNavigate();
  const erp = erpDetails[erpId] || { name: 'Unknown ERP', desc: 'Details not found.', tagline: 'Explore More' };
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [error, setError] = useState('');
  const [isRegistering, setIsRegistering] = useState(false);

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('http://127.0.0.1:8000/api/login/', { email, password });
      localStorage.setItem('token', response.data.access);
      navigate(`/dashboard/${erpId}`);
    } catch (err) {
      setError(err.response?.data?.error || 'Login failed. Please try again.');
    }
  };

  const handleRegister = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('http://127.0.0.1:8000/api/register/', {
        email,
        password,
        confirm_password: confirmPassword,
        erp_id: erpId,  // Send ERP ID to backend
      });
      localStorage.setItem('token', response.data.access);
      navigate(`/dashboard/${erpId}`);
    } catch (err) {
      setError(err.response?.data?.error || 'Registration failed. Please try again.');
    }
  };

  const handleToggle = () => {
    setIsRegistering(!isRegistering);
    setError('');
    setPassword('');
    setConfirmPassword('');
  };

  return (
    <div className="container-fluid erp-page py-5">
      <div className="row justify-content-center">
        <div className="col-md-7 col-lg-6">
          <div className="erp-content p-4 rounded shadow-sm bg-white">
            <h1 className="display-4 fw-bold text-primary">{erp.name}</h1>
            <p className="lead text-muted">{erp.tagline}</p>
            <p className="mt-3">{erp.desc}</p>
            <ul className="list-unstyled mt-4">
              <li className="mb-2">✔ Feature 1: Placeholder for {erp.name}</li>
              <li className="mb-2">✔ Feature 2: More awesomeness</li>
              <li>✔ Feature 3: Why this ERP rocks</li>
            </ul>
          </div>
        </div>
        <div className="col-md-5 col-lg-4">
          <div className="auth-card p-4 rounded shadow">
            <h3 className="text-center mb-4">{isRegistering ? 'Join Now' : 'Welcome Back'}</h3>
            {error && <p className="text-danger text-center">{error}</p>}
            <form onSubmit={isRegistering ? handleRegister : handleLogin}>
              <div className="mb-3">
                <input
                  type="email"
                  className="form-control form-control-lg"
                  placeholder="Email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  required
                />
              </div>
              <div className="mb-4">
                <input
                  type="password"
                  className="form-control form-control-lg"
                  placeholder="Password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  required
                />
              </div>
              {isRegistering && (
                <div className="mb-4">
                  <input
                    type="password"
                    className="form-control form-control-lg"
                    placeholder="Confirm Password"
                    value={confirmPassword}
                    onChange={(e) => setConfirmPassword(e.target.value)}
                    required
                  />
                </div>
              )}
              <button type="submit" className="btn btn-primary btn-lg w-100 mb-3">
                {isRegistering ? 'Register' : 'Login'}
              </button>
              <p className="text-center mb-0">
                {isRegistering ? 'Already have an account?' : 'Need an account?'}
                <button
                  type="button"
                  className="btn btn-link text-primary fw-bold"
                  onClick={handleToggle}
                >
                  {isRegistering ? 'Login' : 'Register'}
                </button>
              </p>
            </form>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ERPDescription;
