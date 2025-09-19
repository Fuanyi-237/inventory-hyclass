import axios from 'axios';

const apiClient = axios.create({
  baseURL: '/api/v1',
});

// Request interceptor for API calls
apiClient.interceptors.request.use(
  async (config) => {
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

// Response interceptor
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      const url = error.config?.url || '';
      // Only force redirect for authentication endpoints or when already on login
      const shouldForceRedirect = url.includes('/auth') || window.location.pathname === '/login';
      if (shouldForceRedirect) {
        localStorage.removeItem('token');
        window.location.href = '/login';
      }
      // Otherwise, allow the caller to handle (e.g., show a message) without immediate logout
    }
    return Promise.reject(error);
  }
);

export default apiClient;
