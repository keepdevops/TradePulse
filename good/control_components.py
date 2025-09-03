#!/usr/bin/env python3
"""
TradePulse Demo Panels - Control Components
Handles demo control component creation and management
"""

import panel as pn
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

class ControlComponents:
    """Handles demo control component creation and management"""
    
    def __init__(self, data_generator):
        self.data_generator = data_generator
        self.components = {}
        
        # Initialize control components
        self.create_control_components()
    
    def create_control_components(self):
        """Create all control components"""
        try:
            logger.info("🔧 Creating control components")
            
            # Symbol selector
            self.components['symbol_selector'] = pn.widgets.Select(
                name='Symbol',
                options=self.data_generator.symbols,
                value=self.data_generator.current_symbol,
                width=150
            )
            
            # Demo control button
            self.components['demo_button'] = pn.widgets.Button(
                name='▶ Start Demo',
                button_type='success',
                width=120
            )
            
            # Status indicator
            self.components['status_indicator'] = pn.indicators.LoadingSpinner(
                value=False,
                color='success',
                size=20
            )
            
            # Reset button
            self.components['reset_button'] = pn.widgets.Button(
                name='🔄 Reset Demo',
                button_type='warning',
                width=120
            )
            
            # Export button
            self.components['export_button'] = pn.widgets.Button(
                name='📤 Export Data',
                button_type='light',
                width=120
            )
            
            logger.info("✅ Control components created")
            
        except Exception as e:
            logger.error(f"Failed to create control components: {e}")
    
    def get_components(self) -> Dict[str, Any]:
        """Get all control components"""
        return self.components.copy()
    
    def setup_callbacks(self, demo_callback, reset_callback, export_callback):
        """Setup component callbacks"""
        try:
            if 'demo_button' in self.components:
                self.components['demo_button'].on_click(demo_callback)
            
            if 'reset_button' in self.components:
                self.components['reset_button'].on_click(reset_callback)
            
            if 'export_button' in self.components:
                self.components['export_button'].on_click(export_callback)
            
            logger.info("✅ Control component callbacks setup complete")
            
        except Exception as e:
            logger.error(f"Failed to setup control component callbacks: {e}")
    
    def update_symbol_selector(self, symbols: list, current_symbol: str):
        """Update symbol selector options"""
        try:
            if 'symbol_selector' in self.components:
                self.components['symbol_selector'].options = symbols
                self.components['symbol_selector'].value = current_symbol
            
        except Exception as e:
            logger.error(f"Failed to update symbol selector: {e}")
    
    def set_demo_status(self, is_running: bool):
        """Set demo status indicator"""
        try:
            if 'status_indicator' in self.components:
                self.components['status_indicator'].value = is_running
                
                # Update button text
                if 'demo_button' in self.components:
                    if is_running:
                        self.components['demo_button'].name = '⏸ Stop Demo'
                        self.components['demo_button'].button_type = 'danger'
                    else:
                        self.components['demo_button'].name = '▶ Start Demo'
                        self.components['demo_button'].button_type = 'success'
            
        except Exception as e:
            logger.error(f"Failed to set demo status: {e}")
    
    def get_control_layout(self) -> pn.Column:
        """Get the control components layout"""
        try:
            layout = pn.Column(
                pn.pane.Markdown("### 🎮 Demo Controls"),
                pn.Row(
                    self.components.get('symbol_selector', pn.pane.Markdown("No selector")),
                    self.components.get('demo_button', pn.pane.Markdown("No button")),
                    self.components.get('status_indicator', pn.pane.Markdown("No indicator")),
                    align='center'
                ),
                pn.Row(
                    self.components.get('reset_button', pn.pane.Markdown("No button")),
                    self.components.get('export_button', pn.pane.Markdown("No button")),
                    align='center'
                ),
                sizing_mode='stretch_width',
                background='#2d2d2d',
                margin=(10, 0)
            )
            
            return layout
            
        except Exception as e:
            logger.error(f"Failed to create control layout: {e}")
            return pn.Column("Error: Failed to create control layout")
