#!/usr/bin/env python3
"""
Dark Mode Configuration for TradePulse
Apply this to fix UI visibility issues in dark mode
"""

import panel as pn
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class DarkModeConfig:
    """Dark mode configuration for TradePulse"""
    
    def __init__(self):
        self.dark_colors = {
            'background': '#1e1e1e',
            'panel_bg': '#2d2d2d',
            'text': '#ffffff',
            'accent': '#00ff88',
            'border': '#404040',
            'success': '#00ff88',
            'warning': '#ffaa00',
            'error': '#ff4444',
            'info': '#4488ff'
        }
    
    def get_dark_css(self):
        """Get CSS for dark mode"""
        return f"""
        <style>
        /* Dark Mode CSS for TradePulse */
        
        /* Global dark theme */
        body {{
            background-color: {self.dark_colors['background']} !important;
            color: {self.dark_colors['text']} !important;
        }}
        
        /* Panel root elements */
        .bk-root {{
            background-color: {self.dark_colors['background']} !important;
        }}
        
        /* Layout components */
        .bk-panel-models-layout-Column {{
            background-color: {self.dark_colors['background']} !important;
        }}
        
        .bk-panel-models-layout-Row {{
            background-color: {self.dark_colors['background']} !important;
        }}
        
        /* Tabs styling */
        .bk-panel-models-widgets-Tabs {{
            background-color: {self.dark_colors['background']} !important;
        }}
        
        .bk-panel-models-widgets-Tabs .bk-tabs-header {{
            background-color: {self.dark_colors['panel_bg']} !important;
            border-color: {self.dark_colors['border']} !important;
        }}
        
        .bk-panel-models-widgets-Tabs .bk-tab {{
            background-color: {self.dark_colors['panel_bg']} !important;
            color: {self.dark_colors['text']} !important;
            border-color: {self.dark_colors['border']} !important;
        }}
        
        .bk-panel-models-widgets-Tabs .bk-tab.bk-active {{
            background-color: {self.dark_colors['border']} !important;
            color: {self.dark_colors['accent']} !important;
        }}
        
        /* DataFrame styling */
        .bk-panel-models-widgets-DataFrame {{
            background-color: {self.dark_colors['panel_bg']} !important;
            color: {self.dark_colors['text']} !important;
        }}
        
        .bk-panel-models-widgets-DataFrame table {{
            background-color: {self.dark_colors['panel_bg']} !important;
            color: {self.dark_colors['text']} !important;
        }}
        
        .bk-panel-models-widgets-DataFrame th {{
            background-color: {self.dark_colors['border']} !important;
            color: {self.dark_colors['text']} !important;
        }}
        
        .bk-panel-models-widgets-DataFrame td {{
            background-color: {self.dark_colors['panel_bg']} !important;
            color: {self.dark_colors['text']} !important;
            border-color: {self.dark_colors['border']} !important;
        }}
        
        /* Button styling */
        .bk-panel-models-widgets-Button {{
            background-color: {self.dark_colors['border']} !important;
            color: {self.dark_colors['text']} !important;
            border-color: {self.dark_colors['border']} !important;
        }}
        
        .bk-panel-models-widgets-Button:hover {{
            background-color: #505050 !important;
        }}
        
        .bk-panel-models-widgets-Button.bk-btn-primary {{
            background-color: {self.dark_colors['accent']} !important;
            color: {self.dark_colors['background']} !important;
        }}
        
        .bk-panel-models-widgets-Button.bk-btn-primary:hover {{
            background-color: #00cc6a !important;
        }}
        
        /* Input styling */
        .bk-panel-models-widgets-TextInput {{
            background-color: {self.dark_colors['panel_bg']} !important;
            color: {self.dark_colors['text']} !important;
            border-color: {self.dark_colors['border']} !important;
        }}
        
        .bk-panel-models-widgets-Select {{
            background-color: {self.dark_colors['panel_bg']} !important;
            color: {self.dark_colors['text']} !important;
            border-color: {self.dark_colors['border']} !important;
        }}
        
        .bk-panel-models-widgets-IntSlider {{
            background-color: {self.dark_colors['panel_bg']} !important;
            color: {self.dark_colors['text']} !important;
        }}
        
        .bk-panel-models-widgets-FloatSlider {{
            background-color: {self.dark_colors['panel_bg']} !important;
            color: {self.dark_colors['text']} !important;
        }}
        
        .bk-panel-models-widgets-FloatInput {{
            background-color: {self.dark_colors['panel_bg']} !important;
            color: {self.dark_colors['text']} !important;
            border-color: {self.dark_colors['border']} !important;
        }}
        
        /* Markdown styling */
        .bk-panel-models-markup-Markdown {{
            background-color: {self.dark_colors['panel_bg']} !important;
            color: {self.dark_colors['text']} !important;
        }}
        
        /* Chart styling */
        .bk-panel-models-plot-Plot {{
            background-color: {self.dark_colors['background']} !important;
        }}
        
        /* Override any light theme elements */
        * {{
            background-color: {self.dark_colors['background']} !important;
            color: {self.dark_colors['text']} !important;
        }}
        
        /* Specific overrides for common elements */
        .panel-widget-box {{
            background-color: {self.dark_colors['panel_bg']} !important;
            border-color: {self.dark_colors['border']} !important;
        }}
        
        .panel-content {{
            background-color: {self.dark_colors['background']} !important;
        }}
        
        /* Success, warning, error colors */
        .success-text {{
            color: {self.dark_colors['success']} !important;
        }}
        
        .warning-text {{
            color: {self.dark_colors['warning']} !important;
        }}
        
        .error-text {{
            color: {self.dark_colors['error']} !important;
        }}
        
        .info-text {{
            color: {self.dark_colors['info']} !important;
        }}
        
        </style>
        """
    
    def apply_dark_theme(self, app):
        """Apply dark theme to existing app"""
        logger.info("🌙 Applying dark theme to TradePulse app...")
        
        # Get dark CSS
        dark_css = self.get_dark_css()
        
        # Create CSS pane
        css_pane = pn.pane.HTML(dark_css)
        
        # Apply dark theme to Panel
        pn.config.theme = 'dark'
        
        # Return app with dark theme
        return pn.Column(css_pane, app)
    
    def create_dark_panel(self, title, content, panel_type='data'):
        """Create a dark mode panel"""
        panel_colors = {
            'data': self.dark_colors['info'],
            'portfolio': self.dark_colors['success'],
            'ai': self.dark_colors['accent'],
            'alerts': self.dark_colors['warning'],
            'system': self.dark_colors['text']
        }
        
        color = panel_colors.get(panel_type, self.dark_colors['text'])
        
        return pn.Column(
            pn.pane.Markdown(f"# {title}", styles={'color': color, 'font-size': '24px'}),
            content,
            background=self.dark_colors['panel_bg'],
            styles={'border': f'1px solid {self.dark_colors["border"]}', 'padding': '10px'}
        )

def apply_dark_mode_to_existing():
    """Apply dark mode to existing TradePulse application"""
    logger.info("🔧 Applying dark mode to existing TradePulse app...")
    
    # Create dark mode config
    dark_config = DarkModeConfig()
    
    # Set Panel theme
    pn.config.theme = 'dark'
    
    # Return the CSS that can be applied
    return dark_config.get_dark_css()

def create_dark_mode_wrapper():
    """Create a wrapper to apply dark mode to any Panel app"""
    def wrapper(app_func):
        def dark_app(*args, **kwargs):
            # Set dark theme
            pn.config.theme = 'dark'
            
            # Create dark config
            dark_config = DarkModeConfig()
            
            # Get the original app
            original_app = app_func(*args, **kwargs)
            
            # Apply dark theme
            dark_css = pn.pane.HTML(dark_config.get_dark_css())
            
            # Return wrapped app
            return pn.Column(dark_css, original_app)
        
        return dark_app
    return wrapper

# Example usage
if __name__ == "__main__":
    logger.info("🌙 Dark mode configuration ready")
    logger.info("Use apply_dark_mode_to_existing() to get CSS")
    logger.info("Use create_dark_mode_wrapper() to wrap existing apps")
