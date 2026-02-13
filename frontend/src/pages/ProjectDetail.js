import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { projectAPI, generatedTestAPI } from '../services/api';

function ProjectDetail() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [project, setProject] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [generating, setGenerating] = useState(false);
  const [generatingCICD, setGeneratingCICD] = useState(false);
  
  const [testScenarios, setTestScenarios] = useState(['']);
  const [testConfig, setTestConfig] = useState({
    include_setup: true,
    include_teardown: true,
    headless: true,
    browser: 'chromium',
    timeout: 30000,
  });
  
  const [cicdConfig, setCicdConfig] = useState({
    provider: 'github_actions',
    on_push: true,
    on_pull_request: true,
    cron_schedule: '0 0 * * *',
  });

  useEffect(() => {
    fetchProject();
  }, [id]);

  const fetchProject = async () => {
    try {
      const response = await projectAPI.get(id);
      setProject(response.data);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching project:', error);
      setError('Failed to load project');
      setLoading(false);
    }
  };

  const handleGenerateTests = async () => {
    setError('');
    setSuccess('');
    setGenerating(true);

    const validScenarios = testScenarios.filter(s => s.trim() !== '');
    
    if (validScenarios.length === 0) {
      setError('Please add at least one test scenario');
      setGenerating(false);
      return;
    }

    try {
      const response = await projectAPI.generateTests(id, {
        test_scenarios: validScenarios,
        ...testConfig,
      });

      setSuccess(`Generated ${response.data.successful} tests successfully!`);
      if (response.data.failed > 0) {
        setError(`Failed to generate ${response.data.failed} tests`);
      }
      
      fetchProject();
    } catch (error) {
      setError(error.response?.data?.error || 'Failed to generate tests');
    } finally {
      setGenerating(false);
    }
  };

  const handleGenerateCICD = async () => {
    setError('');
    setSuccess('');
    setGeneratingCICD(true);

    try {
      const response = await projectAPI.generateCICD(id, cicdConfig);
      setSuccess(response.data.message);
      fetchProject();
    } catch (error) {
      setError(error.response?.data?.error || 'Failed to generate CI/CD pipeline');
    } finally {
      setGeneratingCICD(false);
    }
  };

  const handleDownloadTests = async () => {
    try {
      const response = await projectAPI.downloadTests(id);
      const data = response.data;
      
      const zip = data.tests.map(test => ({
        name: test.file_name,
        content: test.test_code,
      }));

      zip.forEach(file => {
        const blob = new Blob([file.content], { type: 'text/plain' });
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = file.name;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        window.URL.revokeObjectURL(url);
      });

      setSuccess('Tests downloaded successfully!');
    } catch (error) {
      setError('Failed to download tests');
    }
  };

  const handleDownloadCICD = () => {
    if (!project.cicd_pipeline) {
      setError('No CI/CD pipeline generated yet');
      return;
    }

    const blob = new Blob([project.cicd_pipeline.config_content], { type: 'text/plain' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = project.cicd_pipeline.file_path.split('/').pop();
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    window.URL.revokeObjectURL(url);
    setSuccess('CI/CD pipeline downloaded successfully!');
  };

  const addScenario = () => {
    setTestScenarios([...testScenarios, '']);
  };

  const updateScenario = (index, value) => {
    const updated = [...testScenarios];
    updated[index] = value;
    setTestScenarios(updated);
  };

  const removeScenario = (index) => {
    setTestScenarios(testScenarios.filter((_, i) => i !== index));
  };

  if (loading) {
    return <div className="loading">Loading project...</div>;
  }

  if (!project) {
    return <div className="error">Project not found</div>;
  }

  return (
    <div>
      <div className="card">
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start' }}>
          <div>
            <h1>{project.name}</h1>
            <div style={{ display: 'flex', gap: '0.5rem', marginTop: '0.5rem' }}>
              <span className="badge badge-info">{project.framework}</span>
              <span className="badge badge-info">{project.language}</span>
            </div>
          </div>
          <button className="btn btn-secondary" onClick={() => navigate('/projects')}>
            ← Back to Projects
          </button>
        </div>

        {project.description && (
          <p style={{ marginTop: '1rem', color: '#718096' }}>{project.description}</p>
        )}

        <div style={{ marginTop: '1rem' }}>
          <p><strong>Website:</strong> {project.website_url}</p>
          <p><strong>LLM Provider:</strong> {project.llm_provider_details?.name || 'Not configured'}</p>
          <p><strong>Generated Tests:</strong> {project.generated_tests?.length || 0}</p>
        </div>
      </div>

      {error && <div className="error">{error}</div>}
      {success && <div className="success">{success}</div>}

      <div className="card">
        <h2>Generate Tests</h2>
        <p style={{ color: '#718096', marginBottom: '1rem' }}>
          Describe test scenarios and let AI generate executable test code
        </p>

        <div className="form-group">
          <label>Test Scenarios</label>
          {testScenarios.map((scenario, index) => (
            <div key={index} style={{ display: 'flex', gap: '0.5rem', marginBottom: '0.5rem' }}>
              <input
                type="text"
                value={scenario}
                onChange={(e) => updateScenario(index, e.target.value)}
                placeholder="e.g., Test user login with valid credentials"
                style={{ flex: 1 }}
              />
              {testScenarios.length > 1 && (
                <button
                  type="button"
                  className="btn btn-danger"
                  onClick={() => removeScenario(index)}
                  style={{ padding: '0.75rem 1rem' }}
                >
                  Remove
                </button>
              )}
            </div>
          ))}
          <button type="button" className="btn btn-secondary" onClick={addScenario}>
            + Add Scenario
          </button>
        </div>

        <div className="grid grid-2">
          <div className="form-group">
            <label>Browser</label>
            <select
              value={testConfig.browser}
              onChange={(e) => setTestConfig({ ...testConfig, browser: e.target.value })}
            >
              <option value="chromium">Chromium</option>
              <option value="firefox">Firefox</option>
              <option value="webkit">WebKit</option>
            </select>
          </div>

          <div className="form-group">
            <label>Timeout (ms)</label>
            <input
              type="number"
              value={testConfig.timeout}
              onChange={(e) => setTestConfig({ ...testConfig, timeout: parseInt(e.target.value) })}
            />
          </div>
        </div>

        <div style={{ display: 'flex', gap: '1rem', marginTop: '1rem' }}>
          <label>
            <input
              type="checkbox"
              checked={testConfig.headless}
              onChange={(e) => setTestConfig({ ...testConfig, headless: e.target.checked })}
              style={{ marginRight: '0.5rem' }}
            />
            Headless Mode
          </label>
          <label>
            <input
              type="checkbox"
              checked={testConfig.include_setup}
              onChange={(e) => setTestConfig({ ...testConfig, include_setup: e.target.checked })}
              style={{ marginRight: '0.5rem' }}
            />
            Include Setup
          </label>
          <label>
            <input
              type="checkbox"
              checked={testConfig.include_teardown}
              onChange={(e) => setTestConfig({ ...testConfig, include_teardown: e.target.checked })}
              style={{ marginRight: '0.5rem' }}
            />
            Include Teardown
          </label>
        </div>

        <button
          className="btn btn-success"
          onClick={handleGenerateTests}
          disabled={generating}
          style={{ marginTop: '1rem' }}
        >
          {generating ? 'Generating Tests...' : '🤖 Generate Tests'}
        </button>
      </div>

      {project.generated_tests && project.generated_tests.length > 0 && (
        <div className="card">
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <h2>Generated Tests ({project.generated_tests.length})</h2>
            <button className="btn btn-primary" onClick={handleDownloadTests}>
              📥 Download All Tests
            </button>
          </div>

          <div style={{ marginTop: '1rem' }}>
            {project.generated_tests.map((test) => (
              <div
                key={test.id}
                style={{
                  padding: '1rem',
                  background: '#f7fafc',
                  borderRadius: '6px',
                  marginBottom: '1rem',
                }}
              >
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start' }}>
                  <div>
                    <h4>{test.test_name}</h4>
                    <span className={`badge badge-${test.status === 'completed' ? 'success' : test.status === 'failed' ? 'danger' : 'warning'}`}>
                      {test.status}
                    </span>
                  </div>
                  <span style={{ fontSize: '0.875rem', color: '#718096' }}>
                    {test.generation_time ? `${test.generation_time.toFixed(2)}s` : ''}
                  </span>
                </div>
                <p style={{ color: '#718096', marginTop: '0.5rem' }}>{test.test_description}</p>
                <p style={{ fontSize: '0.875rem', color: '#a0aec0', marginTop: '0.5rem' }}>
                  File: {test.file_name}
                </p>
              </div>
            ))}
          </div>
        </div>
      )}

      <div className="card">
        <h2>CI/CD Pipeline Configuration</h2>
        <p style={{ color: '#718096', marginBottom: '1rem' }}>
          Generate GitHub Actions or GitLab CI pipeline configuration
        </p>

        <div className="grid grid-2">
          <div className="form-group">
            <label>CI/CD Provider</label>
            <select
              value={cicdConfig.provider}
              onChange={(e) => setCicdConfig({ ...cicdConfig, provider: e.target.value })}
            >
              <option value="github_actions">GitHub Actions</option>
              <option value="gitlab_ci">GitLab CI</option>
            </select>
          </div>

          <div className="form-group">
            <label>Cron Schedule</label>
            <input
              type="text"
              value={cicdConfig.cron_schedule}
              onChange={(e) => setCicdConfig({ ...cicdConfig, cron_schedule: e.target.value })}
              placeholder="0 0 * * *"
            />
          </div>
        </div>

        <div style={{ display: 'flex', gap: '1rem', marginTop: '1rem' }}>
          <label>
            <input
              type="checkbox"
              checked={cicdConfig.on_push}
              onChange={(e) => setCicdConfig({ ...cicdConfig, on_push: e.target.checked })}
              style={{ marginRight: '0.5rem' }}
            />
            Run on Push
          </label>
          <label>
            <input
              type="checkbox"
              checked={cicdConfig.on_pull_request}
              onChange={(e) => setCicdConfig({ ...cicdConfig, on_pull_request: e.target.checked })}
              style={{ marginRight: '0.5rem' }}
            />
            Run on Pull Request
          </label>
        </div>

        <div style={{ display: 'flex', gap: '1rem', marginTop: '1rem' }}>
          <button
            className="btn btn-success"
            onClick={handleGenerateCICD}
            disabled={generatingCICD}
          >
            {generatingCICD ? 'Generating...' : '⚙️ Generate Pipeline'}
          </button>
          
          {project.cicd_pipeline && (
            <button className="btn btn-primary" onClick={handleDownloadCICD}>
              📥 Download Pipeline Config
            </button>
          )}
        </div>

        {project.cicd_pipeline && (
          <div style={{ marginTop: '1rem', padding: '1rem', background: '#f7fafc', borderRadius: '6px' }}>
            <p><strong>Provider:</strong> {project.cicd_pipeline.provider}</p>
            <p><strong>File:</strong> {project.cicd_pipeline.file_path}</p>
            <p style={{ fontSize: '0.875rem', color: '#718096', marginTop: '0.5rem' }}>
              Last updated: {new Date(project.cicd_pipeline.updated_at).toLocaleString()}
            </p>
          </div>
        )}
      </div>
    </div>
  );
}

export default ProjectDetail;
