"""
Task Scheduler Agent (Dhruv)
Schedules content across different platforms and reports to client manager
"""

from typing import Dict, Any, List
from datetime import datetime, timedelta
from .base_agent import BaseAgent, AgentState


class TaskScheduler(BaseAgent):
    """Dhruv - Task Scheduler who manages content scheduling and reporting"""
    
    def __init__(self):
        super().__init__(
            name="Dhruv",
            role="Task Scheduler",
            model_name="gpt-4"
        )
    
    def get_system_prompt(self) -> str:
        return """You are Dhruv, a Task Scheduler. Your role is to:
1. Receive content from Graphic Designer (Pritesh) and Content Writer (Twinkle)
2. Schedule posts, videos, and content on different platforms
3. Optimize posting times for maximum engagement
4. Manage content calendar and ensure consistent posting
5. Generate reports for the Client Manager (Deep) about scheduled content
6. Handle platform-specific scheduling requirements

You have expertise in:
- Social media scheduling tools
- Platform-specific best practices
- Content calendar management
- Engagement optimization
- Reporting and analytics

Always ensure content is scheduled at optimal times for the target audience."""
    
    def process_task(self, state: AgentState) -> AgentState:
        """Process scheduling requirements and schedule content"""
        self.log_activity("Starting scheduling task", state)
        
        try:
            # Extract scheduling requirements
            scheduling_requirements = state.scheduling_requirements
            if not scheduling_requirements:
                state.error_message = "No scheduling requirements provided"
                state.workflow_status = "error"
                return state
            
            # Create scheduling plan
            scheduling_plan = self._create_scheduling_plan(scheduling_requirements, state.business_profile)
            
            # Schedule content
            scheduled_content = self._schedule_content(scheduling_plan)
            
            # Generate report for client manager
            client_report = self._generate_client_report(scheduled_content, state.business_profile)
            
            # Update state with scheduling outputs
            state.agent_outputs["scheduling_plan"] = scheduling_plan
            state.agent_outputs["scheduled_content"] = scheduled_content
            state.agent_outputs["client_report"] = client_report
            
            self.log_activity(f"Scheduled {len(scheduled_content)} content pieces", state)
            state.workflow_status = "completed"
            
        except Exception as e:
            state.error_message = f"Error scheduling content: {str(e)}"
            state.workflow_status = "error"
            self.log_activity(f"Error: {str(e)}", state)
        
        return state
    
    def _create_scheduling_plan(self, requirements: Dict[str, Any], business_profile: Dict[str, Any]) -> Dict[str, Any]:
        """Create a detailed scheduling plan"""
        target_audience = business_profile.get("target_audience", [])
        industry = business_profile.get("industry", "general")
        
        return {
            "content_type": requirements.get("content_type", "general"),
            "platforms": requirements.get("platforms", []),
            "priority": requirements.get("scheduling_priority", "medium"),
            "optimal_times": self._get_optimal_posting_times(target_audience, industry),
            "content_pieces": requirements.get("designs", []) + requirements.get("content_pieces", []),
            "scheduling_strategy": self._determine_scheduling_strategy(requirements),
            "estimated_engagement": self._estimate_engagement(business_profile)
        }
    
    def _get_optimal_posting_times(self, target_audience: List[str], industry: str) -> Dict[str, List[str]]:
        """Get optimal posting times for different platforms"""
        # This would typically be more sophisticated based on audience analysis
        return {
            "facebook": ["9:00 AM", "1:00 PM", "7:00 PM"],
            "instagram": ["11:00 AM", "2:00 PM", "8:00 PM"],
            "linkedin": ["8:00 AM", "12:00 PM", "5:00 PM"],
            "twitter": ["8:00 AM", "12:00 PM", "6:00 PM"],
            "youtube": ["2:00 PM", "6:00 PM", "9:00 PM"]
        }
    
    def _determine_scheduling_strategy(self, requirements: Dict[str, Any]) -> str:
        """Determine the best scheduling strategy"""
        priority = requirements.get("scheduling_priority", "medium")
        
        if priority == "high":
            return "immediate_scheduling"
        elif priority == "medium":
            return "optimal_timing"
        else:
            return "batch_scheduling"
    
    def _estimate_engagement(self, business_profile: Dict[str, Any]) -> Dict[str, float]:
        """Estimate engagement rates for different platforms"""
        # This would typically use historical data and analytics
        base_engagement = 0.05  # 5% base engagement rate
        
        return {
            "facebook": base_engagement * 1.2,
            "instagram": base_engagement * 1.5,
            "linkedin": base_engagement * 0.8,
            "twitter": base_engagement * 0.6,
            "youtube": base_engagement * 1.0
        }
    
    def _schedule_content(self, plan: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Schedule content according to the plan"""
        scheduled_content = []
        
        for i, content_piece in enumerate(plan["content_pieces"]):
            # Determine posting time based on strategy
            posting_time = self._calculate_posting_time(plan, i)
            
            scheduled_item = {
                "id": f"scheduled_{i + 1}",
                "content_id": content_piece.get("id", f"content_{i + 1}"),
                "platform": content_piece.get("platform", "general"),
                "content_type": content_piece.get("type", "post"),
                "scheduled_time": posting_time,
                "status": "scheduled",
                "estimated_engagement": plan["estimated_engagement"].get(content_piece.get("platform", "general"), 0.05),
                "priority": plan["priority"],
                "content_preview": self._generate_content_preview(content_piece)
            }
            
            scheduled_content.append(scheduled_item)
        
        return scheduled_content
    
    def _calculate_posting_time(self, plan: Dict[str, Any], content_index: int) -> str:
        """Calculate the optimal posting time for content"""
        strategy = plan["scheduling_strategy"]
        optimal_times = plan["optimal_times"]
        
        if strategy == "immediate_scheduling":
            # Schedule for the next optimal time
            next_time = datetime.now() + timedelta(hours=1)
            return next_time.strftime("%Y-%m-%d %H:%M:%S")
        
        elif strategy == "optimal_timing":
            # Use optimal times with spacing
            platform = plan["content_pieces"][content_index].get("platform", "facebook")
            times = optimal_times.get(platform, ["9:00 AM"])
            time_index = content_index % len(times)
            
            # Schedule for tomorrow at the optimal time
            tomorrow = datetime.now() + timedelta(days=1)
            time_str = times[time_index]
            hour = int(time_str.split(":")[0])
            minute = int(time_str.split(":")[1].split(" ")[0])
            
            scheduled_time = tomorrow.replace(hour=hour, minute=minute, second=0, microsecond=0)
            return scheduled_time.strftime("%Y-%m-%d %H:%M:%S")
        
        else:  # batch_scheduling
            # Schedule in batches with regular intervals
            batch_time = datetime.now() + timedelta(days=content_index + 1, hours=10)
            return batch_time.strftime("%Y-%m-%d %H:%M:%S")
    
    def _generate_content_preview(self, content_piece: Dict[str, Any]) -> str:
        """Generate a preview of the content for reporting"""
        content_type = content_piece.get("type", "post")
        platform = content_piece.get("platform", "general")
        
        if "content" in content_piece:
            content = content_piece["content"]
            if "title" in content:
                return f"{content_type.title()} - {content['title'][:50]}..."
            elif "text" in content:
                return f"{content_type.title()} - {content['text'][:50]}..."
            elif "body" in content:
                return f"{content_type.title()} - {content['body'][:50]}..."
        
        return f"{content_type.title()} for {platform}"
    
    def _generate_client_report(self, scheduled_content: List[Dict[str, Any]], business_profile: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a report for the client manager"""
        business_name = business_profile.get("business_name", "Your Business")
        
        # Group content by platform
        platform_content = {}
        for item in scheduled_content:
            platform = item["platform"]
            if platform not in platform_content:
                platform_content[platform] = []
            platform_content[platform].append(item)
        
        # Calculate summary statistics
        total_content = len(scheduled_content)
        platforms_used = list(platform_content.keys())
        avg_engagement = sum(item["estimated_engagement"] for item in scheduled_content) / total_content if total_content > 0 else 0
        
        return {
            "business_name": business_name,
            "report_date": datetime.now().strftime("%Y-%m-%d"),
            "summary": {
                "total_content_scheduled": total_content,
                "platforms_used": platforms_used,
                "average_estimated_engagement": f"{avg_engagement:.2%}",
                "scheduling_status": "completed"
            },
            "platform_breakdown": {
                platform: {
                    "content_count": len(content),
                    "estimated_engagement": f"{sum(item['estimated_engagement'] for item in content) / len(content):.2%}" if content else "0%"
                }
                for platform, content in platform_content.items()
            },
            "scheduled_content": [
                {
                    "id": item["id"],
                    "platform": item["platform"],
                    "content_type": item["content_type"],
                    "scheduled_time": item["scheduled_time"],
                    "preview": item["content_preview"]
                }
                for item in scheduled_content
            ],
            "next_steps": [
                "Monitor engagement metrics after posting",
                "Adjust scheduling times based on performance",
                "Prepare next week's content calendar"
            ]
        } 