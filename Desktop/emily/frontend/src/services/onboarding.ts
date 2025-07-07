import axios from 'axios'
import { OnboardingData } from '@/types'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Add token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

export const onboardingService = {
  async submitOnboarding(data: OnboardingData): Promise<{ message: string; profile: any }> {
    const response = await api.post('/auth/onboarding', data)
    return response.data
  },

  async getOnboardingProgress(): Promise<any> {
    const response = await api.get('/auth/profile')
    return response.data
  },
} 