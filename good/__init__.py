#!/usr/bin/env python3
"""
TradePulse UI Panels Module
Refactored UI panel system with focused components
"""

from .panel_ui import TradePulsePanelUI
from .header_component import HeaderComponent
from .control_panel import ControlPanel
from .data_displays import DataDisplays
from .chart_manager import ChartManager
from .portfolio_widgets import PortfolioWidgets

__all__ = [
    'TradePulsePanelUI',
    'HeaderComponent',
    'ControlPanel',
    'DataDisplays',
    'ChartManager',
    'PortfolioWidgets'
]
