"""
FinVerse Plugin - Finance Education Platform
Provides financial education capabilities and curriculum mapping.
Uses Manim for financial chart visualizations.
"""

import sys
from pathlib import Path
from typing import Dict, List, Any

# Add the engine path for imports
engine_path = Path(__file__).parent.parent.parent / "open-source" / "engine"
sys.path.insert(0, str(engine_path))

from plugin_interface import IVerticalPlugin
from schema.base_models import ConceptNode
from legacy_core.manim_wrapper.scene_manager import SceneManager, RenderJob


class FinVersePlugin(IVerticalPlugin):
    """Finance-specific plugin for VisualVerse with Manim integration"""
    
    def __init__(self):
        super().__init__()
        self.display_name = "Finance"
        self.version = "1.0.0"
        self.subject_id = "finance"
        self.scene_manager = SceneManager()
        self.render_queue: Dict[str, RenderJob] = {}
        
    @property
    def plugin_name(self) -> str:
        return "finance"
        
    def get_concept_map(self):
        """Return finance concepts and dependencies"""
        concepts = {
            "time_value_money": ConceptNode(
                id="time_value_money",
                title="Time Value of Money",
                description="Understanding present and future value calculations",
                difficulty="intermediate",
                prerequisites=[],
                estimated_duration=75
            ),
            "portfolio_theory": ConceptNode(
                id="portfolio_theory",
                title="Portfolio Theory",
                description="Modern portfolio theory and risk-return optimization",
                difficulty="advanced",
                prerequisites=["time_value_money"],
                estimated_duration=120
            )
        }
        return concepts
        
    def create_lesson(self, lesson_id: str, content: str) -> str:
        """Create finance-specific animations using Manim"""
        config = self._parse_finance_content(content)
        return self.scene_manager.create_math_scene(config)
        
    def create_financial_chart(
        self,
        data_points: List[float],
        labels: List[str] = None,
        title: str = "Financial Chart",
        chart_type: str = "line"
    ) -> str:
        """
        Create a financial chart visualization.
        
        Args:
            data_points: List of financial data values
            labels: Optional labels for data points
            title: Title for the chart
            chart_type: Type of chart (line, bar)
            
        Returns:
            Path to the rendered video file
        """
        # Convert to function graph for Manim
        functions = []
        for i, value in enumerate(data_points):
            functions.append({
                "function": f"{value}",
                "color": "GREEN" if value >= 0 else "RED"
            })
            
        math_config = {
            "class_name": f"FinVerse{title.replace(' ', '')}",
            "title": title,
            "functions": functions,
            "equations": [],
            "show_axes": True,
            "output_name": f"finance_{title.lower().replace(' ', '_')}"
        }
        return self.scene_manager.create_math_scene(math_config)
        
    def create_cash_flow_diagram(
        self,
        cash_flows: List[Dict[str, Any]],
        title: str = "Cash Flow Diagram"
    ) -> str:
        """
        Create a cash flow timeline visualization.
        
        Args:
            cash_flows: List of cash flows with 'period', 'amount', 'type' (inflow/outflow)
            title: Title for the diagram
            
        Returns:
            Path to the rendered video file
        """
        config = {
            "class_name": f"CashFlow{title.replace(' ', '')}",
            "title": title,
            "text": [f"Period {cf['period']}: ${cf['amount']} ({cf['type']})" for cf in cash_flows],
            "equations": [],
            "output_name": f"cashflow_{title.lower().replace(' ', '_')}"
        }
        return self.scene_manager.create_scene(config)
        
    def create_portfolio_visualization(
        self,
        assets: List[Dict[str, Any]],
        title: str = "Portfolio Allocation"
    ) -> str:
        """
        Create a portfolio allocation visualization.
        
        Args:
            assets: List of assets with 'name', 'allocation', 'return', 'risk'
            title: Title for the visualization
            
        Returns:
            Path to the rendered video file
        """
        text_content = [f"{asset['name']}: {asset['allocation']}% allocation" for asset in assets]
        
        config = {
            "class_name": f"Portfolio{title.replace(' ', '')}",
            "title": title,
            "text": text_content,
            "equations": [],
            "output_name": f"portfolio_{title.lower().replace(' ', '_')}"
        }
        return self.scene_manager.create_scene(config)
        
    def create_risk_return_plot(
        self,
        investments: List[Dict[str, Any]],
        title: str = "Risk vs Return"
    ) -> str:
        """
        Create a risk-return scatter plot.
        
        Args:
            investments: List of investments with 'name', 'risk', 'return'
            title: Title for the plot
            
        Returns:
            Path to the rendered video file
        """
        math_config = {
            "class_name": f"RiskReturn{title.replace(' ', '')}",
            "title": title,
            "functions": [],
            "equations": ["\\text{Risk-Return Analysis}"],
            "show_axes": True,
            "output_name": f"riskreturn_{title.lower().replace(' ', '_')}"
        }
        return self.scene_manager.create_math_scene(math_config)
        
    def queue_render_job(
        self,
        job_id: str,
        scene_config: Dict[str, Any],
        priority: int = 0
    ) -> str:
        """Queue a rendering job for asynchronous processing."""
        job = RenderJob(job_id, scene_config, priority)
        self.render_queue[job_id] = job
        return job_id
        
    def get_render_status(self, job_id: str) -> Dict[str, Any]:
        """Get the status of a render job."""
        if job_id not in self.render_queue:
            return {"status": "not_found", "error": f"Job {job_id} not found"}
            
        job = self.render_queue[job_id]
        return {
            "job_id": job.job_id,
            "status": job.status,
            "result": job.result,
            "priority": job.priority
        }
        
    def get_subject_specific_objects(self):
        """Return Manim objects for finance"""
        return {
            "financial_charts": {
                "description": "Stock price and financial data charts",
                "manim_classes": ["Axes", "Line", "Dot"]
            },
            "cash_flow_diagrams": {
                "description": "Cash flow timeline visualizations",
                "manim_classes": ["Line", "Arrow", "Text"]
            },
            "risk_return_plots": {
                "description": "Risk-return optimization graphs",
                "manim_classes": ["Axes", "Dot", "Line"]
            },
            "bond_diagrams": {
                "description": "Bond pricing and yield calculations",
                "manim_classes": ["Axes", "Line", "MathTex"]
            },
            "option_payoffs": {
                "description": "Option strategy payoff diagrams",
                "manim_classes": ["Axes", "Line", "MathTex"]
            }
        }
        
    def validate_content(self, content: str) -> bool:
        """Validate finance content"""
        finance_indicators = ['stock', 'bond', 'portfolio', 'risk', 'return', 'cash', 'investment']
        content_lower = content.lower()
        finance_count = sum(1 for indicator in finance_indicators if indicator in content_lower)
        return len(content.strip()) > 10 and finance_count >= 1
        
    def _parse_finance_content(self, content: str) -> Dict[str, Any]:
        """Parse finance content to extract visualization configuration."""
        config = {
            "class_name": "FinVerseLesson",
            "title": "Finance Lesson",
            "functions": [],
            "equations": [],
            "show_axes": True,
            "output_name": "finance_lesson"
        }
        
        # Extract LaTeX equations
        import re
        latex_patterns = re.findall(r'\$.*?\$', content)
        for latex in latex_patterns:
            config["equations"].append(latex.strip('$'))
            
        return config
        
    def cleanup(self):
        """Clean up resources"""
        self.scene_manager.cleanup()
        self.render_queue.clear()
