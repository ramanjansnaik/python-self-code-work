import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { projectAPI } from '../services/api';

function Projects() {
  const [projects, setProjects] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchProjects();
  }, []);

  const fetchProjects = async () => {
    try {
      const response = await projectAPI.list();
      setProjects(response.data.results || response.data);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching projects:', error);
      setError('Failed to load projects');
      setLoading(false);
    }
  };

  const handleDelete = async (id) => {
    if (!window.confirm('Are you sure you want to delete this project?')) {
      return;
    }

    try {
      await projectAPI.delete(id);
      fetchProjects();
    } catch (error) {
      setError('Failed to delete project');
    }
  };

  if (loading) {
    return <div className="loading">Loading projects...</div>;
  }

  return (
    <div>
      <div className="card">
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <h1>Test Projects</h1>
          <Link to="/projects/new" className="btn btn-primary">
            + Create Project
          </Link>
        </div>
      </div>

      {error && <div className="error">{error}</div>}

      <div className="grid grid-2">
        {projects.map((project) => (
          <div key={project.id} className="card">
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start' }}>
              <div>
                <h3>{project.name}</h3>
                <div style={{ display: 'flex', gap: '0.5rem', marginTop: '0.5rem' }}>
                  <span className="badge badge-info">{project.framework}</span>
                  <span className="badge badge-info">{project.language}</span>
                </div>
              </div>
              <button
                className="btn btn-danger"
                onClick={() => handleDelete(project.id)}
                style={{ padding: '0.5rem 1rem' }}
              >
                Delete
              </button>
            </div>
            
            <div style={{ marginTop: '1rem', color: '#718096' }}>
              <p><strong>Website:</strong> {project.website_url}</p>
              <p><strong>Tests:</strong> {project.generated_tests?.length || 0}</p>
              {project.description && (
                <p style={{ marginTop: '0.5rem' }}>{project.description}</p>
              )}
            </div>

            <div style={{ marginTop: '1rem', display: 'flex', gap: '0.5rem' }}>
              <Link
                to={`/projects/${project.id}`}
                className="btn btn-primary"
                style={{ flex: 1 }}
              >
                View Details
              </Link>
            </div>

            <p style={{ fontSize: '0.875rem', color: '#a0aec0', marginTop: '1rem' }}>
              Created: {new Date(project.created_at).toLocaleDateString()}
            </p>
          </div>
        ))}
      </div>

      {projects.length === 0 && (
        <div className="card" style={{ textAlign: 'center', padding: '3rem' }}>
          <h2>No projects yet</h2>
          <p style={{ color: '#718096', marginTop: '1rem' }}>
            Create your first test project to get started!
          </p>
          <Link to="/projects/new" className="btn btn-primary" style={{ marginTop: '1rem' }}>
            Create Your First Project
          </Link>
        </div>
      )}
    </div>
  );
}

export default Projects;
