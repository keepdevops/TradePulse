#!/usr/bin/env python3
"""
TradePulse Modular Panels - Base Panel Class
Base class for all module panels
"""

import panel as pn
from abc import ABC, abstractmethod
from typing import Dict, Any

class BasePanel(ABC):
    """Base class for all module panels"""
    
    def __init__(self, name: str, data_manager=None):
        self.name = name
        self.data_manager = data_manager
        self.components = {}
        self.panel = None
        self.init_panel()
    
    @abstractmethod
    def init_panel(self):
        """Initialize the panel components"""
        pass
    
    @abstractmethod
    def get_panel(self):
        """Get the panel layout"""
        pass
    
    def setup_callbacks(self, all_panels: Dict):
        """Setup callbacks for panel interactions"""
        pass
    
    def update_panel(self):
        """Update panel data"""
        pass
