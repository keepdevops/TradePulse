"""
Data Exporter
Contains methods for exporting data to various formats.
"""

import pandas as pd
from datetime import datetime
from pathlib import Path
from typing import Optional
from utils.logger import LoggerMixin


class DataExporter(LoggerMixin):
    """
    Class for exporting data to various formats.
    
    This class contains the data export methods that were extracted
    from DataFetcher to keep files under 250 lines.
    """
    
    def __init__(self, message_bus):
        """Initialize the data exporter."""
        super().__init__()
        self.message_bus = message_bus
    
    def export_data(
        self, 
        data: pd.DataFrame, 
        ticker: str, 
        format: str = 'csv', 
        filepath: Optional[str] = None
    ) -> bool:
        """
        Export data for a ticker to file.
        
        Args:
            data: Data to export
            ticker: Ticker symbol
            format: Export format ('csv', 'excel', 'json')
            filepath: Output file path (optional)
        
        Returns:
            True if export was successful
        """
        try:
            # Determine filepath
            if filepath is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filepath = f"./exports/{ticker}_{timestamp}.{format}"
            
            # Ensure export directory exists
            Path(filepath).parent.mkdir(parents=True, exist_ok=True)
            
            # Export based on format
            if format.lower() == 'csv':
                data.to_csv(filepath, index=False)
            elif format.lower() == 'excel':
                data.to_excel(filepath, index=False)
            elif format.lower() == 'json':
                data.to_json(filepath, orient='records', indent=2)
            else:
                self.log_error(f"Unsupported export format: {format}")
                return False
            
            self.log_info(f"Exported {ticker} data to {filepath}")
            
            # Publish export message
            self.message_bus.publish("data_exported", {
                'ticker': ticker,
                'format': format,
                'filepath': filepath,
                'rows': len(data)
            })
            
            return True
            
        except Exception as e:
            self.log_error(f"Error exporting data for {ticker}: {e}")
            return False
