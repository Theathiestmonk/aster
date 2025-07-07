import React from 'react'
import { useFormContext } from 'react-hook-form'
import { SOCIAL_MEDIA_PLATFORMS, PRIMARY_GOALS, KEY_METRICS, MONTHLY_BUDGET_RANGES, POSTING_FREQUENCIES } from '@/types'

const Step4SocialGoals: React.FC = () => {
  const { register, formState: { errors }, watch } = useFormContext()
  const socialPlatforms = watch('social_media_platforms') || []
  const primaryGoals = watch('primary_goals') || []
  const keyMetrics = watch('key_metrics_to_track') || []

  const handleCheckboxChange = (field: string, value: string) => {
    const currentValues = watch(field) || []
    const newValues = currentValues.includes(value)
      ? currentValues.filter((v: string) => v !== value)
      : [...currentValues, value]
    
    const event = {
      target: { name: field, value: newValues }
    }
    register(field).onChange(event)
  }

  return (
    <div className="space-y-6">
      <div>
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Social Media & Goals</h3>
        <p className="text-gray-600 mb-6">Tell us about your social media presence and marketing objectives.</p>
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700 mb-3">
          Social Media Platforms (Select all that apply) *
        </label>
        <div className="grid grid-cols-2 gap-3">
          {SOCIAL_MEDIA_PLATFORMS.map((platform) => (
            <label key={platform} className="flex items-center space-x-2 cursor-pointer">
              <input
                type="checkbox"
                checked={socialPlatforms.includes(platform)}
                onChange={() => handleCheckboxChange('social_media_platforms', platform)}
                className="rounded border-gray-300 text-primary focus:ring-primary"
              />
              <span className="text-sm text-gray-700">{platform}</span>
            </label>
          ))}
        </div>
        {errors.social_media_platforms && (
          <p className="text-red-500 text-sm mt-1">{errors.social_media_platforms.message}</p>
        )}
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700 mb-3">
          Primary Goals (Select all that apply) *
        </label>
        <div className="grid grid-cols-2 gap-3">
          {PRIMARY_GOALS.map((goal) => (
            <label key={goal} className="flex items-center space-x-2 cursor-pointer">
              <input
                type="checkbox"
                checked={primaryGoals.includes(goal)}
                onChange={() => handleCheckboxChange('primary_goals', goal)}
                className="rounded border-gray-300 text-primary focus:ring-primary"
              />
              <span className="text-sm text-gray-700">{goal}</span>
            </label>
          ))}
        </div>
        {errors.primary_goals && (
          <p className="text-red-500 text-sm mt-1">{errors.primary_goals.message}</p>
        )}
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700 mb-3">
          Key Metrics to Track (Select all that apply) *
        </label>
        <div className="grid grid-cols-2 gap-3">
          {KEY_METRICS.map((metric) => (
            <label key={metric} className="flex items-center space-x-2 cursor-pointer">
              <input
                type="checkbox"
                checked={keyMetrics.includes(metric)}
                onChange={() => handleCheckboxChange('key_metrics_to_track', metric)}
                className="rounded border-gray-300 text-primary focus:ring-primary"
              />
              <span className="text-sm text-gray-700">{metric}</span>
            </label>
          ))}
        </div>
        {errors.key_metrics_to_track && (
          <p className="text-red-500 text-sm mt-1">{errors.key_metrics_to_track.message}</p>
        )}
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div>
          <label htmlFor="monthly_budget_range" className="block text-sm font-medium text-gray-700 mb-2">
            Monthly Budget Range *
          </label>
          <select
            {...register('monthly_budget_range')}
            id="monthly_budget_range"
            className="input-field"
          >
            <option value="">Select budget range</option>
            {MONTHLY_BUDGET_RANGES.map((range) => (
              <option key={range} value={range}>{range}</option>
            ))}
          </select>
          {errors.monthly_budget_range && (
            <p className="text-red-500 text-sm mt-1">{errors.monthly_budget_range.message}</p>
          )}
        </div>

        <div>
          <label htmlFor="posting_frequency" className="block text-sm font-medium text-gray-700 mb-2">
            Posting Frequency *
          </label>
          <select
            {...register('posting_frequency')}
            id="posting_frequency"
            className="input-field"
          >
            <option value="">Select frequency</option>
            {POSTING_FREQUENCIES.map((frequency) => (
              <option key={frequency} value={frequency}>{frequency}</option>
            ))}
          </select>
          {errors.posting_frequency && (
            <p className="text-red-500 text-sm mt-1">{errors.posting_frequency.message}</p>
          )}
        </div>
      </div>
    </div>
  )
}

export default Step4SocialGoals 