#!/usr/bin/env python3
"""
TradePulse Data Metrics - Components
UI components for the data metrics
"""

import panel as pn
import logging

logger = logging.getLogger(__name__)

class DataMetricsComponents:
    """UI components for data metrics"""
    
    def __init__(self):
        self.metrics_display = None
        self.summary_display = None
        self.history_display = None
        self.export_button = None
        self.clear_button = None
    
    def create_basic_components(self):
        """Create basic UI components"""
        # Metrics display
        self.metrics_display = pn.pane.Markdown("""
        ### 📊 Data Metrics
        **Status**: Ready to calculate metrics
        """)
        
        # Summary display
        self.summary_display = pn.pane.Markdown("""
        ### 📋 Metrics Summary
        No data analyzed yet
        """)
        
        # History display
        self.history_display = pn.pane.Markdown("""
        ### 📈 Calculation History
        No calculations recorded
        """)
        
        # Action buttons
        self.export_button = pn.widgets.Button(
            name='📤 Export Metrics',
            button_type='success',
            width=120,
            disabled=True
        )
        
        self.clear_button = pn.widgets.Button(
            name='🗑️ Clear History',
            button_type='warning',
            width=120,
            disabled=True
        )
    
    def create_metrics_section(self):
        """Create metrics section"""
        return pn.Column(
            self.metrics_display,
            self.summary_display,
            sizing_mode='stretch_width'
        )
    
    def create_history_section(self):
        """Create history section"""
        return pn.Column(
            self.history_display,
            pn.Row(
                self.export_button,
                self.clear_button,
                align='center'
            ),
            sizing_mode='stretch_width'
        )
    
    def create_metrics_panel(self):
        """Create complete metrics panel"""
        return pn.Column(
            pn.pane.Markdown("### 📊 Data Metrics Analysis"),
            self.create_metrics_section(),
            pn.Spacer(height=10),
            self.create_history_section(),
            sizing_mode='stretch_width'
        )
    
    def update_metrics_display(self, metrics: dict):
        """Update metrics display"""
        if self.metrics_display:
            if not metrics or metrics.get('row_count', 0) == 0:
                self.metrics_display.object = """
                ### 📊 Data Metrics
                **Status**: No data available
                """
            else:
                self.metrics_display.object = f"""
                ### 📊 Data Metrics
                **Rows**: {metrics.get('row_count', 0):,}
                **Columns**: {metrics.get('column_count', 0):,}
                **Memory**: {metrics.get('memory_usage_mb', 0.0):.2f} MB
                **Missing Values**: {metrics.get('missing_values', {}).get('total_missing', 0):,}
                """
    
    def update_summary_display(self, summary: str):
        """Update summary display"""
        if self.summary_display:
            self.summary_display.object = f"""
            ### 📋 Metrics Summary
            {summary}
            """
    
    def update_history_display(self, history: list):
        """Update history display"""
        if self.history_display:
            if not history:
                self.history_display.object = """
                ### 📈 Calculation History
                No calculations recorded
                """
            else:
                history_text = ["### 📈 Calculation History"]
                for record in history[-5:]:  # Show last 5 records
                    timestamp = record.get('timestamp', 'Unknown')
                    rows = record.get('row_count', 0)
                    cols = record.get('column_count', 0)
                    memory = record.get('memory_mb', 0.0)
                    history_text.append(f"- **{timestamp}**: {rows:,} rows, {cols} cols, {memory:.2f} MB")
                
                self.history_display.object = "\n".join(history_text)
    
    def update_button_states(self, has_metrics: bool, has_history: bool):
        """Update button enabled/disabled states"""
        if self.export_button:
            self.export_button.disabled = not has_metrics
        
        if self.clear_button:
            self.clear_button.disabled = not has_history



