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
        """Create Day Traders dashboard layout (tabbed interface without Models and AI)"""
        try:
            logger.info("🎯 Creating Day Trader dashboard layout")
            
            # Create tabbed interface (same as default but without Models and AI)
            tabs = pn.Tabs()
            
            # Day Trader specific panels (exclude Models and AI)
            day_trader_panels = {
                '📊 Data': panels.get('📊 Data'),
                '💼 Portfolio': panels.get('💼 Portfolio'),
                '📈 Charts': panels.get('📈 Charts'),
                '🚨 Alerts': panels.get('🚨 Alerts'),
                '⚙️ System': panels.get('⚙️ System')
            }
            
            for panel_name, panel in day_trader_panels.items():
                try:
                    if panel and hasattr(panel, 'get_panel'):
                        panel_content = panel.get_panel()
                        tabs.append((panel_name, panel_content))
                        logger.info(f"✅ Added {panel_name} panel to Day Trader layout")
                    else:
                        error_panel = pn.Column(
                            pn.pane.Markdown(f"### {panel_name}"),
                            pn.pane.Markdown("**Panel unavailable**"),
                            sizing_mode='stretch_width'
                        )
                        tabs.append((panel_name, error_panel))
                        logger.warning(f"⚠️ {panel_name} panel not available")
                except Exception as e:
                    logger.error(f"❌ Failed to create {panel_name} panel: {e}")
                    error_panel = pn.Column(
                        pn.pane.Markdown(f"### {panel_name}"),
                        pn.pane.Markdown(f"**Error loading panel:** {e}"),
                        sizing_mode='stretch_width'
                    )
                    tabs.append((panel_name, error_panel))
            
            # Create main layout with Day Trader specific header
            layout = pn.Column(
                pn.Row(
                    pn.pane.Markdown("# 📈 TradePulse Day Trader Dashboard"),
                    role_switcher,
                    sizing_mode='stretch_width'
                ),
                pn.pane.Markdown("**🎯 Day Trading Focus:** Real-time data, charts, alerts, and portfolio management"),
                pn.pane.Markdown("📢 **Market Status:** Live trading session active"),
                tabs,
                sizing_mode='stretch_width'
            )
            
            logger.info("✅ Day Trader layout created successfully")
            return layout
            
        except Exception as e:
            logger.error(f"Failed to create Day Trader layout: {e}")
            return pn.Column("Error: Failed to create Day Trader layout")
    
    @staticmethod
    def create_ml_analyst_layout(panels: Dict[str, Any], role_switcher) -> pn.Column:
        """Create ML AI Analyst dashboard layout (tabbed interface with Matplotlib)"""
        try:
            logger.info("🎯 Creating ML AI Analyst dashboard layout")
            
            # Create tabbed interface (same as default but with Matplotlib)
            tabs = pn.Tabs()
            
            # ML AI Analyst specific panels (all modules plus Matplotlib)
            ml_analyst_panels = {
                '📊 Data': panels.get('📊 Data'),
                '🤖 Models': panels.get('🤖 Models'),
                '💼 Portfolio': panels.get('💼 Portfolio'),
                '🧠 AI': panels.get('🧠 AI'),
                '📈 Charts': panels.get('📈 Charts'),
                '🚨 Alerts': panels.get('🚨 Alerts'),
                '⚙️ System': panels.get('⚙️ System'),
                '📊 Matplotlib': pn.Column(
                    pn.pane.Markdown("### 📊 Matplotlib Visualization"),
                    pn.pane.Markdown("**Advanced plotting and visualization tools**"),
                    pn.widgets.Button(name="📈 Create Plot", button_type='primary'),
                    pn.widgets.Button(name="🎨 Customize Style", button_type='success'),
                    pn.widgets.Button(name="💾 Export Figure", button_type='warning'),
                    pn.pane.Markdown("**Features:**"),
                    pn.pane.Markdown("- Interactive plotting"),
                    pn.pane.Markdown("- Custom styling and themes"),
                    pn.pane.Markdown("- Figure export capabilities"),
                    pn.pane.Markdown("- Statistical visualizations"),
                    sizing_mode='stretch_width'
                )
            }
            
            for panel_name, panel in ml_analyst_panels.items():
                try:
                    if panel and hasattr(panel, 'get_panel'):
                        panel_content = panel.get_panel()
                        tabs.append((panel_name, panel_content))
                        logger.info(f"✅ Added {panel_name} panel to ML AI Analyst layout")
                    else:
                        # For Matplotlib panel, use the panel directly
                        tabs.append((panel_name, panel))
                        logger.info(f"✅ Added {panel_name} panel to ML AI Analyst layout")
                except Exception as e:
                    logger.error(f"❌ Failed to create {panel_name} panel: {e}")
                    error_panel = pn.Column(
                        pn.pane.Markdown(f"### {panel_name}"),
                        pn.pane.Markdown(f"**Error loading panel:** {e}"),
                        sizing_mode='stretch_width'
                    )
                    tabs.append((panel_name, error_panel))
            
            # Create main layout with ML AI Analyst specific header
            layout = pn.Column(
                pn.Row(
                    pn.pane.Markdown("# 🤖 TradePulse ML AI Analyst Dashboard"),
                    role_switcher,
                    sizing_mode='stretch_width'
                ),
                pn.pane.Markdown("**🧠 AI/ML Focus:** Advanced analytics, model training, and data visualization"),
                pn.pane.Markdown("📊 **Model Performance:** Recent accuracy: 87.2% | Training: Active"),
                tabs,
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
    

