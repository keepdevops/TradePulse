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
        from modular_panels.ai_panel import AIPanel
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
        
        # Create dashboard layout
        def create_dashboard():
            return dashboard_manager.create_dashboard(panels)
        
        # Create initial dashboard
        main_layout = create_dashboard()
        
        # Make the dashboard reactive to role changes
        def update_dashboard():
            try:
                logger.info("🔄 Updating dashboard layout...")
                # Create new dashboard with current role
                new_layout = dashboard_manager.create_dashboard(panels)
                
                # Replace the main layout content
                main_layout.clear()
                if hasattr(new_layout, '__iter__'):
                    for child in new_layout:
                        main_layout.append(child)
                else:
                    main_layout.append(new_layout)
                    
                logger.info("✅ Dashboard layout updated successfully")
            except Exception as e:
                logger.error(f"Failed to update dashboard: {e}")
        
        # Set up the refresh callback
        dashboard_manager.set_refresh_callback(update_dashboard)
        
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
        
        # Configure Panel
        pn.config.sizing_mode = 'stretch_width'
        pn.config.theme = 'dark'
        
        # Make the app servable
        app.servable()
        
        logger.info("✅ Refactored modular UI ready to serve")
        return app, 5006, 'localhost'
        
    except Exception as e:
        logger.error(f"❌ Failed to start refactored modular UI: {e}")
        raise

if __name__ == "__main__":
    app, port, host = main()
    app.show(port=port, host=host)
