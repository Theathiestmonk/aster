from datetime import timedelta
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from app.core.config import settings
from app.services.auth import auth_service
from app.models.user import UserCreate, User, UserProfile, OnboardingData
from app.core.supabase import supabase_manager

router = APIRouter(prefix="/auth", tags=["authentication"])
security = HTTPBearer()


class LoginRequest(BaseModel):
    email: str
    password: str


@router.post("/register", response_model=dict)
async def register(user_data: UserCreate):
    """Register a new user"""
    try:
        user = await auth_service.register_user(user_data)
        if user:
            return {
                "message": "Registration successful! Please check your email and click the confirmation link to verify your account before logging in.",
                "user_id": user.id,
                "email_sent": True
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Registration failed. User might already exist."
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Registration error: {str(e)}"
        )


@router.post("/login", response_model=dict)
async def login(login_data: LoginRequest):
    """Login user and return Supabase access token"""
    try:
        print(f"Login attempt for email: {login_data.email}")
        auth_result = await auth_service.authenticate_user(login_data.email, login_data.password)
        print(f"Auth result: {auth_result}")
        
        if not auth_result:
            print("No auth result returned")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password"
            )
        
        user = auth_result["user"]
        print(f"User object: {user}")
        
        if not user.is_verified:
            print("User not verified")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Please check your email and click the confirmation link to verify your account before logging in."
            )
        
        response_data = {
            "access_token": auth_result["access_token"],
            "refresh_token": auth_result["refresh_token"],
            "token_type": "bearer",
            "user": {
                "id": user.id,
                "email": user.email,
                "full_name": user.full_name,
                "is_verified": user.is_verified
            }
        }
        print(f"Login successful, returning: {response_data}")
        return response_data
    except HTTPException:
        raise
    except Exception as e:
        print(f"Login error: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Login error: {str(e)}"
        )


async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> User:
    """Dependency to get current authenticated user"""
    token = credentials.credentials
    print(f"Validating token: {token[:20]}...")
    user = await auth_service.get_current_user(token)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    print(f"User validated: {user.email}")
    return user


@router.get("/me", response_model=User)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """Get current user information"""
    return current_user


@router.get("/profile", response_model=Optional[UserProfile])
async def get_user_profile(current_user: User = Depends(get_current_user)):
    """Get user profile information"""
    try:
        profile = await supabase_manager.get_user_profile(current_user.id)
        return profile
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching profile: {str(e)}"
        )


@router.post("/onboarding", response_model=dict)
async def complete_onboarding(
    onboarding_data: OnboardingData,
    current_user: User = Depends(get_current_user)
):
    """Complete user onboarding process"""
    try:
        from datetime import datetime
        
        print(f"Starting onboarding for user: {current_user.email}")
        print(f"User ID: {current_user.id}")
        
        # Prepare profile data with all onboarding information
        profile_data = {
            "business_name": onboarding_data.business_name,
            "business_type": onboarding_data.business_type,
            "industry": onboarding_data.industry,
            "business_description": onboarding_data.business_description,
            "target_audience": onboarding_data.target_audience,
            "unique_value_proposition": onboarding_data.unique_value_proposition,
            "brand_voice": onboarding_data.brand_voice,
            "brand_tone": onboarding_data.brand_tone,
            "website_url": onboarding_data.website_url,
            "phone_number": onboarding_data.phone_number,
            "street_address": onboarding_data.street_address,
            "city": onboarding_data.city,
            "state": onboarding_data.state,
            "country": onboarding_data.country,
            "timezone": onboarding_data.timezone,
            "social_media_platforms": onboarding_data.social_media_platforms,
            "primary_goals": onboarding_data.primary_goals,
            "key_metrics_to_track": onboarding_data.key_metrics_to_track,
            "monthly_budget_range": onboarding_data.monthly_budget_range,
            "posting_frequency": onboarding_data.posting_frequency,
            "preferred_content_types": onboarding_data.preferred_content_types,
            "content_themes": onboarding_data.content_themes,
            "main_competitors": onboarding_data.main_competitors,
            "market_position": onboarding_data.market_position,
            "products_or_services": onboarding_data.products_or_services,
            "important_launch_dates": onboarding_data.important_launch_dates,
            "planned_promotions_or_campaigns": onboarding_data.planned_promotions_or_campaigns,
            "top_performing_content_types": onboarding_data.top_performing_content_types,
            "best_time_to_post": onboarding_data.best_time_to_post,
            "successful_campaigns": onboarding_data.successful_campaigns,
            "hashtags_that_work_well": onboarding_data.hashtags_that_work_well,
            "customer_pain_points": onboarding_data.customer_pain_points,
            "typical_customer_journey": onboarding_data.typical_customer_journey,
            "automation_level": onboarding_data.automation_level,
            "platform_specific_tone": onboarding_data.platform_specific_tone,
            "onboarding_completed": True,
            "updated_at": datetime.utcnow().isoformat()
        }
        
        print(f"Profile data prepared, updating profile for user {current_user.id}")
        
        # Update profile in Supabase
        updated_profile = await supabase_manager.update_user_profile(
            current_user.id, profile_data
        )
        
        print(f"Profile update result: {updated_profile}")
        
        if updated_profile:
            # Here you would trigger the LangGraph workflow
            # For now, we'll just return success
            return {
                "message": "Onboarding completed successfully",
                "profile": updated_profile
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to update profile"
            )
    except HTTPException:
        raise
    except Exception as e:
        print(f"Onboarding error: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Onboarding error: {str(e)}"
        )


@router.post("/logout")
async def logout(current_user: User = Depends(get_current_user)):
    """Logout user (client should discard token)"""
    return {"message": "Successfully logged out"} 