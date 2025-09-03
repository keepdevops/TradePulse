#!/usr/bin/env python3
"""
TradePulse Integrated Panels - Section Creators
Handles creation of UI layout sections
"""

import panel as pn
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

class SectionCreators:
    """Handles creation of UI layout sections"""
    
    def __init__(self, ui_components: Dict[str, Any]):
        self.ui_components = ui_components
    
    def create_header_section(self) -> pn.Column:
        """Create header section with title and basic info"""
        try:
            header = pn.Column(
                pn.pane.Markdown("# 🚀 TradePulse Integrated Dashboard", 
                                style={'text-align': 'center', 'color': 'white'}),
                pn.pane.Markdown("**Real-time trading and portfolio management**",
                                style={'text-align': 'center', 'color': 'lightgray'}),
                sizing_mode='stretch_width',
                background='#2d2d2d',
                margin=(10, 0)
            )
            
            return header
            
        except Exception as e:
            logger.error(f"Failed to create header section: {e}")
            return pn.Column("Header Error")
    
    def create_controls_section(self) -> pn.Column:
        """Create controls section with trading controls"""
        try:
            controls = pn.Column(
                pn.pane.Markdown("### 🎮 Trading Controls"),
                pn.Row(
                    self.ui_components.get('symbol_selector', pn.pane.Markdown("No selector")),
                    self.ui_components.get('timeframe_selector', pn.pane.Markdown("No selector")),
                    align='center'
                ),
                pn.Row(
                    self.ui_components.get('start_button', pn.pane.Markdown("No button")),
                    self.ui_components.get('stop_button', pn.pane.Markdown("No button")),
                    self.ui_components.get('pause_button', pn.pane.Markdown("No button")),
                    align='center'
                ),
                sizing_mode='stretch_width',
                background='#3d3d3d',
                margin=(10, 0)
            )
            
            return controls
            
        except Exception as e:
            logger.error(f"Failed to create controls section: {e}")
            return pn.Column("Controls Error")
    
    def create_data_section(self) -> pn.Column:
        """Create data display section"""
        try:
            data_section = pn.Column(
                pn.pane.Markdown("### 📊 Market Data"),
                pn.Row(
                    self.ui_components.get('price_display', pn.pane.Markdown("No price")),
                    self.ui_components.get('change_display', pn.pane.Markdown("No change")),
                    self.ui_components.get('volume_display', pn.pane.Markdown("No volume")),
                    align='center'
                ),
                pn.Row(
                    self.ui_components.get('status_indicator', pn.pane.Markdown("No status")),
                    align='center'
                ),
                sizing_mode='stretch_width',
                background='#4d4d4d',
                margin=(10, 0)
            )
            
            return data_section
            
        except Exception as e:
            logger.error(f"Failed to create data section: {e}")
            return pn.Column("Data Error")
    
    def create_chart_section(self) -> pn.Column:
        """Create chart display section"""
        try:
            chart_section = pn.Column(
                pn.pane.Markdown("### 📈 Charts & Analysis"),
                self.ui_components.get('chart_area', pn.pane.Markdown("No charts")),
                sizing_mode='stretch_width',
                background='#5d5d5d',
                margin=(10, 0)
            )
            
            return chart_section
            
        except Exception as e:
            logger.error(f"Failed to create chart section: {e}")
            return pn.Column("Chart Error")
    
    def create_portfolio_section(self) -> pn.Column:
        """Create portfolio display section"""
        try:
            portfolio_section = pn.Column(
                pn.pane.Markdown("### 💼 Portfolio"),
                self.ui_components.get('portfolio_summary', pn.pane.Markdown("No portfolio")),
                sizing_mode='stretch_width',
                background='#6d6d6d',
                margin=(10, 0)
            )
            
            return portfolio_section
            
        except Exception as e:
            logger.error(f"Failed to create portfolio section: {e}")
            return pn.Column("Portfolio Error")
    
    def create_actions_section(self) -> pn.Column:
        """Create actions section"""
        try:
            actions_section = pn.Column(
                pn.pane.Markdown("### ⚙️ Actions"),
                pn.Row(
                    self.ui_components.get('export_button', pn.pane.Markdown("No export")),
                    self.ui_components.get('settings_button', pn.pane.Markdown("No settings")),
                    align='center'
                ),
                sizing_mode='stretch_width',
                background='#7d7d7d',
                margin=(10, 0)
            )
            
            return actions_section
            
        except Exception as e:
            logger.error(f"Failed to create actions section: {e}")
            return pn.Column("Actions Error")
