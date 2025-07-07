"""
Digital Marketing Executive Agent (Ravi)
Coordinates tasks and delegates work to other agents
"""

from typing import Dict, Any, List
from .base_agent import BaseAgent, AgentState


class DigitalMarketingExecutive(BaseAgent):
    """Ravi - Digital Marketing Executive who coordinates all marketing activities"""
    
    def __init__(self):
        super().__init__(
            name="Ravi",
            role="Digital Marketing Executive",
            model_name="gpt-4"
        )
    
    def get_system_prompt(self) -> str:
        return """You are Ravi, a Digital Marketing Executive. Your role is to:
1. Receive strategy from the Strategy Manager (Deep)
2. Break down strategy into actionable tasks for daily, weekly, and monthly execution
3. Delegate tasks to appropriate agents:
   - Graphic Designer (Pritesh) for visual content
   - Content Writer (Twinkle) for written content
   - Task Scheduler (Dhruv) for scheduling
4. Monitor task progress and ensure deadlines are met
5. Coordinate between different agents and maintain workflow efficiency

You should be organized, detail-oriented, and excellent at project management."""
    
    def process_task(self, state: AgentState) -> AgentState:
        """Process strategy and create task breakdown"""
        self.log_activity("Starting task processing", state)
        
        try:
            # Extract strategy from state
            strategy = state.strategy
            if not strategy:
                state.error_message = "No strategy provided to process"
                state.workflow_status = "error"
                return state
            
            # Create task breakdown
            task_breakdown = self._create_task_breakdown(strategy, state.business_profile)
            
            # Update state with task breakdown
            state.agent_outputs["task_breakdown"] = task_breakdown
            state.agent_outputs["delegation_plan"] = self._create_delegation_plan(task_breakdown)
            
            self.log_activity(f"Created task breakdown with {len(task_breakdown)} task categories", state)
            state.workflow_status = "completed"
            
        except Exception as e:
            state.error_message = f"Error processing task: {str(e)}"
            state.workflow_status = "error"
            self.log_activity(f"Error: {str(e)}", state)
        
        return state
    
    def _create_task_breakdown(self, strategy: Dict[str, Any], business_profile: Dict[str, Any]) -> Dict[str, Any]:
        """Break down strategy into actionable tasks"""
        return {
            "daily_tasks": [
                {
                    "task": "Monitor social media engagement",
                    "priority": "high",
                    "assigned_to": "Dhruvil",  # Data Insights Manager
                    "description": "Track daily engagement metrics across all platforms"
                },
                {
                    "task": "Review scheduled content",
                    "priority": "medium",
                    "assigned_to": "Dhruv",  # Task Scheduler
                    "description": "Check and approve content scheduled for the day"
                }
            ],
            "weekly_tasks": [
                {
                    "task": "Create weekly content calendar",
                    "priority": "high",
                    "assigned_to": "Twinkle",  # Content Writer
                    "description": "Plan and create content for the upcoming week"
                },
                {
                    "task": "Design weekly graphics",
                    "priority": "high",
                    "assigned_to": "Pritesh",  # Graphic Designer
                    "description": "Create visual content for weekly campaigns"
                },
                {
                    "task": "Generate performance report",
                    "priority": "medium",
                    "assigned_to": "Dhruvil",  # Data Insights Manager
                    "description": "Analyze weekly performance and create insights"
                }
            ],
            "monthly_tasks": [
                {
                    "task": "Strategy review and adjustment",
                    "priority": "high",
                    "assigned_to": "Deep",  # Strategy Manager
                    "description": "Review monthly performance and adjust strategy"
                },
                {
                    "task": "Campaign planning",
                    "priority": "high",
                    "assigned_to": "Ravi",  # Self
                    "description": "Plan major campaigns for the upcoming month"
                },
                {
                    "task": "Platform optimization",
                    "priority": "medium",
                    "assigned_to": "Dhruvil",  # Data Insights Manager
                    "description": "Optimize ad campaigns and platform settings"
                }
            ]
        }
    
    def _create_delegation_plan(self, task_breakdown: Dict[str, Any]) -> Dict[str, List[str]]:
        """Create delegation plan for each agent"""
        delegation = {
            "Pritesh": [],  # Graphic Designer
            "Twinkle": [],  # Content Writer
            "Dhruv": [],    # Task Scheduler
            "Dhruvil": [],  # Data Insights Manager
            "Deep": []      # Strategy Manager
        }
        
        for timeframe, tasks in task_breakdown.items():
            for task in tasks:
                assigned_to = task["assigned_to"]
                if assigned_to in delegation:
                    delegation[assigned_to].append({
                        "task": task["task"],
                        "priority": task["priority"],
                        "timeframe": timeframe,
                        "description": task["description"]
                    })
        
        return delegation 