"""
Test script for the Digital Marketing Agent System
Demonstrates the functionality of all agents
"""

import asyncio
import json
from datetime import datetime
from app.agents.workflow_orchestrator import WorkflowOrchestrator


async def test_agent_system():
    """Test the complete agent system"""
    print("🤖 Testing Digital Marketing Agent System")
    print("=" * 50)
    
    # Initialize workflow orchestrator
    orchestrator = WorkflowOrchestrator()
    
    # Sample business profile
    business_profile = {
        "business_name": "TechStart Solutions",
        "business_type": "technology",
        "industry": "technology",
        "target_audience": ["young professionals", "tech entrepreneurs", "startups"],
        "business_goals": ["increase brand awareness", "generate leads", "establish thought leadership"],
        "brand_voice": "professional",
        "brand_colors": ["#2563eb", "#1e40af", "#3b82f6"],
        "brand_fonts": ["Inter", "Roboto"],
        "brand_style": "modern",
        "unique_selling_proposition": "AI-powered business solutions for modern companies"
    }
    
    print(f"📊 Business Profile: {business_profile['business_name']}")
    print(f"🏭 Industry: {business_profile['industry']}")
    print(f"🎯 Target Audience: {', '.join(business_profile['target_audience'])}")
    print()
    
    # Test 1: Complete Workflow
    print("🔄 Test 1: Complete Workflow Execution")
    print("-" * 30)
    
    try:
        result = orchestrator.execute_workflow(
            user_id="test_user_123",
            business_profile=business_profile,
            task_type="strategy_development"
        )
        
        print(f"✅ Workflow Status: {result['workflow_status']}")
        if result.get('strategy'):
            print(f"📋 Strategy Created: {result['strategy'].get('strategy_overview', 'N/A')[:100]}...")
        
        if result.get('agent_outputs'):
            outputs = result['agent_outputs']
            if 'task_breakdown' in outputs:
                tasks = outputs['task_breakdown']
                print(f"📝 Tasks Created: {len(tasks.get('daily_tasks', []))} daily, {len(tasks.get('weekly_tasks', []))} weekly, {len(tasks.get('monthly_tasks', []))} monthly")
            
            if 'insights_report' in outputs:
                insights = outputs['insights_report']
                print(f"📈 Insights Generated: {len(insights.get('key_insights', []))} key insights")
        
        print()
        
    except Exception as e:
        print(f"❌ Workflow Error: {str(e)}")
        print()
    
    # Test 2: Content Creation
    print("✍️ Test 2: Content Creation")
    print("-" * 30)
    
    try:
        result = orchestrator.execute_specific_task(
            user_id="test_user_123",
            business_profile=business_profile,
            task_type="content_creation",
            task_data={"content_requirements": "Create a LinkedIn post about AI in business"}
        )
        
        print(f"✅ Content Creation Status: {result['workflow_status']}")
        if result.get('agent_outputs', {}).get('written_content'):
            content = result['agent_outputs']['written_content']
            print(f"📄 Content Created: {len(content)} pieces")
            for i, piece in enumerate(content[:2]):  # Show first 2 pieces
                print(f"   {i+1}. {piece.get('content', {}).get('title', 'No title')}")
        
        print()
        
    except Exception as e:
        print(f"❌ Content Creation Error: {str(e)}")
        print()
    
    # Test 3: Design Creation
    print("🎨 Test 3: Design Creation")
    print("-" * 30)
    
    try:
        result = orchestrator.execute_specific_task(
            user_id="test_user_123",
            business_profile=business_profile,
            task_type="design_creation",
            task_data={
                "design_requirements": {
                    "content_type": "social_media_post",
                    "platform": "instagram",
                    "message": "AI is transforming business",
                    "call_to_action": "Learn more about our AI solutions"
                }
            }
        )
        
        print(f"✅ Design Creation Status: {result['workflow_status']}")
        if result.get('agent_outputs', {}).get('design_content'):
            designs = result['agent_outputs']['design_content']
            print(f"🎨 Designs Created: {len(designs)} pieces")
            for i, design in enumerate(designs[:2]):  # Show first 2 designs
                print(f"   {i+1}. {design.get('type', 'Unknown')} for {design.get('platform', 'Unknown')}")
        
        print()
        
    except Exception as e:
        print(f"❌ Design Creation Error: {str(e)}")
        print()
    
    # Test 4: Data Analysis
    print("📊 Test 4: Data Analysis")
    print("-" * 30)
    
    try:
        result = orchestrator.execute_specific_task(
            user_id="test_user_123",
            business_profile=business_profile,
            task_type="data_analysis",
            task_data={"data_requirements": {"analysis_period": "last_30_days"}}
        )
        
        print(f"✅ Data Analysis Status: {result['workflow_status']}")
        if result.get('agent_outputs', {}).get('insights_report'):
            insights = result['agent_outputs']['insights_report']
            print(f"📈 Analysis Complete: {insights.get('summary', {}).get('total_content_scheduled', 0)} content pieces analyzed")
            print(f"🎯 Top Platform: {insights.get('executive_summary', {}).get('top_performing_platform', 'N/A')}")
        
        print()
        
    except Exception as e:
        print(f"❌ Data Analysis Error: {str(e)}")
        print()
    
    # Test 5: Workflow Status
    print("📋 Test 5: Workflow Status")
    print("-" * 30)
    
    try:
        status = orchestrator.get_workflow_status()
        print(f"✅ Workflow Status: {status['workflow_status']}")
        print(f"🤖 Active Agents: {len(status['agents'])}")
        for agent_name, agent_info in status['agents'].items():
            print(f"   • {agent_info['name']} ({agent_info['role']}) - {agent_info['status']}")
        
        print()
        
    except Exception as e:
        print(f"❌ Status Error: {str(e)}")
        print()
    
    print("🎉 Agent System Test Complete!")
    print("=" * 50)


def test_individual_agents():
    """Test individual agents without async"""
    print("🧪 Testing Individual Agents")
    print("=" * 30)
    
    # Test Strategy Manager
    print("📋 Testing Strategy Manager (Deep)")
    try:
        from app.agents.strategy_manager import StrategyManager
        strategy_manager = StrategyManager()
        print(f"✅ Strategy Manager initialized: {strategy_manager.name}")
    except Exception as e:
        print(f"❌ Strategy Manager Error: {str(e)}")
    
    # Test Digital Marketing Executive
    print("📊 Testing Digital Marketing Executive (Ravi)")
    try:
        from app.agents.digital_marketing_executive import DigitalMarketingExecutive
        dme = DigitalMarketingExecutive()
        print(f"✅ Digital Marketing Executive initialized: {dme.name}")
    except Exception as e:
        print(f"❌ Digital Marketing Executive Error: {str(e)}")
    
    # Test Content Writer
    print("✍️ Testing Content Writer (Twinkle)")
    try:
        from app.agents.content_writer import ContentWriter
        writer = ContentWriter()
        print(f"✅ Content Writer initialized: {writer.name}")
    except Exception as e:
        print(f"❌ Content Writer Error: {str(e)}")
    
    # Test Graphic Designer
    print("🎨 Testing Graphic Designer (Pritesh)")
    try:
        from app.agents.graphic_designer import GraphicDesigner
        designer = GraphicDesigner()
        print(f"✅ Graphic Designer initialized: {designer.name}")
    except Exception as e:
        print(f"❌ Graphic Designer Error: {str(e)}")
    
    # Test Task Scheduler
    print("📅 Testing Task Scheduler (Dhruv)")
    try:
        from app.agents.task_scheduler import TaskScheduler
        scheduler = TaskScheduler()
        print(f"✅ Task Scheduler initialized: {scheduler.name}")
    except Exception as e:
        print(f"❌ Task Scheduler Error: {str(e)}")
    
    # Test Data Insights Manager
    print("📊 Testing Data Insights Manager (Dhruvil)")
    try:
        from app.agents.data_insights_manager import DataInsightsManager
        analyst = DataInsightsManager()
        print(f"✅ Data Insights Manager initialized: {analyst.name}")
    except Exception as e:
        print(f"❌ Data Insights Manager Error: {str(e)}")
    
    print("=" * 30)


if __name__ == "__main__":
    print("🚀 Starting Agent System Tests")
    print()
    
    # Test individual agents first
    test_individual_agents()
    print()
    
    # Test complete workflow
    try:
        asyncio.run(test_agent_system())
    except Exception as e:
        print(f"❌ Async test failed: {str(e)}")
        print("This might be due to missing dependencies or configuration.") 