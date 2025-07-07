import React from 'react'
import { useFormContext } from 'react-hook-form'
import { CONTENT_TYPES, BEST_TIMES_TO_POST } from '@/types'

const Step7CampaignPlanning: React.FC = () => {
  const { register, formState: { errors }, watch } = useFormContext()
  const topPerformingContentTypes = watch('top_performing_content_types') || []
  const bestTimeToPost = watch('best_time_to_post') || []

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
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Campaign Planning</h3>
        <p className="text-gray-600 mb-6">Tell us about your upcoming campaigns and best performing content.</p>
      </div>

      <div>
        <label htmlFor="important_launch_dates" className="block text-sm font-medium text-gray-700 mb-2">
          Important Launch Dates
        </label>
        <input
          {...register('important_launch_dates')}
          type="date"
          id="important_launch_dates"
          className="input-field"
        />
        {errors.important_launch_dates && (
          <p className="text-red-500 text-sm mt-1">{errors.important_launch_dates.message}</p>
        )}
      </div>

      <div>
        <label htmlFor="planned_promotions_or_campaigns" className="block text-sm font-medium text-gray-700 mb-2">
          Planned Promotions or Campaigns *
        </label>
        <textarea
          {...register('planned_promotions_or_campaigns')}
          id="planned_promotions_or_campaigns"
          rows={3}
          className="input-field"
          placeholder="Mention any offers, discount periods, or seasonal campaigns"
        />
        {errors.planned_promotions_or_campaigns && (
          <p className="text-red-500 text-sm mt-1">{errors.planned_promotions_or_campaigns.message}</p>
        )}
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700 mb-3">
          Top-Performing Content Types (Select all that apply) *
        </label>
        <div className="grid grid-cols-2 gap-3">
          {CONTENT_TYPES.map((type) => (
            <label key={type} className="flex items-center space-x-2 cursor-pointer">
              <input
                type="checkbox"
                checked={topPerformingContentTypes.includes(type)}
                onChange={() => handleCheckboxChange('top_performing_content_types', type)}
                className="rounded border-gray-300 text-primary focus:ring-primary"
              />
              <span className="text-sm text-gray-700">{type}</span>
            </label>
          ))}
        </div>
        {errors.top_performing_content_types && (
          <p className="text-red-500 text-sm mt-1">{errors.top_performing_content_types.message}</p>
        )}
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700 mb-3">
          Best Time to Post (Select all that apply) *
        </label>
        <div className="grid grid-cols-2 gap-3">
          {BEST_TIMES_TO_POST.map((time) => (
            <label key={time} className="flex items-center space-x-2 cursor-pointer">
              <input
                type="checkbox"
                checked={bestTimeToPost.includes(time)}
                onChange={() => handleCheckboxChange('best_time_to_post', time)}
                className="rounded border-gray-300 text-primary focus:ring-primary"
              />
              <span className="text-sm text-gray-700">{time}</span>
            </label>
          ))}
        </div>
        {errors.best_time_to_post && (
          <p className="text-red-500 text-sm mt-1">{errors.best_time_to_post.message}</p>
        )}
      </div>
    </div>
  )
}

export default Step7CampaignPlanning 