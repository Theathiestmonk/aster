"""
Content Management API Endpoints
Provides endpoints for managing content creation, tasks, and requests
"""

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import Dict, Any, Optional, List
from app.api.auth import get_current_user
from app.models.user import User
from app.core.supabase import supabase_manager
import json
from datetime import datetime

router = APIRouter(prefix="/content", tags=["content"])


class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    priority: str = "medium"
    due_date: Optional[str] = None
    assigned_by: Optional[str] = None


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    due_date: Optional[str] = None


class SocialMediaPostCreate(BaseModel):
    title: str
    content: str
    platform: str
    status: str = "draft"
    scheduled_date: Optional[str] = None
    tags: Optional[List[str]] = None


class BlogCreate(BaseModel):
    title: str
    excerpt: Optional[str] = None
    content: str
    status: str = "draft"
    read_time: Optional[int] = None
    tags: Optional[List[str]] = None


class ContentRequestCreate(BaseModel):
    type: str
    title: str
    description: Optional[str] = None
    priority: str = "medium"
    requested_by: Optional[str] = None


@router.get("/tasks")
async def get_tasks(current_user: User = Depends(get_current_user)):
    """Get all tasks for the current user"""
    try:
        response = supabase_manager.client.table("content_tasks").select("*").eq("user_id", current_user.id).order("created_at", desc=True).execute()
        return {"tasks": response.data}
    except Exception as e:
        print(f"Error fetching tasks: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch tasks: {str(e)}"
        )


@router.post("/tasks")
async def create_task(
    task: TaskCreate,
    current_user: User = Depends(get_current_user)
):
    """Create a new task"""
    try:
        task_data = {
            "user_id": current_user.id,
            "title": task.title,
            "description": task.description,
            "priority": task.priority,
            "due_date": task.due_date,
            "assigned_by": task.assigned_by
        }
        
        response = supabase_manager.supabase.table("content_tasks").insert(task_data).execute()
        return {"task": response.data[0]}
    except Exception as e:
        print(f"Error creating task: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create task: {str(e)}"
        )


@router.put("/tasks/{task_id}")
async def update_task(
    task_id: str,
    task_update: TaskUpdate,
    current_user: User = Depends(get_current_user)
):
    """Update a task"""
    try:
        update_data = {k: v for k, v in task_update.dict().items() if v is not None}
        update_data["updated_at"] = datetime.utcnow().isoformat()
        
        response = supabase_manager.client.table("content_tasks").update(update_data).eq("id", task_id).eq("user_id", current_user.id).execute()
        
        if not response.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )
        
        return {"task": response.data[0]}
    except Exception as e:
        print(f"Error updating task: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update task: {str(e)}"
        )


@router.get("/posts")
async def get_social_media_posts(current_user: User = Depends(get_current_user)):
    """Get all social media posts for the current user"""
    try:
        response = supabase_manager.client.table("social_media_posts").select("*").eq("user_id", current_user.id).order("created_at", desc=True).execute()
        return {"posts": response.data}
    except Exception as e:
        print(f"Error fetching posts: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch posts: {str(e)}"
        )


@router.post("/posts")
async def create_social_media_post(
    post: SocialMediaPostCreate,
    current_user: User = Depends(get_current_user)
):
    """Create a new social media post"""
    try:
        post_data = {
            "user_id": current_user.id,
            "title": post.title,
            "content": post.content,
            "platform": post.platform,
            "status": post.status,
            "scheduled_date": post.scheduled_date,
            "tags": post.tags
        }
        
        response = supabase_manager.client.table("social_media_posts").insert(post_data).execute()
        return {"post": response.data[0]}
    except Exception as e:
        print(f"Error creating post: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create post: {str(e)}"
        )


@router.get("/blogs")
async def get_blogs(current_user: User = Depends(get_current_user)):
    """Get all blogs for the current user"""
    try:
        response = supabase_manager.client.table("blogs").select("*").eq("user_id", current_user.id).order("created_at", desc=True).execute()
        return {"blogs": response.data}
    except Exception as e:
        print(f"Error fetching blogs: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch blogs: {str(e)}"
        )


@router.post("/blogs")
async def create_blog(
    blog: BlogCreate,
    current_user: User = Depends(get_current_user)
):
    """Create a new blog"""
    try:
        blog_data = {
            "user_id": current_user.id,
            "title": blog.title,
            "excerpt": blog.excerpt,
            "content": blog.content,
            "status": blog.status,
            "read_time": blog.read_time,
            "tags": blog.tags
        }
        
        response = supabase_manager.client.table("blogs").insert(blog_data).execute()
        return {"blog": response.data[0]}
    except Exception as e:
        print(f"Error creating blog: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create blog: {str(e)}"
        )


@router.get("/requests")
async def get_content_requests(current_user: User = Depends(get_current_user)):
    """Get all content requests for the current user"""
    try:
        response = supabase_manager.client.table("content_requests").select("*").eq("user_id", current_user.id).order("created_at", desc=True).execute()
        return {"requests": response.data}
    except Exception as e:
        print(f"Error fetching requests: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch requests: {str(e)}"
        )


@router.post("/requests")
async def create_content_request(
    request: ContentRequestCreate,
    current_user: User = Depends(get_current_user)
):
    """Create a new content request"""
    try:
        request_data = {
            "user_id": current_user.id,
            "type": request.type,
            "title": request.title,
            "description": request.description,
            "priority": request.priority,
            "requested_by": request.requested_by
        }
        
        response = supabase_manager.client.table("content_requests").insert(request_data).execute()
        return {"request": response.data[0]}
    except Exception as e:
        print(f"Error creating request: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create request: {str(e)}"
        )


@router.post("/history")
async def add_content_history(
    content_data: Dict[str, Any],
    current_user: User = Depends(get_current_user)
):
    """Add content creation history"""
    try:
        history_data = {
            "user_id": current_user.id,
            "content_type": content_data.get("content_type"),
            "title": content_data.get("title"),
            "content": content_data.get("content"),
            "description": content_data.get("description"),
            "platform": content_data.get("platform"),
            "tags": content_data.get("tags"),
            "agent_used": content_data.get("agent_used", "content_writer")
        }
        
        response = supabase_manager.client.table("content_creation_history").insert(history_data).execute()
        return {"history": response.data[0]}
    except Exception as e:
        print(f"Error adding content history: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to add content history: {str(e)}"
        )


@router.get("/stats")
async def get_content_stats(current_user: User = Depends(get_current_user)):
    """Get content statistics for the current user"""
    try:
        # Get counts for different content types
        tasks_response = supabase_manager.client.table("content_tasks").select("status").eq("user_id", current_user.id).execute()
        posts_response = supabase_manager.client.table("social_media_posts").select("status").eq("user_id", current_user.id).execute()
        blogs_response = supabase_manager.client.table("blogs").select("status").eq("user_id", current_user.id).execute()
        requests_response = supabase_manager.client.table("content_requests").select("status").eq("user_id", current_user.id).execute()
        
        # Calculate statistics
        stats = {
            "tasks": {
                "total": len(tasks_response.data),
                "completed": len([t for t in tasks_response.data if t["status"] == "completed"]),
                "pending": len([t for t in tasks_response.data if t["status"] == "pending"]),
                "working": len([t for t in tasks_response.data if t["status"] == "working"])
            },
            "posts": {
                "total": len(posts_response.data),
                "published": len([p for p in posts_response.data if p["status"] == "published"]),
                "draft": len([p for p in posts_response.data if p["status"] == "draft"]),
                "scheduled": len([p for p in posts_response.data if p["status"] == "scheduled"])
            },
            "blogs": {
                "total": len(blogs_response.data),
                "published": len([b for b in blogs_response.data if b["status"] == "published"]),
                "draft": len([b for b in blogs_response.data if b["status"] == "draft"]),
                "review": len([b for b in blogs_response.data if b["status"] == "review"])
            },
            "requests": {
                "total": len(requests_response.data),
                "pending": len([r for r in requests_response.data if r["status"] == "pending"]),
                "approved": len([r for r in requests_response.data if r["status"] == "approved"]),
                "rejected": len([r for r in requests_response.data if r["status"] == "rejected"])
            }
        }
        
        return stats
    except Exception as e:
        print(f"Error fetching content stats: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch content stats: {str(e)}"
        ) 