import axios from 'axios'
import { User, AuthResponse, LoginCredentials, RegisterCredentials } from '@/types'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1'

// Create axios instance with base configuration
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10000, // 10 second timeout
})

// Add token to requests if available
api.interceptors.request.use((config) => {
  console.log('API Request:', config.method?.toUpperCase(), config.url)
  console.log('API Request Headers:', config.headers)
  
  const token = localStorage.getItem('access_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Handle token expiration
api.interceptors.response.use(
  (response) => {
    console.log('API Response:', response.status, response.config.url)
    console.log('API Response Data:', response.data)
    return response
  },
  (error) => {
    console.error('API Error:', error)
    console.error('API Error Response:', error.response)
    console.error('API Error Status:', error.response?.status)
    console.error('API Error Data:', error.response?.data)
    
    if (error.response?.status === 401) {
      localStorage.removeItem('access_token')
      window.location.href = '/auth/login'
    }
    return Promise.reject(error)
  }
)

export const authService = {
  async login(email: string, password: string): Promise<AuthResponse> {
    console.log('Auth service: Making login request to', `${API_BASE_URL}/auth/login`)
    console.log('Auth service: Login data', { email, password: '***' })
    
    try {
      const response = await api.post('/auth/login', { email, password })
      console.log('Auth service: Login response', response.data)
      return response.data
    } catch (error) {
      console.error('Auth service: Login error', error)
      throw error
    }
  },

  async register(email: string, password: string, fullName?: string): Promise<{ message: string }> {
    const response = await api.post('/auth/register', { email, password, full_name: fullName })
    return response.data
  },

  async getCurrentUser(): Promise<User> {
    const response = await api.get('/auth/me')
    return response.data
  },

  async getUserProfile(): Promise<any> {
    const response = await api.get('/auth/profile')
    return response.data
  },

  async updateProfile(profileData: any): Promise<any> {
    const response = await api.post('/auth/onboarding', profileData)
    return response.data
  },

  async logout(): Promise<void> {
    await api.post('/auth/logout')
    localStorage.removeItem('access_token')
  },

  getAccessToken(): string | null {
    return localStorage.getItem('access_token')
  },
} 