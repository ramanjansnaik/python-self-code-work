import React, { useEffect, useState } from 'react';
import { llmProviderAPI } from '../services/api';

function LLMProviders() {
  const [providers, setProviders] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState({
    name: '',
    provider_type: 'openai',
    api_endpoint: '',
    api_key: '',
    model_name: 'gpt-4',
    is_active: true,
  });
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  useEffect(() => {
    fetchProviders();
  }, []);

  const fetchProviders = async () => {
    try {
      const response = await llmProviderAPI.list();
      setProviders(response.data.results || response.data);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching providers:', error);
      setError('Failed to load LLM providers');
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');

    try {
      await llmProviderAPI.create(formData);
      setSuccess('LLM Provider created successfully!');
      setShowForm(false);
      setFormData({
        name: '',
        provider_type: 'openai',
        api_endpoint: '',
        api_key: '',
        model_name: 'gpt-4',
        is_active: true,
      });
      fetchProviders();
    } catch (error) {
      setError(error.response?.data?.detail || 'Failed to create LLM provider');
    }
  };

  const handleDelete = async (id) => {
    if (!window.confirm('Are you sure you want to delete this provider?')) {
      return;
    }

    try {
      await llmProviderAPI.delete(id);
      setSuccess('Provider deleted successfully');
      fetchProviders();
    } catch (error) {
      setError('Failed to delete provider');
    }
  };

  const getDefaultEndpoint = (providerType) => {
    const endpoints = {
      openai: 'https://api.openai.com/v1',
      anthropic: 'https://api.anthropic.com/v1',
      google: 'https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent',
      ollama: 'http://localhost:11434',
      custom: '',
    };
    return endpoints[providerType] || '';
  };

  const handleProviderTypeChange = (e) => {
    const type = e.target.value;
    setFormData({
      ...formData,
      provider_type: type,
      api_endpoint: getDefaultEndpoint(type),
    });
  };

  if (loading) {
    return <div className="loading">Loading LLM providers...</div>;
  }

  return (
    <div>
      <div className="card">
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <h1>LLM Providers</h1>
          <button
            className="btn btn-primary"
            onClick={() => setShowForm(!showForm)}
          >
            {showForm ? 'Cancel' : '+ Add Provider'}
          </button>
        </div>
      </div>

      {error && <div className="error">{error}</div>}
      {success && <div className="success">{success}</div>}

      {showForm && (
        <div className="card">
          <h2>Add New LLM Provider</h2>
          <form onSubmit={handleSubmit}>
            <div className="form-group">
              <label>Provider Name *</label>
              <input
                type="text"
                value={formData.name}
                onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                required
                placeholder="My OpenAI Provider"
              />
            </div>

            <div className="form-group">
              <label>Provider Type *</label>
              <select
                value={formData.provider_type}
                onChange={handleProviderTypeChange}
                required
              >
                <option value="openai">OpenAI</option>
                <option value="anthropic">Anthropic</option>
                <option value="google">Google</option>
                <option value="ollama">Ollama (Local)</option>
                <option value="custom">Custom API</option>
              </select>
            </div>

            <div className="form-group">
              <label>API Endpoint *</label>
              <input
                type="url"
                value={formData.api_endpoint}
                onChange={(e) => setFormData({ ...formData, api_endpoint: e.target.value })}
                required
                placeholder="https://api.openai.com/v1"
              />
            </div>

            <div className="form-group">
              <label>API Key {formData.provider_type !== 'ollama' && '*'}</label>
              <input
                type="password"
                value={formData.api_key}
                onChange={(e) => setFormData({ ...formData, api_key: e.target.value })}
                required={formData.provider_type !== 'ollama'}
                placeholder="sk-..."
              />
            </div>

            <div className="form-group">
              <label>Model Name *</label>
              <input
                type="text"
                value={formData.model_name}
                onChange={(e) => setFormData({ ...formData, model_name: e.target.value })}
                required
                placeholder="gpt-4"
              />
            </div>

            <div className="form-group">
              <label>
                <input
                  type="checkbox"
                  checked={formData.is_active}
                  onChange={(e) => setFormData({ ...formData, is_active: e.target.checked })}
                  style={{ width: 'auto', marginRight: '0.5rem' }}
                />
                Active
              </label>
            </div>

            <button type="submit" className="btn btn-success">
              Create Provider
            </button>
          </form>
        </div>
      )}

      <div className="grid grid-2">
        {providers.map((provider) => (
          <div key={provider.id} className="card">
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start' }}>
              <div>
                <h3>{provider.name}</h3>
                <span className={`badge ${provider.is_active ? 'badge-success' : 'badge-danger'}`}>
                  {provider.is_active ? 'Active' : 'Inactive'}
                </span>
              </div>
              <button
                className="btn btn-danger"
                onClick={() => handleDelete(provider.id)}
                style={{ padding: '0.5rem 1rem' }}
              >
                Delete
              </button>
            </div>
            <div style={{ marginTop: '1rem', color: '#718096' }}>
              <p><strong>Type:</strong> {provider.provider_type}</p>
              <p><strong>Model:</strong> {provider.model_name}</p>
              <p><strong>Endpoint:</strong> {provider.api_endpoint}</p>
              <p style={{ fontSize: '0.875rem', marginTop: '0.5rem' }}>
                Created: {new Date(provider.created_at).toLocaleDateString()}
              </p>
            </div>
          </div>
        ))}
      </div>

      {providers.length === 0 && !showForm && (
        <div className="card" style={{ textAlign: 'center', padding: '3rem' }}>
          <p style={{ color: '#718096', fontSize: '1.125rem' }}>
            No LLM providers configured yet.
          </p>
          <button
            className="btn btn-primary"
            onClick={() => setShowForm(true)}
            style={{ marginTop: '1rem' }}
          >
            Add Your First Provider
          </button>
        </div>
      )}
    </div>
  );
}

export default LLMProviders;
