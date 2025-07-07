import asyncio
import os
from supabase import create_client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Supabase configuration
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

async def test_user_exists(email: str):
    """Test if a user exists and check their status"""
    try:
        print(f"Testing for user: {email}")
        print(f"Supabase URL: {SUPABASE_URL}")
        print(f"Service role key exists: {SUPABASE_SERVICE_ROLE_KEY is not None}")
        
        # Create admin client
        supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)
        
        # List all users
        users = supabase.auth.admin.list_users()
        
        print(f"Total users: {len(users)}")
        
        # Find the specific user
        user = None
        for u in users:
            print(f"User: {u.email}, Confirmed: {u.email_confirmed_at}")
            if u.email == email:
                user = u
                break
        
        if user:
            print(f"\nUser found: {user.email}")
            print(f"User ID: {user.id}")
            print(f"Email confirmed: {user.email_confirmed_at}")
            print(f"Created at: {user.created_at}")
            print(f"Last sign in: {user.last_sign_in_at}")
            print(f"User metadata: {user.user_metadata}")
            print(f"Is confirmed: {user.email_confirmed_at is not None}")
        else:
            print(f"\nUser with email {email} not found")
            
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    # Test with the email you're trying to login with
    email = "test@example.com"  # Change this to your actual email
    asyncio.run(test_user_exists(email)) 