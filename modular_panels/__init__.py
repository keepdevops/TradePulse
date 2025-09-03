#!/usr/bin/env python3
"""
TradePulse Modular Panels Module
Refactored modular panel system with focused components
"""

from .base_component import BaseComponent
from .base_panel import BasePanel
from .data_panel import DataPanel
from .models_panel import ModelsPanel
from .portfolio_panel import PortfolioPanel
from .ai_panel import AIPanel
from .charts_panel import ChartsPanel
from .alerts_panel import AlertsPanel
from .system_panel import SystemPanel
from .component_registry import ComponentRegistry
from .module_integration import ModuleIntegration

__all__ = [
    'BaseComponent',
    'BasePanel',
    'DataPanel',
    'ModelsPanel',
    'PortfolioPanel',
    'AIPanel',
    'ChartsPanel',
    'AlertsPanel',
    'SystemPanel',
    'ComponentRegistry',
    'ModuleIntegration'
]
