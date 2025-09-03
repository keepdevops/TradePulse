#!/usr/bin/env python3
"""
TradePulse Panel UI - Chart Components
Chart display and management components
"""

import panel as pn
from typing import Dict, Callable
import logging

from .base import BaseComponent, DataManager
from .chart_creators import ChartCreator

logger = logging.getLogger(__name__)

class ChartComponent(BaseComponent):
    """Component for creating and managing charts"""
    
    def __init__(self, data_manager: DataManager):
        super().__init__("ChartComponent")
        self.data_manager = data_manager
        self.chart_creator = ChartCreator()
        self.create_components()
    
    def create_components(self):
        """Create chart components"""
        self.components['candlestick'] = pn.pane.Plotly(
            self.chart_creator.create_candlestick_chart(self.data_manager),
            height=400
        )
        
        self.components['volume'] = pn.pane.Plotly(
            self.chart_creator.create_volume_chart(self.data_manager),
            height=200
        )
        
        self.components['indicators'] = pn.pane.Plotly(
            self.chart_creator.create_indicators_chart(self.data_manager),
            height=300
        )
        
        self.components['ml_predictions'] = pn.pane.Plotly(
            self.chart_creator.create_ml_predictions_chart(self.data_manager),
            height=300
        )
    
    def get_layout(self):
        """Get the chart layout"""
        return pn.Column(
            pn.pane.Markdown("### 📈 Price Charts"),
            self.components['candlestick'],
            self.components['volume'],
            pn.pane.Markdown("### 📊 Technical Indicators"),
            self.components['indicators'],
            pn.pane.Markdown("### 🤖 ML Predictions"),
            self.components['ml_predictions']
        )
    
    def update_charts(self, symbol: str):
        """Update all charts for a symbol"""
        self.components['candlestick'].object = self.chart_creator.create_candlestick_chart(self.data_manager, symbol)
        self.components['volume'].object = self.chart_creator.create_volume_chart(self.data_manager, symbol)
        self.components['indicators'].object = self.chart_creator.create_indicators_chart(self.data_manager, symbol)
        self.components['ml_predictions'].object = self.chart_creator.create_ml_predictions_chart(self.data_manager, symbol)
