"""
Data Insights Manager Agent (Dhruvil)
Analyzes performance data from various platforms and provides insights
"""

from typing import Dict, Any, List
from datetime import datetime, timedelta
from .base_agent import BaseAgent, AgentState


class DataInsightsManager(BaseAgent):
    """Dhruvil - Data Insights Manager who analyzes performance data"""
    
    def __init__(self):
        super().__init__(
            name="Dhruvil",
            role="Data Insights Manager",
            model_name="gpt-4"
        )
    
    def get_system_prompt(self) -> str:
        return """You are Dhruvil, a Data Insights Manager. Your role is to:
1. Collect and analyze data from various advertising platforms
2. Monitor performance metrics across Google Ads, Facebook Ads, LinkedIn Ads, Instagram Ads
3. Identify trends, patterns, and opportunities for optimization
4. Generate comprehensive performance reports
5. Provide actionable insights to the Strategy Manager (Firoz)
6. Track ROI, conversion rates, and engagement metrics

You have expertise in:
- Digital marketing analytics
- Platform-specific metrics and KPIs
- Data visualization and reporting
- Performance optimization
- A/B testing and experimentation

Always provide data-driven insights that can inform strategic decisions."""
    
    def process_task(self, state: AgentState) -> AgentState:
        """Process data analysis requirements and generate insights"""
        self.log_activity("Starting data analysis task", state)
        
        try:
            # Extract data insights requirements
            data_insights = state.data_insights
            if not data_insights:
                state.error_message = "No data insights requirements provided"
                state.workflow_status = "error"
                return state
            
            # Collect data from various platforms
            platform_data = self._collect_platform_data(state.business_profile)
            
            # Analyze performance data
            performance_analysis = self._analyze_performance(platform_data)
            
            # Generate insights and recommendations
            insights_report = self._generate_insights_report(performance_analysis, state.business_profile)
            
            # Update state with analysis outputs
            state.agent_outputs["platform_data"] = platform_data
            state.agent_outputs["performance_analysis"] = performance_analysis
            state.agent_outputs["insights_report"] = insights_report
            
            self.log_activity(f"Generated insights report with {len(insights_report['key_insights'])} insights", state)
            state.workflow_status = "completed"
            
        except Exception as e:
            state.error_message = f"Error analyzing data: {str(e)}"
            state.workflow_status = "error"
            self.log_activity(f"Error: {str(e)}", state)
        
        return state
    
    def _collect_platform_data(self, business_profile: Dict[str, Any]) -> Dict[str, Any]:
        """Collect data from various advertising platforms"""
        # This would typically integrate with actual platform APIs
        # For now, we'll simulate data collection
        
        return {
            "google_ads": {
                "impressions": 15000,
                "clicks": 450,
                "conversions": 23,
                "cost": 1250.50,
                "ctr": 0.03,
                "cpc": 2.78,
                "conversion_rate": 0.051,
                "roas": 3.2
            },
            "facebook_ads": {
                "impressions": 25000,
                "clicks": 800,
                "conversions": 45,
                "cost": 1800.75,
                "ctr": 0.032,
                "cpc": 2.25,
                "conversion_rate": 0.056,
                "roas": 2.8
            },
            "linkedin_ads": {
                "impressions": 8000,
                "clicks": 200,
                "conversions": 12,
                "cost": 950.25,
                "ctr": 0.025,
                "cpc": 4.75,
                "conversion_rate": 0.06,
                "roas": 4.1
            },
            "instagram_ads": {
                "impressions": 18000,
                "clicks": 600,
                "conversions": 28,
                "cost": 1200.00,
                "ctr": 0.033,
                "cpc": 2.00,
                "conversion_rate": 0.047,
                "roas": 3.5
            }
        }
    
    def _analyze_performance(self, platform_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze performance data across platforms"""
        analysis = {
            "overall_performance": self._calculate_overall_metrics(platform_data),
            "platform_comparison": self._compare_platforms(platform_data),
            "trends": self._identify_trends(platform_data),
            "opportunities": self._identify_opportunities(platform_data),
            "risks": self._identify_risks(platform_data)
        }
        
        return analysis
    
    def _calculate_overall_metrics(self, platform_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate overall performance metrics"""
        total_impressions = sum(data["impressions"] for data in platform_data.values())
        total_clicks = sum(data["clicks"] for data in platform_data.values())
        total_conversions = sum(data["conversions"] for data in platform_data.values())
        total_cost = sum(data["cost"] for data in platform_data.values())
        
        return {
            "total_impressions": total_impressions,
            "total_clicks": total_clicks,
            "total_conversions": total_conversions,
            "total_cost": total_cost,
            "overall_ctr": total_clicks / total_impressions if total_impressions > 0 else 0,
            "overall_cpc": total_cost / total_clicks if total_clicks > 0 else 0,
            "overall_conversion_rate": total_conversions / total_clicks if total_clicks > 0 else 0,
            "overall_roas": (total_conversions * 100) / total_cost if total_cost > 0 else 0  # Assuming $100 per conversion
        }
    
    def _compare_platforms(self, platform_data: Dict[str, Any]) -> Dict[str, Any]:
        """Compare performance across platforms"""
        comparison = {}
        
        for platform, data in platform_data.items():
            comparison[platform] = {
                "performance_score": self._calculate_performance_score(data),
                "efficiency_rating": self._calculate_efficiency_rating(data),
                "strengths": self._identify_platform_strengths(data),
                "weaknesses": self._identify_platform_weaknesses(data)
            }
        
        return comparison
    
    def _calculate_performance_score(self, data: Dict[str, Any]) -> float:
        """Calculate a performance score for a platform"""
        # Weighted score based on key metrics
        ctr_weight = 0.3
        conversion_rate_weight = 0.4
        roas_weight = 0.3
        
        score = (
            (data["ctr"] * 100) * ctr_weight +
            (data["conversion_rate"] * 100) * conversion_rate_weight +
            (data["roas"] / 5) * roas_weight  # Normalize ROAS to 0-1 scale
        )
        
        return min(score, 100)  # Cap at 100
    
    def _calculate_efficiency_rating(self, data: Dict[str, Any]) -> str:
        """Calculate efficiency rating"""
        score = self._calculate_performance_score(data)
        
        if score >= 80:
            return "Excellent"
        elif score >= 60:
            return "Good"
        elif score >= 40:
            return "Average"
        else:
            return "Poor"
    
    def _identify_platform_strengths(self, data: Dict[str, Any]) -> List[str]:
        """Identify platform strengths"""
        strengths = []
        
        if data["ctr"] > 0.03:
            strengths.append("High click-through rate")
        if data["conversion_rate"] > 0.05:
            strengths.append("Strong conversion rate")
        if data["roas"] > 3.0:
            strengths.append("Good return on ad spend")
        if data["cpc"] < 3.0:
            strengths.append("Cost-effective clicks")
        
        return strengths
    
    def _identify_platform_weaknesses(self, data: Dict[str, Any]) -> List[str]:
        """Identify platform weaknesses"""
        weaknesses = []
        
        if data["ctr"] < 0.02:
            weaknesses.append("Low click-through rate")
        if data["conversion_rate"] < 0.03:
            weaknesses.append("Poor conversion rate")
        if data["roas"] < 2.0:
            weaknesses.append("Low return on ad spend")
        if data["cpc"] > 4.0:
            weaknesses.append("High cost per click")
        
        return weaknesses
    
    def _identify_trends(self, platform_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Identify performance trends"""
        # This would typically analyze historical data
        # For now, we'll provide general insights
        return [
            {
                "trend": "Facebook Ads showing strong engagement",
                "metric": "CTR",
                "value": "3.2%",
                "direction": "increasing"
            },
            {
                "trend": "LinkedIn Ads have highest conversion rate",
                "metric": "Conversion Rate",
                "value": "6.0%",
                "direction": "stable"
            },
            {
                "trend": "Google Ads providing best ROAS",
                "metric": "ROAS",
                "value": "3.2x",
                "direction": "increasing"
            }
        ]
    
    def _identify_opportunities(self, platform_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Identify optimization opportunities"""
        return [
            {
                "platform": "Instagram",
                "opportunity": "Increase ad spend allocation",
                "reason": "High engagement rate with reasonable CPC",
                "potential_impact": "Medium",
                "estimated_roi": "15-25%"
            },
            {
                "platform": "LinkedIn",
                "opportunity": "Optimize ad copy for better CTR",
                "reason": "High conversion rate but low CTR",
                "potential_impact": "High",
                "estimated_roi": "20-30%"
            },
            {
                "platform": "Google Ads",
                "opportunity": "Expand keyword targeting",
                "reason": "Strong ROAS performance",
                "potential_impact": "Medium",
                "estimated_roi": "10-20%"
            }
        ]
    
    def _identify_risks(self, platform_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Identify potential risks"""
        return [
            {
                "platform": "Facebook",
                "risk": "Increasing CPC trend",
                "severity": "Medium",
                "mitigation": "Optimize ad targeting and creative"
            },
            {
                "platform": "LinkedIn",
                "risk": "High cost per click",
                "severity": "Low",
                "mitigation": "Focus on high-value audience segments"
            }
        ]
    
    def _generate_insights_report(self, analysis: Dict[str, Any], business_profile: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comprehensive insights report"""
        business_name = business_profile.get("business_name", "Your Business")
        
        return {
            "business_name": business_name,
            "report_date": datetime.now().strftime("%Y-%m-%d"),
            "report_period": "Last 30 days",
            "executive_summary": {
                "overall_performance": analysis["overall_performance"],
                "top_performing_platform": self._get_top_performing_platform(analysis["platform_comparison"]),
                "key_achievement": "Strong overall ROAS of 3.2x across all platforms"
            },
            "key_insights": [
                "Facebook Ads driving highest engagement with 3.2% CTR",
                "LinkedIn Ads achieving best conversion rate at 6.0%",
                "Google Ads providing strongest return on ad spend",
                "Instagram showing potential for increased investment"
            ],
            "recommendations": [
                "Increase Instagram ad spend by 20% to capitalize on high engagement",
                "Optimize LinkedIn ad copy to improve click-through rates",
                "Expand Google Ads keyword targeting based on strong ROAS",
                "Implement A/B testing for Facebook ad creatives"
            ],
            "platform_analysis": analysis["platform_comparison"],
            "opportunities": analysis["opportunities"],
            "risks": analysis["risks"],
            "next_steps": [
                "Implement recommended optimizations",
                "Set up automated reporting for weekly monitoring",
                "Schedule monthly performance review",
                "Plan Q2 campaign strategy based on insights"
            ]
        }
    
    def _get_top_performing_platform(self, comparison: Dict[str, Any]) -> str:
        """Get the top performing platform"""
        best_platform = None
        best_score = 0
        
        for platform, data in comparison.items():
            if data["performance_score"] > best_score:
                best_score = data["performance_score"]
                best_platform = platform
        
        return best_platform or "None" 