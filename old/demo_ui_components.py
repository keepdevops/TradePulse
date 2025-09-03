#!/usr/bin/env python3
"""
TradePulse Demo Panels - Demo UI Components
Handles demo UI component creation and management
"""

import panel as pn
import pandas as pd
from typing import Dict, Any
import logging

from .ui_components.control_components import ControlComponents
from .ui_components.display_components import DisplayComponents

logger = logging.getLogger(__name__)

class DemoUIComponents:
    """Handles demo UI component creation and management"""
    
    def __init__(self, data_generator):
        self.data_generator = data_generator
        self.ui_components = {}
        
        # Initialize component managers
        self.control_components = ControlComponents(data_generator)
        self.display_components = DisplayComponents(data_generator)
        
        # Initialize UI components
        self.init_ui_components()
    
    def init_ui_components(self):
        """Initialize all demo UI components"""
        try:
            logger.info("🔧 Initializing demo UI components")
            
            # Header component
            self.ui_components['header'] = pn.pane.Markdown("""
            # 🚀 TradePulse Panel UI Demo
            ### Interactive Trading Interface Showcase
            """)
            
            # Get components from managers
            control_comps = self.control_components.get_components()
            display_comps = self.display_components.get_components()
            
            # Update main components dictionary
            self.ui_components.update(control_comps)
            self.ui_components.update(display_comps)
            
            # Additional components
            self._init_additional_components()
            
            logger.info(f"✅ {len(self.ui_components)} demo UI components initialized")
            
        except Exception as e:
            logger.error(f"Failed to initialize demo UI components: {e}")
    
    def _init_additional_components(self):
        """Initialize additional UI components"""
        try:
            # Portfolio summary
            self.ui_components['portfolio_summary'] = pn.pane.Markdown("""
            ### 💼 Portfolio Summary
            **Total Value:** $0.00  
            **Daily P&L:** $0.00 (0.00%)  
            **Total P&L:** $0.00 (0.00%)
            """)
            
            # Trading activity
            self.ui_components['trading_activity'] = pn.pane.Markdown("""
            ### 📈 Trading Activity
            **Today's Trades:** 0  
            **Total Trades:** 0  
            **Win Rate:** 0.00%
            """)
            
            # Performance metrics
            self.ui_components['performance_metrics'] = pn.pane.Markdown("""
            ### 📊 Performance Metrics
            **Sharpe Ratio:** 0.00  
            **Max Drawdown:** 0.00%  
            **Volatility:** 0.00%
            """)
            
        except Exception as e:
            logger.error(f"Failed to initialize additional components: {e}")
    
    def setup_callbacks(self, demo_callback, reset_callback, export_callback):
        """Setup all component callbacks"""
        try:
            # Setup control component callbacks
            self.control_components.setup_callbacks(
                demo_callback, reset_callback, export_callback
            )
            
            logger.info("✅ Demo UI component callbacks setup complete")
            
        except Exception as e:
            logger.error(f"Failed to setup callbacks: {e}")
    
    def get_components(self) -> Dict[str, Any]:
        """Get all UI components"""
        return self.ui_components.copy()
    
    def update_displays(self, market_data: Dict[str, Any]):
        """Update all display components with market data"""
        try:
            # Update price displays
            if 'price' in market_data:
                price = market_data['price']
                change = market_data.get('change', 0.0)
                change_pct = market_data.get('change_pct', 0.0)
                self.display_components.update_price_display(price, change, change_pct)
            
            # Update volume display
            if 'volume' in market_data:
                self.display_components.update_volume_display(market_data['volume'])
            
            # Update market data displays
            if all(key in market_data for key in ['market_cap', 'pe_ratio', 'week_high', 'week_low']):
                self.display_components.update_market_data_display(
                    market_data['market_cap'],
                    market_data['pe_ratio'],
                    market_data['week_high'],
                    market_data['week_low']
                )
            
            logger.debug("✅ Display components updated")
            
        except Exception as e:
            logger.error(f"Failed to update displays: {e}")
    
    def update_portfolio_display(self, portfolio_data: Dict[str, Any]):
        """Update portfolio-related displays"""
        try:
            if 'portfolio_summary' in self.ui_components:
                summary_text = f"""
                ### 💼 Portfolio Summary
                **Total Value:** ${portfolio_data.get('total_value', 0):,.2f}  
                **Daily P&L:** ${portfolio_data.get('daily_pnl', 0):,.2f} ({portfolio_data.get('daily_pnl_pct', 0):.2f}%)  
                **Total P&L:** ${portfolio_data.get('total_pnl', 0):,.2f} ({portfolio_data.get('total_pnl_pct', 0):.2f}%)
                """
                self.ui_components['portfolio_summary'].object = summary_text
            
            if 'trading_activity' in self.ui_components:
                activity_text = f"""
                ### 📈 Trading Activity
                **Today's Trades:** {portfolio_data.get('today_trades', 0)}  
                **Total Trades:** {portfolio_data.get('total_trades', 0)}  
                **Win Rate:** {portfolio_data.get('win_rate', 0):.2f}%
                """
                self.ui_components['trading_activity'].object = activity_text
            
            if 'performance_metrics' in self.ui_components:
                metrics_text = f"""
                ### 📊 Performance Metrics
                **Sharpe Ratio:** {portfolio_data.get('sharpe_ratio', 0):.2f}  
                **Max Drawdown:** {portfolio_data.get('max_drawdown', 0):.2f}%  
                **Volatility:** {portfolio_data.get('volatility', 0):.2f}%
                """
                self.ui_components['performance_metrics'].object = metrics_text
            
        except Exception as e:
            logger.error(f"Failed to update portfolio display: {e}")
    
    def set_demo_status(self, is_running: bool):
        """Set demo status"""
        try:
            self.control_components.set_demo_status(is_running)
            
        except Exception as e:
            logger.error(f"Failed to set demo status: {e}")
    
    def reset_all_displays(self):
        """Reset all displays to default values"""
        try:
            # Reset display components
            self.display_components.reset_displays()
            
            # Reset additional components
            self._init_additional_components()
            
            logger.info("✅ All displays reset")
            
        except Exception as e:
            logger.error(f"Failed to reset displays: {e}")
    
    def get_complete_layout(self) -> pn.Column:
        """Get the complete demo UI layout"""
        try:
            # Get layouts from component managers
            control_layout = self.control_components.get_control_layout()
            display_layout = self.display_components.get_display_layout()
            
            # Create additional components layout
            additional_layout = pn.Column(
                self.ui_components.get('portfolio_summary', pn.pane.Markdown("No summary")),
                pn.Spacer(height=20),
                self.ui_components.get('trading_activity', pn.pane.Markdown("No activity")),
                pn.Spacer(height=20),
                self.ui_components.get('performance_metrics', pn.pane.Markdown("No metrics")),
                sizing_mode='stretch_width',
                background='#4d4d4d',
                margin=(10, 0)
            )
            
            # Create complete layout
            layout = pn.Column(
                self.ui_components.get('header', pn.pane.Markdown("No header")),
                pn.Spacer(height=20),
                control_layout,
                pn.Spacer(height=20),
                display_layout,
                pn.Spacer(height=20),
                additional_layout,
                sizing_mode='stretch_width',
                background='#1e1e1e'
            )
            
            return layout
            
        except Exception as e:
            logger.error(f"Failed to create complete layout: {e}")
            return pn.Column("Error: Failed to create complete layout")
    
    def get_component_status(self) -> Dict[str, Any]:
        """Get component status information"""
        try:
            return {
                'total_components': len(self.ui_components),
                'control_components_count': len(self.control_components.get_components()),
                'display_components_count': len(self.display_components.get_components()),
                'component_type': 'Demo UI Components'
            }
            
        except Exception as e:
            logger.error(f"Failed to get component status: {e}")
            return {}
