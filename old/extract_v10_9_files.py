#!/usr/bin/env python3
"""
Manually extract V10.9 files from the complete list
"""

def extract_v10_9_files():
    """Extract V10.9 files manually"""
    v10_9_files = set()
    
    # Launch Scripts
    v10_9_files.update([
        'launch_modular_ui.py',
        'launch_integrated_ui.py',
        'launch_demo_ui.py',
        'launch_comprehensive_ui.py',
        'launch_panel_ui.py',
        'modular_panel_ui_main_refactored.py'
    ])
    
    # Test Scripts
    v10_9_files.update([
        'test_all_refactored_modules.py',
        'test_modular_panels.py',
        'test_integrated_panels.py',
        'test_ui_panels.py',
        'test_ui_components.py',
        'test_demo_panels.py',
        'test_launch_scripts.py',
        'test_auth_system.py',
        'test_auth_security_utils.py',
        'test_auth_user_manager.py',
        'test_auth_rbac.py',
        'test_auth_session_manager.py',
        'test_auth_service.py',
        'test_auth_admin.py'
    ])
    
    # Auth Module
    v10_9_files.update([
        'auth/__init__.py',
        'auth/auth_admin_ops.py',
        'auth/auth_core.py',
        'auth/auth_maintenance_ops.py',
        'auth/auth_security_ops.py',
        'auth/auth_service.py',
        'auth/auth_session_ops.py',
        'auth/auth_user_ops.py',
        'auth/rbac_core.py',
        'auth/rbac_manager.py',
        'auth/rbac_permissions_core.py',
        'auth/rbac_permissions.py',
        'auth/rbac_role_definitions.py',
        'auth/rbac.py',
        'auth/security_core.py',
        'auth/security_extended.py',
        'auth/security_utils.py',
        'auth/session_core.py',
        'auth/session_db_ops.py',
        'auth/session_maintenance_ops.py',
        'auth/session_manager.py',
        'auth/session_query_ops.py',
        'auth/session_storage.py',
        'auth/session_validation.py',
        'auth/user_activity_advanced.py',
        'auth/user_activity_core.py',
        'auth/user_activity_ops.py',
        'auth/user_core.py',
        'auth/user_crud_ops.py',
        'auth/user_db_ops.py',
        'auth/user_manager.py',
        'auth/user_update_ops.py'
    ])
    
    # Modular Panels Core
    v10_9_files.update([
        'modular_panels/__init__.py',
        'modular_panels/data_panel.py',
        'modular_panels/models_panel.py',
        'modular_panels/portfolio_panel.py',
        'modular_panels/ai_panel.py',
        'modular_panels/charts_panel.py',
        'modular_panels/alerts_panel.py',
        'modular_panels/system_panel.py',
        'modular_panels/base_component.py',
        'modular_panels/base_panel.py',
        'modular_panels/chart_creators.py',
        'modular_panels/component_registry.py',
        'modular_panels/component_templates.py',
        'modular_panels/data_upload_component.py',
        'modular_panels/dataset_selector_callbacks.py',
        'modular_panels/dataset_selector_component.py',
        'modular_panels/dataset_selector_operations.py',
        'modular_panels/dataset_selector_ui_components.py',
        'modular_panels/duplicate_detector.py',
        'modular_panels/integration_analyzer.py',
        'modular_panels/integration_statistics.py',
        'modular_panels/module_integration.py',
        'modular_panels/module_registry.py',
        'modular_panels/portfolio_operations.py',
        'modular_panels/registry_manager.py',
        'modular_panels/shared_components.py',
        'modular_panels/system_operations.py'
    ])
    
    # AI Sub-components
    v10_9_files.update([
        'modular_panels/ai/__init__.py',
        'modular_panels/ai/ai_callbacks.py',
        'modular_panels/ai/ai_operations.py',
        'modular_panels/ai/ai_panel.py',
        'modular_panels/ai/ai_ui_components.py',
        'modular_panels/ai/model_manager.py',
        'modular_panels/ai/prediction_engine.py',
        'modular_panels/ai/training_engine.py'
    ])
    
    # Alerts Sub-components
    v10_9_files.update([
        'modular_panels/alerts/__init__.py',
        'modular_panels/alerts/alert_callbacks.py',
        'modular_panels/alerts/alert_conditions.py',
        'modular_panels/alerts/alert_creator.py',
        'modular_panels/alerts/alert_display.py',
        'modular_panels/alerts/alert_layout.py',
        'modular_panels/alerts/alert_manager.py',
        'modular_panels/alerts/alert_notifications.py',
        'modular_panels/alerts/alert_operations.py',
        'modular_panels/alerts/alerts_panel.py'
    ])
    
    # Charts Sub-components
    v10_9_files.update([
        'modular_panels/charts/__init__.py',
        'modular_panels/charts/chart_callbacks.py',
        'modular_panels/charts/chart_data_processor.py',
        'modular_panels/charts/chart_display.py',
        'modular_panels/charts/chart_export.py',
        'modular_panels/charts/chart_layout.py',
        'modular_panels/charts/chart_manager.py',
        'modular_panels/charts/charts_panel.py'
    ])
    
    # Data Upload Sub-components
    v10_9_files.update([
        'modular_panels/data_upload/__init__.py',
        'modular_panels/data_upload/data_manager_integration.py',
        'modular_panels/data_upload/data_upload_component.py',
        'modular_panels/data_upload/database_loaders.py',
        'modular_panels/data_upload/database_processors.py',
        'modular_panels/data_upload/file_loader.py',
        'modular_panels/data_upload/file_loaders.py',
        'modular_panels/data_upload/file_processor.py',
        'modular_panels/data_upload/file_processors.py',
        'modular_panels/data_upload/format_detector.py',
        'modular_panels/data_upload/format_processors.py',
        'modular_panels/data_upload/processing_history.py',
        'modular_panels/data_upload/text_loaders.py',
        'modular_panels/data_upload/text_processors.py',
        'modular_panels/data_upload/upload_manager.py'
    ])
    
    # Portfolio Sub-components
    v10_9_files.update([
        'modular_panels/portfolio/__init__.py',
        'modular_panels/portfolio/layout_manager.py',
        'modular_panels/portfolio/operations_manager.py',
        'modular_panels/portfolio/optimization_history.py',
        'modular_panels/portfolio/optimization_strategies.py',
        'modular_panels/portfolio/portfolio_manager.py',
        'modular_panels/portfolio/portfolio_optimizer.py',
        'modular_panels/portfolio/portfolio_panel.py',
        'modular_panels/portfolio/portfolio_risk.py',
        'modular_panels/portfolio/ui_components.py'
    ])
    
    # Dataset Selector Sub-components
    v10_9_files.update([
        'modular_panels/dataset_selector/__init__.py',
        'modular_panels/dataset_selector/dataset_activator.py',
        'modular_panels/dataset_selector/dataset_browser.py',
        'modular_panels/dataset_selector/dataset_preview.py',
        'modular_panels/dataset_selector/dataset_selector_component.py'
    ])
    
    # Integrated Panels
    v10_9_files.update([
        'integrated_panels/__init__.py',
        'integrated_panels/alert_checker.py',
        'integrated_panels/component_accessor.py',
        'integrated_panels/component_integrator.py',
        'integrated_panels/database_handler.py',
        'integrated_panels/export_manager.py',
        'integrated_panels/integrated_panel_ui.py',
        'integrated_panels/integration_callbacks.py',
        'integrated_panels/integration_dashboard.py',
        'integrated_panels/integration_initializer.py',
        'integrated_panels/integration_status_tab.py',
        'integrated_panels/integration_summary.py',
        'integrated_panels/layout_manager.py',
        'integrated_panels/main.py',
        'integrated_panels/message_handler.py',
        'integrated_panels/metrics_exporter.py',
        'integrated_panels/monitoring_setup.py',
        'integrated_panels/operation_profiler.py',
        'integrated_panels/performance_display.py',
        'integrated_panels/performance_metrics.py',
        'integrated_panels/performance_tracker.py',
        'integrated_panels/section_creators.py',
        'integrated_panels/system_cleanup.py',
        'integrated_panels/system_integrators.py',
        'integrated_panels/system_monitor.py',
        'integrated_panels/system_tester.py',
        'integrated_panels/tradepulse_integration.py',
        'integrated_panels/ui_components.py',
        'integrated_panels/ui_orchestrator.py',
        'integrated_panels/update_manager.py',
        'integrated_panels/system_monitoring/dashboard_creator.py',
        'integrated_panels/system_monitoring/health_monitor.py'
    ])
    
    # UI Panels
    v10_9_files.update([
        'ui_panels/__init__.py',
        'ui_panels/chart_creator.py',
        'ui_panels/chart_manager.py',
        'ui_panels/chart_operations.py',
        'ui_panels/control_callbacks.py',
        'ui_panels/control_operations.py',
        'ui_panels/control_panel.py',
        'ui_panels/control_ui_components.py',
        'ui_panels/data_displays.py',
        'ui_panels/data_manager.py',
        'ui_panels/header_component.py',
        'ui_panels/layout_manager.py',
        'ui_panels/panel_ui.py',
        'ui_panels/portfolio_layout_manager.py',
        'ui_panels/portfolio_operations.py',
        'ui_panels/portfolio_ui_components.py',
        'ui_panels/portfolio_widgets.py',
        'ui_panels/trading_manager.py',
        'ui_panels/update_manager.py'
    ])
    
    # UI Components
    v10_9_files.update([
        'ui_components/__init__.py',
        'ui_components/alert_component.py',
        'ui_components/alerts.py',
        'ui_components/base_component.py',
        'ui_components/base.py',
        'ui_components/chart_component.py',
        'ui_components/chart_creators.py',
        'ui_components/charts.py',
        'ui_components/control_component.py',
        'ui_components/controls.py',
        'ui_components/data_display_component.py',
        'ui_components/data_manager.py',
        'ui_components/data_updater.py',
        'ui_components/event_handlers.py',
        'ui_components/events.py',
        'ui_components/main.py',
        'ui_components/ml_component.py',
        'ui_components/portfolio_component.py',
        'ui_components/portfolio.py',
        'ui_components/system_status_component.py',
        'ui_components/tradepulse_ui.py',
        'ui_components/ui_callbacks.py',
        'ui_components/data/__init__.py',
        'ui_components/data/data_manager.py',
        'ui_components/data/data_processor.py',
        'ui_components/data/data_metrics.py',
        'ui_components/data/dataset_registry.py'
    ])
    
    # Demo Panels
    v10_9_files.update([
        'demo_panels/__init__.py',
        'demo_panels/chart_factory.py',
        'demo_panels/demo_callbacks.py',
        'demo_panels/demo_chart_manager.py',
        'demo_panels/demo_controller.py',
        'demo_panels/demo_data_generator.py',
        'demo_panels/demo_operations_manager.py',
        'demo_panels/demo_operations.py',
        'demo_panels/demo_panel_ui.py',
        'demo_panels/demo_ui_components.py',
        'demo_panels/portfolio_data_generator.py',
        'demo_panels/price_data_generator.py',
        'demo_panels/tab_creators.py',
        'demo_panels/trading_history_generator.py',
        'demo_panels/ui_components/control_components.py',
        'demo_panels/ui_components/display_components.py'
    ])
    
    return v10_9_files

def main():
    """Main function"""
    v10_9_files = extract_v10_9_files()
    
    # Write to file
    with open('v10_9_files_list.txt', 'w') as f:
        for file_path in sorted(v10_9_files):
            f.write(f"{file_path}\n")
    
    print(f"✅ Extracted {len(v10_9_files)} V10.9 files to v10_9_files_list.txt")

if __name__ == "__main__":
    main()
