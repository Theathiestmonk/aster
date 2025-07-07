"""
Simple Workflow Visualization
Shows the LangGraph workflow structure in text format
"""

def show_workflow_graph():
    """Display the workflow graph in text format"""
    
    print("🔄 DIGITAL MARKETING AGENT SYSTEM - LANGGRAPH WORKFLOW")
    print("=" * 70)
    print()
    
    # Show the workflow structure
    workflow = """
    ┌─────────────────────────────────────────────────────────────────────────────┐
    │                    DIGITAL MARKETING AGENT SYSTEM                          │
    │                              LangGraph Workflow                            │
    └─────────────────────────────────────────────────────────────────────────────┘

    ┌─────────────────┐
    │   Deep (Deep)   │  ← Strategy Manager
    │                 │     • Analyzes business profile
    │ Creates Strategy│     • Defines target audience
    └─────────┬───────┘     • Sets budget allocation
              │
              ▼
    ┌─────────────────┐
    │  Ravi (Ravi)    │  ← Digital Marketing Executive
    │                 │     • Receives strategy from Deep
    │ Delegates Tasks │     • Breaks down into daily/weekly/monthly tasks
    └─────────┬───────┘     • Routes tasks to appropriate agents
              │
              ▼
    ┌─────────────────────────────────────────────────────────────────────────────┐
    │                              SMART ROUTING                                 │
    │                                                                             │
    │  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐  │
    │  │   Route to  │    │   Route to  │    │   Route to  │    │   Route to  │  │
    │  │   Content   │    │   Design    │    │ Scheduling  │    │  Analysis   │  │
    │  └─────┬───────┘    └─────┬───────┘    └─────┬───────┘    └─────┬───────┘  │
    │        │                  │                  │                  │          │
    │        ▼                  ▼                  ▼                  ▼          │
    │  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐  │
    │  │   Twinkle   │    │   Pritesh   │    │    Dhruv    │    │   Dhruvil   │  │
    │  │(Content     │    │(Graphic     │    │(Task        │    │(Data        │  │
    │  │ Writer)     │    │ Designer)   │    │ Scheduler)  │    │ Insights)   │  │
    │  │             │    │             │    │             │    │             │  │
    │  │• Creates    │    │• Creates    │    │• Schedules  │    │• Analyzes   │  │
    │  │  written    │    │  visual     │    │  content    │    │  platform   │  │
    │  │  content    │    │  content    │    │  across     │    │  data       │  │
    │  │• Optimizes  │    │• Follows    │    │  platforms  │    │• Generates  │  │
    │  │  for SEO    │    │• Maintains  │    │• Optimizes  │    │• Tracks     │  │
    │  │• Maintains  │    │  brand      │    │  timing     │    │• Reports    │  │
    │  │  brand voice│    │• Ensures    │    │• Reports    │    │  metrics    │  │
    │  └─────────────┘    │  consistency│    │  to client  │    └─────────────┘  │
    │                     └─────────────┘    └─────────────┘           │        │
    └─────────────────────────────────────────────────────────────────┼────────┘
                                                                      │
                                                                      ▼
    ┌─────────────────────────────────────────────────────────────────────────────┐
    │                              FEEDBACK LOOP                                 │
    │                                                                             │
    │  Data Insights → Strategy Refinement → Improved Tasks → Better Results     │
    │                                                                             │
    │  • Performance metrics inform strategy adjustments                          │
    │  • A/B testing results guide content optimization                          │
    │  • Engagement data shapes platform priorities                              │
    │  • ROI analysis drives budget reallocation                                 │
    └─────────────────────────────────────────────────────────────────────────────┘
    """
    
    print(workflow)
    print()


def show_workflow_details():
    """Show detailed workflow information"""
    
    print("📋 WORKFLOW DETAILS")
    print("=" * 50)
    print()
    
    # Workflow nodes
    print("🔗 WORKFLOW NODES:")
    print("-" * 20)
    nodes = [
        ("strategy_manager", "Deep (Strategy Manager)", "Entry point - Creates marketing strategy"),
        ("digital_marketing_executive", "Ravi (Digital Marketing Executive)", "Coordinates tasks and delegates work"),
        ("route_content_tasks", "Route to Content Tasks", "Smart routing based on task requirements"),
        ("content_writer", "Twinkle (Content Writer)", "Creates written content for multiple platforms"),
        ("route_design_tasks", "Route to Design Tasks", "Smart routing based on task requirements"),
        ("graphic_designer", "Pritesh (Graphic Designer)", "Creates visual content following brand guidelines"),
        ("route_scheduling", "Route to Scheduling", "Smart routing based on task requirements"),
        ("task_scheduler", "Dhruv (Task Scheduler)", "Schedules content across different platforms"),
        ("route_analysis", "Route to Analysis", "Smart routing based on task requirements"),
        ("data_insights_manager", "Dhruvil (Data Insights Manager)", "Analyzes performance data and provides insights")
    ]
    
    for i, (node_id, name, description) in enumerate(nodes, 1):
        print(f"{i:2d}. {node_id:25s} | {name:35s} | {description}")
    
    print()
    
    # Conditional edges
    print("🔄 CONDITIONAL EDGES:")
    print("-" * 20)
    edges = [
        ("strategy_manager", "digital_marketing_executive", "Always"),
        ("digital_marketing_executive", "route_content_tasks", "Always"),
        ("route_content_tasks", "content_writer", "If content tasks exist"),
        ("route_content_tasks", "route_design_tasks", "If no content tasks"),
        ("content_writer", "route_design_tasks", "Always"),
        ("route_design_tasks", "graphic_designer", "If design tasks exist"),
        ("route_design_tasks", "route_scheduling", "If no design tasks"),
        ("graphic_designer", "route_scheduling", "Always"),
        ("route_scheduling", "task_scheduler", "If content/designs exist"),
        ("route_scheduling", "route_analysis", "If no content/designs"),
        ("task_scheduler", "route_analysis", "Always"),
        ("route_analysis", "data_insights_manager", "Always"),
        ("data_insights_manager", "strategy_manager", "Feedback loop")
    ]
    
    for i, (from_node, to_node, condition) in enumerate(edges, 1):
        print(f"{i:2d}. {from_node:25s} → {to_node:25s} | {condition}")
    
    print()
    
    # State management
    print("📊 STATE MANAGEMENT:")
    print("-" * 20)
    state_fields = [
        "user_id: str",
        "business_profile: Dict[str, Any]",
        "current_task: Optional[str]",
        "task_type: Optional[str]",
        "content: Optional[str]",
        "design_requirements: Optional[Dict[str, Any]]",
        "scheduling_requirements: Optional[Dict[str, Any]]",
        "data_insights: Optional[Dict[str, Any]]",
        "strategy: Optional[Dict[str, Any]]",
        "agent_outputs: Dict[str, Any]",
        "workflow_status: str",
        "error_message: Optional[str]"
    ]
    
    print("AgentState contains:")
    for field in state_fields:
        print(f"  • {field}")
    
    print()


def show_agent_workflow():
    """Show the agent workflow process"""
    
    print("🔄 AGENT WORKFLOW PROCESS")
    print("=" * 50)
    print()
    
    workflow_steps = [
        {
            "phase": "Phase 1: Strategy Development",
            "agent": "Deep (Strategy Manager)",
            "actions": [
                "Analyzes business profile and goals",
                "Creates comprehensive marketing strategy",
                "Defines target audience and platform strategy",
                "Sets budget allocation and timelines",
                "Generates actionable plan"
            ]
        },
        {
            "phase": "Phase 2: Task Delegation",
            "agent": "Ravi (Digital Marketing Executive)",
            "actions": [
                "Receives strategy from Deep",
                "Breaks down strategy into actionable tasks",
                "Creates daily, weekly, and monthly task breakdown",
                "Delegates tasks to appropriate agents",
                "Monitors task progress and deadlines"
            ]
        },
        {
            "phase": "Phase 3: Content Creation",
            "agent": "Twinkle & Pritesh (Content & Design)",
            "actions": [
                "Twinkle creates written content for multiple platforms",
                "Pritesh creates visual content following brand guidelines",
                "Both agents optimize content for their respective platforms",
                "Content is prepared for scheduling",
                "Both send content to Dhruv for scheduling"
            ]
        },
        {
            "phase": "Phase 4: Content Scheduling",
            "agent": "Dhruv (Task Scheduler)",
            "actions": [
                "Receives content from Twinkle and Pritesh",
                "Optimizes posting times for maximum engagement",
                "Schedules content across different platforms",
                "Manages content calendar and ensures consistent posting",
                "Generates reports for client manager"
            ]
        },
        {
            "phase": "Phase 5: Data Analysis",
            "agent": "Dhruvil (Data Insights Manager)",
            "actions": [
                "Collects data from various advertising platforms",
                "Analyzes performance metrics and trends",
                "Identifies opportunities and risks",
                "Generates insights and recommendations",
                "Provides data to Deep for strategy refinement"
            ]
        }
    ]
    
    for i, step in enumerate(workflow_steps, 1):
        print(f"{i}. {step['phase']}")
        print(f"   Agent: {step['agent']}")
        print("   Actions:")
        for action in step['actions']:
            print(f"     • {action}")
        print()


def show_api_endpoints():
    """Show available API endpoints"""
    
    print("🌐 API ENDPOINTS")
    print("=" * 50)
    print()
    
    endpoints = [
        ("POST", "/api/v1/agents/workflow/execute", "Execute complete workflow"),
        ("POST", "/api/v1/agents/task/execute", "Execute specific task"),
        ("POST", "/api/v1/agents/content/create", "Create content using Twinkle"),
        ("POST", "/api/v1/agents/design/create", "Create design using Pritesh"),
        ("POST", "/api/v1/agents/content/schedule", "Schedule content using Dhruv"),
        ("POST", "/api/v1/agents/data/analyze", "Analyze data using Dhruvil"),
        ("POST", "/api/v1/agents/strategy/develop", "Develop strategy using Deep"),
        ("GET", "/api/v1/agents/workflow/status", "Get workflow status"),
        ("GET", "/api/v1/agents/agents/list", "List all agents")
    ]
    
    for method, endpoint, description in endpoints:
        print(f"{method:6s} {endpoint:35s} | {description}")
    
    print()


if __name__ == "__main__":
    print("🎨 DIGITAL MARKETING AGENT SYSTEM - WORKFLOW VISUALIZATION")
    print("=" * 70)
    print()
    
    # Show the workflow graph
    show_workflow_graph()
    
    # Show workflow details
    show_workflow_details()
    
    # Show agent workflow process
    show_agent_workflow()
    
    # Show API endpoints
    show_api_endpoints()
    
    print("🎉 Workflow visualization complete!")
    print("📁 The system is ready to use with the above workflow structure.") 