import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import LandingPage from './pages/LandingPage';
import LoginPage from './pages/LoginPage';
import TrainerPage from './pages/TrainerPage';
import PatientPage from './pages/PatientPage';
import './App.css';

function App() {
  return (
    <Router>
      <div className="App">
        <Routes>
          <Route path="/" element={<LandingPage />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/trainer" element={<TrainerPage />} />
          <Route path="/patient" element={<PatientPage />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
