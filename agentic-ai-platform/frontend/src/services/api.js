import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL;

// Create axios instance with base URL
const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add request interceptor to add auth token
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

// Add response interceptor to handle errors
api.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    // Handle 401 errors (unauthorized)
    if (error.response && error.response.status === 401) {
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Auth service
export const authService = {
  login: async (username, password) => {
    try {
      const response = await axios.post(
        `${API_URL}/auth/token`,
        new URLSearchParams({
          username,
          password,
        }),
        {
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
          },
        }
      );
      return response.data;
    } catch (error) {
      throw error;
    }
  },
  
  register: async (userData) => {
    try {
      const response = await api.post('/auth/register', userData);
      return response.data;
    } catch (error) {
      throw error;
    }
  },
  
  getCurrentUser: async () => {
    try {
      const response = await api.get('/users/me');
      return response.data;
    } catch (error) {
      throw error;
    }
  },
};

// Agents service
export const agentsService = {
  getAgents: async () => {
    try {
      const response = await api.get('/agents');
      return response.data;
    } catch (error) {
      throw error;
    }
  },
  
  getAgent: async (agentId) => {
    try {
      const response = await api.get(`/agents/${agentId}`);
      return response.data;
    } catch (error) {
      throw error;
    }
  },
  
  createAgent: async (agentData) => {
    try {
      const response = await api.post('/agents', agentData);
      return response.data;
    } catch (error) {
      throw error;
    }
  },
  
  updateAgent: async (agentId, agentData) => {
    try {
      const response = await api.put(`/agents/${agentId}`, agentData);
      return response.data;
    } catch (error) {
      throw error;
    }
  },
  
  deleteAgent: async (agentId) => {
    try {
      await api.delete(`/agents/${agentId}`);
      return true;
    } catch (error) {
      throw error;
    }
  },
  
  queryAgent: async (agentId, query, parameters = {}) => {
    try {
      const response = await api.post(`/agents/${agentId}/query`, {
        query,
        parameters,
      });
      return response.data;
    } catch (error) {
      throw error;
    }
  },
  
  uploadDocument: async (agentId, file, collectionName = null) => {
    try {
      const formData = new FormData();
      formData.append('file', file);
      
      if (collectionName) {
        formData.append('collection_name', collectionName);
      }
      
      const response = await api.post(`/agents/${agentId}/upload`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      return response.data;
    } catch (error) {
      throw error;
    }
  },
};

export default api;