/**
 * API Service Layer
 * Handles all HTTP requests to the backend API
 */
import axios from 'axios';

// Create axios instance with default config
const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:5000/api',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth token
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

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Token expired or invalid
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// ======================
// AUTH API
// ======================

export const authAPI = {
  register: (data) => api.post('/auth/register', data),
  login: (data) => api.post('/auth/login', data),
  getProfile: () => api.get('/auth/profile'),
  updateProfile: (data) => api.put('/auth/profile', data),
  changePassword: (data) => api.post('/auth/change-password', data),
};

// ======================
// SERVICES API
// ======================

export const servicesAPI = {
  getAll: (activeOnly = true, lang = 'en') => api.get('/services', { params: { active: activeOnly, lang } }),
  getById: (id, lang = 'en') => api.get(`/services/${id}`, { params: { lang } }),
  create: (data) => api.post('/services', data),
  update: (id, data) => api.put(`/services/${id}`, data),
  delete: (id) => api.delete(`/services/${id}`),
};

// ======================
// APPOINTMENTS API
// ======================

export const appointmentsAPI = {
  getMyAppointments: (params = {}, lang = 'en') => api.get('/appointments', { params: { ...params, lang } }),
  getAllAppointments: (params = {}, lang = 'en') => api.get('/appointments/admin', { params: { ...params, lang } }),
  getById: (id, lang = 'en') => api.get(`/appointments/${id}`, { params: { lang } }),
  getAvailableSlots: (serviceId, date) =>
    api.get('/appointments/available-slots', {
      params: { service_id: serviceId, date }
    }),
  create: (data) => api.post('/appointments', data),
  update: (id, data) => api.put(`/appointments/${id}`, data),
  delete: (id) => api.delete(`/appointments/${id}`),
  getStats: () => api.get('/appointments/stats'),
};

// ======================
// AVAILABILITY API
// ======================

export const availabilityAPI = {
  getAll: (activeOnly = true) => api.get('/availability', { params: { active: activeOnly } }),
  getById: (id) => api.get(`/availability/${id}`),
  create: (data) => api.post('/availability', data),
  update: (id, data) => api.put(`/availability/${id}`, data),
  delete: (id) => api.delete(`/availability/${id}`),
};

// ======================
// BLOCKED DATES API
// ======================

export const blockedDatesAPI = {
  getAll: (upcomingOnly = false) => api.get('/blocked-dates', { params: { upcoming: upcomingOnly } }),
  getById: (id) => api.get(`/blocked-dates/${id}`),
  create: (data) => api.post('/blocked-dates', data),
  update: (id, data) => api.put(`/blocked-dates/${id}`, data),
  delete: (id) => api.delete(`/blocked-dates/${id}`),
};

// ======================
// AI API
// ======================

export const aiAPI = {
  chatbot: (message, conversationHistory = []) =>
    api.post('/ai/chatbot', {
      message,
      conversation_history: conversationHistory
    }),
  generateReminder: (appointmentId) =>
    api.post('/ai/generate-reminder', { appointment_id: appointmentId }),
  getServiceSuggestions: (customerNeeds) =>
    api.post('/ai/service-suggestions', { customer_needs: customerNeeds }),
};

export default api;
