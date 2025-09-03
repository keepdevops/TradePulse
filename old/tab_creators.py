#!/usr/bin/env python3
"""
TradePulse Demo Panels - Tab Creators
Handles creation of different demo tabs
"""

import panel as pn
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

class TabCreators:
    """Handles creation of different demo tabs"""
    
    def __init__(self, ui_components, chart_manager, demo_controller, data_generator):
        self.ui_components = ui_components
        self.chart_manager = chart_manager
        self.demo_controller = demo_controller
        self.data_generator = data_generator
    
    def create_main_demo_tab(self) -> pn.Column:
        """Create the main demo tab"""
        try:
            # Control section
            controls = pn.Row(
                self.ui_components.get_component('symbol_selector'),
                self.ui_components.get_component('demo_button'),
                self.ui_components.get_component('status_indicator'),
                self.ui_components.get_component('reset_button'),
                self.ui_components.get_component('export_button'),
                sizing_mode='stretch_width'
            )
            
            # Price display section
            price_displays = pn.Row(
                self.ui_components.get_component('price_display'),
                self.ui_components.get_component('change_display'),
                self.ui_components.get_component('volume_display'),
                sizing_mode='stretch_width'
            )
            
            # Market summary section
            market_summary = self.ui_components.get_component('market_summary')
            
            # Main chart section
            main_chart = pn.pane.Plotly(
                self.chart_manager.get_chart('candlestick'),
                height=400,
                sizing_mode='stretch_width'
            )
            
            # Create main demo tab
            main_tab = pn.Column(
                pn.pane.Markdown('## 🎮 Demo Controls', style={'color': 'white'}),
                controls,
                pn.Spacer(height=20),
                pn.pane.Markdown('## 📊 Price Information', style={'color': 'white'}),
                price_displays,
                pn.Spacer(height=20),
                pn.pane.Markdown('## 📈 Market Chart', style={'color': 'white'}),
                main_chart,
                pn.Spacer(height=20),
                market_summary,
                sizing_mode='stretch_width'
            )
            
            return main_tab
            
        except Exception as e:
            logger.error(f"Failed to create main demo tab: {e}")
            return pn.Column("Error: Failed to create main demo tab")
    
    def create_charts_tab(self) -> pn.Column:
        """Create the charts tab"""
        try:
            # Volume chart
            volume_chart = pn.pane.Plotly(
                self.chart_manager.get_chart('volume'),
                height=200,
                sizing_mode='stretch_width'
            )
            
            # Line chart
            line_chart = pn.pane.Plotly(
                self.chart_manager.get_chart('line'),
                height=300,
                sizing_mode='stretch_width'
            )
            
            # Portfolio performance chart
            portfolio_chart = pn.pane.Plotly(
                self.chart_manager.get_chart('portfolio_performance'),
                height=300,
                sizing_mode='stretch_width'
            )
            
            # Trading activity chart
            trading_chart = pn.pane.Plotly(
                self.chart_manager.get_chart('trading_activity'),
                height=300,
                sizing_mode='stretch_width'
            )
            
            # Create charts tab
            charts_tab = pn.Column(
                pn.pane.Markdown('## 📊 Volume Analysis', style={'color': 'white'}),
                volume_chart,
                pn.Spacer(height=20),
                pn.pane.Markdown('## 📈 Price Trends', style={'color': 'white'}),
                line_chart,
                pn.Spacer(height=20),
                pn.pane.Markdown('## 💼 Portfolio Performance', style={'color': 'white'}),
                portfolio_chart,
                pn.Spacer(height=20),
                pn.pane.Markdown('## 🎯 Trading Activity', style={'color': 'white'}),
                trading_chart,
                sizing_mode='stretch_width'
            )
            
            return charts_tab
            
        except Exception as e:
            logger.error(f"Failed to create charts tab: {e}")
            return pn.Column("Error: Failed to create charts tab")
    
    def create_portfolio_tab(self) -> pn.Column:
        """Create the portfolio tab"""
        try:
            # Portfolio summary
            portfolio_summary = self.ui_components.get_component('portfolio_summary')
            
            # Portfolio performance
            portfolio_performance = self.ui_components.get_component('portfolio_performance')
            
            # Positions table
            positions_table = self.ui_components.get_component('positions_table')
            
            # Portfolio chart
            portfolio_chart = pn.pane.Plotly(
                self.chart_manager.get_chart('bar'),
                height=300,
                sizing_mode='stretch_width'
            )
            
            # Create portfolio tab
            portfolio_tab = pn.Column(
                pn.pane.Markdown('## 💼 Portfolio Overview', style={'color': 'white'}),
                pn.Row(portfolio_summary, portfolio_performance, sizing_mode='stretch_width'),
                pn.Spacer(height=20),
                pn.pane.Markdown('## 📊 Portfolio Positions', style={'color': 'white'}),
                positions_table,
                pn.Spacer(height=20),
                pn.pane.Markdown('## 📈 Position Analysis', style={'color': 'white'}),
                portfolio_chart,
                sizing_mode='stretch_width'
            )
            
            return portfolio_tab
            
        except Exception as e:
            logger.error(f"Failed to create portfolio tab: {e}")
            return pn.Column("Error: Failed to create portfolio tab")
    
    def create_trading_tab(self) -> pn.Column:
        """Create the trading tab"""
        try:
            # Trading form
            trading_form = self.ui_components.get_component('trading_form')
            
            # Trading history
            trading_history = self.ui_components.get_component('trading_history')
            
            # Trade statistics
            trade_statistics = self.ui_components.get_component('trade_statistics')
            
            # Create trading tab
            trading_tab = pn.Column(
                pn.pane.Markdown('## 📈 Trading Interface', style={'color': 'white'}),
                trading_form,
                pn.Spacer(height=20),
                pn.pane.Markdown('## 📊 Trading History', style={'color': 'white'}),
                trading_history,
                pn.Spacer(height=20),
                pn.pane.Markdown('## 📈 Trade Statistics', style={'color': 'white'}),
                trade_statistics,
                sizing_mode='stretch_width'
            )
            
            return trading_tab
            
        except Exception as e:
            logger.error(f"Failed to create trading tab: {e}")
            return pn.Column("Error: Failed to create trading tab")
    
    def create_statistics_tab(self) -> pn.Column:
        """Create the statistics tab"""
        try:
            # Demo statistics
            demo_stats = self.demo_controller.get_demo_statistics()
            
            # Data generator statistics
            data_stats = self.data_generator.get_demo_statistics()
            
            # UI component statistics
            ui_stats = self.ui_components.get_component_status()
            
            # Chart statistics
            chart_stats = self.chart_manager.get_chart_status()
            
            # Create statistics displays
            demo_stats_display = pn.pane.Markdown(
                f"## 🎮 Demo System Statistics\n"
                f"**Demo Running:** {'Yes' if demo_stats.get('demo_controller', {}).get('is_running') else 'No'}\n"
                f"**Update Interval:** {demo_stats.get('demo_controller', {}).get('demo_interval', 0)}s\n"
                f"**Callbacks:** {demo_stats.get('demo_controller', {}).get('callbacks_count', 0)}",
                style={'color': 'white'}
            )
            
            data_stats_display = pn.pane.Markdown(
                f"## 📊 Data Statistics\n"
                f"**Symbols:** {data_stats.get('symbols_count', 0)}\n"
                f"**Data Points:** {data_stats.get('price_data_points', 0):,}\n"
                f"**Portfolio Positions:** {data_stats.get('portfolio_positions', 0)}\n"
                f"**Trading History:** {data_stats.get('trading_history_count', 0)}",
                style={'color': 'white'}
            )
            
            ui_stats_display = pn.pane.Markdown(
                f"## 🎨 UI Component Statistics\n"
                f"**Total Components:** {ui_stats.get('total_components', 0)}\n"
                f"**Callbacks:** {ui_stats.get('callbacks_count', 0)}",
                style={'color': 'white'}
            )
            
            chart_stats_display = pn.pane.Markdown(
                f"## 📈 Chart Statistics\n"
                f"**Total Charts:** {chart_stats.get('total_charts', 0)}\n"
                f"**Chart Configs:** {chart_stats.get('chart_configs', 0)}",
                style={'color': 'white'}
            )
            
            # Create statistics tab
            statistics_tab = pn.Column(
                pn.pane.Markdown('## 📊 System Statistics', style={'color': 'white'}),
                pn.Row(demo_stats_display, data_stats_display, sizing_mode='stretch_width'),
                pn.Spacer(height=20),
                pn.Row(ui_stats_display, chart_stats_display, sizing_mode='stretch_width'),
                sizing_mode='stretch_width'
            )
            
            return statistics_tab
            
        except Exception as e:
            logger.error(f"Failed to create statistics tab: {e}")
            return pn.Column("Error: Failed to create statistics tab")
