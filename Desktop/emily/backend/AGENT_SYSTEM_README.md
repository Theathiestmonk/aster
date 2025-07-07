# Digital Marketing Agent System

A comprehensive, modular agent system built with LangGraph for digital marketing workflows. The system consists of 6 specialized AI agents that work together to create, manage, and optimize digital marketing campaigns.

## 🤖 Agent Team

### 1. **Deep (Strategy Manager)**
- **Role**: Creates comprehensive marketing strategies
- **Responsibilities**:
  - Analyze business profile and goals
  - Review data insights from other agents
  - Create actionable marketing strategies
  - Design budget allocation and timelines
  - Coordinate with Digital Marketing Executive

### 2. **Ravi (Digital Marketing Executive)**
- **Role**: Coordinates tasks and delegates work
- **Responsibilities**:
  - Receive strategy from Strategy Manager
  - Break down strategy into daily/weekly/monthly tasks
  - Delegate tasks to appropriate agents
  - Monitor task progress and deadlines
  - Ensure workflow efficiency

### 3. **Pritesh (Graphic Designer)**
- **Role**: Creates visual content
- **Responsibilities**:
  - Design graphics, videos, and images
  - Follow brand guidelines and color schemes
  - Create platform-specific visual content
  - Ensure brand consistency
  - Send designs to Task Scheduler

### 4. **Twinkle (Content Writer)**
- **Role**: Creates written content
- **Responsibilities**:
  - Write engaging content for multiple platforms
  - Create Facebook posts, blog articles, Instagram captions
  - Optimize content for SEO and engagement
  - Maintain brand voice and tone
  - Send content to Task Scheduler

### 5. **Dhruv (Task Scheduler)**
- **Role**: Schedules and manages content
- **Responsibilities**:
  - Schedule content across different platforms
  - Optimize posting times for maximum engagement
  - Manage content calendar
  - Generate reports for client manager
  - Handle platform-specific requirements

### 6. **Dhruvil (Data Insights Manager)**
- **Role**: Analyzes performance data
- **Responsibilities**:
  - Collect data from advertising platforms
  - Analyze performance metrics and trends
  - Generate insights and recommendations
  - Track ROI and conversion rates
  - Provide data-driven insights to Strategy Manager

## 🏗️ Architecture

### Modular Design
- Each agent is self-contained with specific responsibilities
- Clean separation of concerns
- Easy to extend and modify individual agents
- Shared state management through LangGraph

### Workflow Orchestration
- **WorkflowOrchestrator**: Coordinates all agents
- **StateGraph**: Manages workflow state and transitions
- **Conditional Routing**: Smart task routing based on requirements
- **Error Handling**: Comprehensive error management

### State Management
```python
class AgentState(BaseModel):
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
```

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- FastAPI
- LangGraph
- LangChain
- OpenAI API key

### Installation
1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables:
```bash
cp env.example .env
# Add your OpenAI API key and other configurations
```

3. Run the test script:
```bash
python test_agents.py
```

### API Endpoints

#### Complete Workflow
```http
POST /api/v1/agents/workflow/execute
{
  "task_type": "strategy_development",
  "task_data": {}
}
```

#### Specific Tasks
```http
POST /api/v1/agents/task/execute
{
  "task_type": "content_creation",
  "task_data": {
    "content_requirements": "Create a LinkedIn post about AI"
  }
}
```

#### Content Creation
```http
POST /api/v1/agents/content/create
{
  "content_requirements": "Write a blog post about digital marketing trends"
}
```

#### Design Creation
```http
POST /api/v1/agents/design/create
{
  "design_requirements": {
    "content_type": "social_media_post",
    "platform": "instagram",
    "message": "AI is transforming business",
    "call_to_action": "Learn more"
  }
}
```

#### Content Scheduling
```http
POST /api/v1/agents/content/schedule
{
  "scheduling_requirements": {
    "content_type": "written_content",
    "platforms": ["facebook", "instagram", "linkedin"],
    "scheduling_priority": "high"
  }
}
```

#### Data Analysis
```http
POST /api/v1/agents/data/analyze
{
  "data_requirements": {
    "analysis_period": "last_30_days"
  }
}
```

#### Strategy Development
```http
POST /api/v1/agents/strategy/develop
{
  "business_goals": ["increase brand awareness", "generate leads"],
  "target_audience": ["young professionals", "tech entrepreneurs"]
}
```

## 📊 Workflow Process

### 1. Strategy Development
1. **Deep** analyzes business profile and goals
2. Creates comprehensive marketing strategy
3. Defines target audience, platform strategy, and budget allocation
4. Generates actionable plan

### 2. Task Delegation
1. **Ravi** receives strategy from Deep
2. Breaks down strategy into actionable tasks
3. Creates daily, weekly, and monthly task breakdown
4. Delegates tasks to appropriate agents

### 3. Content Creation
1. **Twinkle** creates written content based on requirements
2. **Pritesh** creates visual content following brand guidelines
3. Both agents send content to **Dhruv** for scheduling

### 4. Content Scheduling
1. **Dhruv** receives content from Twinkle and Pritesh
2. Optimizes posting times for maximum engagement
3. Schedules content across different platforms
4. Generates reports for client manager

### 5. Data Analysis
1. **Dhruvil** collects data from various platforms
2. Analyzes performance metrics and trends
3. Generates insights and recommendations
4. Provides data to **Deep** for strategy refinement

## 🔧 Configuration

### Environment Variables
```bash
OPENAI_API_KEY=your_openai_api_key
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
```

### Agent Configuration
Each agent can be configured with:
- **Model**: GPT-4 (default) or other OpenAI models
- **Temperature**: Controls creativity (0.7 default)
- **System Prompt**: Customizable role descriptions

## 📈 Features

### Smart Routing
- Conditional workflow routing based on task requirements
- Automatic agent selection based on task type
- Dynamic workflow adaptation

### Comprehensive Reporting
- Detailed agent activity logs
- Performance metrics and insights
- Client-ready reports
- Progress tracking

### Platform Integration
- Support for multiple social media platforms
- Platform-specific optimizations
- Cross-platform content adaptation

### Error Handling
- Comprehensive error management
- Graceful failure recovery
- Detailed error reporting
- State preservation

## 🧪 Testing

### Run Tests
```bash
python test_agents.py
```

### Test Individual Agents
```python
from app.agents.strategy_manager import StrategyManager
from app.agents.content_writer import ContentWriter

# Test strategy manager
strategy_manager = StrategyManager()
# Test content writer
content_writer = ContentWriter()
```

### Test Complete Workflow
```python
from app.agents.workflow_orchestrator import WorkflowOrchestrator

orchestrator = WorkflowOrchestrator()
result = orchestrator.execute_workflow(
    user_id="test_user",
    business_profile=business_profile,
    task_type="strategy_development"
)
```

## 🔮 Future Enhancements

### Planned Features
- **Real-time Collaboration**: Live agent communication
- **Advanced Analytics**: Machine learning insights
- **Platform APIs**: Direct integration with social media platforms
- **A/B Testing**: Automated content optimization
- **Multi-language Support**: International market support

### Extensibility
- **Custom Agents**: Easy addition of new specialized agents
- **Plugin System**: Third-party integrations
- **Custom Workflows**: User-defined workflow patterns
- **API Extensions**: Additional endpoints and functionality

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Create an issue in the repository
- Check the documentation
- Review the test examples

---

**Built with ❤️ using LangGraph and FastAPI** 