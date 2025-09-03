#!/usr/bin/env python3
"""
TradePulse Modular Panel UI - Refactored Main Entry Point
Launches the refactored modular panel UI with focused components
"""

import panel as pn
import logging
from pathlib import Path
import sys

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_refactored_modular_ui():
    """Create the refactored modular panel UI"""
    try:
        # Clear any existing Panel state to prevent document conflicts
        try:
            pn.state.clear()
        except AttributeError:
            # pn.state.clear() not available in this version
            pass
        
        # Import refactored panels
        from modular_panels.data_panel import DataPanel
        from modular_panels.models_panel import ModelsPanel
        from modular_panels.portfolio_panel import PortfolioPanel
        from modular_panels.ai.ai_panel import AIPanel
        from modular_panels.charts_panel import ChartsPanel
        from modular_panels.alerts_panel import AlertsPanel
        from modular_panels.system_panel import SystemPanel
        
        # Import data manager and data access
        from ui_components.data_manager import DataManager
        from ui_components.data_access import DataAccessManager
        from ui_components.dashboard_manager import DashboardManager
        
        logger.info("🔧 Initializing refactored modular UI components...")
        
        # Initialize data manager and data access
        data_manager = DataManager()
        data_access_manager = DataAccessManager(data_manager)
        
        # Initialize dashboard manager for role-based layouts
        dashboard_manager = DashboardManager()
        
        # Create refactored panels with data access
        panels = {
            '📊 Data': DataPanel(data_manager, data_access_manager),
            '🤖 Models': ModelsPanel(data_manager, data_access_manager),
            '💼 Portfolio': PortfolioPanel(data_manager, data_access_manager),
            '🧠 AI': AIPanel(data_manager, data_access_manager),
            '📈 Charts': ChartsPanel(data_manager, data_access_manager),
            '🚨 Alerts': AlertsPanel(data_manager, data_access_manager),
            '⚙️ System': SystemPanel()
        }
        
        # Create a reactive dashboard container
        dashboard_container = pn.Column(sizing_mode='stretch_width')
        
        # Create dashboard layout
        def create_dashboard():
            return dashboard_manager.create_dashboard(panels)
        
        # Create initial dashboard
        initial_dashboard = create_dashboard()
        dashboard_container.append(initial_dashboard)
        
        # Make the dashboard reactive to role changes
        def update_dashboard():
            try:
                logger.info("🔄 Updating dashboard layout...")
                # Create new dashboard with current role
                new_layout = dashboard_manager.create_dashboard(panels)
                
                # Clear and replace the dashboard container content
                dashboard_container.clear()
                dashboard_container.append(new_layout)
                    
                logger.info("✅ Dashboard layout updated successfully")
            except Exception as e:
                logger.error(f"Failed to update dashboard: {e}")
        
        # Set up the refresh callback
        dashboard_manager.set_refresh_callback(update_dashboard)
        
        # Return the container instead of the layout directly
        main_layout = dashboard_container
        
        logger.info("✅ Refactored modular UI with role-based dashboards created successfully")
        return main_layout
        
    except Exception as e:
        logger.error(f"❌ Failed to create refactored modular UI: {e}")
        # Return error layout
        error_layout = pn.Column(
            pn.pane.Markdown("# ❌ TradePulse Modular Panel UI - Error"),
            pn.pane.Markdown(f"**Failed to initialize refactored UI:** {e}"),
            pn.pane.Markdown("Please check the logs for more details"),
            sizing_mode='stretch_width'
        )
        return error_layout

def main():
    """Main function to launch the refactored modular UI"""
    try:
        logger.info("📈 Starting TradePulse Refactored Modular Panel UI...")
        
        # Clear any existing sessions to prevent conflicts
        try:
            pn.state.clear()
        except:
            pass
        
        # Create the UI
        app = create_refactored_modular_ui()
        
        # Configure Panel with better styling
        pn.config.sizing_mode = 'stretch_width'
        pn.config.theme = 'dark'
        
        # Apply CSS using Panel's CSS injection method - use a simpler approach
        pn.config.raw_css = ["""
        body, html { background-color: #1a1a1a !important; color: #ffffff !important; }
        .bk-root { background-color: #1a1a1a !important; color: #ffffff !important; }
        .bk-Tabs { background-color: #2d2d2d !important; border: 3px solid #404040 !important; border-radius: 10px !important; margin: 10px !important; }
        .bk-Tabs-header { background-color: #2d2d2d !important; border-bottom: 3px solid #404040 !important; padding: 15px !important; }
        .bk-Tabs-header .bk-Tabs-tab { background-color: #3d3d3d !important; color: #ffffff !important; border: 3px solid #404040 !important; margin-right: 8px !important; padding: 12px 20px !important; border-radius: 8px !important; font-weight: bold !important; font-size: 14px !important; }
        .bk-Tabs-header .bk-Tabs-tab.bk-active { background-color: #007acc !important; color: #ffffff !important; border-color: #007acc !important; box-shadow: 0 4px 8px rgba(0, 122, 204, 0.4) !important; }
        .bk-Tabs-header .bk-Tabs-tab:hover { background-color: #4d4d4d !important; border-color: #007acc !important; transform: translateY(-2px) !important; }
        .bk-Markdown { color: #ffffff !important; background-color: #2d2d2d !important; padding: 20px !important; border-radius: 10px !important; border: 2px solid #404040 !important; }
        .bk-Markdown h1, .bk-Markdown h2, .bk-Markdown h3 { color: #007acc !important; border-bottom: 3px solid #007acc !important; padding-bottom: 8px !important; margin-bottom: 15px !important; }
        .bk-Input { background-color: #3d3d3d !important; color: #ffffff !important; border: 3px solid #404040 !important; border-radius: 8px !important; padding: 12px 16px !important; font-size: 14px !important; }
        .bk-Input:focus { border-color: #007acc !important; box-shadow: 0 0 0 3px rgba(0, 122, 204, 0.3) !important; }
        .bk-Button { background-color: #007acc !important; color: #ffffff !important; border: 3px solid #007acc !important; border-radius: 8px !important; padding: 12px 20px !important; font-weight: bold !important; font-size: 14px !important; transition: all 0.3s ease !important; }
        .bk-Button:hover { background-color: #005a9e !important; border-color: #005a9e !important; transform: translateY(-2px) !important; box-shadow: 0 4px 8px rgba(0, 90, 158, 0.3) !important; }
        .bk-Column, .bk-Row { background-color: #1a1a1a !important; color: #ffffff !important; padding: 15px !important; margin: 5px !important; }
        .bk-DataTable { background-color: #2d2d2d !important; color: #ffffff !important; border: 3px solid #404040 !important; border-radius: 10px !important; }
        .bk-DataTable .slick-header { background-color: #3d3d3d !important; color: #ffffff !important; border-bottom: 3px solid #404040 !important; }
        .bk-DataTable .slick-row { background-color: #2d2d2d !important; color: #ffffff !important; border-bottom: 2px solid #404040 !important; }
        .bk-DataTable .slick-row:nth-child(even) { background-color: #252525 !important; }
        .bk-DataTable .slick-row:hover { background-color: #3d3d3d !important; }
        .bk-Plot { background-color: #2d2d2d !important; color: #ffffff !important; border: 3px solid #404040 !important; border-radius: 10px !important; padding: 15px !important; }
        .bk-Select { background-color: #3d3d3d !important; color: #ffffff !important; border: 3px solid #404040 !important; border-radius: 8px !important; }
        .bk-Select select { background-color: #3d3d3d !important; color: #ffffff !important; border: none !important; }
        .bk-Select option { background-color: #3d3d3d !important; color: #ffffff !important; }
        .bk-Select option:hover { background-color: #007acc !important; color: #ffffff !important; }
        .bk-Select option:checked { background-color: #007acc !important; color: #ffffff !important; }
        .bk-Select option:selected { background-color: #007acc !important; color: #ffffff !important; }
        select { background-color: #3d3d3d !important; color: #ffffff !important; border: 3px solid #404040 !important; border-radius: 8px !important; padding: 8px 12px !important; }
        select option { background-color: #3d3d3d !important; color: #ffffff !important; }
        select option:hover { background-color: #007acc !important; color: #ffffff !important; }
        select option:checked { background-color: #007acc !important; color: #ffffff !important; }
        select option:selected { background-color: #007acc !important; color: #ffffff !important; }
        .bk-MultiChoice { background-color: #3d3d3d !important; color: #ffffff !important; border: 3px solid #404040 !important; border-radius: 8px !important; }
        .bk-MultiChoice select { background-color: #3d3d3d !important; color: #ffffff !important; border: none !important; }
        .bk-MultiChoice option { background-color: #3d3d3d !important; color: #ffffff !important; }
        .bk-MultiChoice option:hover { background-color: #007acc !important; color: #ffffff !important; }
        .bk-MultiChoice option:checked { background-color: #007acc !important; color: #ffffff !important; }
        .bk-MultiChoice option:selected { background-color: #007acc !important; color: #ffffff !important; }
        .bk-TextArea { background-color: #3d3d3d !important; color: #ffffff !important; border: 3px solid #404040 !important; border-radius: 8px !important; }
        .bk-Progress { background-color: #2d2d2d !important; border: 3px solid #404040 !important; border-radius: 8px !important; }
        .bk-Progress .bk-bar { background-color: #007acc !important; }
        .bk-panel { background-color: #2d2d2d !important; color: #ffffff !important; border: 2px solid #404040 !important; border-radius: 8px !important; padding: 15px !important; margin: 10px 0 !important; }
        .bk-pane { background-color: #2d2d2d !important; color: #ffffff !important; border: 2px solid #404040 !important; border-radius: 8px !important; padding: 15px !important; }
        * { color: #ffffff !important; }
        div, section, article { background-color: #1a1a1a !important; }
        """]
        
        # Create a wrapper with the custom CSS
        styled_app = pn.Column(
            app,
            sizing_mode='stretch_width',
            styles={'background': '#1a1a1a', 'color': '#ffffff'}
        )
        
        # Make the styled app servable
        styled_app.servable()
        
        logger.info("✅ Refactored modular UI ready to serve")
        return styled_app, 5006, 'localhost'
        
    except Exception as e:
        logger.error(f"❌ Failed to start refactored modular UI: {e}")
        raise

if __name__ == "__main__":
    app, port, host = main()
    app.show(port=port, host=host)
