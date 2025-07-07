"""
Workflow Orchestrator
Coordinates all agents in the digital marketing workflow
"""

from typing import Dict, Any, List
from datetime import datetime
from langgraph.graph import StateGraph, END
import os
from dotenv import load_dotenv
from .base_agent import AgentState
from .strategy_manager import StrategyManager
from .digital_marketing_executive import DigitalMarketingExecutive
from .graphic_designer import GraphicDesigner
from .content_writer import ContentWriter
from .task_scheduler import TaskScheduler
from .data_insights_manager import DataInsightsManager

# Load environment variables
load_dotenv()


class WorkflowOrchestrator:
    """Orchestrates the complete digital marketing workflow"""
    
    def __init__(self):
        # Check for OpenAI API key
        openai_api_key = os.getenv("OPENAI_API_KEY")
        if not openai_api_key:
            raise ValueError("OPENAI_API_KEY environment variable is required. Please set it in your .env file.")
        
        # Initialize all agents
        self.strategy_manager = StrategyManager()
        self.digital_marketing_executive = DigitalMarketingExecutive()
        self.graphic_designer = GraphicDesigner()
        self.content_writer = ContentWriter()
        self.task_scheduler = TaskScheduler()
        self.data_insights_manager = DataInsightsManager()
        
        # Create the workflow graph
        self.workflow = self._create_workflow()
    
    def _create_workflow(self) -> StateGraph:
        """Create the complete workflow graph"""
        workflow = StateGraph(AgentState)
        
        # Add nodes for each agent
        workflow.add_node("strategy_manager", self._strategy_manager_node)
        workflow.add_node("digital_marketing_executive", self._digital_marketing_executive_node)
        workflow.add_node("graphic_designer", self._graphic_designer_node)
        workflow.add_node("content_writer", self._content_writer_node)
        workflow.add_node("task_scheduler", self._task_scheduler_node)
        workflow.add_node("data_insights_manager", self._data_insights_manager_node)
        
        # Add conditional routing nodes
        workflow.add_node("route_content_tasks", self._route_content_tasks)
        workflow.add_node("route_design_tasks", self._route_design_tasks)
        workflow.add_node("route_scheduling", self._route_scheduling)
        workflow.add_node("route_analysis", self._route_analysis)
        
        # Set entry point
        workflow.set_entry_point("strategy_manager")
        
        # Define workflow edges
        workflow.add_edge("strategy_manager", "digital_marketing_executive")
        workflow.add_edge("digital_marketing_executive", "route_content_tasks")
        
        # Content routing
        workflow.add_conditional_edges(
            "route_content_tasks",
            self._should_create_content,
            {
                "content_writer": "content_writer",
                "route_design_tasks": "route_design_tasks"
            }
        )
        
        # Design routing
        workflow.add_conditional_edges(
            "route_design_tasks",
            self._should_create_designs,
            {
                "graphic_designer": "graphic_designer",
                "route_scheduling": "route_scheduling"
            }
        )
        
        # Scheduling routing
        workflow.add_conditional_edges(
            "route_scheduling",
            self._should_schedule_content,
            {
                "task_scheduler": "task_scheduler",
                "route_analysis": "route_analysis"
            }
        )
        
        # Analysis routing
        workflow.add_conditional_edges(
            "route_analysis",
            self._should_analyze_data,
            {
                "data_insights_manager": "data_insights_manager",
                END: END
            }
        )
        
        # Direct edges from agents to next steps
        workflow.add_edge("content_writer", "route_design_tasks")
        workflow.add_edge("graphic_designer", "route_scheduling")
        workflow.add_edge("task_scheduler", "route_analysis")
        workflow.add_edge("data_insights_manager", END)
        
        return workflow.compile()
    
    def _strategy_manager_node(self, state: AgentState) -> AgentState:
        """Strategy Manager node"""
        print("[Workflow] Starting Strategy Manager (Deep)")
        return self.strategy_manager.execute(state)
    
    def _digital_marketing_executive_node(self, state: AgentState) -> AgentState:
        """Digital Marketing Executive node"""
        print("[Workflow] Starting Digital Marketing Executive (Ravi)")
        return self.digital_marketing_executive.execute(state)
    
    def _graphic_designer_node(self, state: AgentState) -> AgentState:
        """Graphic Designer node"""
        print("[Workflow] Starting Graphic Designer (Pritesh)")
        return self.graphic_designer.execute(state)
    
    def _content_writer_node(self, state: AgentState) -> AgentState:
        """Content Writer node"""
        print("[Workflow] Starting Content Writer (Twinkle)")
        return self.content_writer.execute(state)
    
    def _task_scheduler_node(self, state: AgentState) -> AgentState:
        """Task Scheduler node"""
        print("[Workflow] Starting Task Scheduler (Dhruv)")
        return self.task_scheduler.execute(state)
    
    def _data_insights_manager_node(self, state: AgentState) -> AgentState:
        """Data Insights Manager node"""
        print("[Workflow] Starting Data Insights Manager (Dhruvil)")
        return self.data_insights_manager.execute(state)
    
    def _route_content_tasks(self, state: AgentState) -> AgentState:
        """Route to content creation tasks"""
        print("[Workflow] Routing to content tasks")
        return state
    
    def _route_design_tasks(self, state: AgentState) -> AgentState:
        """Route to design tasks"""
        print("[Workflow] Routing to design tasks")
        return state
    
    def _route_scheduling(self, state: AgentState) -> AgentState:
        """Route to scheduling tasks"""
        print("[Workflow] Routing to scheduling tasks")
        return state
    
    def _route_analysis(self, state: AgentState) -> AgentState:
        """Route to analysis tasks"""
        print("[Workflow] Routing to analysis tasks")
        return state
    
    def _should_create_content(self, state: AgentState) -> str:
        """Determine if content creation is needed"""
        task_breakdown = state.agent_outputs.get("task_breakdown", {})
        weekly_tasks = task_breakdown.get("weekly_tasks", [])
        
        for task in weekly_tasks:
            if task.get("assigned_to") == "Twinkle" and "content" in task.get("task", "").lower():
                return "content_writer"
        
        return "route_design_tasks"
    
    def _should_create_designs(self, state: AgentState) -> str:
        """Determine if design creation is needed"""
        task_breakdown = state.agent_outputs.get("task_breakdown", {})
        weekly_tasks = task_breakdown.get("weekly_tasks", [])
        
        for task in weekly_tasks:
            if task.get("assigned_to") == "Pritesh" and "design" in task.get("task", "").lower():
                return "graphic_designer"
        
        return "route_scheduling"
    
    def _should_schedule_content(self, state: AgentState) -> str:
        """Determine if content scheduling is needed"""
        # Check if we have content or designs to schedule
        has_content = state.agent_outputs.get("written_content") is not None
        has_designs = state.agent_outputs.get("design_content") is not None
        
        if has_content or has_designs:
            return "task_scheduler"
        
        return "route_analysis"
    
    def _should_analyze_data(self, state: AgentState) -> str:
        """Determine if data analysis is needed"""
        # Always run data analysis at the end
        return "data_insights_manager"
    
    def execute_workflow(self, user_id: str, business_profile: Dict[str, Any], task_type: str = "strategy_development") -> Dict[str, Any]:
        """Execute the complete workflow"""
        print(f"[Workflow] Starting workflow for user {user_id}")
        
        # Initialize state
        initial_state = AgentState(
            user_id=user_id,
            business_profile=business_profile,
            task_type=task_type,
            workflow_status="started"
        )
        
        try:
            # Execute workflow
            final_state = self.workflow.invoke(initial_state)
            
            # Prepare response
            response = {
                "workflow_status": final_state.workflow_status,
                "user_id": final_state.user_id,
                "task_type": final_state.task_type,
                "agent_outputs": final_state.agent_outputs,
                "strategy": final_state.strategy,
                "error_message": final_state.error_message,
                "timestamp": datetime.now().isoformat()
            }
            
            print(f"[Workflow] Workflow completed with status: {final_state.workflow_status}")
            return response
            
        except Exception as e:
            print(f"[Workflow] Error executing workflow: {str(e)}")
            return {
                "workflow_status": "error",
                "user_id": user_id,
                "error_message": f"Workflow execution error: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }
    
    def execute_specific_task(self, user_id: str, business_profile: Dict[str, Any], task_type: str, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a specific task with a single agent"""
        print(f"[Workflow] Executing specific task: {task_type}")
        
        # Initialize state with task-specific data
        initial_state = AgentState(
            user_id=user_id,
            business_profile=business_profile,
            task_type=task_type,
            workflow_status="started"
        )
        
        # Add task-specific data to state
        if task_type == "content_creation":
            initial_state.content = task_data.get("content_requirements", "")
        elif task_type == "design_creation":
            initial_state.design_requirements = task_data.get("design_requirements", {})
        elif task_type == "content_scheduling":
            initial_state.scheduling_requirements = task_data.get("scheduling_requirements", {})
        elif task_type == "data_analysis":
            initial_state.data_insights = task_data.get("data_requirements", {})
        
        try:
            # Execute appropriate agent
            if task_type == "content_creation":
                final_state = self.content_writer.execute(initial_state)
            elif task_type == "design_creation":
                final_state = self.graphic_designer.execute(initial_state)
            elif task_type == "content_scheduling":
                final_state = self.task_scheduler.execute(initial_state)
            elif task_type == "data_analysis":
                final_state = self.data_insights_manager.execute(initial_state)
            elif task_type == "strategy_development":
                final_state = self.strategy_manager.execute(initial_state)
            else:
                raise ValueError(f"Unknown task type: {task_type}")
            
            # Prepare response
            response = {
                "task_type": task_type,
                "workflow_status": final_state.workflow_status,
                "user_id": final_state.user_id,
                "agent_outputs": final_state.agent_outputs,
                "error_message": final_state.error_message,
                "timestamp": datetime.now().isoformat()
            }
            
            print(f"[Workflow] Task completed with status: {final_state.workflow_status}")
            return response
            
        except Exception as e:
            print(f"[Workflow] Error executing task: {str(e)}")
            return {
                "task_type": task_type,
                "workflow_status": "error",
                "user_id": user_id,
                "error_message": f"Task execution error: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }
    
    def get_workflow_status(self) -> Dict[str, Any]:
        """Get current workflow status and agent information"""
        return {
            "agents": {
                "strategy_manager": {
                    "name": "Deep",
                    "role": "Strategy Manager",
                    "status": "active"
                },
                "digital_marketing_executive": {
                    "name": "Ravi",
                    "role": "Digital Marketing Executive",
                    "status": "active"
                },
                "graphic_designer": {
                    "name": "Pritesh",
                    "role": "Graphic Designer",
                    "status": "active"
                },
                "content_writer": {
                    "name": "Twinkle",
                    "role": "Content Writer",
                    "status": "active"
                },
                "task_scheduler": {
                    "name": "Dhruv",
                    "role": "Task Scheduler",
                    "status": "active"
                },
                "data_insights_manager": {
                    "name": "Dhruvil",
                    "role": "Data Insights Manager",
                    "status": "active"
                }
            },
            "workflow_status": "ready",
            "timestamp": datetime.now().isoformat()
        } 