#!/usr/bin/env python3
"""
TradePulse Dashboard Manager - Operations
Dashboard-related operations for the dashboard manager
"""

import logging
from typing import Dict, Any, List, Tuple
from datetime import datetime

logger = logging.getLogger(__name__)

class DashboardManagerOperations:
    """Dashboard-related operations for dashboard manager"""
    
    def validate_dashboard_config(self, config: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """Validate dashboard configuration"""
        errors = []
        
        # Check required fields
        required_fields = ['panels', 'role']
        for field in required_fields:
            if field not in config:
                errors.append(f"Missing required field: {field}")
        
        # Validate role
        if 'role' in config:
            role = config['role']
            valid_roles = ['day_trader', 'ml_analyst', 'default']
            if role not in valid_roles:
                errors.append(f"Invalid role: {role}. Must be one of {valid_roles}")
        
        # Validate panels
        if 'panels' in config:
            panels = config['panels']
            if not isinstance(panels, dict):
                errors.append("Panels must be a dictionary")
            else:
                # Check for required panels
                required_panels = ['📊 Data', '💼 Portfolio']
                for panel in required_panels:
                    if panel not in panels:
                        errors.append(f"Missing required panel: {panel}")
        
        return len(errors) == 0, errors
    
    def create_dashboard_id(self) -> str:
        """Create unique dashboard session ID"""
        import uuid
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        unique_id = str(uuid.uuid4())[:8]
        return f"dashboard_{timestamp}_{unique_id}"
    
    def get_dashboard_info(self) -> Dict[str, Any]:
        """Get information about dashboard capabilities"""
        return {
            'supported_roles': [
                'day_trader', 'ml_analyst', 'default'
            ],
            'layout_types': [
                '3-column grid', 'tabbed interface', 'full-width sections'
            ],
            'panel_types': [
                'Data', 'Portfolio', 'AI', 'Alerts', 'Charts', 'System'
            ],
            'customization_level': 'Role-based'
        }
    
    def get_dashboard_statistics(self, dashboard_data: List[Dict]) -> Dict[str, Any]:
        """Get statistics about dashboard data"""
        if not dashboard_data:
            return {
                'total_dashboards': 0,
                'active_dashboards': 0,
                'role_distribution': {},
                'average_panels': 0
            }
        
        stats = {
            'total_dashboards': len(dashboard_data),
            'active_dashboards': len([d for d in dashboard_data if d.get('active', False)]),
            'role_distribution': {},
            'average_panels': sum(len(d.get('panels', {})) for d in dashboard_data) / len(dashboard_data) if dashboard_data else 0
        }
        
        # Calculate role distribution
        for dashboard in dashboard_data:
            role = dashboard.get('role', 'unknown')
            stats['role_distribution'][role] = stats['role_distribution'].get(role, 0) + 1
        
        return stats
    
    def filter_dashboard_data(self, data: List[Dict], role: str = None, 
                             active: bool = None, panel_count: int = None) -> List[Dict]:
        """Filter dashboard data by various criteria"""
        filtered_data = data
        
        if role:
            filtered_data = [d for d in filtered_data if d.get('role') == role]
        
        if active is not None:
            filtered_data = [d for d in filtered_data if d.get('active') == active]
        
        if panel_count is not None:
            filtered_data = [d for d in filtered_data if len(d.get('panels', {})) == panel_count]
        
        return filtered_data
    
    def sort_dashboard_data(self, data: List[Dict], sort_by: str = 'created_at', 
                           reverse: bool = True) -> List[Dict]:
        """Sort dashboard data"""
        return sorted(data, key=lambda x: x.get(sort_by, ''), reverse=reverse)
    
    def get_dashboard_summary(self, dashboard_data: List[Dict]) -> str:
        """Get summary of dashboard data"""
        if not dashboard_data:
            return "No dashboard data available"
        
        stats = self.get_dashboard_statistics(dashboard_data)
        
        summary_lines = [
            f"**Total Dashboards**: {stats['total_dashboards']}",
            f"**Active Dashboards**: {stats['active_dashboards']}",
            f"**Average Panels**: {stats['average_panels']:.1f}",
            f"**Role Distribution**: {stats['role_distribution']}"
        ]
        
        return "\n".join(summary_lines)



