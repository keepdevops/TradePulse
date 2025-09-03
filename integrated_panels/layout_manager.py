#!/usr/bin/env python3
"""
TradePulse Integrated Panels - Layout Manager
Manages UI layout sections and organization
"""

import panel as pn
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

class LayoutManager:
    """Manages UI layout sections and organization"""
    
    def __init__(self, ui_components: Dict[str, Any]):
        self.ui_components = ui_components
        self.layout_sections = {}
        
        # Setup layout sections
        self.setup_layout_sections()
    
    def setup_layout_sections(self):
        """Setup all layout sections"""
        try:
            logger.info("🔧 Setting up layout sections")
            
            from .section_creators import SectionCreators
            creators = SectionCreators(self.ui_components)
            
            # Header section
            self.layout_sections['header'] = creators.create_header_section()
            
            # Controls section
            self.layout_sections['controls'] = creators.create_controls_section()
            
            # Data section
            self.layout_sections['data'] = creators.create_data_section()
            
            # Chart section
            self.layout_sections['chart'] = creators.create_chart_section()
            
            # Portfolio section
            self.layout_sections['portfolio'] = creators.create_portfolio_section()
            
            # Actions section
            self.layout_sections['actions'] = creators.create_actions_section()
            
            logger.info("✅ Layout sections setup complete")
            
        except Exception as e:
            logger.error(f"Failed to setup layout sections: {e}")
    
    def get_layout(self) -> pn.Column:
        """Get the complete UI layout"""
        try:
            layout = pn.Column(
                self.layout_sections['header'],
                pn.Spacer(height=20),
                self.layout_sections['controls'],
                pn.Spacer(height=20),
                self.layout_sections['data'],
                pn.Spacer(height=20),
                self.layout_sections['chart'],
                pn.Spacer(height=20),
                self.layout_sections['portfolio'],
                pn.Spacer(height=20),
                self.layout_sections['actions'],
                sizing_mode='stretch_width',
                background='#1e1e1e'
            )
            
            return layout
            
        except Exception as e:
            logger.error(f"Failed to get layout: {e}")
            return pn.Column("Error: Failed to create layout")
    
    def get_layout_sections(self) -> Dict[str, Any]:
        """Get all layout sections"""
        return self.layout_sections
