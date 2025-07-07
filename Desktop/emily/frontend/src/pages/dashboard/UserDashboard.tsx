import React, { useState, useEffect, useRef } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '@/hooks/useAuth'
import { 
  Send, 
  Bot, 
  User, 
  LogOut, 
  Settings, 
  MessageCircle, 
  Edit, 
  Home,
  BarChart3,
  Calendar,
  FileText,
  Users,
  Target,
  TrendingUp,
  Zap
} from 'lucide-react'
import { toast } from 'react-hot-toast'
import { chatService, ChatResponse } from '@/services/chat'
import { authService } from '@/services/auth'
import LoadingSpinner from '@/components/ui/LoadingSpinner'

interface Message {
  id: string
  text: string
  isUser: boolean
  timestamp: Date
}

const UserDashboard: React.FC = () => {
  const { user, logout } = useAuth()
  const navigate = useNavigate()
  
  const [messages, setMessages] = useState<Message[]>([])
  const [inputMessage, setInputMessage] = useState('')
  const [isTyping, setIsTyping] = useState(false)
  const [userProfile, setUserProfile] = useState<any>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [activeSection, setActiveSection] = useState('home')
  const messagesEndRef = useRef<HTMLDivElement>(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  // Get first word of business name for avatar
  const getBusinessInitial = () => {
    if (!userProfile?.business_name) return 'U'
    const firstWord = userProfile.business_name.split(' ')[0]
    return firstWord.charAt(0).toUpperCase()
  }

  // Fetch user profile on component mount
  useEffect(() => {
    const fetchUserProfile = async () => {
      try {
        const profile = await authService.getUserProfile()
        setUserProfile(profile)
        
        // Set initial message
        setMessages([
          {
            id: '1',
            text: `Hello ${user?.full_name || 'there'}! 👋 I'm your AI Marketing Assistant. I have access to your business information and I'm ready to help you create amazing marketing strategies and content. What would you like to work on today?`,
            isUser: false,
            timestamp: new Date(),
          },
        ])
      } catch (error) {
        console.error('Error fetching user profile:', error)
        setMessages([
          {
            id: '1',
            text: `Hello ${user?.full_name || 'there'}! 👋 I'm your AI Marketing Assistant. I'm here to help you create amazing marketing strategies and content.`,
            isUser: false,
            timestamp: new Date(),
          },
        ])
      } finally {
        setIsLoading(false)
      }
    }

    if (user) {
      fetchUserProfile()
    } else {
      setIsLoading(false)
    }
  }, [user])

  const handleSendMessage = async () => {
    if (!inputMessage.trim() || isTyping) return

    const userMessage: Message = {
      id: Date.now().toString(),
      text: inputMessage,
      isUser: true,
      timestamp: new Date(),
    }

    setMessages(prev => [...prev, userMessage])
    setInputMessage('')
    setIsTyping(true)

    try {
      const response: ChatResponse = await chatService.sendMessage(inputMessage)
      
      const botMessage: Message = {
        id: (Date.now() + 1).toString(),
        text: response.response,
        isUser: false,
        timestamp: new Date(),
      }
      setMessages(prev => [...prev, botMessage])
    } catch (error) {
      console.error('Chat error:', error)
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        text: 'Sorry, I encountered an error. Please try again.',
        isUser: false,
        timestamp: new Date(),
      }
      setMessages(prev => [...prev, errorMessage])
      toast.error('Failed to send message. Please try again.')
    } finally {
      setIsTyping(false)
    }
  }

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSendMessage()
    }
  }

  const handleLogout = () => {
    logout()
    navigate('/auth/login')
  }

  const handleEditProfile = () => {
    navigate('/edit-profile')
  }

  const navigationItems = [
    { id: 'home', icon: Home, label: 'Home', color: 'text-blue-600' },
    { id: 'analytics', icon: BarChart3, label: 'Analytics', color: 'text-green-600' },
    { id: 'content-writer', icon: FileText, label: 'Content Writer', color: 'text-purple-600', external: true },
    { id: 'audience', icon: Users, label: 'Audience', color: 'text-orange-600' },
    { id: 'campaigns', icon: Target, label: 'Campaigns', color: 'text-red-600' },
    { id: 'performance', icon: TrendingUp, label: 'Performance', color: 'text-indigo-600' },
    { id: 'automation', icon: Zap, label: 'Automation', color: 'text-pink-600' },
    { id: 'calendar', icon: Calendar, label: 'Calendar', color: 'text-teal-600' },
  ]

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <LoadingSpinner size="lg" />
          <p className="mt-4 text-gray-600">Loading your dashboard...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50 flex w-full">
      {/* Column 1: Icon Navigation */}
      <div className="w-16 bg-white shadow-lg flex flex-col items-center py-6 space-y-6 flex-shrink-0">
        {/* User Avatar */}
        <div className="w-10 h-10 bg-gradient-to-r from-primary to-accent rounded-full flex items-center justify-center text-white text-sm font-bold">
          {getBusinessInitial()}
        </div>

        {/* Navigation Icons */}
        <div className="flex-1 flex flex-col items-center space-y-4">
          {navigationItems.map((item) => {
            const Icon = item.icon
            return (
              <button
                key={item.id}
                onClick={() => {
                  if (item.external) {
                    navigate('/content-writer-dashboard')
                  } else {
                    setActiveSection(item.id)
                  }
                }}
                className={`w-10 h-10 rounded-lg flex items-center justify-center transition-colors ${
                  activeSection === item.id 
                    ? 'bg-gray-100 text-gray-900' 
                    : 'text-gray-500 hover:text-gray-700 hover:bg-gray-50'
                }`}
                title={item.label}
              >
                <Icon className="w-5 h-5" />
              </button>
            )
          })}
        </div>

        {/* Bottom Actions */}
        <div className="flex flex-col items-center space-y-4">
          <button
            onClick={handleEditProfile}
            className="w-10 h-10 rounded-lg flex items-center justify-center text-gray-500 hover:text-gray-700 hover:bg-gray-50 transition-colors"
            title="Edit Profile"
          >
            <Edit className="w-5 h-5" />
          </button>
          <button
            onClick={handleLogout}
            className="w-10 h-10 rounded-lg flex items-center justify-center text-red-500 hover:text-red-700 hover:bg-red-50 transition-colors"
            title="Logout"
          >
            <LogOut className="w-5 h-5" />
          </button>
        </div>
      </div>

      {/* Column 2: Section Content */}
      <div className="w-72 bg-white shadow-lg flex flex-col flex-shrink-0">
        {/* Section Header */}
        <div className="p-4 border-b border-gray-200">
          <h2 className="text-lg font-semibold text-gray-900 capitalize">
            {navigationItems.find(item => item.id === activeSection)?.label || 'Home'}
          </h2>
          <p className="text-sm text-gray-500 mt-1">
            {user?.full_name} • {userProfile?.business_name}
          </p>
        </div>

        {/* Section Content */}
        <div className="flex-1 p-4">
          {activeSection === 'home' && (
            <div className="space-y-4">
              <div className="bg-gradient-to-r from-blue-50 to-indigo-50 p-3 rounded-lg">
                <h3 className="font-medium text-blue-900 text-sm">Welcome back!</h3>
                <p className="text-xs text-blue-700 mt-1">
                  Your AI marketing assistant is ready to help you grow your business.
                </p>
              </div>
              
              <div className="space-y-3">
                <h4 className="text-sm font-medium text-gray-700">Quick Stats</h4>
                <div className="grid grid-cols-1 gap-3">
                  <div className="bg-gray-50 p-3 rounded-lg">
                    <p className="text-xs text-gray-500">Industry</p>
                    <p className="text-sm font-medium">{userProfile?.industry || 'N/A'}</p>
                  </div>
                  <div className="bg-gray-50 p-3 rounded-lg">
                    <p className="text-xs text-gray-500">Business Type</p>
                    <p className="text-sm font-medium">{userProfile?.business_type || 'N/A'}</p>
                  </div>
                </div>
              </div>
            </div>
          )}

          {activeSection === 'analytics' && (
            <div className="space-y-4">
              <div className="bg-gradient-to-r from-green-50 to-emerald-50 p-3 rounded-lg">
                <h3 className="font-medium text-green-900 text-sm">Analytics Dashboard</h3>
                <p className="text-xs text-green-700 mt-1">
                  Track your marketing performance and insights.
                </p>
              </div>
              <p className="text-sm text-gray-600">Analytics features coming soon...</p>
            </div>
          )}

          {activeSection === 'content' && (
            <div className="space-y-4">
              <div className="bg-gradient-to-r from-purple-50 to-violet-50 p-3 rounded-lg">
                <h3 className="font-medium text-purple-900 text-sm">Content Management</h3>
                <p className="text-xs text-purple-700 mt-1">
                  Create and manage your marketing content.
                </p>
              </div>
              <p className="text-sm text-gray-600">Content features coming soon...</p>
            </div>
          )}

          {/* Add more sections as needed */}
          {!['home', 'analytics', 'content'].includes(activeSection) && (
            <div className="space-y-4">
              <div className="bg-gradient-to-r from-gray-50 to-slate-50 p-3 rounded-lg">
                <h3 className="font-medium text-gray-900 text-sm capitalize">{activeSection}</h3>
                <p className="text-xs text-gray-700 mt-1">
                  This feature is coming soon.
                </p>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Column 3: Business Overview */}
      <div className="w-80 bg-gray-50 p-4 flex-shrink-0">
        <div className="bg-white rounded-xl shadow-lg h-full p-4">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Business Overview</h3>
          <div className="space-y-4">
            <div className="bg-blue-50 p-3 rounded-lg">
              <h4 className="font-medium text-blue-900 text-sm">Marketing Goals</h4>
              <p className="text-xs text-blue-700 mt-1">
                {userProfile?.primary_goals?.join(', ') || 'No goals set'}
              </p>
            </div>
            <div className="bg-green-50 p-3 rounded-lg">
              <h4 className="font-medium text-green-900 text-sm">Target Audience</h4>
              <p className="text-xs text-green-700 mt-1">
                {userProfile?.target_audience?.join(', ') || 'No audience defined'}
              </p>
            </div>
            <div className="bg-gray-50 p-3 rounded-lg">
              <h4 className="font-medium text-gray-900 text-sm">Business Summary</h4>
              <p className="text-xs text-gray-700 mt-1">
                {userProfile?.business_description?.substring(0, 100) + '...' || 'No description available'}
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Column 4: Chatbot Card (flexible width) */}
      <div className="flex-1 bg-gray-50 p-4 min-w-0">
        <div className="bg-white rounded-xl shadow-lg h-full flex flex-col">
          {/* Chat Header */}
          <div className="p-4 border-b border-gray-200">
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 bg-gradient-to-r from-primary to-accent rounded-full flex items-center justify-center">
                <Bot className="w-5 h-5 text-white" />
              </div>
              <div>
                <h3 className="font-semibold text-gray-900">AI Marketing Assistant</h3>
                <p className="text-sm text-gray-500">Ready to help you grow your business</p>
              </div>
            </div>
          </div>

          {/* Messages */}
          <div className="flex-1 overflow-y-auto p-4 space-y-4">
            {messages.map((message) => (
              <div
                key={message.id}
                className={`flex ${message.isUser ? 'justify-end' : 'justify-start'}`}
              >
                <div
                  className={`max-w-md px-4 py-2 rounded-lg ${
                    message.isUser
                      ? 'bg-primary text-white'
                      : 'bg-gray-100 text-gray-900'
                  }`}
                >
                  <p className="text-sm">{message.text}</p>
                  <p className={`text-xs mt-1 ${
                    message.isUser ? 'text-primary-100' : 'text-gray-500'
                  }`}>
                    {message.timestamp.toLocaleTimeString()}
                  </p>
                </div>
              </div>
            ))}
            
            {isTyping && (
              <div className="flex justify-start">
                <div className="bg-gray-100 text-gray-900 px-4 py-2 rounded-lg">
                  <div className="flex items-center space-x-2">
                    <LoadingSpinner size="sm" />
                    <span className="text-sm">Typing...</span>
                  </div>
                </div>
              </div>
            )}
            
            <div ref={messagesEndRef} />
          </div>

          {/* Input */}
          <div className="p-4 border-t border-gray-200">
            <div className="flex space-x-2">
              <input
                type="text"
                value={inputMessage}
                onChange={(e) => setInputMessage(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="Ask me about your business, marketing strategies, or anything else..."
                className="flex-1 px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent"
                disabled={isTyping}
              />
              <button
                onClick={handleSendMessage}
                disabled={!inputMessage.trim() || isTyping}
                className="px-4 py-3 bg-primary text-white rounded-lg hover:bg-accent disabled:opacity-50 disabled:cursor-not-allowed flex items-center transition-colors"
              >
                <Send className="w-4 h-4" />
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Column 5: Quick Actions */}
      <div className="w-80 bg-gray-50 p-4 flex-shrink-0">
        <div className="bg-white rounded-xl shadow-lg h-full p-4">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Quick Actions</h3>
          <div className="space-y-3">
            <button className="w-full p-3 text-left bg-blue-50 hover:bg-blue-100 rounded-lg transition-colors">
              <h4 className="font-medium text-blue-900 text-sm">Create Content</h4>
              <p className="text-xs text-blue-700 mt-1">Generate marketing content</p>
            </button>
            <button className="w-full p-3 text-left bg-green-50 hover:bg-green-100 rounded-lg transition-colors">
              <h4 className="font-medium text-green-900 text-sm">View Analytics</h4>
              <p className="text-xs text-green-700 mt-1">Check performance metrics</p>
            </button>
            <button className="w-full p-3 text-left bg-purple-50 hover:bg-purple-100 rounded-lg transition-colors">
              <h4 className="font-medium text-purple-900 text-sm">Plan Campaign</h4>
              <p className="text-xs text-purple-700 mt-1">Design marketing campaigns</p>
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}

export default UserDashboard 