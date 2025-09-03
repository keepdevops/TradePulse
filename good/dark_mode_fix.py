#!/usr/bin/env python3
"""
TradePulse Dark Mode Fix
Fixes UI panel visibility issues in dark mode
"""

import panel as pn
import hvplot.pandas
import plotly.graph_objects as go
import plotly.express as px
from pathlib import Path
import pandas as pd
import numpy as np
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class DarkModeFix:
    """Fix dark mode visibility issues for TradePulse UI"""
    
    def __init__(self):
        self.dark_theme = {
            'background': '#1e1e1e',
            'text': '#ffffff',
            'accent': '#00ff88',
            'panel_bg': '#2d2d2d',
            'border': '#404040',
            'success': '#00ff88',
            'warning': '#ffaa00',
            'error': '#ff4444',
            'info': '#4488ff'
        }
        
    def create_dark_mode_ui(self):
        """Create a dark mode optimized UI"""
        logger.info("🌙 Creating dark mode optimized UI...")
        
        # Set Panel theme to dark
        pn.config.theme = 'dark'
        
        # Create sample data for demonstration
        dates = pd.date_range(start='2024-01-01', end='2024-12-31', freq='D')
        stock_data = pd.DataFrame({
            'Date': dates,
            'AAPL': np.random.randn(len(dates)).cumsum() + 150,
            'GOOGL': np.random.randn(len(dates)).cumsum() + 2800,
            'MSFT': np.random.randn(len(dates)).cumsum() + 300,
            'TSLA': np.random.randn(len(dates)).cumsum() + 200,
            'AMZN': np.random.randn(len(dates)).cumsum() + 3300
        })
        
        # Create dark mode optimized components
        components = self.create_dark_components(stock_data)
        
        # Create main layout with dark theme
        main_layout = self.create_dark_layout(components)
        
        logger.info("✅ Dark mode UI created successfully")
        return main_layout
    
    def create_dark_components(self, data):
        """Create dark mode optimized components"""
        components = {}
        
        # Data Panel with dark theme
        data_panel = pn.Column(
            pn.pane.Markdown("# 📊 Data Panel", styles={'color': self.dark_theme['text']}),
            pn.widgets.DataFrame(data.head(10), width=800, height=300),
            pn.pane.Markdown("### Data Statistics", styles={'color': self.dark_theme['text']}),
            pn.widgets.DataFrame(data.describe(), width=800, height=200),
            background=self.dark_theme['panel_bg'],
            styles={'border': f'1px solid {self.dark_theme["border"]}'}
        )
        components['data'] = data_panel
        
        # Charts Panel with dark theme
        chart = data.hvplot.line(
            x='Date', 
            y=['AAPL', 'GOOGL', 'MSFT'], 
            title='Stock Prices (Dark Mode)',
            height=400,
            width=800,
            color=['#00ff88', '#4488ff', '#ffaa00']
        ).opts(
            bgcolor=self.dark_theme['background'],
            title_color=self.dark_theme['text'],
            axis_line_color=self.dark_theme['border'],
            grid_color=self.dark_theme['border'],
            text_color=self.dark_theme['text']
        )
        
        charts_panel = pn.Column(
            pn.pane.Markdown("# 📈 Charts Panel", styles={'color': self.dark_theme['text']}),
            chart,
            background=self.dark_theme['panel_bg'],
            styles={'border': f'1px solid {self.dark_theme["border"]}'}
        )
        components['charts'] = charts_panel
        
        # Portfolio Panel with dark theme
        portfolio_data = pd.DataFrame({
            'Symbol': ['AAPL', 'GOOGL', 'MSFT', 'TSLA', 'AMZN'],
            'Shares': [100, 50, 75, 200, 30],
            'Current_Price': [160, 2900, 320, 220, 3400],
            'Total_Value': [16000, 145000, 24000, 44000, 102000]
        })
        
        portfolio_panel = pn.Column(
            pn.pane.Markdown("# 💼 Portfolio Panel", styles={'color': self.dark_theme['text']}),
            pn.widgets.DataFrame(portfolio_data, width=800, height=200),
            pn.pane.Markdown(f"**Total Portfolio Value: ${portfolio_data['Total_Value'].sum():,}**", 
                           styles={'color': self.dark_theme['success']}),
            background=self.dark_theme['panel_bg'],
            styles={'border': f'1px solid {self.dark_theme["border"]}'}
        )
        components['portfolio'] = portfolio_panel
        
        # AI Panel with dark theme
        ai_panel = pn.Column(
            pn.pane.Markdown("# 🤖 AI Panel", styles={'color': self.dark_theme['text']}),
            pn.widgets.Select(name='Model Type', options=['ADM', 'CIPO', 'BICIPO', 'Ensemble']),
            pn.widgets.IntSlider(name='Training Epochs', start=10, end=100, value=50),
            pn.widgets.FloatSlider(name='Learning Rate', start=0.001, end=0.1, value=0.01),
            pn.widgets.Button(name='🚀 Train Model', button_type='primary'),
            pn.pane.Markdown("**Model Status: Ready**", styles={'color': self.dark_theme['success']}),
            background=self.dark_theme['panel_bg'],
            styles={'border': f'1px solid {self.dark_theme["border"]}'}
        )
        components['ai'] = ai_panel
        
        # Alerts Panel with dark theme
        alerts_panel = pn.Column(
            pn.pane.Markdown("# 🚨 Alerts Panel", styles={'color': self.dark_theme['text']}),
            pn.widgets.TextInput(name='Symbol', placeholder='Enter stock symbol'),
            pn.widgets.FloatInput(name='Price Threshold', value=150.0),
            pn.widgets.Select(name='Condition', options=['Above', 'Below']),
            pn.widgets.Button(name='🔔 Create Alert', button_type='primary'),
            pn.pane.Markdown("**Active Alerts: 3**", styles={'color': self.dark_theme['warning']}),
            background=self.dark_theme['panel_bg'],
            styles={'border': f'1px solid {self.dark_theme["border"]}'}
        )
        components['alerts'] = alerts_panel
        
        # System Panel with dark theme
        system_panel = pn.Column(
            pn.pane.Markdown("# ⚙️ System Panel", styles={'color': self.dark_theme['text']}),
            pn.pane.Markdown("**CPU Usage: 15%**", styles={'color': self.dark_theme['success']}),
            pn.pane.Markdown("**Memory Usage: 45%**", styles={'color': self.dark_theme['warning']}),
            pn.pane.Markdown("**System Status: Healthy**", styles={'color': self.dark_theme['success']}),
            pn.widgets.Button(name='🔄 Refresh', button_type='primary'),
            background=self.dark_theme['panel_bg'],
            styles={'border': f'1px solid {self.dark_theme["border"]}'}
        )
        components['system'] = system_panel
        
        return components
    
    def create_dark_layout(self, components):
        """Create dark mode optimized layout"""
        # Create tabs with dark theme
        tabs = pn.Tabs(
            ('📊 Data', components['data']),
            ('📈 Charts', components['charts']),
            ('💼 Portfolio', components['portfolio']),
            ('🤖 AI', components['ai']),
            ('🚨 Alerts', components['alerts']),
            ('⚙️ System', components['system']),
            styles={
                'background': self.dark_theme['background'],
                'color': self.dark_theme['text']
            }
        )
        
        # Create header with dark theme
        header = pn.Column(
            pn.pane.Markdown(
                "# 🌙 TradePulse - Dark Mode", 
                styles={
                    'color': self.dark_theme['accent'],
                    'text-align': 'center',
                    'font-size': '2em',
                    'margin': '10px'
                }
            ),
            pn.pane.Markdown(
                "**Trading Platform with Dark Mode Optimization**",
                styles={
                    'color': self.dark_theme['text'],
                    'text-align': 'center',
                    'font-size': '1.2em'
                }
            ),
            background=self.dark_theme['background'],
            styles={'border-bottom': f'2px solid {self.dark_theme["border"]}'}
        )
        
        # Create main layout
        main_layout = pn.Column(
            header,
            tabs,
            background=self.dark_theme['background'],
            styles={'min-height': '100vh'}
        )
        
        return main_layout
    
    def apply_dark_theme_to_existing(self):
        """Apply dark theme to existing TradePulse components"""
        logger.info("🌙 Applying dark theme to existing components...")
        
        # CSS for dark mode
        dark_css = """
        <style>
        .dark-theme {
            background-color: #1e1e1e !important;
            color: #ffffff !important;
        }
        
        .dark-panel {
            background-color: #2d2d2d !important;
            border: 1px solid #404040 !important;
            color: #ffffff !important;
        }
        
        .dark-text {
            color: #ffffff !important;
        }
        
        .dark-accent {
            color: #00ff88 !important;
        }
        
        .dark-success {
            color: #00ff88 !important;
        }
        
        .dark-warning {
            color: #ffaa00 !important;
        }
        
        .dark-error {
            color: #ff4444 !important;
        }
        
        .dark-info {
            color: #4488ff !important;
        }
        
        .dark-border {
            border-color: #404040 !important;
        }
        
        /* Override Panel default styles */
        .bk-root {
            background-color: #1e1e1e !important;
        }
        
        .bk-panel-models-layout-Column {
            background-color: #1e1e1e !important;
        }
        
        .bk-panel-models-layout-Row {
            background-color: #1e1e1e !important;
        }
        
        .bk-panel-models-widgets-Tabs {
            background-color: #1e1e1e !important;
        }
        
        .bk-panel-models-widgets-Tabs .bk-tabs-header {
            background-color: #2d2d2d !important;
            border-color: #404040 !important;
        }
        
        .bk-panel-models-widgets-Tabs .bk-tab {
            background-color: #2d2d2d !important;
            color: #ffffff !important;
            border-color: #404040 !important;
        }
        
        .bk-panel-models-widgets-Tabs .bk-tab.bk-active {
            background-color: #404040 !important;
            color: #00ff88 !important;
        }
        
        .bk-panel-models-widgets-DataFrame {
            background-color: #2d2d2d !important;
            color: #ffffff !important;
        }
        
        .bk-panel-models-widgets-DataFrame table {
            background-color: #2d2d2d !important;
            color: #ffffff !important;
        }
        
        .bk-panel-models-widgets-DataFrame th {
            background-color: #404040 !important;
            color: #ffffff !important;
        }
        
        .bk-panel-models-widgets-DataFrame td {
            background-color: #2d2d2d !important;
            color: #ffffff !important;
            border-color: #404040 !important;
        }
        
        .bk-panel-models-widgets-Button {
            background-color: #404040 !important;
            color: #ffffff !important;
            border-color: #404040 !important;
        }
        
        .bk-panel-models-widgets-Button:hover {
            background-color: #505050 !important;
        }
        
        .bk-panel-models-widgets-Button.bk-btn-primary {
            background-color: #00ff88 !important;
            color: #1e1e1e !important;
        }
        
        .bk-panel-models-widgets-Button.bk-btn-primary:hover {
            background-color: #00cc6a !important;
        }
        
        .bk-panel-models-widgets-TextInput {
            background-color: #2d2d2d !important;
            color: #ffffff !important;
            border-color: #404040 !important;
        }
        
        .bk-panel-models-widgets-Select {
            background-color: #2d2d2d !important;
            color: #ffffff !important;
            border-color: #404040 !important;
        }
        
        .bk-panel-models-widgets-IntSlider {
            background-color: #2d2d2d !important;
            color: #ffffff !important;
        }
        
        .bk-panel-models-widgets-FloatSlider {
            background-color: #2d2d2d !important;
            color: #ffffff !important;
        }
        
        .bk-panel-models-widgets-FloatInput {
            background-color: #2d2d2d !important;
            color: #ffffff !important;
            border-color: #404040 !important;
        }
        </style>
        """
        
        return dark_css

def create_dark_mode_app():
    """Create and serve dark mode optimized TradePulse app"""
    logger.info("🚀 Creating TradePulse Dark Mode App...")
    
    # Initialize dark mode fix
    dark_fix = DarkModeFix()
    
    # Create dark mode UI
    dark_ui = dark_fix.create_dark_mode_ui()
    
    # Apply dark theme CSS
    dark_css = dark_fix.apply_dark_theme_to_existing()
    
    # Create the app with dark theme
    app = pn.Column(
        pn.pane.HTML(dark_css),
        dark_ui
    )
    
    logger.info("✅ Dark mode app created successfully")
    return app

def main():
    """Main function to run dark mode app"""
    logger.info("🌙 Starting TradePulse Dark Mode...")
    
    # Create dark mode app
    app = create_dark_mode_app()
    
    # Show the app
    app.show(
        port=5008,
        host='localhost',
        title='TradePulse - Dark Mode',
        show=False
    )
    
    logger.info("🌐 Dark mode app available at: http://localhost:5008")

if __name__ == "__main__":
    main()
