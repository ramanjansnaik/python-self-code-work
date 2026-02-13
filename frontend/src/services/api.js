import axios from 'axios';

const API_BASE_URL = '/api/testgen';

const api = axios.create({
  baseURL: API_BASE_URL,
  withCredentials: true,
  headers: {
    'Content-Type': 'application/json',
  },
});

api.interceptors.request.use((config) => {
  const csrfToken = getCookie('csrftoken');
  if (csrfToken) {
    config.headers['X-CSRFToken'] = csrfToken;
  }
  return config;
});

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

export const llmProviderAPI = {
  list: () => api.get('/llm-providers/'),
  create: (data) => api.post('/llm-providers/', data),
  get: (id) => api.get(`/llm-providers/${id}/`),
  update: (id, data) => api.put(`/llm-providers/${id}/`, data),
  delete: (id) => api.delete(`/llm-providers/${id}/`),
};

export const projectAPI = {
  list: () => api.get('/projects/'),
  create: (data) => api.post('/projects/', data),
  get: (id) => api.get(`/projects/${id}/`),
  update: (id, data) => api.put(`/projects/${id}/`, data),
  delete: (id) => api.delete(`/projects/${id}/`),
  generateTests: (id, data) => api.post(`/projects/${id}/generate_tests/`, data),
  generateCICD: (id, data) => api.post(`/projects/${id}/generate_cicd/`, data),
  downloadTests: (id) => api.get(`/projects/${id}/download_tests/`),
};

export const serverConfigAPI = {
  list: (projectId) => api.get('/server-configs/', { params: { project_id: projectId } }),
  create: (data) => api.post('/server-configs/', data),
  delete: (id) => api.delete(`/server-configs/${id}/`),
};

export const generatedTestAPI = {
  list: (projectId) => api.get('/generated-tests/', { params: { project_id: projectId } }),
  get: (id) => api.get(`/generated-tests/${id}/`),
  regenerate: (id) => api.post(`/generated-tests/${id}/regenerate/`),
};

export const cicdPipelineAPI = {
  list: () => api.get('/cicd-pipelines/'),
  get: (id) => api.get(`/cicd-pipelines/${id}/`),
};

export default api;
