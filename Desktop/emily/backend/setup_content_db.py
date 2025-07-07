#!/usr/bin/env python3
"""
Content Database Setup Script
This script sets up the content management database schema and optionally adds sample data.
"""

import os
import sys
import asyncio
from pathlib import Path

# Add the backend directory to the Python path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

from app.core.supabase import supabase_manager
from app.core.config import settings

async def setup_content_schema():
    """Set up the content management database schema"""
    print("Setting up content management database schema...")
    
    try:
        # Read the content schema SQL file
        schema_file = backend_dir / "content_schema.sql"
        with open(schema_file, 'r') as f:
            schema_sql = f.read()
        
        # Execute the schema creation
        # Note: This would typically be done through Supabase migrations
        # For now, we'll just print the schema for manual execution
        print("Content schema SQL:")
        print("=" * 50)
        print(schema_sql)
        print("=" * 50)
        print("\nPlease execute this SQL in your Supabase SQL editor.")
        
        return True
        
    except Exception as e:
        print(f"Error setting up schema: {e}")
        return False

async def create_sample_data(user_id: str):
    """Create sample content data for a specific user"""
    print(f"Creating sample data for user: {user_id}")
    
    try:
        # Sample tasks
        sample_tasks = [
            {
                "user_id": user_id,
                "title": "Create LinkedIn post about AI trends",
                "description": "Write an engaging post about the latest AI trends in marketing",
                "status": "completed",
                "priority": "high",
                "due_date": "2024-01-15",
                "assigned_by": "Ravi"
            },
            {
                "user_id": user_id,
                "title": "Draft blog post on content strategy",
                "description": "Create a comprehensive blog post about content marketing strategies",
                "status": "working",
                "priority": "medium",
                "due_date": "2024-01-20",
                "assigned_by": "Deep"
            },
            {
                "user_id": user_id,
                "title": "Write Instagram captions for product launch",
                "description": "Create engaging captions for the new product launch campaign",
                "status": "pending",
                "priority": "high",
                "due_date": "2024-01-18",
                "assigned_by": "Ravi"
            }
        ]
        
        # Sample social media posts
        sample_posts = [
            {
                "user_id": user_id,
                "title": "AI in Marketing: The Future is Now",
                "content": "Discover how artificial intelligence is revolutionizing the marketing landscape...",
                "platform": "linkedin",
                "status": "published",
                "engagement_likes": 45,
                "engagement_shares": 12,
                "engagement_comments": 8
            },
            {
                "user_id": user_id,
                "title": "5 Content Marketing Tips That Actually Work",
                "content": "Stop wasting time on strategies that don't work. Here are 5 proven tips...",
                "platform": "facebook",
                "status": "published",
                "engagement_likes": 23,
                "engagement_shares": 5,
                "engagement_comments": 3
            },
            {
                "user_id": user_id,
                "title": "Behind the Scenes: Our Creative Process",
                "content": "Ever wondered how we create compelling content? Here's a peek...",
                "platform": "instagram",
                "status": "scheduled"
            }
        ]
        
        # Sample blogs
        sample_blogs = [
            {
                "user_id": user_id,
                "title": "The Complete Guide to Content Marketing in 2024",
                "excerpt": "Learn the latest strategies and trends in content marketing...",
                "content": "Content marketing has evolved significantly over the past few years...",
                "status": "published",
                "read_time": 8,
                "tags": ["content marketing", "strategy", "2024"]
            },
            {
                "user_id": user_id,
                "title": "How to Write Engaging Social Media Posts",
                "excerpt": "Master the art of creating posts that drive engagement...",
                "content": "Creating engaging social media content requires more than just...",
                "status": "draft",
                "read_time": 5,
                "tags": ["social media", "engagement", "writing"]
            }
        ]
        
        # Sample content requests
        sample_requests = [
            {
                "user_id": user_id,
                "type": "blog",
                "title": "SEO Best Practices for 2024",
                "description": "Need a comprehensive blog post about SEO best practices",
                "priority": "high",
                "status": "pending",
                "requested_by": "Deep"
            },
            {
                "user_id": user_id,
                "type": "post",
                "title": "Product Launch Announcement",
                "description": "Create a series of social media posts for product launch",
                "priority": "high",
                "status": "approved",
                "requested_by": "Ravi"
            },
            {
                "user_id": user_id,
                "type": "tweet",
                "title": "Industry Insights Thread",
                "description": "Create a Twitter thread about industry insights",
                "priority": "medium",
                "status": "pending",
                "requested_by": "Deep"
            }
        ]
        
        # Insert sample data
        print("Inserting sample tasks...")
        for task in sample_tasks:
            supabase_manager.client.table("content_tasks").insert(task).execute()
        
        print("Inserting sample posts...")
        for post in sample_posts:
            supabase_manager.client.table("social_media_posts").insert(post).execute()
        
        print("Inserting sample blogs...")
        for blog in sample_blogs:
            supabase_manager.client.table("blogs").insert(blog).execute()
        
        print("Inserting sample requests...")
        for request in sample_requests:
            supabase_manager.client.table("content_requests").insert(request).execute()
        
        print("Sample data created successfully!")
        return True
        
    except Exception as e:
        print(f"Error creating sample data: {e}")
        return False

async def main():
    """Main function to run the setup"""
    print("Content Database Setup")
    print("=" * 30)
    
    # Check if user wants to create sample data
    create_sample = input("Do you want to create sample data? (y/n): ").lower().strip()
    
    if create_sample == 'y':
        user_id = input("Enter the user ID for sample data: ").strip()
        if not user_id:
            print("User ID is required for sample data creation.")
            return
        
        # Create sample data
        success = await create_sample_data(user_id)
        if success:
            print("Setup completed successfully!")
        else:
            print("Setup failed. Please check the error messages above.")
    else:
        # Just show the schema
        await setup_content_schema()
        print("Schema setup instructions displayed above.")

if __name__ == "__main__":
    asyncio.run(main()) 