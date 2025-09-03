#!/usr/bin/env python3
"""
TradePulse Panel UI - Main Application
Main application that orchestrates all components
"""

import panel as pn
import logging
from typing import Dict

# Import TradePulse modules
try:
    from utils.message_bus_client import MessageBusClient
    from utils.database import Database
    from utils.logger import setup_logger
    from models_grid.adm import ADMModel
    from models_grid.cipo import CIPOModel
    from models_grid.bicipo import BICIPOModel
    from ai_module.portfolio.portfolio_optimizer import PortfolioOptimizer
    from ai_module.handlers.strategy_handler import StrategyHandler
    from ai_module.handlers.risk_assessment_handler import RiskAssessmentHandler
    from ai_module.handlers.portfolio_optimization_handler import PortfolioOptimizationHandler
    from data_grid.fetcher import DataFetcher
    from data_grid.chart_manager import ChartManager
    from portfolio_strategies.markowitz_optimizer import MarkowitzOptimizer
    from portfolio_strategies.risk_parity_optimizer import RiskParityOptimizer
    from portfolio_strategies.sharpe_optimizer import SharpeOptimizer
    from visualization_components.predictions_plotter import PredictionsPlotter
    from visualization_components.feature_importance_plotter import FeatureImportancePlotter
    from visualization_components.model_comparison_plotter import ModelComparisonPlotter
    from visualization_components.training_history_plotter import TrainingHistoryPlotter
    print("✅ All TradePulse modules imported successfully")
except ImportError as e:
    print(f"⚠️ Some modules not available: {e}")
    # Create mock classes for missing modules
    class MockModule:
        def __init__(self, *args, **kwargs):
            pass
        def predict(self, *args, **kwargs):
            return np.random.normal(0, 1, 10)
        def fit(self, *args, **kwargs):
            pass
    
    MessageBusClient = MockModule
    Database = MockModule
    ADMModel = MockModule
    CIPOModel = MockModule
    BICIPOModel = MockModule
    PortfolioOptimizer = MockModule
    StrategyHandler = MockModule
    RiskAssessmentHandler = MockModule
    PortfolioOptimizationHandler = MockModule
    DataFetcher = MockModule
    ChartManager = MockModule
    MarkowitzOptimizer = MockModule
    RiskParityOptimizer = MockModule
    SharpeOptimizer = MockModule
    PredictionsPlotter = MockModule
    FeatureImportancePlotter = MockModule
    ModelComparisonPlotter = MockModule
    TrainingHistoryPlotter = MockModule

# Import UI components
from .base import DataManager
from .charts import ChartComponent
from .controls import ControlComponent, DataDisplayComponent
from .portfolio import PortfolioComponent, MLComponent
from .alerts import AlertComponent, SystemStatusComponent
from .events import EventHandler

# Configure Panel
pn.extension('plotly', 'tabulator', sizing_mode='stretch_width')
pn.config.theme = 'dark'

# Setup logging
logger = setup_logger(__name__) if 'setup_logger' in globals() else logging.getLogger(__name__)

class TradePulseModularUI:
    """Modular TradePulse Panel UI"""
    
    def __init__(self):
        self.data_manager = DataManager()
        self.components = {}
        self.event_handler = None
        
        # Initialize components
        self.init_components()
        self.init_event_handler()
        self.init_callbacks()
        self.init_layout()
        self.start_updates()
    
    def init_components(self):
        """Initialize all UI components"""
        self.header = pn.pane.Markdown("""
        # 🚀 TradePulse v10.8 - Modular Trading System
        ### AI-Powered Trading with Real-Time Analytics
        """)
        
        self.components['control'] = ControlComponent(self.data_manager)
        self.components['data_display'] = DataDisplayComponent(self.data_manager)
        self.components['chart'] = ChartComponent(self.data_manager)
        self.components['portfolio'] = PortfolioComponent(self.data_manager)
        self.components['ml'] = MLComponent(self.data_manager)
        self.components['alert'] = AlertComponent(self.data_manager)
        self.components['system_status'] = SystemStatusComponent()
    
    def init_event_handler(self):
        """Initialize event handler"""
        self.event_handler = EventHandler(self.data_manager, self.components)
    
    def init_callbacks(self):
        """Initialize component callbacks"""
        # Control component callbacks
        self.components['control'].set_symbol_change_callback(self.event_handler.on_symbol_change)
        self.components['control'].set_start_callback(self.event_handler.start_trading)
        self.components['control'].set_stop_callback(self.event_handler.stop_trading)
        
        # Portfolio component callbacks
        self.components['portfolio'].set_optimize_callback(self.event_handler.optimize_portfolio)
        self.components['portfolio'].set_place_order_callback(self.event_handler.place_order)
        
        # ML component callbacks
        self.components['ml'].set_predict_callback(self.event_handler.generate_prediction)
        
        # Alert component callbacks
        self.components['alert'].set_add_alert_callback(self.event_handler.add_alert)
    
    def init_layout(self):
        """Initialize the main layout"""
        self.main_layout = pn.Column(
            self.header,
            self.components['control'].get_layout(),
            self.components['data_display'].get_layout(),
            pn.Row(
                pn.Column(self.components['chart'].get_layout(), width=60),
                pn.Column(self.components['portfolio'].get_layout(), width=20),
                pn.Column(
                    self.components['ml'].get_layout(),
                    self.components['alert'].get_layout(),
                    self.components['system_status'].get_layout(),
                    width=20
                )
            ),
            sizing_mode='stretch_width'
        )
    
    def start_updates(self):
        """Start periodic updates"""
        self.event_handler.start_updates()
    
    def get_app(self):
        """Get the Panel app"""
        return self.main_layout

def main():
    """Main function to run the modular Panel UI"""
    logger.info("🚀 Starting TradePulse Modular Panel UI...")
    
    ui = TradePulseModularUI()
    app = ui.get_app()
    
    # Configure the app
    app.servable()
    
    logger.info("✅ TradePulse Modular Panel UI ready")
    return app

if __name__ == "__main__":
    app = main()
    app.show()
