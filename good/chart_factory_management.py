#!/usr/bin/env python3
"""
TradePulse Demo Chart Factory - Management
UI management for the chart factory
"""

import panel as pn
import logging

logger = logging.getLogger(__name__)

class ChartFactoryManagement:
    """UI management for chart factory"""
    
    @staticmethod
    def create_chart_display(chart_figure):
        """Create chart display"""
        try:
            if not chart_figure:
                return pn.pane.Markdown("""
                ### 📊 Chart Display
                No chart available
                """)
            
            return pn.pane.Markdown(f"""
            ### 📊 Chart Display
            Chart created successfully!
            """)
            
        except Exception as e:
            logger.error(f"Failed to create chart display: {e}")
            return pn.pane.Markdown("Error: Failed to create chart display")
    
    @staticmethod
    def create_config_display(chart_type: str, config: dict):
        """Create configuration display"""
        try:
            if not config:
                return pn.pane.Markdown("""
                ### ⚙️ Chart Configuration
                No configuration available
                """)
            
            config_text = f"""
            ### ⚙️ Chart Configuration
            
            **Chart Type**: {chart_type}
            **Height**: {config.get('height', 'N/A')}
            **Template**: {config.get('template', 'N/A')}
            """
            
            return pn.pane.Markdown(config_text)
            
        except Exception as e:
            logger.error(f"Failed to create config display: {e}")
            return pn.pane.Markdown("Error: Failed to create config display")
    
    @staticmethod
    def create_error_display(error_message: str):
        """Create error display"""
        return pn.pane.Markdown(f"""
        ### ❌ Error
        **Message**: {error_message}
        """)
    
    @staticmethod
    def create_success_display(success_message: str):
        """Create success display"""
        return pn.pane.Markdown(f"""
        ### ✅ Success
        **Message**: {success_message}
        """)
    
    @staticmethod
    def create_loading_display():
        """Create loading display"""
        return pn.pane.Markdown("""
        ### ⏳ Creating Chart...
        Please wait while we generate your chart.
        """)
    
    @staticmethod
    def create_chart_type_display(chart_types: list):
        """Create chart type display"""
        try:
            if not chart_types:
                return pn.pane.Markdown("""
                ### 📊 Available Chart Types
                No chart types available
                """)
            
            types_text = "### 📊 Available Chart Types\n\n"
            for chart_type in chart_types:
                types_text += f"- **{chart_type}**\n"
            
            return pn.pane.Markdown(types_text)
            
        except Exception as e:
            logger.error(f"Failed to create chart type display: {e}")
            return pn.pane.Markdown("Error: Failed to create chart type display")
    
    @staticmethod
    def create_chart_preview(chart_type: str, config: dict):
        """Create chart preview"""
        try:
            preview_text = f"""
            ### 📊 Chart Preview
            
            **Type**: {chart_type}
            **Height**: {config.get('height', 'N/A')}px
            **Template**: {config.get('template', 'N/A')}
            **Status**: Ready to create
            """
            
            return pn.pane.Markdown(preview_text)
            
        except Exception as e:
            logger.error(f"Failed to create chart preview: {e}")
            return pn.pane.Markdown("Error: Failed to create chart preview")

