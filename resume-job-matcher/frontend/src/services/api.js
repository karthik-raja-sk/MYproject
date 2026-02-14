/**
 * API client for backend communication.
 * Centralized error handling and request configuration.
 */
import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30000, // 30 seconds
});

// Request interceptor for logging
api.interceptors.request.use(
  (config) => {
    console.log(`[API Request] ${config.method.toUpperCase()} ${config.url}`);
    return config;
  },
  (error) => {
    console.error('[API Request Error]', error);
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => {
    console.log(`[API Response] ${response.config.url} - Status: ${response.status}`);
    return response;
  },
  (error) => {
    console.error('[API Error]', error.response?.data || error.message);
    return Promise.reject(error);
  }
);

/**
 * Upload resume PDF file
 */
export const uploadResume = async (file) => {
  const formData = new FormData();
  formData.append('file', file);

  const response = await api.post('/resumes/upload', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });

  return response.data;
};

/**
 * Create a new job posting
 */
export const createJob = async (jobData) => {
  const response = await api.post('/jobs', jobData);
  return response.data;
};

/**
 * Get all jobs
 */
export const getJobs = async () => {
  const response = await api.get('/jobs');
  return response.data;
};

/**
 * Generate matches for a resume
 */
export const generateMatches = async (resumeId) => {
  const response = await api.post(`/matches/${resumeId}`);
  return response.data;
};

/**
 * Get existing matches for a resume
 */
export const getMatches = async (resumeId) => {
  const response = await api.get(`/resumes/${resumeId}/matches`);
  return response.data;
};

export default api;
