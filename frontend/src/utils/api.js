export const setToken = (token) => localStorage.setItem('jwt_token', token);
export const getToken = () => localStorage.getItem('jwt_token');
export const removeToken = () => localStorage.removeItem('jwt_token');

const API_BASE_URL = 'http://localhost:8000';

export const apiFetch = async (endpoint, options = {}) => {
  const token = getToken();
  const headers = {
    'Content-Type': 'application/json',
    ...options.headers,
  };

  
  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }

 
  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    ...options,
    headers,
  });

 
  if (response.status === 401) {
    removeToken(); 
    window.location.href = '/login'; 
  }

  return response;
};
