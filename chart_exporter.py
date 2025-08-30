"""
Chart Exporter
Contains methods for exporting charts to various formats.
"""

from typing import Any, Optional
from utils.logger import LoggerMixin


class ChartExporter(LoggerMixin):
    """Handles chart export functionality."""
    
    def export_chart(
        self, 
        chart: Any, 
        ticker: str, 
        chart_type: str,
        format: str = 'html',
        filepath: Optional[str] = None,
        message_bus: Optional[Any] = None
    ) -> Optional[str]:
        """
        Export a chart to file.
        
        Args:
            chart: Chart object to export
            ticker: Stock ticker symbol
            chart_type: Type of chart (e.g., 'candlestick', 'line')
            format: Export format ('html', 'png', 'pdf')
            filepath: Output file path (optional)
            message_bus: Message bus for publishing export events
        
        Returns:
            Path to exported file or None if failed
        """
        try:
            if chart is None:
                self.log_warning(f"No chart to export for {ticker}")
                return None
            
            # For now, delegate to chart implementations
            # This could be enhanced with direct export logic
            if hasattr(chart, 'write_html') and format == 'html':
                if filepath is None:
                    filepath = f"charts/{ticker}_{chart_type}.html"
                
                chart.write_html(filepath)
                self.log_info(f"Exported {chart_type} chart for {ticker} to {filepath}")
                
                # Publish export event if message bus available
                if message_bus:
                    message_bus.publish("chart_exported", {
                        'ticker': ticker,
                        'chart_type': chart_type,
                        'format': format,
                        'filepath': filepath
                    })
                
                return filepath
            else:
                self.log_warning(f"Export format {format} not supported for {ticker}")
                return None
            
        except Exception as e:
            self.log_error(f"Error exporting chart for {ticker}: {e}")
            return None
