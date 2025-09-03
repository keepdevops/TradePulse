#!/usr/bin/env python3
"""
TradePulse Data Panel - Components
UI components for the data panel
"""

import panel as pn
import pandas as pd
import numpy as np
import logging

logger = logging.getLogger(__name__)

class DataComponents:
    """UI components for data panel"""
    
    def __init__(self):
        self.symbol_selector = None
        self.timeframe_selector = None
        self.data_source = None
        self.fetch_button = None
        self.export_button = None
        self.clear_button = None
        self.data_table = None
        self.data_stats = None
        self.export_dialog = None
    
    def create_basic_components(self, data_manager):
        """Create basic UI components"""
        # Symbol selector
        self.symbol_selector = pn.widgets.Select(
            name='Symbol',
            options=data_manager.symbols,
            value='AAPL',
            width=150
        )
        
        # Timeframe selector
        self.timeframe_selector = pn.widgets.Select(
            name='Timeframe',
            options=['1m', '5m', '15m', '1h', '1d'],
            value='1h',
            width=100
        )
        
        # Fetch data button
        self.fetch_button = pn.widgets.Button(
            name='📥 Fetch Data',
            button_type='primary',
            width=120
        )
        
        # Data source selector
        self.data_source = pn.widgets.Select(
            name='Data Source',
            options=['Yahoo Finance', 'Alpha Vantage', 'IEX Cloud', 'Mock Data'],
            value='Mock Data',
            width=150
        )
        
        # Data preview table
        self.data_table = pn.widgets.Tabulator(
            self._create_sample_data(),
            height=300
        )
        
        # Data statistics
        self.data_stats = pn.pane.Markdown("""
        ### 📊 Data Statistics
        - **Total Records**: 365
        - **Date Range**: 2024-01-01 to 2024-12-31
        - **Symbols**: 8
        - **Last Updated**: 2024-12-31 23:59:59
        """)
        
        # Export button
        self.export_button = pn.widgets.Button(
            name='💾 Quick Export',
            button_type='primary',
            width=120
        )
        
        # Clear button
        self.clear_button = pn.widgets.Button(
            name='🗑️ Clear Data',
            button_type='warning',
            width=120
        )
        
        # Export dialog area
        self.export_dialog = pn.pane.Markdown("")
    
    def _create_sample_data(self):
        """Create sample data for preview"""
        dates = pd.date_range(start='2024-12-25', end='2024-12-31', freq='D')
        data = []
        
        for date in dates:
            data.append({
                'Date': date.strftime('%Y-%m-%d'),
                'Open': 150.0 + np.random.normal(0, 2),
                'High': 155.0 + np.random.normal(0, 2),
                'Low': 145.0 + np.random.normal(0, 2),
                'Close': 152.0 + np.random.normal(0, 2),
                'Volume': int(1000000 + np.random.normal(0, 200000))
            })
        
        return pd.DataFrame(data)
