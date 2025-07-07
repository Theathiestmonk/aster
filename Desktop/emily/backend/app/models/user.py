from typing import Optional, List, Dict
from pydantic import BaseModel, EmailStr
from datetime import datetime


class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None


class UserInDB(UserBase):
    id: str
    is_active: bool = True
    is_verified: bool = False
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True


class User(UserInDB):
    pass


class UserProfile(BaseModel):
    id: str
    full_name: Optional[str] = None
    company_name: Optional[str] = None
    industry: Optional[str] = None
    business_size: Optional[str] = None
    website: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    onboarding_completed: bool = False
    created_at: str
    updated_at: str
    business_name: Optional[str] = None
    business_type: Optional[str] = None
    business_description: Optional[str] = None
    target_audience: Optional[List[str]] = None
    unique_value_proposition: Optional[str] = None
    brand_voice: Optional[str] = None
    brand_tone: Optional[str] = None
    website_url: Optional[str] = None
    phone_number: Optional[str] = None
    street_address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    timezone: Optional[str] = None
    social_media_platforms: Optional[List[str]] = None
    primary_goals: Optional[List[str]] = None
    key_metrics_to_track: Optional[List[str]] = None
    monthly_budget_range: Optional[str] = None
    posting_frequency: Optional[str] = None
    preferred_content_types: Optional[List[str]] = None
    content_themes: Optional[List[str]] = None
    main_competitors: Optional[str] = None
    market_position: Optional[str] = None
    products_or_services: Optional[str] = None
    important_launch_dates: Optional[str] = None
    planned_promotions_or_campaigns: Optional[str] = None
    top_performing_content_types: Optional[List[str]] = None
    best_time_to_post: Optional[List[str]] = None
    successful_campaigns: Optional[str] = None
    hashtags_that_work_well: Optional[str] = None
    customer_pain_points: Optional[str] = None
    typical_customer_journey: Optional[str] = None
    automation_level: Optional[str] = None
    platform_specific_tone: Optional[Dict[str, str]] = None

    class Config:
        from_attributes = True


class OnboardingData(BaseModel):
    # Basic Business Information
    business_name: str
    business_type: str  # Ecommerce, Service, Restaurant, SaaS, B2B, B2C
    industry: str  # Technology, Retail, Education, Healthcare, Fashion, Food, Travel, Other
    business_description: str
    target_audience: List[str]  # Multiple segments
    unique_value_proposition: str
    
    # Brand Information
    brand_voice: str  # Professional, Casual, Friendly, Bold, Playful
    brand_tone: str  # Formal, Informal, Humorous, Inspirational, Neutral
    
    # Contact Information
    website_url: Optional[str] = None
    phone_number: str
    street_address: str
    city: str
    state: str
    country: str
    timezone: str
    
    # Social Media & Marketing
    social_media_platforms: List[str]
    primary_goals: List[str]
    key_metrics_to_track: List[str]
    monthly_budget_range: str
    posting_frequency: str
    preferred_content_types: List[str]
    content_themes: List[str]
    
    # Competition & Market
    main_competitors: str
    market_position: str  # Leader, Challenger, Niche, New Entrant
    products_or_services: str
    
    # Campaign Planning
    important_launch_dates: Optional[str] = None
    planned_promotions_or_campaigns: str
    top_performing_content_types: List[str]
    best_time_to_post: List[str]
    successful_campaigns: str
    hashtags_that_work_well: str
    
    # Customer Understanding
    customer_pain_points: str
    typical_customer_journey: str
    
    # Automation Preferences
    automation_level: str  # Full Auto, Suggestions Only, Manual Approval
    
    # Platform-Specific Tone
    platform_specific_tone: Dict[str, str]  # platform: tone mapping 