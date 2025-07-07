-- =====================================================
-- Content Management Database Schema
-- For AI Marketing Agent System
-- =====================================================

-- Enable UUID extension if not already enabled
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- =====================================================
-- CONTENT TASKS TABLE
-- =====================================================
CREATE TABLE IF NOT EXISTS content_tasks (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE NOT NULL,
    title TEXT NOT NULL,
    description TEXT,
    status TEXT CHECK (status IN ('pending', 'working', 'completed')) DEFAULT 'pending',
    priority TEXT CHECK (priority IN ('low', 'medium', 'high')) DEFAULT 'medium',
    due_date DATE,
    assigned_by TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- =====================================================
-- SOCIAL MEDIA POSTS TABLE
-- =====================================================
CREATE TABLE IF NOT EXISTS social_media_posts (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE NOT NULL,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    platform TEXT CHECK (platform IN ('facebook', 'instagram', 'linkedin', 'twitter')) NOT NULL,
    status TEXT CHECK (status IN ('draft', 'published', 'scheduled')) DEFAULT 'draft',
    scheduled_date TIMESTAMP WITH TIME ZONE,
    published_date TIMESTAMP WITH TIME ZONE,
    engagement_likes INTEGER DEFAULT 0,
    engagement_shares INTEGER DEFAULT 0,
    engagement_comments INTEGER DEFAULT 0,
    tags TEXT[],
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- =====================================================
-- BLOGS TABLE
-- =====================================================
CREATE TABLE IF NOT EXISTS blogs (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE NOT NULL,
    title TEXT NOT NULL,
    excerpt TEXT,
    content TEXT NOT NULL,
    status TEXT CHECK (status IN ('draft', 'published', 'review')) DEFAULT 'draft',
    read_time INTEGER,
    tags TEXT[],
    published_date TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- =====================================================
-- CONTENT REQUESTS TABLE
-- =====================================================
CREATE TABLE IF NOT EXISTS content_requests (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE NOT NULL,
    type TEXT CHECK (type IN ('post', 'blog', 'article', 'tweet', 'email')) NOT NULL,
    title TEXT NOT NULL,
    description TEXT,
    priority TEXT CHECK (priority IN ('low', 'medium', 'high')) DEFAULT 'medium',
    status TEXT CHECK (status IN ('pending', 'approved', 'rejected')) DEFAULT 'pending',
    requested_by TEXT,
    requested_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    approved_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- =====================================================
-- CONTENT CREATION HISTORY TABLE
-- =====================================================
CREATE TABLE IF NOT EXISTS content_creation_history (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE NOT NULL,
    content_type TEXT NOT NULL,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    description TEXT,
    platform TEXT,
    tags TEXT[],
    status TEXT DEFAULT 'created',
    agent_used TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- =====================================================
-- ENABLE ROW LEVEL SECURITY (RLS)
-- =====================================================
ALTER TABLE content_tasks ENABLE ROW LEVEL SECURITY;
ALTER TABLE social_media_posts ENABLE ROW LEVEL SECURITY;
ALTER TABLE blogs ENABLE ROW LEVEL SECURITY;
ALTER TABLE content_requests ENABLE ROW LEVEL SECURITY;
ALTER TABLE content_creation_history ENABLE ROW LEVEL SECURITY;

-- =====================================================
-- ROW LEVEL SECURITY POLICIES
-- =====================================================

-- Content Tasks Policies
CREATE POLICY "Users can view own tasks" ON content_tasks
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own tasks" ON content_tasks
    FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own tasks" ON content_tasks
    FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY "Users can delete own tasks" ON content_tasks
    FOR DELETE USING (auth.uid() = user_id);

-- Social Media Posts Policies
CREATE POLICY "Users can view own posts" ON social_media_posts
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own posts" ON social_media_posts
    FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own posts" ON social_media_posts
    FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY "Users can delete own posts" ON social_media_posts
    FOR DELETE USING (auth.uid() = user_id);

-- Blogs Policies
CREATE POLICY "Users can view own blogs" ON blogs
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own blogs" ON blogs
    FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own blogs" ON blogs
    FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY "Users can delete own blogs" ON blogs
    FOR DELETE USING (auth.uid() = user_id);

-- Content Requests Policies
CREATE POLICY "Users can view own requests" ON content_requests
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own requests" ON content_requests
    FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own requests" ON content_requests
    FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY "Users can delete own requests" ON content_requests
    FOR DELETE USING (auth.uid() = user_id);

-- Content Creation History Policies
CREATE POLICY "Users can view own history" ON content_creation_history
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own history" ON content_creation_history
    FOR INSERT WITH CHECK (auth.uid() = user_id);

-- =====================================================
-- INDEXES FOR PERFORMANCE
-- =====================================================

-- Content Tasks Indexes
CREATE INDEX IF NOT EXISTS idx_content_tasks_user_id ON content_tasks(user_id);
CREATE INDEX IF NOT EXISTS idx_content_tasks_status ON content_tasks(status);
CREATE INDEX IF NOT EXISTS idx_content_tasks_priority ON content_tasks(priority);
CREATE INDEX IF NOT EXISTS idx_content_tasks_due_date ON content_tasks(due_date);
CREATE INDEX IF NOT EXISTS idx_content_tasks_created_at ON content_tasks(created_at);

-- Social Media Posts Indexes
CREATE INDEX IF NOT EXISTS idx_social_media_posts_user_id ON social_media_posts(user_id);
CREATE INDEX IF NOT EXISTS idx_social_media_posts_platform ON social_media_posts(platform);
CREATE INDEX IF NOT EXISTS idx_social_media_posts_status ON social_media_posts(status);
CREATE INDEX IF NOT EXISTS idx_social_media_posts_created_at ON social_media_posts(created_at);
CREATE INDEX IF NOT EXISTS idx_social_media_posts_scheduled_date ON social_media_posts(scheduled_date);

-- Blogs Indexes
CREATE INDEX IF NOT EXISTS idx_blogs_user_id ON blogs(user_id);
CREATE INDEX IF NOT EXISTS idx_blogs_status ON blogs(status);
CREATE INDEX IF NOT EXISTS idx_blogs_created_at ON blogs(created_at);
CREATE INDEX IF NOT EXISTS idx_blogs_published_date ON blogs(published_date);

-- Content Requests Indexes
CREATE INDEX IF NOT EXISTS idx_content_requests_user_id ON content_requests(user_id);
CREATE INDEX IF NOT EXISTS idx_content_requests_status ON content_requests(status);
CREATE INDEX IF NOT EXISTS idx_content_requests_type ON content_requests(type);
CREATE INDEX IF NOT EXISTS idx_content_requests_priority ON content_requests(priority);
CREATE INDEX IF NOT EXISTS idx_content_requests_created_at ON content_requests(created_at);

-- Content Creation History Indexes
CREATE INDEX IF NOT EXISTS idx_content_creation_history_user_id ON content_creation_history(user_id);
CREATE INDEX IF NOT EXISTS idx_content_creation_history_content_type ON content_creation_history(content_type);
CREATE INDEX IF NOT EXISTS idx_content_creation_history_created_at ON content_creation_history(created_at);

-- =====================================================
-- TRIGGERS FOR UPDATED_AT TIMESTAMP
-- =====================================================

-- Function to update the updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Triggers for updated_at
CREATE TRIGGER update_content_tasks_updated_at 
    BEFORE UPDATE ON content_tasks 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_social_media_posts_updated_at 
    BEFORE UPDATE ON social_media_posts 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_blogs_updated_at 
    BEFORE UPDATE ON blogs 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_content_requests_updated_at 
    BEFORE UPDATE ON content_requests 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- =====================================================
-- HELPER FUNCTIONS
-- =====================================================

-- Function to get content statistics for a user
CREATE OR REPLACE FUNCTION get_user_content_stats(user_uuid UUID)
RETURNS JSON AS $$
DECLARE
    result JSON;
BEGIN
    SELECT json_build_object(
        'tasks', json_build_object(
            'total', (SELECT COUNT(*) FROM content_tasks WHERE user_id = user_uuid),
            'completed', (SELECT COUNT(*) FROM content_tasks WHERE user_id = user_uuid AND status = 'completed'),
            'pending', (SELECT COUNT(*) FROM content_tasks WHERE user_id = user_uuid AND status = 'pending'),
            'working', (SELECT COUNT(*) FROM content_tasks WHERE user_id = user_uuid AND status = 'working')
        ),
        'posts', json_build_object(
            'total', (SELECT COUNT(*) FROM social_media_posts WHERE user_id = user_uuid),
            'published', (SELECT COUNT(*) FROM social_media_posts WHERE user_id = user_uuid AND status = 'published'),
            'draft', (SELECT COUNT(*) FROM social_media_posts WHERE user_id = user_uuid AND status = 'draft'),
            'scheduled', (SELECT COUNT(*) FROM social_media_posts WHERE user_id = user_uuid AND status = 'scheduled')
        ),
        'blogs', json_build_object(
            'total', (SELECT COUNT(*) FROM blogs WHERE user_id = user_uuid),
            'published', (SELECT COUNT(*) FROM blogs WHERE user_id = user_uuid AND status = 'published'),
            'draft', (SELECT COUNT(*) FROM blogs WHERE user_id = user_uuid AND status = 'draft'),
            'review', (SELECT COUNT(*) FROM blogs WHERE user_id = user_uuid AND status = 'review')
        ),
        'requests', json_build_object(
            'total', (SELECT COUNT(*) FROM content_requests WHERE user_id = user_uuid),
            'pending', (SELECT COUNT(*) FROM content_requests WHERE user_id = user_uuid AND status = 'pending'),
            'approved', (SELECT COUNT(*) FROM content_requests WHERE user_id = user_uuid AND status = 'approved'),
            'rejected', (SELECT COUNT(*) FROM content_requests WHERE user_id = user_uuid AND status = 'rejected')
        )
    ) INTO result;
    
    RETURN result;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- =====================================================
-- SAMPLE DATA (OPTIONAL - COMMENT OUT IF NOT NEEDED)
-- =====================================================

-- Uncomment the section below if you want to create sample data
-- Make sure to replace 'YOUR_USER_ID_HERE' with an actual user ID from auth.users

/*
-- Sample data will be created when users interact with the system
-- To create sample data manually, uncomment and modify the following:

-- INSERT INTO content_tasks (user_id, title, description, status, priority, due_date, assigned_by) VALUES
-- ('YOUR_USER_ID_HERE', 'Create LinkedIn post about AI trends', 'Write an engaging post about the latest AI trends in marketing', 'completed', 'high', '2024-01-15', 'Ravi'),
-- ('YOUR_USER_ID_HERE', 'Draft blog post on content strategy', 'Create a comprehensive blog post about content marketing strategies', 'working', 'medium', '2024-01-20', 'Deep'),
-- ('YOUR_USER_ID_HERE', 'Write Instagram captions for product launch', 'Create engaging captions for the new product launch campaign', 'pending', 'high', '2024-01-18', 'Ravi');

-- INSERT INTO social_media_posts (user_id, title, content, platform, status, engagement_likes, engagement_shares, engagement_comments) VALUES
-- ('YOUR_USER_ID_HERE', 'AI in Marketing: The Future is Now', 'Discover how artificial intelligence is revolutionizing the marketing landscape...', 'linkedin', 'published', 45, 12, 8),
-- ('YOUR_USER_ID_HERE', '5 Content Marketing Tips That Actually Work', 'Stop wasting time on strategies that don''t work. Here are 5 proven tips...', 'facebook', 'published', 23, 5, 3),
-- ('YOUR_USER_ID_HERE', 'Behind the Scenes: Our Creative Process', 'Ever wondered how we create compelling content? Here''s a peek...', 'instagram', 'scheduled', 0, 0, 0);

-- INSERT INTO blogs (user_id, title, excerpt, content, status, read_time, tags) VALUES
-- ('YOUR_USER_ID_HERE', 'The Complete Guide to Content Marketing in 2024', 'Learn the latest strategies and trends in content marketing...', 'Content marketing has evolved significantly over the past few years...', 'published', 8, ARRAY['content marketing', 'strategy', '2024']),
-- ('YOUR_USER_ID_HERE', 'How to Write Engaging Social Media Posts', 'Master the art of creating posts that drive engagement...', 'Creating engaging social media content requires more than just...', 'draft', 5, ARRAY['social media', 'engagement', 'writing']);

-- INSERT INTO content_requests (user_id, type, title, description, priority, status, requested_by) VALUES
-- ('YOUR_USER_ID_HERE', 'blog', 'SEO Best Practices for 2024', 'Need a comprehensive blog post about SEO best practices', 'high', 'pending', 'Deep'),
-- ('YOUR_USER_ID_HERE', 'post', 'Product Launch Announcement', 'Create a series of social media posts for product launch', 'high', 'approved', 'Ravi'),
-- ('YOUR_USER_ID_HERE', 'tweet', 'Industry Insights Thread', 'Create a Twitter thread about industry insights', 'medium', 'pending', 'Deep');
*/

-- =====================================================
-- VERIFICATION QUERIES
-- =====================================================

-- Uncomment to verify the setup (run these after executing the schema)

/*
-- Check if tables were created
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public' 
AND table_name IN ('content_tasks', 'social_media_posts', 'blogs', 'content_requests', 'content_creation_history');

-- Check if RLS is enabled
SELECT schemaname, tablename, rowsecurity 
FROM pg_tables 
WHERE tablename IN ('content_tasks', 'social_media_posts', 'blogs', 'content_requests', 'content_creation_history');

-- Check if policies were created
SELECT schemaname, tablename, policyname, permissive, roles, cmd, qual 
FROM pg_policies 
WHERE tablename IN ('content_tasks', 'social_media_posts', 'blogs', 'content_requests', 'content_creation_history');
*/

-- =====================================================
-- SCHEMA CREATION COMPLETE
-- =====================================================

-- This schema creates a complete content management system with:
-- - 5 main tables for different content types
-- - Row Level Security (RLS) policies for data protection
-- - Performance indexes for fast queries
-- - Automatic timestamp updates
-- - Helper functions for statistics
-- - Sample data templates (commented out)

-- After running this schema:
-- 1. Your content management system will be ready
-- 2. The Content Writer Dashboard will work with real data
-- 3. All API endpoints will be functional
-- 4. Data will be properly secured per user 