import React, { createContext, useState, useEffect } from 'react';
import apiClient from '../api';

export const AuthContext = createContext();

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(localStorage.getItem('token') || '');

  useEffect(() => {
    const fetchUser = async () => {
      if (token) {
        try {
          const { data } = await apiClient.get('/auth/me');
          setUser(data);
        } catch (error) {
          console.error('Failed to fetch user data:', error);
          setUser(null);
          // Clear invalid token
          localStorage.removeItem('token');
          setToken('');
        }
      } else {
        setUser(null);
      }
    };

    fetchUser();
  }, [token]);

  const login = async (username, password) => {
    try {
      // Use URLSearchParams for x-www-form-urlencoded format
      const params = new URLSearchParams();
      params.append('grant_type', 'password');
      params.append('username', username);
      params.append('password', password);
      params.append('scope', '');
      
      // Request token from the backend
      const response = await apiClient.post('/auth/token', params, {
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      });
      const { access_token } = response.data;
      
      if (!access_token) {
        throw new Error('No access token received');
      }
      
      // Store the token
      localStorage.setItem('token', access_token);
      
      // Set the token for subsequent requests
      setToken(access_token);
      
      // Fetch user data
      const { data: userData } = await apiClient.get('/auth/me');
      setUser(userData);
      
      return userData;
    } catch (error) {
      console.error('Login failed:', error);
      // Clear any invalid token
      localStorage.removeItem('token');
      setToken('');
      setUser(null);
      throw error;
    }
  };

  const logout = () => {
    setToken('');
    setUser(null);
    localStorage.removeItem('token');
  };

  return (
    <AuthContext.Provider value={{ user, token, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}
