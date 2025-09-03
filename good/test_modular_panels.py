#!/usr/bin/env python3
"""
TradePulse Test - Modular Panels
Tests modular panels module
"""

def run_tests():
    """Test modular panels module"""
    print("🧪 Testing Modular Panels...")
    errors = []
    
    try:
        from modular_panels import (
            DataPanel, ModelsPanel, PortfolioPanel, 
            AIPanel, ChartsPanel, AlertsPanel, SystemPanel
        )
        print("✅ All modular panel classes imported successfully")
        
        # Test creating instances
        try:
            from ui_components.data_manager import DataManager
            dm = DataManager()
            
            # Test each panel
            panels = [
                ('DataPanel', DataPanel),
                ('ModelsPanel', ModelsPanel), 
                ('PortfolioPanel', PortfolioPanel),
                ('AIPanel', AIPanel),
                ('ChartsPanel', ChartsPanel),
                ('AlertsPanel', AlertsPanel),
                ('SystemPanel', SystemPanel)
            ]
            
            for name, panel_class in panels:
                try:
                    if name == 'SystemPanel':
                        panel = panel_class()  # No data manager needed
                    else:
                        panel = panel_class(dm)
                    print(f"✅ {name} created successfully")
                except Exception as e:
                    error_msg = f"❌ Failed to create {name}: {e}"
                    print(error_msg)
                    errors.append(error_msg)
                    
        except Exception as e:
            error_msg = f"❌ Failed to create DataManager: {e}"
            print(error_msg)
            errors.append(error_msg)
            
    except Exception as e:
        error_msg = f"❌ Failed to import modular panels: {e}"
        print(error_msg)
        errors.append(error_msg)
    
    return len(errors) == 0, errors
