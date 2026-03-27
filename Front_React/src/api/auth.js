import axios from 'axios';

const API_URL = import.meta.env.VITE_PROD_API_URL;

const $api = axios.create({
  baseURL: API_URL,
  withCredentials: true,
});

// 🔒 Добавление access_token в каждый запрос
$api.interceptors.request.use(config => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
}, error => Promise.reject(error));




let isRefreshing = false;
let failedQueue = [];

const processQueue = (error, token = null) => {
  failedQueue.forEach(prom => error ? prom.reject(error) : prom.resolve(token));
  failedQueue = [];
};




$api.interceptors.response.use(
  response => response,
  async error => {
    const originalRequest = error.config;

      if (!error.response) {
      console.warn("Network error (сервер недоступен):", error.message);
      return Promise.reject(error); // просто прокидываем дальше
    }
    
    // Пропускаем ошибки не 401 или запросы на обновление токена
    if (error.response?.status !== 401 || originalRequest.url.includes('refreshAccessToken')) {
      return Promise.reject(error);
    }

    if (isRefreshing) {
      return new Promise((resolve, reject) => {
        failedQueue.push({ resolve, reject });
      }).then(token => {
        originalRequest.headers.Authorization = `Bearer ${token}`;
        return $api(originalRequest);
      }).catch(err => Promise.reject(err));
    }

    isRefreshing = true;
    originalRequest._retry = true;

    try {
      const refreshToken = localStorage.getItem('access_token');
      if (!refreshToken) throw new Error('No refresh token');
      
      const res = await axios.post(`${API_URL}/refreshAccessToken/`, null, {
        withCredentials: true,
        headers: { Authorization: `Bearer ${refreshToken}` }
      });

      const newToken = res.data.access_token;
      localStorage.setItem('access_token', newToken);
      $api.defaults.headers.common['Authorization'] = `Bearer ${newToken}`;
      
      processQueue(null, newToken);
      return $api(originalRequest);
    } catch (refreshError) {
      processQueue(refreshError, null);
      localStorage.removeItem('access_token');
      window.location.href = '/login';
      return Promise.reject(refreshError);
    } finally {
      isRefreshing = false;
    }
  }
);

export default $api;