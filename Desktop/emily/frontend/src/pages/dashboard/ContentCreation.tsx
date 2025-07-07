import React, { useState } from 'react'
import { useNavigate, useSearchParams } from 'react-router-dom'
import { useAuth } from '@/hooks/useAuth'
import { 
  ArrowLeft, 
  FileText, 
  Save, 
  Eye, 
  Share2,
  Calendar,
  Hash,
  Image,
  Link
} from 'lucide-react'
import { toast } from 'react-hot-toast'
import { agentService } from '@/services/agents'

interface ContentForm {
  title: string
  content: string
  description: string
  tags: string[]
  platform?: string
  scheduledDate?: string
  status: 'draft' | 'ready' | 'published'
}

const ContentCreation: React.FC = () => {
  const { user } = useAuth()
  const navigate = useNavigate()
  const [searchParams] = useSearchParams()
  const contentType = searchParams.get('type') || 'post'
  
  const [form, setForm] = useState<ContentForm>({
    title: '',
    content: '',
    description: '',
    tags: [],
    platform: contentType === 'post' ? 'linkedin' : undefined,
    scheduledDate: '',
    status: 'draft'
  })

  const [isSubmitting, setIsSubmitting] = useState(false)

  const contentTypes = {
    post: { label: 'Social Media Post', icon: Share2, platforms: ['linkedin', 'facebook', 'instagram', 'twitter'] },
    blog: { label: 'Blog Post', icon: FileText, platforms: [] },
    article: { label: 'Article', icon: FileText, platforms: [] },
    tweet: { label: 'Tweet', icon: Share2, platforms: ['twitter'] },
    email: { label: 'Email Newsletter', icon: FileText, platforms: [] }
  }

  const currentType = contentTypes[contentType as keyof typeof contentTypes] || contentTypes.post

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsSubmitting(true)

    try {
      // Create content using the agent service
      const result = await agentService.createContent({
        content_type: contentType,
        title: form.title,
        content: form.content,
        description: form.description,
        platform: form.platform,
        tags: form.tags,
        scheduled_date: form.scheduledDate,
        status: form.status
      })
      
      console.log('Content creation result:', result)
      toast.success(`${currentType.label} created successfully!`)
      navigate('/content-writer-dashboard')
    } catch (error) {
      console.error('Content creation error:', error)
      toast.error('Failed to create content. Please try again.')
    } finally {
      setIsSubmitting(false)
    }
  }

  const handleAddTag = (tag: string) => {
    if (tag && !form.tags.includes(tag)) {
      setForm(prev => ({ ...prev, tags: [...prev.tags, tag] }))
    }
  }

  const handleRemoveTag = (tagToRemove: string) => {
    setForm(prev => ({ ...prev, tags: prev.tags.filter(tag => tag !== tagToRemove) }))
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white shadow-sm border-b">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between py-6">
            <div className="flex items-center space-x-4">
              <button
                onClick={() => navigate('/content-writer-dashboard')}
                className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
              >
                <ArrowLeft className="w-5 h-5 text-gray-600" />
              </button>
              <div className="flex items-center space-x-3">
                <div className="w-10 h-10 bg-gradient-to-r from-blue-500 to-purple-600 rounded-full flex items-center justify-center">
                  <currentType.icon className="w-5 h-5 text-white" />
                </div>
                <div>
                  <h1 className="text-2xl font-bold text-gray-900">Create {currentType.label}</h1>
                  <p className="text-gray-600">Craft compelling content for your audience</p>
                </div>
              </div>
            </div>
            <div className="flex items-center space-x-3">
              <button className="btn-secondary">
                <Eye className="w-4 h-4 mr-2" />
                Preview
              </button>
              <button 
                type="submit" 
                form="content-form"
                disabled={isSubmitting}
                className="btn-primary"
              >
                {isSubmitting ? (
                  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                ) : (
                  <Save className="w-4 h-4 mr-2" />
                )}
                {isSubmitting ? 'Creating...' : 'Create Content'}
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <form id="content-form" onSubmit={handleSubmit} className="space-y-6">
          {/* Content Type Selection */}
          <div className="card">
            <h2 className="text-lg font-semibold text-gray-900 mb-4">Content Type</h2>
            <div className="grid grid-cols-2 md:grid-cols-5 gap-3">
              {Object.entries(contentTypes).map(([key, type]) => (
                <button
                  key={key}
                  type="button"
                  onClick={() => navigate(`/content/create?type=${key}`)}
                  className={`p-3 rounded-lg border-2 transition-all ${
                    contentType === key
                      ? 'border-primary bg-primary/5 text-primary'
                      : 'border-gray-200 hover:border-gray-300 text-gray-600'
                  }`}
                >
                  <type.icon className="w-5 h-5 mx-auto mb-2" />
                  <span className="text-xs font-medium">{type.label}</span>
                </button>
              ))}
            </div>
          </div>

          {/* Platform Selection (for social media posts) */}
          {currentType.platforms.length > 0 && (
            <div className="card">
              <h2 className="text-lg font-semibold text-gray-900 mb-4">Platform</h2>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                {currentType.platforms.map((platform) => (
                  <button
                    key={platform}
                    type="button"
                    onClick={() => setForm(prev => ({ ...prev, platform }))}
                    className={`p-3 rounded-lg border-2 transition-all ${
                      form.platform === platform
                        ? 'border-primary bg-primary/5 text-primary'
                        : 'border-gray-200 hover:border-gray-300 text-gray-600'
                    }`}
                  >
                    <span className="text-lg mb-1 block">
                      {platform === 'linkedin' && '💼'}
                      {platform === 'facebook' && '📘'}
                      {platform === 'instagram' && '📷'}
                      {platform === 'twitter' && '🐦'}
                    </span>
                    <span className="text-xs font-medium capitalize">{platform}</span>
                  </button>
                ))}
              </div>
            </div>
          )}

          {/* Title */}
          <div className="card">
            <label htmlFor="title" className="block text-sm font-medium text-gray-700 mb-2">
              Title
            </label>
            <input
              type="text"
              id="title"
              value={form.title}
              onChange={(e) => setForm(prev => ({ ...prev, title: e.target.value }))}
              className="input-field"
              placeholder="Enter a compelling title..."
              required
            />
          </div>

          {/* Description */}
          <div className="card">
            <label htmlFor="description" className="block text-sm font-medium text-gray-700 mb-2">
              Description
            </label>
            <textarea
              id="description"
              value={form.description}
              onChange={(e) => setForm(prev => ({ ...prev, description: e.target.value }))}
              className="input-field"
              rows={3}
              placeholder="Brief description of your content..."
            />
          </div>

          {/* Content */}
          <div className="card">
            <label htmlFor="content" className="block text-sm font-medium text-gray-700 mb-2">
              Content
            </label>
            <textarea
              id="content"
              value={form.content}
              onChange={(e) => setForm(prev => ({ ...prev, content: e.target.value }))}
              className="input-field"
              rows={8}
              placeholder="Write your content here..."
              required
            />
            <div className="mt-2 flex items-center justify-between text-xs text-gray-500">
              <span>{form.content.length} characters</span>
              {contentType === 'tweet' && (
                <span className={form.content.length > 280 ? 'text-red-500' : ''}>
                  {280 - form.content.length} remaining
                </span>
              )}
            </div>
          </div>

          {/* Tags */}
          <div className="card">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Tags
            </label>
            <div className="space-y-3">
              <div className="flex flex-wrap gap-2">
                {form.tags.map((tag) => (
                  <span
                    key={tag}
                    className="inline-flex items-center px-3 py-1 rounded-full text-sm bg-primary/10 text-primary"
                  >
                    <Hash className="w-3 h-3 mr-1" />
                    {tag}
                    <button
                      type="button"
                      onClick={() => handleRemoveTag(tag)}
                      className="ml-2 hover:text-primary-dark"
                    >
                      ×
                    </button>
                  </span>
                ))}
              </div>
              <input
                type="text"
                placeholder="Add a tag and press Enter..."
                className="input-field"
                onKeyPress={(e) => {
                  if (e.key === 'Enter') {
                    e.preventDefault()
                    handleAddTag((e.target as HTMLInputElement).value)
                    ;(e.target as HTMLInputElement).value = ''
                  }
                }}
              />
            </div>
          </div>

          {/* Scheduling */}
          <div className="card">
            <h2 className="text-lg font-semibold text-gray-900 mb-4">Publishing</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label htmlFor="scheduledDate" className="block text-sm font-medium text-gray-700 mb-2">
                  Schedule Date (Optional)
                </label>
                <input
                  type="datetime-local"
                  id="scheduledDate"
                  value={form.scheduledDate}
                  onChange={(e) => setForm(prev => ({ ...prev, scheduledDate: e.target.value }))}
                  className="input-field"
                />
              </div>
              <div>
                <label htmlFor="status" className="block text-sm font-medium text-gray-700 mb-2">
                  Status
                </label>
                <select
                  id="status"
                  value={form.status}
                  onChange={(e) => setForm(prev => ({ ...prev, status: e.target.value as any }))}
                  className="input-field"
                >
                  <option value="draft">Draft</option>
                  <option value="ready">Ready for Review</option>
                  <option value="published">Published</option>
                </select>
              </div>
            </div>
          </div>
        </form>
      </div>
    </div>
  )
}

export default ContentCreation 