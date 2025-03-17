import React from 'react';
import { Link } from 'react-router-dom';
import 'bootstrap/dist/css/bootstrap.min.css';

const erps = [
  { name: 'Education ERP', id: 'education', description: 'Manage schools effortlessly.', image: 'https://picsum.photos/300/200?random=1' },
  { name: 'Small Business ERP', id: 'small-business', description: 'Streamline small business operations.', image: 'https://picsum.photos/300/200?random=2' },
  { name: 'Freelancer ERP', id: 'freelancer', description: 'Boost freelance productivity.', image: 'https://picsum.photos/300/200?random=3' },
  { name: 'Retail/E-commerce ERP', id: 'retail', description: 'Power your online store.', image: 'https://picsum.photos/300/200?random=4' },
  { name: 'Nonprofit ERP', id: 'nonprofit', description: 'Support nonprofit missions.', image: 'https://picsum.photos/300/200?random=5' },
  { name: 'Manufacturing ERP', id: 'manufacturing', description: 'Optimize production.', image: 'https://picsum.photos/300/200?random=6' },
  { name: 'Healthcare ERP', id: 'healthcare', description: 'Enhance patient care.', image: 'https://picsum.photos/300/200?random=7' },
  { name: 'HR ERP', id: 'hr', description: 'Simplify HR tasks.', image: 'https://picsum.photos/300/200?random=8' },
  { name: 'Financial ERP', id: 'financial', description: 'Master your finances.', image: 'https://picsum.photos/300/200?random=9' },
  { name: 'CRM ERP', id: 'crm', description: 'Grow customer relationships.', image: 'https://picsum.photos/300/200?random=10' },
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
                <img src={erp.image} className="card-img-top" alt={`${erp.name} preview`} />
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
