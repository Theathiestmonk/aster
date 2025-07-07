"""
Test Environment Variables
Simple script to verify environment variables are loaded correctly
"""

import os
from dotenv import load_dotenv

def test_environment():
    """Test if environment variables are loaded correctly"""
    
    print("🔧 Testing Environment Variables")
    print("=" * 40)
    
    # Load environment variables
    load_dotenv()
    
    # Check OpenAI API key
    openai_key = os.getenv("OPENAI_API_KEY")
    if openai_key:
        print("✅ OPENAI_API_KEY found")
        print(f"   Key: {openai_key[:10]}...{openai_key[-4:] if len(openai_key) > 14 else '***'}")
    else:
        print("❌ OPENAI_API_KEY not found")
        print("   Please add OPENAI_API_KEY to your .env file")
    
    # Check other important variables
    variables = [
        "SUPABASE_URL",
        "SUPABASE_ANON_KEY", 
        "SECRET_KEY",
        "DATABASE_URL"
    ]
    
    print("\n📋 Other Environment Variables:")
    for var in variables:
        value = os.getenv(var)
        if value:
            print(f"✅ {var}: Found")
        else:
            print(f"❌ {var}: Not found")
    
    # Test if we can import the agents
    print("\n🤖 Testing Agent Imports:")
    try:
        from app.agents.base_agent import BaseAgent, AgentState
        print("✅ BaseAgent imported successfully")
    except Exception as e:
        print(f"❌ BaseAgent import failed: {str(e)}")
    
    try:
        from app.agents.strategy_manager import StrategyManager
        print("✅ StrategyManager imported successfully")
    except Exception as e:
        print(f"❌ StrategyManager import failed: {str(e)}")
    
    try:
        from app.agents.workflow_orchestrator import WorkflowOrchestrator
        print("✅ WorkflowOrchestrator imported successfully")
    except Exception as e:
        print(f"❌ WorkflowOrchestrator import failed: {str(e)}")
    
    print("\n🎯 Environment Test Complete!")


if __name__ == "__main__":
    test_environment() 