from supabase import create_client, Client
from app.core.config import settings


class SupabaseManager:
    def __init__(self):
        self.client: Client = create_client(
            settings.SUPABASE_URL, 
            settings.SUPABASE_ANON_KEY
        )
        self.admin_client: Client = create_client(
            settings.SUPABASE_URL, 
            settings.SUPABASE_SERVICE_ROLE_KEY
        )
    
    def get_client(self) -> Client:
        return self.client
    
    def get_admin_client(self) -> Client:
        return self.admin_client
    
    async def get_user_by_id(self, user_id: str):
        """Get user profile from Supabase auth.users"""
        try:
            response = self.admin_client.auth.admin.get_user_by_id(user_id)
            return response.user
        except Exception as e:
            print(f"Error getting user: {e}")
            return None
    
    async def create_user_profile(self, user_id: str, profile_data: dict):
        """Create user profile in profiles table"""
        try:
            profile_data["id"] = user_id
            response = self.client.table("profiles").insert(profile_data).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error creating user profile: {e}")
            return None
    
    async def get_user_profile(self, user_id: str):
        """Get user profile from profiles table"""
        try:
            response = self.client.table("profiles").select("*").eq("id", user_id).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error getting user profile: {e}")
            return None
    
    async def update_user_profile(self, user_id: str, profile_data: dict):
        """Update user profile in profiles table"""
        try:
            print(f"Updating profile for user {user_id}")
            print(f"Profile data: {profile_data}")
            
            # First check if profile exists
            existing_profile = await self.get_user_profile(user_id)
            if not existing_profile:
                print(f"Profile doesn't exist for user {user_id}, creating new profile")
                return await self.create_user_profile(user_id, profile_data)
            
            # Use admin client with RLS bypass for profile updates
            response = self.admin_client.table("profiles").update(profile_data).eq("id", user_id).execute()
            print(f"Update response: {response}")
            
            if response.data:
                print(f"Profile updated successfully: {response.data[0]}")
                return response.data[0]
            else:
                print("No data returned from update")
                # Try to get the profile to see if it was actually updated
                updated_profile = await self.get_user_profile(user_id)
                if updated_profile:
                    print("Profile was updated but response.data is empty")
                    return updated_profile
                return None
        except Exception as e:
            print(f"Error updating user profile: {e}")
            print(f"Error type: {type(e)}")
            import traceback
            traceback.print_exc()
            return None


# Global instance
supabase_manager = SupabaseManager() 