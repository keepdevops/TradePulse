#!/usr/bin/env python3
"""
TradePulse Dashboard Manager - Components
UI components for the dashboard manager
"""

import panel as pn
import logging

logger = logging.getLogger(__name__)

class DashboardManagerComponents:
    """UI components for dashboard manager"""
    
    def __init__(self):
        self.role_switcher = None
        self.search_input = None
        self.status_display = None
        self.navigation_bar = None
    
    def create_basic_components(self):
        """Create basic UI components"""
        # Role switcher
        self.role_switcher = pn.widgets.Select(
            name="🎭 User Role",
            options=[
                ("Day Trader", "day_trader"),
                ("ML AI Trend Analyst", "ml_analyst"),
                ("Default", "default")
            ],
            value="default",
            width=200
        )
        
        # Search input
        self.search_input = pn.widgets.TextInput(
            name="🔍 Search",
            placeholder="Search...",
            width=300
        )
        
        # Status display
        self.status_display = pn.pane.Markdown("""
        ### 📊 Dashboard Status
        - **Role**: Default
        - **Status**: Active
        - **Last Update**: Just now
        """)
        
        # Navigation bar
        self.navigation_bar = pn.Row(
            self.role_switcher,
            self.search_input,
            self.status_display,
            sizing_mode='stretch_width'
        )
    
    def create_role_specific_components(self, role: str):
        """Create role-specific components"""
        if role == "day_trader":
            return self.create_day_trader_components()
        elif role == "ml_analyst":
            return self.create_ml_analyst_components()
        else:
            return self.create_default_components()
    
    def create_day_trader_components(self):
        """Create Day Trader specific components"""
        return {
            'quick_search': pn.widgets.TextInput(
                name="🔍 Quick Search",
                placeholder="Search assets/symbols...",
                width=300
            ),
            'global_alerts': pn.pane.Markdown("📢 **Global Alerts:** Market open, high volatility detected"),
            'market_status': pn.pane.Markdown("📈 **Market Status:** Open")
        }
    
    def create_ml_analyst_components(self):
        """Create ML Analyst specific components"""
        return {
            'advanced_search': pn.widgets.TextInput(
                name="🔍 Advanced Search",
                placeholder="Search datasets/models...",
                width=300
            ),
            'performance_metrics': pn.pane.Markdown("📊 **Performance:** Recent model accuracy: 87.2%"),
            'model_status': pn.pane.Markdown("🤖 **Model Status:** Active")
        }
    
    def create_default_components(self):
        """Create default components"""
        return {
            'basic_search': pn.widgets.TextInput(
                name="🔍 Search",
                placeholder="Search...",
                width=300
            ),
            'status_info': pn.pane.Markdown("📊 **Status:** Ready"),
            'help_text': pn.pane.Markdown("ℹ️ **Help:** Select your role above to customize the dashboard")
        }

