#!/usr/bin/env python3
"""
TradePulse UI Panels - Control UI Components
Handles control panel UI component creation
"""

import panel as pn
import logging

logger = logging.getLogger(__name__)

class ControlUIComponents:
    """Handles control panel UI component creation"""
    
    def create_symbol_selector(self, symbols: list, current_symbol: str):
        """Create symbol selection component"""
        try:
            symbol_selector = pn.widgets.Select(
                name='Symbol',
                options=symbols,
                value=current_symbol,
                width=150
            )
            
            return symbol_selector
            
        except Exception as e:
            logger.error(f"Failed to create symbol selector: {e}")
            return pn.pane.Markdown("**Symbol Selector Error**")
    
    def create_timeframe_selector(self, timeframes: list, current_timeframe: str):
        """Create timeframe selection component"""
        try:
            timeframe_selector = pn.widgets.Select(
                name='Timeframe',
                options=timeframes,
                value=current_timeframe,
                width=100
            )
            
            return timeframe_selector
            
        except Exception as e:
            logger.error(f"Failed to create timeframe selector: {e}")
            return pn.pane.Markdown("**Timeframe Selector Error**")
    
    def create_trading_controls(self, operations):
        """Create trading control buttons"""
        try:
            start_button = pn.widgets.Button(
                name='▶ Start Trading',
                button_type='success',
                width=120
            )
            start_button.on_click(operations.start_trading)
            
            stop_button = pn.widgets.Button(
                name='⏹ Stop Trading',
                button_type='danger',
                width=120
            )
            stop_button.on_click(operations.stop_trading)
            
            pause_button = pn.widgets.Button(
                name='⏸ Pause',
                button_type='warning',
                width=120
            )
            pause_button.on_click(operations.pause_trading)
            
            controls_row = pn.Row(
                start_button,
                stop_button,
                pause_button,
                align='center'
            )
            
            return controls_row
            
        except Exception as e:
            logger.error(f"Failed to create trading controls: {e}")
            return pn.pane.Markdown("**Trading Controls Error**")
    
    def create_status_indicator(self):
        """Create status indicator component"""
        try:
            status_indicator = pn.indicators.LoadingSpinner(
                value=False,
                color='success',
                size=20
            )
            
            return status_indicator
            
        except Exception as e:
            logger.error(f"Failed to create status indicator: {e}")
            return pn.pane.Markdown("**Status Indicator Error**")
    
    def create_control_layout(self, symbol_selector, timeframe_selector, trading_controls, status_indicator):
        """Create the complete control panel layout"""
        try:
            # Main control row
            control_row = pn.Row(
                pn.pane.Markdown("**🎛️ Trading Controls**"),
                pn.Spacer(width=20),
                symbol_selector,
                timeframe_selector,
                pn.Spacer(width=20),
                trading_controls,
                pn.Spacer(width=20),
                status_indicator,
                align='center',
                sizing_mode='stretch_width'
            )
            
            return control_row
            
        except Exception as e:
            logger.error(f"Failed to create control layout: {e}")
            return pn.pane.Markdown("**Control Layout Error**")
