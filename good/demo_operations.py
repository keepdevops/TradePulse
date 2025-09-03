#!/usr/bin/env python3
"""
TradePulse Demo Panels - Demo Operations
Handles demo system operations and management
"""

from datetime import datetime
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

class DemoOperations:
    """Handles demo system operations and management"""
    
    def __init__(self, demo_controller, ui_components, chart_manager):
        self.demo_controller = demo_controller
        self.ui_components = ui_components
        self.chart_manager = chart_manager
    
    def start_demo(self):
        """Start the demo system"""
        try:
            logger.info("🚀 Starting demo system")
            self.demo_controller.start_demo()
        except Exception as e:
            logger.error(f"Failed to start demo: {e}")
    
    def stop_demo(self):
        """Stop the demo system"""
        try:
            logger.info("⏸ Stopping demo system")
            self.demo_controller.stop_demo()
        except Exception as e:
            logger.error(f"Failed to stop demo: {e}")
    
    def reset_demo(self):
        """Reset the demo system"""
        try:
            logger.info("🔄 Resetting demo system")
            self.demo_controller.reset_demo()
        except Exception as e:
            logger.error(f"Failed to reset demo: {e}")
    
    def refresh_demo(self):
        """Refresh the demo system"""
        try:
            logger.info("🔄 Refreshing demo system")
            
            # Refresh UI components
            self.ui_components.refresh_components()
            
            # Refresh charts
            self.chart_manager.refresh_charts()
            
            logger.info("✅ Demo system refreshed")
            
        except Exception as e:
            logger.error(f"Failed to refresh demo: {e}")
    
    def get_demo_status(self) -> Dict[str, Any]:
        """Get comprehensive demo status"""
        try:
            return {
                'demo_controller': self.demo_controller.get_demo_status(),
                'ui_components': self.ui_components.get_component_status(),
                'chart_manager': self.chart_manager.get_chart_status(),
                'demo_timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Failed to get demo status: {e}")
            return {}
    
    def test_demo_system(self) -> Dict[str, bool]:
        """Test the demo system functionality"""
        try:
            test_results = {}
            
            # Test UI components
            try:
                ui_stats = self.ui_components.get_component_status()
                test_results['ui_components'] = bool(ui_stats)
            except Exception:
                test_results['ui_components'] = False
            
            # Test chart manager
            try:
                chart_stats = self.chart_manager.get_chart_status()
                test_results['chart_manager'] = bool(chart_stats)
            except Exception:
                test_results['chart_manager'] = False
            
            # Test demo controller
            try:
                controller_stats = self.demo_controller.get_demo_status()
                test_results['demo_controller'] = bool(controller_stats)
            except Exception:
                test_results['demo_controller'] = False
            
            # Overall test result
            test_results['overall'] = all(test_results.values())
            
            return test_results
            
        except Exception as e:
            logger.error(f"Failed to test demo system: {e}")
            return {'overall': False}
    
    def export_demo_data(self, data_generator) -> Dict[str, Any]:
        """Export demo data"""
        try:
            export_data = {
                'data_generator': data_generator.export_demo_data(),
                'demo_controller': self.demo_controller.export_demo_state(),
                'export_timestamp': datetime.now().isoformat()
            }
            
            logger.info("📤 Demo data exported")
            return export_data
            
        except Exception as e:
            logger.error(f"Failed to export demo data: {e}")
            return {}
    
    def import_demo_data(self, demo_data: Dict[str, Any], data_generator):
        """Import demo data"""
        try:
            if 'data_generator' in demo_data:
                data_generator.import_demo_data(demo_data['data_generator'])
            
            if 'demo_controller' in demo_data:
                self.demo_controller.import_demo_state(demo_data['demo_controller'])
            
            logger.info("📥 Demo data imported")
            
        except Exception as e:
            logger.error(f"Failed to import demo data: {e}")
    
    def cleanup_demo_system(self):
        """Cleanup the demo system"""
        try:
            logger.info("🧹 Cleaning up demo system")
            
            # Cleanup demo controller
            self.demo_controller.cleanup_demo_system()
            
            logger.info("✅ Demo system cleanup completed")
            
        except Exception as e:
            logger.error(f"Failed to cleanup demo system: {e}")
    
    def setup_initial_displays(self):
        """Setup initial display values"""
        try:
            logger.info("🔧 Setting up initial displays")
            
            # Update all displays
            self.ui_components._update_all_displays()
            
            # Update charts
            self.chart_manager.update_charts()
            
            logger.info("✅ Initial displays setup completed")
            
        except Exception as e:
            logger.error(f"Failed to setup initial displays: {e}")
