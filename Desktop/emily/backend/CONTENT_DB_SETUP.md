# Content Database Setup Guide

## Overview
This guide will help you set up the content management database tables for the Content Writer Dashboard.

## Step 1: Execute the Schema SQL

1. Go to your Supabase dashboard
2. Navigate to the SQL Editor
3. Copy and paste the contents of `content_schema.sql` into the editor
4. Execute the SQL to create the tables

## Step 2: Verify Tables Created

After executing the SQL, you should see these tables in your Supabase dashboard:

- `content_tasks` - Task management
- `social_media_posts` - Social media content
- `blogs` - Blog posts
- `content_requests` - Content requests
- `content_creation_history` - Content creation tracking

## Step 3: Test the Setup

1. Start your backend server:
   ```bash
   cd backend
   python -m uvicorn app.main:app --reload
   ```

2. Start your frontend:
   ```bash
   cd frontend
   npm run dev
   ```

3. Navigate to the Content Writer Dashboard
4. The dashboard should load with mock data (since no real data exists yet)

## Step 4: Create Sample Data (Optional)

If you want to see real data in the dashboard, you can create sample data:

1. First, get your user ID from the Supabase auth.users table
2. Run the setup script:
   ```bash
   cd backend
   python setup_content_db.py
   ```
3. Follow the prompts to create sample data

## Troubleshooting

### Error: "Key (user_id)=(...) is not present in table 'users'"

This error occurs when trying to insert data with a user ID that doesn't exist in the `auth.users` table.

**Solution:**
1. Make sure you have a user account created in your Supabase auth
2. Use the correct user ID from the `auth.users` table
3. The user ID should match the one you're logged in with

### Tables Not Created

If the tables aren't created after running the SQL:

1. Check for any SQL syntax errors in the Supabase SQL editor
2. Make sure you have the necessary permissions in your Supabase project
3. Try running the SQL statements one by one

### Dashboard Shows No Data

If the dashboard shows empty panels:

1. Check the browser console for any API errors
2. Verify that the backend is running and accessible
3. Check that the API endpoints are working by testing them directly
4. The dashboard will show mock data if the backend is not available

## API Endpoints

Once set up, these endpoints will be available:

- `GET /api/v1/content/tasks` - Get user tasks
- `POST /api/v1/content/tasks` - Create new task
- `GET /api/v1/content/posts` - Get social media posts
- `POST /api/v1/content/posts` - Create new post
- `GET /api/v1/content/blogs` - Get blogs
- `POST /api/v1/content/blogs` - Create new blog
- `GET /api/v1/content/requests` - Get content requests
- `POST /api/v1/content/requests` - Create new request
- `POST /api/v1/content/history` - Track content creation
- `GET /api/v1/content/stats` - Get content statistics

## Next Steps

After setup:

1. Test creating content through the dashboard
2. Verify that data is being saved to the database
3. Test the content creation form
4. Explore the different content types and features

## Support

If you encounter any issues:

1. Check the browser console for frontend errors
2. Check the backend logs for API errors
3. Verify your Supabase configuration
4. Ensure all environment variables are set correctly 