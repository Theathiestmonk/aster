import React from 'react'
import { useFormContext } from 'react-hook-form'
import { MARKET_POSITIONS } from '@/types'

const Step6MarketCompetition: React.FC = () => {
  const { register, formState: { errors } } = useFormContext()

  return (
    <div className="space-y-6">
      <div>
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Market & Competition</h3>
        <p className="text-gray-600 mb-6">Help us understand your market position and competition.</p>
      </div>

      <div>
        <label htmlFor="main_competitors" className="block text-sm font-medium text-gray-700 mb-2">
          Main Competitors *
        </label>
        <textarea
          {...register('main_competitors')}
          id="main_competitors"
          rows={3}
          className="input-field"
          placeholder="List names of competitors or similar brands"
        />
        {errors.main_competitors && (
          <p className="text-red-500 text-sm mt-1">{errors.main_competitors.message}</p>
        )}
      </div>

      <div>
        <label htmlFor="market_position" className="block text-sm font-medium text-gray-700 mb-2">
          Market Position *
        </label>
        <select
          {...register('market_position')}
          id="market_position"
          className="input-field"
        >
          <option value="">Select market position</option>
          {MARKET_POSITIONS.map((position) => (
            <option key={position} value={position}>{position}</option>
          ))}
        </select>
        {errors.market_position && (
          <p className="text-red-500 text-sm mt-1">{errors.market_position.message}</p>
        )}
      </div>

      <div>
        <label htmlFor="products_or_services" className="block text-sm font-medium text-gray-700 mb-2">
          Products or Services *
        </label>
        <textarea
          {...register('products_or_services')}
          id="products_or_services"
          rows={4}
          className="input-field"
          placeholder="List key products or services you want to promote"
        />
        {errors.products_or_services && (
          <p className="text-red-500 text-sm mt-1">{errors.products_or_services.message}</p>
        )}
      </div>
    </div>
  )
}

export default Step6MarketCompetition 