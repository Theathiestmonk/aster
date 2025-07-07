import React, { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { useForm, FormProvider } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'
import { useAuth } from '@/hooks/useAuth'
import { authService } from '@/services/auth'
import { toast } from 'react-hot-toast'
import { ArrowLeft, Save, User } from 'lucide-react'
import LoadingSpinner from '@/components/ui/LoadingSpinner'

// Import all the step components from onboarding
import Step1BasicBusiness from '@/components/onboarding/Step1BasicBusiness'
import Step2BusinessDescription from '@/components/onboarding/Step2BusinessDescription'
import Step3BrandContact from '@/components/onboarding/Step3BrandContact'
import Step4SocialGoals from '@/components/onboarding/Step4SocialGoals'
import Step5ContentStrategy from '@/components/onboarding/Step5ContentStrategy'
import Step6MarketCompetition from '@/components/onboarding/Step6MarketCompetition'
import Step7CampaignPlanning from '@/components/onboarding/Step7CampaignPlanning'
import Step8PerformanceCustomer from '@/components/onboarding/Step8PerformanceCustomer'
import Step9AutomationPlatformTone from '@/components/onboarding/Step9AutomationPlatformTone'

// Zod schema for profile editing (same as onboarding)
const profileSchema = z.object({
  business_name: z.string().min(1, 'Business name is required'),
  business_type: z.string().min(1),
  industry: z.string().min(1),
  business_description: z.string().min(1),
  target_audience: z.array(z.string()).min(1),
  unique_value_proposition: z.string().min(1),
  brand_voice: z.string().min(1),
  brand_tone: z.string().min(1),
  website_url: z.string().url().optional().or(z.literal('')),
  phone_number: z.string().min(1),
  street_address: z.string().min(1),
  city: z.string().min(1),
  state: z.string().min(1),
  country: z.string().min(1),
  timezone: z.string().min(1),
  social_media_platforms: z.array(z.string()).min(1),
  primary_goals: z.array(z.string()).min(1),
  key_metrics_to_track: z.array(z.string()).min(1),
  monthly_budget_range: z.string().min(1),
  posting_frequency: z.string().min(1),
  preferred_content_types: z.array(z.string()).min(1),
  content_themes: z.array(z.string()).min(1),
  main_competitors: z.string().min(1),
  market_position: z.string().min(1),
  products_or_services: z.string().min(1),
  important_launch_dates: z.string().optional().or(z.literal('')),
  planned_promotions_or_campaigns: z.string().min(1),
  top_performing_content_types: z.array(z.string()).min(1),
  best_time_to_post: z.array(z.string()).min(1),
  successful_campaigns: z.string().min(1),
  hashtags_that_work_well: z.string().min(1),
  customer_pain_points: z.string().min(1),
  typical_customer_journey: z.string().min(1),
  automation_level: z.string().min(1),
  platform_specific_tone: z.record(z.string()),
})

type ProfileFormData = z.infer<typeof profileSchema>

const steps = [
  'Basic Business Info',
  'Business Description',
  'Brand & Contact',
  'Social Media & Goals',
  'Content Strategy',
  'Market & Competition',
  'Campaign Planning',
  'Performance & Customer',
  'Automation & Platform Tone',
]

const EditProfile: React.FC = () => {
  const [step, setStep] = useState(0)
  const [saving, setSaving] = useState(false)
  const [loading, setLoading] = useState(true)
  const [userProfile, setUserProfile] = useState<any>(null)
  const navigate = useNavigate()
  const { user } = useAuth()

  const methods = useForm<ProfileFormData>({
    resolver: zodResolver(profileSchema),
    mode: 'onTouched',
  })

  // Fetch current profile data
  useEffect(() => {
    const fetchProfile = async () => {
      try {
        const profile = await authService.getUserProfile()
        setUserProfile(profile)
        
        // Set form default values from profile
        if (profile) {
          const defaultValues = {
            business_name: profile.business_name || '',
            business_type: profile.business_type || '',
            industry: profile.industry || '',
            business_description: profile.business_description || '',
            target_audience: profile.target_audience || [],
            unique_value_proposition: profile.unique_value_proposition || '',
            brand_voice: profile.brand_voice || '',
            brand_tone: profile.brand_tone || '',
            website_url: profile.website_url || '',
            phone_number: profile.phone_number || '',
            street_address: profile.street_address || '',
            city: profile.city || '',
            state: profile.state || '',
            country: profile.country || '',
            timezone: profile.timezone || Intl.DateTimeFormat().resolvedOptions().timeZone || '',
            social_media_platforms: profile.social_media_platforms || [],
            primary_goals: profile.primary_goals || [],
            key_metrics_to_track: profile.key_metrics_to_track || [],
            monthly_budget_range: profile.monthly_budget_range || '',
            posting_frequency: profile.posting_frequency || '',
            preferred_content_types: profile.preferred_content_types || [],
            content_themes: profile.content_themes || [],
            main_competitors: profile.main_competitors || '',
            market_position: profile.market_position || '',
            products_or_services: profile.products_or_services || '',
            important_launch_dates: profile.important_launch_dates || '',
            planned_promotions_or_campaigns: profile.planned_promotions_or_campaigns || '',
            top_performing_content_types: profile.top_performing_content_types || [],
            best_time_to_post: profile.best_time_to_post || [],
            successful_campaigns: profile.successful_campaigns || '',
            hashtags_that_work_well: profile.hashtags_that_work_well || '',
            customer_pain_points: profile.customer_pain_points || '',
            typical_customer_journey: profile.typical_customer_journey || '',
            automation_level: profile.automation_level || '',
            platform_specific_tone: profile.platform_specific_tone || {},
          }
          
          methods.reset(defaultValues)
        }
      } catch (error) {
        console.error('Error fetching profile:', error)
        toast.error('Failed to load profile data')
      } finally {
        setLoading(false)
      }
    }

    fetchProfile()
  }, [methods])

  const nextStep = () => {
    setStep(s => Math.min(s + 1, steps.length - 1))
  }

  const prevStep = () => setStep(s => Math.max(s - 1, 0))

  const onSubmit = async (data: ProfileFormData) => {
    setSaving(true)
    try {
      // Use the same onboarding service to update the profile
      await authService.updateProfile(data)
      toast.success('Profile updated successfully!')
      navigate('/user-dashboard')
    } catch (e: any) {
      toast.error(e.response?.data?.detail || 'Update failed')
    } finally {
      setSaving(false)
    }
  }

  // Render the appropriate step component
  const renderStep = () => {
    switch (step) {
      case 0:
        return <Step1BasicBusiness />
      case 1:
        return <Step2BusinessDescription />
      case 2:
        return <Step3BrandContact />
      case 3:
        return <Step4SocialGoals />
      case 4:
        return <Step5ContentStrategy />
      case 5:
        return <Step6MarketCompetition />
      case 6:
        return <Step7CampaignPlanning />
      case 7:
        return <Step8PerformanceCustomer />
      case 8:
        return <Step9AutomationPlatformTone />
      default:
        return <Step1BasicBusiness />
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <LoadingSpinner size="lg" />
          <p className="mt-4 text-gray-600">Loading your profile...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center space-x-4">
              <button
                onClick={() => navigate('/user-dashboard')}
                className="flex items-center space-x-2 text-gray-600 hover:text-gray-900 transition-colors"
              >
                <ArrowLeft className="w-5 h-5" />
                <span>Back to Dashboard</span>
              </button>
            </div>
            <div className="flex items-center space-x-3">
              <User className="w-5 h-5 text-gray-500" />
              <span className="text-sm text-gray-700">
                {user?.full_name || user?.email}
              </span>
            </div>
          </div>
        </div>
      </div>

      <FormProvider {...methods}>
        <div className="max-w-2xl mx-auto bg-white rounded-xl shadow-lg p-8 mt-8">
          <div className="mb-8">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-xl font-bold gradient-text">Edit Business Profile: {steps[step]}</h2>
              <span className="text-sm text-gray-500">Step {step + 1} of {steps.length}</span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-2 mb-4">
              <div 
                className="bg-gradient-to-r from-primary to-accent h-2 rounded-full" 
                style={{ width: `${((step + 1) / steps.length) * 100}%` }}
              ></div>
            </div>
          </div>
          
          <form onSubmit={methods.handleSubmit(onSubmit)}>
            {renderStep()}
            
            <div className="flex justify-between mt-8">
              <button 
                type="button" 
                onClick={prevStep} 
                disabled={step === 0} 
                className="btn-secondary"
              >
                Back
              </button>
              {step < steps.length - 1 ? (
                <button 
                  type="button" 
                  onClick={nextStep} 
                  className="btn-primary"
                >
                  Next
                </button>
              ) : (
                <button 
                  type="submit" 
                  className="btn-primary flex items-center space-x-2" 
                  disabled={saving}
                >
                  {saving ? (
                    <>
                      <LoadingSpinner size="sm" />
                      <span>Saving...</span>
                    </>
                  ) : (
                    <>
                      <Save className="w-4 h-4" />
                      <span>Save Changes</span>
                    </>
                  )}
                </button>
              )}
            </div>
          </form>
        </div>
      </FormProvider>
    </div>
  )
}

export default EditProfile 