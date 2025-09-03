#!/usr/bin/env python3
"""
TradePulse Demo Chart Factory - Components
UI components for the chart factory
"""

import panel as pn
import logging

logger = logging.getLogger(__name__)

class ChartFactoryComponents:
    """UI components for chart factory"""
    
    def __init__(self):
        self.chart_type_selector = None
        self.height_input = None
        self.template_selector = None
        self.create_chart_button = None
        self.chart_display = None
        self.config_display = None
    
    def create_basic_components(self):
        """Create basic UI components"""
        # Chart type selector
        self.chart_type_selector = pn.widgets.Select(
            name='Chart Type',
            options=['candlestick', 'volume', 'line', 'bar', 'portfolio_performance', 'trading_activity'],
            value='candlestick',
            width=200
        )
        
        # Height input
        self.height_input = pn.widgets.IntInput(
            name='Chart Height',
            start=200,
            value=400,
            width=150
        )
        
        # Template selector
        self.template_selector = pn.widgets.Select(
            name='Template',
            options=['plotly_dark', 'plotly_white', 'plotly_light'],
            value='plotly_dark',
            width=150
        )
        
        # Create chart button
        self.create_chart_button = pn.widgets.Button(
            name='📊 Create Chart',
            button_type='primary',
            width=150
        )
        
        # Chart display
        self.chart_display = pn.pane.Markdown("""
        ### 📊 Chart Display
        Select a chart type and click "Create Chart" to generate a chart
        """)
        
        # Config display
        self.config_display = pn.pane.Markdown("""
        ### ⚙️ Chart Configuration
        No configuration selected
        """)
    
    def create_chart_controls(self):
        """Create chart control section"""
        return pn.Column(
            pn.pane.Markdown("### 🎛️ Chart Controls"),
            pn.Row(
                self.chart_type_selector,
                align='center'
            ),
            pn.Row(
                self.height_input,
                self.template_selector,
                align='center'
            ),
            pn.Row(
                self.create_chart_button,
                align='center'
            ),
            sizing_mode='stretch_width'
        )
    
    def create_chart_display_section(self):
        """Create chart display section"""
        return pn.Column(
            self.chart_display,
            self.config_display,
            sizing_mode='stretch_width'
        )
    
    def create_chart_factory_panel(self):
        """Create complete chart factory panel"""
        return pn.Column(
            pn.pane.Markdown("### 📊 Chart Factory"),
            self.create_chart_controls(),
            pn.Spacer(height=10),
            self.create_chart_display_section(),
            sizing_mode='stretch_width'
        )
    
    def update_chart_display(self, chart_figure):
        """Update chart display"""
        if self.chart_display and chart_figure:
            self.chart_display.object = f"""
            ### 📊 Chart Display
            Chart created successfully!
            """
    
    def update_config_display(self, chart_type: str, config: dict):
        """Update configuration display"""
        if self.config_display:
            config_text = f"""
            ### ⚙️ Chart Configuration
            
            **Chart Type**: {chart_type}
            **Height**: {config.get('height', 'N/A')}
            **Template**: {config.get('template', 'N/A')}
            """
            self.config_display.object = config_text
    
    def update_button_states(self, can_create: bool):
        """Update button enabled/disabled states"""
        if self.create_chart_button:
            self.create_chart_button.disabled = not can_create



