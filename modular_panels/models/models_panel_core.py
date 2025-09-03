#!/usr/bin/env python3
"""
TradePulse Models Panel - Core Functionality
Core models panel class with basic functionality
"""

import panel as pn
import logging
from typing import Dict

from .models_panel_components import ModelsPanelComponents
from .models_panel_operations import ModelsPanelOperations
from .models_panel_management import ModelsPanelManagement
from .models_panel_callbacks import ModelsPanelCallbacks
from ..dataset_selector_component import DatasetSelectorComponent
from ..model_storage import ModelStorage
from ..model_training import ModelTrainer
from ..model_performance import ModelPerformanceTracker
from ..model_ui_components import ModelUIComponents
from ..model_data_manager import ModelDataManager
from ..model_ui_init import ModelUIInitializer
from ui_components.module_data_access import ModuleDataAccess

logger = logging.getLogger(__name__)

class ModelsPanelCore:
    """Core models panel functionality"""
    
    def __init__(self, data_manager, data_access_manager=None):
        self.dataset_selector = DatasetSelectorComponent(data_manager, 'models')
        self.data_access = ModuleDataAccess(data_manager, data_access_manager, 'models')
        self.model_storage = ModelStorage()
        self.model_trainer = ModelTrainer(self.model_storage)
        self.performance_tracker = ModelPerformanceTracker()
        self.ui_components = ModelUIComponents()
        self.data_manager_helper = ModelDataManager(self.data_access, data_manager)
        self.ui_initializer = ModelUIInitializer()
        
        # Initialize components
        self.components = ModelsPanelComponents()
        self.operations = ModelsPanelOperations()
        self.management = ModelsPanelManagement()
        self.callbacks = None
        
        self.init_panel()
    
    def init_panel(self):
        """Initialize models panel components"""
        # Dataset selector
        self.components['dataset_selector'] = self.dataset_selector.get_component()
        
        # Model selector
        self.components['model_selector'] = self.ui_initializer.create_model_selector()
        
        # Training parameters
        training_params = self.ui_initializer.create_training_parameters()
        self.components.update(training_params)
        
        # Action buttons
        action_buttons = self.ui_initializer.create_action_buttons()
        self.components.update(action_buttons)
        
        # Display components
        display_components = self.ui_initializer.create_display_components(self.performance_tracker)
        self.components.update(display_components)
        
        # Initialize callbacks
        logger.info("🔧 Initializing ModelCallbacks...")
        self.callbacks = ModelsPanelCallbacks(
            self.performance_tracker,
            self.model_trainer,
            self.ui_components,
            self.components
        )
        
        # Verify callbacks object is properly created
        if self.callbacks is None:
            logger.error("❌ Failed to create ModelCallbacks instance")
            raise RuntimeError("ModelCallbacks initialization failed")
        
        # Setup callbacks
        self.ui_initializer.setup_callbacks(
            self.components,
            self.callbacks,
            self.data_access,
            self.data_manager_helper,
            self.model_storage
        )
        
        # Store a reference to ensure it doesn't get lost
        self._callbacks_reference = self.callbacks
        logger.info(f"✅ Stored callbacks reference: {self._callbacks_reference is not None}")
        
        # Final verification of callbacks
        logger.info(f"✅ Callbacks initialized: {self.callbacks is not None}")
        if self.callbacks:
            available_methods = [method for method in dir(self.callbacks) if not method.startswith('_')]
            logger.info(f"✅ Callback methods available: {available_methods}")
            
            # Verify critical methods exist
            critical_methods = ['update_performance_callback', 'update_status_callback', 'update_progress_callback']
            for method in critical_methods:
                if hasattr(self.callbacks, method):
                    logger.info(f"✅ Critical method '{method}' is available")
                else:
                    logger.error(f"❌ Critical method '{method}' is missing!")
        else:
            logger.error("❌ Callbacks object is None after initialization!")
    
    def get_panel(self):
        """Get the models panel layout"""
        return self.management.create_main_layout(self.components, self.ui_components)
    
    def train_model(self, event):
        """Train the selected model using uploaded data"""
        return self.operations.train_model(
            self.components,
            self.callbacks,
            self.data_access,
            self.data_manager_helper,
            self.model_trainer,
            self.ui_components
        )
    
    def make_prediction(self, event):
        """Make prediction with selected model using uploaded data"""
        return self.operations.make_prediction(
            self.components,
            self.callbacks,
            self.data_access,
            self.data_manager_helper,
            self.model_trainer,
            self.ui_components
        )
    
    def __post_init__(self):
        """Post-initialization tasks"""
        # Safety check: ensure we have valid callbacks
        callbacks_to_use = self.callbacks if self.callbacks is not None else getattr(self, '_callbacks_reference', None)
        if callbacks_to_use:
            try:
                callbacks_to_use.refresh_data(None, self.data_access, self.data_manager_helper)
                logger.info("✅ Post-init data refresh completed")
            except Exception as e:
                logger.warning(f"⚠️ Could not refresh data in post-init: {e}")
        else:
            logger.info("ℹ️ Callbacks not yet initialized, skipping post-init refresh")



