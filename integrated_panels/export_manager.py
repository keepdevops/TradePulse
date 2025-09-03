#!/usr/bin/env python3
"""
TradePulse Integrated Panels - Export Manager
Handles export functionality
"""

import pandas as pd
from datetime import datetime
from typing import Dict, List, Any
import logging

logger = logging.getLogger(__name__)

class ExportManager:
    """Handles export functionality"""
    
    def __init__(self):
        pass
    
    def export_data(self, ui_components: Dict[str, Any]):
        """Export current data"""
        try:
            # Prepare export data
            export_data = self.prepare_export_data(ui_components)
            
            # Create export file
            self.create_export_file(export_data)
            
        except Exception as e:
            logger.error(f"Failed to export data: {e}")
    
    def prepare_export_data(self, ui_components: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Prepare data for export"""
        try:
            export_data = []
            
            # Add timestamp
            export_data.append({
                'type': 'export_timestamp',
                'data': datetime.now().isoformat(),
                'timestamp': datetime.now().isoformat()
            })
            
            # Add component values
            component_values = {}
            for name, component in ui_components.items():
                if hasattr(component, 'value'):
                    component_values[name] = component.value
                elif hasattr(component, 'object'):
                    component_values[name] = str(component.object)
            
            export_data.append({
                'type': 'ui_component_values',
                'data': component_values,
                'timestamp': datetime.now().isoformat()
            })
            
            return export_data
            
        except Exception as e:
            logger.error(f"Failed to prepare export data: {e}")
            return []
    
    def create_export_file(self, export_data: List[Dict[str, Any]]):
        """Create export file"""
        try:
            # Convert to DataFrame for easy export
            df = pd.DataFrame(export_data)
            
            # Export to CSV
            filename = f"ui_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            df.to_csv(filename, index=False)
            
            logger.info(f"✅ Export file created: {filename}")
            
        except Exception as e:
            logger.error(f"Failed to create export file: {e}")
