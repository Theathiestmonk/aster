import React from 'react'
import { useFormContext } from 'react-hook-form'
import { AUTOMATION_LEVELS, PLATFORMS, PLATFORM_TONES } from '@/types'

const Step9AutomationPlatformTone: React.FC = () => {
  const { register, formState: { errors }, watch, setValue } = useFormContext()
  const platformSpecificTone = watch('platform_specific_tone') || {}

  const handleToneChange = (platform: string, tone: string) => {
    setValue('platform_specific_tone', {
      ...platformSpecificTone,
      [platform]: tone,
    })
  }

  return (
    <div className="space-y-6">
      <div>
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Automation & Platform-Specific Tone</h3>
        <p className="text-gray-600 mb-6">Choose your automation preference and set the tone for each platform.</p>
      </div>

      <div>
        <label htmlFor="automation_level" className="block text-sm font-medium text-gray-700 mb-2">
          Automation Level *
        </label>
        <select
          {...register('automation_level')}
          id="automation_level"
          className="input-field"
        >
          <option value="">Select automation level</option>
          {AUTOMATION_LEVELS.map((level) => (
            <option key={level} value={level}>{level}</option>
          ))}
        </select>
        {errors.automation_level && (
          <p className="text-red-500 text-sm mt-1">{errors.automation_level.message}</p>
        )}
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Platform-Specific Tone *
        </label>
        <div className="overflow-x-auto">
          <table className="min-w-full border border-gray-200 rounded-lg">
            <thead>
              <tr>
                <th className="px-2 py-1 border-b text-left text-xs font-semibold text-gray-700">Platform</th>
                {PLATFORM_TONES.map((tone) => (
                  <th key={tone} className="px-2 py-1 border-b text-xs font-semibold text-gray-700">{tone}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {PLATFORMS.map((platform) => (
                <tr key={platform}>
                  <td className="px-2 py-1 border-b text-sm text-gray-700 font-medium">{platform}</td>
                  {PLATFORM_TONES.map((tone) => (
                    <td key={tone} className="px-2 py-1 border-b text-center">
                      <input
                        type="radio"
                        name={`platform_specific_tone.${platform}`}
                        checked={platformSpecificTone[platform] === tone}
                        onChange={() => handleToneChange(platform, tone)}
                        className="accent-primary"
                      />
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        {errors.platform_specific_tone && (
          <p className="text-red-500 text-sm mt-1">{errors.platform_specific_tone.message}</p>
        )}
      </div>
    </div>
  )
}

export default Step9AutomationPlatformTone 