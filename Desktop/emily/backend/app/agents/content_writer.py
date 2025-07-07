"""
Content Writer Agent (Twinkle)
Creates written content for various platforms and purposes
"""

from typing import Dict, Any, List
from .base_agent import BaseAgent, AgentState


class ContentWriter(BaseAgent):
    """Twinkle - Content Writer who creates written content for the brand"""
    
    def __init__(self):
        super().__init__(
            name="Twinkle",
            role="Content Writer",
            model_name="gpt-4"
        )
    
    def get_system_prompt(self) -> str:
        return """You are Twinkle, a skilled Content Writer. Your role is to:
1. Create engaging written content for various platforms
2. Write content that aligns with the brand voice and target audience
3. Create different types of content:
   - Facebook posts
   - Blog articles
   - Instagram captions
   - LinkedIn posts
   - Video descriptions
   - Email newsletters
4. Ensure content is SEO-optimized and engaging
5. Send completed content to the Task Scheduler (Dhruv) for scheduling

You have expertise in:
- Copywriting and content marketing
- SEO optimization
- Platform-specific content requirements
- Brand voice development
- Storytelling and engagement

Always maintain the brand's tone and voice while creating compelling content."""
    
    def process_task(self, state: AgentState) -> AgentState:
        """Process content requirements and create written content"""
        self.log_activity("Starting content creation task", state)
        
        try:
            # Extract content requirements
            content_requirements = state.content
            if not content_requirements:
                state.error_message = "No content requirements provided"
                state.workflow_status = "error"
                return state
            
            # Create content specifications
            content_specs = self._create_content_specifications(content_requirements, state.business_profile)
            
            # Generate content
            written_content = self._generate_content(content_specs)
            
            # Update state with content outputs
            state.agent_outputs["content_specifications"] = content_specs
            state.agent_outputs["written_content"] = written_content
            state.agent_outputs["scheduling_requirements"] = self._create_scheduling_requirements(written_content)
            
            self.log_activity(f"Created {len(written_content)} content pieces", state)
            state.workflow_status = "completed"
            
        except Exception as e:
            state.error_message = f"Error creating content: {str(e)}"
            state.workflow_status = "error"
            self.log_activity(f"Error: {str(e)}", state)
        
        return state
    
    def _create_content_specifications(self, requirements: str, business_profile: Dict[str, Any]) -> Dict[str, Any]:
        """Create detailed content specifications"""
        brand_voice = business_profile.get("brand_voice", "professional")
        target_audience = business_profile.get("target_audience", [])
        industry = business_profile.get("industry", "general")
        
        return {
            "content_type": self._determine_content_type(requirements),
            "platform": self._determine_platform(requirements),
            "brand_voice": brand_voice,
            "target_audience": target_audience,
            "industry": industry,
            "content_topic": requirements,
            "tone": self._get_tone_for_platform(self._determine_platform(requirements)),
            "word_count": self._get_word_count_for_type(self._determine_content_type(requirements)),
            "hashtags_needed": self._needs_hashtags(self._determine_platform(requirements)),
            "call_to_action_required": True
        }
    
    def _determine_content_type(self, requirements: str) -> str:
        """Determine the type of content needed"""
        requirements_lower = requirements.lower()
        
        if any(word in requirements_lower for word in ["blog", "article", "post"]):
            return "blog_article"
        elif any(word in requirements_lower for word in ["facebook", "fb"]):
            return "facebook_post"
        elif any(word in requirements_lower for word in ["instagram", "ig", "caption"]):
            return "instagram_caption"
        elif any(word in requirements_lower for word in ["linkedin", "professional"]):
            return "linkedin_post"
        elif any(word in requirements_lower for word in ["video", "youtube", "description"]):
            return "video_description"
        elif any(word in requirements_lower for word in ["email", "newsletter"]):
            return "email_newsletter"
        else:
            return "social_media_post"
    
    def _determine_platform(self, requirements: str) -> str:
        """Determine the target platform"""
        requirements_lower = requirements.lower()
        
        if "facebook" in requirements_lower or "fb" in requirements_lower:
            return "facebook"
        elif "instagram" in requirements_lower or "ig" in requirements_lower:
            return "instagram"
        elif "linkedin" in requirements_lower:
            return "linkedin"
        elif "twitter" in requirements_lower or "x" in requirements_lower:
            return "twitter"
        elif "youtube" in requirements_lower:
            return "youtube"
        else:
            return "general"
    
    def _get_tone_for_platform(self, platform: str) -> str:
        """Get appropriate tone for different platforms"""
        tones = {
            "facebook": "friendly",
            "instagram": "casual",
            "linkedin": "professional",
            "twitter": "conversational",
            "youtube": "engaging",
            "general": "professional"
        }
        return tones.get(platform, "professional")
    
    def _get_word_count_for_type(self, content_type: str) -> Dict[str, int]:
        """Get word count requirements for different content types"""
        counts = {
            "blog_article": {"min": 800, "max": 2000},
            "facebook_post": {"min": 50, "max": 200},
            "instagram_caption": {"min": 100, "max": 300},
            "linkedin_post": {"min": 100, "max": 400},
            "video_description": {"min": 50, "max": 150},
            "email_newsletter": {"min": 200, "max": 500},
            "social_media_post": {"min": 50, "max": 150}
        }
        return counts.get(content_type, {"min": 50, "max": 200})
    
    def _needs_hashtags(self, platform: str) -> bool:
        """Determine if hashtags are needed for the platform"""
        return platform in ["instagram", "twitter", "facebook"]
    
    def _generate_content(self, specs: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate content based on specifications"""
        content_pieces = []
        
        # Create main content piece
        main_content = {
            "id": f"content_{len(content_pieces) + 1}",
            "type": specs["content_type"],
            "platform": specs["platform"],
            "content": {
                "title": self._generate_title(specs),
                "body": self._generate_body(specs),
                "call_to_action": self._generate_cta(specs),
                "hashtags": self._generate_hashtags(specs) if specs["hashtags_needed"] else []
            },
            "specifications": {
                "tone": specs["tone"],
                "word_count": specs["word_count"],
                "target_audience": specs["target_audience"]
            },
            "status": "ready_for_scheduling"
        }
        content_pieces.append(main_content)
        
        # Create variations for different platforms if needed
        if specs["platform"] == "general":
            # Create platform-specific versions
            platforms = ["facebook", "instagram", "linkedin"]
            for platform in platforms:
                platform_content = main_content.copy()
                platform_content["id"] = f"content_{len(content_pieces) + 1}"
                platform_content["platform"] = platform
                platform_content["specifications"]["tone"] = self._get_tone_for_platform(platform)
                content_pieces.append(platform_content)
        
        return content_pieces
    
    def _generate_title(self, specs: Dict[str, Any]) -> str:
        """Generate a title for the content"""
        # This would typically use the LLM to generate titles
        return f"Engaging {specs['content_type'].replace('_', ' ').title()} for {specs['industry']}"
    
    def _generate_body(self, specs: Dict[str, Any]) -> str:
        """Generate the main body content"""
        # This would typically use the LLM to generate content
        return f"Professional {specs['content_type'].replace('_', ' ')} content tailored for {specs['target_audience']} in the {specs['industry']} industry."
    
    def _generate_cta(self, specs: Dict[str, Any]) -> str:
        """Generate call to action"""
        ctas = [
            "Learn more about our services!",
            "Contact us today for a consultation",
            "Follow us for more updates",
            "Share this with your network",
            "Book your free consultation now"
        ]
        return ctas[0]  # In practice, this would be more dynamic
    
    def _generate_hashtags(self, specs: Dict[str, Any]) -> List[str]:
        """Generate relevant hashtags"""
        base_hashtags = [f"#{specs['industry']}", "#business", "#marketing"]
        platform_hashtags = {
            "instagram": ["#instagood", "#socialmedia"],
            "twitter": ["#business", "#marketing"],
            "facebook": ["#business", "#entrepreneur"]
        }
        return base_hashtags + platform_hashtags.get(specs["platform"], [])
    
    def _create_scheduling_requirements(self, content: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Create requirements for the task scheduler"""
        return {
            "content_type": "written_content",
            "content_pieces": content,
            "scheduling_priority": "high",
            "platforms": list(set(piece["platform"] for piece in content)),
            "estimated_completion_time": "1-2 hours",
            "special_requirements": "Ensure content is optimized for each platform"
        } 