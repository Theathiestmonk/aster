"""
Base Agent Class
Provides common functionality for all agents in the system
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from datetime import datetime
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class AgentState(BaseModel):
    """Shared state for all agents"""
    user_id: str
    business_profile: Dict[str, Any]
    current_task: Optional[str] = None
    task_type: Optional[str] = None
    content: Optional[str] = None
    design_requirements: Optional[Dict[str, Any]] = None
    scheduling_requirements: Optional[Dict[str, Any]] = None
    data_insights: Optional[Dict[str, Any]] = None
    strategy: Optional[Dict[str, Any]] = None
    agent_outputs: Dict[str, Any] = {}
    workflow_status: str = "pending"
    error_message: Optional[str] = None


class BaseAgent(ABC):
    """Base class for all agents in the system"""
    
    def __init__(self, name: str, role: str, model_name: str = "gpt-4"):
        self.name = name
        self.role = role
        
        # Get OpenAI API key from environment
        openai_api_key = os.getenv("OPENAI_API_KEY")
        if not openai_api_key:
            raise ValueError("OPENAI_API_KEY environment variable is required")
        
        self.llm = ChatOpenAI(
            model=model_name, 
            temperature=0.7,
            openai_api_key=openai_api_key
        )
        self.graph = None
        
    @abstractmethod
    def process_task(self, state: AgentState) -> AgentState:
        """Process the current task and return updated state"""
        pass
    
    @abstractmethod
    def get_system_prompt(self) -> str:
        """Return the system prompt for this agent"""
        pass
    
    def create_graph(self) -> StateGraph:
        """Create the LangGraph for this agent"""
        workflow = StateGraph(AgentState)
        
        # Add the main processing node
        workflow.add_node(self.name, self.process_task)
        
        # Set the entry point
        workflow.set_entry_point(self.name)
        
        # Set the end point
        workflow.add_edge(self.name, END)
        
        return workflow.compile()
    
    def execute(self, state: AgentState) -> AgentState:
        """Execute the agent's workflow"""
        if self.graph is None:
            self.graph = self.create_graph()
        
        try:
            result = self.graph.invoke(state)
            return result
        except Exception as e:
            state.error_message = f"Error in {self.name}: {str(e)}"
            state.workflow_status = "error"
            return state
    
    def log_activity(self, message: str, state: AgentState):
        """Log agent activity"""
        print(f"[{self.name}] {message}")
        if "activity_log" not in state.agent_outputs:
            state.agent_outputs["activity_log"] = []
        state.agent_outputs["activity_log"].append({
            "agent": self.name,
            "message": message,
            "timestamp": datetime.now().isoformat()
        }) 