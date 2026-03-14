import React from 'react';
import './App.css';

function App() {
  return (
    <div className="App">
      <div className="landing-container">
        <h1 className="title">Klinik-dPS</h1>
        <p className="subtitle">Digitales Patientensimulationssystem</p>
        <button 
          className="simulation-button"
          onClick={() => window.location.href = 'http://localhost:5173'}
        >
          Go to Simulation
        </button>
      </div>
    </div>
  );
}

export default App;
