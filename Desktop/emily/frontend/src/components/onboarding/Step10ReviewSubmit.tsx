import React from 'react'
import { useFormContext } from 'react-hook-form'
import { PLATFORMS } from '@/types'

const Step10ReviewSubmit: React.FC = () => {
  const { getValues } = useFormContext()
  const values = getValues()

  return (
    <div className="space-y-6">
      <div>
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Review & Submit</h3>
        <p className="text-gray-600 mb-6">Please review your answers before submitting. You can go back to edit any step.</p>
      </div>
      <div className="bg-gray-50 rounded-lg p-4 border border-gray-200">
        <h4 className="font-semibold mb-2 text-primary">Business Info</h4>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-2 text-sm">
          <div><span className="font-medium">Business Name:</span> {values.business_name}</div>
          <div><span className="font-medium">Business Type:</span> {values.business_type}</div>
          <div><span className="font-medium">Industry:</span> {values.industry}</div>
          <div><span className="font-medium">Description:</span> {values.business_description}</div>
          <div><span className="font-medium">Target Audience:</span> {values.target_audience?.join(', ')}</div>
          <div><span className="font-medium">Unique Value Proposition:</span> {values.unique_value_proposition}</div>
          <div><span className="font-medium">Brand Voice:</span> {values.brand_voice}</div>
          <div><span className="font-medium">Brand Tone:</span> {values.brand_tone}</div>
          <div><span className="font-medium">Website:</span> {values.website_url}</div>
          <div><span className="font-medium">Phone:</span> {values.phone_number}</div>
          <div><span className="font-medium">Address:</span> {values.street_address}, {values.city}, {values.state}, {values.country}</div>
          <div><span className="font-medium">Timezone:</span> {values.timezone}</div>
          <div><span className="font-medium">Social Platforms:</span> {values.social_media_platforms?.join(', ')}</div>
          <div><span className="font-medium">Primary Goals:</span> {values.primary_goals?.join(', ')}</div>
          <div><span className="font-medium">Key Metrics:</span> {values.key_metrics_to_track?.join(', ')}</div>
          <div><span className="font-medium">Budget:</span> {values.monthly_budget_range}</div>
          <div><span className="font-medium">Posting Frequency:</span> {values.posting_frequency}</div>
          <div><span className="font-medium">Preferred Content Types:</span> {values.preferred_content_types?.join(', ')}</div>
          <div><span className="font-medium">Content Themes:</span> {values.content_themes?.join(', ')}</div>
          <div><span className="font-medium">Competitors:</span> {values.main_competitors}</div>
          <div><span className="font-medium">Market Position:</span> {values.market_position}</div>
          <div><span className="font-medium">Products/Services:</span> {values.products_or_services}</div>
          <div><span className="font-medium">Launch Dates:</span> {values.important_launch_dates}</div>
          <div><span className="font-medium">Promotions/Campaigns:</span> {values.planned_promotions_or_campaigns}</div>
          <div><span className="font-medium">Top Content Types:</span> {values.top_performing_content_types?.join(', ')}</div>
          <div><span className="font-medium">Best Time to Post:</span> {values.best_time_to_post?.join(', ')}</div>
          <div><span className="font-medium">Successful Campaigns:</span> {values.successful_campaigns}</div>
          <div><span className="font-medium">Hashtags:</span> {values.hashtags_that_work_well}</div>
          <div><span className="font-medium">Customer Pain Points:</span> {values.customer_pain_points}</div>
          <div><span className="font-medium">Customer Journey:</span> {values.typical_customer_journey}</div>
          <div><span className="font-medium">Automation Level:</span> {values.automation_level}</div>
        </div>
        <div className="mt-4">
          <h4 className="font-semibold mb-2 text-primary">Platform-Specific Tone</h4>
          <ul className="text-sm">
            {PLATFORMS.map((platform) => (
              <li key={platform}><span className="font-medium">{platform}:</span> {values.platform_specific_tone?.[platform]}</li>
            ))}
          </ul>
        </div>
      </div>
      <div className="text-center mt-6">
        <p className="text-gray-700">If everything looks good, click <span className="font-semibold text-primary">Submit</span> to finish onboarding.</p>
      </div>
    </div>
  )
}

export default Step10ReviewSubmit 