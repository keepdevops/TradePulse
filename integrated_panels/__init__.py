#!/usr/bin/env python3
"""
TradePulse Integrated Panels Module
Refactored integrated panel system with focused components
"""

from .integrated_panel_ui import TradePulseIntegratedUI
from .tradepulse_integration import TradePulseIntegration
from .ui_orchestrator import UIOrchestrator
from .system_monitor import SystemMonitor
from .performance_tracker import PerformanceTracker

__all__ = [
    'TradePulseIntegratedUI',
    'TradePulseIntegration',
    'UIOrchestrator',
    'SystemMonitor',
    'PerformanceTracker'
]
