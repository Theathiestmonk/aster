import React, { useState } from 'react'
import { useForm, FormProvider } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'
import { useNavigate } from 'react-router-dom'
import { onboardingService } from '@/services/onboarding'
import { toast } from 'react-hot-toast'
import {
  BUSINESS_TYPES, INDUSTRIES, TARGET_AUDIENCES, BRAND_VOICES, BRAND_TONES, SOCIAL_MEDIA_PLATFORMS, PRIMARY_GOALS, KEY_METRICS, MONTHLY_BUDGET_RANGES, POSTING_FREQUENCIES, CONTENT_TYPES, CONTENT_THEMES, MARKET_POSITIONS, AUTOMATION_LEVELS, BEST_TIMES_TO_POST, PLATFORM_TONES, PLATFORMS
} from '@/types'

// Import step components
import Step1BasicBusiness from '@/components/onboarding/Step1BasicBusiness'
import Step2BusinessDescription from '@/components/onboarding/Step2BusinessDescription'
import Step3BrandContact from '@/components/onboarding/Step3BrandContact'
import Step4SocialGoals from '@/components/onboarding/Step4SocialGoals'
import Step5ContentStrategy from '@/components/onboarding/Step5ContentStrategy'
import Step6MarketCompetition from '@/components/onboarding/Step6MarketCompetition'
import Step7CampaignPlanning from '@/components/onboarding/Step7CampaignPlanning'
import Step8PerformanceCustomer from '@/components/onboarding/Step8PerformanceCustomer'
import Step9AutomationPlatformTone from '@/components/onboarding/Step9AutomationPlatformTone'
import Step10ReviewSubmit from '@/components/onboarding/Step10ReviewSubmit'

// Zod schema for onboarding
const onboardingSchema = z.object({
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
  platform_specific_tone: z.record(z.string()).refine(obj => Object.keys(obj).length === PLATFORMS.length, { message: 'Please select a tone for each platform.' })
})

type OnboardingFormData = z.infer<typeof onboardingSchema>

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
  'Review & Submit',
]

const defaultValues: OnboardingFormData = {
  business_name: '',
  business_type: '',
  industry: '',
  business_description: '',
  target_audience: [],
  unique_value_proposition: '',
  brand_voice: '',
  brand_tone: '',
  website_url: '',
  phone_number: '',
  street_address: '',
  city: '',
  state: '',
  country: '',
  timezone: Intl.DateTimeFormat().resolvedOptions().timeZone || '',
  social_media_platforms: [],
  primary_goals: [],
  key_metrics_to_track: [],
  monthly_budget_range: '',
  posting_frequency: '',
  preferred_content_types: [],
  content_themes: [],
  main_competitors: '',
  market_position: '',
  products_or_services: '',
  important_launch_dates: '',
  planned_promotions_or_campaigns: '',
  top_performing_content_types: [],
  best_time_to_post: [],
  successful_campaigns: '',
  hashtags_that_work_well: '',
  customer_pain_points: '',
  typical_customer_journey: '',
  automation_level: '',
  platform_specific_tone: Object.fromEntries(PLATFORMS.map(p => [p, ''])),
}

const Onboarding: React.FC = () => {
  const [step, setStep] = useState(0)
  const [submitting, setSubmitting] = useState(false)
  const navigate = useNavigate()
  const methods = useForm<OnboardingFormData>({
    resolver: zodResolver(onboardingSchema),
    defaultValues,
    mode: 'onTouched',
  })

  const nextStep = async () => {
    console.log('Next step clicked, current step:', step)
    
    // For now, just move to next step without validation to test navigation
    console.log('Moving to next step')
    setStep(s => Math.min(s + 1, steps.length - 1))
    
    // TODO: Add step-specific validation later
    // const valid = await methods.trigger()
    // if (valid) {
    //   setStep(s => Math.min(s + 1, steps.length - 1))
    // } else {
    //   console.log('Form validation failed:', methods.formState.errors)
    // }
  }
  const prevStep = () => setStep(s => Math.max(s - 1, 0))

  const onSubmit = async (data: OnboardingFormData) => {
    setSubmitting(true)
    try {
      await onboardingService.submitOnboarding(data)
      toast.success('Onboarding complete!')
      navigate('/user-dashboard')
    } catch (e: any) {
      toast.error(e.response?.data?.detail || 'Submission failed')
    } finally {
      setSubmitting(false)
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
      case 9:
        return <Step10ReviewSubmit />
      default:
        return <Step1BasicBusiness />
    }
  }

  return (
    <FormProvider {...methods}>
      <div className="max-w-2xl mx-auto bg-white rounded-xl shadow-lg p-8 mt-8">
        <div className="mb-8">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-xl font-bold gradient-text">Onboarding: {steps[step]}</h2>
            <span className="text-sm text-gray-500">Step {step + 1} of {steps.length}</span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-2 mb-4">
            <div className="bg-gradient-to-r from-primary to-accent h-2 rounded-full" style={{ width: `${((step + 1) / steps.length) * 100}%` }}></div>
          </div>
        </div>
        
        <form onSubmit={methods.handleSubmit(onSubmit)}>
          {renderStep()}
          
          <div className="flex justify-between mt-8">
            <button type="button" onClick={prevStep} disabled={step === 0} className="btn-secondary">Back</button>
            {step < steps.length - 1 ? (
              <button type="button" onClick={nextStep} className="btn-primary">Next</button>
            ) : (
              <button type="submit" className="btn-primary" disabled={submitting}>{submitting ? 'Submitting...' : 'Submit'}</button>
            )}
          </div>
        </form>
      </div>
    </FormProvider>
  )
}

export default Onboarding 