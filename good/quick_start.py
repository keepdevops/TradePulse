#!/usr/bin/env python3
"""
TradePulse Quick Start Script
Demonstrates how to use the 303 files under 200 lines
"""

import os
import sys
from pathlib import Path

def show_file_categories():
    """Show different categories of files"""
    print("=" * 60)
    print("📁 TRADEPULSE FILES UNDER 200 LINES")
    print("=" * 60)
    
    categories = {
        "🔐 Authentication": [
            "auth/rbac.py (17 lines)",
            "auth/security_utils.py (32 lines)", 
            "auth/auth_core.py (106 lines)",
            "auth/user_manager.py (107 lines)",
            "auth/auth_service.py (120 lines)",
            "auth/session_manager.py (191 lines)"
        ],
        "🤖 AI Components": [
            "modular_panels/ai/model_manager_refactored.py (89 lines)",
            "modular_panels/ai/prediction_engine_refactored.py (60 lines)",
            "modular_panels/ai/training_engine_refactored.py (60 lines)",
            "modular_panels/ai/ai_panel.py (40 lines)"
        ],
        "📊 Data Management": [
            "ui_components/data_manager_refactored.py (109 lines)",
            "ui_components/dashboard_manager_refactored.py (47 lines)",
            "modular_panels/data_panel_refactored.py (131 lines)",
            "ui_components/data/data_metrics_refactored.py (59 lines)"
        ],
        "📈 Charts & Visualization": [
            "modular_panels/charts_panel_refactored.py (53 lines)",
            "demo_panels/chart_factory_refactored.py (76 lines)",
            "ui_components/charts.py (64 lines)"
        ],
        "💼 Portfolio Management": [
            "modular_panels/portfolio_panel_refactored.py (63 lines)",
            "modular_panels/portfolio/portfolio_optimizer.py (74 lines)",
            "modular_panels/portfolio/portfolio_trading.py (129 lines)"
        ],
        "🚨 Alert System": [
            "modular_panels/alerts_panel_refactored.py (68 lines)",
            "modular_panels/alerts/alert_creator_refactored.py (58 lines)",
            "ui_components/alert_component.py (71 lines)"
        ],
        "⚙️ System & Monitoring": [
            "integrated_panels/system_monitor_refactored.py (71 lines)",
            "integrated_panels/performance_display_refactored.py (75 lines)",
            "ui_components/system_status_component.py (41 lines)"
        ]
    }
    
    for category, files in categories.items():
        print(f"\n{category}:")
        for file in files:
            print(f"  ✅ {file}")
    
    print(f"\n📊 Total: 303 files under 200 lines")
    print("=" * 60)

def demonstrate_usage():
    """Demonstrate how to use the components"""
    print("\n🚀 USAGE EXAMPLES")
    print("=" * 60)
    
    examples = [
        {
            "title": "🔐 Authentication Setup",
            "code": '''
from auth.rbac import RBACManager
from auth.user_manager import UserManager

# Initialize authentication
rbac = RBACManager()
user_manager = UserManager()

# Create user with role
user = user_manager.create_user("trader1", "password123", "trader")
rbac.assign_role(user.id, "trader")
'''
        },
        {
            "title": "📊 Data Management",
            "code": '''
from ui_components.data_manager_refactored import DataManager
from ui_components.dashboard_manager_refactored import DashboardManager

# Initialize data management
data_manager = DataManager()
dashboard_manager = DashboardManager()

# Load and manage data
data = data_manager.load_data("stock_data.csv")
dashboard = dashboard_manager.create_dashboard()
'''
        },
        {
            "title": "🤖 AI Model Management",
            "code": '''
from modular_panels.ai.model_manager_refactored import ModelManager
from modular_panels.ai.prediction_engine_refactored import PredictionEngine

# Initialize AI components
model_manager = ModelManager()
prediction_engine = PredictionEngine()

# Train and predict
model = model_manager.train_model(data)
predictions = prediction_engine.predict(model, new_data)
'''
        },
        {
            "title": "📈 Chart Creation",
            "code": '''
from modular_panels.charts_panel_refactored import ChartsPanel
from demo_panels.chart_factory_refactored import ChartFactory

# Create charts
charts_panel = ChartsPanel()
chart_factory = ChartFactory()

# Generate visualizations
chart = chart_factory.create_price_chart(data)
performance_chart = charts_panel.create_performance_chart()
'''
        },
        {
            "title": "💼 Portfolio Operations",
            "code": '''
from modular_panels.portfolio_panel_refactored import PortfolioPanel
from modular_panels.portfolio.portfolio_optimizer import PortfolioOptimizer

# Portfolio management
portfolio_panel = PortfolioPanel()
optimizer = PortfolioOptimizer()

# Optimize portfolio
portfolio = portfolio_panel.create_portfolio(assets)
optimized = optimizer.optimize(portfolio, risk_tolerance)
'''
        },
        {
            "title": "🚨 Alert System",
            "code": '''
from modular_panels.alerts_panel_refactored import AlertsPanel
from modular_panels.alerts.alert_creator_refactored import AlertCreator

# Alert management
alerts_panel = AlertsPanel()
alert_creator = AlertCreator()

# Create and manage alerts
alert = alert_creator.create_price_alert("AAPL", 150.0, "above")
alerts_panel.add_alert(alert)
'''
        }
    ]
    
    for example in examples:
        print(f"\n{example['title']}:")
        print(example['code'])

def show_launch_options():
    """Show how to launch the application"""
    print("\n🎯 LAUNCH OPTIONS")
    print("=" * 60)
    
    launch_methods = [
        {
            "method": "🚀 Full Application Runner",
            "command": "python run_tradepulse_app.py",
            "description": "Handles all dependencies and port conflicts automatically"
        },
        {
            "method": "⚡ Simple Launcher",
            "command": "python simple_launcher.py", 
            "description": "Quick start with basic UI components"
        },
        {
            "method": "🔧 Refactored Main UI",
            "command": "python modular_panel_ui_main_refactored.py",
            "description": "Full modular panel interface"
        },
        {
            "method": "📊 Status Monitor",
            "command": "python app_status.py",
            "description": "Check application status and file statistics"
        }
    ]
    
    for method in launch_methods:
        print(f"\n{method['method']}:")
        print(f"  Command: {method['command']}")
        print(f"  Description: {method['description']}")
    
    print(f"\n🌐 Access URL: http://localhost:5006 (or next available port)")

def main():
    """Main function to demonstrate usage"""
    print("🎯 TRADEPULSE QUICK START GUIDE")
    print("Using 303 files under 200 lines of code")
    
    show_file_categories()
    demonstrate_usage()
    show_launch_options()
    
    print("\n" + "=" * 60)
    print("✅ Ready to use TradePulse with modular components!")
    print("=" * 60)

if __name__ == "__main__":
    main()
