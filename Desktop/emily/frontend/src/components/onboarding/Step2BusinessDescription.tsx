import React from 'react'
import { useFormContext } from 'react-hook-form'
import { TARGET_AUDIENCES } from '@/types'

const Step2BusinessDescription: React.FC = () => {
  const { register, formState: { errors }, watch } = useFormContext()
  const targetAudience = watch('target_audience') || []

  const handleCheckboxChange = (value: string) => {
    const currentValues = targetAudience
    const newValues = currentValues.includes(value)
      ? currentValues.filter((v: string) => v !== value)
      : [...currentValues, value]
    
    // Update the form value
    const event = {
      target: { name: 'target_audience', value: newValues }
    }
    register('target_audience').onChange(event)
  }

  return (
    <div className="space-y-6">
      <div>
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Describe your business</h3>
        <p className="text-gray-600 mb-6">Help us understand what makes your business unique.</p>
      </div>

      <div>
        <label htmlFor="business_description" className="block text-sm font-medium text-gray-700 mb-2">
          Business Description *
        </label>
        <textarea
          {...register('business_description')}
          id="business_description"
          rows={4}
          className="input-field"
          placeholder="Briefly describe what your business does"
        />
        {errors.business_description && (
          <p className="text-red-500 text-sm mt-1">{errors.business_description.message}</p>
        )}
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700 mb-3">
          Target Audience (Select all that apply) *
        </label>
        <div className="grid grid-cols-2 gap-3">
          {TARGET_AUDIENCES.map((audience) => (
            <label key={audience} className="flex items-center space-x-2 cursor-pointer">
              <input
                type="checkbox"
                checked={targetAudience.includes(audience)}
                onChange={() => handleCheckboxChange(audience)}
                className="rounded border-gray-300 text-primary focus:ring-primary"
              />
              <span className="text-sm text-gray-700">{audience}</span>
            </label>
          ))}
        </div>
        {errors.target_audience && (
          <p className="text-red-500 text-sm mt-1">{errors.target_audience.message}</p>
        )}
      </div>

      <div>
        <label htmlFor="unique_value_proposition" className="block text-sm font-medium text-gray-700 mb-2">
          Unique Value Proposition *
        </label>
        <textarea
          {...register('unique_value_proposition')}
          id="unique_value_proposition"
          rows={3}
          className="input-field"
          placeholder="What makes your business or product unique?"
        />
        {errors.unique_value_proposition && (
          <p className="text-red-500 text-sm mt-1">{errors.unique_value_proposition.message}</p>
        )}
      </div>
    </div>
  )
}

export default Step2BusinessDescription 