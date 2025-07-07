"""
Workflow Visualization Script
Creates a visual representation of the agent workflow
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, ConnectionPatch
import numpy as np


def create_workflow_visualization():
    """Create a visual representation of the agent workflow"""
    
    # Create figure and axis
    fig, ax = plt.subplots(1, 1, figsize=(16, 12))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 12)
    ax.axis('off')
    
    # Define colors for different agent types
    colors = {
        'strategy': '#FF6B6B',      # Red for strategy
        'coordination': '#4ECDC4',  # Teal for coordination
        'content': '#45B7D1',       # Blue for content
        'design': '#96CEB4',        # Green for design
        'scheduling': '#FFEAA7',    # Yellow for scheduling
        'analysis': '#DDA0DD',      # Purple for analysis
        'routing': '#F8F9FA'        # Light gray for routing
    }
    
    # Define agent positions and properties
    agents = {
        'strategy_manager': {
            'pos': (5, 10),
            'name': 'Deep\n(Strategy Manager)',
            'color': colors['strategy'],
            'description': 'Creates marketing\nstrategies'
        },
        'digital_marketing_executive': {
            'pos': (5, 8.5),
            'name': 'Ravi\n(Digital Marketing\nExecutive)',
            'color': colors['coordination'],
            'description': 'Coordinates tasks\nand delegates work'
        },
        'route_content_tasks': {
            'pos': (2, 7),
            'name': 'Route to\nContent Tasks',
            'color': colors['routing'],
            'description': 'Smart routing\nbased on tasks'
        },
        'content_writer': {
            'pos': (1, 5.5),
            'name': 'Twinkle\n(Content Writer)',
            'color': colors['content'],
            'description': 'Creates written\ncontent'
        },
        'route_design_tasks': {
            'pos': (5, 7),
            'name': 'Route to\nDesign Tasks',
            'color': colors['routing'],
            'description': 'Smart routing\nbased on tasks'
        },
        'graphic_designer': {
            'pos': (5, 5.5),
            'name': 'Pritesh\n(Graphic Designer)',
            'color': colors['design'],
            'description': 'Creates visual\ncontent'
        },
        'route_scheduling': {
            'pos': (8, 7),
            'name': 'Route to\nScheduling',
            'color': colors['routing'],
            'description': 'Smart routing\nbased on tasks'
        },
        'task_scheduler': {
            'pos': (8, 5.5),
            'name': 'Dhruv\n(Task Scheduler)',
            'color': colors['scheduling'],
            'description': 'Schedules content\nacross platforms'
        },
        'route_analysis': {
            'pos': (5, 4),
            'name': 'Route to\nAnalysis',
            'color': colors['routing'],
            'description': 'Smart routing\nbased on tasks'
        },
        'data_insights_manager': {
            'pos': (5, 2.5),
            'name': 'Dhruvil\n(Data Insights\nManager)',
            'color': colors['analysis'],
            'description': 'Analyzes performance\ndata'
        }
    }
    
    # Draw agents
    for agent_id, agent_info in agents.items():
        x, y = agent_info['pos']
        name = agent_info['name']
        color = agent_info['color']
        description = agent_info['description']
        
        # Create agent box
        if 'route' in agent_id:
            # Routing nodes are smaller
            box = FancyBboxPatch(
                (x-0.8, y-0.6), 1.6, 1.2,
                boxstyle="round,pad=0.1",
                facecolor=color,
                edgecolor='#333',
                linewidth=2
            )
        else:
            # Agent nodes are larger
            box = FancyBboxPatch(
                (x-1.2, y-0.8), 2.4, 1.6,
                boxstyle="round,pad=0.1",
                facecolor=color,
                edgecolor='#333',
                linewidth=2
            )
        
        ax.add_patch(box)
        
        # Add agent name
        ax.text(x, y+0.2, name, ha='center', va='center', 
                fontsize=10, fontweight='bold', color='#333')
        
        # Add description
        ax.text(x, y-0.2, description, ha='center', va='center', 
                fontsize=8, color='#666')
    
    # Define workflow connections
    connections = [
        # Main workflow flow
        ('strategy_manager', 'digital_marketing_executive'),
        ('digital_marketing_executive', 'route_content_tasks'),
        
        # Content routing
        ('route_content_tasks', 'content_writer'),
        ('content_writer', 'route_design_tasks'),
        
        # Design routing
        ('route_design_tasks', 'graphic_designer'),
        ('graphic_designer', 'route_scheduling'),
        
        # Scheduling routing
        ('route_scheduling', 'task_scheduler'),
        ('task_scheduler', 'route_analysis'),
        
        # Analysis routing
        ('route_analysis', 'data_insights_manager'),
        
        # Alternative routes (dashed lines)
        ('route_content_tasks', 'route_design_tasks'),
        ('route_design_tasks', 'route_scheduling'),
        ('route_scheduling', 'route_analysis'),
    ]
    
    # Draw connections
    for start_agent, end_agent in connections:
        start_pos = agents[start_agent]['pos']
        end_pos = agents[end_agent]['pos']
        
        # Determine line style
        if 'route' in start_agent and 'route' in end_agent:
            # Alternative routes are dashed
            linestyle = '--'
            color = '#999'
            alpha = 0.6
        else:
            # Main workflow is solid
            linestyle = '-'
            color = '#333'
            alpha = 1.0
        
        # Draw connection line
        connection = ConnectionPatch(
            start_pos, end_pos, "data", "data",
            arrowstyle="->", shrinkA=5, shrinkB=5,
            mutation_scale=20, fc=color, ec=color,
            linestyle=linestyle, alpha=alpha, linewidth=2
        )
        ax.add_patch(connection)
    
    # Add feedback loop from data insights to strategy
    feedback_start = agents['data_insights_manager']['pos']
    feedback_end = agents['strategy_manager']['pos']
    
    # Create curved feedback connection
    feedback_connection = ConnectionPatch(
        feedback_start, feedback_end, "data", "data",
        arrowstyle="->", shrinkA=5, shrinkB=5,
        mutation_scale=20, fc='#FF6B6B', ec='#FF6B6B',
        linestyle='-', alpha=0.8, linewidth=3,
        connectionstyle="arc3,rad=0.3"
    )
    ax.add_patch(feedback_connection)
    
    # Add feedback label
    ax.text(8, 6.5, "Feedback Loop\n(Data → Strategy)", 
            ha='center', va='center', fontsize=9, 
            bbox=dict(boxstyle="round,pad=0.3", facecolor='#FFE6E6', alpha=0.8))
    
    # Add title and legend
    ax.text(5, 11.5, 'Digital Marketing Agent System - LangGraph Workflow', 
            ha='center', va='center', fontsize=16, fontweight='bold')
    
    # Add workflow phases
    phases = [
        (1, 11, "Phase 1: Strategy Development", colors['strategy']),
        (1, 10.5, "Phase 2: Task Delegation", colors['coordination']),
        (1, 10, "Phase 3: Content Creation", colors['content']),
        (1, 9.5, "Phase 4: Content Scheduling", colors['scheduling']),
        (1, 9, "Phase 5: Data Analysis", colors['analysis'])
    ]
    
    for x, y, phase, color in phases:
        ax.text(x, y, phase, ha='left', va='center', fontsize=10, fontweight='bold',
                bbox=dict(boxstyle="round,pad=0.2", facecolor=color, alpha=0.3))
    
    # Add legend
    legend_elements = [
        patches.Patch(color=colors['strategy'], label='Strategy'),
        patches.Patch(color=colors['coordination'], label='Coordination'),
        patches.Patch(color=colors['content'], label='Content'),
        patches.Patch(color=colors['design'], label='Design'),
        patches.Patch(color=colors['scheduling'], label='Scheduling'),
        patches.Patch(color=colors['analysis'], label='Analysis'),
        patches.Patch(color=colors['routing'], label='Routing')
    ]
    
    ax.legend(handles=legend_elements, loc='upper right', bbox_to_anchor=(0.98, 0.98))
    
    # Add workflow description
    description_text = """
    Workflow Description:
    • Deep creates marketing strategy based on business profile
    • Ravi breaks down strategy into actionable tasks
    • Smart routing determines which agents to activate
    • Twinkle creates written content, Pritesh creates visual content
    • Dhruv schedules content across platforms
    • Dhruvil analyzes performance data
    • Feedback loop provides insights back to strategy
    """
    
    ax.text(0.5, 1.5, description_text, ha='left', va='top', fontsize=9,
            bbox=dict(boxstyle="round,pad=0.5", facecolor='#F8F9FA', alpha=0.8))
    
    plt.tight_layout()
    return fig


def create_simple_workflow_diagram():
    """Create a simpler ASCII-based workflow diagram"""
    
    diagram = """
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
    │  │  for SEO    │    │  brand      │    │• Optimizes  │    │  insights   │  │
    │  │• Maintains  │    │  guidelines │    │  timing     │    │• Tracks     │  │
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

    ┌─────────────────────────────────────────────────────────────────────────────┐
    │                              WORKFLOW STATES                               │
    │                                                                             │
    │  AgentState:                                                                │
    │  • user_id: str                                                            │
    │  • business_profile: Dict[str, Any]                                        │
    │  • current_task: Optional[str]                                             │
    │  • task_type: Optional[str]                                                │
    │  • content: Optional[str]                                                  │
    │  • design_requirements: Optional[Dict[str, Any]]                           │
    │  • scheduling_requirements: Optional[Dict[str, Any]]                       │
    │  • data_insights: Optional[Dict[str, Any]]                                 │
    │  • strategy: Optional[Dict[str, Any]]                                      │
    │  • agent_outputs: Dict[str, Any]                                           │
    │  • workflow_status: str                                                    │
    │  • error_message: Optional[str]                                            │
    └─────────────────────────────────────────────────────────────────────────────┘
    """
    
    return diagram


def print_workflow_info():
    """Print detailed workflow information"""
    
    info = """
    🔄 LANGGRAPH WORKFLOW DETAILS
    =============================

    📋 WORKFLOW NODES:
    ------------------
    1. strategy_manager (Deep)
       - Entry point of the workflow
       - Creates comprehensive marketing strategy
       - Analyzes business profile and goals

    2. digital_marketing_executive (Ravi)
       - Receives strategy from Deep
       - Breaks down into actionable tasks
       - Creates task delegation plan

    3. route_content_tasks
       - Conditional routing node
       - Determines if content creation is needed
       - Routes to Twinkle or next step

    4. content_writer (Twinkle)
       - Creates written content
       - Handles multiple platforms
       - Optimizes for SEO and engagement

    5. route_design_tasks
       - Conditional routing node
       - Determines if design creation is needed
       - Routes to Pritesh or next step

    6. graphic_designer (Pritesh)
       - Creates visual content
       - Follows brand guidelines
       - Platform-specific design requirements

    7. route_scheduling
       - Conditional routing node
       - Determines if scheduling is needed
       - Routes to Dhruv or next step

    8. task_scheduler (Dhruv)
       - Schedules content across platforms
       - Optimizes posting times
       - Generates client reports

    9. route_analysis
       - Conditional routing node
       - Always routes to data analysis
       - Final step in workflow

    10. data_insights_manager (Dhruvil)
        - Analyzes performance data
        - Generates insights and recommendations
        - Provides feedback for strategy refinement

    🔗 CONDITIONAL EDGES:
    ---------------------
    • route_content_tasks → content_writer (if content tasks exist)
    • route_content_tasks → route_design_tasks (if no content tasks)
    • route_design_tasks → graphic_designer (if design tasks exist)
    • route_design_tasks → route_scheduling (if no design tasks)
    • route_scheduling → task_scheduler (if content/designs exist)
    • route_scheduling → route_analysis (if no content/designs)
    • route_analysis → data_insights_manager (always)

    📊 STATE MANAGEMENT:
    --------------------
    • Shared AgentState across all nodes
    • Each agent updates state with outputs
    • State flows through the entire workflow
    • Error handling preserves state on failures

    🎯 WORKFLOW BENEFITS:
    ---------------------
    • Modular: Each agent has specific responsibilities
    • Scalable: Easy to add new agents or modify existing ones
    • Flexible: Conditional routing based on requirements
    • Robust: Comprehensive error handling and recovery
    • Observable: Full activity logging and state tracking
    """
    
    print(info)


if __name__ == "__main__":
    print("🎨 Creating LangGraph Workflow Visualization...")
    
    # Create and save the visual graph
    try:
        fig = create_workflow_visualization()
        fig.savefig('workflow_diagram.png', dpi=300, bbox_inches='tight')
        print("✅ Visual workflow diagram saved as 'workflow_diagram.png'")
    except Exception as e:
        print(f"❌ Could not create visual diagram: {str(e)}")
    
    # Print ASCII diagram
    print("\n📋 ASCII Workflow Diagram:")
    print(create_simple_workflow_diagram())
    
    # Print detailed workflow information
    print_workflow_info()
    
    print("\n🎉 Workflow visualization complete!")
    print("📁 Check 'workflow_diagram.png' for the visual representation") 