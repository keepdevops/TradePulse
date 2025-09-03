#!/usr/bin/env python3
"""
TradePulse Data Metrics - Management
UI management for the data metrics
"""

import panel as pn
import logging

logger = logging.getLogger(__name__)

class DataMetricsManagement:
    """UI management for data metrics"""
    
    @staticmethod
    def create_metrics_summary(metrics: dict) -> str:
        """Create metrics summary for display"""
        try:
            if not metrics or metrics.get('row_count', 0) == 0:
                return "No data available for analysis"
            
            summary_lines = [
                f"**Dataset Size**: {metrics.get('row_count', 0):,} rows × {metrics.get('column_count', 0)} columns",
                f"**Memory Usage**: {metrics.get('memory_usage_mb', 0.0):.2f} MB",
                f"**Data Types**: {metrics.get('numeric_columns', 0)} numeric, {metrics.get('categorical_columns', 0)} categorical",
                f"**Missing Values**: {metrics.get('missing_values', {}).get('total_missing', 0):,} ({metrics.get('missing_values', {}).get('missing_percentage', 0.0):.1f}%)",
                f"**Duplicates**: {metrics.get('duplicate_count', 0):,} rows"
            ]
            
            return "\n".join(summary_lines)
            
        except Exception as e:
            logger.error(f"Failed to create metrics summary: {e}")
            return "Error creating summary"
    
    @staticmethod
    def create_metrics_report(metrics: dict, data) -> dict:
        """Create comprehensive metrics report"""
        try:
            report = {
                'basic_info': {
                    'rows': metrics.get('row_count', 0),
                    'columns': metrics.get('column_count', 0),
                    'memory_mb': metrics.get('memory_usage_mb', 0.0),
                    'data_types': metrics.get('data_types', {})
                },
                'quality_metrics': {
                    'missing_values': metrics.get('missing_values', {}),
                    'duplicates': metrics.get('duplicate_count', 0),
                    'consistency': metrics.get('consistency', {})
                },
                'statistical_summary': {
                    'numeric_columns': metrics.get('numeric_columns', 0),
                    'categorical_columns': metrics.get('categorical_columns', 0),
                    'numeric_statistics': metrics.get('numeric_statistics', {}),
                    'categorical_statistics': metrics.get('categorical_statistics', {})
                }
            }
            
            return report
            
        except Exception as e:
            logger.error(f"Failed to create metrics report: {e}")
            return {}
    
    @staticmethod
    def create_metrics_display(metrics: dict):
        """Create metrics display panel"""
        try:
            if not metrics or metrics.get('row_count', 0) == 0:
                return pn.pane.Markdown("""
                ### 📊 Data Metrics
                **Status**: No data available
                """)
            
            metrics_text = f"""
            ### 📊 Data Metrics
            
            **Dataset Size**: {metrics.get('row_count', 0):,} rows × {metrics.get('column_count', 0)} columns  
            **Memory Usage**: {metrics.get('memory_usage_mb', 0.0):.2f} MB  
            **Data Types**: {metrics.get('numeric_columns', 0)} numeric, {metrics.get('categorical_columns', 0)} categorical  
            **Missing Values**: {metrics.get('missing_values', {}).get('total_missing', 0):,} ({metrics.get('missing_values', {}).get('missing_percentage', 0.0):.1f}%)  
            **Duplicates**: {metrics.get('duplicate_count', 0):,} rows
            """
            
            return pn.pane.Markdown(metrics_text)
            
        except Exception as e:
            logger.error(f"Failed to create metrics display: {e}")
            return pn.pane.Markdown("Error: Failed to create metrics display")
    
    @staticmethod
    def create_history_display(history: list):
        """Create history display panel"""
        try:
            if not history:
                return pn.pane.Markdown("""
                ### 📈 Calculation History
                No calculations recorded
                """)
            
            history_lines = ["### 📈 Calculation History"]
            for record in history[-5:]:  # Show last 5 records
                timestamp = record.get('timestamp', 'Unknown')
                rows = record.get('row_count', 0)
                cols = record.get('column_count', 0)
                memory = record.get('memory_mb', 0.0)
                history_lines.append(f"- **{timestamp}**: {rows:,} rows, {cols} cols, {memory:.2f} MB")
            
            return pn.pane.Markdown("\n".join(history_lines))
            
        except Exception as e:
            logger.error(f"Failed to create history display: {e}")
            return pn.pane.Markdown("Error: Failed to create history display")
    
    @staticmethod
    def create_error_display(error_message: str):
        """Create error display"""
        return pn.pane.Markdown(f"""
        ### ❌ Error
        **Message**: {error_message}
        """)
    
    @staticmethod
    def create_success_display(success_message: str):
        """Create success display"""
        return pn.pane.Markdown(f"""
        ### ✅ Success
        **Message**: {success_message}
        """)
    
    @staticmethod
    def create_loading_display():
        """Create loading display"""
        return pn.pane.Markdown("""
        ### ⏳ Calculating Metrics...
        Please wait while we analyze your data.
        """)



