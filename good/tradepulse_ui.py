#!/usr/bin/env python3
"""
TradePulse UI Main Coordinator
Main UI coordinator for the modular TradePulse Panel UI
"""

import panel as pn
import threading
import time
import logging
from .data_manager import DataManager
from .control_component import ControlComponent
from .data_display_component import DataDisplayComponent
from .chart_component import ChartComponent
from .portfolio_component import PortfolioComponent
from .ml_component import MLComponent
from .alert_component import AlertComponent
from .system_status_component import SystemStatusComponent
from .ui_callbacks import UICallbacks

logger = logging.getLogger(__name__)

class TradePulseModularUI:
    """Modular TradePulse Panel UI"""
    
    def __init__(self):
        self.data_manager = DataManager()
        self.current_symbol = "AAPL"
        self.update_interval = 5  # seconds
        self.is_running = False
        
        # Initialize components
        self.init_components()
        self.init_callbacks()
        self.init_layout()
        self.start_updates()
    
    def init_components(self):
        """Initialize all UI components"""
        self.header = pn.pane.Markdown("""
        # 📈 TradePulse v10.9- Modular Trading System
        ### AI-Powered Trading with Real-Time Analytics
        """)
        
        self.control_component = ControlComponent(self.data_manager)
        self.data_display_component = DataDisplayComponent(self.data_manager)
        self.chart_component = ChartComponent(self.data_manager)
        self.portfolio_component = PortfolioComponent(self.data_manager)
        self.ml_component = MLComponent(self.data_manager)
        self.alert_component = AlertComponent(self.data_manager)
        self.system_status_component = SystemStatusComponent()
    
    def init_callbacks(self):
        """Initialize component callbacks"""
        self.callbacks = UICallbacks(self)
        
        # Control component callbacks
        self.control_component.set_symbol_change_callback(self.callbacks.on_symbol_change)
        self.control_component.set_start_callback(self.callbacks.start_trading)
        self.control_component.set_stop_callback(self.callbacks.stop_trading)
        
        # Portfolio component callbacks
        self.portfolio_component.set_optimize_callback(self.callbacks.optimize_portfolio)
        self.portfolio_component.set_place_order_callback(self.callbacks.place_order)
        
        # ML component callbacks
        self.ml_component.set_predict_callback(self.callbacks.generate_prediction)
        
        # Alert component callbacks
        self.alert_component.set_add_alert_callback(self.callbacks.add_alert)
    
    def init_layout(self):
        """Initialize the main layout"""
        self.main_layout = pn.Column(
            self.header,
            self.control_component.get_layout(),
            self.data_display_component.get_layout(),
            pn.Row(
                pn.Column(self.chart_component.get_layout(), width=60),
                pn.Column(self.portfolio_component.get_layout(), width=20),
                pn.Column(
                    self.ml_component.get_layout(),
                    self.alert_component.get_layout(),
                    self.system_status_component.get_layout(),
                    width=20
                )
            ),
            sizing_mode='stretch_width'
        )
    
    def start_updates(self):
        """Start periodic updates"""
        def update_loop():
            while True:
                try:
                    self.data_display_component.update_price_display(self.current_symbol)
                    self.portfolio_component.update_portfolio_display()
                    time.sleep(self.update_interval)
                except Exception as e:
                    logger.error(f"❌ Error in update loop: {e}")
                    time.sleep(self.update_interval)
        
        threading.Thread(target=update_loop, daemon=True).start()
    
    def get_app(self):
        """Get the Panel app"""
        return self.main_layout
