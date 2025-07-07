from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.core.config import settings
from app.core.supabase import supabase_manager
from app.models.user import UserCreate, User


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:
    def __init__(self):
        self.pwd_context = pwd_context
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(plain_password, hashed_password)
    
    def get_password_hash(self, password: str) -> str:
        return self.pwd_context.hash(password)
    
    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return encoded_jwt
    
    def verify_token(self, token: str) -> Optional[str]:
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            user_id: str = payload.get("sub")
            if user_id is None:
                return None
            return user_id
        except JWTError:
            return None
    
    async def register_user(self, user_data: UserCreate) -> Optional[User]:
        """Register a new user using Supabase Auth"""
        try:
            print(f"Attempting to register user: {user_data.email}")
            
            # Create user in Supabase Auth
            response = supabase_manager.get_client().auth.sign_up({
                "email": user_data.email,
                "password": user_data.password,
                "options": {
                    "data": {
                        "full_name": user_data.full_name
                    }
                }
            })
            
            print(f"Supabase signup response: {response}")
            
            if response.user:
                print(f"User created in Supabase: {response.user.id}")
                
                # Create profile in profiles table
                profile_data = {
                    "full_name": user_data.full_name,
                    "onboarding_completed": False,
                    "created_at": str(response.user.created_at),
                    "updated_at": str(response.user.updated_at)
                }
                
                profile_result = await supabase_manager.create_user_profile(response.user.id, profile_data)
                print(f"Profile creation result: {profile_result}")
                
                user = User(
                    id=response.user.id,
                    email=response.user.email,
                    full_name=user_data.full_name,
                    is_active=response.user.email_confirmed_at is not None,
                    is_verified=response.user.email_confirmed_at is not None,
                    created_at=str(response.user.created_at),
                    updated_at=str(response.user.updated_at)
                )
                print(f"Registered user object: {user}")
                return user
            
            print("No user returned from Supabase signup")
            return None
        except Exception as e:
            print(f"Error registering user: {e}")
            print(f"Error type: {type(e)}")
            print(f"Error details: {str(e)}")
            import traceback
            traceback.print_exc()
            return None
    
    async def authenticate_user(self, email: str, password: str) -> Optional[dict]:
        """Authenticate user using Supabase Auth and return user with token"""
        try:
            print(f"Attempting to authenticate user: {email}")
            response = supabase_manager.get_client().auth.sign_in_with_password({
                "email": email,
                "password": password
            })
            
            print(f"Supabase auth response: {response}")
            
            if response.user and response.session:
                user = User(
                    id=response.user.id,
                    email=response.user.email,
                    full_name=response.user.user_metadata.get("full_name"),
                    is_active=response.user.email_confirmed_at is not None,
                    is_verified=response.user.email_confirmed_at is not None,
                    created_at=str(response.user.created_at),
                    updated_at=str(response.user.updated_at)
                )
                print(f"Authenticated user: {user}")
                return {
                    "user": user,
                    "access_token": response.session.access_token,
                    "refresh_token": response.session.refresh_token
                }
            
            print("No user or session returned from Supabase auth")
            return None
        except Exception as e:
            print(f"Error authenticating user: {e}")
            print(f"Error type: {type(e)}")
            print(f"Error details: {str(e)}")
            return None
    
    async def get_current_user(self, token: str) -> Optional[User]:
        """Get current user from Supabase JWT token"""
        try:
            # Try using the service role client to get user from token
            user = supabase_manager.get_admin_client().auth.get_user(token)
            if user and user.user:
                return User(
                    id=user.user.id,
                    email=user.user.email,
                    full_name=user.user.user_metadata.get("full_name", ""),
                    is_active=user.user.email_confirmed_at is not None,
                    is_verified=user.user.email_confirmed_at is not None,
                    created_at=str(user.user.created_at) if user.user.created_at else "",
                    updated_at=str(user.user.updated_at) if user.user.updated_at else ""
                )
            return None
        except Exception as e:
            print(f"Error getting current user from Supabase token: {e}")
            print(f"Token preview: {token[:20]}...")
            import traceback
            traceback.print_exc()
            return None


auth_service = AuthService() 