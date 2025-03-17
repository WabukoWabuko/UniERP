import React from 'react';
import { Link } from 'react-router-dom';
import 'bootstrap/dist/css/bootstrap.min.css';

const erps = [
  { name: 'Education ERP', id: 'education', description: 'Manage schools effortlessly.' },
  { name: 'Small Business ERP', id: 'small-business', description: 'Streamline small business operations.' },
  { name: 'Freelancer ERP', id: 'freelancer', description: 'Boost freelance productivity.' },
  { name: 'Retail/E-commerce ERP', id: 'retail', description: 'Power your online store.' },
  { name: 'Nonprofit ERP', id: 'nonprofit', description: 'Support nonprofit missions.' },
  { name: 'Manufacturing ERP', id: 'manufacturing', description: 'Optimize production.' },
  { name: 'Healthcare ERP', id: 'healthcare', description: 'Enhance patient care.' },
  { name: 'HR ERP', id: 'hr', description: 'Simplify HR tasks.' },
  { name: 'Financial ERP', id: 'financial', description: 'Master your finances.' },
  { name: 'CRM ERP', id: 'crm', description: 'Grow customer relationships.' },
];

const LandingPage = () => {
  return (
    <div className="container mt-5">
      <h1 className="text-center mb-4">SuperERP</h1>
      <p className="text-center mb-5">Explore our powerful ERP solutions:</p>
      <div className="row">
        {erps.map((erp) => (
          <div className="col-md-4 mb-4" key={erp.id}>
            <Link to={`/erp/${erp.id}`} className="text-decoration-none">
              <div className="card h-100 shadow-sm">
                <div className="card-body text-center">
                  <h5 className="card-title">{erp.name}</h5>
                  <p className="card-text">{erp.description}</p>
                </div>
              </div>
            </Link>
          </div>
        ))}
      </div>
    </div>
  );
};

export default LandingPage;
