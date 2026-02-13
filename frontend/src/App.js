import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import './App.css';
import Dashboard from './pages/Dashboard';
import LLMProviders from './pages/LLMProviders';
import Projects from './pages/Projects';
import ProjectDetail from './pages/ProjectDetail';
import CreateProject from './pages/CreateProject';

function App() {
  return (
    <Router>
      <div className="App">
        <nav className="navbar">
          <div className="container">
            <Link to="/" className="logo">
              <h1>🤖 TestGen</h1>
            </Link>
            <div className="nav-links">
              <Link to="/">Dashboard</Link>
              <Link to="/projects">Projects</Link>
              <Link to="/llm-providers">LLM Providers</Link>
            </div>
          </div>
        </nav>
        
        <main className="main-content">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/projects" element={<Projects />} />
            <Route path="/projects/new" element={<CreateProject />} />
            <Route path="/projects/:id" element={<ProjectDetail />} />
            <Route path="/llm-providers" element={<LLMProviders />} />
          </Routes>
        </main>
        
        <footer className="footer">
          <div className="container">
            <p>&copy; 2024 TestGen - AI-Powered Test Generation Platform</p>
          </div>
        </footer>
      </div>
    </Router>
  );
}

export default App;
