#!/usr/bin/env python3
"""
TradePulse Data Panel - Export
Data export functionality for the data panel
"""

import pandas as pd
import logging
from typing import Optional

logger = logging.getLogger(__name__)

class DataExport:
    """Data export functionality"""
    
    def quick_export_csv(self, data: pd.DataFrame) -> str:
        """Quick export data to CSV format"""
        try:
            if data is None or data.empty:
                return "### ❌ No Data to Export\nPlease fetch or upload data first."
            
            # Create filename with timestamp
            timestamp = pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')
            filename = f"tradepulse_data_{timestamp}.csv"
            
            # Export to CSV
            data.to_csv(filename, index=False)
            
            logger.info(f"✅ Data exported to {filename}")
            
            return f"""
            ### ✅ Export Successful!
            
            **File**: {filename}
            **Format**: CSV
            **Records**: {len(data):,}
            **Columns**: {len(data.columns)}
            
            File saved to: `/Users/moose/TradePulse/{filename}`
            
            ---
            *Click Export again to export with different options*
            """
            
        except Exception as e:
            logger.error(f"Quick export failed: {e}")
            return f"### ❌ Export Failed\nError: {str(e)}"
    
    def export_data_advanced(self, data: pd.DataFrame, format_type: str, filename: str) -> str:
        """Advanced export with multiple formats"""
        try:
            if data is None or data.empty:
                return "### ❌ No Data to Export\nPlease fetch or upload data first."
            
            # Ensure filename has no spaces and is valid
            filename = filename.replace(' ', '_')
            
            if format_type == 'csv':
                filepath = f"{filename}.csv"
                data.to_csv(filepath, index=False)
            elif format_type == 'json':
                filepath = f"{filename}.json"
                data.to_json(filepath, orient='records')
            elif format_type == 'excel':
                filepath = f"{filename}.xlsx"
                data.to_excel(filepath, index=False)
            elif format_type == 'feather':
                filepath = f"{filename}.feather"
                data.to_feather(filepath)
            elif format_type == 'parquet':
                filepath = f"{filename}.parquet"
                data.to_parquet(filepath)
            else:
                return f"### ❌ Export Failed\nUnsupported format: {format_type}"
            
            logger.info(f"✅ Data exported to {filepath}")
            
            return f"""
            ### ✅ Export Successful!
            
            **File**: {filepath}
            **Format**: {format_type.upper()}
            **Records**: {len(data):,}
            **Columns**: {len(data.columns)}
            
            File saved to: `/Users/moose/TradePulse/{filepath}`
            """
            
        except Exception as e:
            logger.error(f"Advanced export failed: {e}")
            return f"### ❌ Export Failed\nError: {str(e)}"
    
    def get_export_formats(self) -> list:
        """Get available export formats"""
        return ['CSV', 'JSON', 'Excel', 'Feather', 'Parquet']
    
    def validate_filename(self, filename: str) -> bool:
        """Validate filename for export"""
        if not filename or len(filename.strip()) == 0:
            return False
        
        # Check for invalid characters
        invalid_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
        return not any(char in filename for char in invalid_chars)
