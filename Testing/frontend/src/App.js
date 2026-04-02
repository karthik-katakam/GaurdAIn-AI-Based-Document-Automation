import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';

import AdminLogin from './pages/AdminLogin';
import ActivityLog from './pages/ActivityLog';
import AdminRegister from './pages/AdminRegister';
import FileAnalysis from './pages/FileAnalysis';
import Directory from './pages/Directory';
import CaseDetail from './pages/CaseDetail';
import CaseListings from './pages/CaseListings';
import Upload from './pages/Upload';
import Dashboard from './pages/Dashboard';
//import Dashboard from './components/Dashboard'; // Assuming you'll move Dashboard here
import LandingPage from './pages/LandingPage'; // Added LandingPage
import './styles.css';


function App() {
  return (
    
    <Router>
      <Routes>
        <Route path="/" element={<LandingPage />} /> 
        <Route path="/login" element={<AdminLogin />} />
        <Route path="/register" element={<AdminRegister />} />
        <Route path="/upload" element={<Upload />} />
        <Route path="/activity-log" element={<ActivityLog />} />
        <Route path="/case-listings" element={<CaseListings />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/case-detail/:id" element={<CaseDetail />} />
        <Route path="/directory" element={<Directory />} />
        <Route path="/file-analysis" element={<FileAnalysis />} />
        
      </Routes>
    </Router>
    
  );
}

if(process.env.REACT_APP_SITE_KEY){
  console.log("REACT_APP_SITE_KEY IS VALID")
}



export default App;