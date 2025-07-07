"""
Graphic Designer Agent (Pritesh)
Creates visual content based on brand guidelines and requirements
"""

from typing import Dict, Any, List
from .base_agent import BaseAgent, AgentState


class GraphicDesigner(BaseAgent):
    """Pritesh - Graphic Designer who creates visual content for the brand"""
    
    def __init__(self):
        super().__init__(
            name="Pritesh",
            role="Graphic Designer",
            model_name="gpt-4"
        )
    
    def get_system_prompt(self) -> str:
        return """You are Pritesh, a talented Graphic Designer. Your role is to:
1. Create visual content (graphics, videos, images) based on brand guidelines
2. Follow the brand manual, color scheme, and design theme
3. Create content for various platforms (Instagram, Facebook, LinkedIn, etc.)
4. Ensure all designs are on-brand and visually appealing
5. Send completed designs to the Task Scheduler (Dhruv) for scheduling

You have expertise in:
- Social media graphics
- Video content creation
- Brand identity design
- Platform-specific design requirements
- Color theory and typography

Always consider the brand's visual identity and target audience when creating content."""
    
    def process_task(self, state: AgentState) -> AgentState:
        """Process design requirements and create visual content"""
        self.log_activity("Starting design task", state)
        
        try:
            # Extract design requirements
            design_requirements = state.design_requirements
            if not design_requirements:
                state.error_message = "No design requirements provided"
                state.workflow_status = "error"
                return state
            
            # Create design specifications
            design_specs = self._create_design_specifications(design_requirements, state.business_profile)
            
            # Generate design content
            design_content = self._generate_design_content(design_specs)
            
            # Update state with design outputs
            state.agent_outputs["design_specifications"] = design_specs
            state.agent_outputs["design_content"] = design_content
            state.agent_outputs["scheduling_requirements"] = self._create_scheduling_requirements(design_content)
            
            self.log_activity(f"Created {len(design_content)} design pieces", state)
            state.workflow_status = "completed"
            
        except Exception as e:
            state.error_message = f"Error creating design: {str(e)}"
            state.workflow_status = "error"
            self.log_activity(f"Error: {str(e)}", state)
        
        return state
    
    def _create_design_specifications(self, requirements: Dict[str, Any], business_profile: Dict[str, Any]) -> Dict[str, Any]:
        """Create detailed design specifications"""
        brand_colors = business_profile.get("brand_colors", ["#000000", "#FFFFFF"])
        brand_fonts = business_profile.get("brand_fonts", ["Arial", "Helvetica"])
        brand_style = business_profile.get("brand_style", "modern")
        
        return {
            "content_type": requirements.get("content_type", "social_media_post"),
            "platform": requirements.get("platform", "instagram"),
            "dimensions": self._get_platform_dimensions(requirements.get("platform", "instagram")),
            "brand_colors": brand_colors,
            "brand_fonts": brand_fonts,
            "brand_style": brand_style,
            "content_message": requirements.get("message", ""),
            "target_audience": business_profile.get("target_audience", []),
            "call_to_action": requirements.get("call_to_action", ""),
            "visual_elements": requirements.get("visual_elements", []),
            "tone": requirements.get("tone", "professional")
        }
    
    def _get_platform_dimensions(self, platform: str) -> Dict[str, int]:
        """Get optimal dimensions for different platforms"""
        dimensions = {
            "instagram": {"width": 1080, "height": 1080},
            "instagram_story": {"width": 1080, "height": 1920},
            "facebook": {"width": 1200, "height": 630},
            "linkedin": {"width": 1200, "height": 627},
            "twitter": {"width": 1200, "height": 675},
            "youtube_thumbnail": {"width": 1280, "height": 720}
        }
        return dimensions.get(platform, dimensions["instagram"])
    
    def _generate_design_content(self, specs: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate design content based on specifications"""
        designs = []
        
        # Create main design
        main_design = {
            "id": f"design_{len(designs) + 1}",
            "type": specs["content_type"],
            "platform": specs["platform"],
            "dimensions": specs["dimensions"],
            "content": {
                "text": specs["content_message"],
                "call_to_action": specs["call_to_action"],
                "visual_elements": specs["visual_elements"]
            },
            "brand_elements": {
                "colors": specs["brand_colors"],
                "fonts": specs["brand_fonts"],
                "style": specs["brand_style"]
            },
            "status": "ready_for_scheduling"
        }
        designs.append(main_design)
        
        # Create variations for different platforms if needed
        if specs["platform"] == "instagram":
            # Create story version
            story_design = main_design.copy()
            story_design["id"] = f"design_{len(designs) + 1}"
            story_design["platform"] = "instagram_story"
            story_design["dimensions"] = self._get_platform_dimensions("instagram_story")
            designs.append(story_design)
        
        return designs
    
    def _create_scheduling_requirements(self, designs: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Create requirements for the task scheduler"""
        return {
            "content_type": "visual_content",
            "designs": designs,
            "scheduling_priority": "high",
            "platforms": list(set(design["platform"] for design in designs)),
            "estimated_completion_time": "2-4 hours",
            "special_requirements": "Ensure brand consistency across all platforms"
        } 