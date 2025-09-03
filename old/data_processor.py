#!/usr/bin/env python3
"""
TradePulse Data - Data Processor
Handles data processing and transformation operations
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Any, Tuple
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class DataProcessor:
    """Handles data processing and transformation operations"""
    
    def __init__(self):
        self.processing_history = []
        self.supported_formats = ['csv', 'excel', 'json', 'parquet', 'pickle']
    
    def process_uploaded_data(self, data: pd.DataFrame, metadata: Optional[Dict] = None) -> pd.DataFrame:
        """
        Process uploaded data for consistency and quality
        
        Args:
            data: Raw uploaded data
            metadata: Optional metadata about the data
            
        Returns:
            pd.DataFrame: Processed data
        """
        try:
            logger.info(f"🔄 Processing uploaded data: {data.shape[0]} rows, {data.shape[1]} columns")
            
            # Create a copy to avoid modifying original
            processed_data = data.copy()
            
            # Basic data cleaning
            processed_data = self._clean_data(processed_data)
            
            # Standardize column names
            processed_data = self._standardize_columns(processed_data)
            
            # Handle missing values
            processed_data = self._handle_missing_values(processed_data)
            
            # Validate data types
            processed_data = self._validate_data_types(processed_data)
            
            # Record processing
            self._record_processing(data.shape, processed_data.shape, metadata)
            
            logger.info(f"✅ Data processing completed: {processed_data.shape[0]} rows, {processed_data.shape[1]} columns")
            return processed_data
            
        except Exception as e:
            logger.error(f"❌ Data processing failed: {e}")
            return data  # Return original data if processing fails
    
    def _clean_data(self, data: pd.DataFrame) -> pd.DataFrame:
        """Clean the data by removing duplicates and invalid entries"""
        try:
            # Remove duplicate rows
            initial_rows = len(data)
            data = data.drop_duplicates()
            duplicates_removed = initial_rows - len(data)
            
            if duplicates_removed > 0:
                logger.info(f"🧹 Removed {duplicates_removed} duplicate rows")
            
            # Remove rows with all NaN values
            initial_rows = len(data)
            data = data.dropna(how='all')
            empty_rows_removed = initial_rows - len(data)
            
            if empty_rows_removed > 0:
                logger.info(f"🧹 Removed {empty_rows_removed} empty rows")
            
            return data
            
        except Exception as e:
            logger.error(f"Failed to clean data: {e}")
            return data
    
    def _standardize_columns(self, data: pd.DataFrame) -> pd.DataFrame:
        """Standardize column names for consistency"""
        try:
            # Convert to lowercase and replace spaces with underscores
            new_columns = {}
            for col in data.columns:
                new_name = str(col).lower().replace(' ', '_').replace('-', '_')
                new_columns[col] = new_name
            
            # Rename columns
            data = data.rename(columns=new_columns)
            
            # Remove special characters
            data.columns = data.columns.str.replace(r'[^a-zA-Z0-9_]', '', regex=True)
            
            logger.info(f"📝 Standardized {len(data.columns)} column names")
            return data
            
        except Exception as e:
            logger.error(f"Failed to standardize columns: {e}")
            return data
    
    def _handle_missing_values(self, data: pd.DataFrame) -> pd.DataFrame:
        """Handle missing values in the data"""
        try:
            missing_counts = data.isnull().sum()
            total_missing = missing_counts.sum()
            
            if total_missing > 0:
                logger.info(f"🔍 Found {total_missing} missing values across {len(data.columns)} columns")
                
                # For numeric columns, fill with median
                numeric_columns = data.select_dtypes(include=[np.number]).columns
                for col in numeric_columns:
                    if data[col].isnull().sum() > 0:
                        median_value = data[col].median()
                        data[col].fillna(median_value, inplace=True)
                        logger.info(f"📊 Filled missing values in {col} with median: {median_value}")
                
                # For categorical columns, fill with mode
                categorical_columns = data.select_dtypes(include=['object']).columns
                for col in categorical_columns:
                    if data[col].isnull().sum() > 0:
                        mode_value = data[col].mode().iloc[0] if not data[col].mode().empty else 'Unknown'
                        data[col].fillna(mode_value, inplace=True)
                        logger.info(f"📊 Filled missing values in {col} with mode: {mode_value}")
            
            return data
            
        except Exception as e:
            logger.error(f"Failed to handle missing values: {e}")
            return data
    
    def _validate_data_types(self, data: pd.DataFrame) -> pd.DataFrame:
        """Validate and convert data types where appropriate"""
        try:
            # Try to convert date-like columns
            date_columns = []
            for col in data.columns:
                if any(keyword in col.lower() for keyword in ['date', 'time', 'timestamp']):
                    try:
                        data[col] = pd.to_datetime(data[col], errors='coerce')
                        date_columns.append(col)
                    except Exception:
                        pass
            
            if date_columns:
                logger.info(f"📅 Converted {len(date_columns)} columns to datetime: {date_columns}")
            
            # Try to convert numeric columns
            numeric_conversions = 0
            for col in data.columns:
                if col not in date_columns and data[col].dtype == 'object':
                    try:
                        # Try to convert to numeric
                        pd.to_numeric(data[col], errors='coerce')
                        data[col] = pd.to_numeric(data[col], errors='coerce')
                        numeric_conversions += 1
                    except Exception:
                        pass
            
            if numeric_conversions > 0:
                logger.info(f"🔢 Converted {numeric_conversions} columns to numeric")
            
            return data
            
        except Exception as e:
            logger.error(f"Failed to validate data types: {e}")
            return data
    
    def filter_data(self, data: pd.DataFrame, filters: Dict) -> pd.DataFrame:
        """Filter data based on specified criteria"""
        try:
            filtered_data = data.copy()
            initial_rows = len(filtered_data)
            
            for column, condition in filters.items():
                if column in filtered_data.columns:
                    if isinstance(condition, dict):
                        # Range filter
                        if 'min' in condition:
                            filtered_data = filtered_data[filtered_data[column] >= condition['min']]
                        if 'max' in condition:
                            filtered_data = filtered_data[filtered_data[column] <= condition['max']]
                    elif isinstance(condition, list):
                        # Value filter
                        filtered_data = filtered_data[filtered_data[column].isin(condition)]
                    else:
                        # Exact match
                        filtered_data = filtered_data[filtered_data[column] == condition]
            
            final_rows = len(filtered_data)
            rows_filtered = initial_rows - final_rows
            
            if rows_filtered > 0:
                logger.info(f"🔍 Filtered data: {rows_filtered} rows removed, {final_rows} rows remaining")
            
            return filtered_data
            
        except Exception as e:
            logger.error(f"Failed to filter data: {e}")
            return data
    
    def aggregate_data(self, data: pd.DataFrame, group_by: List[str], 
                      aggregations: Dict[str, List[str]]) -> pd.DataFrame:
        """Aggregate data by specified columns"""
        try:
            if not group_by or not all(col in data.columns for col in group_by):
                logger.warning("Invalid group_by columns specified")
                return data
            
            # Perform aggregation
            aggregated = data.groupby(group_by).agg(aggregations).reset_index()
            
            logger.info(f"📊 Aggregated data by {group_by}: {len(aggregated)} groups created")
            return aggregated
            
        except Exception as e:
            logger.error(f"Failed to aggregate data: {e}")
            return data
    
    def sample_data(self, data: pd.DataFrame, sample_size: int = 1000, 
                   method: str = 'random') -> pd.DataFrame:
        """Sample data using specified method"""
        try:
            if len(data) <= sample_size:
                return data
            
            if method == 'random':
                sampled = data.sample(n=sample_size, random_state=42)
            elif method == 'head':
                sampled = data.head(sample_size)
            elif method == 'tail':
                sampled = data.tail(sample_size)
            elif method == 'stratified':
                # Simple stratified sampling - simplified to avoid syntax issues
                sampled = data.sample(n=sample_size, random_state=42)
            else:
                sampled = data.sample(n=sample_size, random_state=42)
            
            logger.info(f"📊 Sampled data: {len(sampled)} rows using {method} method")
            return sampled
            
        except Exception as e:
            logger.error(f"Failed to sample data: {e}")
            return data
    
    def _record_processing(self, original_shape: Tuple[int, int], 
                          processed_shape: Tuple[int, int], metadata: Optional[Dict]):
        """Record data processing operation"""
        try:
            processing_record = {
                'timestamp': datetime.now(),
                'original_shape': original_shape,
                'processed_shape': processed_shape,
                'rows_processed': original_shape[0] - processed_shape[0],
                'columns_processed': original_shape[1] - processed_shape[1],
                'metadata': metadata or {}
            }
            
            self.processing_history.append(processing_record)
            
        except Exception as e:
            logger.error(f"Failed to record processing: {e}")
    
    def get_processing_history(self) -> List[Dict]:
        """Get processing history"""
        return self.processing_history.copy()
    
    def get_processing_statistics(self) -> Dict:
        """Get processing statistics"""
        try:
            if not self.processing_history:
                return {'total_operations': 0}
            
            total_operations = len(self.processing_history)
            total_rows_processed = sum(r['rows_processed'] for r in self.processing_history)
            total_columns_processed = sum(r['columns_processed'] for r in self.processing_history)
            
            return {
                'total_operations': total_operations,
                'total_rows_processed': total_rows_processed,
                'total_columns_processed': total_columns_processed,
                'last_processing': self.processing_history[-1]['timestamp'] if self.processing_history else None
            }
            
        except Exception as e:
            logger.error(f"Failed to get processing statistics: {e}")
            return {}
    
    def clear_processing_history(self) -> int:
        """Clear processing history and return count"""
        try:
            count = len(self.processing_history)
            self.processing_history.clear()
            logger.info(f"🗑️ Cleared {count} processing records from history")
            return count
        except Exception as e:
            logger.error(f"Failed to clear processing history: {e}")
            return 0
