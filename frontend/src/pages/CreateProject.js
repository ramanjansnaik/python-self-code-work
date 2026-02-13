import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { projectAPI, llmProviderAPI } from '../services/api';

function CreateProject() {
  const navigate = useNavigate();
  const [providers, setProviders] = useState([]);
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    website_url: '',
    framework: 'playwright',
    language: 'python',
    llm_provider: '',
  });
  const [serverConfigs, setServerConfigs] = useState([]);
  const [currentServer, setCurrentServer] = useState({
    hostname: '',
    port: 443,
    protocol: 'https',
    username: '',
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchProviders();
  }, []);

  const fetchProviders = async () => {
    try {
      const response = await llmProviderAPI.list();
      const providerList = response.data.results || response.data;
      setProviders(providerList.filter(p => p.is_active));
    } catch (error) {
      console.error('Error fetching providers:', error);
    }
  };

  const addServerConfig = () => {
    if (!currentServer.hostname) {
      alert('Hostname is required');
      return;
    }
    setServerConfigs([...serverConfigs, currentServer]);
    setCurrentServer({
      hostname: '',
      port: 443,
      protocol: 'https',
      username: '',
    });
  };

  const removeServerConfig = (index) => {
    setServerConfigs(serverConfigs.filter((_, i) => i !== index));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const projectData = {
        ...formData,
        server_configs: serverConfigs,
      };

      const response = await projectAPI.create(projectData);
      navigate(`/projects/${response.data.id}`);
    } catch (error) {
      setError(error.response?.data?.detail || 'Failed to create project');
      setLoading(false);
    }
  };

  return (
    <div>
      <div className="card">
        <h1>Create New Test Project</h1>
      </div>

      {error && <div className="error">{error}</div>}

      <form onSubmit={handleSubmit}>
        <div className="card">
          <h2>Project Details</h2>

          <div className="form-group">
            <label>Project Name *</label>
            <input
              type="text"
              value={formData.name}
              onChange={(e) => setFormData({ ...formData, name: e.target.value })}
              required
              placeholder="My E-commerce Tests"
            />
          </div>

          <div className="form-group">
            <label>Description</label>
            <textarea
              value={formData.description}
              onChange={(e) => setFormData({ ...formData, description: e.target.value })}
              placeholder="Describe your test project..."
            />
          </div>

          <div className="form-group">
            <label>Website URL *</label>
            <input
              type="url"
              value={formData.website_url}
              onChange={(e) => setFormData({ ...formData, website_url: e.target.value })}
              required
              placeholder="https://example.com"
            />
          </div>

          <div className="grid grid-2">
            <div className="form-group">
              <label>Framework *</label>
              <select
                value={formData.framework}
                onChange={(e) => setFormData({ ...formData, framework: e.target.value })}
                required
              >
                <option value="playwright">Playwright</option>
                <option value="selenium">Selenium</option>
              </select>
            </div>

            <div className="form-group">
              <label>Language *</label>
              <select
                value={formData.language}
                onChange={(e) => setFormData({ ...formData, language: e.target.value })}
                required
              >
                <option value="python">Python</option>
                <option value="javascript">JavaScript</option>
                <option value="typescript">TypeScript</option>
                <option value="java">Java</option>
                <option value="csharp">C#</option>
              </select>
            </div>
          </div>

          <div className="form-group">
            <label>LLM Provider *</label>
            <select
              value={formData.llm_provider}
              onChange={(e) => setFormData({ ...formData, llm_provider: e.target.value })}
              required
            >
              <option value="">Select a provider...</option>
              {providers.map((provider) => (
                <option key={provider.id} value={provider.id}>
                  {provider.name} ({provider.provider_type})
                </option>
              ))}
            </select>
            {providers.length === 0 && (
              <p style={{ color: '#f56565', fontSize: '0.875rem', marginTop: '0.5rem' }}>
                No active LLM providers found. Please create one first.
              </p>
            )}
          </div>
        </div>

        <div className="card">
          <h2>Server Configuration (Optional)</h2>
          <p style={{ color: '#718096', marginBottom: '1rem' }}>
            Add server details if you need to test against specific environments
          </p>

          <div className="grid grid-2">
            <div className="form-group">
              <label>Hostname</label>
              <input
                type="text"
                value={currentServer.hostname}
                onChange={(e) => setCurrentServer({ ...currentServer, hostname: e.target.value })}
                placeholder="staging.example.com"
              />
            </div>

            <div className="form-group">
              <label>Port</label>
              <input
                type="number"
                value={currentServer.port}
                onChange={(e) => setCurrentServer({ ...currentServer, port: parseInt(e.target.value) })}
              />
            </div>

            <div className="form-group">
              <label>Protocol</label>
              <select
                value={currentServer.protocol}
                onChange={(e) => setCurrentServer({ ...currentServer, protocol: e.target.value })}
              >
                <option value="https">HTTPS</option>
                <option value="http">HTTP</option>
              </select>
            </div>

            <div className="form-group">
              <label>Username</label>
              <input
                type="text"
                value={currentServer.username}
                onChange={(e) => setCurrentServer({ ...currentServer, username: e.target.value })}
                placeholder="admin"
              />
            </div>
          </div>

          <button
            type="button"
            className="btn btn-secondary"
            onClick={addServerConfig}
          >
            + Add Server
          </button>

          {serverConfigs.length > 0 && (
            <div style={{ marginTop: '1.5rem' }}>
              <h3>Added Servers</h3>
              {serverConfigs.map((server, index) => (
                <div
                  key={index}
                  style={{
                    padding: '1rem',
                    background: '#f7fafc',
                    borderRadius: '6px',
                    marginTop: '0.5rem',
                    display: 'flex',
                    justifyContent: 'space-between',
                    alignItems: 'center',
                  }}
                >
                  <div>
                    <strong>{server.protocol}://{server.hostname}:{server.port}</strong>
                    {server.username && <span style={{ color: '#718096', marginLeft: '1rem' }}>User: {server.username}</span>}
                  </div>
                  <button
                    type="button"
                    className="btn btn-danger"
                    onClick={() => removeServerConfig(index)}
                    style={{ padding: '0.5rem 1rem' }}
                  >
                    Remove
                  </button>
                </div>
              ))}
            </div>
          )}
        </div>

        <div style={{ display: 'flex', gap: '1rem' }}>
          <button
            type="submit"
            className="btn btn-success"
            disabled={loading || providers.length === 0}
          >
            {loading ? 'Creating...' : 'Create Project'}
          </button>
          <button
            type="button"
            className="btn btn-secondary"
            onClick={() => navigate('/projects')}
          >
            Cancel
          </button>
        </div>
      </form>
    </div>
  );
}

export default CreateProject;
