import React from 'react'
import { useFormContext } from 'react-hook-form'
import { BUSINESS_TYPES, INDUSTRIES } from '@/types'

const Step1BasicBusiness: React.FC = () => {
  const { register, formState: { errors } } = useFormContext()

  return (
    <div className="space-y-6">
      <div>
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Tell us about your business</h3>
        <p className="text-gray-600 mb-6">Let's start with the basics to understand your business better.</p>
      </div>

      <div>
        <label htmlFor="business_name" className="block text-sm font-medium text-gray-700 mb-2">
          Business Name *
        </label>
        <input
          {...register('business_name')}
          type="text"
          id="business_name"
          className="input-field"
          placeholder="Enter your business name"
        />
        {errors.business_name && (
          <p className="text-red-500 text-sm mt-1">{errors.business_name.message}</p>
        )}
      </div>

      <div>
        <label htmlFor="business_type" className="block text-sm font-medium text-gray-700 mb-2">
          Business Type *
        </label>
        <select
          {...register('business_type')}
          id="business_type"
          className="input-field"
        >
          <option value="">Select business type</option>
          {BUSINESS_TYPES.map((type) => (
            <option key={type} value={type}>{type}</option>
          ))}
        </select>
        {errors.business_type && (
          <p className="text-red-500 text-sm mt-1">{errors.business_type.message}</p>
        )}
      </div>

      <div>
        <label htmlFor="industry" className="block text-sm font-medium text-gray-700 mb-2">
          Industry *
        </label>
        <select
          {...register('industry')}
          id="industry"
          className="input-field"
        >
          <option value="">Select industry</option>
          {INDUSTRIES.map((industry) => (
            <option key={industry} value={industry}>{industry}</option>
          ))}
        </select>
        {errors.industry && (
          <p className="text-red-500 text-sm mt-1">{errors.industry.message}</p>
        )}
      </div>
    </div>
  )
}

export default Step1BasicBusiness 