#!/usr/bin/env python3
"""
TradePulse Demo Panels Module
Refactored demo panel system with focused components
"""

from .demo_panel_ui import TradePulseDemo
from .demo_data_generator import DemoDataGenerator
from .demo_ui_components import DemoUIComponents
from .demo_chart_manager import DemoChartManager
from .demo_controller import DemoController

__all__ = [
    'TradePulseDemo',
    'DemoDataGenerator',
    'DemoUIComponents',
    'DemoChartManager',
    'DemoController'
]
