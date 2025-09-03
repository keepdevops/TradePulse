#!/usr/bin/env python3
"""
TradePulse Modular Panels - Integration Statistics
Handles integration statistics and reporting
"""

import logging
from typing import Dict, List, Any
from datetime import datetime

logger = logging.getLogger(__name__)

class IntegrationStatistics:
    """Handles integration statistics and reporting"""
    
    def __init__(self, module_registry, shared_components, integration_analyzer):
        self.module_registry = module_registry
        self.shared_components = shared_components
        self.integration_analyzer = integration_analyzer
    
    def get_integration_statistics(self) -> Dict[str, Any]:
        """Get comprehensive integration statistics"""
        try:
            total_modules = len(self.module_registry.integrated_modules)
            total_shared_components = len(self.shared_components.shared_components)
            total_integrations = len(self.module_registry.integration_history)
            
            # Calculate success rate
            successful_integrations = sum(1 for record in self.module_registry.integration_history if record['status'] == 'success')
            success_rate = (successful_integrations / total_integrations * 100) if total_integrations > 0 else 0
            
            # Get module type breakdown
            module_types = {}
            for info in self.module_registry.integrated_modules.values():
                module_type = info['type']
                module_types[module_type] = module_types.get(module_type, 0) + 1
            
            # Get system health
            health_summary = self.integration_analyzer.get_system_health_summary()
            
            return {
                'total_modules': total_modules,
                'total_shared_components': total_shared_components,
                'total_integrations': total_integrations,
                'successful_integrations': successful_integrations,
                'success_rate': success_rate,
                'module_types': module_types,
                'duplicates_detected': len(self.integration_analyzer.detect_duplicate_functionality()),
                'last_integration': self.module_registry.integration_history[-1]['timestamp'] if self.module_registry.integration_history else None,
                'system_health': health_summary
            }
            
        except Exception as e:
            logger.error(f"Failed to get integration statistics: {e}")
            return {}
    
    def export_integration_state(self) -> Dict[str, Any]:
        """Export the complete integration state"""
        try:
            export_data = {
                'integrated_modules': {name: {'type': info['type'], 'path': info['path'], 'status': info['status']} 
                                     for name, info in self.module_registry.integrated_modules.items()},
                'shared_components': list(self.shared_components.shared_components.keys()),
                'integration_history': self.module_registry.integration_history.copy(),
                'export_timestamp': datetime.now()
            }
            
            logger.info("📤 Module integration state exported")
            return export_data
            
        except Exception as e:
            logger.error(f"Failed to export integration state: {e}")
            return {}
    
    def import_integration_state(self, integration_data: Dict[str, Any]):
        """Import integration state from external source"""
        try:
            if 'integration_history' in integration_data:
                self.module_registry.integration_history.extend(integration_data['integration_history'])
            
            logger.info("📥 Module integration state imported")
            
        except Exception as e:
            logger.error(f"Failed to import integration state: {e}")
    
    def generate_integration_report(self) -> str:
        """Generate a human-readable integration report"""
        try:
            stats = self.get_integration_statistics()
            
            report = f"""
# TradePulse Module Integration Report
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Overview
- **Total Modules**: {stats.get('total_modules', 0)}
- **Total Shared Components**: {stats.get('total_shared_components', 0)}
- **Integration Success Rate**: {stats.get('success_rate', 0):.1f}%
- **System Health**: {stats.get('system_health', {}).get('overall_health', 0):.1%}

## Module Types
"""
            
            for module_type, count in stats.get('module_types', {}).items():
                report += f"- **{module_type}**: {count} modules\n"
            
            report += f"""
## Issues
"""
            
            issues = stats.get('system_health', {}).get('issues', [])
            if issues:
                for issue in issues:
                    report += f"- {issue}\n"
            else:
                report += "- No issues detected\n"
            
            report += f"""
## Recent Activity
"""
            
            recent_integrations = self.module_registry.integration_history[-5:] if self.module_registry.integration_history else []
            for record in recent_integrations:
                status_icon = "✅" if record['status'] == 'success' else "❌"
                report += f"- {status_icon} {record['module_name']} ({record['module_type']}) - {record['status']}\n"
            
            return report
            
        except Exception as e:
            logger.error(f"Failed to generate integration report: {e}")
            return f"Error generating report: {e}"
    
    def get_performance_metrics(self) -> Dict[str, Any]:
        """Get performance-related metrics"""
        try:
            stats = self.get_integration_statistics()
            
            # Calculate performance metrics
            avg_components_per_module = (stats.get('total_shared_components', 0) / 
                                       stats.get('total_modules', 1))
            
            # Calculate integration efficiency
            efficiency = (stats.get('successful_integrations', 0) / 
                         max(stats.get('total_integrations', 1), 1))
            
            return {
                'avg_components_per_module': avg_components_per_module,
                'integration_efficiency': efficiency,
                'system_health_score': stats.get('system_health', {}).get('overall_health', 0),
                'duplicate_ratio': (stats.get('duplicates_detected', 0) / 
                                  max(stats.get('total_modules', 1), 1))
            }
            
        except Exception as e:
            logger.error(f"Failed to get performance metrics: {e}")
            return {}
