import React from 'react'
import { useFormContext } from 'react-hook-form'

const Step8PerformanceCustomer: React.FC = () => {
  const { register, formState: { errors } } = useFormContext()

  return (
    <div className="space-y-6">
      <div>
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Performance & Customer</h3>
        <p className="text-gray-600 mb-6">Share insights about your best campaigns and your customers.</p>
      </div>

      <div>
        <label htmlFor="successful_campaigns" className="block text-sm font-medium text-gray-700 mb-2">
          Successful Campaigns *
        </label>
        <textarea
          {...register('successful_campaigns')}
          id="successful_campaigns"
          rows={3}
          className="input-field"
          placeholder="Mention any marketing campaigns that worked well for you"
        />
        {errors.successful_campaigns && (
          <p className="text-red-500 text-sm mt-1">{errors.successful_campaigns.message}</p>
        )}
      </div>

      <div>
        <label htmlFor="hashtags_that_work_well" className="block text-sm font-medium text-gray-700 mb-2">
          Hashtags That Work Well *
        </label>
        <textarea
          {...register('hashtags_that_work_well')}
          id="hashtags_that_work_well"
          rows={2}
          className="input-field"
          placeholder="List hashtags that gave good reach or engagement"
        />
        {errors.hashtags_that_work_well && (
          <p className="text-red-500 text-sm mt-1">{errors.hashtags_that_work_well.message}</p>
        )}
      </div>

      <div>
        <label htmlFor="customer_pain_points" className="block text-sm font-medium text-gray-700 mb-2">
          Customer Pain Points *
        </label>
        <textarea
          {...register('customer_pain_points')}
          id="customer_pain_points"
          rows={2}
          className="input-field"
          placeholder="What common problems does your product or service solve?"
        />
        {errors.customer_pain_points && (
          <p className="text-red-500 text-sm mt-1">{errors.customer_pain_points.message}</p>
        )}
      </div>

      <div>
        <label htmlFor="typical_customer_journey" className="block text-sm font-medium text-gray-700 mb-2">
          Typical Customer Journey *
        </label>
        <textarea
          {...register('typical_customer_journey')}
          id="typical_customer_journey"
          rows={2}
          className="input-field"
          placeholder="Describe the usual journey your customer takes before buying"
        />
        {errors.typical_customer_journey && (
          <p className="text-red-500 text-sm mt-1">{errors.typical_customer_journey.message}</p>
        )}
      </div>
    </div>
  )
}

export default Step8PerformanceCustomer 