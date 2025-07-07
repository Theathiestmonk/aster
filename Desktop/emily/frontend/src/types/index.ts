export interface User {
  id: string
  email: string
  full_name?: string
  is_active: boolean
  is_verified: boolean
  created_at: string
  updated_at: string
}

export interface UserProfile {
  id: string
  full_name?: string
  business_name?: string
  business_type?: string
  industry?: string
  business_description?: string
  target_audience?: string[]
  unique_value_proposition?: string
  brand_voice?: string
  brand_tone?: string
  website_url?: string
  phone_number?: string
  street_address?: string
  city?: string
  state?: string
  country?: string
  timezone?: string
  social_media_platforms?: string[]
  primary_goals?: string[]
  key_metrics_to_track?: string[]
  monthly_budget_range?: string
  posting_frequency?: string
  preferred_content_types?: string[]
  content_themes?: string[]
  main_competitors?: string
  market_position?: string
  products_or_services?: string
  important_launch_dates?: string
  planned_promotions_or_campaigns?: string
  top_performing_content_types?: string[]
  best_time_to_post?: string[]
  successful_campaigns?: string
  hashtags_that_work_well?: string
  customer_pain_points?: string
  typical_customer_journey?: string
  automation_level?: string
  platform_specific_tone?: Record<string, string>
  onboarding_completed: boolean
  created_at: string
  updated_at: string
}

export interface OnboardingData {
  business_name: string
  business_type: string
  industry: string
  business_description: string
  target_audience: string[]
  unique_value_proposition: string
  brand_voice: string
  brand_tone: string
  website_url?: string
  phone_number: string
  street_address: string
  city: string
  state: string
  country: string
  timezone: string
  social_media_platforms: string[]
  primary_goals: string[]
  key_metrics_to_track: string[]
  monthly_budget_range: string
  posting_frequency: string
  preferred_content_types: string[]
  content_themes: string[]
  main_competitors: string
  market_position: string
  products_or_services: string
  important_launch_dates?: string
  planned_promotions_or_campaigns: string
  top_performing_content_types: string[]
  best_time_to_post: string[]
  successful_campaigns: string
  hashtags_that_work_well: string
  customer_pain_points: string
  typical_customer_journey: string
  automation_level: string
  platform_specific_tone: Record<string, string>
}

export interface AuthResponse {
  access_token: string
  token_type: string
  user: User
}

export interface ApiResponse<T = any> {
  message: string
  data?: T
}

export interface LoginCredentials {
  email: string
  password: string
}

export interface RegisterCredentials {
  email: string
  password: string
  full_name?: string
}

// Onboarding form options
export const BUSINESS_TYPES = [
  'Ecommerce',
  'Service',
  'Restaurant',
  'SaaS',
  'B2B',
  'B2C'
] as const

export const INDUSTRIES = [
  'Technology',
  'Retail',
  'Education',
  'Healthcare',
  'Fashion',
  'Food',
  'Travel',
  'Other'
] as const

export const TARGET_AUDIENCES = [
  'Young Professionals',
  'Outdoor Enthusiasts',
  'Students',
  'Parents',
  'Fitness Lovers',
  'Working Adults',
  'Seniors',
  'Teens'
] as const

export const BRAND_VOICES = [
  'Professional',
  'Casual',
  'Friendly',
  'Bold',
  'Playful'
] as const

export const BRAND_TONES = [
  'Formal',
  'Informal',
  'Humorous',
  'Inspirational',
  'Neutral'
] as const

export const SOCIAL_MEDIA_PLATFORMS = [
  'Instagram',
  'Facebook',
  'LinkedIn',
  'YouTube',
  'Pinterest',
  'X (Twitter)',
  'TikTok'
] as const

export const PRIMARY_GOALS = [
  'Increase Sales',
  'Brand Awareness',
  'Website Traffic',
  'Lead Generation',
  'Community Building',
  'Customer Engagement'
] as const

export const KEY_METRICS = [
  'Followers',
  'Clicks',
  'Engagement Rate',
  'Leads',
  'Shares',
  'Comments',
  'Conversions'
] as const

export const MONTHLY_BUDGET_RANGES = [
  '₹0–₹5,000',
  '₹5,000–₹10,000',
  '₹10,000–₹25,000',
  '₹25,000–₹50,000',
  '₹50,000+'
] as const

export const POSTING_FREQUENCIES = [
  'Daily',
  '3x/Week',
  'Weekly',
  'Bi-Weekly',
  'Monthly'
] as const

export const CONTENT_TYPES = [
  'Image Posts',
  'Reels',
  'Carousels',
  'Stories',
  'Blogs',
  'Videos',
  'Live Sessions'
] as const

export const CONTENT_THEMES = [
  'Product Features',
  'Behind the Scenes',
  'Customer Stories',
  'Tips & Tricks',
  'Educational',
  'Announcements',
  'User-Generated Content'
] as const

export const MARKET_POSITIONS = [
  'Leader',
  'Challenger',
  'Niche',
  'New Entrant'
] as const

export const AUTOMATION_LEVELS = [
  'Full Auto – Let AI handle everything',
  'Suggestions Only – Show suggestions for review',
  'Manual Approval – I want to approve every step'
] as const

export const BEST_TIMES_TO_POST = [
  'Morning',
  'Afternoon',
  'Evening',
  'Weekends',
  'Weekdays'
] as const

export const PLATFORM_TONES = [
  'Fun',
  'Professional',
  'Casual',
  'Humorous',
  'Bold',
  'Neutral'
] as const

export const PLATFORMS = [
  'Instagram',
  'Facebook',
  'LinkedIn',
  'YouTube',
  'X'
] as const 