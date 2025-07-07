-- Create profiles table for user onboarding data
CREATE TABLE IF NOT EXISTS profiles (
    id UUID REFERENCES auth.users(id) ON DELETE CASCADE PRIMARY KEY,
    full_name TEXT,
    company_name TEXT,
    industry TEXT,
    business_size TEXT,
    website TEXT,
    phone TEXT,
    address TEXT,
    onboarding_completed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    -- Onboarding fields
    business_name TEXT,
    business_type TEXT,
    business_description TEXT,
    target_audience TEXT[],
    unique_value_proposition TEXT,
    brand_voice TEXT,
    brand_tone TEXT,
    website_url TEXT,
    phone_number TEXT,
    street_address TEXT,
    city TEXT,
    state TEXT,
    country TEXT,
    timezone TEXT,
    social_media_platforms TEXT[],
    primary_goals TEXT[],
    key_metrics_to_track TEXT[],
    monthly_budget_range TEXT,
    posting_frequency TEXT,
    preferred_content_types TEXT[],
    content_themes TEXT[],
    main_competitors TEXT,
    market_position TEXT,
    products_or_services TEXT,
    important_launch_dates TEXT,
    planned_promotions_or_campaigns TEXT,
    top_performing_content_types TEXT[],
    best_time_to_post TEXT[],
    successful_campaigns TEXT,
    hashtags_that_work_well TEXT,
    customer_pain_points TEXT,
    typical_customer_journey TEXT,
    automation_level TEXT,
    platform_specific_tone JSONB
);

-- Enable Row Level Security
ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;

-- Create policy to allow users to read their own profile
CREATE POLICY "Users can view own profile" ON profiles
    FOR SELECT USING (auth.uid() = id);

-- Create policy to allow users to update their own profile
CREATE POLICY "Users can update own profile" ON profiles
    FOR UPDATE USING (auth.uid() = id);

-- Create policy to allow users to insert their own profile
CREATE POLICY "Users can insert own profile" ON profiles
    FOR INSERT WITH CHECK (auth.uid() = id);

-- Create function to automatically create profile on user signup
CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO public.profiles (id, full_name, created_at, updated_at)
    VALUES (NEW.id, NEW.raw_user_meta_data->>'full_name', NOW(), NOW());
    RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Create trigger to automatically create profile
DROP TRIGGER IF EXISTS on_auth_user_created ON auth.users;
CREATE TRIGGER on_auth_user_created
    AFTER INSERT ON auth.users
    FOR EACH ROW EXECUTE FUNCTION public.handle_new_user(); 