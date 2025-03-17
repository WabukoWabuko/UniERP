import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import LandingPage from './components/LandingPage';
import ERPDescription from './components/ERPDescription';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/erp/:erpId" element={<ERPDescription />} />
      </Routes>
    </Router>
  );
}

export default App;
