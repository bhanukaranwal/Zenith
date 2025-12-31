import axios from 'axios'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

export const api = axios.create({
  baseURL: `${API_URL}/api/v1`,
  headers: {
    'Content-Type': 'application/json',
  },
})

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('access_token')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export const authApi = {
  login: (username: string, password: string) =>
    api.post('/auth/login', new URLSearchParams({ username, password }), {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    }),
  register: (data: any) => api.post('/auth/register', data),
  me: () => api.get('/auth/me'),
}

export const projectsApi = {
  list: () => api.get('/projects'),
  create: (data: any) => api.post('/projects', data),
  get: (id: number) => api.get(`/projects/${id}`),
  update: (id: number, data: any) => api.put(`/projects/${id}`, data),
  delete: (id: number) => api.delete(`/projects/${id}`),
}

export const experimentsApi = {
  list: (projectId: number) => api.get('/experiments', { params: { project_id: projectId } }),
  create: (data: any) => api.post('/experiments', data),
  createRun: (data: any) => api.post('/experiments/runs', data),
  getRun: (id: number) => api.get(`/experiments/runs/${id}`),
  logMetrics: (runId: number, metrics: any[]) => api.post(`/experiments/runs/${runId}/metrics`, metrics),
  logParameters: (runId: number, parameters: any[]) => api.post(`/experiments/runs/${runId}/parameters`, parameters),
  getMetrics: (runId: number) => api.get(`/experiments/runs/${runId}/metrics`),
}

export const modelsApi = {
  list: (projectId: number) => api.get('/models', { params: { project_id: projectId } }),
  create: (data: any) => api.post('/models', data),
  createVersion: (data: any) => api.post('/models/versions', data),
  listVersions: (modelId: number) => api.get(`/models/${modelId}/versions`),
  promoteVersion: (versionId: number, stage: string) => api.post(`/models/versions/${versionId}/promote`, { stage }),
}

export const deploymentsApi = {
  list: () => api.get('/deployments'),
  create: (data: any) => api.post('/deployments', data),
  get: (id: number) => api.get(`/deployments/${id}`),
  predict: (id: number, inputs: any) => api.post(`/deployments/${id}/predict`, inputs),
  delete: (id: number) => api.delete(`/deployments/${id}`),
}

export const monitoringApi = {
  getMetrics: (deploymentId: number, startTime?: string, endTime?: string) =>
    api.get(`/monitoring/deployments/${deploymentId}/metrics`, { params: { start_time: startTime, end_time: endTime } }),
  checkDrift: (deploymentId: number, referenceData: any, currentData: any) =>
    api.post(`/monitoring/deployments/${deploymentId}/drift`, { reference_data: referenceData, current_data: currentData }),
  getTraces: (deploymentId: number, limit?: number) =>
    api.get(`/monitoring/deployments/${deploymentId}/traces`, { params: { limit } }),
}

export const agentsApi = {
  list: (projectId: number) => api.get('/agents', { params: { project_id: projectId } }),
  create: (data: any) => api.post('/agents', data),
  execute: (agentId: number, inputData: any) => api.post(`/agents/${agentId}/execute`, inputData),
  listExecutions: (agentId: number) => api.get(`/agents/${agentId}/executions`),
}

export const promptsApi = {
  list: (projectId: number) => api.get('/prompts', { params: { project_id: projectId } }),
  create: (data: any) => api.post('/prompts', data),
  createVersion: (templateId: number, data: any) => api.post(`/prompts/${templateId}/versions`, data),
  listVersions: (templateId: number) => api.get(`/prompts/${templateId}/versions`),
  test: (templateId: number, version: string, variables: any) =>
    api.post(`/prompts/${templateId}/test`, { version, variables }),
}
