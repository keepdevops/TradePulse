#!/usr/bin/env python3
"""
TradePulse Charts - Chart Export Manager
Handles chart export and saving operations
"""

import pandas as pd
import json
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)

class ChartExportManager:
    """Handles chart export and saving operations"""
    
    def __init__(self):
        self.export_history = []
        self.supported_formats = ['png', 'jpg', 'svg', 'pdf', 'html', 'json']
    
    def export_chart(self, chart_data: Dict, format_type: str, 
                    export_path: Optional[str] = None) -> str:
        """
        Export chart data in the specified format
        
        Args:
            chart_data: Chart data to export
            format_type: Export format (png, jpg, svg, pdf, html, json)
            export_path: Optional custom export path
            
        Returns:
            str: Path to exported file
        """
        try:
            if format_type not in self.supported_formats:
                raise ValueError(f"Unsupported export format: {format_type}")
            
            # Generate export path if not provided
            if not export_path:
                timestamp = pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')
                export_path = f"chart_export_{timestamp}.{format_type}"
            
            # Export based on format
            if format_type == 'json':
                export_path = self._export_to_json(chart_data, export_path)
            elif format_type == 'html':
                export_path = self._export_to_html(chart_data, export_path)
            else:
                export_path = self._export_to_image(chart_data, format_type, export_path)
            
            # Record export in history
            self._record_export(chart_data, format_type, export_path)
            
            logger.info(f"✅ Chart exported successfully to {export_path}")
            return export_path
            
        except Exception as e:
            logger.error(f"❌ Chart export failed: {e}")
            raise
    
    def _export_to_json(self, chart_data: Dict, export_path: str) -> str:
        """Export chart data to JSON format"""
        try:
            # Convert chart data to JSON-serializable format
            json_data = {
                'export_timestamp': pd.Timestamp.now().isoformat(),
                'chart_data': chart_data,
                'metadata': {
                    'total_datasets': len(chart_data),
                    'export_format': 'json'
                }
            }
            
            with open(export_path, 'w') as f:
                json.dump(json_data, f, indent=2, default=str)
            
            return export_path
            
        except Exception as e:
            logger.error(f"Failed to export to JSON: {e}")
            raise
    
    def _export_to_html(self, chart_data: Dict, export_path: str) -> str:
        """Export chart data to HTML format"""
        try:
            # Create HTML representation of chart data
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>Chart Export</title>
                <style>
                    body {{ font-family: Arial, sans-serif; margin: 20px; }}
                    .dataset {{ margin: 20px 0; padding: 15px; border: 1px solid #ddd; }}
                    .stats {{ background: #f5f5f5; padding: 10px; margin: 10px 0; }}
                </style>
            </head>
            <body>
                <h1>Chart Export</h1>
                <p><strong>Export Time:</strong> {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                <p><strong>Total Datasets:</strong> {len(chart_data)}</p>
            """
            
            for dataset_id, data in chart_data.items():
                html_content += f"""
                <div class="dataset">
                    <h3>Dataset: {dataset_id}</h3>
                    <div class="stats">
                        <p><strong>Rows:</strong> {len(data)}</p>
                        <p><strong>Columns:</strong> {data.shape[1]}</p>
                        <p><strong>Columns:</strong> {', '.join(data.columns)}</p>
                    </div>
                </div>
                """
            
            html_content += """
            </body>
            </html>
            """
            
            with open(export_path, 'w') as f:
                f.write(html_content)
            
            return export_path
            
        except Exception as e:
            logger.error(f"Failed to export to HTML: {e}")
            raise
    
    def _export_to_image(self, chart_data: Dict, format_type: str, export_path: str) -> str:
        """Export chart data to image format"""
        try:
            # Here you would implement actual image export using matplotlib/plotly
            # For now, create a placeholder image export
            
            # Create a simple text representation as placeholder
            image_content = f"""
            Chart Export - {format_type.upper()}
            ================================
            Export Time: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}
            Total Datasets: {len(chart_data)}
            
            """
            
            for dataset_id, data in chart_data.items():
                image_content += f"""
                Dataset: {dataset_id}
                Rows: {len(data)}
                Columns: {data.shape[1]}
                Column Names: {', '.join(data.columns)}
                
                """
            
            # Save as text file for now (in real implementation, this would be an image)
            text_path = export_path.replace(f'.{format_type}', '.txt')
            with open(text_path, 'w') as f:
                f.write(image_content)
            
            logger.info(f"Image export placeholder saved to {text_path}")
            return text_path
            
        except Exception as e:
            logger.error(f"Failed to export to image: {e}")
            raise
    
    def _record_export(self, chart_data: Dict, format_type: str, export_path: str):
        """Record export operation in history"""
        try:
            export_record = {
                'timestamp': pd.Timestamp.now(),
                'format': format_type,
                'export_path': export_path,
                'datasets_count': len(chart_data),
                'total_rows': sum(len(data) for data in chart_data.values())
            }
            
            self.export_history.append(export_record)
            
        except Exception as e:
            logger.error(f"Failed to record export: {e}")
    
    def get_export_history(self) -> List[Dict]:
        """Get export history"""
        return self.export_history.copy()
    
    def get_export_statistics(self) -> Dict:
        """Get export statistics"""
        try:
            total_exports = len(self.export_history)
            format_counts = {}
            
            for export in self.export_history:
                format_type = export['format']
                format_counts[format_type] = format_counts.get(format_type, 0) + 1
            
            return {
                'total_exports': total_exports,
                'format_distribution': format_counts,
                'last_export': self.export_history[-1]['timestamp'] if self.export_history else None
            }
            
        except Exception as e:
            logger.error(f"Failed to get export statistics: {e}")
            return {}
    
    def clear_export_history(self) -> int:
        """Clear export history and return count of cleared records"""
        try:
            count = len(self.export_history)
            self.export_history.clear()
            logger.info(f"🗑️ Cleared {count} export records")
            return count
        except Exception as e:
            logger.error(f"Failed to clear export history: {e}")
            return 0
