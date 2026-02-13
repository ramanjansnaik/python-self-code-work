import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { projectAPI, llmProviderAPI } from '../services/api';

function Dashboard() {
  const [stats, setStats] = useState({
    projects: 0,
    providers: 0,
    tests: 0,
  });
  const [loading, setLoading] = useState(true);
  const [recentProjects, setRecentProjects] = useState([]);

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      const [projectsRes, providersRes] = await Promise.all([
        projectAPI.list(),
        llmProviderAPI.list(),
      ]);

      const projects = projectsRes.data.results || projectsRes.data;
      const providers = providersRes.data.results || providersRes.data;

      const totalTests = projects.reduce((sum, p) => sum + (p.generated_tests?.length || 0), 0);

      setStats({
        projects: projects.length,
        providers: providers.length,
        tests: totalTests,
      });

      setRecentProjects(projects.slice(0, 5));
      setLoading(false);
    } catch (error) {
      console.error('Error fetching dashboard data:', error);
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="loading">Loading dashboard...</div>;
  }

  return (
    <div>
      <div className="card">
        <h1>Welcome to TestGen 🚀</h1>
        <p style={{ marginTop: '1rem', color: '#718096' }}>
          AI-powered test generation platform for Playwright and Selenium
        </p>
      </div>

      <div className="grid grid-2">
        <div className="card">
          <h3>📊 Projects</h3>
          <div style={{ fontSize: '2.5rem', fontWeight: 'bold', margin: '1rem 0', color: '#667eea' }}>
            {stats.projects}
          </div>
          <Link to="/projects" className="btn btn-primary">
            View All Projects
          </Link>
        </div>

        <div className="card">
          <h3>🤖 LLM Providers</h3>
          <div style={{ fontSize: '2.5rem', fontWeight: 'bold', margin: '1rem 0', color: '#667eea' }}>
            {stats.providers}
          </div>
          <Link to="/llm-providers" className="btn btn-primary">
            Manage Providers
          </Link>
        </div>

        <div className="card">
          <h3>✅ Generated Tests</h3>
          <div style={{ fontSize: '2.5rem', fontWeight: 'bold', margin: '1rem 0', color: '#667eea' }}>
            {stats.tests}
          </div>
          <p style={{ color: '#718096' }}>Total tests generated</p>
        </div>

        <div className="card">
          <h3>⚡ Quick Actions</h3>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem', marginTop: '1rem' }}>
            <Link to="/projects/new" className="btn btn-success">
              + Create New Project
            </Link>
            <Link to="/llm-providers" className="btn btn-secondary">
              + Add LLM Provider
            </Link>
          </div>
        </div>
      </div>

      {recentProjects.length > 0 && (
        <div className="card" style={{ marginTop: '2rem' }}>
          <h2>Recent Projects</h2>
          <div style={{ marginTop: '1rem' }}>
            {recentProjects.map((project) => (
              <div
                key={project.id}
                style={{
                  padding: '1rem',
                  borderBottom: '1px solid #e2e8f0',
                  display: 'flex',
                  justifyContent: 'space-between',
                  alignItems: 'center',
                }}
              >
                <div>
                  <h4>{project.name}</h4>
                  <p style={{ color: '#718096', fontSize: '0.875rem', marginTop: '0.25rem' }}>
                    {project.framework} • {project.language} • {project.generated_tests?.length || 0} tests
                  </p>
                </div>
                <Link to={`/projects/${project.id}`} className="btn btn-secondary">
                  View Details
                </Link>
              </div>
            ))}
          </div>
        </div>
      )}

      <div className="card" style={{ marginTop: '2rem', background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)', color: 'white' }}>
        <h2>🎯 Getting Started</h2>
        <ol style={{ marginTop: '1rem', paddingLeft: '1.5rem', lineHeight: '2' }}>
          <li>Configure an LLM provider (OpenAI, Anthropic, Google, or Ollama)</li>
          <li>Create a new test project with your website details</li>
          <li>Add server configurations if needed</li>
          <li>Generate tests using AI by describing test scenarios</li>
          <li>Download generated tests and CI/CD pipeline configuration</li>
        </ol>
      </div>
    </div>
  );
}

export default Dashboard;
