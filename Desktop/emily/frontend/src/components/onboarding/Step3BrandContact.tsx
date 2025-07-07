import React from 'react'
import { useFormContext } from 'react-hook-form'
import { BRAND_VOICES, BRAND_TONES } from '@/types'

const Step3BrandContact: React.FC = () => {
  const { register, formState: { errors } } = useFormContext()

  return (
    <div className="space-y-6">
      <div>
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Brand & Contact Information</h3>
        <p className="text-gray-600 mb-6">Tell us about your brand voice and how to reach you.</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div>
          <label htmlFor="brand_voice" className="block text-sm font-medium text-gray-700 mb-2">
            Brand Voice *
          </label>
          <select
            {...register('brand_voice')}
            id="brand_voice"
            className="input-field"
          >
            <option value="">Select brand voice</option>
            {BRAND_VOICES.map((voice) => (
              <option key={voice} value={voice}>{voice}</option>
            ))}
          </select>
          {errors.brand_voice && (
            <p className="text-red-500 text-sm mt-1">{errors.brand_voice.message}</p>
          )}
        </div>

        <div>
          <label htmlFor="brand_tone" className="block text-sm font-medium text-gray-700 mb-2">
            Brand Tone *
          </label>
          <select
            {...register('brand_tone')}
            id="brand_tone"
            className="input-field"
          >
            <option value="">Select brand tone</option>
            {BRAND_TONES.map((tone) => (
              <option key={tone} value={tone}>{tone}</option>
            ))}
          </select>
          {errors.brand_tone && (
            <p className="text-red-500 text-sm mt-1">{errors.brand_tone.message}</p>
          )}
        </div>
      </div>

      <div>
        <label htmlFor="website_url" className="block text-sm font-medium text-gray-700 mb-2">
          Website URL
        </label>
        <input
          {...register('website_url')}
          type="url"
          id="website_url"
          className="input-field"
          placeholder="Enter your business website (if any)"
        />
        {errors.website_url && (
          <p className="text-red-500 text-sm mt-1">{errors.website_url.message}</p>
        )}
      </div>

      <div>
        <label htmlFor="phone_number" className="block text-sm font-medium text-gray-700 mb-2">
          Phone Number *
        </label>
        <input
          {...register('phone_number')}
          type="tel"
          id="phone_number"
          className="input-field"
          placeholder="Enter your contact number"
        />
        {errors.phone_number && (
          <p className="text-red-500 text-sm mt-1">{errors.phone_number.message}</p>
        )}
      </div>

      <div>
        <label htmlFor="street_address" className="block text-sm font-medium text-gray-700 mb-2">
          Street Address *
        </label>
        <input
          {...register('street_address')}
          type="text"
          id="street_address"
          className="input-field"
          placeholder="Enter your business address"
        />
        {errors.street_address && (
          <p className="text-red-500 text-sm mt-1">{errors.street_address.message}</p>
        )}
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div>
          <label htmlFor="city" className="block text-sm font-medium text-gray-700 mb-2">
            City *
          </label>
          <input
            {...register('city')}
            type="text"
            id="city"
            className="input-field"
            placeholder="City"
          />
          {errors.city && (
            <p className="text-red-500 text-sm mt-1">{errors.city.message}</p>
          )}
        </div>

        <div>
          <label htmlFor="state" className="block text-sm font-medium text-gray-700 mb-2">
            State *
          </label>
          <input
            {...register('state')}
            type="text"
            id="state"
            className="input-field"
            placeholder="State"
          />
          {errors.state && (
            <p className="text-red-500 text-sm mt-1">{errors.state.message}</p>
          )}
        </div>

        <div>
          <label htmlFor="country" className="block text-sm font-medium text-gray-700 mb-2">
            Country *
          </label>
          <input
            {...register('country')}
            type="text"
            id="country"
            className="input-field"
            placeholder="Country"
          />
          {errors.country && (
            <p className="text-red-500 text-sm mt-1">{errors.country.message}</p>
          )}
        </div>
      </div>

      <div>
        <label htmlFor="timezone" className="block text-sm font-medium text-gray-700 mb-2">
          Timezone *
        </label>
        <select
          {...register('timezone')}
          id="timezone"
          className="input-field"
        >
          <option value="">Select timezone</option>
          <option value="Asia/Kolkata">Asia/Kolkata (IST)</option>
          <option value="Europe/London">Europe/London (GMT)</option>
          <option value="America/New_York">America/New_York (EST)</option>
          <option value="America/Los_Angeles">America/Los_Angeles (PST)</option>
          <option value="Europe/Paris">Europe/Paris (CET)</option>
          <option value="Asia/Tokyo">Asia/Tokyo (JST)</option>
          <option value="Australia/Sydney">Australia/Sydney (AEST)</option>
        </select>
        {errors.timezone && (
          <p className="text-red-500 text-sm mt-1">{errors.timezone.message}</p>
        )}
      </div>
    </div>
  )
}

export default Step3BrandContact 