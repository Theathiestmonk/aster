import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10000,
})

// Add token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

export interface ChatMessage {
  message: string
}

export interface ChatResponse {
  response: string
  user_profile?: any
}

export const chatService = {
  async sendMessage(message: string): Promise<ChatResponse> {
    const response = await api.post('/chat/send', { message })
    return response.data
  },
} 