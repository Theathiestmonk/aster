import React, { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '@/hooks/useAuth'
import { Send, Bot, User } from 'lucide-react'
import { toast } from 'react-hot-toast'
import { chatService, ChatResponse } from '@/services/chat'
import { authService } from '@/services/auth'

interface Message {
  id: string
  text: string
  sender: 'user' | 'bot'
  timestamp: Date
}

const Dashboard: React.FC = () => {
  const { user } = useAuth()
  const navigate = useNavigate()
  
  console.log('Dashboard rendered, user:', user)
  const [messages, setMessages] = useState<Message[]>([])
  const [inputMessage, setInputMessage] = useState('')
  const [isTyping, setIsTyping] = useState(false)
  const [userProfile, setUserProfile] = useState<any>(null)
  const [isLoading, setIsLoading] = useState(true)

  const handleSendMessage = async () => {
    if (!inputMessage.trim() || isTyping) return

    const userMessage: Message = {
      id: Date.now().toString(),
      text: inputMessage,
      sender: 'user',
      timestamp: new Date(),
    }

    setMessages(prev => [...prev, userMessage])
    setInputMessage('')
    setIsTyping(true)

    try {
      const response: ChatResponse = await chatService.sendMessage(inputMessage)
      
      const botResponse: Message = {
        id: (Date.now() + 1).toString(),
        text: response.response,
        sender: 'bot',
        timestamp: new Date(),
      }
      setMessages(prev => [...prev, botResponse])
    } catch (error) {
      console.error('Chat error:', error)
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        text: 'Sorry, I encountered an error. Please try again.',
        sender: 'bot',
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

  // Fetch user profile on component mount
  useEffect(() => {
    const fetchUserProfile = async () => {
      try {
        const profile = await authService.getUserProfile()
        setUserProfile(profile)
        
        // Set initial message based on onboarding status
        if (profile?.onboarding_completed) {
          // Redirect to user dashboard if onboarding is completed
          navigate('/user-dashboard')
          return
        } else {
          setMessages([
            {
              id: '1',
              text: `Hello ${user?.full_name || 'there'}! 👋 I'm your AI Marketing Agent. I'm here to help you create amazing marketing strategies and content. Please complete your onboarding first so I can provide personalized assistance.`,
              sender: 'bot',
              timestamp: new Date(),
            },
          ])
        }
      } catch (error) {
        console.error('Error fetching user profile:', error)
        setMessages([
          {
            id: '1',
            text: `Hello ${user?.full_name || 'there'}! 👋 I'm your AI Marketing Agent. I'm here to help you create amazing marketing strategies and content.`,
            sender: 'bot',
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

  if (isLoading) {
    return (
      <div className="max-w-4xl mx-auto">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading your dashboard...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="max-w-4xl mx-auto">
      {/* Welcome Section */}
      <div className="text-center mb-8">
        <h1 className="text-3xl font-bold gradient-text mb-4">
          Welcome to Your AI Marketing Dashboard
        </h1>
        <p className="text-gray-600 text-lg mb-6">
          Your intelligent marketing companion is ready to help you grow your business
        </p>
        
        {/* Show onboarding CTA only if onboarding is not completed */}
        {!userProfile?.onboarding_completed && (
          <div className="bg-gradient-to-r from-primary to-accent p-6 rounded-xl text-white mb-8">
            <h2 className="text-xl font-semibold mb-2">🚀 Complete Your Setup!</h2>
            <p className="mb-4 opacity-90">
              Complete your onboarding to unlock personalized marketing strategies and AI-powered content creation.
            </p>
            <button
              onClick={() => navigate('/onboarding')}
              className="bg-white text-primary px-6 py-2 rounded-lg font-medium hover:bg-gray-100 transition-colors"
            >
              Complete Onboarding
            </button>
          </div>
        )}
        
        {/* Show success message if onboarding is completed */}
        {userProfile?.onboarding_completed && (
          <div className="bg-gradient-to-r from-green-500 to-green-600 p-6 rounded-xl text-white mb-8">
            <h2 className="text-xl font-semibold mb-2">✅ Onboarding Complete!</h2>
            <p className="mb-4 opacity-90">
              Your business profile is set up and I'm ready to provide personalized marketing assistance.
            </p>
            <div className="text-sm opacity-90">
              <p>Business: {userProfile.business_name}</p>
              <p>Industry: {userProfile.industry}</p>
            </div>
          </div>
        )}
      </div>

      {/* Chat Interface */}
      <div className="card">
        <div className="flex items-center space-x-3 mb-6">
          <div className="w-10 h-10 bg-gradient-to-r from-primary to-accent rounded-full flex items-center justify-center">
            <Bot className="w-5 h-5 text-white" />
          </div>
          <div>
            <h3 className="font-semibold text-gray-900">AI Marketing Agent</h3>
            <p className="text-sm text-gray-500">Ready to help you grow</p>
          </div>
        </div>

        {/* Messages */}
        <div className="space-y-4 mb-6 max-h-96 overflow-y-auto">
          {messages.map((message) => (
            <div
              key={message.id}
              className={`flex ${message.sender === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div
                className={`max-w-xs lg:max-w-md px-4 py-2 rounded-lg ${
                  message.sender === 'user'
                    ? 'bg-primary text-white'
                    : 'bg-gray-100 text-gray-900'
                }`}
              >
                <p className="text-sm">{message.text}</p>
                <p className="text-xs opacity-70 mt-1">
                  {message.timestamp.toLocaleTimeString()}
                </p>
              </div>
            </div>
          ))}
          
          {isTyping && (
            <div className="flex justify-start">
              <div className="bg-gray-100 text-gray-900 px-4 py-2 rounded-lg">
                <div className="flex space-x-1">
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Input */}
        <div className="flex space-x-2">
          <input
            type="text"
            value={inputMessage}
            onChange={(e) => setInputMessage(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Ask me about marketing strategies, content ideas, or anything else..."
            className="input-field flex-1"
            disabled={isTyping}
          />
          <button
            onClick={handleSendMessage}
            disabled={!inputMessage.trim() || isTyping}
            className="btn-primary px-4"
          >
            <Send className="w-4 h-4" />
          </button>
        </div>
      </div>
    </div>
  )
}

export default Dashboard 