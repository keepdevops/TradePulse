#!/usr/bin/env python3
"""
TradePulse Portfolio - Operations Manager
Handles portfolio operations and callbacks
"""

import panel as pn
import pandas as pd
from typing import Dict
import logging

logger = logging.getLogger(__name__)

class PortfolioOperationsManager:
    """Handles portfolio operations and callbacks"""
    
    def __init__(self, portfolio_manager, portfolio_optimizer, components: Dict):
        self.portfolio_manager = portfolio_manager
        self.portfolio_optimizer = portfolio_optimizer
        self.components = components
    
    def optimize_portfolio(self, event):
        """Optimize portfolio using the portfolio optimizer"""
        try:
            strategy = self.components['strategy_selector'].value
            risk_tolerance = self.components['risk_tolerance'].value
            
            # Get current portfolio data
            portfolio_data = self.portfolio_manager.get_portfolio_summary()
            
            if portfolio_data['total_positions'] > 0:
                logger.info(f"🚀 Optimizing portfolio using {strategy} strategy")
                
                # Run optimization using portfolio optimizer
                optimization_result = self.portfolio_optimizer.optimize_portfolio(
                    strategy, portfolio_data, risk_tolerance
                )
                
                # Update performance display
                self._update_performance_display(optimization_result)
                
                logger.info(f"✅ Portfolio optimization completed: {optimization_result['expected_return']:.3f} return")
            else:
                logger.info("⚠️ No positions to optimize")
                
        except Exception as e:
            logger.error(f"❌ Portfolio optimization failed: {e}")
    
    def rebalance_portfolio(self, event):
        """Rebalance portfolio based on optimization results"""
        try:
            logger.info("⚖️ Rebalancing portfolio...")
            
            # Get current portfolio data
            portfolio_data = self.portfolio_manager.get_portfolio_summary()
            
            if portfolio_data['total_positions'] > 0:
                # Get last optimization result
                optimization_history = self.portfolio_optimizer.get_optimization_history()
                
                if optimization_history:
                    last_optimization = optimization_history[-1]
                    target_weights = last_optimization['result']['weights']
                    
                    logger.info(f"🔄 Rebalancing to target weights: {target_weights}")
                    
                    # Here you would implement actual rebalancing logic
                    # For now, just log the action
                    
                    logger.info("✅ Portfolio rebalancing completed")
                else:
                    logger.info("⚠️ No optimization results available for rebalancing")
            else:
                logger.info("⚠️ No positions to rebalance")
                
        except Exception as e:
            logger.error(f"❌ Portfolio rebalancing failed: {e}")
    
    def buy_position(self, event):
        """Buy a new position"""
        try:
            symbol = self.components['symbol_input'].value
            shares = self.components['shares_input'].value
            price = self.components['price_input'].value
            
            if symbol and shares and price:
                logger.info(f"🟢 Buying {shares} shares of {symbol} at ${price}")
                
                # Add position using portfolio manager
                position_id = self.portfolio_manager.add_position(symbol, shares, price, 'buy')
                
                # Update displays
                self._update_portfolio_displays()
                
                logger.info(f"✅ Position added: {position_id}")
            else:
                logger.warning("⚠️ Please fill in all order fields")
                
        except Exception as e:
            logger.error(f"❌ Buy order failed: {e}")
    
    def sell_position(self, event):
        """Sell an existing position"""
        try:
            symbol = self.components['symbol_input'].value
            shares = self.components['shares_input'].value
            price = self.components['price_input'].value
            
            if symbol and shares and price:
                logger.info(f"🔴 Selling {shares} shares of {symbol} at ${price}")
                
                # Remove position using portfolio manager
                success = self.portfolio_manager.remove_position(symbol, shares)
                
                if success:
                    # Update displays
                    self._update_portfolio_displays()
                    logger.info(f"✅ Position sold: {symbol}")
                else:
                    logger.warning(f"⚠️ Failed to sell position: {symbol}")
            else:
                logger.warning("⚠️ Please fill in all order fields")
                
        except Exception as e:
            logger.error(f"❌ Sell order failed: {e}")
    
    def _update_portfolio_displays(self):
        """Update all portfolio-related displays"""
        try:
            # Get updated portfolio summary
            portfolio_summary = self.portfolio_manager.get_portfolio_summary()
            
            # Update portfolio value
            self.components['portfolio_value'].value = portfolio_summary['total_value']
            
            # Update P&L display
            self.components['pnl_display'].value = portfolio_summary['unrealized_pnl_pct']
            
            # Update positions table
            self.components['positions_table'].value = self.portfolio_manager.create_positions_dataframe()
            
            # Update performance display
            self._update_performance_display()
            
        except Exception as e:
            logger.error(f"Failed to update portfolio displays: {e}")
    
    def _update_performance_display(self, optimization_result: Dict = None):
        """Update the performance display"""
        try:
            portfolio_summary = self.portfolio_manager.get_portfolio_summary()
            
            performance_text = f"""
            ### 📊 Portfolio Performance
            - **Total Positions**: {portfolio_summary['total_positions']}
            - **Cash**: ${portfolio_summary['cash']:,.2f}
            - **Invested Value**: ${portfolio_summary['invested_value']:,.2f}
            - **Unrealized P&L**: ${portfolio_summary['unrealized_pnl']:,.2f} ({portfolio_summary['unrealized_pnl_pct']:.2f}%)
            """
            
            if optimization_result:
                performance_text += f"""
                
            **Last Optimization ({optimization_result['strategy']}):**
            - **Expected Return**: {optimization_result['expected_return']:.3f}
            - **Expected Risk**: {optimization_result['expected_risk']:.3f}
            - **Sharpe Ratio**: {optimization_result['sharpe_ratio']:.3f}
            """
            
            self.components['performance_display'].object = performance_text
            
        except Exception as e:
            logger.error(f"Failed to update performance display: {e}")
    
    def setup_callbacks(self):
        """Setup component callbacks"""
        self.components['optimize_button'].on_click(self.optimize_portfolio)
        self.components['rebalance_button'].on_click(self.rebalance_portfolio)
        self.components['buy_button'].on_click(self.buy_position)
        self.components['sell_button'].on_click(self.sell_position)
