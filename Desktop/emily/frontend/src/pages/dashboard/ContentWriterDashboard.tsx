import React, { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '@/hooks/useAuth'
import { 
  FileText, 
  Calendar, 
  CheckCircle, 
  Clock, 
  AlertCircle,
  Plus,
  Edit,
  Trash2,
  Eye,
  Share2,
  Download,
  Filter,
  Search,
  RefreshCw,
  Home,
  BarChart3,
  Users,
  Target,
  TrendingUp,
  Zap,
  LogOut,
  Bot
} from 'lucide-react'
import { toast } from 'react-hot-toast'
import { agentService, Task, SocialMediaPost, Blog, ContentRequest } from '@/services/agents'
import { authService } from '@/services/auth'

const ContentWriterDashboard: React.FC = () => {
  const { user } = useAuth()
  const navigate = useNavigate()
  
  // State for different panels
  const [tasks, setTasks] = useState<Task[]>([])
  const [socialMediaPosts, setSocialMediaPosts] = useState<SocialMediaPost[]>([])
  const [blogs, setBlogs] = useState<Blog[]>([])
  const [contentRequests, setContentRequests] = useState<ContentRequest[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [activeTab, setActiveTab] = useState('tasks')
  const [userProfile, setUserProfile] = useState<any>(null)

  // Get first word of business name for avatar
  const getBusinessInitial = () => {
    if (!userProfile?.business_name) return 'U'
    const firstWord = userProfile.business_name.split(' ')[0]
    return firstWord.charAt(0).toUpperCase()
  }

  const handleLogout = () => {
    // Handle logout logic
    navigate('/auth/login')
  }

  const handleEditProfile = () => {
    navigate('/edit-profile')
  }

  const navigationItems = [
    { id: 'home', icon: Home, label: 'Home', color: 'text-blue-600' },
    { id: 'analytics', icon: BarChart3, label: 'Analytics', color: 'text-green-600' },
    { id: 'content-writer', icon: FileText, label: 'Content Writer', color: 'text-purple-600', active: true },
    { id: 'audience', icon: Users, label: 'Audience', color: 'text-orange-600' },
    { id: 'campaigns', icon: Target, label: 'Campaigns', color: 'text-red-600' },
    { id: 'performance', icon: TrendingUp, label: 'Performance', color: 'text-indigo-600' },
    { id: 'automation', icon: Zap, label: 'Automation', color: 'text-pink-600' },
    { id: 'calendar', icon: Calendar, label: 'Calendar', color: 'text-teal-600' },
  ]

  // Load data from backend or use mock data as fallback
  useEffect(() => {
    const loadData = async () => {
      try {
        // Fetch user profile
        const profile = await authService.getUserProfile()
        setUserProfile(profile)
        
        // Try to get real data from backend first
        const [tasksData, postsData, blogsData, requestsData] = await Promise.all([
          agentService.getTasks(),
          agentService.getSocialMediaPosts(),
          agentService.getBlogs(),
          agentService.getContentRequests()
        ])
        
        setTasks(tasksData)
        setSocialMediaPosts(postsData)
        setBlogs(blogsData)
        setContentRequests(requestsData)
        
      } catch (error) {
        console.error('Error loading data from backend, using mock data:', error)
        // Fallback to mock data if backend is not available
        setTasks(agentService.getMockTasks())
        setSocialMediaPosts(agentService.getMockSocialMediaPosts())
        setBlogs(agentService.getMockBlogs())
        setContentRequests(agentService.getMockContentRequests())
      } finally {
        setIsLoading(false)
      }
    }

    loadData()
  }, [])

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed':
        return 'bg-green-100 text-green-800 border-green-200'
      case 'working':
        return 'bg-blue-100 text-blue-800 border-blue-200'
      case 'pending':
        return 'bg-yellow-100 text-yellow-800 border-yellow-200'
      default:
        return 'bg-gray-100 text-gray-800 border-gray-200'
    }
  }

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'high':
        return 'bg-red-100 text-red-800'
      case 'medium':
        return 'bg-yellow-100 text-yellow-800'
      case 'low':
        return 'bg-green-100 text-green-800'
      default:
        return 'bg-gray-100 text-gray-800'
    }
  }

  const getPlatformIcon = (platform: string) => {
    switch (platform) {
      case 'linkedin':
        return '💼'
      case 'facebook':
        return '📘'
      case 'instagram':
        return '📷'
      case 'twitter':
        return '🐦'
      default:
        return '📱'
    }
  }

  const handleCreateContent = (type: string) => {
    toast.success(`Creating new ${type}...`)
    // Navigate to content creation form
    navigate(`/content/create?type=${type}`)
  }

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <RefreshCw className="w-8 h-8 animate-spin mx-auto mb-4 text-primary" />
          <p className="text-gray-600">Loading your content dashboard...</p>
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
                  if (item.id === 'content-writer') {
                    // Stay on current page
                    return
                  } else if (item.id === 'home') {
                    navigate('/user-dashboard')
                  } else {
                    // Navigate to other sections (future implementation)
                    toast(`${item.label} dashboard coming soon!`)
                  }
                }}
                className={`w-10 h-10 rounded-lg flex items-center justify-center transition-colors ${
                  item.active 
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
          <h2 className="text-lg font-semibold text-gray-900">Content Writer</h2>
          <p className="text-sm text-gray-500 mt-1">
            {user?.full_name} • {userProfile?.business_name}
          </p>
        </div>

        {/* Section Content */}
        <div className="flex-1 p-4 space-y-4">
          <div className="bg-gradient-to-r from-purple-50 to-violet-50 p-3 rounded-lg">
            <h3 className="font-medium text-purple-900 text-sm">Content Dashboard</h3>
            <p className="text-xs text-purple-700 mt-1">
              Manage your content creation tasks and track progress.
            </p>
          </div>

          {/* Target Audience Panel */}
          <div className="bg-green-50 p-3 rounded-lg">
            <h4 className="font-medium text-green-900 text-sm mb-2 flex items-center gap-2">
              <Users className="w-4 h-4 text-green-700" /> Target Audience
            </h4>
            {userProfile?.target_audience && userProfile.target_audience.length > 0 ? (
              <ul className="list-disc list-inside text-xs text-green-800 space-y-1">
                {userProfile.target_audience.map((aud: string, idx: number) => (
                  <li key={idx}>{aud}</li>
                ))}
              </ul>
            ) : (
              <p className="text-xs text-green-700">No target audience defined yet.</p>
            )}
          </div>

          <div className="space-y-3">
            <h4 className="text-sm font-medium text-gray-700">Quick Stats</h4>
            <div className="grid grid-cols-1 gap-3">
              <div className="bg-gray-50 p-3 rounded-lg">
                <p className="text-xs text-gray-500">Tasks</p>
                <p className="text-sm font-medium">{tasks.length} total</p>
              </div>
              <div className="bg-gray-50 p-3 rounded-lg">
                <p className="text-xs text-gray-500">Posts</p>
                <p className="text-sm font-medium">{socialMediaPosts.length} created</p>
              </div>
              <div className="bg-gray-50 p-3 rounded-lg">
                <p className="text-xs text-gray-500">Blogs</p>
                <p className="text-sm font-medium">{blogs.length} written</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Column 3: Business Overview */}
      <div className="w-80 bg-gray-50 p-4 flex-shrink-0">
        <div className="bg-white rounded-xl shadow-lg h-full p-4">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Content Overview</h3>
          <div className="space-y-4">
            <div className="bg-blue-50 p-3 rounded-lg">
              <h4 className="font-medium text-blue-900 text-sm">Content Goals</h4>
              <p className="text-xs text-blue-700 mt-1">
                {userProfile?.primary_goals?.join(', ') || 'No goals set'}
              </p>
            </div>
            <div className="bg-gray-50 p-3 rounded-lg">
              <h4 className="font-medium text-gray-900 text-sm">Content Themes</h4>
              <p className="text-xs text-gray-700 mt-1">
                {userProfile?.content_themes?.join(', ') || 'No themes defined'}
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Column 4: Content Panels (flexible width) */}
      <div className="flex-1 bg-gray-50 p-4 min-w-0">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 h-full">
          
          {/* Panel 1: Tasks List */}
          <div className="bg-white rounded-xl shadow-lg p-6">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-lg font-semibold text-gray-900">Tasks</h2>
              <div className="flex space-x-1">
                <span className="text-xs bg-green-100 text-green-800 px-2 py-1 rounded-full">
                  {tasks.filter(t => t.status === 'completed').length} Done
                </span>
                <span className="text-xs bg-blue-100 text-blue-800 px-2 py-1 rounded-full">
                  {tasks.filter(t => t.status === 'working').length} Working
                </span>
                <span className="text-xs bg-yellow-100 text-yellow-800 px-2 py-1 rounded-full">
                  {tasks.filter(t => t.status === 'pending').length} Pending
                </span>
              </div>
            </div>
            
            <div className="space-y-3 max-h-64 overflow-y-auto">
              {tasks.map((task) => (
                <div key={task.id} className="border rounded-lg p-3 hover:shadow-md transition-shadow">
                  <div className="flex items-start justify-between mb-2">
                    <h3 className="font-medium text-gray-900 text-sm">{task.title}</h3>
                    <span className={`text-xs px-2 py-1 rounded-full border ${getStatusColor(task.status)}`}>
                      {task.status}
                    </span>
                  </div>
                  <p className="text-xs text-gray-600 mb-2">{task.description}</p>
                  <div className="flex items-center justify-between">
                    <span className={`text-xs px-2 py-1 rounded ${getPriorityColor(task.priority)}`}>
                      {task.priority}
                    </span>
                    <span className="text-xs text-gray-500">Due: {task.dueDate}</span>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Panel 2: Social Media Posts */}
          <div className="bg-white rounded-xl shadow-lg p-6">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-lg font-semibold text-gray-900">Social Media Posts</h2>
              <button 
                onClick={() => handleCreateContent('post')}
                className="text-primary hover:text-primary-dark text-sm font-medium"
              >
                <Plus className="w-4 h-4 inline mr-1" />
                New Post
              </button>
            </div>
            
            <div className="space-y-3 max-h-64 overflow-y-auto">
              {socialMediaPosts.map((post) => (
                <div key={post.id} className="border rounded-lg p-3 hover:shadow-md transition-shadow">
                  <div className="flex items-start justify-between mb-2">
                    <div className="flex items-center space-x-2">
                      <span className="text-lg">{getPlatformIcon(post.platform)}</span>
                      <span className="text-xs text-gray-500 uppercase">{post.platform}</span>
                    </div>
                    <span className={`text-xs px-2 py-1 rounded-full border ${getStatusColor(post.status)}`}>
                      {post.status}
                    </span>
                  </div>
                  <h3 className="font-medium text-gray-900 text-sm mb-1">{post.title}</h3>
                  <p className="text-xs text-gray-600 mb-2 line-clamp-2">{post.content}</p>
                  {post.engagement && (
                    <div className="flex items-center space-x-3 text-xs text-gray-500">
                      <span>❤️ {post.engagement.likes}</span>
                      <span>🔄 {post.engagement.shares}</span>
                      <span>💬 {post.engagement.comments}</span>
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>

          {/* Panel 3: Generated Blogs */}
          <div className="bg-white rounded-xl shadow-lg p-6">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-lg font-semibold text-gray-900">Blogs</h2>
              <button 
                onClick={() => handleCreateContent('blog')}
                className="text-primary hover:text-primary-dark text-sm font-medium"
              >
                <Plus className="w-4 h-4 inline mr-1" />
                New Blog
              </button>
            </div>
            
            <div className="space-y-3 max-h-64 overflow-y-auto">
              {blogs.map((blog) => (
                <div key={blog.id} className="border rounded-lg p-3 hover:shadow-md transition-shadow">
                  <div className="flex items-start justify-between mb-2">
                    <h3 className="font-medium text-gray-900 text-sm">{blog.title}</h3>
                    <span className={`text-xs px-2 py-1 rounded-full border ${getStatusColor(blog.status)}`}>
                      {blog.status}
                    </span>
                  </div>
                  <p className="text-xs text-gray-600 mb-2 line-clamp-2">{blog.excerpt}</p>
                  <div className="flex items-center justify-between">
                    <span className="text-xs text-gray-500">{blog.readTime} min read</span>
                    <div className="flex space-x-1">
                      {blog.tags.slice(0, 2).map((tag, index) => (
                        <span key={index} className="text-xs bg-gray-100 text-gray-600 px-2 py-1 rounded">
                          {tag}
                        </span>
                      ))}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Panel 4: Content Requests */}
          <div className="bg-white rounded-xl shadow-lg p-6">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-lg font-semibold text-gray-900">Content Requests</h2>
              <button className="text-primary hover:text-primary-dark text-sm font-medium">
                <Eye className="w-4 h-4 inline mr-1" />
                View All
              </button>
            </div>
            
            <div className="space-y-3 max-h-64 overflow-y-auto">
              {contentRequests.map((request) => (
                <div key={request.id} className="border rounded-lg p-3 hover:shadow-md transition-shadow">
                  <div className="flex items-start justify-between mb-2">
                    <div className="flex items-center space-x-2">
                      <span className="text-sm font-medium text-gray-900">{request.type}</span>
                      <span className={`text-xs px-2 py-1 rounded ${getPriorityColor(request.priority)}`}>
                        {request.priority}
                      </span>
                    </div>
                    <span className={`text-xs px-2 py-1 rounded-full border ${getStatusColor(request.status)}`}>
                      {request.status}
                    </span>
                  </div>
                  <h3 className="font-medium text-gray-900 text-sm mb-1">{request.title}</h3>
                  <p className="text-xs text-gray-600 mb-2 line-clamp-2">{request.description}</p>
                  <div className="flex items-center justify-between">
                    <span className="text-xs text-gray-500">By: {request.requestedBy}</span>
                    <div className="flex space-x-1">
                      <button className="text-xs text-primary hover:text-primary-dark">
                        <Edit className="w-3 h-3" />
                      </button>
                      <button className="text-xs text-green-600 hover:text-green-700">
                        <CheckCircle className="w-3 h-3" />
                      </button>
                    </div>
                  </div>
                </div>
              ))}
            </div>

            {/* Quick Actions */}
            <div className="mt-4 pt-4 border-t">
              <h3 className="text-sm font-medium text-gray-900 mb-3">Quick Create</h3>
              <div className="grid grid-cols-2 gap-2">
                <button 
                  onClick={() => handleCreateContent('post')}
                  className="text-xs bg-blue-50 text-blue-700 px-3 py-2 rounded hover:bg-blue-100 transition-colors"
                >
                  📝 Post
                </button>
                <button 
                  onClick={() => handleCreateContent('blog')}
                  className="text-xs bg-green-50 text-green-700 px-3 py-2 rounded hover:bg-green-100 transition-colors"
                >
                  📄 Blog
                </button>
                <button 
                  onClick={() => handleCreateContent('article')}
                  className="text-xs bg-purple-50 text-purple-700 px-3 py-2 rounded hover:bg-purple-100 transition-colors"
                >
                  📰 Article
                </button>
                <button 
                  onClick={() => handleCreateContent('tweet')}
                  className="text-xs bg-blue-50 text-blue-700 px-3 py-2 rounded hover:bg-blue-100 transition-colors"
                >
                  🐦 Tweet
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default ContentWriterDashboard 