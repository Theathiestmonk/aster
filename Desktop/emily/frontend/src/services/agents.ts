import { authService } from './auth'

const API_BASE_URL = (import.meta as any).env?.VITE_API_URL || 'http://localhost:8000'

export interface Task {
  id: string
  title: string
  description: string
  status: 'pending' | 'working' | 'completed'
  priority: 'low' | 'medium' | 'high'
  dueDate: string
  assignedBy: string
  createdAt: string
}

export interface SocialMediaPost {
  id: string
  title: string
  content: string
  platform: 'facebook' | 'instagram' | 'linkedin' | 'twitter'
  status: 'draft' | 'published' | 'scheduled'
  createdAt: string
  engagement?: {
    likes: number
    shares: number
    comments: number
  }
}

export interface Blog {
  id: string
  title: string
  excerpt: string
  content: string
  status: 'draft' | 'published' | 'review'
  createdAt: string
  readTime: number
  tags: string[]
}

export interface ContentRequest {
  id: string
  type: 'post' | 'blog' | 'article' | 'tweet' | 'email'
  title: string
  description: string
  priority: 'low' | 'medium' | 'high'
  status: 'pending' | 'approved' | 'rejected'
  requestedBy: string
  requestedAt: string
}

export interface ContentCreationRequest {
  content_type: string
  title: string
  content: string
  description?: string
  platform?: string
  tags?: string[]
  scheduled_date?: string
  status?: string
}

export interface WorkflowRequest {
  task_type: string
  task_data?: any
}

export interface WorkflowResponse {
  workflow_status: string
  user_id: string
  task_type: string
  agent_outputs: any
  strategy?: any
  error_message?: string
  timestamp: string
}

class AgentService {
  private async getAuthHeaders() {
    const token = await authService.getAccessToken()
    return {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json',
    }
  }

  async createContent(request: ContentCreationRequest): Promise<any> {
    try {
      const headers = await this.getAuthHeaders()
      const response = await fetch(`${API_BASE_URL}/content/history`, {
        method: 'POST',
        headers,
        body: JSON.stringify({
          content_type: request.content_type,
          title: request.title,
          content: request.content,
          description: request.description,
          platform: request.platform,
          tags: request.tags,
          agent_used: "content_writer"
        })
      })

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      return await response.json()
    } catch (error) {
      console.error('Error creating content:', error)
      throw error
    }
  }

  async getTasks(): Promise<Task[]> {
    try {
      const headers = await this.getAuthHeaders()
      const response = await fetch(`${API_BASE_URL}/content/tasks`, {
        method: 'GET',
        headers
      })

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      const data = await response.json()
      return data.tasks || []
    } catch (error) {
      console.error('Error fetching tasks:', error)
      return this.getMockTasks()
    }
  }

  async getSocialMediaPosts(): Promise<SocialMediaPost[]> {
    try {
      const headers = await this.getAuthHeaders()
      const response = await fetch(`${API_BASE_URL}/content/posts`, {
        method: 'GET',
        headers
      })

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      const data = await response.json()
      return data.posts || []
    } catch (error) {
      console.error('Error fetching posts:', error)
      return this.getMockSocialMediaPosts()
    }
  }

  async getBlogs(): Promise<Blog[]> {
    try {
      const headers = await this.getAuthHeaders()
      const response = await fetch(`${API_BASE_URL}/content/blogs`, {
        method: 'GET',
        headers
      })

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      const data = await response.json()
      return data.blogs || []
    } catch (error) {
      console.error('Error fetching blogs:', error)
      return this.getMockBlogs()
    }
  }

  async getContentRequests(): Promise<ContentRequest[]> {
    try {
      const headers = await this.getAuthHeaders()
      const response = await fetch(`${API_BASE_URL}/content/requests`, {
        method: 'GET',
        headers
      })

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      const data = await response.json()
      return data.requests || []
    } catch (error) {
      console.error('Error fetching requests:', error)
      return this.getMockContentRequests()
    }
  }

  async executeWorkflow(request: WorkflowRequest): Promise<WorkflowResponse> {
    try {
      const headers = await this.getAuthHeaders()
      const response = await fetch(`${API_BASE_URL}/agents/workflow/execute`, {
        method: 'POST',
        headers,
        body: JSON.stringify(request)
      })

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      return await response.json()
    } catch (error) {
      console.error('Error executing workflow:', error)
      throw error
    }
  }

  async executeSpecificTask(taskType: string, taskData: any): Promise<WorkflowResponse> {
    try {
      const headers = await this.getAuthHeaders()
      const response = await fetch(`${API_BASE_URL}/agents/task/execute`, {
        method: 'POST',
        headers,
        body: JSON.stringify({
          task_type: taskType,
          task_data: taskData
        })
      })

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      return await response.json()
    } catch (error) {
      console.error('Error executing specific task:', error)
      throw error
    }
  }

  async getWorkflowStatus(): Promise<any> {
    try {
      const headers = await this.getAuthHeaders()
      const response = await fetch(`${API_BASE_URL}/agents/workflow/status`, {
        method: 'GET',
        headers
      })

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      return await response.json()
    } catch (error) {
      console.error('Error getting workflow status:', error)
      throw error
    }
  }

  async listAgents(): Promise<any> {
    try {
      const headers = await this.getAuthHeaders()
      const response = await fetch(`${API_BASE_URL}/agents/agents/list`, {
        method: 'GET',
        headers
      })

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      return await response.json()
    } catch (error) {
      console.error('Error listing agents:', error)
      throw error
    }
  }

  // Mock data methods for development (fallback when backend is not available)
  getMockTasks(): Task[] {
    return [
      {
        id: '1',
        title: 'Create LinkedIn post about AI trends',
        description: 'Write an engaging post about the latest AI trends in marketing',
        status: 'completed',
        priority: 'high',
        dueDate: '2024-01-15',
        assignedBy: 'Ravi',
        createdAt: '2024-01-10'
      },
      {
        id: '2',
        title: 'Draft blog post on content strategy',
        description: 'Create a comprehensive blog post about content marketing strategies',
        status: 'working',
        priority: 'medium',
        dueDate: '2024-01-20',
        assignedBy: 'Deep',
        createdAt: '2024-01-12'
      },
      {
        id: '3',
        title: 'Write Instagram captions for product launch',
        description: 'Create engaging captions for the new product launch campaign',
        status: 'pending',
        priority: 'high',
        dueDate: '2024-01-18',
        assignedBy: 'Ravi',
        createdAt: '2024-01-14'
      }
    ]
  }

  getMockSocialMediaPosts(): SocialMediaPost[] {
    return [
      {
        id: '1',
        title: 'AI in Marketing: The Future is Now',
        content: 'Discover how artificial intelligence is revolutionizing the marketing landscape...',
        platform: 'linkedin',
        status: 'published',
        createdAt: '2024-01-15',
        engagement: { likes: 45, shares: 12, comments: 8 }
      },
      {
        id: '2',
        title: '5 Content Marketing Tips That Actually Work',
        content: 'Stop wasting time on strategies that don\'t work. Here are 5 proven tips...',
        platform: 'facebook',
        status: 'published',
        createdAt: '2024-01-14',
        engagement: { likes: 23, shares: 5, comments: 3 }
      },
      {
        id: '3',
        title: 'Behind the Scenes: Our Creative Process',
        content: 'Ever wondered how we create compelling content? Here\'s a peek...',
        platform: 'instagram',
        status: 'scheduled',
        createdAt: '2024-01-13'
      }
    ]
  }

  getMockBlogs(): Blog[] {
    return [
      {
        id: '1',
        title: 'The Complete Guide to Content Marketing in 2024',
        excerpt: 'Learn the latest strategies and trends in content marketing...',
        content: 'Content marketing has evolved significantly over the past few years...',
        status: 'published',
        createdAt: '2024-01-10',
        readTime: 8,
        tags: ['content marketing', 'strategy', '2024']
      },
      {
        id: '2',
        title: 'How to Write Engaging Social Media Posts',
        excerpt: 'Master the art of creating posts that drive engagement...',
        content: 'Creating engaging social media content requires more than just...',
        status: 'draft',
        createdAt: '2024-01-12',
        readTime: 5,
        tags: ['social media', 'engagement', 'writing']
      }
    ]
  }

  getMockContentRequests(): ContentRequest[] {
    return [
      {
        id: '1',
        type: 'blog',
        title: 'SEO Best Practices for 2024',
        description: 'Need a comprehensive blog post about SEO best practices',
        priority: 'high',
        status: 'pending',
        requestedBy: 'Deep',
        requestedAt: '2024-01-15'
      },
      {
        id: '2',
        type: 'post',
        title: 'Product Launch Announcement',
        description: 'Create a series of social media posts for product launch',
        priority: 'high',
        status: 'approved',
        requestedBy: 'Ravi',
        requestedAt: '2024-01-14'
      },
      {
        id: '3',
        type: 'tweet',
        title: 'Industry Insights Thread',
        description: 'Create a Twitter thread about industry insights',
        priority: 'medium',
        status: 'pending',
        requestedBy: 'Deep',
        requestedAt: '2024-01-13'
      }
    ]
  }
}

export const agentService = new AgentService() 