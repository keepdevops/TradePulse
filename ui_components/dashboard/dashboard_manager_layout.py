#!/usr/bin/env python3
"""
TradePulse Dashboard Manager - Layout
Additional layout methods for the dashboard manager
"""

import panel as pn
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class DashboardManagerLayout:
    """Additional layout methods for dashboard manager"""
    
    @staticmethod
    def create_default_layout(panels: Dict[str, Any], role_switcher) -> pn.Column:
        """Create default dashboard layout (original tabbed interface)"""
        try:
            logger.info("🎯 Creating default dashboard layout")
            
            # Create tabbed interface
            tabs = pn.Tabs()
            
            for panel_name, panel in panels.items():
                try:
                    panel_content = panel.get_panel()
                    tabs.append((panel_name, panel_content))
                    logger.info(f"✅ Added {panel_name} panel")
                except Exception as e:
                    logger.error(f"❌ Failed to create {panel_name} panel: {e}")
                    error_panel = pn.Column(
                        pn.pane.Markdown(f"### {panel_name}"),
                        pn.pane.Markdown(f"**Error loading panel:** {e}"),
                        sizing_mode='stretch_width'
                    )
                    tabs.append((panel_name, error_panel))
            
            # Create main layout
            layout = pn.Column(
                pn.Row(
                    pn.pane.Markdown("# 📈 TradePulse Modular Panel UI"),
                    role_switcher,
                    sizing_mode='stretch_width'
                ),
                pn.pane.Markdown("**Select your role above to customize the dashboard**"),
                tabs,
                sizing_mode='stretch_width'
            )
            
            logger.info("✅ Default layout created successfully")
            return layout
            
        except Exception as e:
            logger.error(f"Failed to create default layout: {e}")
            return pn.Column("Error: Failed to create default layout")
    
    @staticmethod
    def create_error_panel(panel_name: str, error: str) -> pn.Column:
        """Create error panel for failed panel loading"""
        return pn.Column(
            pn.pane.Markdown(f"### {panel_name}"),
            pn.pane.Markdown(f"**Error loading panel:** {error}"),
            sizing_mode='stretch_width'
        )
    
    @staticmethod
    def create_navigation_bar(role_switcher, search_input=None, status_display=None):
        """Create navigation bar component"""
        components = [role_switcher]
        
        if search_input:
            components.append(search_input)
        
        if status_display:
            components.append(status_display)
        
        return pn.Row(
            *components,
            sizing_mode='stretch_width'
        )
    
    @staticmethod
    def create_section_header(title: str, level: int = 2) -> pn.pane.Markdown:
        """Create section header"""
        header_markers = "#" * level
        return pn.pane.Markdown(f"{header_markers} {title}")
    
    @staticmethod
    def create_panel_section(title: str, panel_content, width: int = None):
        """Create panel section with title and content"""
        section = pn.Column(
            DashboardManagerLayout.create_section_header(title),
            panel_content,
            sizing_mode='stretch_width'
        )
        
        if width:
            section.width = width
        
        return section



