import React, { useState, useEffect, createContext, useContext } from 'react'
import { User } from '@/types'
import { authService } from '@/services/auth'

interface AuthContextType {
  user: User | null
  loading: boolean
  login: (email: string, password: string) => Promise<void>
  register: (email: string, password: string, fullName?: string) => Promise<void>
  logout: () => void
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    // Check for existing token on app load
    const token = localStorage.getItem('access_token')
    console.log('Checking for existing token:', token ? 'found' : 'not found')
    if (token) {
      authService.getCurrentUser()
        .then(user => {
          console.log('getCurrentUser response:', user)
          if (user) {
            setUser(user)
          }
        })
        .catch((error) => {
          console.error('getCurrentUser error:', error)
          localStorage.removeItem('access_token')
        })
        .finally(() => {
          setLoading(false)
        })
    } else {
      setLoading(false)
    }
  }, [])

  const login = async (email: string, password: string) => {
    try {
      console.log('Login attempt for:', email)
      const response = await authService.login(email, password)
      console.log('Login response:', response)
      localStorage.setItem('access_token', response.access_token)
      setUser(response.user)
      console.log('User set in state:', response.user)
    } catch (error) {
      console.error('Login error:', error)
      throw error
    }
  }

  const register = async (email: string, password: string, fullName?: string) => {
    try {
      await authService.register(email, password, fullName)
    } catch (error) {
      throw error
    }
  }

  const logout = () => {
    localStorage.removeItem('access_token')
    setUser(null)
  }

  return (
    <AuthContext.Provider value={{ user, loading, login, register, logout }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
} 