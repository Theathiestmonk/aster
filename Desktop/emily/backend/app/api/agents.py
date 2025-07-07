"""
Agent System API Endpoints
Provides endpoints for interacting with the digital marketing agent system
"""

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import Dict, Any, Optional, List
from app.api.auth import get_current_user
from app.models.user import User
from app.core.supabase import supabase_manager
from app.agents.workflow_orchestrator import WorkflowOrchestrator
import json

router = APIRouter(prefix="/agents", tags=["agents"])

# Initialize workflow orchestrator
workflow_orchestrator = WorkflowOrchestrator()


class WorkflowRequest(BaseModel):
    task_type: str = "strategy_development"
    task_data: Optional[Dict[str, Any]] = None


class SpecificTaskRequest(BaseModel):
    task_type: str
    task_data: Dict[str, Any]


class WorkflowResponse(BaseModel):
    workflow_status: str
    user_id: str
    task_type: str
    agent_outputs: Dict[str, Any]
    strategy: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None
    timestamp: str


@router.post("/workflow/execute", response_model=WorkflowResponse)
async def execute_workflow(
    request: WorkflowRequest,
    current_user: User = Depends(get_current_user)
):
    """Execute the complete digital marketing workflow"""
    try:
        print(f"Executing workflow for user {current_user.email}")
        
        # Get user's business profile
        business_profile = await supabase_manager.get_user_profile(current_user.id)
        
        if not business_profile:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Business profile not found. Please complete onboarding first."
            )
        
        # Execute workflow
        result = workflow_orchestrator.execute_workflow(
            user_id=current_user.id,
            business_profile=business_profile,
            task_type=request.task_type
        )
        
        return WorkflowResponse(**result)
        
    except Exception as e:
        print(f"Workflow execution error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Workflow execution failed: {str(e)}"
        )


@router.post("/task/execute", response_model=WorkflowResponse)
async def execute_specific_task(
    request: SpecificTaskRequest,
    current_user: User = Depends(get_current_user)
):
    """Execute a specific task with a single agent"""
    try:
        print(f"Executing specific task {request.task_type} for user {current_user.email}")
        
        # Get user's business profile
        business_profile = await supabase_manager.get_user_profile(current_user.id)
        
        if not business_profile:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Business profile not found. Please complete onboarding first."
            )
        
        # Execute specific task
        result = workflow_orchestrator.execute_specific_task(
            user_id=current_user.id,
            business_profile=business_profile,
            task_type=request.task_type,
            task_data=request.task_data
        )
        
        return WorkflowResponse(**result)
        
    except Exception as e:
        print(f"Task execution error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Task execution failed: {str(e)}"
        )


@router.get("/workflow/status")
async def get_workflow_status():
    """Get current workflow status and agent information"""
    try:
        return workflow_orchestrator.get_workflow_status()
    except Exception as e:
        print(f"Error getting workflow status: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get workflow status: {str(e)}"
        )


@router.post("/content/create")
async def create_content(
    request: Dict[str, Any],
    current_user: User = Depends(get_current_user)
):
    """Create content using the Content Writer agent"""
    try:
        print(f"Creating content for user {current_user.email}")
        
        # Get user's business profile
        business_profile = await supabase_manager.get_user_profile(current_user.id)
        
        if not business_profile:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Business profile not found. Please complete onboarding first."
            )
        
        # Execute content creation task
        result = workflow_orchestrator.execute_specific_task(
            user_id=current_user.id,
            business_profile=business_profile,
            task_type="content_creation",
            task_data={"content_requirements": request.get("content_requirements", "")}
        )
        
        return result
        
    except Exception as e:
        print(f"Content creation error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Content creation failed: {str(e)}"
        )


@router.post("/design/create")
async def create_design(
    request: Dict[str, Any],
    current_user: User = Depends(get_current_user)
):
    """Create design using the Graphic Designer agent"""
    try:
        print(f"Creating design for user {current_user.email}")
        
        # Get user's business profile
        business_profile = await supabase_manager.get_user_profile(current_user.id)
        
        if not business_profile:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Business profile not found. Please complete onboarding first."
            )
        
        # Execute design creation task
        result = workflow_orchestrator.execute_specific_task(
            user_id=current_user.id,
            business_profile=business_profile,
            task_type="design_creation",
            task_data={"design_requirements": request.get("design_requirements", {})}
        )
        
        return result
        
    except Exception as e:
        print(f"Design creation error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Design creation failed: {str(e)}"
        )


@router.post("/content/schedule")
async def schedule_content(
    request: Dict[str, Any],
    current_user: User = Depends(get_current_user)
):
    """Schedule content using the Task Scheduler agent"""
    try:
        print(f"Scheduling content for user {current_user.email}")
        
        # Get user's business profile
        business_profile = await supabase_manager.get_user_profile(current_user.id)
        
        if not business_profile:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Business profile not found. Please complete onboarding first."
            )
        
        # Execute scheduling task
        result = workflow_orchestrator.execute_specific_task(
            user_id=current_user.id,
            business_profile=business_profile,
            task_type="content_scheduling",
            task_data={"scheduling_requirements": request.get("scheduling_requirements", {})}
        )
        
        return result
        
    except Exception as e:
        print(f"Content scheduling error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Content scheduling failed: {str(e)}"
        )


@router.post("/data/analyze")
async def analyze_data(
    request: Dict[str, Any],
    current_user: User = Depends(get_current_user)
):
    """Analyze data using the Data Insights Manager agent"""
    try:
        print(f"Analyzing data for user {current_user.email}")
        
        # Get user's business profile
        business_profile = await supabase_manager.get_user_profile(current_user.id)
        
        if not business_profile:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Business profile not found. Please complete onboarding first."
            )
        
        # Execute data analysis task
        result = workflow_orchestrator.execute_specific_task(
            user_id=current_user.id,
            business_profile=business_profile,
            task_type="data_analysis",
            task_data={"data_requirements": request.get("data_requirements", {})}
        )
        
        return result
        
    except Exception as e:
        print(f"Data analysis error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Data analysis failed: {str(e)}"
        )


@router.post("/strategy/develop")
async def develop_strategy(
    request: Dict[str, Any],
    current_user: User = Depends(get_current_user)
):
    """Develop strategy using the Strategy Manager agent"""
    try:
        print(f"Developing strategy for user {current_user.email}")
        
        # Get user's business profile
        business_profile = await supabase_manager.get_user_profile(current_user.id)
        
        if not business_profile:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Business profile not found. Please complete onboarding first."
            )
        
        # Execute strategy development task
        result = workflow_orchestrator.execute_specific_task(
            user_id=current_user.id,
            business_profile=business_profile,
            task_type="strategy_development",
            task_data=request
        )
        
        return result
        
    except Exception as e:
        print(f"Strategy development error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Strategy development failed: {str(e)}"
        )


@router.get("/agents/list")
async def list_agents():
    """List all available agents and their roles"""
    return {
        "agents": [
            {
                "name": "Deep",
                "role": "Strategy Manager",
                "description": "Creates comprehensive marketing strategies based on business profile and data insights",
                "responsibilities": [
                    "Analyze business profile and goals",
                    "Create marketing strategies",
                    "Design actionable plans",
                    "Coordinate with other agents"
                ]
            },
            {
                "name": "Ravi",
                "role": "Digital Marketing Executive",
                "description": "Coordinates tasks and delegates work to other agents",
                "responsibilities": [
                    "Break down strategy into tasks",
                    "Delegate tasks to appropriate agents",
                    "Monitor task progress",
                    "Ensure workflow efficiency"
                ]
            },
            {
                "name": "Pritesh",
                "role": "Graphic Designer",
                "description": "Creates visual content based on brand guidelines",
                "responsibilities": [
                    "Create graphics and videos",
                    "Follow brand guidelines",
                    "Design for multiple platforms",
                    "Ensure brand consistency"
                ]
            },
            {
                "name": "Twinkle",
                "role": "Content Writer",
                "description": "Creates written content for various platforms",
                "responsibilities": [
                    "Write engaging content",
                    "Optimize for SEO",
                    "Maintain brand voice",
                    "Create platform-specific content"
                ]
            },
            {
                "name": "Dhruv",
                "role": "Task Scheduler",
                "description": "Schedules content across different platforms",
                "responsibilities": [
                    "Schedule content optimally",
                    "Manage content calendar",
                    "Generate reports",
                    "Optimize posting times"
                ]
            },
            {
                "name": "Dhruvil",
                "role": "Data Insights Manager",
                "description": "Analyzes performance data and provides insights",
                "responsibilities": [
                    "Analyze platform data",
                    "Generate insights",
                    "Track performance metrics",
                    "Provide recommendations"
                ]
            }
        ]
    } 