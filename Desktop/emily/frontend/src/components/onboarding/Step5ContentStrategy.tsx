import React from 'react'
import { useFormContext } from 'react-hook-form'
import { CONTENT_TYPES, CONTENT_THEMES } from '@/types'

const Step5ContentStrategy: React.FC = () => {
  const { register, formState: { errors }, watch } = useFormContext()
  const preferredContentTypes = watch('preferred_content_types') || []
  const contentThemes = watch('content_themes') || []

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
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Content Strategy</h3>
        <p className="text-gray-600 mb-6">What types of content do you prefer to create and share?</p>
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700 mb-3">
          Preferred Content Types (Select all that apply) *
        </label>
        <div className="grid grid-cols-2 gap-3">
          {CONTENT_TYPES.map((type) => (
            <label key={type} className="flex items-center space-x-2 cursor-pointer">
              <input
                type="checkbox"
                checked={preferredContentTypes.includes(type)}
                onChange={() => handleCheckboxChange('preferred_content_types', type)}
                className="rounded border-gray-300 text-primary focus:ring-primary"
              />
              <span className="text-sm text-gray-700">{type}</span>
            </label>
          ))}
        </div>
        {errors.preferred_content_types && (
          <p className="text-red-500 text-sm mt-1">{errors.preferred_content_types.message}</p>
        )}
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700 mb-3">
          Content Themes (Select all that apply) *
        </label>
        <div className="grid grid-cols-2 gap-3">
          {CONTENT_THEMES.map((theme) => (
            <label key={theme} className="flex items-center space-x-2 cursor-pointer">
              <input
                type="checkbox"
                checked={contentThemes.includes(theme)}
                onChange={() => handleCheckboxChange('content_themes', theme)}
                className="rounded border-gray-300 text-primary focus:ring-primary"
              />
              <span className="text-sm text-gray-700">{theme}</span>
            </label>
          ))}
        </div>
        {errors.content_themes && (
          <p className="text-red-500 text-sm mt-1">{errors.content_themes.message}</p>
        )}
      </div>
    </div>
  )
}

export default Step5ContentStrategy 