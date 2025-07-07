from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import Optional
from app.api.auth import get_current_user
from app.models.user import User
from app.core.supabase import supabase_manager
import json

router = APIRouter(prefix="/chat", tags=["chatbot"])


class ChatMessage(BaseModel):
    message: str


class ChatResponse(BaseModel):
    response: str
    user_profile: Optional[dict] = None


@router.post("/send", response_model=ChatResponse)
async def send_message(
    chat_message: ChatMessage,
    current_user: User = Depends(get_current_user)
):
    """Send a message to the chatbot and get a personalized response"""
    try:
        print(f"Chat message from user {current_user.email}: {chat_message.message}")
        
        # Get user's profile data
        user_profile = await supabase_manager.get_user_profile(current_user.id)
        print(f"User profile: {user_profile}")
        
        if not user_profile:
            return ChatResponse(
                response="I don't have your business information yet. Please complete your onboarding first.",
                user_profile=None
            )
        
        # Simple response logic based on the message
        message_lower = chat_message.message.lower()
        
        if "business name" in message_lower or "company name" in message_lower:
            business_name = user_profile.get("business_name", "your business")
            response = f"Your business name is {business_name}."
        
        elif "what is my business" in message_lower or "tell me about my business" in message_lower:
            business_name = user_profile.get("business_name", "your business")
            business_type = user_profile.get("business_type", "business")
            industry = user_profile.get("industry", "industry")
            response = f"Your business is {business_name}, which is a {business_type} in the {industry} industry."
        
        elif "industry" in message_lower:
            industry = user_profile.get("industry", "your industry")
            response = f"You operate in the {industry} industry."
        
        elif "target audience" in message_lower or "audience" in message_lower:
            target_audience = user_profile.get("target_audience", [])
            if target_audience:
                audience_str = ", ".join(target_audience)
                response = f"Your target audience includes: {audience_str}."
            else:
                response = "I don't have information about your target audience yet."
        
        elif "help" in message_lower:
            response = """I can help you with information about your business! Try asking me:
- What is my business name?
- Tell me about my business
- What industry am I in?
- Who is my target audience?
- What are my business goals?"""
        
        else:
            response = f"I understand you said: '{chat_message.message}'. I'm here to help with information about your business. Try asking about your business name, industry, or target audience!"
        
        return ChatResponse(
            response=response,
            user_profile=user_profile
        )
        
    except Exception as e:
        print(f"Chat error: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Chat error: {str(e)}"
        ) 