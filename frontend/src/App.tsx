import React from 'react';
import { Routes, Route } from 'react-router-dom';
import InstancesPage from './components/InstancesPage';
import './App.css';

function App() {
  return (
    <div className="app">
      <nav className="navbar">
        <div className="nav-brand">Prism Hub</div>
        <ul className="nav-links">
          <li><Link to="/">Instances</Link></li>
          <li><Link to="/settings">Settings</Link></li>
        </ul>
      </nav>
      <main className="main-content">
        <Routes>
          <Route path="/" element={<InstancesPage />} />
          <Route path="/instances" element={<InstancesPage />} />
          <Route path="/settings" element={<SettingsPage />} />
        </Routes>
      </main>
    </div>
  );
}

const SettingsPage: React.FC = () => (
  <div className="settings-page">
    <h1>Settings</h1>
    <p>Settings page - coming soon</p>
  </div>
);

import { Link } from 'react-router-dom';

export default App;