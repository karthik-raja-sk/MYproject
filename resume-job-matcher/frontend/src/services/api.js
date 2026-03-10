import axios from 'axios';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000',
});

// Add a request interceptor to include the JWT token in all requests
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

export const authService = {
  login: async (email, password) => {
    const response = await api.post('/api/auth/login', { email, password });
    if (response.data.access_token) {
      localStorage.setItem('token', response.data.access_token);
    }
    return response.data;
  },
  register: async (userData) => {
    const response = await api.post('/api/auth/register', userData);
    return response.data;
  },
  logout: () => {
    localStorage.removeItem('token');
  },
  getCurrentUser: async () => {
    // Current user can be fetched from a /me endpoint if we add it, 
    // for now we'll just check if token exists and assume valid if not expired
    return localStorage.getItem('token') ? { email: 'user@example.com' } : null;
  }
};

export const resumeService = {
  upload: async (file) => {
    const formData = new FormData();
    formData.append('file', file);
    const response = await api.post('/api/resumes/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
    return response.data;
  },
  list: async () => {
    const response = await api.get('/api/resumes/list');
    return response.data;
  },
};

export const jobService = {
  create: async (jobData) => {
    const response = await api.post('/api/jobs/create', jobData);
    return response.data;
  },
  list: async () => {
    const response = await api.get('/api/jobs/list');
    return response.data;
  },
  delete: async (id) => {
    const response = await api.delete(`/api/jobs/${id}`);
    return response.data;
  },
};

export const matchService = {
  run: async (resumeId) => {
    const response = await api.post(`/api/matches/run/${resumeId}`);
    return response.data;
  },
  getHistory: async () => {
    const response = await api.get('/api/matches/history');
    return response.data;
  },
  getStats: async () => {
    const response = await api.get('/api/matches/stats');
    return response.data;
  },
};

export default api;
