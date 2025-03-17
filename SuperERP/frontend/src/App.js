import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import LandingPage from './components/LandingPage';
import ERPDescription from './components/ERPDescription';
import EducationDashboard from './components/EducationDashboard';
import SmallBusinessDashboard from './components/SmallBusinessDashboard';

const ProtectedRoute = ({ children }) => {
  const token = localStorage.getItem('token');
  return token ? children : <Navigate to="/" />;
};

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/erp/:erpId" element={<ERPDescription />} />
        <Route
          path="/dashboard/education"
          element={<ProtectedRoute><EducationDashboard /></ProtectedRoute>}
        />
        <Route
          path="/dashboard/small-business"
          element={<ProtectedRoute><SmallBusinessDashboard /></ProtectedRoute>}
        />
        {/* Add other 8 ERPs later */}
      </Routes>
    </Router>
  );
}

export default App;
