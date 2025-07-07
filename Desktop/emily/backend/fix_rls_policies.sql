-- Add policy to allow service role to access all profiles
CREATE POLICY "Service role can access all profiles" ON profiles
    FOR ALL USING (auth.role() = 'service_role');

-- Add policy to allow service role to bypass RLS
CREATE POLICY "Service role bypass RLS" ON profiles
    FOR ALL USING (true);

-- Grant necessary permissions to service role
GRANT ALL ON profiles TO service_role; 