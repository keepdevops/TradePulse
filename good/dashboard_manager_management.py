#!/usr/bin/env python3
"""
TradePulse Dashboard Manager - Management
Layout creation and management for the dashboard manager
"""

import panel as pn
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class DashboardManagerManagement:
    """Layout creation and management for dashboard manager"""
    
    @staticmethod
    def create_day_trader_layout(panels: Dict[str, Any], role_switcher) -> pn.Column:
        """Create Day Traders dashboard layout (3-column grid)"""
        try:
            logger.info("🎯 Creating Day Trader dashboard layout")
            
            # Top navigation with role selector and global alerts
            top_nav = pn.Row(
                role_switcher,
                pn.widgets.TextInput(
                    name="🔍 Quick Search",
                    placeholder="Search assets/symbols...",
                    width=300
                ),
                pn.pane.Markdown("📢 **Global Alerts:** Market open, high volatility detected"),
                sizing_mode='stretch_width'
            )
            
            # Center column (Main Focus, 60% width) - Charts Panel
            center_column = pn.Column(
                pn.pane.Markdown("## 📈 Real-Time Charts"),
                panels.get('📈 Charts', pn.pane.Markdown("Charts panel unavailable")),
                sizing_mode='stretch_width'
            )
            
            # Left column (Monitoring, 20% width) - Alerts Panel
            left_column = pn.Column(
                pn.pane.Markdown("## 🚨 Live Alerts"),
                panels.get('🚨 Alerts', pn.pane.Markdown("Alerts panel unavailable")),
                sizing_mode='stretch_width'
            )
            
            # Right column (Insights, 20% width) - Data Panel
            right_column = pn.Column(
                pn.pane.Markdown("## 📊 Live Data"),
                panels.get('📊 Data', pn.pane.Markdown("Data panel unavailable")),
                sizing_mode='stretch_width'
            )
            
            # Bottom dock - Portfolio and AI panels
            bottom_dock = pn.Row(
                pn.Column(
                    pn.pane.Markdown("## 💼 Portfolio"),
                    panels.get('💼 Portfolio', pn.pane.Markdown("Portfolio panel unavailable"))
                ),
                pn.Column(
                    pn.pane.Markdown("## 🧠 AI Insights"),
                    panels.get('🧠 AI', pn.pane.Markdown("AI panel unavailable"))
                ),
                sizing_mode='stretch_width'
            )
            
            # Main layout with 3-column grid
            layout = pn.Column(
                top_nav,
                pn.Row(
                    left_column,
                    center_column,
                    right_column,
                    sizing_mode='stretch_width'
                ),
                pn.Spacer(height=10),
                bottom_dock,
                sizing_mode='stretch_width'
            )
            
            logger.info("✅ Day Trader layout created successfully")
            return layout
            
        except Exception as e:
            logger.error(f"Failed to create Day Trader layout: {e}")
            return pn.Column("Error: Failed to create Day Trader layout")
    
    @staticmethod
    def create_ml_analyst_layout(panels: Dict[str, Any], role_switcher) -> pn.Column:
        """Create ML AI Trend Analysts dashboard layout (tabbed interface)"""
        try:
            logger.info("🎯 Creating ML AI Analyst dashboard layout")
            
            # Top navigation with role selector and performance metrics
            top_nav = pn.Row(
                role_switcher,
                pn.widgets.TextInput(
                    name="🔍 Advanced Search",
                    placeholder="Search datasets/models...",
                    width=300
                ),
                pn.pane.Markdown("📊 **Performance:** Recent model accuracy: 87.2%"),
                sizing_mode='stretch_width'
            )
            
            # Top section (Data and Models, full width)
            top_section = pn.Column(
                pn.pane.Markdown("## 📊 Data & Models"),
                pn.Row(
                    pn.Column(
                        pn.pane.Markdown("### 📊 Data Management"),
                        panels.get('📊 Data', pn.pane.Markdown("Data panel unavailable"))
                    ),
                    pn.Column(
                        pn.pane.Markdown("### 🤖 Model Training"),
                        panels.get('🤖 Models', pn.pane.Markdown("Models panel unavailable"))
                    ),
                    sizing_mode='stretch_width'
                ),
                sizing_mode='stretch_width'
            )
            
            # Middle section (Analysis, full width)
            middle_section = pn.Column(
                pn.pane.Markdown("## 🧠 AI Analysis"),
                panels.get('🧠 AI', pn.pane.Markdown("AI panel unavailable")),
                sizing_mode='stretch_width'
            )
            
            # Bottom section (Outputs and Insights)
            bottom_section = pn.Row(
                pn.Column(
                    pn.pane.Markdown("## 💼 Portfolio Optimization"),
                    panels.get('💼 Portfolio', pn.pane.Markdown("Portfolio panel unavailable"))
                ),
                pn.Column(
                    pn.pane.Markdown("## 📈 Advanced Charts"),
                    panels.get('📈 Charts', pn.pane.Markdown("Charts panel unavailable"))
                ),
                sizing_mode='stretch_width'
            )
            
            # Side toolbar
            side_toolbar = pn.Column(
                pn.pane.Markdown("## 🚨 Model Alerts"),
                panels.get('🚨 Alerts', pn.pane.Markdown("Alerts panel unavailable")),
                pn.pane.Markdown("## ⚙️ System Monitor"),
                panels.get('⚙️ System', pn.pane.Markdown("System panel unavailable"))
            )
            
            # Main layout with tabbed sections
            layout = pn.Column(
                top_nav,
                pn.Spacer(height=10),
                top_section,
                pn.Spacer(height=10),
                middle_section,
                pn.Spacer(height=10),
                pn.Row(
                    bottom_section,
                    side_toolbar,
                    sizing_mode='stretch_width'
                ),
                sizing_mode='stretch_width'
            )
            
            logger.info("✅ ML AI Analyst layout created successfully")
            return layout
            
        except Exception as e:
            logger.error(f"Failed to create ML AI Analyst layout: {e}")
            return pn.Column("Error: Failed to create ML AI Analyst layout")
    
    @staticmethod
    def create_trend_analyst_layout(panels: Dict[str, Any], role_switcher) -> pn.Column:
        """Create Trend Analyst dashboard layout (tabbed interface with Matplotlib)"""
        try:
            logger.info("🎯 Creating Trend Analyst dashboard layout")
            
            # Create tabbed interface (same as default but with Matplotlib)
            tabs = pn.Tabs()
            
            # Trend Analyst specific panels (all modules plus Matplotlib)
            trend_analyst_panels = {
                '📊 Data': panels.get('📊 Data'),
                '🤖 Models': panels.get('🤖 Models'),
                '💼 Portfolio': panels.get('💼 Portfolio'),
                '🧠 AI': panels.get('🧠 AI'),
                '📈 Charts': panels.get('📈 Charts'),
                '🚨 Alerts': panels.get('🚨 Alerts'),
                '⚙️ System': panels.get('⚙️ System'),
                '📊 Matplotlib': pn.Column(
                    pn.pane.Markdown("### 📊 Matplotlib Visualization"),
                    pn.pane.Markdown("**Advanced trend analysis and plotting tools**"),
                    pn.widgets.Button(name="📈 Trend Plot", button_type='primary'),
                    pn.widgets.Button(name="📊 Technical Indicators", button_type='success'),
                    pn.widgets.Button(name="🎯 Pattern Recognition", button_type='warning'),
                    pn.widgets.Button(name="💾 Export Analysis", button_type='default'),
                    pn.pane.Markdown("**Features:**"),
                    pn.pane.Markdown("- Trend line analysis"),
                    pn.pane.Markdown("- Technical indicator plots"),
                    pn.pane.Markdown("- Pattern recognition charts"),
                    pn.pane.Markdown("- Statistical trend analysis"),
                    sizing_mode='stretch_width'
                )
            }
            
            for panel_name, panel in trend_analyst_panels.items():
                try:
                    if panel and hasattr(panel, 'get_panel'):
                        panel_content = panel.get_panel()
                        tabs.append((panel_name, panel_content))
                        logger.info(f"✅ Added {panel_name} panel to Trend Analyst layout")
                    else:
                        # For Matplotlib panel, use the panel directly
                        tabs.append((panel_name, panel))
                        logger.info(f"✅ Added {panel_name} panel to Trend Analyst layout")
                except Exception as e:
                    logger.error(f"❌ Failed to create {panel_name} panel: {e}")
                    error_panel = pn.Column(
                        pn.pane.Markdown(f"### {panel_name}"),
                        pn.pane.Markdown(f"**Error loading panel:** {e}"),
                        sizing_mode='stretch_width'
                    )
                    tabs.append((panel_name, error_panel))
            
            # Create main layout with Trend Analyst specific header
            layout = pn.Column(
                pn.Row(
                    pn.pane.Markdown("# 📈 TradePulse Trend Analyst Dashboard"),
                    role_switcher,
                    sizing_mode='stretch_width'
                ),
                pn.pane.Markdown("**📈 Trend Analysis Focus:** Technical analysis, pattern recognition, and trend visualization"),
                pn.pane.Markdown("📊 **Market Status:** Bullish momentum detected | Volatility: Medium"),
                tabs,
                sizing_mode='stretch_width'
            )
            
            logger.info("✅ Trend Analyst layout created successfully")
            return layout
            
        except Exception as e:
            logger.error(f"Failed to create Trend Analyst layout: {e}")
            return pn.Column("Error: Failed to create Trend Analyst layout")
    

