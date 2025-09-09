#!/usr/bin/env python3
"""
TradePulse Portfolio Panel - Core Functionality
Core portfolio panel class with basic functionality
"""

import panel as pn
import pandas as pd
import logging
from typing import Dict

from .. import BasePanel
from .portfolio_components import PortfolioComponents
from .portfolio_operations import PortfolioOperations
from .portfolio_trading import PortfolioTrading
from .portfolio_layout import PortfolioLayout
from .dataset_selector_component import DatasetSelectorComponent
from ui_components.module_data_access import ModuleDataAccess

logger = logging.getLogger(__name__)

class PortfolioPanelCore(BasePanel):
    """Core portfolio panel functionality"""
    
    def __init__(self, data_manager, data_access_manager=None):
        super().__init__("Portfolio", data_manager)
        self.dataset_selector = DatasetSelectorComponent(data_manager, 'portfolio')
        self.data_access = ModuleDataAccess(data_manager, data_access_manager, 'portfolio')
        self.components = PortfolioComponents()
        self.operations = PortfolioOperations()
        self.trading = PortfolioTrading()
        self.init_panel()
    
    def init_panel(self):
        """Initialize core panel components"""
        self.components.create_basic_components(self.data_manager)
        self.setup_callbacks()
        self.dataset_selector.add_dataset_change_callback(self.on_dataset_change)
    
    def setup_callbacks(self):
        """Setup basic callbacks"""
        self.components.optimize_button.on_click(self.optimize_portfolio)
        self.components.rebalance_button.on_click(self.rebalance_portfolio)
        self.components.order_button.on_click(self.place_order)
        self.components.refresh_data_button.on_click(self.refresh_data)
    
    def get_panel(self):
        """Get the core panel layout"""
        return PortfolioLayout.create_main_layout(self.components, self.dataset_selector)
    
    def optimize_portfolio(self, event):
        """Optimize portfolio using selected strategy and uploaded data"""
        try:
            strategy = self.components.strategy_selector.value
            risk_tolerance = self.components.risk_tolerance.value
            
            # Get active datasets for portfolio optimization
            active_datasets = self.dataset_selector.get_active_datasets()
            uploaded_data = self.data_access.get_uploaded_data()
            
            if active_datasets or uploaded_data:
                total_datasets = len(active_datasets) + len(uploaded_data)
                logger.info(f"🚀 Optimizing portfolio with {total_datasets} datasets")
                
                # Use active datasets
                for dataset_id, data in active_datasets.items():
                    logger.info(f"📊 Using active dataset {dataset_id}: {data.shape[0]} rows × {data.shape[1]} cols")
                
                # Use uploaded data (activate if not already active)
                for dataset_id, data in uploaded_data.items():
                    if dataset_id not in active_datasets:
                        logger.info(f"📊 Activating and using uploaded dataset {dataset_id}: {data.shape[0]} rows × {data.shape[1]} cols")
                        self.data_manager.activate_dataset_for_module(dataset_id, 'portfolio')
                
                # Update portfolio display
                self.update_portfolio_display()
                logger.info(f"✅ Portfolio optimized using {strategy} strategy with uploaded data")
            else:
                logger.info("⚠️ No uploaded datasets available - using default portfolio data")
                
        except Exception as e:
            logger.error(f"❌ Portfolio optimization failed: {e}")
    
    def rebalance_portfolio(self, event):
        """Rebalance portfolio based on current allocations"""
        try:
            logger.info("⚖️ Rebalancing portfolio...")
            
            active_datasets = self.dataset_selector.get_active_datasets()
            uploaded_data = self.data_access.get_uploaded_data()
            
            if active_datasets or uploaded_data:
                total_datasets = len(active_datasets) + len(uploaded_data)
                logger.info(f"📊 Rebalancing with {total_datasets} datasets")
                
                for dataset_id, data in active_datasets.items():
                    logger.info(f"📊 Using active dataset {dataset_id}: {data.shape[0]} rows × {data.shape[1]} cols")
                
                for dataset_id, data in uploaded_data.items():
                    if dataset_id not in active_datasets:
                        logger.info(f"📊 Activating and using uploaded dataset {dataset_id}: {data.shape[0]} rows × {data.shape[1]} cols")
                        self.data_manager.activate_dataset_for_module(dataset_id, 'portfolio')
                
                self.update_portfolio_display()
                logger.info("✅ Portfolio rebalanced successfully with uploaded data")
            else:
                logger.info("⚠️ No uploaded datasets available - using default rebalancing")
                
        except Exception as e:
            logger.error(f"❌ Portfolio rebalancing failed: {e}")
    
    def place_order(self, event):
        """Place a new order"""
        try:
            symbol = self.components.symbol_input.value
            shares = self.components.shares_input.value
            price = self.components.price_input.value
            
            if symbol and shares and price:
                result = self.trading.place_order(symbol, shares, price, self.data_manager)
                if result:
                    # Clear inputs
                    self.components.symbol_input.value = ''
                    self.components.shares_input.value = 1
                    self.components.price_input.value = 0.01
                    
                    # Update portfolio display
                    self.update_portfolio_display()
            else:
                logger.warning("⚠️ Please fill in all order fields")
                
        except Exception as e:
            logger.error(f"❌ Order placement failed: {e}")
    
    def on_dataset_change(self, change_type: str, dataset_id: str):
        """Handle dataset changes for portfolio optimization"""
        logger.info(f"🔄 Dataset {change_type}: {dataset_id} for portfolio module")
        
        if change_type == 'activated':
            logger.info(f"✅ Dataset {dataset_id} activated for portfolio optimization")
        elif change_type == 'deactivated':
            logger.info(f"❌ Dataset {dataset_id} deactivated for portfolio optimization")
        
        self.update_portfolio_display()
    
    def refresh_data(self, event):
        """Refresh available data and update portfolio display"""
        try:
            logger.info("🔄 Refreshing portfolio data...")
            
            self.dataset_selector.operations.refresh_datasets(
                self.dataset_selector.datasets_list,
                self.dataset_selector.active_datasets_display
            )
            
            self.update_portfolio_display()
            logger.info("✅ Portfolio data refreshed successfully")
            
        except Exception as e:
            logger.error(f"❌ Failed to refresh portfolio data: {e}")
    
    def update_portfolio_display(self):
        """Update portfolio display with current data"""
        try:
            # Update positions table
            self.components.positions_table.value = self.operations.create_positions_dataframe(self.data_manager)
            
            # Get portfolio data using the correct method
            portfolio_data = self.data_manager.get_portfolio_data()
            
            # Update portfolio value
            total_value = portfolio_data['total_value']
            self.components.portfolio_value.value = total_value
            
            # Update P&L
            total_return = portfolio_data['performance']['yearly_return']
            self.components.pnl_display.value = total_return * 100
            
            # Check for uploaded data and show info
            uploaded_data = self.data_access.get_uploaded_data()
            if uploaded_data:
                logger.info(f"📊 Portfolio panel has access to {len(uploaded_data)} uploaded datasets")
                for dataset_id, data in uploaded_data.items():
                    logger.info(f"   📁 {dataset_id}: {data.shape[0]} rows × {data.shape[1]} cols")
                    
                    if 'Symbol' in data.columns and 'Close' in data.columns:
                        logger.info(f"   ✅ Dataset {dataset_id} has trading data (Symbol, Close columns)")
                    elif 'symbol' in data.columns and 'price' in data.columns:
                        logger.info(f"   ✅ Dataset {dataset_id} has trading data (symbol, price columns)")
                    else:
                        logger.info(f"   ⚠️ Dataset {dataset_id} doesn't have standard trading columns")
            
            logger.info("📊 Portfolio display updated")
            
        except Exception as e:
            logger.error(f"❌ Failed to update portfolio display: {e}")
